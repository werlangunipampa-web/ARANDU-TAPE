"""Scope gate must not equate normal source screening with release clearance."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("release_scope",ROOT/"scripts"/"verificar-escopo-release.py")
scope=importlib.util.module_from_spec(spec)
spec.loader.exec_module(scope)

class ReleaseScope(unittest.TestCase):
    def test_held_paths(self):
        self.assertEqual(scope.blocked_paths(scope.HOLD),sorted(scope.HOLD))

    def test_public_and_private_paths(self):
        self.assertEqual(scope.blocked_paths(["docs/DESIGN_CORE.md","ARANDU-DESKTOP/app.py","nested/LAB-PRIVATE/example.py"]),["nested/LAB-PRIVATE/example.py"])

    def test_immutable_ref_required(self):
        for ref in ("HEAD","main","abc123","--all"):
            with self.assertRaises(ValueError):
                scope.check(ref)

    def test_commit_tree_only(self):
        sha="a"*40
        held=sorted(scope.HOLD)[0]
        with patch.object(scope.subprocess,"check_output",side_effect=[(sha+"\n").encode(),("docs/README.md\0"+held+"\0").encode()]):
            self.assertEqual(scope.check(sha),[held])

if __name__=="__main__":
    unittest.main()
