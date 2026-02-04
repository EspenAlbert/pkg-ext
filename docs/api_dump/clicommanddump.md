# CLICommandDump

<!-- === DO_NOT_EDIT: pkg-ext clicommanddump_def === -->
## class: CLICommandDump
- [source](../../pkg_ext/_internal/models/api_dump.py#L79)
> **Since:** 0.1.0

```python
class CLICommandDump(SymbolDumpBase):
    name: str
    module_path: str
    docstring: str = ''
    line_number: int | None = None
    type: Literal[cli_command] = 'cli_command'
    signature: CallableSignature
    cli_params: list[CLIParamInfo] = ...
```

A typer CLI command with rich parameter metadata.
<!-- === OK_EDIT: pkg-ext clicommanddump_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | - | 0.1.0 |
| module_path | `str` | - | 0.1.0 |
| docstring | `str` | `''` | 0.1.0 |
| line_number | `int | None` | - | 0.1.0 |
| type | `Literal[cli_command]` | `'cli_command'` | 0.1.0 |
| signature | `CallableSignature` | - | 0.1.0 |
| cli_params | `list[CLIParamInfo]` | `...` | 0.1.0 |

<!-- === DO_NOT_EDIT: pkg-ext clicommanddump_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | field 'line_number' default added: None |
| unreleased | added base class 'SymbolDumpBase' |
| 0.2.0 | field 'module_path' default removed (was: PydanticUndefined) |
| 0.2.0 | field 'signature' default removed (was: PydanticUndefined) |
| 0.2.0 | field 'name' default removed (was: PydanticUndefined) |
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext clicommanddump_changes === -->