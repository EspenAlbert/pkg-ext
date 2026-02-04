# FunctionDump

<!-- === DO_NOT_EDIT: pkg-ext functiondump_def === -->
## class: FunctionDump
- [source](../../pkg_ext/_internal/models/api_dump.py#L59)
> **Since:** 0.1.0

```python
class FunctionDump(SymbolDumpBase):
    name: str
    module_path: str
    docstring: str = ''
    line_number: int | None = None
    type: Literal[function] = 'function'
    signature: CallableSignature
```
<!-- === OK_EDIT: pkg-ext functiondump_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | - | 0.1.0 |
| module_path | `str` | - | 0.1.0 |
| docstring | `str` | `''` | 0.1.0 |
| line_number | `int | None` | - | 0.1.0 |
| type | `Literal[function]` | `'function'` | 0.1.0 |
| signature | `CallableSignature` | - | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext functiondump_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | field 'line_number' default added: None |
| unreleased | added base class 'SymbolDumpBase' |
| 0.2.0 | field 'module_path' default removed (was: PydanticUndefined) |
| 0.2.0 | field 'signature' default removed (was: PydanticUndefined) |
| 0.2.0 | field 'name' default removed (was: PydanticUndefined) |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext functiondump_changes === -->