from datetime import UTC, datetime
from unittest.mock import patch

from ask_shell._internal.interactive import select_dict, select_list_choice

from pkg_ext._internal.changelog.actions import FixAction, KeepPrivateAction
from pkg_ext._internal.changelog.rebase import (
    UnmatchedResolution,
    apply_remap_to_actions,
    build_sha_remap,
    find_stale_shas,
    match_by_message,
    prompt_unmatched_fix,
    remove_actions_by_sha,
)
from pkg_ext._internal.git_usage.state import GitCommit


def _commit(sha: str, message: str, ts: datetime | None = None) -> GitCommit:
    return GitCommit(
        sha=sha,
        message=message,
        ts=ts or datetime(2025, 1, 1, tzinfo=UTC),
        author="test",
        file_changes=set(),
    )


def _fix(sha: str, message: str, ts: datetime | None = None, ignored: bool = False) -> FixAction:
    return FixAction(
        short_sha=sha,
        message=message,
        name="group1",
        ts=ts or datetime(2025, 1, 1, tzinfo=UTC),
        author="test",
        ignored=ignored,
    )


def test_find_stale_shas():
    commits = [_commit("aaa111", "fix: A"), _commit("bbb222", "fix: B")]
    actions = [_fix("aaa111", "fix: A"), _fix("ccc333", "fix: C")]
    stale = find_stale_shas(actions, commits)
    assert len(stale) == 1
    assert stale[0].short_sha == "ccc333"


def test_find_stale_shas_none_stale():
    commits = [_commit("aaa111", "fix: A")]
    assert not find_stale_shas([_fix("aaa111", "fix: A")], commits)


def test_match_by_message_exact():
    commit = _commit("new111", "fix: something")
    assert match_by_message(_fix("old111", "fix: something"), [commit]) == commit


def test_match_by_message_no_match():
    assert match_by_message(_fix("old111", "fix: X"), [_commit("new111", "fix: Y")]) is None


def test_match_by_message_prefers_closest_ts():
    ts_early = datetime(2025, 1, 1, tzinfo=UTC)
    ts_mid = datetime(2025, 6, 1, tzinfo=UTC)
    ts_late = datetime(2025, 12, 1, tzinfo=UTC)
    action = _fix("old111", "fix: dup", ts=ts_mid)
    c_early = _commit("aaa111", "fix: dup", ts=ts_early)
    c_late = _commit("ccc333", "fix: dup", ts=ts_late)
    assert match_by_message(action, [c_early, c_late]) == c_early


def test_build_sha_remap():
    commits = [_commit("new111", "fix: A"), _commit("new222", "fix: B")]
    stale = [_fix("old111", "fix: A"), _fix("old222", "fix: missing")]
    remap, unmatched = build_sha_remap(stale, commits)
    assert remap == {"old111": "new111"}
    assert len(unmatched) == 1
    assert unmatched[0].short_sha == "old222"


def test_apply_remap_to_actions():
    actions = [_fix("aaa111", "fix: A"), _fix("bbb222", "fix: B")]
    count = apply_remap_to_actions(actions, {"aaa111": "ccc333"})
    assert count == 1
    assert actions[0].short_sha == "ccc333"
    assert actions[1].short_sha == "bbb222"


def test_apply_remap_to_actions_skips_non_fix():
    keep_private = KeepPrivateAction(name="some_func", full_path="_internal.mod.some_func")
    actions = [keep_private, _fix("aaa111", "fix: A")]
    count = apply_remap_to_actions(actions, {"aaa111": "bbb222"})
    assert count == 1
    assert actions[1].short_sha == "bbb222"


def test_remove_actions_by_sha():
    actions = [_fix("aaa111", "fix: keep"), _fix("bbb222", "fix: remove")]
    result = remove_actions_by_sha(actions, {"bbb222"})
    assert len(result) == 1
    assert isinstance(result[0], FixAction)
    assert result[0].short_sha == "aaa111"


def test_remove_actions_by_sha_keeps_non_fix():
    keep_private = KeepPrivateAction(name="some_func", full_path="_internal.mod.some_func")
    actions = [keep_private, _fix("aaa111", "fix: remove")]
    result = remove_actions_by_sha(actions, {"aaa111"})
    assert len(result) == 1
    assert result[0] is keep_private


def test_prompt_unmatched_fix_pick():
    module_name = prompt_unmatched_fix.__module__
    commits = [_commit("new111", "fix: A")]
    action = _fix("old111", "fix: gone")
    with (
        patch(f"{module_name}.{select_dict.__name__}", return_value=UnmatchedResolution.PICK_COMMIT) as _sd,
        patch(f"{module_name}.{select_list_choice.__name__}", return_value="new111") as _slc,
    ):
        resolution, sha = prompt_unmatched_fix(action, commits)
    assert resolution == UnmatchedResolution.PICK_COMMIT
    assert sha == "new111"


def test_prompt_unmatched_fix_remove():
    module_name = prompt_unmatched_fix.__module__
    action = _fix("old111", "fix: gone")
    with patch(f"{module_name}.{select_dict.__name__}", return_value=UnmatchedResolution.REMOVE_ENTRY):
        resolution, sha = prompt_unmatched_fix(action, [])
    assert resolution == UnmatchedResolution.REMOVE_ENTRY
    assert sha == ""
