# Contributing to Pkg Ext

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) for dependency management
- [gh CLI](https://cli.github.com/) for PR info detection

## Local Development Setup

```bash
git clone <repo>
cd pkg-ext
uv sync
```

Run the CLI locally:

```bash
uv run pkg-ext --help
```

## Running Tests

```bash
uv run pytest
```

## Development Cycle

1. Create branch, make code changes
2. Run `pkg-ext pre-change` - prompts for new/removed symbols, generates scaffolds
3. Fill in examples, run tests locally
4. Run `pkg-ext pre-commit` - validates decisions, updates `-dev` files and docs
5. Commit and push
6. CI runs `pkg-ext pre-commit` - validates all decisions, regenerates docs
7. After merge, CI runs `pkg-ext post-merge` - bumps version, writes real files, creates tag

## Stability Workflow

1. Mark new group as experimental: `pkg-ext exp --target new_group`
2. Develop features, symbols auto-inherit group stability
3. Graduate to GA: `pkg-ext ga --target new_group`
4. Mark arg for deprecation: `pkg-ext dep --target group.func.old_arg --replacement new_arg`

## Git Hook Setup

**Manual hook** (`.git/hooks/pre-commit`):

```bash
#!/bin/bash
pkg-ext pre-commit
```

**[pre-commit](https://pre-commit.com/) framework** (`.pre-commit-config.yaml`):

```yaml
repos:
  - repo: local
    hooks:
      - id: pkg-ext
        name: pkg-ext pre-commit
        entry: pkg-ext pre-commit
        language: system
        pass_filenames: false
```

## Extending the CLI

New commands are added in `pkg_ext/_internal/cli/`. Each command module exports a Typer app that is registered in the main CLI.

To add a command:
1. Create `pkg_ext/_internal/cli/your_command.py`
2. Define a Typer app with your command logic
3. Register it in the main CLI entry point

See existing commands in `workflows.py`, `stability.py` for patterns.

## Submitting PRs

1. Ensure `pkg-ext pre-commit` passes
2. Add changelog entries via `pkg-ext pre-change` for API changes
3. Run tests locally before pushing
4. CI validates all decisions are made and docs are up-to-date
