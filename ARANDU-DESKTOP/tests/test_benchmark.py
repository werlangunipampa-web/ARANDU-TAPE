import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from benchmark import (cpu_ticks, cpu_percent, sample_session, summarize,
                       compare_reports, read_report, write_private_new)


class BenchmarkContract(unittest.TestCase):
    def test_cpu_math(self):
        self.assertEqual(cpu_ticks("cpu 10 0 10 80 0 0 0 0 0 0\n"), (100, 80))
        self.assertEqual(cpu_percent((100, 80), (200, 110)), 70)
        with self.assertRaises(ValueError):
            cpu_percent((100, 80), (90, 70))

    def test_bounded_sampling_no_real_delay(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "stat").write_text("cpu 10 0 10 80\n")
            (root / "meminfo").write_text(
                "MemTotal: 4096000 kB\nMemAvailable: 2048000 kB\n")
            ticks = [100, 150, 200]
            def fake_sleep(_seconds):
                tick = ticks.pop(1)
                (root / "stat").write_text(
                    f"cpu {tick} 0 0 {100} 0\n")
            result = sample_session(2, .5, proc_root=root, sleep=fake_sleep)
            self.assertEqual(result["summary"]["count"], 2)
            self.assertEqual(len(result["samples"]), 2)
            self.assertEqual(result["summary"]["ram_used_mib"]["median"], 2000)
            for invalid in ((1, 1), (21, 1), (2, .1), (2, 10)):
                with self.assertRaises(ValueError):
                    sample_session(*invalid, proc_root=root, sleep=fake_sleep)

    def test_offline_comparison_and_private_report(self):
        samples_a = [{"ram_used_mib": 1000, "ram_available_mib": 3000,
                      "cpu_percent": 5, "swap_used_mib": 0}] * 3
        samples_b = [{"ram_used_mib": 1200, "ram_available_mib": 2800,
                      "cpu_percent": 8, "swap_used_mib": 0}] * 3
        a = {"schema": "arandu-benchmark-v1", "session": "arandu",
             "summary": summarize(samples_a)}
        b = {"schema": "arandu-benchmark-v1", "session": "gnome",
             "summary": summarize(samples_b)}
        outcome = compare_reports(a, b)
        self.assertEqual(outcome["metrics"]["ram_used_mib"]["b_minus_a"], 200)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reports" / "arandu.json"
            write_private_new(path, json.dumps(a))
            self.assertEqual(read_report(path)["session"], "arandu")
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            with self.assertRaises(FileExistsError):
                write_private_new(path, json.dumps(b))

    def test_no_background_sampling_or_network(self):
        source = (Path(__file__).resolve().parents[1] / "benchmark.py").read_text()
        self.assertIn('mode.add_argument("--measure"', source)
        self.assertIn('mode.add_argument("--compare"', source)
        self.assertNotIn("threading", source)
        self.assertNotIn("requests.", source)
        self.assertNotIn("subprocess.", source)
        self.assertNotIn("shell=True", source)


if __name__ == "__main__":
    unittest.main()
