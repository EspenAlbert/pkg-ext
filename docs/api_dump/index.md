<!-- === DO_NOT_EDIT: pkg-ext header === -->
# api_dump

<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`CLICommandDump`](#clicommanddump_def)
- [`CLIParamInfo`](#cliparaminfo_def)
- [`CallableSignature`](#callablesignature_def)
- [`ClassDump`](#classdump_def)
- [`ClassFieldInfo`](#classfieldinfo_def)
- [`ExceptionDump`](#exceptiondump_def)
- [`FuncParamInfo`](#funcparaminfo_def)
- [`FunctionDump`](#functiondump_def)
- [`GlobalVarDump`](#globalvardump_def)
- [`GroupDump`](#groupdump_def)
- [`ParamDefault`](#paramdefault_def)
- [`ParamKind`](#paramkind_def)
- [`PublicApiDump`](#publicapidump_def)
- [`TypeAliasDump`](#typealiasdump_def)
<!-- === OK_EDIT: pkg-ext symbols === -->

<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->

<!-- === DO_NOT_EDIT: pkg-ext clicommanddump_def === -->
<a id="clicommanddump_def"></a>

### class: `CLICommandDump`
- [source](../../pkg_ext/_internal/models/api_dump.py#L79)
> **Since:** 0.1.0

```python
class CLICommandDump(SymbolDumpBase):
    name: str = PydanticUndefined
    module_path: str = PydanticUndefined
    docstring: str = ''
    line_number: int | None
    type: Literal[cli_command] = 'cli_command'
    signature: CallableSignature = PydanticUndefined
    cli_params: list[CLIParamInfo] = ...
```

A typer CLI command with rich parameter metadata.

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | `PydanticUndefined` | 0.1.0 |
| module_path | `str` | `PydanticUndefined` | 0.1.0 |
| docstring | `str` | `''` | 0.1.0 |
| line_number | `int | None` | - | 0.1.0 |
| type | `Literal[cli_command]` | `'cli_command'` | 0.1.0 |
| signature | `CallableSignature` | `PydanticUndefined` | 0.1.0 |
| cli_params | `list[CLIParamInfo]` | `...` | 0.1.0 |
<!-- === OK_EDIT: pkg-ext clicommanddump_def === -->
<!-- === DO_NOT_EDIT: pkg-ext cliparaminfo_def === -->
<a id="cliparaminfo_def"></a>

### class: `CLIParamInfo`
- [source](../../pkg_ext/_internal/models/api_dump.py#L64)
> **Since:** 0.1.0

```python
class CLIParamInfo(Entity):
    param_name: str = PydanticUndefined
    type_annotation: str | None
    flags: list[str] = ...
    help: str | None
    default_repr: str | None
    required: bool = False
    envvar: str | None
    is_argument: bool = False
    hidden: bool = False
    choices: list[str] | None
```

CLI parameter metadata from typer OptionInfo/ArgumentInfo.

| Field | Type | Default | Since |
|---|---|---|---|
| param_name | `str` | `PydanticUndefined` | 0.1.0 |
| type_annotation | `str | None` | - | 0.1.0 |
| flags | `list[str]` | `...` | 0.1.0 |
| help | `str | None` | - | 0.1.0 |
| default_repr | `str | None` | - | 0.1.0 |
| required | `bool` | `False` | 0.1.0 |
| envvar | `str | None` | - | 0.1.0 |
| is_argument | `bool` | `False` | 0.1.0 |
| hidden | `bool` | `False` | 0.1.0 |
| choices | `list[str] | None` | - | 0.1.0 |
<!-- === OK_EDIT: pkg-ext cliparaminfo_def === -->
<!-- === DO_NOT_EDIT: pkg-ext callablesignature_def === -->
<a id="callablesignature_def"></a>

### class: `CallableSignature`
- [source](../../pkg_ext/_internal/models/api_dump.py#L34)
> **Since:** 0.1.0

```python
class CallableSignature(Entity):
    parameters: list[FuncParamInfo] = ...
    return_annotation: str | None
    return_type_imports: list[str] = ...
```

| Field | Type | Default | Since |
|---|---|---|---|
| parameters | `list[FuncParamInfo]` | `...` | 0.1.0 |
| return_annotation | `str | None` | - | 0.1.0 |
| return_type_imports | `list[str]` | `...` | 0.1.0 |
<!-- === OK_EDIT: pkg-ext callablesignature_def === -->
<!-- === DO_NOT_EDIT: pkg-ext classdump_def === -->
<a id="classdump_def"></a>

### class: `ClassDump`
- [source](../../pkg_ext/_internal/models/api_dump.py#L87)
> **Since:** 0.1.0

```python
class ClassDump(SymbolDumpBase):
    name: str = PydanticUndefined
    module_path: str = PydanticUndefined
    docstring: str = ''
    line_number: int | None
    type: Literal[class] = 'class'
    direct_bases: list[str] = ...
    init_signature: CallableSignature | None
    fields: list[ClassFieldInfo] | None
```

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | `PydanticUndefined` | 0.1.0 |
| module_path | `str` | `PydanticUndefined` | 0.1.0 |
| docstring | `str` | `''` | 0.1.0 |
| line_number | `int | None` | - | 0.1.0 |
| type | `Literal[class]` | `'class'` | 0.1.0 |
| direct_bases | `list[str]` | `...` | 0.1.0 |
| init_signature | `CallableSignature | None` | - | 0.1.0 |
| fields | `list[ClassFieldInfo] | None` | - | 0.1.0 |
<!-- === OK_EDIT: pkg-ext classdump_def === -->
<!-- === DO_NOT_EDIT: pkg-ext classfieldinfo_def === -->
<a id="classfieldinfo_def"></a>

### class: `ClassFieldInfo`
- [source](../../pkg_ext/_internal/models/api_dump.py#L40)
> **Since:** 0.1.0

```python
class ClassFieldInfo(Entity):
    name: str = PydanticUndefined
    type_annotation: str | None
    type_imports: list[str] = ...
    default: ParamDefault | None
    is_class_var: bool = False
    is_computed: bool = False
    description: str | None
    deprecated: str | None
    env_vars: list[str] | None
```

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | `PydanticUndefined` | 0.1.0 |
| type_annotation | `str | None` | - | 0.1.0 |
| type_imports | `list[str]` | `...` | 0.1.0 |
| default | `ParamDefault | None` | - | 0.1.0 |
| is_class_var | `bool` | `False` | 0.1.0 |
| is_computed | `bool` | `False` | 0.1.0 |
| description | `str | None` | - | 0.1.0 |
| deprecated | `str | None` | - | 0.1.0 |
| env_vars | `list[str] | None` | - | 0.1.0 |
<!-- === OK_EDIT: pkg-ext classfieldinfo_def === -->
<!-- === DO_NOT_EDIT: pkg-ext exceptiondump_def === -->
<a id="exceptiondump_def"></a>

### class: `ExceptionDump`
- [source](../../pkg_ext/_internal/models/api_dump.py#L94)
> **Since:** 0.1.0

```python
class ExceptionDump(SymbolDumpBase):
    name: str = PydanticUndefined
    module_path: str = PydanticUndefined
    docstring: str = ''
    line_number: int | None
    type: Literal[exception] = 'exception'
    direct_bases: list[str] = ...
    init_signature: CallableSignature | None
```

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | `PydanticUndefined` | 0.1.0 |
| module_path | `str` | `PydanticUndefined` | 0.1.0 |
| docstring | `str` | `''` | 0.1.0 |
| line_number | `int | None` | - | 0.1.0 |
| type | `Literal[exception]` | `'exception'` | 0.1.0 |
| direct_bases | `list[str]` | `...` | 0.1.0 |
| init_signature | `CallableSignature | None` | - | 0.1.0 |
<!-- === OK_EDIT: pkg-ext exceptiondump_def === -->
<!-- === DO_NOT_EDIT: pkg-ext funcparaminfo_def === -->
<a id="funcparaminfo_def"></a>

### class: `FuncParamInfo`
- [source](../../pkg_ext/_internal/models/api_dump.py#L26)
> **Since:** 0.1.0

```python
class FuncParamInfo(Entity):
    name: str = PydanticUndefined
    kind: ParamKind = PydanticUndefined
    type_annotation: str | None
    type_imports: list[str] = ...
    default: ParamDefault | None
```

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | `PydanticUndefined` | 0.1.0 |
| kind | `ParamKind` | `PydanticUndefined` | 0.1.0 |
| type_annotation | `str | None` | - | 0.1.0 |
| type_imports | `list[str]` | `...` | 0.1.0 |
| default | `ParamDefault | None` | - | 0.1.0 |
<!-- === OK_EDIT: pkg-ext funcparaminfo_def === -->
<!-- === DO_NOT_EDIT: pkg-ext functiondump_def === -->
<a id="functiondump_def"></a>

### class: `FunctionDump`
- [source](../../pkg_ext/_internal/models/api_dump.py#L59)
> **Since:** 0.1.0

```python
class FunctionDump(SymbolDumpBase):
    name: str = PydanticUndefined
    module_path: str = PydanticUndefined
    docstring: str = ''
    line_number: int | None
    type: Literal[function] = 'function'
    signature: CallableSignature = PydanticUndefined
```

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | `PydanticUndefined` | 0.1.0 |
| module_path | `str` | `PydanticUndefined` | 0.1.0 |
| docstring | `str` | `''` | 0.1.0 |
| line_number | `int | None` | - | 0.1.0 |
| type | `Literal[function]` | `'function'` | 0.1.0 |
| signature | `CallableSignature` | `PydanticUndefined` | 0.1.0 |
<!-- === OK_EDIT: pkg-ext functiondump_def === -->
<!-- === DO_NOT_EDIT: pkg-ext globalvardump_def === -->
<a id="globalvardump_def"></a>

### class: `GlobalVarDump`
- [source](../../pkg_ext/_internal/models/api_dump.py#L105)
> **Since:** 0.1.0

```python
class GlobalVarDump(SymbolDumpBase):
    name: str = PydanticUndefined
    module_path: str = PydanticUndefined
    docstring: str = ''
    line_number: int | None
    type: Literal[global_var] = 'global_var'
    annotation: str | None
    value_repr: str | None
```

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | `PydanticUndefined` | 0.1.0 |
| module_path | `str` | `PydanticUndefined` | 0.1.0 |
| docstring | `str` | `''` | 0.1.0 |
| line_number | `int | None` | - | 0.1.0 |
| type | `Literal[global_var]` | `'global_var'` | 0.1.0 |
| annotation | `str | None` | - | 0.1.0 |
| value_repr | `str | None` | - | 0.1.0 |
<!-- === OK_EDIT: pkg-ext globalvardump_def === -->
<!-- === DO_NOT_EDIT: pkg-ext groupdump_def === -->
<a id="groupdump_def"></a>

### class: `GroupDump`
- [source](../../pkg_ext/_internal/models/api_dump.py#L117)
> **Since:** 0.1.0

```python
class GroupDump(Entity):
    name: str = PydanticUndefined
    symbols: list[Annotated[FunctionDump | CLICommandDump | ClassDump | ExceptionDump | TypeAliasDump | GlobalVarDump, annotation=NoneType required=True discriminator='type']] = ...
```

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | `PydanticUndefined` | 0.1.0 |
| symbols | `list[Annotated[FunctionDump | CLICommandDump | ClassDump | ExceptionDump | TypeAliasDump | GlobalVarDump, annotation=NoneType required=True discriminator='type']]` | `...` | 0.1.0 |
<!-- === OK_EDIT: pkg-ext groupdump_def === -->
<!-- === DO_NOT_EDIT: pkg-ext paramdefault_def === -->
<a id="paramdefault_def"></a>

### class: `ParamDefault`
- [source](../../pkg_ext/_internal/models/api_dump.py#L21)
> **Since:** 0.1.0

```python
class ParamDefault(Entity):
    value_repr: str = PydanticUndefined
    is_factory: bool = False
```

| Field | Type | Default | Since |
|---|---|---|---|
| value_repr | `str` | `PydanticUndefined` | 0.1.0 |
| is_factory | `bool` | `False` | 0.1.0 |
<!-- === OK_EDIT: pkg-ext paramdefault_def === -->
<!-- === DO_NOT_EDIT: pkg-ext paramkind_def === -->
<a id="paramkind_def"></a>

### class: `ParamKind`
- [source](../../pkg_ext/_internal/models/api_dump.py#L13)
> **Since:** 0.1.0

```python
class ParamKind(StrEnum):
    ...
```
<!-- === OK_EDIT: pkg-ext paramkind_def === -->
<!-- === DO_NOT_EDIT: pkg-ext publicapidump_def === -->
<a id="publicapidump_def"></a>

### class: `PublicApiDump`
- [source](../../pkg_ext/_internal/models/api_dump.py#L128)
> **Since:** 0.1.0

```python
class PublicApiDump(Entity):
    pkg_import_name: str = PydanticUndefined
    version: str = PydanticUndefined
    groups: list[GroupDump] = ...
    dumped_at: datetime = PydanticUndefined
```

| Field | Type | Default | Since |
|---|---|---|---|
| pkg_import_name | `str` | `PydanticUndefined` | 0.1.0 |
| version | `str` | `PydanticUndefined` | 0.1.0 |
| groups | `list[GroupDump]` | `...` | 0.1.0 |
| dumped_at | `datetime` | `PydanticUndefined` | 0.1.0 |
<!-- === OK_EDIT: pkg-ext publicapidump_def === -->
<!-- === DO_NOT_EDIT: pkg-ext typealiasdump_def === -->
<a id="typealiasdump_def"></a>

### class: `TypeAliasDump`
- [source](../../pkg_ext/_internal/models/api_dump.py#L100)
> **Since:** 0.1.0

```python
class TypeAliasDump(SymbolDumpBase):
    name: str = PydanticUndefined
    module_path: str = PydanticUndefined
    docstring: str = ''
    line_number: int | None
    type: Literal[type_alias] = 'type_alias'
    alias_target: str = PydanticUndefined
```

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | `PydanticUndefined` | 0.1.0 |
| module_path | `str` | `PydanticUndefined` | 0.1.0 |
| docstring | `str` | `''` | 0.1.0 |
| line_number | `int | None` | - | 0.1.0 |
| type | `Literal[type_alias]` | `'type_alias'` | 0.1.0 |
| alias_target | `str` | `PydanticUndefined` | 0.1.0 |
<!-- === OK_EDIT: pkg-ext typealiasdump_def === -->