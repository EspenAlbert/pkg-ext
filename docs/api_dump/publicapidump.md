# PublicApiDump

<!-- === DO_NOT_EDIT: pkg-ext publicapidump_def === -->
## class: PublicApiDump
- [source](../../pkg_ext/_internal/models/api_dump.py#L138)
> **Since:** 0.1.0

```python
class PublicApiDump(Entity):
    pkg_import_name: str
    version: str
    groups: list[GroupDump] = ...
    dumped_at: datetime
```
<!-- === OK_EDIT: pkg-ext publicapidump_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| pkg_import_name | `str` | - | 0.1.0 |
| version | `str` | - | 0.1.0 |
| groups | `list[GroupDump]` | `...` | 0.1.0 |
| dumped_at | `datetime` | - | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext publicapidump_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | added base class 'Entity' |
| 0.2.0 | field 'pkg_import_name' default removed (was: PydanticUndefined) |
| 0.2.0 | field 'version' default removed (was: PydanticUndefined) |
| 0.2.0 | field 'dumped_at' default removed (was: PydanticUndefined) |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext publicapidump_changes === -->