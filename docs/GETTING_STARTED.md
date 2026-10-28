# Getting started — Cat Jump Motion Analysis

This repository contains the 2023 school project **Кошкоскок**, created by Margarita Trott and Irina Khlebina, plus newer scripts that make some saved data easier to reproduce. There are **two distinct workflows**: replot existing keypoint data (easy), or repeat the original video experiment (manual, more involved). We used a pretrained **DeepLabCut Model Zoo** model; we did not train one.

## A. Reproduce the saved plots (recommended)

Use Python 3.10+; open a terminal in the cloned repository folder.

~~~bash
python3 -m venv .venv
source .venv/bin/activate                # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python src/analyze.py --data data/ear.csv --output results/ear.png --name "Left ear"
python src/analyze.py --data data/throat.csv --output results/throat.png --name "Throat"
python src/analyze.py --data data/tail.csv --output results/tail.png --name "Tail"
python -m unittest discover -s tests -v
~~~

Outputs: one PNG per keypoint, showing its x/y trajectory (colored by confidence) and coordinate sequences. The x/y coordinates are **pixels**. The sample order in these three filtered CSVs is **not time** or necessarily the original frame index.

To overlay a *descriptive* quadratic fit (not a validated physics model):

~~~bash
python src/analyze.py --data data/ear.csv --output results/ear_fit.png --name "Left ear" --degree 2
~~~

### DeepLabCut source data and recovered frame indices

- [Full body-point export — 170 frames and 18 keypoints](../data/original/deeplabcut-all-keypoints-170-frames.csv): a portable, flat-column CSV converted from the original Excel workbook.

### Recovered frame indices for experiment 1 (left ear)

- [Full left-ear data — 170 frames](../data/original/left-ear-all-frames.csv): original frame ID, x/y pixel coordinates and likelihood, including low-confidence observations.
- [Filtered left-ear data — 109 records](../data/original/left-ear-filtered-with-frame-ids.csv): original selected point sequence matched to the full export to restore frame IDs.

These new CSVs were extracted from the original DeepLabCut Excel file. For other experiments, reliable frame/time correspondence has not been reconstructed. Frame number is **not** seconds: interpreting it as elapsed time requires verified source-video FPS.

## B. Calibrate pixel positions to centimeters

The original 2023 procedure used a **bright square sticker of known physical side length** on the jump surface. The color-isolation program [legacy/color_threshold_original.py](../legacy/color_threshold_original.py) displayed HSV trackbars. [legacy/square_detection_original.py](../legacy/square_detection_original.py) searched image contours and printed rectangle corners.

For your own video, choose the square's four corner coordinates **in original-resolution pixels**, in perimeter order. Average the four edge lengths and divide by the physical side length in cm:

~~~bash
# HYPOTHETICAL numbers, not a historical measurement:
python src/calibration.py --side-cm 5 --corners 10,20 75,20 75,85 10,85
# 13 pixels/cm for this imaginary 65-pixel marker
~~~

Supply your **independently verified** scale to the plotting program:

~~~bash
python src/analyze.py --data data/ear.csv --output results/ear_cm.png \
  --name "Left ear" --pixels-per-cm 13
~~~

The historical original scripts contained a setting `kalibr = 13`, with the comment "13 pixels per cm". **Do not reuse 13 automatically** for a different video or camera setup. Adjust for resizing and perspective. See [calibration details](calibration.md).

## C. Original video-to-graph experiment (2023 school instructions)

This is a faithful English explanation of the original Russian [2023 instruction document](original/README.md), not an assertion that the legacy GUI tools run unmodified on current platforms.

1. **Record a video.** Use good lighting and a plain background. Attach the brightly colored measured square to the surface the cat jumps from. Keep the camera fixed, ideally parallel to the jump plane.
2. **Run the existing pose-estimation notebook.** The original workflow used the [DeepLabCut Model Zoo Google Colab notebook](https://colab.research.google.com/github/DeepLabCut/DeepLabCut/blob/master/examples/COLAB/COLAB_DLC_ModelZoo.ipynb). Follow its current upload and inference steps. In the 2023 guide, the result was a coordinate CSV, video with colored keypoints, and keypoint-color legend. The notebook UI may have changed.
3. **Select a keypoint and filter confidence.** Watch the labeled footage; select one anatomical landmark (the school project studied left ear, throat and tail). Save its x/y/likelihood columns. The old guide suggested keeping detections with likelihood above about 0.7–0.8. **Keep frame IDs in any new experiment**; the original filtered TXT files lost them.
4. **Measure the reference square.** Use the original HSV color-selection and rectangle-corner programs, noting that their filenames and thresholds are hardcoded. Compute adjacent-corner pixel distance divided by the sticker's side length in centimeters. The legacy GUI scripts need a separately installed `opencv-python` package and may need compatibility fixes (e.g., older NumPy naming). They do not automatically calculate scale.
5. **Build the original graphs.** The programs preserved under [legacy/](../legacy/) are named for trajectory, position over time, velocity and acceleration. The historical guide asks the researcher to select a segment using left/right sliders, view selected points by pressing space, then advance with **q** to fitted polynomials of several degrees. Time values were manually recorded from visible video/laptop frames. To plot velocities, the user entered coefficients from the position fits; to plot accelerations, they entered coefficients from the velocity fits.
6. **Interpret with caution.** The original 27 graphs remain available in the [research gallery](../results/original/README.md). Original speed and acceleration graphs are **historical exploratory outputs**, not independently validated measures; aligning frames, timing, calibration and confidence is essential to any new physics analysis.

The original scripts expect manual paths, screen windows, handwritten time lists and manually chosen polynomial coefficients. They are **not an automated end-to-end pipeline**. The newer `src/analyze.py` works on saved coordinates only; it does not rerun DeepLabCut or compute physical speed or acceleration.

## Files and reproducibility

| Location | Purpose |
|---|---|
| [data/](../data/) | Simplified coordinate files used by the new plotter |
| [data/original/](../data/original/) | Original 2023 XLSX and TXT files, plus restored left-ear frame IDs |
| [results/original/](../results/original/README.md) | All 27 original figures (three experiments) |
| [media/](../media/) | Short original/tracked video examples and animated GIF |
| [legacy/](../legacy/) | Original Python programs as historical reference |
| [docs/calibration.md](calibration.md) | Original and optional modern spatial calibration |
| [docs/original/](original/README.md) | Unmodified Russian DOCX manual and PPTX presentation |

**Project attribution:** original joint research by Margarita Trott and Irina Khlebina; original video recordings by Margarita Trott.
