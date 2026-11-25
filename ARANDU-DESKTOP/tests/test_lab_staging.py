"""The staging guard refuses the working ARANDU account and mismatched commits."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("stage_lab",ROOT/"scripts"/"preparar-lab-gnome.py")
lab=importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

class LabStaging(unittest.TestCase):
    def test_conflicts(self):
        self.assertTrue(lab.conflicts("arandu-foundation@arandulab"))
        self.assertTrue(lab.conflicts("confluencia@arandulab"))
        self.assertFalse(lab.conflicts("unrelated@example.invalid"))

    def test_moving_ref(self):
        with self.assertRaises(ValueError):
            lab.validate("HEAD")

    def test_existing_arandu_blocks_before_audit(self):
        sha="a"*40
        with patch.object(lab.os,"geteuid",return_value=1000), patch.dict(lab.os.environ,{"XDG_SESSION_TYPE":"x11"}), patch.object(lab,"run",side_effect=[sha,"","GNOME Shell 46.0","arandu-foundation@arandulab"]), patch.object(lab.subprocess,"run") as execute:
            with self.assertRaises(ValueError):
                lab.validate(sha)
            execute.assert_not_called()

if __name__=="__main__":
    unittest.main()
