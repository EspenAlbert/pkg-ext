# ExceptionDump

<!-- === DO_NOT_EDIT: pkg-ext exceptiondump_def === -->
## class: ExceptionDump
- [source](../../pkg_ext/_internal/models/api_dump.py#L99)
> **Since:** 0.1.0

```python
class ExceptionDump(SymbolDumpBase):
    name: str
    module_path: str
    docstring: str = ''
    line_number: int | None = None
    type: Literal[exception] = 'exception'
    mro_bases: list[str] = ...
    num_direct_bases: int = 0
    init_signature: CallableSignature | None = None
```
<!-- === OK_EDIT: pkg-ext exceptiondump_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | - | 0.1.0 |
| module_path | `str` | - | 0.1.0 |
| docstring | `str` | `''` | 0.1.0 |
| line_number | `int | None` | - | 0.1.0 |
| type | `Literal[exception]` | `'exception'` | 0.1.0 |
| direct_bases | `list[str]` | `...` | 0.1.0 |
| init_signature | `CallableSignature | None` | - | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext exceptiondump_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | field 'init_signature' default added: None |
| 0.3.0 | field 'line_number' default added: None |
| 0.3.0 | added optional field 'num_direct_bases' (default: 0) |
| 0.3.0 | added optional field 'mro_bases' (default: ...) |
| 0.3.0 | removed field 'direct_bases' |
| 0.3.0 | added base class 'SymbolDumpBase' |
| 0.2.0 | field 'module_path' default removed (was: PydanticUndefined) |
| 0.2.0 | field 'name' default removed (was: PydanticUndefined) |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext exceptiondump_changes === -->