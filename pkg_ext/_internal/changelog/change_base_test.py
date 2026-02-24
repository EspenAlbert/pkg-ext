from pathlib import Path
from unittest.mock import patch

from pkg_ext._internal.changelog import change_base
from pkg_ext._internal.changelog.actions import (
    ChoreAction,
    MakePublicAction,
    changelog_filepath,
    dump_changelog_actions,
    parse_changelog_file_path,
)
from pkg_ext._internal.changelog.change_base import (
    consolidate_changelog_files,
    find_changelog_files_in_diff,
    find_foreign_changelog_files,
    validate_no_foreign_changelog,
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


def _mock_run_result(stdout: str):
    class _Result:
        def __init__(self):
            self.stdout = stdout

    return _Result()


def test_find_changelog_files_in_diff(tmp_path: Path):
    changelog_dir = tmp_path / ".changelog"
    changelog_dir.mkdir()
    (changelog_dir / "015.yaml").write_text("actions: []")
    (changelog_dir / "016.yaml").write_text("actions: []")

    module_name = change_base.find_changelog_files_in_diff.__module__
    with patch(
        f"{module_name}.run_and_wait", return_value=_mock_run_result(".changelog/015.yaml\n.changelog/016.yaml\n")
    ):
        result = find_changelog_files_in_diff(tmp_path, changelog_dir, "main")
    assert len(result) == 2
    assert all(p.suffix == ".yaml" for p in result)


def test_find_changelog_files_in_diff_empty(tmp_path: Path):
    changelog_dir = tmp_path / ".changelog"
    changelog_dir.mkdir()
    module_name = change_base.find_changelog_files_in_diff.__module__
    with patch(f"{module_name}.run_and_wait", return_value=_mock_run_result("")):
        result = find_changelog_files_in_diff(tmp_path, changelog_dir, "main")
    assert result == []


def test_validate_no_foreign_changelog(tmp_path: Path):
    changelog_dir = tmp_path / ".changelog"
    changelog_dir.mkdir()
    (changelog_dir / "015.yaml").write_text("actions: []")
    (changelog_dir / "016.yaml").write_text("actions: []")

    module_name = change_base.find_changelog_files_in_diff.__module__
    with patch(
        f"{module_name}.run_and_wait", return_value=_mock_run_result(".changelog/015.yaml\n.changelog/016.yaml\n")
    ):
        foreign = validate_no_foreign_changelog(tmp_path, changelog_dir, "main", 16)
    assert len(foreign) == 1
    assert foreign[0].stem == "015"
