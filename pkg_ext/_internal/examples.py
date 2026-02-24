from __future__ import annotations

import contextlib
import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING

from model_lib import Entity
from model_lib.serialize.yaml_serialize import parse_yaml_str

from pkg_ext._internal.config import GroupConfig, ProjectConfig, load_project_config
from pkg_ext._internal.generation.docs_render import format_signature
from pkg_ext._internal.models.api_dump import (
    ClassDump,
    FunctionDump,
    GroupDump,
    PublicApiDump,
    SymbolDumpBase,
)

if TYPE_CHECKING:
    from pkg_ext._internal.settings import PkgSettings

logger = logging.getLogger(__name__)

_COMMENT_PATTERN = re.compile(r"\A<!--\s*\n(?P<body>.*?)\n-->\s*\n", re.DOTALL)


class ExampleMetadata(Entity):
    description: str = ""


def parse_description_comment(path: Path) -> str:
    text = path.read_text()
    if comment_match := _COMMENT_PATTERN.match(text):
        with contextlib.suppress(Exception):
            raw = parse_yaml_str(comment_match.group("body"))
            meta = ExampleMetadata.model_validate(raw)
            if meta.description:
                return meta.description
    return path.stem


def _load_examples_include(config: ProjectConfig) -> dict[str, list[str]]:
    return {name: group_cfg.examples_include for name, group_cfg in config.groups.items() if group_cfg.examples_include}


def filter_group_by_examples_include(group: GroupDump, config: ProjectConfig) -> GroupDump | None:
    group_cfg = config.groups.get(group.name, GroupConfig())
    if not group_cfg.examples_include:
        return None
    return group.filter_symbols(set(group_cfg.examples_include))


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


def _format_related_type(rt: SymbolDumpBase) -> str:
    sig = format_signature(rt)  # type: ignore[arg-type]
    return f"### {rt.name}\n```python\n{sig}\n```"


def _format_symbol_context(
    symbol: SymbolDumpBase,
    related_types: list[SymbolDumpBase],
    test_code: str,
) -> str:
    parts: list[str] = []

    sig = format_signature(symbol)  # type: ignore[arg-type]
    parts.append(f"**Signature:**\n```python\n{sig}\n```")

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
