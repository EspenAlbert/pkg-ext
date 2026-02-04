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
    line_number: int | None = None
    type: Literal[class] = 'class'
    mro_bases: list[str] = ...
    num_direct_bases: int = 0
    init_signature: CallableSignature | None = None
    fields: list[ClassFieldInfo] | None = None
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
| unreleased | field 'init_signature' default added: None |
| unreleased | field 'line_number' default added: None |
| unreleased | field 'fields' default added: None |
| unreleased | added optional field 'num_direct_bases' (default: 0) |
| unreleased | added optional field 'mro_bases' (default: ...) |
| unreleased | removed field 'direct_bases' |
| unreleased | added base class 'SymbolDumpBase' |
| 0.2.0 | field 'module_path' default removed (was: PydanticUndefined) |
| 0.2.0 | field 'name' default removed (was: PydanticUndefined) |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext classdump_changes === -->