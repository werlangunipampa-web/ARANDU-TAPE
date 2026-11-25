"""Regression tests for public snapshot screening."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("snapshot_audit", ROOT / "scripts" / "auditar-snapshot.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class SnapshotAudit(unittest.TestCase):
    def test_secrets_are_detected_without_literals(self):
        self.assertIn("github-token", audit.inspect_bytes(b"gh" + b"p_" + b"Z" * 36))
        self.assertIn("private-key", audit.inspect_bytes(b"-----BEGIN " + b"PRIVATE KEY-----"))
        self.assertEqual(audit.inspect_bytes(b"OPENAI_API_KEY"), [])

    def test_restricted_paths(self):
        for path in ("x/.env", "lab-private/code.py", "data/session.db", "keys/key.pem"):
            self.assertIsNotNone(audit.inspect_path(path))
        self.assertIsNone(audit.inspect_path("ARANDU-DESKTOP/app.py"))

    def test_checkout_snapshot(self):
        commit, count, flags, review = audit.scan("HEAD")
        print(f'Public snapshot {commit}: {count} entries, {len(flags)} blocking indicators, {len(review)} research references')
        for path in review:
            print(f'REVIEW: {path!r}')
        self.assertEqual(len(commit), 40)
        self.assertGreater(count, 0)
        self.assertEqual(flags, [])
        self.assertTrue(any("ontology_contract.py" in p for p in review))

if __name__ == "__main__":
    unittest.main()
