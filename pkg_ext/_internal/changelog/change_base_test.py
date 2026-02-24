from pathlib import Path

from pkg_ext._internal.changelog.actions import (
    ChoreAction,
    MakePublicAction,
    changelog_filepath,
    dump_changelog_actions,
    parse_changelog_file_path,
)
from pkg_ext._internal.changelog.change_base import (
    consolidate_changelog_files,
    find_foreign_changelog_files,
)


def test_find_foreign_changelog_files():
    files = [Path(f"{n:03d}.yaml") for n in [15, 16, 17]]
    foreign = find_foreign_changelog_files(files, current_pr=16)
    assert [f.stem for f in foreign] == ["015", "017"]


def test_find_foreign_changelog_files_all_match():
    files = [Path("016.yaml")]
    assert not find_foreign_changelog_files(files, current_pr=16)


def test_consolidate_changelog_files(tmp_path: Path):
    target = changelog_filepath(tmp_path, 16)
    source = changelog_filepath(tmp_path, 15)
    dump_changelog_actions(source, [MakePublicAction(name="Foo", group="g1", full_path="g1.Foo", author="test")])

    consolidate_changelog_files(target, [source])

    assert target.exists()
    assert not source.exists()
    actions = parse_changelog_file_path(target)
    assert len(actions) == 1
    assert actions[0].name == "Foo"


def test_consolidate_preserves_existing_target(tmp_path: Path):
    target = changelog_filepath(tmp_path, 16)
    source = changelog_filepath(tmp_path, 15)
    dump_changelog_actions(target, [ChoreAction(description="existing chore", author="test")])
    dump_changelog_actions(source, [MakePublicAction(name="Bar", group="g2", full_path="g2.Bar", author="test")])

    consolidate_changelog_files(target, [source])

    actions = parse_changelog_file_path(target)
    assert len(actions) == 2
    assert not source.exists()
