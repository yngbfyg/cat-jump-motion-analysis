"""Quick standard-library tests: python -m unittest discover -s tests -v."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analyze import fit_trajectory, load_samples


class TestAnalysis(unittest.TestCase):
    def make_csv(self, rows):
        tmp = tempfile.TemporaryDirectory()
        path = Path(tmp.name) / 'samples.csv'
        with path.open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['sample_index', 'x_px', 'y_px', 'confidence'])
            writer.writerows(rows)
        self.addCleanup(tmp.cleanup)
        return path

    def test_load_and_filter(self):
        path = self.make_csv([[0, 1, 2, .7], [1, 3, 4, .95]])
        samples = load_samples(path, 0.8)
        self.assertEqual(samples.shape, (1, 4))
        self.assertAlmostEqual(samples[0, 1], 3.0)

    def test_empty_after_filter(self):
        with self.assertRaises(ValueError):
            load_samples(self.make_csv([[0, 1, 2, .4]]), 0.9)

    def test_bad_confidence(self):
        with self.assertRaises(ValueError):
            load_samples(self.make_csv([[0, 1, 2, 1.5]]))

    def test_quadratic_fit(self):
        x = np.arange(6, dtype=float)
        points = np.column_stack([x, x, 2*x*x + 3, np.ones_like(x)])
        _xx, _yy, rmse = fit_trajectory(points, degree=2)
        self.assertLess(rmse, 1e-9)

    def test_insufficient_unique_x(self):
        with self.assertRaises(ValueError):
            fit_trajectory(np.array([[0, 1, 2, .8], [1, 1, 3, .9]]), degree=2)


if __name__ == '__main__':
    unittest.main()
