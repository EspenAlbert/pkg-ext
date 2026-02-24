from unittest.mock import patch

from pkg_ext._internal import clipboard


def test_add_to_clipboard_with_pbcopy():
    module_name = clipboard.add_to_clipboard.__module__
    with (
        patch(f"{module_name}.which", return_value="/usr/bin/pbcopy") as mock_which,
        patch(f"{module_name}.subprocess") as mock_subprocess,
    ):
        clipboard.add_to_clipboard("hello")
        mock_which.assert_called_once_with("pbcopy")
        mock_subprocess.run.assert_called_once_with("/usr/bin/pbcopy", text=True, input="hello", check=True)


def test_add_to_clipboard_no_pbcopy():
    module_name = clipboard.add_to_clipboard.__module__
    with patch(f"{module_name}.which", return_value=None):
        clipboard.add_to_clipboard("hello")
