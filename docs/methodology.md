# Methodology notes and known issues

These notes summarize the original project files; they are not a scientific
validation of the original physical measurements.

## Original procedure

The original Russian-language instruction document describes a controlled
recording setup: bright lighting, a simple background, a fixed camera
roughly parallel to the jump plane, and a square marker of known side length.
Video was processed with DeepLabCut's Google Colab Model Zoo notebook.
Selected x/y/likelihood columns were copied out of the resulting CSV and
low-confidence detections were discarded. OpenCV HSV thresholding and
rectangle corners were used to estimate image scale. Separate interactive
Python scripts then plotted trajectory, position against handwritten time,
speed, and acceleration based on polynomial coefficients.

## Caveats discovered when preparing a reproducible public demo

1. The filtered TXT coordinate files contain only (x,y,likelihood), without
   original frame indices. The original source archive also has a full
   DeepLabCut Excel export for the left-ear experiment (170 frame-numbered
   entries). All 109 filtered left-ear points match that export, so indices
   have been recovered for this experiment in `data/original/`. The
   original Excel workbook is also included in that folder. Frame/time
   mapping for the other experiments remains unverified, and filtered
   rows cannot simply be paired with handwritten time lists.
2. Some old plotting scripts hardcode a video-frame height of 1000 pixels
   even though original clips have different frame sizes.
3. The original scripts read local filenames and depend on OpenCV GUI
   windows/trackbars; there is no general command-line batch workflow.
4. Estimating physical acceleration by differentiating fitted polynomials
   requires synchronized timestamps, verified spatial scale, and an
   explicit treatment of pose-estimation uncertainty.
5. A curve fitted as y(x) is not a time parameterization. A good geometric
   fit alone does not imply physically realistic speed or acceleration.
6. Short preview footage is included in `media/`: `tracking_demo.gif`,
   `original_jump.mp4`, and `tracked_jump.mp4`. The videos were recorded
   by Margarita Trott or derived from her recordings. Full-length raw
   recordings and pretrained DeepLabCut model weights are not included.

## Useful future improvements

Export the DeepLabCut keypoint tracks **with original frame indices and
timestamps**; validate the pixel-to-centimeter scale independently for each
video; separate motion phases; visualize uncertainty and occlusions; compare
low-order polynomial, spline, and physically motivated ballistic models.

## Pixel-to-centimeter calibration

The original video workflow used a colored square of known size: HSV thresholding,
contour/rectangle corners and a pixels-per-centimeter coefficient stored as
kalibr = 13 in historical plot scripts. The camera/resolution/physical marker
measurements have not been revalidated for all experiments. See
[calibration.md](calibration.md) for the original method and the modern optional
scale calculator. Default regenerated plots stay in pixels.
