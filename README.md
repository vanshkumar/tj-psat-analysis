# tj-psat-analysis

Reproducible data pipeline for a TJHSST admissions-change analysis.

The current checked-in pipeline builds a canonical school roster, source-backed
NMSF observation layer, grade-11 enrollment denominator panel, and analytical
panel for Classes 2019-2026. The source workbook
`docs/source_notes/tj psat investigation.xlsx` remains the seed for roster and
legacy enrollment inputs, while every numeric NMSF count is sourced through the
manifest and observation layer.

Canonical aliases, school-history events, public NCES identifiers, and
admissions-policy caveats come from curated repo inputs and
`docs/source_notes/FCPS Regulation 3355.16 TJHSST Admissions.pdf`. That
regulation supports treating private-school rows as non-public applicants for
unallocated seats rather than assigning them from school location alone. High
school NMSF pathway buckets remain analytical geographies unless actual TJHSST
pathway/offers data are sourced later. Annual Notice 3355 materials and older
regulation versions are still needed before making class-specific admissions
mechanism claims.

## Pipeline Build

After the uv environment is already synced, the current committed artifacts can
be regenerated with:

```bash
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_seed_data.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_school_roster.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_enrollment_panel.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/apply_nmsf_counts.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_nmsf_observations.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_nmsf_pilot_2023_2026.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_analysis_panel.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_descriptive_outputs.py
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/validate_nmsf_sources.py data/interim/panel_nmsf.csv
UV_CACHE_DIR=.uv-cache uv run --no-sync python -m unittest discover -s tests
```

Generated pipeline outputs include:

- `data/manual/tj psat investigation.xlsx`
- `data/interim/canonical_schools.csv`
- `data/interim/public_enrollment_raw.csv`
- `data/interim/public_grade11_enrollment.csv`
- `data/interim/panel_seed.csv`
- `data/interim/panel_nmsf.csv`
- `data/processed/analysis_panel.csv`
- `data/processed/enrollment_panel.csv`
- `data/processed/nmsf_observations.csv`
- `data/processed/nmsf_observations_2023_2026.csv`
- `data/processed/schools.csv`
- `data/processed/school_roster.csv`
- `data/processed/public_enrollment.csv`
- `data/processed/class_year_mapping.csv`
- `data/manual/public_school_nces_ids.csv`
- `data/manual/school_aliases.csv`
- `data/manual/school_history.csv`
- `reports/data_quality/workbook_ingestion.md`
- `reports/data_quality/roster_review.md`
- `reports/data_quality/enrollment_coverage.md`
- `reports/data_quality/nmsf_source_registry.md`
- `reports/data_quality/nmsf_reconciliation_2023_2026.md`
- `reports/data_quality/final_panel_checks.md`
- `reports/descriptive_results.md`
- `reports/figures/*.svg`
- `reports/tables/*.csv`

The build command reads the seed workbook from
`docs/source_notes/tj psat investigation.xlsx`, preserves it unchanged, and
creates a byte-identical copy under `data/manual/` for the manual source
inventory required by the task plan.

`scripts/build_school_roster.py` builds the Milestone 2 roster deliverables
from the seed roster, curated source files, and the admissions-policy PDF. To
refresh public-school NCES IDs from the official CCD directory ZIP, run:

```bash
python scripts/build_school_roster.py --ccd-directory-zip /path/to/ccd_sch_029_2324_w_1a_073124.zip
```

The roster build accepts `--admissions-policy-pdf` if the admissions-policy PDF
is moved from its default path.

## Enrollment Denominators

Milestone 3 builds a school-by-class-year grade-11 enrollment panel with
machine-readable missingness statuses:

```bash
python scripts/ingest_public_enrollment_2024_25.py \
  --membership-zip /path/to/ccd_sch_052_2425_l_1a_073025.zip

python scripts/ingest_private_pss.py \
  --pss-zip 2017-18=/path/to/pss1718_pu_csv.zip \
  --pss-zip 2019-20=/path/to/pss1920_pu_csv.zip \
  --pss-zip 2021-22=/path/to/pss2122_pu_csv.zip

python scripts/build_enrollment_panel.py
```

The public Class 2026 source is the NCES CCD 2024-25 school membership file.
Private-school rows use curated PSS `PPIN` matches, `P290` for grade 11, and
preserve `F_P290`; PSS non-survey years are left blank rather than estimated.

## Development Checks

```bash
UV_CACHE_DIR=.uv-cache uv run --no-sync python -m ruff format --check .
UV_CACHE_DIR=.uv-cache uv run --no-sync python -m ruff check .
UV_CACHE_DIR=.uv-cache uv run --no-sync python -m mypy
UV_CACHE_DIR=.uv-cache uv run --no-sync python -m unittest discover -s tests
```

## NMSF Count Ingestion

`data/sources/nmsf_counts.csv` stores source-backed count transcriptions. The
current source slices cover official FCPS/TJHSST National Merit Semifinalist
releases for Classes 2019 through 2026, APS releases for Classes 2023, 2025,
and 2026, PWCS public high-school releases for Classes 2023, 2024, 2025, and
2026, LCPS school-attributed releases for Classes 2023, 2024, and 2026, and a
total-only LCPS release for Class 2025. It also includes local Patch
articles for Fairfax City, McLean, Vienna/Oakton, Arlington, Falls Church,
Ashburn/Loudoun, and Woodbridge school rows not covered by the district
releases.
The importer computes source hashes from the
source metadata plus transcribed count rows, matches schools against the
canonical roster, and writes `data/interim/panel_nmsf.csv`.

`scripts/build_nmsf_observations.py` builds the Milestone 4 count-observation
layer at `data/processed/nmsf_observations.csv`. It validates
`data/sources/source_manifest.yml`, keeps NMSF observations separate from
enrollment denominators, and uses `verified_zero` only for manifest sources
marked complete for the relevant scope. The current FCPS 2019-2026, PWCS
2023-2026, APS 2023/2025/2026, and LCPS 2023/2024/2026 official sources are complete
named public high-school lists, so absent rostered public schools inside those
scopes receive source-backed zero observations for those classes. Schools
outside the source scope remain `missing_source`. APS/LCPS resident TJHSST
subsets and PWCS former-middle-school TJHSST references are retained in
count-only source snapshots for reconciliation but are not imported as separate
observations because TJHSST remains one school row.
The official LCPS Class 2025 release is retained as a source-incomplete total
for reconciliation only because it does not list school affiliations; a local
Ashburn Patch article supplies the imported positive LCPS Class 2025 school rows.
Overlapping public-school rows from the Patch articles are retained only in
source snapshots when official district rows already cover those counts; the
local articles are not used for zero inference.

`scripts/build_nmsf_pilot_2023_2026.py` builds the Milestone 5 pilot outputs:
`data/processed/nmsf_observations_2023_2026.csv`,
`reports/data_quality/nmsf_reconciliation_2023_2026.md`, and
`reports/data_quality/manual_review_queue.csv`. The current four-year pilot has
304 observation rows: 189 `verified_count`, 78 `verified_zero`, and 37
`missing_source`. The reconciliation report's Source Gaps table is the
authoritative summary of unresolved observations; the manual review queue also
contains excluded count-only snapshot rows used to reconcile source totals.

The historical Classes 2019-2022 backfill is optional robustness work rather
than a prerequisite for the analytical panel. The pre-analysis stopping point is
the official FCPS/TJHSST 2019-2022 slice already in the main observation layer;
non-FCPS historical rows should remain `missing_source` unless a clear,
source-backed bulk lead is added later.

## Analysis Panel

`scripts/build_analysis_panel.py` joins the canonical roster, NMSF observation
layer, enrollment panel, class-year mapping, and school-history flags into
`data/processed/analysis_panel.csv`.

The panel calculates `nmsf_per_100_juniors` only when both a source-backed NMSF
count and a grade-11 denominator are present. Missing NMSF observations and
missing denominators remain blank with status fields rather than being imputed.
Pathway aggregate fields are covered-subset totals: they sum only school rows
with compatible NMSF and denominator coverage, and they include coverage flags
showing whether the pathway-year is complete, partial, or has no compatible
rows. The pathway buckets are analytical geographies, not observed TJHSST
admissions pathways.

Virginia NMSF Selection Index cutoff and statewide semifinalist total columns
are included as `not_sourced` placeholders until reliable class-year sources
are added. Grade-11 enrollment denominators are kept separate from admissions
seat-allocation inputs; no 8th-grade allocation population is included in this
panel.

## Descriptive Outputs

`scripts/build_descriptive_outputs.py` reads `data/processed/analysis_panel.csv`
and generates Task 8 outputs under `reports/figures/`, `reports/tables/`, and
`reports/descriptive_results.md`.

The figures include school-by-class raw-count and per-100-juniors heatmaps, a
pathway-by-class covered-rate heatmap, TJHSST/base-public/private comparisons,
TJ-zone totals with and without TJHSST, base-public versus private totals,
pre/post summaries for Classes 2023-2024 versus 2025-2026, and a data-coverage
chart. The companion tables keep observed NMSF count totals separate from
rate-compatible count/enrollment totals, so denominator gaps and NMSF source
gaps remain visible. Pathway values are covered-subset aggregates, not
full-pathway totals unless the coverage status is complete.

Virginia cutoff and statewide-total fields remain `not_sourced` placeholders in
the analysis panel. The descriptive report documents that gap and the figures
do not annotate cutoff changes until source-backed cutoff values are added.

## Source Discipline

- Do not use the workbook `nsmf 2019` sheet as evidence for NMSF counts.
- Numeric NMSF counts require URL, title, date, and source hash.
- Missing schools in incomplete articles are blank, not zero.
- `verified_zero` is only valid for complete named lists for the geography and year.
- `verified_count` is the status for positive source-backed counts.
- TJHSST stays as a single school row.
- Private-school observations are not allocated to public TJ pathways by school
  location alone; Regulation 3355.16 puts non-public applicants in the
  unallocated-seat pool.
- Grade-11 enrollment denominators normalize NMSF outcomes; they are not
  substitutes for the 8th-grade populations used in admissions-seat allocation.
