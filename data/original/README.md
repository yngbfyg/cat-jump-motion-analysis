# Original data and source provenance

The original 2023 archive contains a multi-keypoint DeepLabCut Excel export for the **left-ear experiment** and three coordinate TXT files from separate experiments. Files in the parent `data/` folder are cleaned-up input for modern plotting and do **not** store original frame IDs.

## Complete DeepLabCut export as CSV

[deeplabcut-all-keypoints-170-frames.csv](deeplabcut-all-keypoints-170-frames.csv) contains the complete numerical data from the original 2023 Excel workbook: **170 frames × 18 tracked body parts**, with x, y and likelihood values (55 columns including frame index). The header is flattened for easy use with Python and other tools. The original multirow Excel header is not preserved in this CSV, but its labels and values are.

## Uploaded, recoverable data

- [left-ear-all-frames.csv](left-ear-all-frames.csv): **170 original frame-indexed** left-ear x/y/likelihood observations, including low-confidence and zero-valued observations.
- [left-ear-filtered-with-frame-ids.csv](left-ear-filtered-with-frame-ids.csv): **109 selected** left-ear points, each matched back to the original Excel export to recover the frame index.

Values are in **pixels**, not centimeters. A frame number is not a timestamp. Frame/time alignment is not independently established for throat and tail.

## Uploaded original TXT sources

- [Left-ear original coordinate triples](left-ear-filtered-positions.txt), [throat](throat-filtered-positions.txt), [tail](tail-filtered-positions.txt): original tab-delimited x/y/likelihood triples, preserved with decimal commas.
- [Left-ear handwritten times](left-ear-handwritten-times.txt) and [additional handwritten times](additional-handwritten-times.txt): two original time records.

**Caution:** neither time list can automatically be aligned with confidence-filtered coordinates by row number; the original association has not been independently verified.

## Optional original Excel workbook

The source-documents package contains `left-ear-deeplabcut-170-frames.xlsx`, the untouched original multi-body-part export. The two frame-indexed CSVs above already allow examination of the original left-ear coordinate series. The original XLSX itself requires a separate upload to GitHub.

The original joint research is credited to Margarita Trott and Irina Khlebina (2023).
