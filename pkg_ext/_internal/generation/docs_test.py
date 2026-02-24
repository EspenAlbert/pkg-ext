from datetime import UTC, datetime
from pathlib import Path

from zero_3rdparty.file_utils import ensure_parents_write_text
from zero_3rdparty.sections import parse_sections

from pkg_ext._internal.changelog.actions import FixAction, MakePublicAction
from pkg_ext._internal.config import (
    PKG_EXT_TOOL_NAME,
    ROOT_GROUP_NAME,
    GroupConfig,
    ProjectConfig,
)
from pkg_ext._internal.generation.docs import (
    GeneratedDocsOutput,
    SymbolContext,
    build_symbol_context,
    generate_docs,
    group_dir_name,
    has_env_vars,
    render_group_index,
)
from pkg_ext._internal.generation.docs_constants import MD_CONFIG, ROOT_DIR
from pkg_ext._internal.models.api_dump import (
    CallableSignature,
    ClassDump,
    ClassFieldInfo,
    FunctionDump,
    GroupDump,
    ParamDefault,
    PublicApiDump,
)


def _func_dump(name: str) -> FunctionDump:
    return FunctionDump(name=name, module_path="mod", signature=CallableSignature())


def _class_dump(name: str, env_var: str | None = None) -> ClassDump:
    fields = None
    if env_var:
        fields = [ClassFieldInfo(name="field", env_vars=[env_var])]
    return ClassDump(name=name, module_path="mod", fields=fields)


def test_group_dir_name_root():
    group = GroupDump(name=ROOT_GROUP_NAME, symbols=[])
    assert group_dir_name(group) == ROOT_DIR


def test_group_dir_name_regular():
    group = GroupDump(name="config", symbols=[])
    assert group_dir_name(group) == "config"


def test_has_env_vars():
    func = _func_dump("func")
    assert not has_env_vars(func)
    cls_no_env = _class_dump("NoEnv")
    assert not has_env_vars(cls_no_env)
    cls_with_env = _class_dump("WithEnv", env_var="MY_VAR")
    assert has_env_vars(cls_with_env)


def test_symbol_context_complexity():
    simple = SymbolContext(symbol=_func_dump("simple"))
    assert not simple.needs_own_page

    with_env = SymbolContext(symbol=_class_dump("env", "VAR"), has_env_vars=True)
    assert with_env.needs_own_page

    with_changes = SymbolContext(symbol=_func_dump("ch"), has_meaningful_changes=True)
    assert with_changes.needs_own_page


def test_build_symbol_context_only_make_public_not_complex():
    func = _func_dump("my_func")
    action = MakePublicAction(name="my_func", group="config", full_path="mod.my_func", ts=datetime.now(UTC))
    ctx = build_symbol_context(func, "config", [action])
    assert not ctx.has_meaningful_changes
    assert not ctx.needs_own_page


def test_build_symbol_context_fix_action_is_complex():
    func = _func_dump("my_func")
    action = FixAction(name="my_func", short_sha="abc123", message="fix", ts=datetime.now(UTC))
    ctx = build_symbol_context(func, "config", [action])
    assert ctx.has_meaningful_changes
    assert ctx.needs_own_page


def test_build_symbol_context_primary_not_complex():
    func = _func_dump("config")
    ctx = build_symbol_context(func, "config", [])
    assert ctx.is_primary
    assert not ctx.needs_own_page


def test_symbol_context_primary_overrides_complex():
    ctx = SymbolContext(symbol=_func_dump("copy"), has_meaningful_changes=True, is_primary=True)
    assert ctx.is_primary
    assert not ctx.needs_own_page


def test_render_group_index_has_valid_sections():
    group = GroupDump(name="config", symbols=[_func_dump("load"), _func_dump("save")])
    contexts = [SymbolContext(symbol=s) for s in group.symbols]
    content = render_group_index(group, contexts, GroupConfig())

    sections = parse_sections(content, PKG_EXT_TOOL_NAME, MD_CONFIG)
    section_ids = {s.id for s in sections}
    assert "header" in section_ids
    assert "symbols" in section_ids
    assert "symbol_details_header" in section_ids
    assert "[`load`](#load_def)" in content
    assert "[`save`](#save_def)" in content


def test_render_group_index_includes_docstring():
    group = GroupDump(name="config", symbols=[])
    group_config = GroupConfig(docstring="Configuration utilities.")
    content = render_group_index(group, [], group_config)
    assert "Configuration utilities." in content


def test_render_group_index_includes_signatures():
    cls = ClassDump(
        name="SimpleClass",
        module_path="mod",
        fields=[
            ClassFieldInfo(
                name="timeout",
                type_annotation="int",
                default=ParamDefault(value_repr="30"),
            ),
        ],
    )
    group = GroupDump(name="utils", symbols=[cls])
    contexts = [SymbolContext(symbol=cls)]
    content = render_group_index(group, contexts, GroupConfig())
    assert "class SimpleClass:" in content
    assert "timeout: int = 30" in content


def test_generate_docs_creates_index_and_complex_pages(project_config: ProjectConfig):
    api_dump = PublicApiDump(
        pkg_import_name="my_pkg",
        version="1.0.0",
        dumped_at=datetime.now(UTC),
        groups=[
            GroupDump(
                name="config",
                symbols=[
                    _func_dump("simple_func"),
                    _class_dump("EnvClass", env_var="MY_VAR"),
                ],
            )
        ],
    )
    result = generate_docs(api_dump, project_config, [])
    assert isinstance(result, GeneratedDocsOutput)
    assert "config/index.md" in result.path_contents
    assert "config/envclass.md" in result.path_contents
    assert "config/simple_func.md" not in result.path_contents


def test_render_group_index_with_primary_symbol():
    func = _func_dump("copy")
    other = _func_dump("helper")
    group = GroupDump(name="copy", symbols=[func, other])
    contexts = [
        SymbolContext(symbol=func, is_primary=True),
        SymbolContext(symbol=other),
    ]
    content = render_group_index(group, contexts, GroupConfig())

    sections = parse_sections(content, PKG_EXT_TOOL_NAME, MD_CONFIG)
    section_ids = {s.id for s in sections}
    assert "header" in section_ids
    assert "copy_def" in section_ids
    assert "symbol_details_header" in section_ids
    assert "# copy" in content
    assert "[`copy`](#copy_def)" in content
    assert "[`helper`](#helper_def)" in content


def test_generate_docs_primary_symbol_no_separate_file(project_config: ProjectConfig):
    api_dump = PublicApiDump(
        pkg_import_name="my_pkg",
        version="1.0.0",
        dumped_at=datetime.now(UTC),
        groups=[
            GroupDump(
                name="copy",
                symbols=[
                    _func_dump("copy"),
                    _class_dump("CopyOptions", env_var="COPY_VAR"),
                ],
            )
        ],
    )
    result = generate_docs(api_dump, project_config, [])
    assert "copy/index.md" in result.path_contents
    assert "copy/copy.md" not in result.path_contents
    assert "copy/copyoptions.md" in result.path_contents
    assert "# copy" in result.path_contents["copy/index.md"]


def test_render_group_index_with_examples(tmp_path: Path):
    examples_dir = tmp_path / "docs" / "examples"
    ensure_parents_write_text(
        examples_dir / "sections" / "parse_sections.md",
        "<!--\ndescription: Parse content into named sections\n-->\n# Example",
    )
    group = GroupDump(name="sections", symbols=[_func_dump("parse_sections")])
    contexts = [SymbolContext(symbol=s) for s in group.symbols]
    config = GroupConfig(examples_include=["parse_sections"])
    content = render_group_index(group, contexts, config, docs_dir=tmp_path / "docs")
    assert "- [Example: Parse content into named sections](../examples/sections/parse_sections.md)" in content


def test_render_group_index_no_examples():
    group = GroupDump(name="sections", symbols=[_func_dump("f")])
    contexts = [SymbolContext(symbol=s) for s in group.symbols]
    content = render_group_index(group, contexts, GroupConfig())
    assert "Example" not in content


def test_generate_docs_with_inline_example_links(tmp_path: Path):
    docs_dir = tmp_path / "docs"
    ensure_parents_write_text(
        docs_dir / "examples" / "sections" / "parse_sections.md",
        "<!--\ndescription: Parse content into named sections\n-->\n# Example",
    )
    api_dump = PublicApiDump(
        pkg_import_name="my_pkg",
        version="1.0.0",
        dumped_at=datetime.now(UTC),
        groups=[GroupDump(name="sections", symbols=[_func_dump("parse_sections")])],
    )
    config = ProjectConfig(groups={"sections": GroupConfig(examples_include=["parse_sections"])})
    result = generate_docs(api_dump, config, [], docs_dir=docs_dir)
    index_content = result.path_contents["sections/index.md"]
    assert "- [Example: Parse content into named sections](../examples/sections/parse_sections.md)" in index_content


def test_generate_docs_own_page_symbol_with_example(tmp_path: Path):
    docs_dir = tmp_path / "docs"
    ensure_parents_write_text(
        docs_dir / "examples" / "config" / "EnvClass.md",
        "<!--\ndescription: Environment configuration\n-->\n# Example",
    )
    api_dump = PublicApiDump(
        pkg_import_name="my_pkg",
        version="1.0.0",
        dumped_at=datetime.now(UTC),
        groups=[
            GroupDump(
                name="config",
                symbols=[_class_dump("EnvClass", env_var="MY_VAR")],
            )
        ],
    )
    config = ProjectConfig(groups={"config": GroupConfig(examples_include=["EnvClass"])})
    result = generate_docs(api_dump, config, [], docs_dir=docs_dir, pkg_src_dir=tmp_path)
    page_content = result.path_contents["config/envclass.md"]
    assert "- [Example: Environment configuration](../../examples/config/EnvClass.md)" in page_content
