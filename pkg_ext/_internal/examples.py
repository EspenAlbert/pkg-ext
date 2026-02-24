from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from pkg_ext._internal.config import ProjectConfig, load_project_config
from pkg_ext._internal.models.api_dump import (
    CallableSignature,
    ClassDump,
    ClassFieldInfo,
    FunctionDump,
    PublicApiDump,
    SymbolDumpBase,
)

if TYPE_CHECKING:
    from pkg_ext._internal.settings import PkgSettings

logger = logging.getLogger(__name__)


def _load_examples_include(config: ProjectConfig) -> dict[str, list[str]]:
    return {name: group_cfg.examples_include for name, group_cfg in config.groups.items() if group_cfg.examples_include}


def _missing_example_files(settings: PkgSettings, config: ProjectConfig) -> list[tuple[str, str, Path]]:
    missing: list[tuple[str, str, Path]] = []
    for group_name, symbols in _load_examples_include(config).items():
        for symbol in symbols:
            path = settings.example_file_path(group_name, symbol)
            if not path.exists():
                missing.append((group_name, symbol, path))
    return missing


def check_examples_exist(settings: PkgSettings) -> list[tuple[str, str, Path]]:
    config = load_project_config(settings.state_dir)
    return _missing_example_files(settings, config)


def _build_symbol_lookup(api_dump: PublicApiDump) -> dict[str, SymbolDumpBase]:
    lookup: dict[str, SymbolDumpBase] = {}
    for group in api_dump.groups:
        for symbol in group.symbols:
            key = f"{api_dump.pkg_import_name}.{symbol.module_path}.{symbol.name}"
            lookup[key] = symbol
    return lookup


def _collect_type_imports(symbol: SymbolDumpBase) -> list[str]:
    imports: list[str] = []
    if isinstance(symbol, FunctionDump):
        for p in symbol.signature.parameters:
            imports.extend(p.type_imports)
        imports.extend(symbol.signature.return_type_imports)
    elif isinstance(symbol, ClassDump):
        if symbol.fields:
            for f in symbol.fields:
                imports.extend(f.type_imports)
        if symbol.init_signature:
            for p in symbol.init_signature.parameters:
                imports.extend(p.type_imports)
            imports.extend(symbol.init_signature.return_type_imports)
    return imports


def _find_related_types(symbol: SymbolDumpBase, lookup: dict[str, SymbolDumpBase]) -> list[SymbolDumpBase]:
    related: list[SymbolDumpBase] = []
    seen: set[str] = set()
    for imp in _collect_type_imports(symbol):
        if imp in seen or imp not in lookup:
            continue
        seen.add(imp)
        related.append(lookup[imp])
    return related


def _find_test_file(symbol: SymbolDumpBase, settings: PkgSettings) -> str:
    parts = symbol.module_path.split(".")
    test_path = (
        settings.pkg_directory / "/".join(parts[:-1]) / f"{parts[-1]}_test.py"
        if len(parts) > 1
        else settings.pkg_directory / f"{parts[0]}_test.py"
    )
    if test_path.exists():
        return test_path.read_text()
    return ""


def _format_signature(sig: CallableSignature) -> str:
    params = []
    for p in sig.parameters:
        s = p.name
        if p.type_annotation:
            s += f": {p.type_annotation}"
        if p.default:
            s += f" = {p.default.value_repr}"
        params.append(s)
    ret = f" -> {sig.return_annotation}" if sig.return_annotation else ""
    return f"({', '.join(params)}){ret}"


def _format_fields(fields: list[ClassFieldInfo]) -> str:
    lines = []
    for f in fields:
        if f.is_class_var:
            continue
        line = f"  {f.name}"
        if f.type_annotation:
            line += f": {f.type_annotation}"
        if f.default:
            line += f" = {f.default.value_repr}"
        lines.append(line)
    return "\n".join(lines)


def _format_related_type(rt: SymbolDumpBase) -> str:
    if isinstance(rt, ClassDump) and rt.fields:
        return f"### {rt.name}\n```\n{_format_fields(rt.fields)}\n```"
    if isinstance(rt, FunctionDump):
        return f"### {rt.name}\n`{rt.name}{_format_signature(rt.signature)}`"
    return f"### {rt.name}\n{rt.docstring or '(no docstring)'}"


def _format_symbol_context(
    symbol: SymbolDumpBase,
    related_types: list[SymbolDumpBase],
    test_code: str,
) -> str:
    parts: list[str] = []

    if isinstance(symbol, FunctionDump):
        parts.append(f"**Signature:**\n`{symbol.name}{_format_signature(symbol.signature)}`")
    elif isinstance(symbol, ClassDump):
        if symbol.fields:
            parts.append(f"**Fields:**\n```\n{_format_fields(symbol.fields)}\n```")
        if symbol.init_signature:
            parts.append(f"**Init signature:**\n`{_format_signature(symbol.init_signature)}`")

    if symbol.docstring:
        parts.append(f"**Docstring:**\n{symbol.docstring}")

    if related_types:
        formatted = [_format_related_type(rt) for rt in related_types]
        parts.append("**Related types:**\n\n" + "\n\n".join(formatted))

    if test_code:
        module_test = f"{symbol.module_path}_test.py"
        parts.append(f"**Test code** (from `{module_test}`):\n```python\n{test_code}\n```")

    return "\n\n".join(parts)


def build_example_prompt(
    settings: PkgSettings,
    api_dump: PublicApiDump,
    config: ProjectConfig,
    filter_group: str | None = None,
) -> str:
    examples_include = _load_examples_include(config)
    if filter_group:
        examples_include = {k: v for k, v in examples_include.items() if k == filter_group}
    if not examples_include:
        return ""

    lookup = _build_symbol_lookup(api_dump)
    sections: list[str] = []

    for group_name, symbol_names in examples_include.items():
        group_dump = next((g for g in api_dump.groups if g.name == group_name), None)
        if not group_dump:
            continue
        filtered = group_dump.filter_symbols(set(symbol_names))
        if not filtered:
            continue

        for symbol in filtered.symbols:
            path = settings.example_file_path(group_name, symbol.name)
            if path.exists():
                continue
            related = _find_related_types(symbol, lookup)
            test_code = _find_test_file(symbol, settings)
            context = _format_symbol_context(symbol, related, test_code)
            sections.append(f"## {group_name}: {symbol.name}\n\nOutput file: {path}\n\n{context}")

    if not sections:
        return ""

    header = f"Use the write-examples skill to create example docs for {api_dump.pkg_import_name}.\nWrite files to: {settings.examples_dir}/\n"
    return header + "\n\n---\n\n".join(["", *sections])
