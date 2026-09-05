from pathlib import Path
from unittest.mock import patch

import pytest
from zero_3rdparty.file_utils import ensure_parents_write_text

from pkg_ext._internal.changelog.actions import KeepPrivateAction
from pkg_ext._internal.config import ExposeMode
from pkg_ext._internal.context import pkg_ctx
from pkg_ext._internal.git_usage import GitChanges
from pkg_ext._internal.models import PkgCodeState, RefSymbol, SymbolType
from pkg_ext._internal.models.py_files import PkgSrcFile
from pkg_ext._internal.pkg_state import PkgExtState
from pkg_ext._internal.reference_handling import added
from pkg_ext._internal.settings import PkgSettings


def _ref(name: str, rel_path: str = "cmds.py") -> RefSymbol:
    return RefSymbol(name=name, type=SymbolType.FUNCTION, rel_path=rel_path)


def _code_state(*refs: RefSymbol) -> PkgCodeState:
    import_id_refs = {f"pkg.{r.local_id}": r for r in refs}
    seen_paths: set[str] = set()
    unique_files: list[PkgSrcFile] = []
    for r in refs:
        if r.rel_path in seen_paths:
            continue
        seen_paths.add(r.rel_path)
        unique_files.append(
            PkgSrcFile(path=Path(f"/tmp/{r.rel_path}"), relative_path=r.rel_path, pkg_import_name="pkg")
        )
    return PkgCodeState(pkg_import_name="pkg", import_id_refs=import_id_refs, files=unique_files)


def _ctx(
    tmp_path: Path,
    expose_mode: ExposeMode,
    *,
    keep_private: bool = False,
    grouped: bool = True,
) -> pkg_ctx:
    ensure_parents_write_text(tmp_path / "pkg" / "__init__.py", "")
    changelog_dir = tmp_path / ".changelog"
    changelog_dir.mkdir()
    pkg_path = tmp_path / "pkg"
    settings = PkgSettings(
        repo_root=tmp_path,
        pkg_directory=pkg_path,
        skip_open_in_editor=True,
        expose_mode=expose_mode,
        keep_private=keep_private,
    )
    tool_state = PkgExtState(repo_root=tmp_path, changelog_dir=changelog_dir, pkg_path=pkg_path)
    if grouped:
        tool_state.groups.add_module("cli", "cmds")
    cli_ref = _ref("cli_cmd")
    helper_ref = _ref("helper")
    code_state = _code_state(cli_ref, helper_ref)
    return pkg_ctx(
        settings=settings,
        tool_state=tool_state,
        code_state=code_state,
        git_changes=GitChanges.empty(),
    )


def _action_types(ctx: pkg_ctx) -> list[str]:
    return [action.type for action in ctx._actions]


@pytest.fixture
def expose_ctx(tmp_path: Path) -> pkg_ctx:
    return _ctx(tmp_path, ExposeMode.prompt)


def test_prompt_mode_prompts_for_non_cli(expose_ctx: pkg_ctx):
    with (
        patch.object(added, "_is_cli_command_ref", side_effect=lambda _cs, ref: ref.name == "cli_cmd"),
        patch.object(added, "ensure_function_args_exposed", return_value={}),
        patch.object(added, "select_multiple_refs", return_value=[]) as select_refs,
        patch.object(added, "new_task"),
    ):
        added.handle_added_refs(expose_ctx)

    select_refs.assert_called_once()
    assert _action_types(expose_ctx).count("make_public") == 1
    assert _action_types(expose_ctx).count("keep_private") == 1


def test_cli_only_auto_exposes_cli_only(expose_ctx: pkg_ctx):
    expose_ctx.settings.expose_mode = ExposeMode.cli_only
    with (
        patch.object(added, "_is_cli_command_ref", side_effect=lambda _cs, ref: ref.name == "cli_cmd"),
        patch.object(added, "ensure_function_args_exposed", return_value={}),
        patch.object(added, "select_multiple_refs") as select_refs,
        patch.object(added, "new_task"),
    ):
        added.handle_added_refs(expose_ctx)

    select_refs.assert_not_called()
    assert _action_types(expose_ctx) == ["make_public", "keep_private"]


def test_opt_in_keeps_all_private(tmp_path: Path):
    ctx = _ctx(tmp_path, ExposeMode.opt_in)
    with patch.object(added, "_is_cli_command_ref", return_value=True), patch.object(added, "new_task"):
        added.handle_added_refs(ctx)
    assert len(ctx._actions) == 2
    assert all(isinstance(a, KeepPrivateAction) for a in ctx._actions)


def test_keep_private_overrides_cli_only(tmp_path: Path):
    ctx = _ctx(tmp_path, ExposeMode.cli_only, keep_private=True)
    with (
        patch.object(added, "_is_cli_command_ref", return_value=True),
        patch.object(added, "select_multiple_refs") as select_refs,
        patch.object(added, "new_task"),
    ):
        added.handle_added_refs(ctx)
    select_refs.assert_not_called()
    assert all(isinstance(a, KeepPrivateAction) for a in ctx._actions)


def test_cli_only_prompts_for_group_when_ungrouped(tmp_path: Path):
    ctx = _ctx(tmp_path, ExposeMode.cli_only, grouped=False)
    with (
        patch.object(added, "_is_cli_command_ref", side_effect=lambda _cs, ref: ref.name == "cli_cmd"),
        patch.object(added, "ensure_function_args_exposed", return_value={}),
        patch.object(added, "select_group") as select_group,
        patch.object(added, "new_task"),
    ):
        select_group.return_value = ctx.tool_state.groups.get_or_create_group("new_group")
        added.handle_added_refs(ctx)

    select_group.assert_called_once()
    assert _action_types(ctx) == ["group_module", "make_public", "keep_private"]
