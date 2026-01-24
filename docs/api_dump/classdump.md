# ClassDump

<!-- === DO_NOT_EDIT: pkg-ext classdump_def === -->
## class: ClassDump
- [source](../../pkg_ext/_internal/models/api_dump.py#L87)
> **Since:** 0.1.0

```python
class ClassDump(SymbolDumpBase):
    name: str
    module_path: str
    docstring: str = ''
    line_number: int | None
    type: Literal[class] = 'class'
    direct_bases: list[str] = ...
    init_signature: CallableSignature | None
    fields: list[ClassFieldInfo] | None
```
<!-- === OK_EDIT: pkg-ext classdump_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | - | 0.1.0 |
| module_path | `str` | - | 0.1.0 |
| docstring | `str` | `''` | 0.1.0 |
| line_number | `int | None` | - | 0.1.0 |
| type | `Literal[class]` | `'class'` | 0.1.0 |
| direct_bases | `list[str]` | `...` | 0.1.0 |
| init_signature | `CallableSignature | None` | - | 0.1.0 |
| fields | `list[ClassFieldInfo] | None` | - | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext classdump_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.1.0 | Made public |
| unreleased | field 'module_path' default removed (was: PydanticUndefined) |
| unreleased | field 'name' default removed (was: PydanticUndefined) |
<!-- === OK_EDIT: pkg-ext classdump_changes === -->