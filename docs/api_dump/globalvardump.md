# GlobalVarDump

<!-- === DO_NOT_EDIT: pkg-ext globalvardump_def === -->
## class: GlobalVarDump
- [source](../../pkg_ext/_internal/models/api_dump.py#L105)
> **Since:** 0.1.0

```python
class GlobalVarDump(SymbolDumpBase):
    name: str
    module_path: str
    docstring: str = ''
    line_number: int | None
    type: Literal[global_var] = 'global_var'
    annotation: str | None
    value_repr: str | None
```
<!-- === OK_EDIT: pkg-ext globalvardump_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | - | 0.1.0 |
| module_path | `str` | - | 0.1.0 |
| docstring | `str` | `''` | 0.1.0 |
| line_number | `int | None` | - | 0.1.0 |
| type | `Literal[global_var]` | `'global_var'` | 0.1.0 |
| annotation | `str | None` | - | 0.1.0 |
| value_repr | `str | None` | - | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext globalvardump_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.1.0 | Made public |
| unreleased | field 'module_path' default removed (was: PydanticUndefined) |
| unreleased | field 'name' default removed (was: PydanticUndefined) |
<!-- === OK_EDIT: pkg-ext globalvardump_changes === -->