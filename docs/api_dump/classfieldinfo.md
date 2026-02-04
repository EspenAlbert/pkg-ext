# ClassFieldInfo

<!-- === DO_NOT_EDIT: pkg-ext classfieldinfo_def === -->
## class: ClassFieldInfo
- [source](../../pkg_ext/_internal/models/api_dump.py#L40)
> **Since:** 0.1.0

```python
class ClassFieldInfo(Entity):
    name: str
    type_annotation: str | None = None
    type_imports: list[str] = ...
    default: ParamDefault | None = None
    is_class_var: bool = False
    is_computed: bool = False
    description: str | None = None
    deprecated: str | None = None
    env_vars: list[str] | None = None
```
<!-- === OK_EDIT: pkg-ext classfieldinfo_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | - | 0.1.0 |
| type_annotation | `str | None` | - | 0.1.0 |
| type_imports | `list[str]` | `...` | 0.1.0 |
| default | `ParamDefault | None` | - | 0.1.0 |
| is_class_var | `bool` | `False` | 0.1.0 |
| is_computed | `bool` | `False` | 0.1.0 |
| description | `str | None` | - | 0.1.0 |
| deprecated | `str | None` | - | 0.1.0 |
| env_vars | `list[str] | None` | - | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext classfieldinfo_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | field 'type_annotation' default added: None |
| 0.3.0 | field 'default' default added: None |
| 0.3.0 | field 'env_vars' default added: None |
| 0.3.0 | field 'deprecated' default added: None |
| 0.3.0 | field 'description' default added: None |
| 0.3.0 | added base class 'Entity' |
| 0.2.0 | field 'name' default removed (was: PydanticUndefined) |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext classfieldinfo_changes === -->