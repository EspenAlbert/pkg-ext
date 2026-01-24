# Changelog

## 0.2.0 2026-01-24T21-18Z

### __Root__
- BREAKING `__ROOT__.PkgSettings`: field 'pkg_directory' default removed (was: PydanticUndefined)
- BREAKING `__ROOT__.PkgSettings`: field 'repo_root' default removed (was: PydanticUndefined)

### Api_Dump
- BREAKING `api_dump.CLIParamInfo`: field 'param_name' default removed (was: PydanticUndefined)
- BREAKING `api_dump.FuncParamInfo`: field 'name' default removed (was: PydanticUndefined)
- BREAKING `api_dump.FuncParamInfo`: field 'kind' default removed (was: PydanticUndefined)
- BREAKING `api_dump.GroupDump`: field 'name' default removed (was: PydanticUndefined)
- BREAKING `api_dump.ParamDefault`: field 'value_repr' default removed (was: PydanticUndefined)
- BREAKING `api_dump.ExceptionDump`: field 'name' default removed (was: PydanticUndefined)
- BREAKING `api_dump.ExceptionDump`: field 'module_path' default removed (was: PydanticUndefined)
- BREAKING `api_dump.CLICommandDump`: field 'name' default removed (was: PydanticUndefined)
- BREAKING `api_dump.CLICommandDump`: field 'signature' default removed (was: PydanticUndefined)
- BREAKING `api_dump.CLICommandDump`: field 'module_path' default removed (was: PydanticUndefined)
- BREAKING `api_dump.ClassDump`: field 'name' default removed (was: PydanticUndefined)
- BREAKING `api_dump.ClassDump`: field 'module_path' default removed (was: PydanticUndefined)
- BREAKING `api_dump.GlobalVarDump`: field 'name' default removed (was: PydanticUndefined)
- BREAKING `api_dump.GlobalVarDump`: field 'module_path' default removed (was: PydanticUndefined)
- BREAKING `api_dump.ClassFieldInfo`: field 'name' default removed (was: PydanticUndefined)
- BREAKING `api_dump.TypeAliasDump`: field 'name' default removed (was: PydanticUndefined)
- BREAKING `api_dump.TypeAliasDump`: field 'module_path' default removed (was: PydanticUndefined)
- BREAKING `api_dump.TypeAliasDump`: field 'alias_target' default removed (was: PydanticUndefined)
- BREAKING `api_dump.FunctionDump`: field 'name' default removed (was: PydanticUndefined)
- BREAKING `api_dump.FunctionDump`: field 'signature' default removed (was: PydanticUndefined)
- BREAKING `api_dump.FunctionDump`: field 'module_path' default removed (was: PydanticUndefined)
- BREAKING `api_dump.PublicApiDump`: field 'dumped_at' default removed (was: PydanticUndefined)
- BREAKING `api_dump.PublicApiDump`: field 'version' default removed (was: PydanticUndefined)
- BREAKING `api_dump.PublicApiDump`: field 'pkg_import_name' default removed (was: PydanticUndefined)


## 0.1.1 2026-01-24T21-01Z

### __Root__
- `__ROOT__.PkgSettings`: added optional field 'default_branch' (default: 'main')
- `__ROOT__.PkgSettings`: added optional field 'repo_url' (default: '')


## 0.1.0 2026-01-24T18-18Z

### __Root__
- New class `PkgSettings`

### Api_Commands
- New function `dump_api`
- New function `diff_api`

### Api_Dump
- New class `CLIParamInfo`
- New class `CLICommandDump`
- New class `ParamKind`
- New class `ParamDefault`
- New class `FuncParamInfo`
- New class `CallableSignature`
- New class `ClassFieldInfo`
- New class `FunctionDump`
- New class `ClassDump`
- New class `ExceptionDump`
- New class `TypeAliasDump`
- New class `GlobalVarDump`
- New class `GroupDump`
- New class `PublicApiDump`

### Changelog
- New function `release_notes`
- New function `chore`
- New function `promote`

### Generate
- New function `gen_examples`
- New function `gen_tests`
- New function `gen_docs`

### Stability
- New function `exp`
- New function `ga`
- New function `dep`

### Workflows
- New function `post_merge`
- New function `pre_change`
- New function `pre_commit`
