"""Semente: indicadores reais e proteção contra regressão de sessão."""
import pathlib
import sys
import tempfile
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from system_status import battery_status, network_status, clock_text

ROOT = pathlib.Path(__file__).resolve().parents[1]

class SeedStatusContract(unittest.TestCase):
    def test_no_battery_is_not_invented(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(battery_status(pathlib.Path(d)), "Sem bateria detectada")

    def test_actual_battery(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "BAT0"
            p.mkdir()
            (p / "type").write_text("Battery\n")
            (p / "capacity").write_text("85\n")
            (p / "status").write_text("Discharging\n")
            self.assertIn("85%", battery_status(pathlib.Path(d)))

    def test_network_route_not_claimed_as_internet(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "route"
            p.write_text("Iface Destination Gateway Flags\nwlan0 00000000 01010101 0003\n")
            self.assertIn("Internet não verificada", network_status(p))
            p.write_text("Iface Destination Gateway Flags\n")
            self.assertIn("Sem rota", network_status(p))

    def test_clock_format(self):
        self.assertRegex(clock_text(), r"^\d\d:\d\d$")

    def test_ui_session_has_confirmation_and_keeps_gnome_safe(self):
        app = (ROOT / "app.py").read_text()
        self.assertIn('Gtk.Button(label="--:--")', app)
        self.assertIn('def show_seed_status(self):', app)
        self.assertIn('def show_session_menu(self):', app)
        self.assertIn('Gtk.MessageDialog(', app)
        self.assertIn('response != Gtk.ResponseType.ACCEPT', app)
        self.assertIn('"swaymsg", "-t", "command", "exit"', app)
        self.assertIn('Gtk.Button(label="Área de Trabalho")', app.replace('self.quick_action("Área de Trabalho", "desktop")', 'Gtk.Button(label="Área de Trabalho")'))
        self.assertIn('GLib.UserDirectory.DIRECTORY_DESKTOP', app)


if __name__ == "__main__":
    unittest.main()
