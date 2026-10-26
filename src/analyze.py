"""Plot tracked keypoint samples from the original Cat Jump project.

The CSV files contain filtered keypoint observations, not frame numbers.
The plot deliberately uses *sample order*, never seconds, and makes no
claim to estimate physical speed or acceleration.
"""

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def load_samples(path: Path, min_confidence: float = 0.0) -> np.ndarray:
    """Return columns sample_index, x_px, y_px, confidence."""
    if not 0 <= min_confidence <= 1:
        raise ValueError("min_confidence must be between 0 and 1")
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        expected = {"sample_index", "x_px", "y_px", "confidence"}
        if not expected.issubset(reader.fieldnames or []):
            raise ValueError(f"CSV must contain columns: {', '.join(sorted(expected))}")
        rows = []
        for row in reader:
            values = [float(row[k]) for k in ("sample_index", "x_px", "y_px", "confidence")]
            if not all(np.isfinite(values)):
                raise ValueError("CSV contains non-finite values")
            if not 0 <= values[3] <= 1:
                raise ValueError("confidence must be between 0 and 1")
            if values[3] >= min_confidence:
                rows.append(values)
    if not rows:
        raise ValueError("No samples remain after confidence filtering")
    return np.asarray(rows, dtype=float)


def fit_trajectory(samples: np.ndarray, degree: int = 2):
    """Fit y(x); return (x_grid, y_grid, root-mean-square residual)."""
    if degree < 1:
        raise ValueError("degree must be at least one")
    x, y = samples[:, 1], samples[:, 2]
    if len(np.unique(x)) <= degree:
        raise ValueError("Not enough unique x positions for this polynomial degree")
    # Center/scale x before fitting for numerical stability.
    mu, sd = float(np.mean(x)), float(np.std(x))
    if sd == 0:
        raise ValueError("All x positions are identical")
    x_scaled = (x - mu) / sd
    coeff = np.polyfit(x_scaled, y, degree)
    grid = np.linspace(float(x.min()), float(x.max()), 250)
    fitted = np.polyval(coeff, (grid - mu) / sd)
    rmse = float(np.sqrt(np.mean((np.polyval(coeff, x_scaled) - y) ** 2)))
    return grid, fitted, rmse


def plot_samples(samples: np.ndarray, output: Path, name: str, degree: int | None) -> None:
    indices, x, y, confidence = samples.T
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.4), layout="constrained")
    ax = axs[0]
    scatter = ax.scatter(x, y, c=confidence, s=25, cmap="viridis", vmin=0, vmax=1)
    if degree is not None:
        grid, values, rmse = fit_trajectory(samples, degree)
        ax.plot(grid, values, color="orangered", lw=2,
                label=f"Degree {degree} fit (RMSE {rmse:.1f} px)")
        ax.legend(fontsize=8)
    ax.invert_yaxis()  # Video/image coordinates: y increases downward.
    ax.set_xlabel("X position (pixels)")
    ax.set_ylabel("Y position (pixels; origin at top)")
    ax.set_title("Observed keypoint trajectory")
    ax.grid(alpha=0.2)
    fig.colorbar(scatter, ax=ax, label="Keypoint confidence", shrink=0.83)

    ax = axs[1]
    ax.plot(indices, x, '.-', label='X (px)', markersize=3)
    ax.plot(indices, y, '.-', label='Y (px)', markersize=3)
    ax.set_xlabel("Recorded sample index (NOT frame or time)")
    ax.set_ylabel("Position (pixels)")
    ax.set_title("Tracked positions in recorded order")
    ax.legend()
    ax.grid(alpha=0.2)
    fig.suptitle(f"Cat Jump | {name} | {len(samples)} retained observations", fontsize=13)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path, help="CSV of keypoint samples")
    parser.add_argument("--output", required=True, type=Path, help="Output PNG path")
    parser.add_argument("--name", default="tracked keypoint")
    parser.add_argument("--degree", type=int, default=0,
                        help="Optional degree for illustrative y(x) curve fit; default 0 (off)")
    parser.add_argument("--min-confidence", type=float, default=0.0)
    args = parser.parse_args()
    samples = load_samples(args.data, args.min_confidence)
    plot_samples(samples, args.output, args.name,
                 None if args.degree == 0 else args.degree)
    print(f"Saved {args.output} ({len(samples)} samples)")


if __name__ == "__main__":
    main()
