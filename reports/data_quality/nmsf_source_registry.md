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
| missing_source | 474 |
| not_operating | 9 |
| verified_count | 91 |
| verified_zero | 34 |

## Observation Basis Counts

| Basis | Rows |
| --- | --- |
| complete_source_zero_inference | 34 |
| manual_transcription | 91 |
| no_source_recorded | 474 |
| school_not_operating | 9 |

## Source Coverage Counts

| Source ID | Rows |
| --- | --- |
| (none) | 483 |
| aps_2025_semifinalists | 4 |
| aps_2026_semifinalists | 4 |
| fcps_2023_semifinalists | 25 |
| fcps_2024_semifinalists | 25 |
| fcps_2025_semifinalists | 25 |
| fcps_2026_semifinalists | 25 |
| lcps_2026_semifinalists | 17 |

## Archived Sources

| Source ID | Archived File | SHA-256 |
| --- | --- | --- |
| aps_2025_semifinalists | data/raw/nmsf/aps/aps_2025_semifinalists_snapshot.csv | 3a0e137a66860cbc8a8266d9a6780ea91c0a9356b597af52af2e080bea6f0a59 |
| aps_2026_semifinalists | data/raw/nmsf/aps/aps_2026_semifinalists_snapshot.csv | 4def00f7243f66ead12ee99ab53ed621bfe13cb61c976ebe4e069e78ff631006 |
| fcps_2023_semifinalists | data/raw/nmsf/fcps/fcps_2023_semifinalists_snapshot.csv | 650629fa8bfa58ed7c46301186fa7228c2ed0e5cd1736eb3674e71b352612e83 |
| fcps_2024_semifinalists | data/raw/nmsf/fcps/fcps_2024_semifinalists_snapshot.csv | 8df2123dcb4d6f606fb0170a3f1f0fdb5c2684a6380d5a428f87df83aa812250 |
| fcps_2025_semifinalists | data/raw/nmsf/fcps/fcps_2025_semifinalists_snapshot.csv | d8da3a5ff4630944278159da0b77d3c4a95fae6f40010c135c4e38ef00abfa54 |
| fcps_2026_semifinalists | data/raw/nmsf/fcps/fcps_2026_semifinalists_snapshot.csv | 25436587ef644424c6476a967be884e61a83ba8385a187d948a49eaed194d295 |
| lcps_2025_semifinalists | data/raw/nmsf/lcps/lcps_2025_semifinalists_snapshot.csv | bdfe4856bc2c9d6c75def4551571cb910270556d5bff5a0014043306e7247d63 |
| lcps_2026_semifinalists | data/raw/nmsf/lcps/lcps_2026_semifinalists_snapshot.csv | b7d76805097061b66c8d3812ec38d0029671b1eb68ed0a773ea0807cea290259 |

## Source Rules

- Positive NMSF counts use `verified_count` and require source metadata.
- Inferred zeros use `verified_zero` only for manifest sources marked complete for the scope.
- Missing schools outside a complete source scope remain `missing_source`.
- Enrollment denominators and rates are intentionally excluded from this observation layer.

## Machine Summary

- missing_source: 474
- not_operating: 9
- verified_count: 91
- verified_zero: 34