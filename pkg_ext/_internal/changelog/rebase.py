import logging
import re
from pathlib import Path

from ask_shell._internal.interactive import ChoiceTyped, select_dict, select_list_choice
from zero_3rdparty.enum_utils import StrEnum

from pkg_ext._internal.changelog.actions import FixAction, dump_changelog_actions, parse_changelog_file_path
from pkg_ext._internal.git_usage.state import GitCommit

logger = logging.getLogger(__name__)

_SHORT_SHA_PATTERN = re.compile(r"(?P<key>short_sha:\s*)(?P<sha>[0-9a-f]{6})")


def find_stale_shas(fix_actions: list[FixAction], current_commits: list[GitCommit]) -> list[FixAction]:
    current_shas = {c.sha for c in current_commits}
    return [a for a in fix_actions if a.short_sha not in current_shas]


def match_by_message(stale_action: FixAction, current_commits: list[GitCommit]) -> GitCommit | None:
    matches = [c for c in current_commits if c.message == stale_action.message]
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]
    return min(matches, key=lambda c: abs((c.ts - stale_action.ts).total_seconds()))


def build_sha_remap(
    stale_actions: list[FixAction], current_commits: list[GitCommit]
) -> tuple[dict[str, str], list[FixAction]]:
    remap: dict[str, str] = {}
    unmatched: list[FixAction] = []
    for action in stale_actions:
        if commit := match_by_message(action, current_commits):
            remap[action.short_sha] = commit.sha
        else:
            unmatched.append(action)
    return remap, unmatched


def apply_remap_to_file(path: Path, remap: dict[str, str]) -> bool:
    text = path.read_text()
    original = text
    for old_sha, new_sha in remap.items():
        text = _SHORT_SHA_PATTERN.sub(
            lambda m: f"{m.group('key')}{new_sha}" if m.group("sha") == old_sha else m.group(0),
            text,
        )
    if text == original:
        return False
    path.write_text(text)
    return True


def remove_actions_from_file(path: Path, shas_to_remove: set[str]) -> None:
    actions = parse_changelog_file_path(path)
    remaining = [a for a in actions if not (isinstance(a, FixAction) and a.short_sha in shas_to_remove)]
    if remaining:
        dump_changelog_actions(path, remaining)
    else:
        path.unlink(missing_ok=True)


class UnmatchedResolution(StrEnum):
    PICK_COMMIT = "pick_commit"
    REMOVE_ENTRY = "remove_entry"
    KEEP_STALE = "keep_stale"


def prompt_unmatched_fix(stale_action: FixAction, current_commits: list[GitCommit]) -> tuple[UnmatchedResolution, str]:
    prompt = f"Stale SHA {stale_action.short_sha}: {stale_action.message} (group={stale_action.name})"
    resolution = select_dict(
        prompt,
        {r: r for r in list(UnmatchedResolution)},
        default=UnmatchedResolution.KEEP_STALE,
    )
    if resolution == UnmatchedResolution.PICK_COMMIT:
        choices = [ChoiceTyped(name=f"{c.sha} {c.message}", value=c.sha) for c in sorted(current_commits, reverse=True)]
        new_sha = select_list_choice("Pick replacement commit:", choices)
        return UnmatchedResolution.PICK_COMMIT, new_sha
    return resolution, ""
