# TypeAliasDump

<!-- === DO_NOT_EDIT: pkg-ext typealiasdump_def === -->
## class: TypeAliasDump
- [source](../../pkg_ext/_internal/models/api_dump.py#L110)
> **Since:** 0.1.0

```python
class TypeAliasDump(SymbolDumpBase):
    name: str
    module_path: str
    docstring: str = ''
    line_number: int | None = None
    type: Literal[type_alias] = 'type_alias'
    alias_target: str
```
<!-- === OK_EDIT: pkg-ext typealiasdump_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | - | 0.1.0 |
| module_path | `str` | - | 0.1.0 |
| docstring | `str` | `''` | 0.1.0 |
| line_number | `int | None` | - | 0.1.0 |
| type | `Literal[type_alias]` | `'type_alias'` | 0.1.0 |
| alias_target | `str` | - | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext typealiasdump_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.2.0 | field 'alias_target' default removed (was: PydanticUndefined) |
| 0.2.0 | field 'module_path' default removed (was: PydanticUndefined) |
| 0.2.0 | field 'name' default removed (was: PydanticUndefined) |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext typealiasdump_changes === -->