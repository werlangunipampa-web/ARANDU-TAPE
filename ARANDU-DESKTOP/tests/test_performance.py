import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from performance import memory_kib, snapshot_mem, collect, process_info


class PerformanceContract(unittest.TestCase):
    def test_available_not_raw_free(self):
        text = ("MemTotal: 8000000 kB\nMemFree: 100000 kB\n"
                "MemAvailable: 4000000 kB\nSwapTotal: 200000 kB\n"
                "SwapFree: 150000 kB\n")
        result = snapshot_mem(text)
        self.assertAlmostEqual(result["used_excluding_reclaimable_mib"],
                               4000000 / 1024, delta=0.1)
        self.assertAlmostEqual(result["swap_used_mib"], 50000 / 1024, delta=0.1)

    def test_processes_and_load_from_mock_proc(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "meminfo").write_text(
                "MemTotal: 4096000 kB\nMemAvailable: 2048000 kB\n")
            (root / "loadavg").write_text("0.15 0.30 0.45 1/100 9\n")
            for pid, rss in ((11, 1024), (12, 4096)):
                folder = root / str(pid)
                folder.mkdir()
                (folder / "status").write_text(
                    f"Name:\tapp-{pid}\nVmRSS:\t{rss} kB\n")
            output = collect(root, limit=2)
            self.assertEqual(output["memory"]["total_mib"], 4000)
            self.assertEqual(output["load_average"]["one_min"], .15)
            self.assertEqual(output["top_processes"][0]["pid"], 12)
            self.assertEqual(output["top_processes"][0]["rss_mib"], 4.0)
            self.assertIn("páginas", output["process_rss_note"])

    def test_missing_process_is_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(process_info(99999, pathlib.Path(tmp)))

    def test_ui_does_not_sample_continuously_or_save_automatically(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        app = (root / "app.py").read_text()
        self.assertIn('Gtk.Button(label="Desempenho")', app)
        self.assertIn("def show_performance(self):", app)
        panel = app.split("    def show_performance(self):", 1)[1].split(
            "    def start_benchmark(self):", 1)[0]
        self.assertIn("collect(limit=8)", panel)
        self.assertNotIn("timeout_add", panel)
        self.assertNotIn("subprocess.Popen(", panel)
        self.assertNotIn("with open(", panel)
        self.assertNotIn("Path.open(", panel)
        self.assertNotIn("subprocess.", panel)
        core = (root / "performance.py").read_text()
        self.assertIn("parser.add_argument(\"--save\"", core)
        self.assertIn("os.O_EXCL", core)


if __name__ == "__main__":
    unittest.main()
