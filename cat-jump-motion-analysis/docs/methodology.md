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

1. The original exported coordinate TXT files contain only (x,y,likelihood)
   values. Frame numbers have not been preserved after manual filtering.
   Original handwritten time lists contain more entries than the exported
   coordinate lists, so pairing by row index is unjustified.
2. Some old plotting scripts hardcode a video-frame height of 1000 pixels
   even though original clips have different frame sizes.
3. The original scripts read local filenames and depend on OpenCV GUI
   windows/trackbars; there is no general command-line batch workflow.
4. Estimating physical acceleration by differentiating fitted polynomials
   requires synchronized timestamps, verified spatial scale, and an
   explicit treatment of pose-estimation uncertainty.
5. A curve fitted as y(x) is not a time parameterization. A good geometric
   fit alone does not imply physically realistic speed or acceleration.
6. Video/model weights and potentially identifiable footage have been
   intentionally excluded from this shareable draft.

## Useful future improvements

Export the DeepLabCut keypoint tracks **with original frame indices and
timestamps**; validate the pixel-to-centimeter scale independently for each
video; separate motion phases; visualize uncertainty and occlusions; compare
low-order polynomial, spline, and physically motivated ballistic models.
