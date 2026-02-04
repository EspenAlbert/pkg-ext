<!-- === DO_NOT_EDIT: pkg-ext header === -->
# api_dump

<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [CLICommandDump](./clicommanddump.md)
- [CLIParamInfo](./cliparaminfo.md)
- [`CallableSignature`](#callablesignature_def)
- [ClassDump](./classdump.md)
- [ClassFieldInfo](./classfieldinfo.md)
- [ExceptionDump](./exceptiondump.md)
- [FuncParamInfo](./funcparaminfo.md)
- [FunctionDump](./functiondump.md)
- [GlobalVarDump](./globalvardump.md)
- [GroupDump](./groupdump.md)
- [ParamDefault](./paramdefault.md)
- [`ParamKind`](#paramkind_def)
- [PublicApiDump](./publicapidump.md)
- [TypeAliasDump](./typealiasdump.md)
<!-- === OK_EDIT: pkg-ext symbols === -->

<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->

<!-- === DO_NOT_EDIT: pkg-ext callablesignature_def === -->
<a id="callablesignature_def"></a>

### class: `CallableSignature`
- [source](../../pkg_ext/_internal/models/api_dump.py#L34)
> **Since:** 0.1.0

```python
class CallableSignature(Entity):
    parameters: list[FuncParamInfo] = ...
    return_annotation: str | None = None
    return_type_imports: list[str] = ...
```

| Field | Type | Default | Since |
|---|---|---|---|
| parameters | `list[FuncParamInfo]` | `...` | 0.1.0 |
| return_annotation | `str | None` | `None` | 0.1.0 |
| return_type_imports | `list[str]` | `...` | 0.1.0 |

### Changes

| Version | Change |
|---------|--------|
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext callablesignature_def === -->
<!-- === DO_NOT_EDIT: pkg-ext paramkind_def === -->
<a id="paramkind_def"></a>

### class: `ParamKind`
- [source](../../pkg_ext/_internal/models/api_dump.py#L13)
> **Since:** 0.1.0

```python
class ParamKind(StrEnum):
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext paramkind_def === -->