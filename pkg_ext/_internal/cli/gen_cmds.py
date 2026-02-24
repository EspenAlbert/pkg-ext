"""Generation commands: gen_docs."""

import logging
from pathlib import Path

import typer

from pkg_ext._internal.cli.options import option_group, option_output_dir
from pkg_ext._internal.cli.workflow_cmds import generate_docs_for_pkg
from pkg_ext._internal.settings import PkgSettings

logger = logging.getLogger(__name__)


def gen_docs(
    ctx: typer.Context,
    output_dir: Path | None = option_output_dir,
    group: str | None = option_group,
):
    """Generate documentation from public API."""
    settings: PkgSettings = ctx.obj
    count = generate_docs_for_pkg(settings, output_dir=output_dir, filter_group=group)
    docs_dir = output_dir or settings.docs_dir
    logger.info(f"Generated {count} doc files in {docs_dir}")
