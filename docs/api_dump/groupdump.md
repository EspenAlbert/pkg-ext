# GroupDump

<!-- === DO_NOT_EDIT: pkg-ext groupdump_def === -->
## class: GroupDump
- [source](../../pkg_ext/_internal/models/api_dump.py#L127)
> **Since:** 0.1.0

```python
class GroupDump(Entity):
    name: str
    symbols: list[Annotated[FunctionDump | CLICommandDump | ClassDump | ExceptionDump | TypeAliasDump | GlobalVarDump, annotation=NoneType required=True discriminator='type']] = ...
```
<!-- === OK_EDIT: pkg-ext groupdump_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | - | 0.1.0 |
| symbols | `list[Annotated[FunctionDump | CLICommandDump | ClassDump | ExceptionDump | TypeAliasDump | GlobalVarDump, annotation=NoneType required=True discriminator='type']]` | `...` | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext groupdump_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | added base class 'Entity' |
| 0.2.0 | field 'name' default removed (was: PydanticUndefined) |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext groupdump_changes === -->