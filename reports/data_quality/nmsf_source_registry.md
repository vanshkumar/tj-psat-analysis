# NMSF Source Registry Report

This report is generated from the Milestone 4 NMSF observation builder.
Counts and verified zeros are stored separately from enrollment denominators.

## Output Summary

| Output | Rows |
| --- | --- |
| data/processed/nmsf_observations.csv | 608 |

## Observation Status Counts

| Status | Rows |
| --- | --- |
| missing_source | 524 |
| not_operating | 9 |
| verified_count | 53 |
| verified_zero | 22 |

## Observation Basis Counts

| Basis | Rows |
| --- | --- |
| complete_source_zero_inference | 22 |
| manual_transcription | 53 |
| no_source_recorded | 524 |
| school_not_operating | 9 |

## Source Coverage Counts

| Source ID | Rows |
| --- | --- |
| (none) | 533 |
| fcps_2024_semifinalists | 25 |
| fcps_2025_semifinalists | 25 |
| fcps_2026_semifinalists | 25 |

## Source Rules

- Positive NMSF counts use `verified_count` and require source metadata.
- Inferred zeros use `verified_zero` only for manifest sources marked complete for the scope.
- Missing schools outside a complete source scope remain `missing_source`.
- Enrollment denominators and rates are intentionally excluded from this observation layer.

## Machine Summary

- missing_source: 524
- not_operating: 9
- verified_count: 53
- verified_zero: 22