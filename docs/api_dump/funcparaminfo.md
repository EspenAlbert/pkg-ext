# FuncParamInfo

<!-- === DO_NOT_EDIT: pkg-ext funcparaminfo_def === -->
## class: FuncParamInfo
- [source](../../pkg_ext/_internal/models/api_dump.py#L26)
> **Since:** 0.1.0

```python
class FuncParamInfo(Entity):
    name: str
    kind: ParamKind
    type_annotation: str | None = None
    type_imports: list[str] = ...
    default: ParamDefault | None = None
```
<!-- === OK_EDIT: pkg-ext funcparaminfo_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | - | 0.1.0 |
| kind | `ParamKind` | - | 0.1.0 |
| type_annotation | `str | None` | - | 0.1.0 |
| type_imports | `list[str]` | `...` | 0.1.0 |
| default | `ParamDefault | None` | - | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext funcparaminfo_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | field 'type_annotation' default added: None |
| unreleased | field 'default' default added: None |
| unreleased | added base class 'Entity' |
| 0.2.0 | field 'kind' default removed (was: PydanticUndefined) |
| 0.2.0 | field 'name' default removed (was: PydanticUndefined) |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext funcparaminfo_changes === -->