from pkg_ext._internal.changelog.actions import (
    ChangelogAction,
    parse_changelog_actions,
    unreleased_make_public_paths,
)
from pkg_ext._internal.models import PkgCodeState, PublicGroups
from pkg_ext._internal.pkg_state import PkgExtState
from pkg_ext._internal.settings import PkgSettings


def parse_changelog(
    settings: PkgSettings, code_state: PkgCodeState | None = None
) -> tuple[PkgExtState, list[ChangelogAction]]:
    changelog_path = settings.changelog_dir
    changelog_path.mkdir(parents=True, exist_ok=True)
    actions = parse_changelog_actions(changelog_path)
    groups = settings.parse_computed_public_groups(PublicGroups)
    disk_owned_refs = {ref for g in groups.groups for ref in g.owned_refs}
    unreleased_full_paths = unreleased_make_public_paths(actions)
    tool_state = PkgExtState(
        repo_root=settings.repo_root,
        changelog_dir=changelog_path,
        pkg_path=settings.pkg_directory,
        groups=groups,
        disk_owned_refs=disk_owned_refs,
        unreleased_full_paths=unreleased_full_paths,
    )
    for action in actions:
        tool_state.update_state(action)
    # Note: Group module tracking is now handled via GroupModuleAction in changelog
    # No extra actions needed - groups are updated when changelog is parsed
    return tool_state, []
