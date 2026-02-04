# CLIParamInfo

<!-- === DO_NOT_EDIT: pkg-ext cliparaminfo_def === -->
## class: CLIParamInfo
- [source](../../pkg_ext/_internal/models/api_dump.py#L64)
> **Since:** 0.1.0

```python
class CLIParamInfo(Entity):
    param_name: str
    type_annotation: str | None = None
    flags: list[str] = ...
    help: str | None = None
    default_repr: str | None = None
    required: bool = False
    envvar: str | None = None
    is_argument: bool = False
    hidden: bool = False
    choices: list[str] | None = None
```

CLI parameter metadata from typer OptionInfo/ArgumentInfo.
<!-- === OK_EDIT: pkg-ext cliparaminfo_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| param_name | `str` | - | 0.1.0 |
| type_annotation | `str | None` | - | 0.1.0 |
| flags | `list[str]` | `...` | 0.1.0 |
| help | `str | None` | - | 0.1.0 |
| default_repr | `str | None` | - | 0.1.0 |
| required | `bool` | `False` | 0.1.0 |
| envvar | `str | None` | - | 0.1.0 |
| is_argument | `bool` | `False` | 0.1.0 |
| hidden | `bool` | `False` | 0.1.0 |
| choices | `list[str] | None` | - | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext cliparaminfo_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.2.0 | field 'param_name' default removed (was: PydanticUndefined) |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext cliparaminfo_changes === -->