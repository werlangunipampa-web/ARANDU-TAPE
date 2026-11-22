"""Regressões: ações da Semente/Opy devem ser explícitas e seguras."""
import pathlib
import sys
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from session import windows


class ActionContract(unittest.TestCase):
    def test_no_sway_session_means_no_window_mutation(self):
        with patch.dict("os.environ", {"ARANDU_SESSION_LAB": "0", "SWAYSOCK": ""}):
            self.assertFalse(windows.window_action(10, "encerrar"))
            self.assertFalse(windows.window_action(10, "recolher"))
            self.assertFalse(windows.show_scratchpad())

    def test_stale_and_unlisted_window_never_acted_on(self):
        with patch.dict("os.environ", {"ARANDU_SESSION_LAB": "1", "SWAYSOCK": "/tmp/sway-test"}):
            with patch.object(windows, "list_windows", return_value=({"id": 13, "title": "editor", "app": "editor"},)):
                with patch.object(windows.subprocess, "run") as run:
                    self.assertFalse(windows.window_action(14, "encerrar"))
                    self.assertFalse(windows.window_action(13, "destruir"))
                    self.assertFalse(windows.window_action("13", "encerrar"))
                    run.assert_not_called()

    def test_only_validated_window_id_reaches_sway(self):
        from subprocess import CompletedProcess
        with patch.dict("os.environ", {"ARANDU_SESSION_LAB": "1", "SWAYSOCK": "/tmp/sway-test"}):
            with patch.object(windows, "list_windows", return_value=({"id": 13, "title": "editor", "app": "editor"},)):
                with patch.object(windows.subprocess, "run", return_value=CompletedProcess(
                        args=[], returncode=0, stdout='[{"success": true}]')) as run:
                    self.assertTrue(windows.window_action(13, "recolher"))
                    self.assertIn("[con_id=13] move scratchpad", run.call_args.args[0])
                    self.assertTrue(windows.window_action(13, "encerrar"))
                    self.assertIn("[con_id=13] kill", run.call_args.args[0])

    def test_graphical_actions_require_user_click(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('Gtk.Button(label="Capturar → Colar")', app)
        self.assertIn('capture_button.connect("clicked"', app)
        self.assertIn('def show_clipboard_help(self):', app)
        self.assertIn('def confirm_close_window(self, window):', app)
        self.assertIn('dialog.connect("response", self.finish_close_window, window["id"])', app)
        self.assertIn('def restore_recollected(self):', app)
        self.assertIn('quick_action("Opy · Janelas", "opy")', app)
        self.assertIn('quick_action("Navegador", "firefox")', app)
        self.assertNotIn("shell=True", app)

    def test_comparator_is_preserved(self):
        self.assertTrue((ROOT / "benchmark.py").is_file())
        self.assertIn('Gtk.Button(label="Desempenho")',
                      (ROOT / "app.py").read_text())


if __name__ == "__main__":
    unittest.main()
