import logging
import os

import typer

from pkg_ext._internal.cli.options import option_group
from pkg_ext._internal.cli.workflows import create_api_dump
from pkg_ext._internal.clipboard import add_to_clipboard
from pkg_ext._internal.config import load_project_config
from pkg_ext._internal.examples import build_example_prompt, check_examples_exist
from pkg_ext._internal.settings import PkgSettings

logger = logging.getLogger(__name__)


def gen_example_prompt(
    ctx: typer.Context,
    group: str | None = option_group,
):
    """Build an AI prompt for missing example docs and copy to clipboard."""
    settings: PkgSettings = ctx.obj
    api_dump = create_api_dump(settings)
    config = load_project_config(settings.state_dir)
    prompt = build_example_prompt(settings, api_dump, config, filter_group=group)
    if prompt:
        add_to_clipboard(prompt)
        symbol_count = prompt.count("\n## ")
        logger.info(f"Prompt generated for {symbol_count} symbol(s)")
    else:
        logger.info("All examples already exist")


def check_examples(ctx: typer.Context):
    """Verify all symbols in examples_include have corresponding .md files."""
    if os.getenv("SKIP_EXAMPLES_CHECK") == "1":
        logger.info("Skipping examples check (SKIP_EXAMPLES_CHECK=1)")
        return
    settings: PkgSettings = ctx.obj
    missing = check_examples_exist(settings)
    if missing:
        logger.error("Missing example files:")
        for group, symbol, path in missing:
            logger.error(f"  {group}/{symbol}: {path}")
        raise typer.Exit(1)
    logger.info("All required examples exist")
