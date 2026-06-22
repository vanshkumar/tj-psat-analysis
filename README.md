# tj-psat-analysis

Reproducible data pipeline and documentation for a TJHSST-area National Merit
Semifinalist analysis.

The repo builds a canonical school roster, source-backed NMSF observation layer,
grade-11 enrollment denominator panel, analysis panel, figures, tables, and
interpretive reports for graduating Classes 2019-2026. The source workbook
`docs/source_notes/tj psat investigation.xlsx` remains the seed for roster and
legacy enrollment inputs. Every numeric NMSF value, including zero, is routed
through source metadata and hash validation.

## Current Status

The core descriptive NMSF project is complete at the documented public-data
stopping point.

What is complete:

- Canonical panel: 608 school-year rows, 76 schools, Classes 2019-2026.
- Focal NMSF coverage: Classes 2023, 2024, and 2026 have complete count
  coverage from source-backed lists; Class 2025 has five public rows left
  `missing_source`.
- Public denominator coverage: the fixed public rate panel covers 54 schools,
  including TJHSST and 53 conventional base public schools.
- Private counts: all 16 rostered private schools have source-backed counts for
  Classes 2023-2026.
- Private rates: no balanced private rate panel exists because exact-year
  private grade-11 denominators remain unavailable for Classes 2024 and 2026;
  the 2023-24 NCES Private School Search locator is used only as an interim
  Class 2025 denominator source.
- Interpretation: reports support a narrow descriptive finding of reduced
  NMSF concentration at TJHSST, partial and delayed base-school gains, and no
  credible private-school offset estimate.

Known unresolved public-data items:

- A complete Class 2025 Virginia school-by-school NMSF list would resolve the
  remaining five public count gaps and allow source-backed Class 2025 statewide
  shares.
- The committed Class 2026 Virginia supplied-list snapshot totals 494
  semifinalists, while the public NMSC 2026 guide cross-check lists Virginia at
  489. Local school counts and zero-inference coverage are unchanged, but
  statewide-share denominators should be treated as provisional until that
  discrepancy is reconciled.
- Historical non-FCPS Classes 2019-2022 backfill is optional robustness work,
  not part of the current core analysis.
- Stronger causal or school-context claims require non-public/public-records
  data such as school-level PSAT participation and scores, TJ applicant/offers/
  enrollment by source school and allocation pool, and broader upper-tail
  outcomes.

## Main Outputs

- `reports/conclusions.md`: compact decision-oriented summary.
- `reports/robustness.md`: balanced panels, offsets, private sensitivity,
  statewide normalization, and policy-source caveats.
- `reports/limitations.md`: claim boundaries and missing-data limits.
- `reports/initial_findings.md`: conservative interpretation of the results.
- `reports/data_quality/focal_period_completion.md`: focal source gaps and
  stopping decision.
- `reports/descriptive_results.md`: generated figure/table inventory and
  descriptive summaries.
- `data/processed/analysis_panel.csv`: final analysis panel.
- `docs/data_dictionary.md`: field, status, and output definitions.
- `TASKS.md`: concise completion ledger and optional future work.

## Reproduce

After the uv environment has been synced, regenerate the committed artifacts
with:

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

Development checks:

```bash
UV_CACHE_DIR=.uv-cache uv run --no-sync python -m ruff format --check .
UV_CACHE_DIR=.uv-cache uv run --no-sync python -m ruff check .
UV_CACHE_DIR=.uv-cache uv run --no-sync python -m mypy
UV_CACHE_DIR=.uv-cache uv run --no-sync python -m unittest discover -s tests
```

## Data Rules

- Do not use the workbook `nsmf 2019` sheet as count evidence.
- Numeric NMSF counts require URL, title, date, and source hash.
- A missing school in an incomplete article is blank, not zero.
- `verified_zero` is valid only for complete named lists covering the relevant
  geography and class year.
- TJHSST stays as one school row; do not split TJ students back to base
  schools.
- Private-school rows are non-public/unallocated analytical buckets. School
  location alone does not establish residence, TJ eligibility, application
  status, or counterfactual base school.
- Grade-11 enrollment normalizes NMSF outcomes. It is not an admissions-seat
  allocation denominator.

## Source Boundaries

`docs/source_notes/FCPS Regulation 3355.16 TJHSST Admissions.pdf` supports the
current roster treatment of non-public applicants and the unallocated-seat pool.
It should not be applied retroactively as the governing regulation for the
Class 2025 or Class 2026 admissions cycles. Task 9 interpretation instead uses
Regulation 3355.14, Regulation 3355.15, official class-specific FCPS bulletins,
Board materials, and the documented absence of archived annual Notice 3355
procedures.

The repo is intentionally conservative: when a source is incomplete, missing
rows stay missing; when a denominator is unavailable, rates stay blank.
