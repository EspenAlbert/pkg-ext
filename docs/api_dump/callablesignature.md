# CallableSignature

<!-- === DO_NOT_EDIT: pkg-ext callablesignature_def === -->
## class: CallableSignature
- [source](../../pkg_ext/_internal/models/api_dump.py#L34)
> **Since:** 0.1.0

```python
class CallableSignature(Entity):
    parameters: list[FuncParamInfo] = ...
    return_annotation: str | None = None
    return_type_imports: list[str] = ...
```
<!-- === OK_EDIT: pkg-ext callablesignature_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| parameters | `list[FuncParamInfo]` | `...` | 0.1.0 |
| return_annotation | `str | None` | `None` | unreleased |
| return_type_imports | `list[str]` | `...` | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext callablesignature_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | field 'return_annotation' default added: None |
| 0.3.0 | added base class 'Entity' |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext callablesignature_changes === -->