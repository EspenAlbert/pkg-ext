<!-- === DO_NOT_EDIT: pkg-ext header === -->
# generate

<!-- === OK_EDIT: pkg-ext header === -->
<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`gen_docs`](#gen_docs_def)
- [`gen_tests`](#gen_tests_def)
<!-- === OK_EDIT: pkg-ext symbols === -->
<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->
<!-- === DO_NOT_EDIT: pkg-ext gen_docs_def === -->
<a id="gen_docs_def"></a>

### cli_command: `gen_docs`
- [source](../../pkg_ext/_internal/cli/gen_cmds.py#L30)
> **Since:** 0.1.0

```python
def gen_docs(*, output_dir: Path | None = ..., group: str | None = ...):
    ...
```

Generate documentation from public API.

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `-o`, `--output-dir` | `Path | None` | *required* | Output directory (default: docs/) |
| `-g`, `--group` | `str | None` | *required* | Generate for specific group only |

### Changes

| Version | Change |
|---------|--------|
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext gen_docs_def === -->
<!-- === DO_NOT_EDIT: pkg-ext gen_tests_def === -->
<a id="gen_tests_def"></a>

### cli_command: `gen_tests`
- [source](../../pkg_ext/_internal/cli/gen_cmds.py#L19)
> **Since:** 0.1.0

```python
def gen_tests(*, group: str | None = ...):
    ...
```

Generate parameterized test files from examples.

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `-g`, `--group` | `str | None` | *required* | Generate for specific group only |

### Changes

| Version | Change |
|---------|--------|
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext gen_tests_def === -->