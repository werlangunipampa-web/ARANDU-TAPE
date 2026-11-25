"""Contratos de identificação científica sem acesso à rede ou GTK."""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

class ScientificIdentity(unittest.TestCase):
    def test_seed_has_explicit_about_action(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        ast.parse(source)
        self.assertIn('about_shortcut.connect("clicked", self.show_about)', source)
        self.assertIn('self.tools_box.append(about_shortcut)', source)
        self.assertIn("Versão instalada: ", source)
        self.assertIn("DOI geral e DOI desta versão: ainda não registrados", source)
        self.assertIn("Gtk.LinkButton.new_with_label", source)

    def test_gnome_seed_help_has_identity(self):
        source = (REPO / "ARANDU-SUITE/Confluencia/shell/implementation.js.in").read_text(encoding="utf-8")
        self.assertIn("SOBRE O ARANDU", source)
        self.assertIn("DOI: ainda não registrado nesta compilação", source)
        self.assertIn("link.connect('clicked'", source)
        self.assertIn("Gio.AppInfo.launch_default_for_uri(uri,null)", source)

if __name__ == "__main__":
    unittest.main()
