from datetime import UTC, datetime

from pkg_ext._internal.changelog import DeleteAction, KeepPrivateAction, MakePublicAction
from pkg_ext._internal.models import PublicGroups, RefSymbol, SymbolType
from pkg_ext._internal.pkg_state import PkgExtState


def _create_ref(name: str, module: str = "_internal.mymodule") -> RefSymbol:
    return RefSymbol(name=name, type=SymbolType.FUNCTION, rel_path=module.replace(".", "/") + ".py")


def _create_state(tmp_path) -> PkgExtState:
    (tmp_path / "changelog").mkdir()
    (tmp_path / "pkg").mkdir()
    return PkgExtState(
        repo_root=tmp_path,
        changelog_dir=tmp_path / "changelog",
        pkg_path=tmp_path / "pkg",
        groups=PublicGroups(),
    )


def test_make_public_adds_to_owned_refs(tmp_path):
    ref = _create_ref("my_func")
    state = _create_state(tmp_path)
    action = MakePublicAction(
        name="my_func", group="my_group", full_path=ref.local_id, ts=datetime(2025, 1, 1, tzinfo=UTC)
    )
    state.update_state(action)

    group = state.groups.name_to_group.get("my_group")
    assert group is not None
    assert ref.local_id in group.owned_refs
    assert ref.module_path in group.owned_modules


def test_keep_private_removes_from_owned_refs(tmp_path):
    ref = _create_ref("my_func")
    state = _create_state(tmp_path)
    state.groups.get_or_create_group("my_group").owned_refs.add(ref.local_id)

    action = KeepPrivateAction(name="my_func", full_path=ref.local_id, ts=datetime(2025, 1, 1, tzinfo=UTC))
    state.update_state(action)

    group = state.groups.name_to_group.get("my_group")
    assert group is not None
    assert ref.local_id not in group.owned_refs


def test_delete_removes_from_owned_refs(tmp_path):
    ref = _create_ref("my_func")
    state = _create_state(tmp_path)

    make_public = MakePublicAction(
        name="my_func", group="my_group", full_path=ref.local_id, ts=datetime(2025, 1, 1, tzinfo=UTC)
    )
    state.update_state(make_public)

    delete = DeleteAction(name="my_func", group="my_group", ts=datetime(2025, 1, 2, tzinfo=UTC))
    state.update_state(delete)

    group = state.groups.name_to_group.get("my_group")
    assert group is not None
    assert ref.local_id not in group.owned_refs


def test_keep_private_then_make_public_stays_public(tmp_path):
    ref = _create_ref("my_func")
    state = _create_state(tmp_path)

    keep_private = KeepPrivateAction(name="my_func", full_path=ref.local_id, ts=datetime(2025, 1, 1, tzinfo=UTC))
    make_public = MakePublicAction(
        name="my_func", group="my_group", full_path=ref.local_id, ts=datetime(2025, 1, 2, tzinfo=UTC)
    )

    state.update_state(keep_private)
    state.update_state(make_public)

    group = state.groups.name_to_group.get("my_group")
    assert group is not None
    assert ref.local_id in group.owned_refs


def test_make_public_then_keep_private_removes(tmp_path):
    ref = _create_ref("my_func")
    state = _create_state(tmp_path)

    make_public = MakePublicAction(
        name="my_func", group="my_group", full_path=ref.local_id, ts=datetime(2025, 1, 1, tzinfo=UTC)
    )
    keep_private = KeepPrivateAction(name="my_func", full_path=ref.local_id, ts=datetime(2025, 1, 2, tzinfo=UTC))

    state.update_state(make_public)
    state.update_state(keep_private)

    group = state.groups.name_to_group.get("my_group")
    assert group is not None
    assert ref.local_id not in group.owned_refs
