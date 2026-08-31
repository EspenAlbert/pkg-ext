from unittest.mock import patch

import pytest

from pkg_ext._internal import py_format


def test_format_python_string_raises_when_ruff_missing():
    module_name = py_format.format_python_string.__module__
    with (
        patch(f"{module_name}.subprocess.run", side_effect=FileNotFoundError("ruff")),
        pytest.raises(FileNotFoundError, match="ruff"),
    ):
        py_format.format_python_string("x = 1")
