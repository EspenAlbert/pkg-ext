# ParamDefault

<!-- === DO_NOT_EDIT: pkg-ext paramdefault_def === -->
## class: ParamDefault
- [source](../../pkg_ext/_internal/models/api_dump.py#L21)
> **Since:** 0.1.0

```python
class ParamDefault(Entity):
    value_repr: str
    is_factory: bool = False
```
<!-- === OK_EDIT: pkg-ext paramdefault_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| value_repr | `str` | - | 0.1.0 |
| is_factory | `bool` | `False` | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext paramdefault_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.2.0 | field 'value_repr' default removed (was: PydanticUndefined) |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext paramdefault_changes === -->