# GlobalVarDump

<!-- === DO_NOT_EDIT: pkg-ext globalvardump_def === -->
## class: GlobalVarDump
- [source](../../pkg_ext/_internal/models/api_dump.py#L115)
> **Since:** 0.1.0

```python
class GlobalVarDump(SymbolDumpBase):
    name: str
    module_path: str
    docstring: str = ''
    line_number: int | None = None
    type: Literal[global_var] = 'global_var'
    annotation: str | None = None
    value_repr: str | None = None
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
| unreleased | field 'value_repr' default added: None |
| unreleased | field 'line_number' default added: None |
| unreleased | field 'annotation' default added: None |
| unreleased | added base class 'SymbolDumpBase' |
| 0.2.0 | field 'module_path' default removed (was: PydanticUndefined) |
| 0.2.0 | field 'name' default removed (was: PydanticUndefined) |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext globalvardump_changes === -->