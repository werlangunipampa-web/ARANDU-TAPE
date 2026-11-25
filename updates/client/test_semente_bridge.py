#!/usr/bin/env python3
import pathlib
import tempfile
import unittest
from semente_bridge import view, read_status

class TestBridge(unittest.TestCase):
    def test_failure_hidden(self):
        self.assertEqual(view({"status": "unavailable"})["indicator"], "hidden")
    def test_found_not_installable(self):
        result = view({"status": "stable_release_found", "version": "v2.8.4"})
        self.assertEqual(result["indicator"], "informational")
        self.assertFalse(result["install_enabled"])
        self.assertFalse(result["release_verified"])
    def test_bad_tag_hidden(self):
        self.assertEqual(view({"status": "stable_release_found", "version": "bad"})["indicator"], "hidden")
    def test_missing_file(self):
        self.assertIsNone(read_status(pathlib.Path("/nonexistent/arandu-status.json")))

if __name__ == "__main__":
    unittest.main()
