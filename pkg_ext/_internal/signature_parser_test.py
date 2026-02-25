from dataclasses import dataclass
from enum import StrEnum
from typing import Callable, Union

import typer
from pydantic import BaseModel, Field, computed_field

from pkg_ext._internal.models.api_dump import ParamKind
from pkg_ext._internal.signature_parser import (
    _annotation_str,
    extract_cli_params,
    is_cli_command,
    parse_class_fields,
    parse_mro_bases,
    parse_signature,
    stable_repr,
    strip_memory_addresses,
)


def sample_func(a: int, b: str = "hello", *args, kwonly: bool = False, **kwargs) -> str:
    return ""


class SampleModel(BaseModel):
    name: str
    count: int = Field(default=0, description="A count field")
    optional_tags: list[str] | None = None

    @computed_field
    @property
    def double_count(self) -> int:
        return self.count * 2


@dataclass
class SampleDataclass:
    name: str
    value: int = 10


class ChildClass(SampleModel):
    extra: str = ""


def test_parse_signature_covers_all_param_kinds():
    sig = parse_signature(sample_func)
    assert len(sig.parameters) == 5
    kinds = [p.kind for p in sig.parameters]
    assert ParamKind.POSITIONAL_OR_KEYWORD in kinds
    assert ParamKind.VAR_POSITIONAL in kinds
    assert ParamKind.KEYWORD_ONLY in kinds
    assert ParamKind.VAR_KEYWORD in kinds
    assert sig.return_annotation == "str"


def test_parse_pydantic_model_fields():
    fields = parse_class_fields(SampleModel)
    assert fields
    field_names = [f.name for f in fields]
    assert "name" in field_names
    assert "count" in field_names
    assert "double_count" in field_names
    computed = next(f for f in fields if f.name == "double_count")
    assert computed.is_computed


def test_parse_pydantic_none_default():
    fields = parse_class_fields(SampleModel)
    assert fields
    optional_field = next(f for f in fields if f.name == "optional_tags")
    assert optional_field.default is not None
    assert optional_field.default.value_repr == "None"
    assert not optional_field.default.is_factory


def test_parse_dataclass_fields():
    fields = parse_class_fields(SampleDataclass)
    assert fields
    assert len(fields) == 2
    value_field = next(f for f in fields if f.name == "value")
    assert value_field.default
    assert value_field.default.value_repr == "10"


def test_parse_mro_bases():
    mro, num_direct = parse_mro_bases(ChildClass)
    assert "SampleModel" in mro
    assert num_direct == 1


class OutputFormat(StrEnum):
    JSON = "json"
    YAML = "yaml"


def _sample_cli_command(
    name: str = typer.Option(..., "--name", "-n", help="The name"),
    count: int = typer.Option(0, "--count", help="Count value"),
    format: OutputFormat = typer.Option(OutputFormat.JSON, help="Output format"),
    verbose: bool = typer.Option(False),
) -> None:
    pass


def _regular_function(a: int, b: str = "default") -> str:
    return ""


def _context_only_cli(ctx: typer.Context) -> None:
    pass


def test_is_cli_command():
    assert is_cli_command(_sample_cli_command)
    assert is_cli_command(_context_only_cli)
    assert not is_cli_command(_regular_function)
    assert not is_cli_command(sample_func)


def test_extract_cli_params():
    params = extract_cli_params(_sample_cli_command)
    assert len(params) == 4
    name_param = next(p for p in params if p.param_name == "name")
    assert name_param.flags == ["--name", "-n"]
    assert name_param.required
    assert name_param.help == "The name"
    count_param = next(p for p in params if p.param_name == "count")
    assert count_param.default_repr == "0"
    assert not count_param.required
    format_param = next(p for p in params if p.param_name == "format")
    assert format_param.choices == ["json", "yaml"]
    verbose_param = next(p for p in params if p.param_name == "verbose")
    assert verbose_param.flags == ["--verbose"]


def test_stable_repr_normalizes_memory_addresses():
    sentinel = object()
    result = stable_repr(sentinel)
    assert result == "<object object>"
    assert "0x" not in result


def test_stable_repr_preserves_normal_values():
    assert stable_repr("hello") == "'hello'"
    assert stable_repr(42) == "42"
    assert stable_repr(None) == "None"
    assert stable_repr([1, 2, 3]) == "[1, 2, 3]"


class _CustomSentinel:
    pass


def test_stable_repr_handles_custom_sentinel_class():
    sentinel = _CustomSentinel()
    result = stable_repr(sentinel)
    assert result.startswith("<")
    assert "_CustomSentinel" in result
    assert "0x" not in result


def test_strip_memory_addresses_handles_embedded_patterns():
    s = "Callable[[X], <function foo at 0x123abc>]"
    result = strip_memory_addresses(s)
    assert result == "Callable[[X], <function foo>]"


def test_strip_memory_addresses_handles_multiple_patterns():
    s = "<object object at 0xabc> and <function bar at 0xdef>"
    result = strip_memory_addresses(s)
    assert result == "<object object> and <function bar>"
    assert "0x" not in result


def test_stable_repr_strips_embedded_memory_addresses():
    """stable_repr should strip memory addresses embedded in complex reprs like AfterValidator."""

    class _FakeValidator:
        def __init__(self, func):
            self.func = func

        def __repr__(self):
            return f"FakeValidator(func=<function {self.func.__name__} at 0xdeadbeef>)"

    def my_func():
        pass

    result = stable_repr(_FakeValidator(my_func))
    assert result == "FakeValidator(func=<function my_func>)"
    assert "0x" not in result


def test_annotation_str_callable_with_union_params():
    """Callable param lists with Union should use pipe syntax, not typing.Union[...]."""
    cb = Callable[[Union[int, str, float]], bool]
    assert _annotation_str(cb) == "Callable[[int | str | float], bool]"


def test_annotation_str_callable_with_pipe_union_params():
    cb = Callable[[int | str | float], bool]
    assert _annotation_str(cb) == "Callable[[int | str | float], bool]"


def test_annotation_str_callable_union_and_pipe_produce_same_output():
    """Union[...] and | syntax inside Callable produce identical strings."""
    cb_union = Callable[[Union[int, str]], bool]
    cb_pipe = Callable[[int | str], bool]
    assert _annotation_str(cb_union) == _annotation_str(cb_pipe)
