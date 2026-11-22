"""Centro de Atualizações ARANDU: nunca instalar sem gestão oficial."""
import pathlib
import sys
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import updates


class UpdateContract(unittest.TestCase):
    def test_cached_apt_count_excludes_headers(self):
        with patch.object(updates, "_read", return_value=(
                "Listing... Done\nfoo/noble 2.0 amd64 [upgradable from: 1.0]\n"
                "bar/noble 3.0 amd64 [upgradable from: 2.0]\n", None)):
            result = updates.apt_cached_updates()
        self.assertEqual(result["available"], 2)
        self.assertIn("Cache", result["detail"])

    def test_missing_apt_is_not_zero_updates(self):
        with patch.object(updates, "_read", return_value=(None, "Consulta indisponível")):
            self.assertIsNone(updates.apt_cached_updates()["available"])

    def test_fixed_updater_allowlist(self):
        with patch.object(updates.shutil, "which", side_effect=lambda x: "/usr/bin/mintupdate" if x == "mintupdate" else None):
            self.assertEqual(updates.official_updater(), "/usr/bin/mintupdate")
        with patch.object(updates.shutil, "which", return_value=None):
            self.assertIsNone(updates.official_updater())

    def test_no_installs_or_remote_checks_in_module(self):
        code = (ROOT / "updates.py").read_text()
        self.assertIn('["apt", "list", "--upgradable"]', code)
        for forbidden in ("apt upgrade", "apt update", "apt install", "flatpak update",
                          "sudo", "pkexec", "systemctl restart", "shell=True"):
            self.assertNotIn(forbidden, code)

    def test_ui_only_opens_official_update_tool_by_click(self):
        code = (ROOT / "app.py").read_text()
        self.assertIn('Gtk.Button(label="Atualizações")', code)
        self.assertIn('updates.connect("clicked", lambda *_: self.show_updates())', code)
        self.assertIn('button.connect("clicked", lambda *_: self.open_updater())', code)
        self.assertIn('def check_updates(self):', code)
        self.assertIn('threading.Thread(target=worker, daemon=True).start()', code)
        self.assertIn('if os.environ.get("ARANDU_SESSION_LAB") != "1"', code)
        self.assertNotIn('["sudo", "apt"', code)


if __name__ == "__main__":
    unittest.main()
