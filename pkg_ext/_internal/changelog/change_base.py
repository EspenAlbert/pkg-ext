from __future__ import annotations

import logging
from pathlib import Path

from ask_shell._internal._run import run_and_wait

from pkg_ext._internal.changelog.actions import (
    dump_changelog_actions,
    parse_changelog_file_path,
)

logger = logging.getLogger(__name__)


def find_changelog_files_in_diff(repo_path: Path, changelog_dir: Path, base_ref: str) -> list[Path]:
    changelog_dir_rel = changelog_dir.relative_to(repo_path)
    result = run_and_wait(
        f"git diff --name-only {base_ref}...HEAD -- {changelog_dir_rel}",
        cwd=repo_path,
    )
    paths = []
    for line in result.stdout.strip().splitlines():
        if not line.strip():
            continue
        abs_path = repo_path / line.strip()
        if abs_path.exists() and abs_path.suffix == ".yaml":
            paths.append(abs_path)
    return paths


def find_foreign_changelog_files(changelog_files: list[Path], current_pr: int) -> list[Path]:
    return [f for f in changelog_files if f.stem.isdigit() and int(f.stem) != current_pr]


def consolidate_changelog_files(target_path: Path, source_paths: list[Path]) -> Path:
    actions = []
    if target_path.exists():
        actions.extend(parse_changelog_file_path(target_path))
    for source in source_paths:
        if source.exists():
            actions.extend(parse_changelog_file_path(source))
    if actions:
        dump_changelog_actions(target_path, actions)
    for source in source_paths:
        if source.exists():
            source.unlink()
            logger.info(f"Deleted {source.name}")
    return target_path


def validate_no_foreign_changelog(repo_path: Path, changelog_dir: Path, base_ref: str, current_pr: int) -> list[Path]:
    diff_files = find_changelog_files_in_diff(repo_path, changelog_dir, base_ref)
    return find_foreign_changelog_files(diff_files, current_pr)
