from datetime import UTC, datetime

from zero_3rdparty.file_utils import ensure_parents_write_text

from pkg_ext._internal.config import GroupConfig, ProjectConfig
from pkg_ext._internal.examples import build_example_prompt, check_examples_exist
from pkg_ext._internal.models.api_dump import (
    CallableSignature,
    FuncParamInfo,
    FunctionDump,
    GroupDump,
    ParamKind,
    PublicApiDump,
)
from pkg_ext._internal.settings import PkgSettings


def _api_dump(pkg_name: str = "my_pkg") -> PublicApiDump:
    return PublicApiDump(
        pkg_import_name=pkg_name,
        version="0.1.0",
        dumped_at=datetime.now(UTC),
        groups=[
            GroupDump(
                name="sections",
                symbols=[
                    FunctionDump(
                        name="parse_sections",
                        module_path="_internal.sections",
                        docstring="Parse content into sections.",
                        signature=CallableSignature(
                            parameters=[
                                FuncParamInfo(
                                    name="content", kind=ParamKind.POSITIONAL_OR_KEYWORD, type_annotation="str"
                                ),
                                FuncParamInfo(
                                    name="tool_name", kind=ParamKind.POSITIONAL_OR_KEYWORD, type_annotation="str"
                                ),
                            ],
                            return_annotation="dict[str, str]",
                        ),
                    ),
                    FunctionDump(
                        name="replace_sections",
                        module_path="_internal.sections",
                        docstring="Replace sections in content.",
                        signature=CallableSignature(),
                    ),
                ],
            ),
        ],
    )


def _config(*symbol_names: str) -> ProjectConfig:
    return ProjectConfig(groups={"sections": GroupConfig(examples_include=list(symbol_names))})


def test_build_example_prompt_with_missing_symbols(settings: PkgSettings):
    api_dump = _api_dump(settings.pkg_import_name)
    config = _config("parse_sections")
    prompt = build_example_prompt(settings, api_dump, config)
    assert "write-examples" in prompt
    assert "parse_sections" in prompt
    assert "Parse content into sections." in prompt
    assert "content: str" in prompt


def test_build_example_prompt_skips_existing(settings: PkgSettings):
    api_dump = _api_dump(settings.pkg_import_name)
    config = _config("parse_sections")
    ensure_parents_write_text(settings.example_file_path("sections", "parse_sections"), "# example")
    assert build_example_prompt(settings, api_dump, config) == ""


def test_check_examples_exist_missing(settings: PkgSettings):
    config_path = settings.state_dir / "pyproject.toml"
    config_path.write_text('[tool.pkg-ext.groups.sections]\nexamples_include = ["parse_sections", "CommentConfig"]\n')
    missing = check_examples_exist(settings)
    assert len(missing) == 2
    assert missing[0][1] == "parse_sections"
    assert missing[1][1] == "CommentConfig"
    assert missing[1][2].name == "CommentConfig.md"


def test_check_examples_exist_all_present(settings: PkgSettings):
    config_path = settings.state_dir / "pyproject.toml"
    config_path.write_text('[tool.pkg-ext.groups.sections]\nexamples_include = ["parse_sections"]\n')
    ensure_parents_write_text(settings.example_file_path("sections", "parse_sections"), "# example")
    assert check_examples_exist(settings) == []
