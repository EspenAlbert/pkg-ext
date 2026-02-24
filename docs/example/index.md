<!-- === DO_NOT_EDIT: pkg-ext header === -->
# example

<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`check_examples`](#check_examples_def)
- [`gen_example_prompt`](#gen_example_prompt_def)
<!-- === OK_EDIT: pkg-ext symbols === -->

<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->

<!-- === DO_NOT_EDIT: pkg-ext check_examples_def === -->
<a id="check_examples_def"></a>

### cli_command: `check_examples`
- [source](../../pkg_ext/_internal/cli/example_cmds.py#L33)
> **Since:** unreleased

```python
def check_examples():
    ...
```

Verify all symbols in examples_include have corresponding .md files.

### Changes

| Version | Change |
|---------|--------|
| unreleased | Made public |
<!-- === OK_EDIT: pkg-ext check_examples_def === -->
<!-- === DO_NOT_EDIT: pkg-ext gen_example_prompt_def === -->
<a id="gen_example_prompt_def"></a>

### cli_command: `gen_example_prompt`
- [source](../../pkg_ext/_internal/cli/example_cmds.py#L16)
> **Since:** unreleased

```python
def gen_example_prompt(*, group: str | None = ...):
    ...
```

Build an AI prompt for missing example docs and copy to clipboard.

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `-g`, `--group` | `str | None` | *required* | Generate for specific group only |

### Changes

| Version | Change |
|---------|--------|
| unreleased | Made public |
<!-- === OK_EDIT: pkg-ext gen_example_prompt_def === -->