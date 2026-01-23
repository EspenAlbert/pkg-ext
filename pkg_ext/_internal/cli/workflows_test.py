from datetime import UTC, datetime

import pytest

from pkg_ext._internal.changelog import (
    KeepPrivateAction,
    MakePublicAction,
    dump_changelog_actions,
)
from pkg_ext._internal.cli.workflows import reconcile_groups_with_changelog
from pkg_ext._internal.context import RunState, pkg_ctx
from pkg_ext._internal.models import PkgCodeState, PublicGroups, RefSymbol, SymbolType
from pkg_ext._internal.pkg_state import PkgExtState
from pkg_ext._internal.settings import PkgSettings


def _create_ref(name: str, module: str = "_internal.mymodule") -> RefSymbol:
    return RefSymbol(name=name, type=SymbolType.FUNCTION, rel_path=module.replace(".", "/") + ".py")


def _create_ctx(settings: PkgSettings, refs: list[RefSymbol]) -> pkg_ctx:
    settings.changelog_dir.mkdir(parents=True, exist_ok=True)
    code_state = PkgCodeState(
        pkg_import_name=settings.pkg_import_name,
        import_id_refs={ref.local_id: ref for ref in refs},
        files=[],
    )
    groups = PublicGroups(storage_path=settings.public_groups_path)
    tool_state = PkgExtState(
        repo_root=settings.repo_root,
        changelog_dir=settings.changelog_dir,
        pkg_path=settings.pkg_directory,
        groups=groups,
    )
    return pkg_ctx(
        settings=settings,
        tool_state=tool_state,
        code_state=code_state,
        git_changes=None,  # type: ignore[arg-type]
        run_state=RunState(),
        explicit_pr=1,
    )


def test_keep_private_followed_by_make_public_results_in_public(settings: PkgSettings):
    ref = _create_ref("my_func")
    ctx = _create_ctx(settings, [ref])
    actions = [
        KeepPrivateAction(
            name="my_func",
            full_path=ref.local_id,
            ts=datetime(2025, 1, 1, tzinfo=UTC),
        ),
        MakePublicAction(
            name="my_func",
            group="my_group",
            ts=datetime(2025, 1, 2, tzinfo=UTC),
        ),
    ]
    dump_changelog_actions(settings.changelog_dir / "001.yaml", actions)

    reconcile_groups_with_changelog(ctx)

    group = ctx.tool_state.groups.name_to_group.get("my_group")
    assert group is not None
    assert ref.local_id in group.owned_refs


def test_keep_private_removes_ref_from_group(settings: PkgSettings):
    ref = _create_ref("my_func")
    ctx = _create_ctx(settings, [ref])
    ctx.tool_state.groups.get_or_create_group("my_group").owned_refs.add(ref.local_id)

    actions = [
        KeepPrivateAction(
            name="my_func",
            full_path=ref.local_id,
            ts=datetime(2025, 1, 1, tzinfo=UTC),
        ),
    ]
    dump_changelog_actions(settings.changelog_dir / "001.yaml", actions)

    reconcile_groups_with_changelog(ctx)

    group = ctx.tool_state.groups.name_to_group.get("my_group")
    assert group is not None
    assert ref.local_id not in group.owned_refs


def test_make_public_adds_ref_to_group(settings: PkgSettings):
    ref = _create_ref("my_func")
    ctx = _create_ctx(settings, [ref])
    actions = [
        MakePublicAction(
            name="my_func",
            group="my_group",
            ts=datetime(2025, 1, 1, tzinfo=UTC),
        ),
    ]
    dump_changelog_actions(settings.changelog_dir / "001.yaml", actions)

    reconcile_groups_with_changelog(ctx)

    group = ctx.tool_state.groups.name_to_group.get("my_group")
    assert group is not None
    assert ref.local_id in group.owned_refs
    assert ref.module_path in group.owned_modules


def test_make_public_then_keep_private_raises_error(settings: PkgSettings):
    ref = _create_ref("my_func")
    ctx = _create_ctx(settings, [ref])
    actions = [
        MakePublicAction(
            name="my_func",
            group="my_group",
            ts=datetime(2025, 1, 1, tzinfo=UTC),
        ),
        KeepPrivateAction(
            name="my_func",
            full_path=ref.local_id,
            ts=datetime(2025, 1, 2, tzinfo=UTC),
        ),
    ]
    dump_changelog_actions(settings.changelog_dir / "001.yaml", actions)

    with pytest.raises(AssertionError, match="Use DeleteAction to remove a public symbol"):
        reconcile_groups_with_changelog(ctx)
