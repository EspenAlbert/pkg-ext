"""Release commands: release_notes."""

import logging
from pathlib import Path

import typer
from zero_3rdparty.file_utils import ensure_parents_write_text

from pkg_ext._internal.changelog import ReleaseAction, parse_changelog_actions
from pkg_ext._internal.changelog.write_changelog_md import read_changelog_section
from pkg_ext._internal.settings import PkgSettings

logger = logging.getLogger(__name__)


def find_release_action(changelog_dir: Path, version: str) -> ReleaseAction:
    for changelog_action in parse_changelog_actions(changelog_dir):
        if isinstance(changelog_action, ReleaseAction) and changelog_action.name == version:
            pr = changelog_action.pr
            assert pr, f"found changelog action: {changelog_action} but pr missing"
            return changelog_action
    raise ValueError(f"couldn't find a release for {version}")


def release_notes(
    ctx: typer.Context,
    tag_name: str = typer.Option(..., "--tag", help="tag to find release notes for"),
):
    settings: PkgSettings = ctx.obj
    version = tag_name.removeprefix(settings.tag_prefix)
    action = find_release_action(settings.changelog_dir, version)
    content = read_changelog_section(
        settings.changelog_md.read_text(),
        old_version=action.old_version,
        new_version=action.name,
    )
    output_file = settings.repo_root / f"dist/{tag_name}.changelog.md"
    ensure_parents_write_text(output_file, content)
