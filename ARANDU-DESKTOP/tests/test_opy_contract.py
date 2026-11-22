"""A Opy não deve se confundir com janelas de usuário nem exigir scripts externos."""
from pathlib import Path
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "session"))
from windows import user_windows

ROOT = Path(__file__).resolve().parents[1]


class OpyContract(unittest.TestCase):
    def test_opy_is_not_an_open_app(self):
        items = ({"id": 11, "app": "org.arandulab.OpySwitcher",
                  "title": "Opy · Encontro das janelas"},
                 {"id": 12, "app": "firefox", "title": "Firefox"})
        self.assertEqual(user_windows(items), (items[1],))

    def test_opy_requires_active_arandu_sway(self):
        code = (ROOT / "opy.py").read_text(encoding="utf-8")
        self.assertIn('os.environ.get("ARANDU_SESSION_LAB") == "1"', code)
        self.assertIn('os.environ.get("SWAYSOCK")', code)
        self.assertIn('list_windows()', code)
        self.assertIn('focus_window(self.rows[index]["id"])', code)
        self.assertNotIn('shell=True', code)
        self.assertNotIn("git pull", code)

    def test_opy_keyboard_and_explicit_activation(self):
        code = (ROOT / "opy.py").read_text(encoding="utf-8")
        self.assertIn("Gdk.KEY_Escape", code)
        self.assertIn("Gdk.KEY_Return", code)
        self.assertIn("Gdk.KEY_Down, Gdk.KEY_Up", code)
        self.assertIn('self.list_box.connect("row-activated"', code)
        self.assertNotIn('application.launch(', code)
        self.assertNotIn('kill(', code)

    def test_both_session_templates_bind_alt_tab(self):
        for path in ("session/sway.config.in", "session/login/sway-login.config.in"):
            cfg = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("bindsym Mod1+Tab exec __ARANDU_OPY__", cfg)
            self.assertIn('for_window [app_id="org.arandulab.OpySwitcher"] floating enable', cfg)
        for path in ("session/start-nested.sh", "session/login/start-login.sh"):
            runner = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("__ARANDU_OPY__", runner)
            self.assertIn("str(opy)", runner)

    def test_print_screen_and_arandu_return_preserved(self):
        cfg = (ROOT / "session/login/sway-login.config.in").read_text()
        self.assertIn("bindsym Print exec __ARANDU_CAPTURE__", cfg)
        self.assertIn("bindsym Shift+Print exec __ARANDU_CAPTURE_SAVE__", cfg)
        self.assertIn('bindsym Ctrl+Alt+a [title="^ARANDU Desktop"] focus', cfg)
        self.assertIn("bindsym Ctrl+Alt+Shift+q exit", cfg)


if __name__ == "__main__":
    unittest.main()
