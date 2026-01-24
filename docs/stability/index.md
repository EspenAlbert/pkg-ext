<!-- === DO_NOT_EDIT: pkg-ext header === -->
# stability

<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`dep`](#dep_def)
- [`exp`](#exp_def)
- [`ga`](#ga_def)
<!-- === OK_EDIT: pkg-ext symbols === -->

<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->

<!-- === DO_NOT_EDIT: pkg-ext dep_def === -->
<a id="dep_def"></a>

### cli_command: `dep`
- [source](../../pkg_ext/_internal/cli/stability_cmds.py#L84)
> **Since:** unreleased

```python
def dep(*, target: str = ..., replacement: str | None = ...):
    ...
```

Mark target as deprecated.

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `--target`, `-t` | `str` | *required* | Target: group \| group.symbol \| group.symbol.arg |
| `--replacement`, `-r` | `str | None` | *required* | Replacement suggestion |
<!-- === OK_EDIT: pkg-ext dep_def === -->
<!-- === DO_NOT_EDIT: pkg-ext exp_def === -->
<a id="exp_def"></a>

### cli_command: `exp`
- [source](../../pkg_ext/_internal/cli/stability_cmds.py#L22)
> **Since:** unreleased

```python
def exp(*, target: str = ...):
    ...
```

Mark target as experimental.

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `--target`, `-t` | `str` | *required* | Target: group \| group.symbol \| group.symbol.arg |
<!-- === OK_EDIT: pkg-ext exp_def === -->
<!-- === DO_NOT_EDIT: pkg-ext ga_def === -->
<a id="ga_def"></a>

### cli_command: `ga`
- [source](../../pkg_ext/_internal/cli/stability_cmds.py#L54)
> **Since:** unreleased

```python
def ga(*, target: str = ...):
    ...
```

Graduate target to GA (general availability).

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `--target`, `-t` | `str` | *required* | Target: group \| group.symbol \| group.symbol.arg |
<!-- === OK_EDIT: pkg-ext ga_def === -->