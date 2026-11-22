import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import Session, RIVERS


class CoreContract(unittest.TestCase):
    def test_navigation_is_reversible(self):
        model = Session()
        for river in RIVERS:
            model.select(river)
            self.assertTrue(model.active)
            self.assertEqual(model.river, river)
            model.retract()
            self.assertFalse(model.active)
            self.assertIsNone(model.river)

    def test_invalid_river_cannot_modify_state(self):
        model = Session()
        with self.assertRaises(ValueError):
            model.select("unknown")
        self.assertFalse(model.active)

    def test_eca_is_disabled(self):
        model = Session()
        self.assertFalse(model.bridge_enabled)
        self.assertEqual(model.status()["eca"], "isolated")

    def test_no_observation_without_provider(self):
        model = Session()
        self.assertEqual(model.read_items("open"), ())
        self.assertEqual(model.read_items("frequent"), ())
        self.assertEqual(model.status()["window_provider"], "not-connected")


if __name__ == "__main__":
    unittest.main()
