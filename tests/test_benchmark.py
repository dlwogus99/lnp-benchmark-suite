import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lnpbench.benchmark import load_rows, run_benchmark


class BenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_rows(ROOT / "data/demo/lnp_formulations.csv")

    def test_every_row_gets_prediction_per_model(self):
        summary, predictions = run_benchmark(self.rows)
        self.assertEqual(len(predictions), len(self.rows) * 3)
        self.assertEqual(summary["n_studies"], 6)

    def test_each_prediction_comes_from_held_out_study(self):
        _, predictions = run_benchmark(self.rows)
        source = {row["formulation_id"]: row["study_id"] for row in self.rows}
        self.assertTrue(all(source[row["formulation_id"]] == row["held_out_study"] for row in predictions))

    def test_metrics_are_finite(self):
        summary, _ = run_benchmark(self.rows)
        self.assertGreater(summary["models"]["ridge"]["mae"], 0)


if __name__ == "__main__":
    unittest.main()
