"""Calculate a video-specific pixels-per-centimeter scale from marker corners.

Supply four corners measured on the original, full-resolution frame, in order
around the square, and the real side length in centimeters.
This tool does not detect the marker; see the historical OpenCV legacy scripts.
"""
import argparse
import math


def pixels_per_cm(corners: list[tuple[float, float]], side_cm: float) -> float:
    """Average four adjacent edge lengths and divide by the known side in cm."""
    if not math.isfinite(side_cm) or side_cm <= 0:
        raise ValueError("side_cm must be positive and finite")
    if len(corners) != 4:
        raise ValueError("Exactly four corners are required")
    if not all(len(c) == 2 and all(math.isfinite(v) for v in c) for c in corners):
        raise ValueError("Corners must have two finite values each")
    edges = [math.dist(corners[i], corners[(i + 1) % 4]) for i in range(4)]
    if any(edge == 0 for edge in edges):
        raise ValueError("Zero-length edge")
    return sum(edges) / (4 * side_cm)


def parse_corner(value: str) -> tuple[float, float]:
    try:
        x, y = value.split(",")
        return float(x), float(y)
    except (ValueError, TypeError) as exc:
        raise argparse.ArgumentTypeError("Use x,y format") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side-cm", required=True, type=float)
    parser.add_argument("--corners", nargs=4, required=True, type=parse_corner,
                        metavar="X,Y", help="Four corners ordered around marker")
    args = parser.parse_args()
    try:
        ratio = pixels_per_cm(args.corners, args.side_cm)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Estimated scale: {ratio:.6g} pixels/cm")
    print(f"Pass --pixels-per-cm {ratio:.9g} to src/analyze.py")
    print("Use only with observations from the same original-resolution recording.")


if __name__ == "__main__":
    main()
