from unittest.mock import patch

import pytest

from pkg_ext._internal import py_format


def test_format_python_string_raises_when_ruff_missing():
    with (
        patch("pkg_ext._internal.py_format.which", return_value=None),
        pytest.raises(FileNotFoundError, match="ruff is required on PATH"),
    ):
        py_format.format_python_string("x = 1")
