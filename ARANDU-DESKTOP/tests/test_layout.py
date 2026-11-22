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

    def test_seed_is_inside_canvas(self):
        self.assertTrue(0 < SEED[0] < WIDTH)
        self.assertTrue(0 < SEED[1] < HEIGHT)


if __name__ == "__main__":
    unittest.main()
