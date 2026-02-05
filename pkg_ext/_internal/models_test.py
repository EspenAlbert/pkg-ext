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


def test_reconcile_moved_refs_no_changes(_public_groups):
    """When all refs are at their expected paths, no changes are made."""
    _public_groups.get_or_create_group("my_group").owned_refs.add("_internal.models.MyClass")
    name_to_current = {"MyClass": "_internal.models.MyClass"}

    updated = _public_groups.reconcile_moved_refs(name_to_current)

    assert updated == 0
    assert "_internal.models.MyClass" in _public_groups.name_to_group["my_group"].owned_refs


def test_reconcile_moved_refs_updates_moved_symbol(_public_groups, caplog):
    """When a symbol moves to a different module, the ref is updated but owned_modules unchanged."""
    group = _public_groups.get_or_create_group("my_group")
    group.owned_refs.add("_internal.old_module.MyClass")
    group.owned_modules.add("_internal.old_module")
    name_to_current = {"MyClass": "_internal.new_module.MyClass"}

    updated = _public_groups.reconcile_moved_refs(name_to_current)

    assert updated == 1
    assert "_internal.new_module.MyClass" in group.owned_refs
    assert "_internal.old_module.MyClass" not in group.owned_refs
    # owned_modules NOT updated - it's for routing new symbols, not tracking moved refs
    assert "_internal.new_module" not in group.owned_modules
    assert "Symbol moved:" in caplog.text


def test_reconcile_moved_refs_keeps_deleted_symbol(_public_groups):
    """When a symbol is deleted (not in code), the ref is kept for removed_refs flow."""
    group = _public_groups.get_or_create_group("my_group")
    group.owned_refs.add("_internal.models.DeletedClass")
    name_to_current = {}  # Symbol not in code

    updated = _public_groups.reconcile_moved_refs(name_to_current)

    assert updated == 0
    assert "_internal.models.DeletedClass" in group.owned_refs


def test_reconcile_moved_refs_multiple_groups(_public_groups, caplog):
    """Reconciliation works across multiple groups."""
    group1 = _public_groups.get_or_create_group("group1")
    group2 = _public_groups.get_or_create_group("group2")
    group1.owned_refs.add("_internal.old.Func1")
    group2.owned_refs.add("_internal.old.Func2")
    name_to_current = {
        "Func1": "_internal.new.Func1",
        "Func2": "_internal.new.Func2",
    }

    updated = _public_groups.reconcile_moved_refs(name_to_current)

    assert updated == 2
    assert "_internal.new.Func1" in group1.owned_refs
    assert "_internal.new.Func2" in group2.owned_refs
