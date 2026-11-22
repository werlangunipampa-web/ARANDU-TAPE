import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from layout import WIDTH, HEIGHT, SEED, paths, assets_exist


class VisualContract(unittest.TestCase):
    def test_assets_are_original(self):
        self.assertTrue(assets_exist())

    def test_three_real_paths_have_five_positions(self):
        data = paths()
        self.assertEqual(set(data), {"memory", "open", "frequent"})
        for coordinates in data.values():
            self.assertEqual(len(coordinates), 5)
            for x, y in coordinates:
                self.assertGreaterEqual(x, 0)
                self.assertLessEqual(x, WIDTH)
                self.assertGreaterEqual(y, 0)
                self.assertLessEqual(y, HEIGHT)

    def test_gtk4_does_not_use_unsupported_accessible_name_setter(self):
        source = (Path(__file__).resolve().parents[1] / "visual.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn(".set_accessible_name(", source)
        self.assertIn(".set_tooltip_text(", source)

    def test_compact_canvas_keeps_seed_and_markers_visible(self):
        from visual_contract import compact_geometry
        contract = compact_geometry()
        self.assertEqual(contract["size"], (900, 375))
        self.assertEqual(contract["seed"], (482, 266))
        for river in ("memory", "open", "frequent"):
            for x, y in contract["markers"][river]:
                self.assertGreaterEqual(x, 0)
                self.assertLessEqual(x, contract["size"][0])
                self.assertGreaterEqual(y, 0)
                self.assertLessEqual(y, contract["size"][1])

    def test_seed_is_inside_canvas(self):
        self.assertTrue(0 < SEED[0] < WIDTH)
        self.assertTrue(0 < SEED[1] < HEIGHT)


if __name__ == "__main__":
    unittest.main()
