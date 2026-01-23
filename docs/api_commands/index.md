<!-- === DO_NOT_EDIT: pkg-ext header === -->
# api_commands

<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`diff_api`](#diff_api_def)
- [`dump_api`](#dump_api_def)
<!-- === OK_EDIT: pkg-ext symbols === -->

<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->

<!-- === DO_NOT_EDIT: pkg-ext diff_api_def === -->
<a id="diff_api_def"></a>

### cli_command: `diff_api`
- [source](../../pkg_ext/_internal/cli/api_cmds.py#L36)
> **Since:** unreleased

```python
def diff_api(*, baseline_ref: str | None = ...):
    ...
```

Show API changes between baseline and dev dump.

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `--baseline` | `str | None` | *required* | Git tag/ref to compare against (default: {pkg}.api.yaml file) |
<!-- === OK_EDIT: pkg-ext diff_api_def === -->
<!-- === DO_NOT_EDIT: pkg-ext dump_api_def === -->
<a id="dump_api_def"></a>

### cli_command: `dump_api`
- [source](../../pkg_ext/_internal/cli/api_cmds.py#L20)
> **Since:** unreleased

```python
def dump_api(*, output: Path | None = ..., dev: bool = False):
    ...
```

Dump public API to YAML for diffing and breaking change detection.

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `-o`, `--output` | `Path | None` | *required* | Output file path |
| `--dev` | `bool` | `False` | Write to -dev file (gitignored for local comparison) |
<!-- === OK_EDIT: pkg-ext dump_api_def === -->