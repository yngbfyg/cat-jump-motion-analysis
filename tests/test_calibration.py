"""Unit tests for square-marker calibration and centimeter plotting."""
import math
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analyze import plot_samples
from calibration import pixels_per_cm


class TestCalibration(unittest.TestCase):
    def test_square_scale(self):
        self.assertAlmostEqual(
            pixels_per_cm([(10, 20), (75, 20), (75, 85), (10, 85)], 5), 13
        )

    def test_rotated_square(self):
        d = 5 / math.sqrt(2)
        self.assertAlmostEqual(
            pixels_per_cm([(0, -d), (d, 0), (0, d), (-d, 0)], 1), 5
        )

    def test_invalid_side(self):
        corners = [(0, 0), (5, 0), (5, 5), (0, 5)]
        for value in [0, -1, float("inf"), float("nan")]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                pixels_per_cm(corners, value)

    def test_invalid_corners(self):
        with self.assertRaises(ValueError):
            pixels_per_cm([(0, 0), (0, 0), (5, 5), (0, 5)], 5)

    def test_plot_in_cm_without_mutation(self):
        points = np.array([[0, 13, 26, 0.95], [1, 26, 39, 0.93],
                           [2, 39, 52, 0.92]])
        original = points.copy()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "test_cm.png"
            plot_samples(points, output, "Demo", None, pixels_per_cm=13)
            self.assertTrue(output.exists())
        np.testing.assert_array_equal(points, original)

    def test_negative_scale_rejected(self):
        points = np.array([[0, 13, 26, 0.9]])
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(ValueError):
            plot_samples(points, Path(tmp) / "bad.png", "Demo", None,
                         pixels_per_cm=-1)


if __name__ == "__main__":
    unittest.main()
