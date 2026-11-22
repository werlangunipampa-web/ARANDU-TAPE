"""Contrato mínimo de usabilidade antes de recomendar a sessão de login ARANDU."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EssentialsContract(unittest.TestCase):
    def test_keyboard_actions_and_titleless_default_are_in_both_sessions(self):
        for file in ("session/sway.config.in", "session/login/sway-login.config.in"):
            config = (ROOT / file).read_text()
            for fragment in (
                "default_border none",
                "default_floating_border none",
                "workspace_layout default",
                "bindsym $mod+t layout tabbed",
                "bindsym $mod+q kill",
                "bindsym $mod+h move scratchpad",
                "bindsym $mod+Shift+h scratchpad show",
                "bindsym Mod1+Tab exec __ARANDU_OPY__",
                "bindsym Print exec __ARANDU_CAPTURE__",
                "bindsym Shift+Print exec __ARANDU_CAPTURE_SAVE__",
                'bindsym Ctrl+Alt+a [title="^ARANDU Desktop"] focus',
                "bindsym Ctrl+Alt+Shift+q exit",
            ):
                self.assertIn(fragment, config, (file, fragment))

    def test_diagnostics_are_nondestructive(self):
        script = (ROOT / "session/verify-essentials.sh").read_text()
        self.assertIn("python3 -m unittest discover", script)
        self.assertIn("compileall", script)
        for forbidden in ("apt install", "sudo ", "systemctl restart",
                          "swaymsg -t command", "rm -rf", "pkill", "reboot"):
            self.assertNotIn(forbidden, script)

    def test_opy_and_capture_present(self):
        self.assertTrue((ROOT / "opy.py").is_file())
        self.assertTrue((ROOT / "session/capture-screen.sh").is_file())


if __name__ == "__main__":
    unittest.main()
