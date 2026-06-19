# NMSF Reconciliation 2023-2026

This report is generated for Milestone 5 from the source-backed NMSF observation layer.
TJHSST is kept as one school row; jurisdictional TJHSST subsets in APS/LCPS releases are excluded from the panel and retained only for reconciliation notes.

## Output Summary

| Output | Rows |
| --- | --- |
| data/processed/nmsf_observations_2023_2026.csv | 304 |
| reports/data_quality/manual_review_queue.csv | 181 |

## Observation Status Counts

| Status | Rows |
| --- | --- |
| missing_source | 175 |
| verified_count | 95 |
| verified_zero | 34 |

## Coverage By Division And Class

| Class | Division | Rows | Verified Count | Verified Zero | Missing Source | Not Operating |
| --- | --- | --- | --- | --- | --- | --- |
| 2023 | APS | 5 | 4 | 0 | 1 | 0 |
| 2023 | FCPS | 36 | 18 | 7 | 11 | 0 |
| 2023 | Falls Church City | 1 | 0 | 0 | 1 | 0 |
| 2023 | LCPS | 19 | 0 | 0 | 19 | 0 |
| 2023 | PWCS | 15 | 0 | 0 | 15 | 0 |
| 2024 | APS | 5 | 0 | 0 | 5 | 0 |
| 2024 | FCPS | 36 | 15 | 10 | 11 | 0 |
| 2024 | Falls Church City | 1 | 0 | 0 | 1 | 0 |
| 2024 | LCPS | 19 | 0 | 0 | 19 | 0 |
| 2024 | PWCS | 15 | 0 | 0 | 15 | 0 |
| 2025 | APS | 5 | 4 | 0 | 1 | 0 |
| 2025 | FCPS | 36 | 19 | 6 | 11 | 0 |
| 2025 | Falls Church City | 1 | 0 | 0 | 1 | 0 |
| 2025 | LCPS | 19 | 0 | 0 | 19 | 0 |
| 2025 | PWCS | 15 | 0 | 0 | 15 | 0 |
| 2026 | APS | 5 | 3 | 1 | 1 | 0 |
| 2026 | FCPS | 36 | 19 | 6 | 11 | 0 |
| 2026 | Falls Church City | 1 | 0 | 0 | 1 | 0 |
| 2026 | LCPS | 19 | 13 | 4 | 2 | 0 |
| 2026 | PWCS | 15 | 0 | 0 | 15 | 0 |

## Source Reconciliation

| Source ID | Class | Reported Total | In-Panel Count Total | Excluded Snapshot Total | Reconciled Total | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| aps_2023_semifinalists | 2023 | 17 | 15 | 2 | 17 | reconciled | Thomas Jefferson High School for Science and Technology: 2 excluded_tjhsst_resident_subset |
| aps_2025_semifinalists | 2025 | 22 | 15 | 7 | 22 | reconciled | Thomas Jefferson High School for Science and Technology: 7 excluded_tjhsst_resident_subset |
| aps_2026_semifinalists | 2026 | 30 | 20 | 10 | 30 | reconciled | Arlington Tech: 1 excluded_nonroster_school; Thomas Jefferson High School for Science and Technology: 9 excluded_tjhsst_resident_subset |
| fcps_2023_semifinalists | 2023 | 238 | 238 | 0 | 238 | reconciled | FCPS high schools including TJHSST |
| fcps_2024_semifinalists | 2024 | 264 | 264 | 0 | 264 | reconciled | FCPS high schools including TJHSST |
| fcps_2025_semifinalists | 2025 | 191 | 191 | 0 | 191 | reconciled | FCPS high schools including TJHSST |
| fcps_2026_semifinalists | 2026 | 262 | 262 | 0 | 262 | reconciled | FCPS high schools including TJHSST |
| lcps_2025_semifinalists | 2025 | 57 | 0 | 57 | 57 | reconciled | LCPS unattributed semifinalist total: 57 source_incomplete_unattributed_total |
| lcps_2026_semifinalists | 2026 | 69 | 57 | 12 | 69 | reconciled | Thomas Jefferson High School for Science and Technology: 12 excluded_tjhsst_resident_subset |

## Source Gaps

| Class | Division | Missing Rows |
| --- | --- | --- |
| 2023 | APS | 1 |
| 2023 | FCPS | 11 |
| 2023 | Falls Church City | 1 |
| 2023 | LCPS | 19 |
| 2023 | PWCS | 15 |
| 2024 | APS | 5 |
| 2024 | FCPS | 11 |
| 2024 | Falls Church City | 1 |
| 2024 | LCPS | 19 |
| 2024 | PWCS | 15 |
| 2025 | APS | 1 |
| 2025 | FCPS | 11 |
| 2025 | Falls Church City | 1 |
| 2025 | LCPS | 19 |
| 2025 | PWCS | 15 |
| 2026 | APS | 1 |
| 2026 | FCPS | 11 |
| 2026 | Falls Church City | 1 |
| 2026 | LCPS | 2 |
| 2026 | PWCS | 15 |

## Source Rules

- Positive counts are imported only from manifest-backed school-level source transcriptions.
- Verified zeros are inferred only from manifest entries marked complete for the division scope.
- Source-incomplete district totals may reconcile a source without creating school observations.
- APS/LCPS resident TJHSST subsets are not imported as separate TJHSST observations because the panel keeps TJHSST as one row.
- Missing rows remain missing; incomplete or inaccessible source searches do not become zeros.