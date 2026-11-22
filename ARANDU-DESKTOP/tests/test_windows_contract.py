import pathlib
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "session"))
from windows import flatten_windows, list_windows, focus_window, user_windows, hide_arandu


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

    def test_own_arandu_window_is_excluded(self):
        data = (
            {"id": 1, "title": "ARANDU Desktop · Laboratório 0.5",
             "app": "org.arandulab.DesktopSessionLab"},
            {"id": 2, "title": "Foot", "app": "foot"},
        )
        self.assertEqual(user_windows(data), (data[1],))

    def test_focus_rejected_without_lab_or_invalid_identifier(self):
        with patch.dict("os.environ", {}, clear=True):
            with patch("subprocess.run") as run:
                self.assertFalse(focus_window(10))
                self.assertFalse(focus_window(-1))
                self.assertFalse(focus_window("10"))
                run.assert_not_called()

    def test_focus_uses_validated_id_and_no_shell(self):
        import json
        from types import SimpleNamespace
        tree = {"id": 0, "nodes": [
            {"id": 17, "app_id": "foot", "name": "Terminal"}
        ]}
        outputs = [
            SimpleNamespace(stdout=json.dumps(tree)),
            SimpleNamespace(stdout='[{"success": true}]'),
        ]
        with patch.dict("os.environ", {"SWAYSOCK": "/tmp/sway-test.sock",
                                       "ARANDU_SESSION_LAB": "1"}):
            with patch("subprocess.run", side_effect=outputs) as run:
                self.assertTrue(focus_window(17))
                self.assertEqual(run.call_count, 2)
                args = run.call_args.args[0]
                self.assertEqual(args, ["swaymsg", "-r", "-t", "command",
                                        "[con_id=17] focus"])
                self.assertNotIn("shell", run.call_args.kwargs)

    def test_stale_window_never_receives_focus_command(self):
        import json
        from types import SimpleNamespace
        tree = {"id": 0, "nodes": [
            {"id": 17, "app_id": "foot", "name": "Terminal"}
        ]}
        with patch.dict("os.environ", {"SWAYSOCK": "test",
                                       "ARANDU_SESSION_LAB": "1"}):
            with patch("subprocess.run",
                       return_value=SimpleNamespace(stdout=json.dumps(tree))) as run:
                self.assertFalse(focus_window(18))
                self.assertEqual(run.call_count, 1)

    def test_retract_requires_lab_and_never_uses_shell(self):
        with patch.dict("os.environ", {}, clear=True):
            with patch("subprocess.run") as run:
                self.assertFalse(hide_arandu())
                run.assert_not_called()
        from types import SimpleNamespace
        with patch.dict("os.environ", {"SWAYSOCK": "/tmp/sway-test.sock",
                                       "ARANDU_SESSION_LAB": "1"}):
            with patch("subprocess.run",
                       return_value=SimpleNamespace(stdout='[{"success": true}]')) as run:
                self.assertTrue(hide_arandu())
                self.assertEqual(run.call_args.args[0], [
                    "swaymsg", "-r", "-t", "command",
                    '[title="^ARANDU Desktop"] move scratchpad'
                ])
                self.assertNotIn("shell", run.call_args.kwargs)

    def test_without_nested_session_does_not_run_subprocess(self):
        with patch.dict("os.environ", {}, clear=True):
            with patch("subprocess.run") as run:
                self.assertEqual(list_windows(), ())
                run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
