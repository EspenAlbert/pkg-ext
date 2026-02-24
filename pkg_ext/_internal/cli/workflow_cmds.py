"""Git workflow commands: pre_change, pre_commit, post_merge, change_base."""

import logging
from pathlib import Path

import typer
from git import InvalidGitRepositoryError, Repo

from pkg_ext._internal.changelog import changelog_filepath, parse_changelog_actions
from pkg_ext._internal.changelog.change_base import (
    consolidate_changelog_files,
    find_changelog_files_in_diff,
    find_foreign_changelog_files,
    validate_no_foreign_changelog,
)
from pkg_ext._internal.cli.changelog_cmds import _create_chore_action
from pkg_ext._internal.cli.options import (
    option_full,
    option_git_changes_since,
    option_group,
    option_keep_private,
    option_pr,
    option_push,
    option_skip_clean,
    option_skip_dirty_check,
    option_skip_docs,
    option_skip_fix_commits,
    option_skip_open_in_editor,
)
from pkg_ext._internal.cli.workflows import (
    GenerateApiInput,
    clean_old_entries,
    create_ctx,
    create_release_action,
    create_stability_ctx,
    generate_api_workflow,
    post_merge_commit_workflow,
    run_api_diff,
    sync_files,
    update_changelog_entries,
    write_api_dump,
)
from pkg_ext._internal.config import load_project_config
from pkg_ext._internal.generation import docs, docs_mkdocs
from pkg_ext._internal.git_usage import GitSince, find_pr_info_or_none, head_merge_pr
from pkg_ext._internal.models import PublicGroups
from pkg_ext._internal.settings import PkgSettings
from pkg_ext._internal.version_bump import read_current_version

logger = logging.getLogger(__name__)


def get_generated_file_paths(settings: PkgSettings) -> list[Path]:
    """Return paths of all generated files (relative to repo root)."""
    repo_root = settings.repo_root
    paths = [
        settings.public_groups_path.relative_to(repo_root),
        settings.changelog_md.relative_to(repo_root),
        settings.init_path.relative_to(repo_root),
    ]
    if settings.warnings_file_path.exists():
        paths.append(settings.warnings_file_path.relative_to(repo_root))
    groups = settings.parse_computed_public_groups(PublicGroups)
    for group in groups.groups_no_root:
        group_path = settings.group_module_path(group.name)
        paths.append(group_path.relative_to(repo_root))
    docs_dir = settings.docs_dir
    if docs_dir.exists():
        for md_file in docs_dir.rglob("*.md"):
            paths.append(md_file.relative_to(repo_root))
    return paths


def check_generated_files_dirty(settings: PkgSettings) -> list[str]:
    """Check if generated files are modified (unstaged) or untracked."""
    try:
        repo = Repo(settings.repo_root)
    except InvalidGitRepositoryError:
        logger.debug("Not a git repo, skipping dirty check")
        return []
    generated_paths = {str(p) for p in get_generated_file_paths(settings)}
    modified = [f"{item.a_path} (modified)" for item in repo.index.diff(None) if item.a_path in generated_paths]
    untracked = [f"{path} (untracked)" for path in repo.untracked_files if path in generated_paths]
    return modified + untracked


def generate_docs_for_pkg(
    settings: PkgSettings,
    output_dir: Path | None = None,
    filter_group: str | None = None,
) -> int:
    from pkg_ext._internal import api_dumper

    pkg_ctx = create_stability_ctx(settings)
    groups = settings.parse_computed_public_groups(PublicGroups)
    version = str(read_current_version(pkg_ctx))
    refs = {ref.local_id: ref for ref in pkg_ctx.code_state.import_id_refs.values()}
    api_dump = api_dumper.dump_public_api(groups, refs, settings.pkg_import_name, version)
    config = load_project_config(settings.state_dir)
    changelog_actions = parse_changelog_actions(settings.changelog_dir)
    docs_dir = output_dir or settings.docs_dir

    output = docs.generate_docs(
        api_dump=api_dump,
        config=config,
        changelog_actions=changelog_actions,
        docs_dir=docs_dir,
        pkg_src_dir=settings.repo_root,
    )
    if filter_group:
        dir_name = docs.group_dir_name(api_dump.get_group(filter_group))
        output.path_contents = {k: v for k, v in output.path_contents.items() if k.startswith(dir_name)}
    docs_mkdocs.copy_readme_as_index(
        settings.state_dir,
        docs_dir,
        settings.pkg_import_name,
        settings.repo_url,
        settings.default_branch,
    )
    count = docs_mkdocs.write_docs_files(output, docs_dir)
    complex_symbols = docs_mkdocs.extract_complex_symbols(output, api_dump.groups)
    nav = docs_mkdocs.generate_mkdocs_nav(api_dump, settings.pkg_import_name, complex_symbols)
    docs_mkdocs.write_mkdocs_yml(settings.mkdocs_yml, settings.pkg_import_name, nav, config.mkdocs_skip_sections)
    return count


def post_merge(
    ctx: typer.Context,
    explicit_pr: int = option_pr,
    push: bool = option_push,
    skip_clean_old_entries: bool = option_skip_clean,
    force_reason: str = typer.Option(
        "",
        "--force-reason",
        help="Force release with this reason (creates ChoreAction if no changelog entries)",
    ),
):
    settings: PkgSettings = ctx.obj
    settings.force_bot()
    pr = explicit_pr or head_merge_pr(Path(settings.repo_root))
    logger.info(f"pr found: {pr}")
    api_input = GenerateApiInput(
        settings=settings,
        git_changes_since=GitSince.NO_GIT_CHANGES,
        bump_version=True,
        create_tag=True,
        push=push,
        explicit_pr=pr,
    )
    pkg_ctx = create_ctx(api_input)
    sync_files(api_input, pkg_ctx)
    write_api_dump(settings, dev_mode=False)

    has_version_bump = pkg_ctx.run_state.old_version != pkg_ctx.run_state.new_version
    if not has_version_bump:
        if force_reason:
            _create_chore_action(settings, pr, force_reason)
            pkg_ctx = create_ctx(api_input)
            sync_files(api_input, pkg_ctx)
            logger.info(f"Forced release with chore: {force_reason}")
        else:
            logger.info(
                f"No changelog entries for PR {pr}, skipping release "
                f"(version stays at {pkg_ctx.run_state.old_version}). "
                "Use --force-reason to release anyway."
            )
            count = generate_docs_for_pkg(settings)
            logger.info(f"Regenerated {count} doc files (no release)")
            return

    # Create ReleaseAction first so docs generation has correct since_version
    create_release_action(
        changelog_dir_path=pkg_ctx.settings.changelog_dir,
        pr_number=pr,
        old_version=pkg_ctx.run_state.old_version,
        new_version=pkg_ctx.run_state.new_version,
    )
    count = generate_docs_for_pkg(settings)
    logger.info(f"Regenerated {count} doc files with release version")
    # Now commit with docs that have correct since_version
    post_merge_commit_workflow(
        repo_path=settings.repo_root,
        tag_prefix=settings.tag_prefix,
        new_version=pkg_ctx.run_state.new_version,
        push=push,
    )
    if not skip_clean_old_entries:
        clean_old_entries(settings)


def _dump_diff_and_docs(settings: PkgSettings, skip_docs: bool) -> None:
    """Write API dump, run diff (which may add changelog entries), then regenerate docs."""
    write_api_dump(settings, dev_mode=True)
    pr_info = find_pr_info_or_none(settings.repo_root)
    run_api_diff(settings, pr_info.pr_number if pr_info else 0)
    if skip_docs:
        logger.info("Skipped docs regeneration")
        return
    count = generate_docs_for_pkg(settings)
    logger.info(f"Regenerated {count} doc files")


def pre_change(
    ctx: typer.Context,
    group: str | None = option_group,
    git_changes_since: GitSince = option_git_changes_since,
    skip_fix_commits: bool = option_skip_fix_commits,
    full: bool = option_full,
    skip_docs: bool = option_skip_docs,
    skip_open_in_editor: bool | None = option_skip_open_in_editor,
    keep_private: bool = option_keep_private,
):
    """Handle new symbols, update changelog, optionally sync files and docs."""
    settings: PkgSettings = ctx.obj
    if skip_open_in_editor is not None:
        settings.skip_open_in_editor = skip_open_in_editor
    if keep_private:
        settings.keep_private = True
    api_input = GenerateApiInput(
        settings=settings,
        git_changes_since=git_changes_since,
        bump_version=False,
        create_tag=False,
        push=False,
        skip_fix_commits=skip_fix_commits,
    )
    pkg_ctx = update_changelog_entries(api_input)
    if not pkg_ctx:
        return
    if not full:
        return
    settings.dev_mode = True
    sync_files(api_input, pkg_ctx)
    _dump_diff_and_docs(settings, skip_docs)


def pre_commit(
    ctx: typer.Context,
    git_changes_since: GitSince = option_git_changes_since,
    skip_docs: bool = option_skip_docs,
    skip_dirty_check: bool = option_skip_dirty_check,
):
    """Update changelog and regenerate docs (bot mode, writes to -dev files)."""
    settings: PkgSettings = ctx.obj
    settings.force_bot()
    settings.dev_mode = True

    api_input = GenerateApiInput(
        settings=settings,
        git_changes_since=git_changes_since,
        bump_version=False,
        create_tag=False,
        push=False,
    )
    if not generate_api_workflow(api_input):
        raise typer.Exit(1)

    _dump_diff_and_docs(settings, skip_docs)

    if pr_info := find_pr_info_or_none(settings.repo_root):
        foreign = validate_no_foreign_changelog(
            settings.repo_root, settings.changelog_dir, pr_info.base_ref_name, pr_info.pr_number
        )
        if foreign:
            stems = ", ".join(f.stem for f in foreign)
            logger.error(
                f"Found changelog files for other PRs: {stems}. "
                "This usually means the PR base was changed. "
                f"Run: pkg-ext change-base --new-base {pr_info.base_ref_name}"
            )
            raise typer.Exit(1)

    if skip_dirty_check:
        return
    if dirty_files := check_generated_files_dirty(settings):
        logger.error("Generated files have unstaged changes:")
        for f in dirty_files:
            logger.error(f"  {f}")
        logger.error("Run `git add` on these files before committing.")
        raise typer.Exit(1)


def change_base(
    ctx: typer.Context,
    new_base: str = typer.Option(..., "--new-base", help="The new base branch (e.g., 'main')"),
    pr_number: int = option_pr,
):
    """Consolidate changelog files from closed PRs after re-targeting a stacked PR."""
    settings: PkgSettings = ctx.obj
    if not pr_number:
        pr_info = find_pr_info_or_none(settings.repo_root)
        if not pr_info:
            logger.error("No active PR found. Use --pr to specify the PR number.")
            raise typer.Exit(1)
        pr_number = pr_info.pr_number

    diff_files = find_changelog_files_in_diff(settings.repo_root, settings.changelog_dir, new_base)
    foreign = find_foreign_changelog_files(diff_files, pr_number)
    if not foreign:
        logger.info("No foreign changelog files, nothing to consolidate")
        return

    target = changelog_filepath(settings.changelog_dir, pr_number)
    consolidate_changelog_files(target, foreign)
    stems = ", ".join(f.stem for f in foreign)
    logger.info(f"Consolidated {len(foreign)} changelog files into {target.name}: {stems}")
