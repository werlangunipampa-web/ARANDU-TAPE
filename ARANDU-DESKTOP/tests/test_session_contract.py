"""O laboratório de sessão não instala compositor nem altera GNOME."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SESSION = ROOT / "session"


class NestedSessionContract(unittest.TestCase):
    def test_files_are_present(self):
        for filename in ("start-nested.sh", "launch-arandu.sh", "sway.config.in"):
            self.assertTrue((SESSION / filename).is_file(), filename)

    def test_compositor_is_nested_x11_and_does_not_touch_login(self):
        script = (SESSION / "start-nested.sh").read_text(encoding="utf-8")
        self.assertIn("WLR_BACKENDS=x11", script)
        self.assertIn("WLR_LIBINPUT_NO_DEVICES=1", script)
        self.assertIn('sway -c "$ARANDU_SESSION_CONFIG"', script)
        for prohibited in ("sudo ", "apt install", "pkill ", "systemctl ", "/usr/share/wayland-sessions"):
            self.assertNotIn(prohibited, script)

    def test_emergency_exit_and_explicit_child(self):
        config = (SESSION / "sway.config.in").read_text(encoding="utf-8")
        self.assertIn("bindsym Ctrl+Alt+Shift+q exit", config)
        self.assertIn("bindsym $mod+Shift+Escape exit", config)
        self.assertEqual(config.count("__ARANDU_LAUNCHER__"), 1)
        self.assertIn("exec __ARANDU_LAUNCHER__", config)

    def test_gapplication_identity_does_not_collide(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        launcher = (SESSION / "launch-arandu.sh").read_text(encoding="utf-8")
        self.assertIn("org.arandulab.DesktopSessionLab", app)
        self.assertIn("ARANDU_SESSION_LAB", launcher)
        self.assertIn("GDK_BACKEND=wayland", launcher)

    def test_no_automatic_eca_connection(self):
        for name in ("start-nested.sh", "launch-arandu.sh", "sway.config.in"):
            source = (SESSION / name).read_text(encoding="utf-8")
            for sensitive in ("ARANDU-ECA-PRIVATE", "ARANDU-G4-PRIVATE", "migrate-seed"):
                self.assertNotIn(sensitive, source)


if __name__ == "__main__":
    unittest.main()
