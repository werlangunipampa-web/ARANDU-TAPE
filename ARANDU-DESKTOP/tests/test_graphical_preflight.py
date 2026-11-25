"""Preflight reports compatibility without changing a graphical session."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("preflight",ROOT/"scripts"/"preflight-grafico.py")
preflight=importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)

class GraphicalPreflight(unittest.TestCase):
    def test_gnome46_x11_without_arandu(self):
        r=preflight.session_assessment("GNOME Shell 46.0","x11","some-extension@example.invalid",True)
        self.assertTrue(r["isolated_session_candidate"])
        self.assertFalse(r["arandu_extension_active"])

    def test_refuse_concurrent_arandu(self):
        for uuid in ("arandu-foundation@arandulab","confluencia@arandulab"):
            r=preflight.session_assessment("GNOME Shell 46.0","x11",uuid,True)
            self.assertFalse(r["isolated_session_candidate"])
            self.assertTrue(r["arandu_extension_active"])

    def test_missing_or_wrong_environment(self):
        for version,session,ok in (("GNOME Shell 47.0","x11",True),("GNOME Shell 46.0","wayland",True),("","",False),("GNOME Shell 46","x11",False)):
            self.assertFalse(preflight.session_assessment(version,session,"",ok)["isolated_session_candidate"])

    def test_moving_refs_and_dirty_tree(self):
        with self.assertRaises(ValueError):
            preflight.preflight("HEAD")
        sha="a"*40
        with patch.object(preflight,"execute",side_effect=[(0,sha+"\n"),(0," M changed.py\n")]):
            with self.assertRaises(ValueError):
                preflight.preflight(sha)
        with patch.object(preflight,"execute",side_effect=[(0,"b"*40+"\n"),(0,"")]):
            with self.assertRaises(ValueError):
                preflight.preflight(sha)

if __name__=="__main__":
    unittest.main()
