"""Autonomia sem operações privilegiadas: terminal, Git e atualizador."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TerminalEvolutionContract(unittest.TestCase):
    def test_terminal_is_themed_but_runs_real_foot(self):
        cfg = (ROOT / "session/foot-arandu.ini").read_text()
        launcher = (ROOT / "session/terminal-arandu.sh").read_text()
        self.assertIn("background=14221d", cfg)
        self.assertIn("foreground=e6eedf", cfg)
        self.assertIn('exec foot -c "$HERE/foot-arandu.ini" "$@"', launcher)
        self.assertNotIn("sudo", launcher)

    def test_terminal_keyboard_in_all_sway_templates(self):
        for path in ("session/sway.config.in", "session/login/sway-login.config.in"):
            cfg = (ROOT / path).read_text()
            self.assertIn("bindsym $mod+Return exec __ARANDU_TERMINAL__", cfg)
        for path in ("session/start-nested.sh", "session/login/start-login.sh"):
            source = (ROOT / path).read_text()
            self.assertIn("__ARANDU_TERMINAL__", source)
            self.assertIn("str(terminal)", source)

    def test_git_update_requires_clean_branch_confirmation_and_tests(self):
        script = (ROOT / "session/evolve-arandu.sh").read_text()
        for fragment in (
            "git status --porcelain", "git pull --ff-only origin main",
            '[[ "$CONFIRM" != "ATUALIZAR" ]]',
            "python3 -m unittest discover", "python3 -m compileall",
            "ultimo-commit-anterior.txt"):
            self.assertIn(fragment, script)
        for forbidden in ("sudo ", "apt upgrade", "git reset --hard",
                          "systemctl restart", "swaymsg exit", "rm -rf"):
            self.assertNotIn(forbidden, script)

    def test_ui_exposes_real_terminal_and_manual_evolution(self):
        app = (ROOT / "app.py").read_text()
        self.assertIn('quick_action("Terminal ARANDU", "terminal")', app)
        self.assertIn('Gtk.Button(label="Consultar e atualizar ARANDU no Terminal")', app)
        self.assertIn('def launch_evolution_console(self):', app)
        self.assertIn('str(script), "--update"', app)
        self.assertIn("official_updater()", app)


if __name__ == "__main__":
    unittest.main()
