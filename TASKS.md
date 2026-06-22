# Project Status And Completion Ledger

This file is now a concise completion ledger. Earlier milestone-by-milestone
planning prose has been folded into the generated reports, data-quality outputs,
and `README.md`.

## Final Public-Data Stopping Point

The core descriptive NMSF analysis is complete at the current public-data
stopping point.

- The canonical roster, aliases, school history, public identifiers, and
  private PSS identifiers are validated.
- The analysis panel has 608 rows: 76 schools across Classes 2019-2026.
- Every school-year has an explicit NMSF status such as `verified_count`,
  `verified_zero`, `missing_source`, or `not_operating`.
- Every numeric NMSF value has source URL, title, date, and source hash.
- Grade-11 enrollment is either sourced or explicitly blank with a status.
- Figures, tables, data-quality reports, and Task 9 interpretation are
  regenerated from committed inputs.

## Remaining Public NMSF Count Gaps

The focal Classes 2023, 2024, and 2026 have complete count coverage. Class 2025
has five remaining public `missing_source` rows:

| Class | Division | School |
| --- | --- | --- |
| 2025 | Falls Church City | Meridian High School |
| 2025 | LCPS | Loudoun Valley High School |
| 2025 | LCPS | Park View High School |
| 2025 | LCPS | Tuscarora High School |
| 2025 | LCPS | Woodgrove High School |

Do not infer zeros for these rows from the total-only LCPS release, incomplete
local articles, or failed searches. Resolve them only with a school-attributed
source or a complete Class 2025 Virginia list.

## Private-School Status

Private-school focal-period counts are complete: all 16 rostered private rows
have source-backed counts for Classes 2023-2026.

That does not create a credible private-school offset estimate. The exact
grade-11 denominator years needed for comparable private rates are not complete:
the 2023-24 NCES Private School Search locator supports only an interim Class
2025 denominator pass, while Classes 2024 and 2026 still lack compatible
private denominator rows. Counts also do not establish residence, TJHSST
eligibility, applications, or counterfactual base-school placement.

## Statewide-Share Caveat

The panel carries source-backed Virginia statewide totals for Classes 2023,
2024, and 2026 from complete list snapshots, and leaves Class 2025 blank in the
canonical panel. The Class 2026 supplied-list snapshot currently totals 494,
while the public NMSC 2026 guide lists Virginia at 489 semifinalists. This
does not change local school counts or focal coverage, but statewide-share
metrics should be treated as provisional until the discrepancy is reconciled.

## Optional Future Work

Only continue NMSF scraping when a source can resolve multiple rows or a whole
class-year scope. Do not resume low-yield school-by-school searching as routine
cleanup.

Highest-value optional additions:

- Complete Class 2025 Virginia school-by-school NMSF list.
- Official NCES PSS 2023-24 public-use file, once available, to replace the
  locator supplement and preserve imputation flags.
- Complete Virginia Class 2022 or Class 2021 lists if recovered through a broad
  source workflow.
- School-level PSAT participation and score distributions.
- TJ applicant, eligible-applicant, offer, waitpool, acceptance, enrolled
  student, and allocation-pool counts by source school or division.
- Eighth-grade allocation population inputs used in the relevant TJ admissions
  cycles.
- Broader right-tail outcomes such as SAT thresholds, AP 5 rates, AIME, USACO,
  and other competition results.

Out of scope for the current public-data package:

- Guessing or interpolating missing counts.
- Treating absent names in incomplete articles as zero.
- Public-records requests.
- Reconstructing every historical Virginia cutoff.
- Reassigning TJHSST students to base schools.

## Class-Year Mapping

| Graduating class | Qualifying PSAT year | Grade 11 enrollment year |
| ---: | ---: | ---: |
| 2019 | Fall 2017 | 2017-18 |
| 2020 | Fall 2018 | 2018-19 |
| 2021 | Fall 2019 | 2019-20 |
| 2022 | Fall 2020 | 2020-21 |
| 2023 | Fall 2021 | 2021-22 |
| 2024 | Fall 2022 | 2022-23 |
| 2025 | Fall 2023 | 2023-24 |
| 2026 | Fall 2024 | 2024-25 |

## Regeneration Commands

```bash
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_seed_data.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_school_roster.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_enrollment_panel.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/apply_nmsf_counts.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_nmsf_observations.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_nmsf_pilot_2023_2026.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_focal_period_completion.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_analysis_panel.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_descriptive_outputs.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_task9_outputs.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/validate_nmsf_sources.py data/interim/panel_nmsf.csv
```

## Canonical Reports

- `reports/conclusions.md`
- `reports/robustness.md`
- `reports/limitations.md`
- `reports/initial_findings.md`
- `reports/task9_completion.md`
- `reports/descriptive_results.md`
- `reports/data_quality/focal_period_completion.md`
- `reports/data_quality/final_panel_checks.md`
- `docs/data_dictionary.md`
