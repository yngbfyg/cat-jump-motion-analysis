# Pixel-to-centimeter calibration (original 2023 method)

The original Russian instruction document specifies a bright square sticker of known physical side length attached to the launch surface. The camera should remain stationary, ideally parallel to the plane of the cat's jump.

## Original workflow

1. The color-threshold program (legacy/color_threshold_original.py) let the researcher tune an HSV range to isolate the sticker.
2. The square-detection program (legacy/square_detection_original.py) used OpenCV contours, minAreaRect and boxPoints to find and print four square-corner coordinates. The relevant rectangle was selected manually among other detections.
3. Following the original guide, the researcher measured the pixel distance between TWO ADJACENT corners using the Pythagorean theorem and divided by the real square side in centimeters:

   pixels_per_cm = sqrt((x2-x1)^2 + (y2-y1)^2) / actual_side_cm

4. The original plotting scripts then divided the tracked coordinates by a constant named kalibr. The retained scripts say "13 пикселей в 1 см", with kalibr = 13. A separate variable scale=3 resized only the video display and cancelled out in the final conversion.

The old scripts are preserved under legacy/ but do not automatically calculate or validate the physical scale. Their paths and HSV thresholds are hardcoded.

## Optional modern helper

After obtaining four square corners (in perimeter order), you can average the four edge lengths using a new, separate tool:

~~~bash
# HYPOTHETICAL 65-pixel square, 5-cm side: not a measured project value.
python src/calibration.py --side-cm 5 --corners 10,20 75,20 75,85 10,85
# Estimated scale: 13 pixels/cm
~~~

Then use a VERIFIED value to label spatial axes in centimeters:

~~~bash
python src/analyze.py --data data/ear.csv --output results/ear_cm.png --name "Left ear" --pixels-per-cm 13
~~~

The examples above are illustrative, NOT an independent confirmation that 13 pixels/cm is accurate for each original experiment. Use the same camera/video/resolution as the tracking coordinates, and measure the marker side in centimeters. If the corners were found in a resized image, convert coordinates back to the original resolution first. Perspective may require more advanced correction.

The new analysis does not compute speed or acceleration; those require reliable timing as well as calibrated positions.

## Additional original source materials

The full original archive still contains a Russian step-by-step DOCX guide (including illustrative screenshots), a PPTX presentation, full source videos, TXT files of filtered coordinates and manually collected times, and the original DeepLabCut Excel export for the left-ear experiment. The 170-row frame-indexed left-ear Excel export matches all 109 filtered left-ear points, so original frame indices for that experiment are recoverable. The standard `data/ear.csv` contains sample order, but [new frame-indexed exports](../data/original/) now preserve the original frame IDs for the left-ear experiment (170 total observations and 109 original filtered observations). Time and frame correspondence for the other two experiments is not independently verified. The DOCX/PPTX and original XLSX are available as optional source-file uploads.
