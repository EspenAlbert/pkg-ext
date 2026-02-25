from __future__ import annotations

from datetime import UTC, datetime

import pytest

from pkg_ext._internal.api_diff import (
    ChangeKind,
    DiffResult,
    _compare_bases,
    compare_api_dumps,
    compare_fields,
    compare_params,
    format_diff_results,
    normalize_type,
    reconcile_auto_actions,
    types_equal,
)
from pkg_ext._internal.changelog.actions import AdditionalChangeAction, BreakingChangeAction
from pkg_ext._internal.models.api_dump import (
    ClassFieldInfo,
    FuncParamInfo,
    ParamDefault,
    ParamKind,
    PublicApiDump,
)


def _param(
    name: str,
    kind: ParamKind = ParamKind.POSITIONAL_OR_KEYWORD,
    type_annotation: str | None = None,
    default: ParamDefault | None = None,
) -> FuncParamInfo:
    return FuncParamInfo(name=name, kind=kind, type_annotation=type_annotation, default=default)


def _default(value: str, is_factory: bool = False) -> ParamDefault:
    return ParamDefault(value_repr=value, is_factory=is_factory)


def _field(
    name: str,
    type_annotation: str | None = None,
    default: ParamDefault | None = None,
    is_computed: bool = False,
) -> ClassFieldInfo:
    return ClassFieldInfo(
        name=name,
        type_annotation=type_annotation,
        default=default,
        is_computed=is_computed,
    )


def test_normalize_type_none_input():
    assert normalize_type(None) is None


def test_normalize_type_union_ordering():
    assert normalize_type("str | None") == "None | str"
    assert normalize_type("None | str") == "None | str"
    assert normalize_type("int | str | None") == "None | int | str"


def test_normalize_type_union_bracket_syntax():
    assert normalize_type("Union[str, int]") == "int | str"
    assert normalize_type("typing.Union[str, int, None]") == "None | int | str"


def test_normalize_type_union_bracket_nested_in_callable():
    old = "Callable[[typing.Union[A, B, C]], bool]"
    new = "Callable[[A | B | C], bool]"
    assert normalize_type(old) == normalize_type(new)


def test_normalize_type_nested_pipe_not_corrupted():
    """Top-level | split must not break on | inside brackets."""
    t = "Callable[[A | B], R] | None"
    assert normalize_type(t) == "Callable[[A | B], R] | None"


def test_normalize_type_qualified_names():
    assert normalize_type("pathlib.Path") == "Path"
    assert normalize_type("list[pathlib.Path]") == "list[Path]"
    assert normalize_type("dict[str, pathlib.Path]") == "dict[str, Path]"


def test_types_equal():
    assert types_equal("str | None", "None | str")
    assert types_equal("pathlib.Path", "Path")
    assert not types_equal("str", "int")
    assert types_equal(None, None)


def test_types_equal_union_vs_pipe():
    assert types_equal(
        "list[Callable[[typing.Union[A, B, C]], bool]]",
        "list[Callable[[A | B | C], bool]]",
    )


def test_types_equal_union_with_qualified_names():
    assert types_equal(
        "list[Callable[[typing.Union[pkg.mod.A, pkg.mod.B]], bool | None]]",
        "list[Callable[[A | B], bool | None]]",
    )


def test_types_equal_class_tag_vs_name():
    assert types_equal(
        "Callable[[<class 'ask_shell._internal.models.ShellRun'>], bool]",
        "Callable[[ShellRun], bool]",
    )


def test_normalize_type_strips_class_tags():
    assert normalize_type("<class 'str'>") == "str"
    assert normalize_type("Callable[[<class 'int'>], bool]") == "Callable[[int], bool]"


def test_compare_params_removed():
    baseline = [_param("x"), _param("y")]
    dev = [_param("x")]
    results = compare_params(baseline, dev, "func", "group")
    assert len(results) == 1
    assert results[0].change_kind == ChangeKind.PARAM_REMOVED
    assert "removed param 'y'" in results[0].details


def test_compare_params_required_added():
    baseline = [_param("x")]
    dev = [_param("x"), _param("y")]
    results = compare_params(baseline, dev, "func", "group")
    assert len(results) == 1
    assert results[0].change_kind == ChangeKind.REQUIRED_PARAM_ADDED


def test_compare_params_optional_added():
    baseline = [_param("x")]
    dev = [_param("x"), _param("y", default=_default("10"))]
    results = compare_params(baseline, dev, "func", "group")
    assert len(results) == 1
    assert results[0].change_kind == ChangeKind.OPTIONAL_PARAM_ADDED


def test_compare_params_type_changed():
    baseline = [_param("x", type_annotation="str")]
    dev = [_param("x", type_annotation="int")]
    results = compare_params(baseline, dev, "func", "group")
    assert len(results) == 1
    assert results[0].change_kind == ChangeKind.PARAM_TYPE_CHANGED
    assert "str -> int" in results[0].details


def test_compare_params_default_removed():
    baseline = [_param("x", default=_default("10"))]
    dev = [_param("x")]
    results = compare_params(baseline, dev, "func", "group")
    assert len(results) == 1
    assert results[0].change_kind == ChangeKind.DEFAULT_REMOVED


def test_compare_params_default_added():
    baseline = [_param("x")]
    dev = [_param("x", default=_default("10"))]
    results = compare_params(baseline, dev, "func", "group")
    assert len(results) == 1
    assert results[0].change_kind == ChangeKind.DEFAULT_ADDED


def test_compare_params_default_changed():
    baseline = [_param("x", default=_default("10"))]
    dev = [_param("x", default=_default("20"))]
    results = compare_params(baseline, dev, "func", "group")
    assert len(results) == 1
    assert results[0].change_kind == ChangeKind.DEFAULT_CHANGED
    assert "10 -> 20" in results[0].details


def test_compare_params_factory_defaults_no_false_positive():
    baseline = [_param("x", default=_default("...", is_factory=True))]
    dev = [_param("x", default=_default("...", is_factory=True))]
    results = compare_params(baseline, dev, "func", "group")
    assert len(results) == 0


def test_compare_params_skips_self():
    baseline = [_param("self"), _param("x")]
    dev = [_param("self")]
    results = compare_params(baseline, dev, "method", "group")
    assert len(results) == 1
    assert results[0].change_kind == ChangeKind.PARAM_REMOVED
    assert "removed param 'x'" in results[0].details


def test_compare_params_union_type_normalization():
    baseline = [_param("x", type_annotation="str | None")]
    dev = [_param("x", type_annotation="None | str")]
    results = compare_params(baseline, dev, "func", "group")
    assert len(results) == 0


def test_compare_fields_removed():
    baseline = [_field("x"), _field("y")]
    dev = [_field("x")]
    results = compare_fields(baseline, dev, "MyClass", "group")
    assert len(results) == 1
    assert results[0].change_kind == ChangeKind.FIELD_REMOVED


def test_compare_fields_required_added():
    baseline = [_field("x")]
    dev = [_field("x"), _field("y")]
    results = compare_fields(baseline, dev, "MyClass", "group")
    assert len(results) == 1
    assert results[0].change_kind == ChangeKind.REQUIRED_FIELD_ADDED


def test_compare_fields_optional_added():
    baseline = [_field("x")]
    dev = [_field("x"), _field("y", default=_default("None"))]
    results = compare_fields(baseline, dev, "MyClass", "group")
    assert len(results) == 1
    assert results[0].change_kind == ChangeKind.OPTIONAL_FIELD_ADDED


def test_compare_fields_skips_computed():
    baseline = [_field("x"), _field("computed", is_computed=True)]
    dev = [_field("x")]
    results = compare_fields(baseline, dev, "MyClass", "group")
    assert len(results) == 0


def test_diff_result_to_breaking_change_action():
    diff = DiffResult(
        name="func",
        group="core",
        action_type="breaking_change",
        change_kind=ChangeKind.PARAM_REMOVED,
        details="removed param 'x'",
    )
    action = diff.to_changelog_action()
    assert isinstance(action, BreakingChangeAction)
    assert action.name == "func"
    assert action.group == "core"
    assert action.auto_generated


def test_diff_result_to_additional_change_action():
    diff = DiffResult(
        name="func",
        group="core",
        action_type="additional_change",
        change_kind=ChangeKind.DEFAULT_ADDED,
        details="param 'x' default added: 10",
    )
    action = diff.to_changelog_action()
    assert isinstance(action, AdditionalChangeAction)
    assert action.auto_generated


def test_compare_api_dumps_none_baseline_returns_empty():
    dev = PublicApiDump(
        pkg_import_name="test",
        version="1.0.0",
        groups=[],
        dumped_at=datetime.now(UTC),
    )
    assert not compare_api_dumps(None, dev)


def test_format_diff_results_empty():
    assert format_diff_results([]) == "No API changes detected."


def test_format_diff_results_grouped():
    results = [
        DiffResult(
            name="func",
            group="core",
            action_type="breaking_change",
            change_kind=ChangeKind.PARAM_REMOVED,
            details="removed param 'x'",
        ),
        DiffResult(
            name="helper",
            group="utils",
            action_type="additional_change",
            change_kind=ChangeKind.DEFAULT_ADDED,
            details="param 'y' default added: 10",
        ),
    ]
    output = format_diff_results(results)
    assert "Breaking Changes (1)" in output
    assert "Additional Changes (1)" in output
    assert "[core] func: removed param 'x'" in output
    assert "1 breaking, 1 additional" in output


def test_compare_fields_populates_field_name():
    baseline = [_field("x")]
    dev = [_field("x"), _field("y", default=_default("None"))]
    results = compare_fields(baseline, dev, "MyClass", "group")
    assert results[0].field_name == "y"


def test_diff_result_to_action_includes_field_name():
    diff = DiffResult(
        name="MyClass",
        group="core",
        action_type="additional_change",
        change_kind=ChangeKind.OPTIONAL_FIELD_ADDED,
        details="added field 'new_field'",
        field_name="new_field",
    )
    action = diff.to_changelog_action()
    assert isinstance(action, AdditionalChangeAction)
    assert action.field_name == "new_field"


@pytest.mark.parametrize(
    "baseline_direct,dev_direct,dev_mro_bases,expected_kinds",
    [
        # Base moved to intermediate (still in MRO) -> only reports added
        (["BaseModel"], ["PRFieldsBase"], ["PRFieldsBase", "BaseModel"], [ChangeKind.BASE_CLASS_ADDED]),
        # Base truly removed (not in MRO) -> BASE_CLASS_REMOVED
        (["BaseModel"], [], [], [ChangeKind.BASE_CLASS_REMOVED]),
        # New base added -> BASE_CLASS_ADDED
        ([], ["NewBase"], ["NewBase"], [ChangeKind.BASE_CLASS_ADDED]),
        # No change
        (["Base"], ["Base"], ["Base"], []),
    ],
    ids=["base_in_mro", "base_removed", "base_added", "no_change"],
)
def test_compare_bases_mro_aware(baseline_direct, dev_direct, dev_mro_bases, expected_kinds):
    results = _compare_bases(baseline_direct, dev_direct, dev_mro_bases, "TestClass", "group")
    assert [r.change_kind for r in results] == expected_kinds


def test_reconcile_preserves_timestamp_and_removes_stale():
    old_ts = datetime(2025, 1, 1, tzinfo=UTC)
    existing = [
        BreakingChangeAction(
            name="func",
            group="core",
            details="old details",
            change_kind="param_removed",
            auto_generated=True,
            ts=old_ts,
        ),
        BreakingChangeAction(
            name="stale",
            group="core",
            details="will be removed",
            change_kind="param_removed",
            auto_generated=True,
        ),
    ]
    new_diff = [
        DiffResult(
            name="func",
            group="core",
            action_type="breaking_change",
            change_kind=ChangeKind.PARAM_REMOVED,
            details="new details",
        ),
        DiffResult(
            name="new_func",
            group="core",
            action_type="additional_change",
            change_kind=ChangeKind.DEFAULT_ADDED,
            details="param default added",
        ),
    ]
    result = reconcile_auto_actions(existing, new_diff)

    assert len(result) == 2
    assert result[0].ts == old_ts
    assert result[0].details == "new details"
    assert result[1].name == "new_func"
    assert result[1].auto_generated
