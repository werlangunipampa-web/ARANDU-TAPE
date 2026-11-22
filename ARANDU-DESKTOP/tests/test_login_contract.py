"""Verificações de segurança da sessão de login (sem executá-la)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LOGIN = ROOT / "session" / "login"


class LoginContract(unittest.TestCase):
    def test_files(self):
        for name in ("sway-login.config.in", "start-login.sh", "manage-login.sh"):
            self.assertTrue((LOGIN / name).is_file(), name)

    def test_login_is_native_wayland_and_unprivileged(self):
        source = (LOGIN / "start-login.sh").read_text()
        self.assertIn("unset WLR_BACKENDS WLR_X11_OUTPUTS WLR_LIBINPUT_NO_DEVICES", source)
        self.assertIn('sway -c "$CONFIG"', source)
        self.assertIn("EUID", source)
        self.assertIn("XDG_RUNTIME_DIR", source)
        self.assertNotIn("export WLR_BACKENDS=x11", source)

    def test_emergency_exit_and_return(self):
        cfg = (LOGIN / "sway-login.config.in").read_text()
        self.assertIn("bindsym Ctrl+Alt+Shift+q exit", cfg)
        self.assertIn("bindsym Ctrl+Alt+a", cfg)
        self.assertEqual(cfg.count("__ARANDU_LAUNCHER__"), 1)

    def test_installation_requires_opt_in(self):
        source = (LOGIN / "manage-login.sh").read_text()
        for fragment in ('--check|--install|--remove', 'EUID != 0',
                         'X-ARANDU-Managed=true', 'ARANDU_MANAGED_LOGIN_WRAPPER'):
            self.assertIn(fragment, source)
        for unsafe in ("systemctl restart", "update-alternatives", "lightdm.conf",
                       "loginctl terminate", "reboot"):
            self.assertNotIn(unsafe, source)

    def test_print_to_clipboard_without_saving(self):
        capture = (ROOT / "session" / "capture-screen.sh").read_text()
        self.assertIn('grim - | wl-copy --type image/png', capture)
        self.assertIn('--clipboard)', capture)
        self.assertIn('--save)', capture)
        self.assertNotIn('wl-paste', capture)
        config = (LOGIN / "sway-login.config.in").read_text()
        self.assertIn('bindsym Print exec __ARANDU_CAPTURE__', config)
        self.assertIn('bindsym Shift+Print exec __ARANDU_CAPTURE_SAVE__', config)
        source = (LOGIN / "start-login.sh").read_text()
        self.assertIn('template.replace("__ARANDU_CAPTURE__"', source)
        self.assertIn('template.replace("__ARANDU_CAPTURE_SAVE__"', source)

    def test_no_unrequested_cognitive_connection(self):
        for path in LOGIN.iterdir():
            content = path.read_text()
            for forbidden in ("ARANDU-ECA-PRIVATE", "migrate-seed", "git pull"):
                self.assertNotIn(forbidden, content)


if __name__ == "__main__":
    unittest.main()
