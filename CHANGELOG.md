# Changelog

## 0.4.0 2026-02-24T23-39Z

### Example
- New function `gen_example_prompt`
- New function `check_examples`

### Generate
- Removed `generate.gen_examples`
- Removed `generate.gen_tests`

### Workflows
- New function `change_base`


## 0.3.5 2026-02-17T21-21Z

### Workflows
- fix: rename commit message to `chore: release commit for` (removed pre-release) [2857c0](https://github.com/EspenAlbert/pkg-ext/commit/2857c0)


## 0.3.4 2026-02-11T06-09Z

### Generate
- fix: stable_repr now strips embedded memory addresses from complex reprs [efd3cd](https://github.com/EspenAlbert/pkg-ext/commit/efd3cd)

### Workflows
- fix(pkg-ext): reorder pre-change to run api-diff before docs generation [0c8ac3](https://github.com/EspenAlbert/pkg-ext/commit/0c8ac3)


## 0.3.3 2026-02-06T10-50Z

### Other Changes
- Chore: updated dependencies
- Chore: updated dependencies


## 0.3.2 2026-02-06T06-10Z

### Other Changes
- Chore: updated dependencies


## 0.3.1 2026-02-05T11-45Z

### Workflows
- fix(pkg-ext): clarify behavior of owned_modules during symbol movement updates in tests and implementation [f44f0c](https://github.com/EspenAlbert/pkg-ext/commit/f44f0c)


## 0.3.0 2026-02-04T07-14Z

### __Root__
- `__ROOT__.PkgSettings`: added base class 'BaseSettings'
- `__ROOT__.PkgSettings`: field 'max_bump_type' default added: None
- `__ROOT__.PkgSettings`: field 'after_file_write_hooks' default added: None

### Api_Dump
- BREAKING `api_dump.ClassDump`: removed field 'direct_bases'
- BREAKING `api_dump.ExceptionDump`: removed field 'direct_bases'
- `api_dump.CLICommandDump`: added base class 'SymbolDumpBase'
- `api_dump.CLICommandDump`: field 'line_number' default added: None
- `api_dump.FuncParamInfo`: added base class 'Entity'
- `api_dump.FuncParamInfo`: field 'default' default added: None
- `api_dump.FuncParamInfo`: field 'type_annotation' default added: None
- `api_dump.ClassDump`: added base class 'SymbolDumpBase'
- `api_dump.ClassDump`: added optional field 'mro_bases' (default: ...)
- `api_dump.ClassDump`: added optional field 'num_direct_bases' (default: 0)
- `api_dump.ClassDump`: field 'fields' default added: None
- `api_dump.ClassDump`: field 'line_number' default added: None
- `api_dump.ClassDump`: field 'init_signature' default added: None
- `api_dump.FunctionDump`: added base class 'SymbolDumpBase'
- `api_dump.FunctionDump`: field 'line_number' default added: None
- `api_dump.PublicApiDump`: added base class 'Entity'
- `api_dump.TypeAliasDump`: added base class 'SymbolDumpBase'
- `api_dump.TypeAliasDump`: field 'line_number' default added: None
- `api_dump.ParamKind`: added base class 'StrEnum'
- `api_dump.ParamDefault`: added base class 'Entity'
- `api_dump.CLIParamInfo`: added base class 'Entity'
- `api_dump.CLIParamInfo`: field 'envvar' default added: None
- `api_dump.CLIParamInfo`: field 'choices' default added: None
- `api_dump.CLIParamInfo`: field 'help' default added: None
- `api_dump.CLIParamInfo`: field 'default_repr' default added: None
- `api_dump.CLIParamInfo`: field 'type_annotation' default added: None
- `api_dump.CallableSignature`: added base class 'Entity'
- `api_dump.CallableSignature`: field 'return_annotation' default added: None
- `api_dump.GlobalVarDump`: added base class 'SymbolDumpBase'
- `api_dump.GlobalVarDump`: field 'annotation' default added: None
- `api_dump.GlobalVarDump`: field 'line_number' default added: None
- `api_dump.GlobalVarDump`: field 'value_repr' default added: None
- `api_dump.ExceptionDump`: added base class 'SymbolDumpBase'
- `api_dump.ExceptionDump`: added optional field 'mro_bases' (default: ...)
- `api_dump.ExceptionDump`: added optional field 'num_direct_bases' (default: 0)
- `api_dump.ExceptionDump`: field 'line_number' default added: None
- `api_dump.ExceptionDump`: field 'init_signature' default added: None
- `api_dump.GroupDump`: added base class 'Entity'
- `api_dump.ClassFieldInfo`: added base class 'Entity'
- `api_dump.ClassFieldInfo`: field 'description' default added: None
- `api_dump.ClassFieldInfo`: field 'deprecated' default added: None
- `api_dump.ClassFieldInfo`: field 'env_vars' default added: None
- `api_dump.ClassFieldInfo`: field 'default' default added: None
- `api_dump.ClassFieldInfo`: field 'type_annotation' default added: None
- fix(pkg-ext): capture None as explicit default in pydantic field parsing [833c63](https://github.com/EspenAlbert/pkg-ext/commit/833c63)

### Generate
- fix(docs_version): correct sorting logic for symbol changes to prioritize unreleased versions [757c70](https://github.com/EspenAlbert/pkg-ext/commit/757c70)


## 0.2.1 2026-01-24T21-48Z

### Api_Dump
- fix: Implements stable representation and memory address stripping for improved output consistency [b2ed78](https://github.com/EspenAlbert/pkg-ext/commit/b2ed78)


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
