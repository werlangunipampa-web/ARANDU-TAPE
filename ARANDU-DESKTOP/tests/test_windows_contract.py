import pathlib
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "session"))
from windows import flatten_windows, list_windows


class WindowAdapterContract(unittest.TestCase):
    def test_tree_distinguishes_real_windows(self):
        tree = {
            "id": 0, "name": "root", "nodes": [
                {"id": 4, "name": "Firefox", "app_id": "firefox",
                 "nodes": [], "floating_nodes": []},
                {"id": 9, "name": "Workspace", "nodes": [
                    {"id": 10, "name": "Terminal", "app_id": None,
                     "window_properties": {"class": "xterm"}}]},
            ],
        }
        self.assertEqual(flatten_windows(tree), (
            {"id": 4, "title": "Firefox", "app": "firefox"},
            {"id": 10, "title": "Terminal", "app": "xterm"},
        ))

    def test_without_nested_session_does_not_run_subprocess(self):
        with patch.dict("os.environ", {}, clear=True):
            with patch("subprocess.run") as run:
                self.assertEqual(list_windows(), ())
                run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
