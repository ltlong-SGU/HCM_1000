# Provenance and release boundaries

The source archive digest is in `release_metadata.json`. Every included repackaged source file has its original member path, new path, size, and SHA-256 in `source_mapping.json`. Parameter workbook filenames were standardized; data bytes are unchanged. All substantive data repairs predate this packaging and are listed in `validation/archived_reports/coordinate_changes.csv` and `time_window_changes.csv`.

Use final data and `validation/archived_reports/metadata.json` as the authoritative V2 state. Files under `provenance/pre_matrix_selection/` are intermediate candidate-selection records: their `complete: false` and `matrices_rebuilt: false` fields describe that earlier stage, not the final V2 package. They are retained for provenance only.

The 528 compressed OSRM replies consist of 484 source/destination matrix blocks and 44 canonical snapping responses. Archived replies support inspection; they do not pin the live server's historical road extract or exact profile version. Map PNG images and original notes are omitted from this public-core package because their auxiliary copyright provenance is incomplete. Administrative labels are archived inputs and their present-day accuracy is not warranted.

The construction workbook contains nominal parameters, including seed 792026. A seed and parameter table do not fully specify unarchived generator implementation details. Exact reuse of released inputs is supported; complete historical regeneration is not claimed.

This dataset package contains validation code and feasible witnesses. Full OR-Tools/PyVRP solver adapters, tuning, and comparison traces are outside this data-only package and must be provided separately before claiming end-to-end reproduction of the paper's solver experiment.

The final experiment archive SHA-256 is also recorded in `release_metadata.json`. Its 56 TXT files, eight matrices, and 168 witness/schedule/validation files (232 critical files) were compared byte-for-byte with this package's source and match. The extra external revalidation CSV is retained from that final archive. Historical construction scripts are not included here because they depend on the original separate input archive, live routing, and environment-specific paths.
