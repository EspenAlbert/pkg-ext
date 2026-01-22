# Stability Decorators and Warnings

pkg-ext provides decorators to mark functions, classes, and arguments as experimental or deprecated. Warnings are emitted at call time (not import time).

## Decorators

### `@experimental`

Marks a function or class as experimental. Emits `PkgExtExperimentalWarning` when called.

```python
from pkg_ext import experimental

@experimental
def new_feature():
    ...

@experimental
class NewClass:
    ...
```

### `@deprecated`

Re-exported from Python 3.13+ standard library ([PEP 702](https://peps.python.org/pep-0702/)). Emits `DeprecationWarning` when called. Type checkers (pyright/mypy) show deprecation warnings.

```python
from pkg_ext import deprecated
# or: from warnings import deprecated

@deprecated("Use new_feature instead")
def old_feature():
    ...
```

### `@experimental_args`

Marks specific keyword arguments as experimental. Warning emitted only when the argument is passed.

```python
from pkg_ext import experimental_args

@experimental_args("new_format")
def export(data, format="json", new_format=None):
    ...

export(data, new_format="parquet")  # warns
export(data)  # no warning
```

### `@deprecated_args`

Marks specific keyword arguments as deprecated. Supports rename hints.

```python
from pkg_ext import deprecated_args

# Simple deprecation
@deprecated_args("old_opt")
def func(old_opt=None):
    ...

# With rename hint
@deprecated_args(old_format="format")
def export(data, format="json", old_format=None):
    ...
```

### `@deprecated_arg`

Single-argument deprecation with optional reason and rename.

```python
from pkg_ext import deprecated_arg

@deprecated_arg("unsafe", reason="security vulnerability")
def func(unsafe=False):
    ...

@deprecated_arg("callback", new_name="on_done", reason="renamed for clarity")
def async_op(callback=None, on_done=None):
    ...
```

## Warning Classes

| Class | Purpose | Inherits |
|-------|---------|----------|
| `PkgExtWarning` | Base class | `UserWarning` |
| `PkgExtExperimentalWarning` | Experimental features | `PkgExtWarning` |
| `PkgExtDeprecationWarning` | Deprecated features (pkg-ext decorators) | `PkgExtWarning`, `DeprecationWarning` |

Standard `@deprecated` (PEP 702) emits `DeprecationWarning` directly, not `PkgExtDeprecationWarning`.

## Suppressing Warnings

### Runtime

```python
import warnings
from pkg_ext import PkgExtWarning, PkgExtExperimentalWarning, PkgExtDeprecationWarning

# Suppress all pkg-ext warnings
warnings.filterwarnings("ignore", category=PkgExtWarning)

# Suppress only experimental warnings
warnings.filterwarnings("ignore", category=PkgExtExperimentalWarning)

# Suppress only pkg-ext deprecation warnings
warnings.filterwarnings("ignore", category=PkgExtDeprecationWarning)

# Suppress standard @deprecated warnings (PEP 702)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Suppress all deprecation warnings (both pkg-ext and standard)
warnings.filterwarnings("ignore", category=DeprecationWarning)
```

### By Message Pattern

Filter warnings for specific symbols:

```python
import warnings

# Suppress warnings for a specific function
warnings.filterwarnings("ignore", message="'my_function'.*experimental")

# Suppress warnings for a specific argument
warnings.filterwarnings("ignore", message="Argument 'old_opt'.*deprecated")
```

### Pytest Configuration

In `pyproject.toml`:

```toml
[tool.pytest.ini_options]
filterwarnings = [
    # Suppress all pkg-ext experimental warnings in tests
    "ignore::pkg_ext.PkgExtExperimentalWarning",
    # Suppress specific symbol
    "ignore:'my_function'.*experimental:pkg_ext.PkgExtExperimentalWarning",
    # Suppress standard deprecation warnings
    "ignore::DeprecationWarning",
]
```

Or in `pytest.ini`:

```ini
[pytest]
filterwarnings =
    ignore::pkg_ext.PkgExtExperimentalWarning
    ignore::DeprecationWarning
```

## Limitations

- **Non-callable symbols:** Constants and type aliases in experimental/deprecated groups don't emit warnings. `@experimental` and `@deprecated` only work on functions and classes.
- **Positional arguments:** `@experimental_args` and `@deprecated_args` only detect keyword arguments. Positional arguments passed without the keyword name won't trigger warnings.
