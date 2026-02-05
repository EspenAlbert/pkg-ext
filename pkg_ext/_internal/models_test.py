from datetime import UTC, datetime
from typing import Callable

import pytest
from model_lib import parse

from pkg_ext._internal.changelog.actions import (
    GroupModuleAction,
    MakePublicAction,
    changelog_filepath,
    dump_changelog_actions,
)
from pkg_ext._internal.changelog.parser import parse_changelog
from pkg_ext._internal.models import (
    PublicGroups,
    RefSymbol,
    SymbolType,
)
from pkg_ext._internal.settings import PkgSettings


@pytest.fixture()
def _public_groups(tmp_path) -> PublicGroups:
    path = tmp_path / PkgSettings.PUBLIC_GROUPS_STORAGE_FILENAME
    return PublicGroups(storage_path=path)


@pytest.fixture()
def _public_group_check(_public_groups, file_regression_testdata) -> Callable[[], PublicGroups]:
    def check():
        file_regression_testdata(_public_groups.storage_path.read_text(), "yaml")
        return parse.parse_model(_public_groups.storage_path, t=PublicGroups)

    return check


def test_public_groups_dumping_after_new_ref_symbol(_public_groups, _public_group_check):
    ref = RefSymbol(name="my_func", type=SymbolType.FUNCTION, rel_path="my_module")
    _public_groups.add_ref(ref, "test")
    groups = _public_group_check()
    test_group = groups.matching_group(ref)
    assert test_group.name == "test"
    assert test_group.owned_refs == {"my_module.my_func"}


def test_public_groups_add_to_existing_group(_public_groups, _public_group_check):
    ref = RefSymbol(name="my_func", type=SymbolType.FUNCTION, rel_path="my_module")
    ref2 = RefSymbol(name="my_func2", type=SymbolType.FUNCTION, rel_path="my_module")
    _public_groups.add_ref(ref, "test")
    _public_groups.add_ref(ref2, "test")
    assert len(_public_groups.groups_no_root) == 1
    _public_group_check()


def test_tool_state_update_state(settings):
    actions = [
        GroupModuleAction(
            name="git_inferred",
            ts=datetime(2025, 8, 25, 17, 37, 2, tzinfo=UTC),
            author="UNSET",
            module_path="inferred",
        ),
        MakePublicAction(
            name="inferred",
            group="git_inferred",
            full_path="inferred.inferred",
            ts=datetime(2025, 8, 25, 17, 37, 2, tzinfo=UTC),
            author="UNSET",
            details="created in inferred.py",
        ),
    ]
    dump_changelog_actions(changelog_filepath(settings.changelog_dir, 1), actions)
    state, _ = parse_changelog(settings)
    assert [group.name for group in state.groups.groups_no_root] == ["git_inferred"]


def _ref(name: str, rel_path: str) -> RefSymbol:
    return RefSymbol(name=name, type=SymbolType.FUNCTION, rel_path=rel_path)


def _refs_dict(*refs: RefSymbol) -> dict[str, RefSymbol]:
    return {f"pkg.{r.local_id}": r for r in refs}


def test_reconcile_moved_refs_no_changes(_public_groups):
    _public_groups.get_or_create_group("my_group").owned_refs.add("_internal.models.MyClass")
    refs = _refs_dict(_ref("MyClass", "_internal/models"))

    assert _public_groups.reconcile_moved_refs(refs) == 0
    assert "_internal.models.MyClass" in _public_groups.name_to_group["my_group"].owned_refs


def test_reconcile_moved_refs_updates_moved_symbol(_public_groups, caplog):
    group = _public_groups.get_or_create_group("my_group")
    group.owned_refs.add("_internal.old_module.MyClass")
    group.owned_modules.add("_internal.old_module")
    refs = _refs_dict(_ref("MyClass", "_internal/new_module"))

    assert _public_groups.reconcile_moved_refs(refs) == 1
    assert "_internal.new_module.MyClass" in group.owned_refs
    assert "_internal.old_module.MyClass" not in group.owned_refs
    assert "Symbol moved:" in caplog.text


def test_reconcile_moved_refs_keeps_deleted_symbol(_public_groups):
    group = _public_groups.get_or_create_group("my_group")
    group.owned_refs.add("_internal.models.DeletedClass")

    assert _public_groups.reconcile_moved_refs({}) == 0
    assert "_internal.models.DeletedClass" in group.owned_refs


def test_reconcile_moved_refs_multiple_groups(_public_groups, caplog):
    group1 = _public_groups.get_or_create_group("group1")
    group2 = _public_groups.get_or_create_group("group2")
    group1.owned_refs.add("_internal.old.Func1")
    group2.owned_refs.add("_internal.old.Func2")
    refs = _refs_dict(_ref("Func1", "_internal/new"), _ref("Func2", "_internal/new"))

    assert _public_groups.reconcile_moved_refs(refs) == 2
    assert "_internal.new.Func1" in group1.owned_refs
    assert "_internal.new.Func2" in group2.owned_refs


def test_reconcile_disambiguates_via_owned_modules(_public_groups):
    group = _public_groups.get_or_create_group("my_group")
    group.owned_refs.add("_internal.old.Parser")
    group.owned_modules.add("_internal.models")
    refs = _refs_dict(_ref("Parser", "_internal/models"), _ref("Parser", "_internal/utils"))

    assert _public_groups.reconcile_moved_refs(refs) == 1
    assert "_internal.models.Parser" in group.owned_refs


def test_reconcile_disambiguates_via_other_groups(_public_groups):
    group1 = _public_groups.get_or_create_group("group1")
    group2 = _public_groups.get_or_create_group("group2")
    group1.owned_refs.add("_internal.old.Parser")
    group2.owned_refs.add("_internal.utils.Parser")  # already owned by group2
    refs = _refs_dict(_ref("Parser", "_internal/models"), _ref("Parser", "_internal/utils"))

    assert _public_groups.reconcile_moved_refs(refs) == 1
    assert "_internal.models.Parser" in group1.owned_refs


def test_reconcile_logs_when_ambiguous(_public_groups, caplog):
    group = _public_groups.get_or_create_group("my_group")
    group.owned_refs.add("_internal.old.Parser")
    refs = _refs_dict(_ref("Parser", "_internal/a"), _ref("Parser", "_internal/b"))

    assert _public_groups.reconcile_moved_refs(refs) == 0
    assert "_internal.old.Parser" in group.owned_refs  # kept stale
    assert "Cannot resolve" in caplog.text
