# Public API Specification Research

This document explores existing approaches to capturing library/package public APIs in machine-readable formats, informing the design of `PublicApiDump`.

## Problem Statement

Unlike REST APIs (which have [OpenAPI](https://www.openapis.org/)), **no widely adopted standard exists for describing library/package public APIs**. This gap creates challenges for:
- Breaking change detection between versions
- Automated documentation generation
- Code generation (e.g., example classes with typed fields)

## Existing Tools and Approaches

### Python-Specific

| Tool | Purpose | Format | Tracks Defaults | Tracks Deprecation |
|------|---------|--------|-----------------|-------------------|
| [griffe](https://mkdocstrings.github.io/griffe/) | API extraction for mkdocstrings | JSON | Partial | No |
| [py-api-dumper](https://pypi.org/project/py-api-dumper/) | API diff between versions | Text | Unknown | No |
| `.pyi` stub files ([PEP 561](https://peps.python.org/pep-0561/)) | Type information | Python | No | No |
| [sphinx-autoapi](https://sphinx-autoapi.readthedocs.io/) | Sphinx documentation | RST/HTML | No | Via docstring |

### Cross-Language

| Tool | Language | Purpose | Format |
|------|----------|---------|--------|
| [api-extractor](https://api-extractor.com/) | TypeScript | API surface tracking | `.api.md`, `.api.json` |
| [cargo-semver-checks](https://github.com/obi1kenobi/cargo-semver-checks) | Rust | Breaking change lint | Uses rustdoc JSON |
| Elm package manager | Elm | Enforced semver | Module signatures |
| [rustdoc JSON](https://doc.rust-lang.org/nightly/nightly-rustc/rustdoc_json_types/) | Rust | Machine-readable docs | JSON |

## Design Inspirations

### From api-extractor (TypeScript)

Microsoft's [api-extractor](https://api-extractor.com/) provides a workflow model worth emulating:

- **Baseline file**: Committed `.api.md` file representing the approved API surface
- **Review workflow**: PR diffs show exactly what changed in the public API
- **Rollup**: Consolidates public exports into a single report

Our `{pkg_name}.api.yaml` / `{pkg_name}.api-dev.yaml` workflow mirrors this approach:

```
1. Before changes: pkg-ext dump-api (creates baseline)
2. Make changes
3. Compare: pkg-ext dump-api --dev (creates local version)
4. diff {pkg_name}.api.yaml {pkg_name}.api-dev.yaml
```

### From griffe (Python)

[griffe](https://mkdocstrings.github.io/griffe/) is the extraction engine behind mkdocstrings. Key concepts:

- **Object model**: Structured representation of modules, classes, functions
- **Parameter kinds**: Positional-only, keyword-only, etc.
- **Docstring parsing**: Extracts structured documentation
- **JSON export**: Machine-readable output

### From Python Type Stubs (.pyi)

[PEP 561](https://peps.python.org/pep-0561/) defines stub files as type information containers:

- Already a semi-standard for public API surface
- Tooling support (mypy, pyright)
- **Limitation**: Only captures types, not default values, deprecation info, or documentation

### From Rust's Approach

Rust's ecosystem offers two relevant tools:

- **rustdoc JSON**: Nightly feature producing machine-readable API documentation
- **cargo-semver-checks**: Lints for semver violations using rustdoc output

The separation of concerns (dump format vs. analysis tool) is worth noting.

### From Elm's Package Manager

Elm enforces semantic versioning based on API changes:

- Package manager automatically detects breaking changes
- Rejects invalid version bumps
- API surface implicitly tracked via exposed module signatures

## What Makes PublicApiDump Novel

The `PublicApiDump` model adds value beyond existing tools:

| Feature | Existing Tools | PublicApiDump |
|---------|---------------|---------------|
| Pydantic Field metadata | Not extracted | description, deprecated |
| BaseSettings awareness | Not extracted | env_var names |
| Default value tracking | Limited | value_repr, is_factory, source |
| Stability levels | Not tracked | Per-group stability |
| Format | JSON/Text | YAML (diff-friendly) |

## Format Comparison

### PublicApiDump (YAML)

```yaml
pkg_import_name: model_lib
version: "1.2.0"
dumped_at: "2026-01-12T10:30:00Z"
groups:
  - name: serialize
    stability: ga
    symbols:
      - name: dump_yaml
        type: function
        module_path: model_lib.serialize
        signature:
          parameters:
            - name: obj
              kind: positional_or_keyword
              type_annotation: "Any"
            - name: indent
              kind: keyword_only
              type_annotation: "int"
              default:
                value_repr: "2"
                source: plain
          return_annotation: "str"
```

### api-extractor (.api.md)

```markdown
## API Report File for "model-lib"

### Functions

// @public
export function dump_yaml(obj: Any, indent?: number): string;
```

### griffe (JSON)

```json
{
  "name": "dump_yaml",
  "kind": "function",
  "parameters": [
    {"name": "obj", "annotation": "Any"},
    {"name": "indent", "annotation": "int", "default": "2"}
  ]
}
```

The YAML approach balances machine-parseability with human readability, optimizing for diff review.

## Recommendations Applied to PublicApiDump

Based on this research:

1. **Keep YAML format**: More diff-friendly than JSON, better for PR reviews
2. **Maintain baseline + dev workflow**: Matches proven api-extractor pattern
3. **Include stability per-symbol**: Consider adding to `SymbolDump` (not just `GroupDump`)
4. **Add since_version field**: Track when symbols were added (future enhancement)
5. **Gitignore pattern**: Add `*-dev.yaml` to `.gitignore` templates

## Future Considerations

- **Diff tool**: `pkg-ext api-diff` command comparing two dumps
- **CI integration**: Fail PR if breaking changes detected without version bump
- **Export to .pyi**: Generate stub files from dump for tooling interop
- **JSON Schema**: Define schema for YAML validation

## References

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [PEP 561 - Distributing and Packaging Type Information](https://peps.python.org/pep-0561/)
- [PEP 702 - Marking deprecations using the type system](https://peps.python.org/pep-0702/)
- [griffe Documentation](https://mkdocstrings.github.io/griffe/)
- [api-extractor](https://api-extractor.com/)
- [cargo-semver-checks](https://github.com/obi1kenobi/cargo-semver-checks)
