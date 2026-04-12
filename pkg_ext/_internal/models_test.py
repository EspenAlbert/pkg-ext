from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

import pytest
from model_lib import parse

from pkg_ext._internal.changelog.actions import (
    GroupModuleAction,
    KeepPrivateAction,
    MakePublicAction,
    changelog_filepath,
    dump_changelog_actions,
)
from pkg_ext._internal.changelog.parser import parse_changelog
from pkg_ext._internal.errors import RefSymbolNotInCodeError
from pkg_ext._internal.models import (
    PkgCodeState,
    PublicGroups,
    RefSymbol,
    SymbolType,
)
from pkg_ext._internal.models.py_files import PkgSrcFile
from pkg_ext._internal.models.ref_state import RefState, RefStateType
from pkg_ext._internal.pkg_state import PkgExtState
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
    assert "_internal.new_module" in group.owned_modules
    assert "_internal.old_module" not in group.owned_modules
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


def _code_state(*refs: RefSymbol) -> PkgCodeState:
    import_id_refs = {f"pkg.{r.local_id}": r for r in refs}
    files = [
        PkgSrcFile(
            path=Path(f"/tmp/{r.rel_path}.py"),
            relative_path=r.rel_path,
            pkg_import_name="pkg",
        )
        for r in refs
    ]
    seen_paths: set[str] = set()
    unique_files = []
    for f in files:
        if f.relative_path not in seen_paths:
            seen_paths.add(f.relative_path)
            unique_files.append(f)
    return PkgCodeState(pkg_import_name="pkg", import_id_refs=import_id_refs, files=unique_files)


def _tool_state(tmp_path: Path) -> PkgExtState:
    changelog_dir = tmp_path / ".changelog"
    changelog_dir.mkdir()
    pkg_path = tmp_path / "pkg"
    pkg_path.mkdir()
    return PkgExtState(repo_root=tmp_path, changelog_dir=changelog_dir, pkg_path=pkg_path)


def test_named_refs_preserves_duplicate_short_names():
    """Two functions named init_cmd in different modules both appear in named_refs."""
    core_ref = _ref("init_cmd", "_internal/core/cmd_init")
    config_ref = _ref("init_cmd", "_internal/config/cmd_config")
    code = _code_state(core_ref, config_ref)

    named = code.named_refs
    assert len(named) == 2
    local_ids = set(named.keys())
    assert "_internal.core.cmd_init.init_cmd" in local_ids
    assert "_internal.config.cmd_config.init_cmd" in local_ids


def test_has_decision_distinguishes_same_name(tmp_path):
    """has_decision for one init_cmd must not block the other."""
    state = _tool_state(tmp_path)
    state.update_state(
        MakePublicAction(name="init_cmd", group="core", full_path="_internal.core.cmd_init.init_cmd", author="test")
    )
    assert state.has_decision("_internal.core.cmd_init.init_cmd")
    assert not state.has_decision("_internal.config.cmd_config.init_cmd")


def test_added_refs_includes_both_same_name(tmp_path):
    """Both init_cmd refs appear as added when neither has a decision."""
    core_ref = _ref("init_cmd", "_internal/core/cmd_init")
    config_ref = _ref("init_cmd", "_internal/config/cmd_config")
    code = _code_state(core_ref, config_ref)
    state = _tool_state(tmp_path)

    added = state.added_refs(code.named_refs)
    assert len(added) == 2


def test_added_refs_filters_only_decided(tmp_path):
    """After deciding one init_cmd, the other still appears as added."""
    core_ref = _ref("init_cmd", "_internal/core/cmd_init")
    config_ref = _ref("init_cmd", "_internal/config/cmd_config")
    code = _code_state(core_ref, config_ref)
    state = _tool_state(tmp_path)
    state.update_state(
        MakePublicAction(name="init_cmd", group="core", full_path="_internal.core.cmd_init.init_cmd", author="test")
    )

    added = state.added_refs(code.named_refs)
    assert len(added) == 1
    assert "_internal.config.cmd_config.init_cmd" in added


def test_keep_private_does_not_shadow_other_same_name(tmp_path):
    """keep_private for one ref must not block the other from appearing as added."""
    core_ref = _ref("init_cmd", "_internal/core/cmd_init")
    config_ref = _ref("init_cmd", "_internal/config/cmd_config")
    code = _code_state(core_ref, config_ref)
    state = _tool_state(tmp_path)
    state.update_state(KeepPrivateAction(name="init_cmd", full_path="_internal.core.cmd_init.init_cmd", author="test"))

    added = state.added_refs(code.named_refs)
    assert len(added) == 1
    assert "_internal.config.cmd_config.init_cmd" in added


def test_ref_symbol_lookup_by_local_id():
    core_ref = _ref("init_cmd", "_internal/core/cmd_init")
    config_ref = _ref("init_cmd", "_internal/config/cmd_config")
    code = _code_state(core_ref, config_ref)

    found = code.ref_symbol("_internal.core.cmd_init.init_cmd")
    assert found.rel_path == "_internal/core/cmd_init"

    found2 = code.ref_symbol("_internal.config.cmd_config.init_cmd")
    assert found2.rel_path == "_internal/config/cmd_config"

    # import_id key lookup (first branch in ref_symbol)
    found3 = code.ref_symbol(f"pkg.{core_ref.local_id}")
    assert found3.rel_path == "_internal/core/cmd_init"

    with pytest.raises(RefSymbolNotInCodeError):
        code.ref_symbol("nonexistent_func")


def test_exposed_refs_keys_by_local_id(tmp_path):
    ref_a = _ref("my_func", "_internal/mod_a")
    code = _code_state(ref_a)
    state = _tool_state(tmp_path)
    state.update_state(
        MakePublicAction(name="my_func", group="grp", full_path="_internal.mod_a.my_func", author="test")
    )
    exposed = state.exposed_refs("grp", code.named_refs)
    assert "_internal.mod_a.my_func" in exposed


def test_exposed_refs_preserves_both_same_name(tmp_path):
    core_ref = _ref("init_cmd", "_internal/core/cmd_init")
    config_ref = _ref("init_cmd", "_internal/config/cmd_config")
    code = _code_state(core_ref, config_ref)
    state = _tool_state(tmp_path)
    state.update_state(
        MakePublicAction(name="init_cmd", group="grp", full_path="_internal.core.cmd_init.init_cmd", author="test")
    )
    state.update_state(
        MakePublicAction(name="init_cmd", group="grp", full_path="_internal.config.cmd_config.init_cmd", author="test")
    )
    exposed = state.exposed_refs("grp", code.named_refs)
    assert len(exposed) == 2
    assert "_internal.core.cmd_init.init_cmd" in exposed
    assert "_internal.config.cmd_config.init_cmd" in exposed


def test_ref_symbol_raises_on_ambiguous_short_name():
    core_ref = _ref("init_cmd", "_internal/core/cmd_init")
    config_ref = _ref("init_cmd", "_internal/config/cmd_config")
    code = _code_state(core_ref, config_ref)

    with pytest.raises(RefSymbolNotInCodeError, match="ambiguous"):
        code.ref_symbol("init_cmd")


def test_ref_symbol_unique_short_name_resolves():
    ref_a = _ref("my_func", "_internal/mod_a")
    code = _code_state(ref_a)
    found = code.ref_symbol("my_func")
    assert found.rel_path == "_internal/mod_a"


def test_code_ref_resolves_via_owned_refs(tmp_path):
    core_ref = _ref("init_cmd", "_internal/core/cmd_init")
    config_ref = _ref("init_cmd", "_internal/config/cmd_config")
    code = _code_state(core_ref, config_ref)
    state = _tool_state(tmp_path)
    state.update_state(
        MakePublicAction(name="init_cmd", group="core", full_path="_internal.core.cmd_init.init_cmd", author="test")
    )
    state.update_state(
        MakePublicAction(
            name="init_cmd", group="config", full_path="_internal.config.cmd_config.init_cmd", author="test"
        )
    )
    result = state.code_ref(code, "core", "init_cmd")
    assert result is not None
    assert result.rel_path == "_internal/core/cmd_init"

    result2 = state.code_ref(code, "config", "init_cmd")
    assert result2 is not None
    assert result2.rel_path == "_internal/config/cmd_config"


def test_removed_refs_fallback_without_group(tmp_path):
    """Legacy ref without group info: short-name fallback keeps it when any same-name ref exists."""
    state = _tool_state(tmp_path)
    state.refs["init_cmd"] = RefState(name="init_cmd", type=RefStateType.EXPOSED)
    config_ref = _ref("init_cmd", "_internal/config/cmd_config")
    code = _code_state(config_ref)

    removed = state.removed_refs(code)
    assert len(removed) == 0


def test_reconcile_with_code_covers_moved_symbol(tmp_path):
    """After a symbol moves, reconcile_with_code prevents re-flagging as new."""
    state = _tool_state(tmp_path)
    state.update_state(
        MakePublicAction(name="check_cmd", group="core", full_path="_internal.core.cmd_check.check_cmd", author="test")
    )
    assert state.has_decision("_internal.core.cmd_check.check_cmd")
    assert not state.has_decision("_internal.check.cmd_check.check_cmd")

    new_ref = _ref("check_cmd", "_internal/check/cmd_check")
    code = _code_state(new_ref)
    state.reconcile_with_code(code.import_id_refs)
    assert state.has_decision("_internal.check.cmd_check.check_cmd")

    added = state.added_refs(code.named_refs)
    assert len(added) == 0


def test_reconcile_with_code_no_move_leaves_decisions_unchanged(tmp_path):
    """When nothing moves, no new decisions are added from owned_refs."""
    state = _tool_state(tmp_path)
    grp = state.groups.get_or_create_group("core")
    grp.owned_refs.add("_internal.core.cmd_init.init_cmd")

    ref = _ref("init_cmd", "_internal/core/cmd_init")
    code = _code_state(ref)
    state.reconcile_with_code(code.import_id_refs)

    assert not state.has_decision("_internal.core.cmd_init.init_cmd")


def test_removed_refs_detects_specific_deletion(tmp_path):
    """When core.init_cmd is deleted but config.init_cmd remains, only core is removed."""
    state = _tool_state(tmp_path)
    state.update_state(
        MakePublicAction(name="init_cmd", group="core", full_path="_internal.core.cmd_init.init_cmd", author="test")
    )
    state.update_state(
        MakePublicAction(
            name="init_cmd", group="config", full_path="_internal.config.cmd_config.init_cmd", author="test"
        )
    )
    # Only config.init_cmd remains in code
    config_ref = _ref("init_cmd", "_internal/config/cmd_config")
    code = _code_state(config_ref)

    removed = state.removed_refs(code)
    assert len(removed) == 1
    group, ref_state = removed[0]
    assert group == "core"
    assert ref_state.name == "init_cmd"
