from datetime import UTC, datetime
from pathlib import Path

from pkg_ext._internal.config import ROOT_GROUP_NAME
from pkg_ext._internal.generation.docs import GeneratedDocsOutput
from pkg_ext._internal.generation.docs_mkdocs import (
    MkdocsSection,
    NavItem,
    _render_nav_yaml,
    copy_readme_as_index,
    extract_complex_symbols,
    generate_mkdocs_nav,
    transform_repo_root_links,
    write_docs_files,
    write_mkdocs_yml,
)
from pkg_ext._internal.models.api_dump import ClassDump, GroupDump, PublicApiDump


def test_copy_readme_as_index(tmp_path: Path):
    state_dir = tmp_path / "pkg"
    state_dir.mkdir()
    (state_dir / "readme.md").write_text("# My Package\n\nDescription here.")
    docs_dir = tmp_path / "docs"
    index = copy_readme_as_index(state_dir, docs_dir, "my_pkg")
    assert index.exists()
    assert "# My Package" in index.read_text()


def test_copy_readme_fallback(tmp_path: Path):
    state_dir = tmp_path / "pkg"
    state_dir.mkdir()
    docs_dir = tmp_path / "docs"
    index = copy_readme_as_index(state_dir, docs_dir, "my_pkg")
    assert index.read_text() == "# my_pkg\n"


def test_transform_repo_root_links_converts_root_files():
    content = "See [CONTRIBUTING.md](CONTRIBUTING.md) for details."
    repo_url = "https://github.com/user/repo"
    result = transform_repo_root_links(content, repo_url, "main", {"CONTRIBUTING.md"})
    assert result == "See [CONTRIBUTING.md](https://github.com/user/repo/blob/main/CONTRIBUTING.md) for details."


def test_transform_repo_root_links_handles_dot_slash():
    content = "See [CONTRIBUTING.md](./CONTRIBUTING.md) for details."
    repo_url = "https://github.com/user/repo"
    result = transform_repo_root_links(content, repo_url, "main", {"CONTRIBUTING.md"})
    assert result == "See [CONTRIBUTING.md](https://github.com/user/repo/blob/main/CONTRIBUTING.md) for details."


def test_transform_repo_root_links_preserves_absolute_urls():
    content = "See [docs](https://example.com) and [anchor](#section)."
    result = transform_repo_root_links(content, "https://github.com/user/repo", "main", {"docs"})
    assert content == result


def test_transform_repo_root_links_preserves_path_with_directory():
    content = "See [api docs](docs/api.md) for details."
    result = transform_repo_root_links(content, "https://github.com/user/repo", "main", {"api.md"})
    assert content == result


def test_transform_repo_root_links_preserves_unknown_files():
    content = "See [unknown.md](unknown.md) for details."
    result = transform_repo_root_links(content, "https://github.com/user/repo", "main", {"CONTRIBUTING.md"})
    assert content == result


def test_generate_mkdocs_nav():
    api_dump = PublicApiDump(
        pkg_import_name="my_pkg",
        version="1.0.0",
        dumped_at=datetime.now(UTC),
        groups=[
            GroupDump(name=ROOT_GROUP_NAME, symbols=[]),
            GroupDump(name="config", symbols=[]),
        ],
    )
    nav = generate_mkdocs_nav(api_dump, "my_pkg")
    assert nav[0] == {"Home": "index.md"}
    assert {"my_pkg": "_root/index.md"} in nav
    assert {"config": "config/index.md"} in nav


def test_generate_mkdocs_nav_with_complex_symbols():
    api_dump = PublicApiDump(
        pkg_import_name="my_pkg",
        version="1.0.0",
        dumped_at=datetime.now(UTC),
        groups=[
            GroupDump(
                name=ROOT_GROUP_NAME,
                symbols=[ClassDump(name="Settings", module_path="settings", docstring="")],
            ),
        ],
    )
    complex_symbols = {ROOT_GROUP_NAME: [("Settings", "settings.md")]}
    nav = generate_mkdocs_nav(api_dump, "my_pkg", complex_symbols)
    root_nav = nav[1]["my_pkg"]
    assert isinstance(root_nav, list)
    assert {"Overview": "_root/index.md"} in root_nav
    assert {"Settings": "_root/settings.md"} in root_nav


def test_extract_complex_symbols():
    groups = [
        GroupDump(
            name=ROOT_GROUP_NAME,
            symbols=[ClassDump(name="Settings", module_path="settings", docstring="")],
        ),
    ]
    output = GeneratedDocsOutput(
        path_contents={
            "_root/index.md": "# Root",
            "_root/settings.md": "# Settings",
        }
    )
    result = extract_complex_symbols(output, groups)
    assert ROOT_GROUP_NAME in result
    assert ("Settings", "settings.md") in result[ROOT_GROUP_NAME]


def test_write_mkdocs_yml_creates_new(tmp_path: Path):
    mkdocs_path = tmp_path / "mkdocs.yml"
    nav: list[NavItem] = [{"Home": "index.md"}, {"config": "config/index.md"}]
    write_mkdocs_yml(mkdocs_path, "my_pkg", nav)
    content = mkdocs_path.read_text()
    assert "site_name: my_pkg" in content
    assert "nav:" in content
    for section in MkdocsSection:
        assert f"DO_NOT_EDIT: pkg-ext {section.value}" in content


def test_write_mkdocs_yml_honors_skip_sections(tmp_path: Path):
    mkdocs_path = tmp_path / "mkdocs.yml"
    nav: list[NavItem] = [{"Home": "index.md"}]
    write_mkdocs_yml(mkdocs_path, "my_pkg", nav, skip_sections=("theme", "extensions"))
    content = mkdocs_path.read_text()
    assert "site_name:" in content
    assert "theme:" not in content


def test_write_docs_files_idempotent(tmp_path: Path):
    docs_dir = tmp_path / "docs"
    output = GeneratedDocsOutput(path_contents={"config/index.md": "# Config\n"})
    count1 = write_docs_files(output, docs_dir)
    content1 = (docs_dir / "config/index.md").read_text()
    count2 = write_docs_files(output, docs_dir)
    content2 = (docs_dir / "config/index.md").read_text()
    assert count1 == count2 == 1
    assert content1 == content2


def test_generate_mkdocs_nav_with_examples():
    api_dump = PublicApiDump(
        pkg_import_name="my_pkg",
        version="1.0.0",
        dumped_at=datetime.now(UTC),
        groups=[GroupDump(name="sections", symbols=[])],
    )
    examples_include = {"sections": ["parse_sections", "CommentConfig"]}
    nav = generate_mkdocs_nav(api_dump, "my_pkg", examples_include=examples_include)
    sections_nav = nav[1]["sections"]
    assert isinstance(sections_nav, list)
    assert {"Overview": "sections/index.md"} in sections_nav
    examples_entry = sections_nav[-1]
    assert "Examples" in examples_entry
    example_children = examples_entry["Examples"]
    assert isinstance(example_children, list)
    assert {"parse_sections": "examples/sections/parse_sections.md"} in example_children
    assert {"CommentConfig": "examples/sections/CommentConfig.md"} in example_children


def test_generate_mkdocs_nav_flat_group_becomes_nested_with_examples():
    api_dump = PublicApiDump(
        pkg_import_name="my_pkg",
        version="1.0.0",
        dumped_at=datetime.now(UTC),
        groups=[GroupDump(name="config", symbols=[])],
    )
    nav_without = generate_mkdocs_nav(api_dump, "my_pkg")
    assert nav_without[1] == {"config": "config/index.md"}

    nav_with = generate_mkdocs_nav(api_dump, "my_pkg", examples_include={"config": ["load"]})
    children = nav_with[1]["config"]
    assert isinstance(children, list)
    assert {"Overview": "config/index.md"} in children


def test_render_nav_yaml_with_examples():
    nav: list[NavItem] = [
        {"Home": "index.md"},
        {
            "sections": [
                {"Overview": "sections/index.md"},
                {"Examples": [{"parse_sections": "examples/sections/parse_sections.md"}]},
            ]
        },
    ]
    yaml = _render_nav_yaml(nav)
    assert "      - parse_sections: examples/sections/parse_sections.md" in yaml
    assert "    - Examples:" in yaml
