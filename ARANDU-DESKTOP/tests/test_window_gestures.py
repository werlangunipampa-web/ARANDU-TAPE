"""Tests for the public gesture vocabulary, not a compositor integration."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from window_gestures import classify_handle, corner_intent, HEADER_MIN_HEIGHT


class WindowGestures(unittest.TestCase):
    def test_hover_and_incomplete_drag_do_not_execute(self):
        self.assertIsNone(classify_handle(50, -50))
        self.assertIsNone(classify_handle(50, -50, released=True, cancelled=True))
        self.assertIsNone(classify_handle(0, -12, released=True))
        self.assertIsNone(classify_handle(70, -10, released=True))
        self.assertIsNone(classify_handle(40, -65, released=True))
        self.assertIsNone(classify_handle(float("nan"), -60, released=True))

    def test_vertical_and_diagonal_are_distinct(self):
        self.assertEqual(classify_handle(0, -60, released=True), "imersao")
        self.assertEqual(classify_handle(5, 60, released=True), "recolher_ao_rio")
        for dx in (-50, 50):
            self.assertEqual(classify_handle(dx, -50, released=True),
                             "solicitar_encerramento")

    def test_panel_never_closes_application(self):
        self.assertEqual(classify_handle(50, -50, released=True, target="panel"), "fechar_painel")
        self.assertEqual(classify_handle(0, 60, released=True, target="panel"), "recolher_painel")
        self.assertIsNone(classify_handle(0, -60, released=True, target="panel"))
        self.assertIsNone(classify_handle(0, 60, released=True, target="unknown"))

    def test_arrows_require_intent_and_preview(self):
        self.assertIsNone(corner_intent("upper_right"))
        self.assertIsNone(corner_intent("lower_right", activated=True))
        self.assertEqual(corner_intent("upper_right", activated=True), "imersao")
        self.assertEqual(corner_intent("lower_right", activated=True, preview=True), "confirmar_redimensionamento")
        self.assertIsNone(corner_intent("lower_right", activated=True, preview=True, cancelled=True))

    def test_header_reservation(self):
        self.assertEqual(HEADER_MIN_HEIGHT, 52)
        desktop = (ROOT / "app.py").read_text()
        gnome = (ROOT.parent / "ARANDU-SUITE/Confluencia/app/main.py").read_text()
        self.assertIn("header.set_size_request(-1, HEADER_MIN_HEIGHT)", desktop)
        self.assertIn("head.set_size_request(-1, 52)", gnome)
        self.assertIn("set_show_title_buttons(True)", desktop)
        self.assertIn("set_show_close_button(True)", gnome)
        opy = (ROOT / "opy.py").read_text()
        self.assertIn("header.set_size_request(-1, HEADER_MIN_HEIGHT)", opy)
        self.assertIn('header.set_decoration_layout(":close")', opy)


if __name__ == "__main__":
    unittest.main()
