<!-- === DO_NOT_EDIT: pkg-ext header === -->
# changelog

<!-- === OK_EDIT: pkg-ext header === -->
<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`chore`](#chore_def)
- [`promote`](#promote_def)
- [`release_notes`](#release_notes_def)
<!-- === OK_EDIT: pkg-ext symbols === -->
<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->
<!-- === DO_NOT_EDIT: pkg-ext release_notes_def === -->
<a id="release_notes_def"></a>

### cli_command: `release_notes`
- [source](../../pkg_ext/_internal/cli/changelog_cmds.py#L121)
> **Since:** 0.1.0

```python
def release_notes(*, tag_name: str = ...):
    ...
```

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `--tag` | `str` | *required* | tag to find release notes for |

### Changes

| Version | Change |
|---------|--------|
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext release_notes_def === -->
<!-- === DO_NOT_EDIT: pkg-ext chore_def === -->
<a id="chore_def"></a>

### cli_command: `chore`
- [source](../../pkg_ext/_internal/cli/changelog_cmds.py#L43)
> **Since:** 0.1.0

```python
def chore(*, description: str = ..., pr_number: int = 0):
    ...
```

Create a ChoreAction for internal changes that warrant a release.

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `--description`, `-d` | `str` | *required* | Description of internal changes (e.g., 'CI improvements', 'Dependency updates') |
| `--pr` | `int` | `0` | PR number (auto-detected from current branch if not provided) |

### Changes

| Version | Change |
|---------|--------|
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext chore_def === -->
<!-- === DO_NOT_EDIT: pkg-ext promote_def === -->
<a id="promote_def"></a>

### cli_command: `promote`
- [source](../../pkg_ext/_internal/cli/changelog_cmds.py#L66)
> **Since:** 0.1.0

```python
def promote(*, name: str | None = ..., group: str | None = ..., module_filter: str | None = ..., pattern: str | None = ..., undecided: bool = False, pr_number: int = 0):
    ...
```

Promote symbols to public API (private or undecided).

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `--name`, `-n` | `str | None` | *required* | Symbol name to promote |
| `--group`, `-g` | `str | None` | *required* | Target group |
| `--module`, `-m` | `str | None` | *required* | Filter by module path prefix (inside the package, don't include the package name) |
| `--pattern`, `-p` | `str | None` | *required* | Filter by name pattern (e.g., 'dump_*') |
| `--undecided`, `-u` | `bool` | `False` | Include symbols without changelog entry (not yet decided) |
| `--pr` | `int` | `0` | PR number (auto-detected if not provided) |

### Changes

| Version | Change |
|---------|--------|
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext promote_def === -->