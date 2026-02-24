"""Generate mkdocs-compatible markdown files from PublicApiDump."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from model_lib import Entity
from zero_3rdparty.sections import slug, wrap_section

from pkg_ext._internal.changelog.actions import ChangelogAction
from pkg_ext._internal.config import (
    PKG_EXT_TOOL_NAME,
    ROOT_GROUP_NAME,
    GroupConfig,
    ProjectConfig,
)
from pkg_ext._internal.examples import parse_description_comment
from pkg_ext._internal.generation.docs_constants import MD_CONFIG, ROOT_DIR
from pkg_ext._internal.generation.docs_render import (
    render_inline_symbol,
    render_symbol_page,
)
from pkg_ext._internal.generation.docs_version import (
    MEANINGFUL_CHANGE_ACTIONS,
    build_symbol_changes,
)
from pkg_ext._internal.models.api_dump import ClassDump, GroupDump, PublicApiDump, SymbolDump

logger = logging.getLogger(__name__)


class GeneratedDocsOutput(Entity):
    path_contents: dict[str, str]


@dataclass
class SymbolContext:
    symbol: SymbolDump
    has_env_vars: bool = False
    has_meaningful_changes: bool = False
    is_primary: bool = False

    @property
    def needs_own_page(self) -> bool:
        if self.is_primary:
            return False
        return self.has_env_vars or self.has_meaningful_changes

    @property
    def page_filename(self) -> str:
        return f"{slug(self.symbol.name)}.md"


def group_dir_name(group: GroupDump) -> str:
    return ROOT_DIR if group.name == ROOT_GROUP_NAME else group.name


def has_env_vars(symbol: SymbolDump) -> bool:
    if not isinstance(symbol, ClassDump):
        return False
    if not symbol.fields:
        return False
    return any(f.env_vars for f in symbol.fields)


def build_symbol_context(
    symbol: SymbolDump,
    group_name: str,
    changelog_actions: list[ChangelogAction],
) -> SymbolContext:
    has_changes = any(
        action.name == symbol.name and isinstance(action, MEANINGFUL_CHANGE_ACTIONS) for action in changelog_actions
    )
    is_primary = symbol.name.lower() == group_name.lower()
    return SymbolContext(
        symbol=symbol,
        has_env_vars=has_env_vars(symbol),
        has_meaningful_changes=has_changes,
        is_primary=is_primary,
    )


def render_symbol_entry(ctx: SymbolContext) -> str:
    name = ctx.symbol.name
    if ctx.needs_own_page:
        return f"- [{name}](./{slug(name)}.md)"
    return f"- [`{name}`](#{slug(name)}_def)"


def _build_example_link(
    symbol_name: str,
    group_name: str,
    examples_set: set[str],
    examples_dir: Path | None,
    relative_prefix: str,
) -> tuple[str, str] | None:
    if symbol_name not in examples_set:
        return None
    url = f"{relative_prefix}{group_name}/{symbol_name}.md"
    desc = ""
    if examples_dir:
        path = examples_dir / group_name / f"{symbol_name}.md"
        if path.exists():
            desc = parse_description_comment(path)
    return (url, desc)


def render_group_index(
    group: GroupDump,
    contexts: list[SymbolContext],
    group_config: GroupConfig,
    changelog_actions: Sequence[ChangelogAction] | None = None,
    *,
    docs_dir: Path | None = None,
    pkg_src_dir: Path | None = None,
    pkg_import_name: str | None = None,
) -> str:
    dir_name = group_dir_name(group)
    index_path = docs_dir / dir_name / "index.md" if docs_dir else None
    examples_dir = docs_dir / "examples" if docs_dir else None

    primary_ctx = next((c for c in contexts if c.is_primary), None)
    other_contexts = sorted([c for c in contexts if not c.is_primary], key=lambda c: c.symbol.name)
    sorted_contexts = [primary_ctx, *other_contexts] if primary_ctx else other_contexts

    header_name = primary_ctx.symbol.name if primary_ctx else group.name
    header = f"# {header_name}\n"
    if group_config.docstring:
        header += f"\n{group_config.docstring}\n"

    symbol_entries = [render_symbol_entry(c) for c in sorted_contexts]
    symbol_list = "\n".join(symbol_entries)

    examples_set = set(group_config.examples_include)
    inline_sections = []
    changelog_actions_list = list(changelog_actions) if changelog_actions else []
    for ctx in sorted_contexts:
        if not ctx.needs_own_page:
            section_id = f"{slug(ctx.symbol.name)}_def"
            symbol_changes = build_symbol_changes(ctx.symbol.name, changelog_actions_list)
            example_link = _build_example_link(ctx.symbol.name, group.name, examples_set, examples_dir, "../examples/")
            inline_content = render_inline_symbol(
                ctx,
                changelog_actions,
                symbol_changes,
                symbol_doc_path=index_path,
                pkg_src_dir=pkg_src_dir,
                pkg_import_name=pkg_import_name,
                example_link=example_link,
            )
            inline_sections.append(wrap_section(inline_content, section_id, PKG_EXT_TOOL_NAME, MD_CONFIG))

    parts = [
        wrap_section(header, "header", PKG_EXT_TOOL_NAME, MD_CONFIG),
        "",
        wrap_section(symbol_list, "symbols", PKG_EXT_TOOL_NAME, MD_CONFIG),
    ]

    other_inline_contexts = [c for c in other_contexts if not c.needs_own_page]
    if other_inline_contexts:
        parts.extend(
            (
                "",
                wrap_section(
                    "## Symbol Details",
                    "symbol_details_header",
                    PKG_EXT_TOOL_NAME,
                    MD_CONFIG,
                ),
                "",
                *inline_sections,
            )
        )
    elif inline_sections:
        parts.extend(("", *inline_sections))

    return "\n".join(parts)


def generate_docs(
    api_dump: PublicApiDump,
    config: ProjectConfig,
    changelog_actions: list[ChangelogAction],
    docs_dir: Path | None = None,
    pkg_src_dir: Path | None = None,
) -> GeneratedDocsOutput:
    path_contents: dict[str, str] = {}
    pkg_import_name = api_dump.pkg_import_name

    examples_dir = docs_dir / "examples" if docs_dir else None

    for group in api_dump.groups:
        dir_name = group_dir_name(group)
        group_config = config.groups.get(group.name, GroupConfig())
        examples_set = set(group_config.examples_include)
        contexts = [build_symbol_context(s, group.name, changelog_actions) for s in group.symbols]
        index_path = f"{dir_name}/index.md"
        path_contents[index_path] = render_group_index(
            group,
            contexts,
            group_config,
            changelog_actions,
            docs_dir=docs_dir,
            pkg_src_dir=pkg_src_dir,
            pkg_import_name=pkg_import_name,
        )

        for ctx in contexts:
            if ctx.needs_own_page:
                symbol_path = f"{dir_name}/{ctx.page_filename}"
                if docs_dir and pkg_src_dir:
                    symbol_doc_path = docs_dir / symbol_path
                    symbol_changes = build_symbol_changes(ctx.symbol.name, changelog_actions)
                    example_link = _build_example_link(
                        ctx.symbol.name, group.name, examples_set, examples_dir, "../examples/"
                    )
                    path_contents[symbol_path] = render_symbol_page(
                        ctx,
                        group,
                        symbol_doc_path,
                        pkg_src_dir,
                        pkg_import_name,
                        changes=symbol_changes,
                        changelog_actions=changelog_actions,
                        has_env_vars_fn=has_env_vars,
                        example_link=example_link,
                    )
                else:
                    path_contents[symbol_path] = f"# {ctx.symbol.name}\n"

    return GeneratedDocsOutput(path_contents=path_contents)
