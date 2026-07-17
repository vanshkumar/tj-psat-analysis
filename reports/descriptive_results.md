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
| `reports/tables/virginia_share_by_class.csv` | TJ-zone group counts as shares of source-backed Virginia totals. |

## Source And Coverage Status

| NMSF status | Rows |
| --- | --- |
| missing_source | 196 |
| not_operating | 9 |
| verified_count | 271 |
| verified_zero | 132 |

| Rate status | Rows |
| --- | --- |
| calculated | 362 |
| missing_grade11_enrollment | 41 |
| missing_nmsf_and_grade11_enrollment | 61 |
| missing_nmsf_count | 135 |
| not_operating | 9 |

| Pathway coverage status | Rows |
| --- | --- |
| complete_compatible_coverage | 339 |
| no_compatible_rows | 221 |
| partial_compatible_coverage | 48 |

## TJ-Zone Count Summary

| Class | With TJHSST observed | With TJHSST missing rows | Without TJHSST observed | Without TJHSST missing rows | TJHSST |
| --- | --- | --- | --- | --- | --- |
| 2019 | 254 | 48 | 95 | 48 | 159 |
| 2020 | 237 | 48 | 80 | 48 | 157 |
| 2021 | 212 | 49 | 80 | 49 | 132 |
| 2022 | 215 | 50 | 71 | 50 | 144 |
| 2023 | 325 | 0 | 193 | 0 | 132 |
| 2024 | 367 | 0 | 202 | 0 | 165 |
| 2025 | 288 | 1 | 207 | 1 | 81 |
| 2026 | 385 | 0 | 272 | 0 | 113 |

## Virginia Statewide Shares

Shares use the source-backed Virginia school-location media-packet total so the denominator matches the location-based school counts. Official NMSC state-selection-unit totals are retained separately.

| Class | Group | Count | VA total | Share % | Coverage note |
| --- | --- | --- | --- | --- | --- |
| 2023 | TJ-zone including TJHSST | 325 | 400 | 81.250000 | source-backed count and scope-matched Virginia school-location denominator |
| 2023 | TJHSST | 132 | 400 | 33.000000 | source-backed count and scope-matched Virginia school-location denominator |
| 2023 | Conventional base public | 164 | 400 | 41.000000 | source-backed count and scope-matched Virginia school-location denominator |
| 2023 | Private/homeschool unallocated | 26 | 400 | 6.500000 | source-backed count and scope-matched Virginia school-location denominator |
| 2023 | TJ-zone excluding TJHSST | 193 | 400 | 48.250000 | source-backed count and scope-matched Virginia school-location denominator |
| 2023 | Virginia outside TJ-zone | 75 | 400 | 18.750000 | source-backed count and scope-matched Virginia school-location denominator |
| 2024 | TJ-zone including TJHSST | 367 | 470 | 78.085106 | source-backed count and scope-matched Virginia school-location denominator |
| 2024 | TJHSST | 165 | 470 | 35.106383 | source-backed count and scope-matched Virginia school-location denominator |
| 2024 | Conventional base public | 175 | 470 | 37.234043 | source-backed count and scope-matched Virginia school-location denominator |
| 2024 | Private/homeschool unallocated | 26 | 470 | 5.531915 | source-backed count and scope-matched Virginia school-location denominator |
| 2024 | TJ-zone excluding TJHSST | 202 | 470 | 42.978723 | source-backed count and scope-matched Virginia school-location denominator |
| 2024 | Virginia outside TJ-zone | 103 | 470 | 21.914894 | source-backed count and scope-matched Virginia school-location denominator |
| 2025 | TJ-zone including TJHSST | (missing) | (missing) | (missing) | Virginia school-location total not source-backed for this class year |
| 2025 | TJHSST | 81 | (missing) | (missing) | Virginia school-location total not source-backed for this class year |
| 2025 | Conventional base public | (missing) | (missing) | (missing) | Virginia school-location total not source-backed for this class year |
| 2025 | Private/homeschool unallocated | 34 | (missing) | (missing) | Virginia school-location total not source-backed for this class year |
| 2025 | TJ-zone excluding TJHSST | (missing) | (missing) | (missing) | Virginia school-location total not source-backed for this class year |
| 2025 | Virginia outside TJ-zone | (missing) | (missing) | (missing) | Virginia school-location total not source-backed for this class year |
| 2026 | TJ-zone including TJHSST | 385 | 494 | 77.935223 | source-backed count and scope-matched Virginia school-location denominator |
| 2026 | TJHSST | 113 | 494 | 22.874494 | source-backed count and scope-matched Virginia school-location denominator |
| 2026 | Conventional base public | 231 | 494 | 46.761134 | source-backed count and scope-matched Virginia school-location denominator |
| 2026 | Private/homeschool unallocated | 35 | 494 | 7.085020 | source-backed count and scope-matched Virginia school-location denominator |
| 2026 | TJ-zone excluding TJHSST | 272 | 494 | 55.060729 | source-backed count and scope-matched Virginia school-location denominator |
| 2026 | Virginia outside TJ-zone | 109 | 494 | 22.064777 | source-backed count and scope-matched Virginia school-location denominator |

NMSC state-selection-unit totals are 397, 467, and 489 for Classes 2023, 2024, and 2026, compared with school-location totals of 400, 470, and 494. Classes 2023 and 2026 reconcile through boarding-school blocks; two Class 2024 students remain scope-unresolved.

## Pre/Post Summary

The pre period is Classes 2023-2024 and the post period is Classes 2025-2026. Observed count totals are not adjusted for missing rows.

| Period | Group | Observed total | Annual average | Missing NMSF rows | Covered rate | Small-number warning |
| --- | --- | --- | --- | --- | --- | --- |
| pre_2023_2024 | Base public schools | 343 | 171.500000 | 0 | 0.576209 | false |
| pre_2023_2024 | Private schools | 52 | 26.000000 | 0 | 1.430031 | false |
| pre_2023_2024 | TJHSST | 297 | 148.500000 | 0 | 32.926829 | false |
| post_2025_2026 | Base public schools | 410 | 205.000000 | 1 | 0.664926 | false |
| post_2025_2026 | Private schools | 69 | 34.500000 | 0 | 2.748815 | false |
| post_2025_2026 | TJHSST | 194 | 97.000000 | 0 | 18.889971 | false |

## Warnings

- Small-number warnings in the tables flag observed totals below 10, where one-student changes can dominate the apparent trend.
- Private-school and historical non-FCPS rows have important NMSF and denominator gaps; the figures show available coverage rather than imputing missing schools.
- TJHSST is kept as one school row and is not split back to base public schools.
- Public pathway buckets are analytical geographies, not observed TJHSST admissions pathway outcomes.

## Cutoff And Statewide Placeholder Gap

Virginia cutoff statuses in the analysis panel: `not_sourced`. Statewide total statuses: `not_sourced, source_backed_state_selection_unit_total`.
No Virginia Selection Index cutoff change is annotated in the figures because the cutoff fields are not sourced in the current panel.
