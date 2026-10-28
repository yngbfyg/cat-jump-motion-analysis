# Original data and source provenance

The original 2023 archive contains a multi-keypoint DeepLabCut Excel export for the **left-ear experiment** and three coordinate TXT files from separate experiments. Files in the parent \`data/\` folder are cleaned-up input for modern plotting and do **not** store original frame IDs.

## Uploaded, recoverable data

- [left-ear-all-frames.csv](left-ear-all-frames.csv): **170 original frame-indexed** left-ear x/y/likelihood observations, including low-confidence and zero-valued observations.
- [left-ear-filtered-with-frame-ids.csv](left-ear-filtered-with-frame-ids.csv): **109 selected** left-ear points, each matched back to the original Excel export to recover the frame index.

Values are in **pixels**, not centimeters. A frame number is not a timestamp. Frame/time alignment is not independently established for throat and tail.

## Historical source files (optional upload)

The source-package ZIP also includes:
- \`left-ear-deeplabcut-170-frames.xlsx\`: unmodified original 2023 multi-body-part spreadsheet;
- \`left-ear-filtered-positions.txt\`, \`throat-filtered-positions.txt\`, \`tail-filtered-positions.txt\`: original tab-separated coordinate triples, with decimal commas;
- \`left-ear-handwritten-times.txt\`, \`additional-handwritten-times.txt\`: the original handwritten time values.

The source TXT time lists **must not** be paired to filtered coordinates by row index without verifying their association. These binary/original files require a separate upload if not yet visible here.

The original joint research is credited to Margarita Trott and Irina Khlebina (2023).
