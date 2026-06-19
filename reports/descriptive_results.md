# Descriptive Results

This report is generated from `data/processed/analysis_panel.csv`.
Numeric NMSF counts remain limited to source-backed `verified_count` and `verified_zero` rows. Missing observations are displayed as missing, not zero.
Rates use grade 11 enrollment as an outcome denominator and are calculated only when both the NMSF count and denominator are available.
Pathway heatmap values are covered-subset aggregates. Treat them as full pathway totals only when coverage is marked `complete_compatible_coverage`.

## Figures

| Figure | Purpose |
| --- | --- |
| `reports/figures/data_coverage_by_class.svg` | Row-level rate compatibility and missingness display. |
| `reports/figures/nmsf_rates_by_school_year.svg` | School-by-class NMSF per 100 juniors heatmap. |
| `reports/figures/pathway_by_class_heatmap.svg` | Covered-subset pathway rate heatmap with coverage labels. |
| `reports/figures/pre_post_summary.svg` | Classes 2023-2024 versus 2025-2026 observed count summary. |
| `reports/figures/public_private_counts_by_class.svg` | Observed base-public versus private totals. |
| `reports/figures/raw_nmsf_counts_by_school_year.svg` | School-by-class source-backed raw counts heatmap. |
| `reports/figures/tj_zone_counts_with_without_tjhsst.svg` | Observed TJ-zone totals with and without TJHSST. |
| `reports/figures/tjhsst_vs_base_public_private_counts.svg` | TJHSST plotted separately from base public and private rows. |

## Tables

| Table | Purpose |
| --- | --- |
| `reports/tables/data_coverage_by_class.csv` | Coverage and missingness counts by class. |
| `reports/tables/pathway_by_class_heatmap.csv` | Source table for pathway heatmap values and coverage. |
| `reports/tables/pre_post_summary_2023_2024_vs_2025_2026.csv` | Pre/post summaries for Classes 2023-2024 versus 2025-2026. |
| `reports/tables/school_counts_by_year.csv` | Raw source-backed counts and count missingness by school/class. |
| `reports/tables/school_group_totals_by_class.csv` | TJHSST, base-public, and private observed totals by class. |
| `reports/tables/school_rates_by_year.csv` | Rates, denominators, and rate missingness by school/class. |
| `reports/tables/tj_zone_counts_by_class.csv` | Observed counts with and without TJHSST by class. |

## Source And Coverage Status

| NMSF status | Rows |
| --- | --- |
| missing_source | 232 |
| not_operating | 9 |
| verified_count | 259 |
| verified_zero | 108 |

| Rate status | Rows |
| --- | --- |
| calculated | 324 |
| missing_grade11_enrollment | 43 |
| missing_nmsf_and_grade11_enrollment | 82 |
| missing_nmsf_count | 150 |
| not_operating | 9 |

| Pathway coverage status | Rows |
| --- | --- |
| complete_compatible_coverage | 231 |
| no_compatible_rows | 255 |
| partial_compatible_coverage | 122 |

## TJ-Zone Count Summary

| Class | With TJHSST observed | With TJHSST missing rows | Without TJHSST observed | Without TJHSST missing rows | TJHSST |
| --- | --- | --- | --- | --- | --- |
| 2019 | 254 | 48 | 95 | 48 | 159 |
| 2020 | 237 | 48 | 80 | 48 | 157 |
| 2021 | 212 | 49 | 80 | 49 | 132 |
| 2022 | 215 | 50 | 71 | 50 | 144 |
| 2023 | 312 | 13 | 180 | 13 | 132 |
| 2024 | 359 | 12 | 194 | 12 | 165 |
| 2025 | 288 | 5 | 207 | 5 | 81 |
| 2026 | 379 | 7 | 266 | 7 | 113 |

## Pre/Post Summary

The pre period is Classes 2023-2024 and the post period is Classes 2025-2026. Observed count totals are not adjusted for missing rows.

| Period | Group | Observed total | Annual average | Missing NMSF rows | Covered rate | Small-number warning |
| --- | --- | --- | --- | --- | --- | --- |
| pre_2023_2024 | Base public schools | 343 | 171.500000 | 2 | 0.582662 | false |
| pre_2023_2024 | Private schools | 31 | 15.500000 | 23 | 0.507614 | false |
| pre_2023_2024 | TJHSST | 297 | 148.500000 | 0 | 32.926829 | false |
| post_2025_2026 | Base public schools | 405 | 202.500000 | 6 | 0.670045 | false |
| post_2025_2026 | Private schools | 68 | 34.000000 | 6 | (missing) | false |
| post_2025_2026 | TJHSST | 194 | 97.000000 | 0 | 18.889971 | false |

## Warnings

- Small-number warnings in the tables flag observed totals below 10, where one-student changes can dominate the apparent trend.
- Private-school and historical non-FCPS rows have important NMSF and denominator gaps; the figures show available coverage rather than imputing missing schools.
- TJHSST is kept as one school row and is not split back to base public schools.
- Public pathway buckets are analytical geographies, not observed TJHSST admissions pathway outcomes.

## Cutoff And Statewide Placeholder Gap

Virginia cutoff statuses in the analysis panel: `not_sourced`. Statewide total statuses: `not_sourced`.
No Virginia Selection Index cutoff change is annotated in the figures because the cutoff fields are not sourced in the current panel.
