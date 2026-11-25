"""Testes do recurso gráfico procedural, sem dependência do GTK."""
import ast
import math
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "ARANDU-SUITE" / "Confluencia" / "app"


class LandscapeContract(unittest.TestCase):
    def test_no_external_photo_dependency(self):
        source = (APP / "mapview.py").read_text(encoding="utf-8")
        self.assertNotIn("paisagem.jpg", source)
        self.assertFalse((APP / "assets" / "paisagem.jpg").exists())
        self.assertIn("draw_landscape(cr,px,py,pw,ph)", source)

    def test_procedural_geometry_calls_and_context(self):
        tree = ast.parse((APP / "mapview.py").read_text(encoding="utf-8"))
        functions = [node for node in tree.body
                     if isinstance(node, ast.FunctionDef)
                     and node.name in ("color", "draw_landscape")]
        self.assertEqual(len(functions), 2)
        env = {"math": math, "cairo": SimpleNamespace(LinearGradient=MagicMock())}
        module = ast.Module(body=functions, type_ignores=[])
        exec(compile(module, "<landscape>", "exec"), env)
        context = MagicMock()
        env["draw_landscape"](context, 10, 20, 164, 95)
        context.save.assert_called_once()
        context.restore.assert_called_once()
        context.translate.assert_called_once_with(10, 20)
        context.scale.assert_called_once_with(164, 95)
        self.assertGreaterEqual(context.fill.call_count, 6)
        self.assertGreater(context.curve_to.call_count, 0)


if __name__ == "__main__":
    unittest.main()
