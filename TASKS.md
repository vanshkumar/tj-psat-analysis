# TJ PSAT Analysis — Task List

## Goal

Build a reproducible dataset and analysis of National Merit Semifinalist (NMSF) outcomes across the TJHSST geographic area before and after the admissions-policy change.

The first analytical output should be a pathway-by-year view of NMSF counts normalized by junior-class enrollment, with every numeric value traceable to a public source.

Current sequencing note: the Classes 2023-2026 pilot plus the completed
FCPS/TJHSST Classes 2019-2022 historical slice are enough to proceed to the
analytical panel. The remaining historical backfill is optional robustness
work, not a blocker for Milestone 7.

## Non-negotiable data rules

- Do not guess, interpolate, or fabricate NMSF counts.
- Do not convert a missing observation into zero.
- Record `verified_zero` only when a complete source establishes that a school had no semifinalists for that class year.
- Every numeric NMSF count must include source metadata.
- Preserve the original workbook unchanged.
- Treat the workbook's `nsmf 2019` sheet and prior chat-generated figures as untrusted until independently verified.
- Treat TJHSST as one school row; do not assign TJ students back to hypothetical base schools.
- Leave unavailable enrollment values blank with an explicit status or note.
- Preserve school openings, closures, renames, relocations, and program-status distinctions.

## Class-year mapping

| Graduating class | Qualifying PSAT year | Grade 11 enrollment year |
|---:|---:|---:|
| 2019 | Fall 2017 | 2017-18 |
| 2020 | Fall 2018 | 2018-19 |
| 2021 | Fall 2019 | 2019-20 |
| 2022 | Fall 2020 | 2020-21 |
| 2023 | Fall 2021 | 2021-22 |
| 2024 | Fall 2022 | 2022-23 |
| 2025 | Fall 2023 | 2023-24 |
| 2026 | Fall 2024 | 2024-25 |

---

## Milestone 1 — Repository scaffold and workbook ingestion

- [x] Add `AGENTS.md` with the data-integrity rules above.
- [x] Add the source workbook under `data/manual/`.
- [x] Create a Python package and dependency configuration.
- [x] Add formatting, linting, typing, and test commands.
- [x] Add GitHub Actions CI.
- [x] Write a deterministic script that reads the workbook without modifying it.
- [x] Parse the `raw` sheet into a canonical school roster.
- [x] Parse `Sheet6` into a long public-school grade-11 enrollment table.
- [x] Add the class-year mapping table.
- [x] Generate data-quality reports for duplicates, missing fields, and ambiguous school names.
- [x] Confirm that no values from `nsmf 2019` enter processed data.

### Deliverables

- `data/processed/schools.csv`
- `data/processed/public_enrollment.csv`
- `data/processed/class_year_mapping.csv`
- `reports/data_quality/workbook_ingestion.md`
- tests and passing CI

### Definition of done

- One documented command regenerates all outputs from the workbook.
- Original input files remain byte-for-byte unchanged.
- Every processed school has a stable ID.
- Duplicate and ambiguous records fail validation or appear in a review queue.

---

## Milestone 2 — Canonical school roster and aliases

- [x] Validate the full set of public and private schools in scope for Classes 2019-2026.
- [x] Assign each school to its TJ pathway:
  - Arlington
  - Falls Church City
  - Loudoun
  - Prince William
  - FCPS Region 1
  - FCPS Region 2
  - FCPS Region 3
  - FCPS Region 4
  - FCPS Region 5
  - TJHSST
  - Private/homeschool unallocated applicant rows
- [x] Record sector: public, private, homeschool, program, or other.
- [x] Record district/division and NCES identifiers where available.
- [x] Add aliases used in NMSC lists, district releases, and historical enrollment files.
- [x] Resolve the two Freedom High Schools unambiguously.
- [x] Record school-history events, including:
  - Washington-Lee → Washington-Liberty
  - George Mason → Meridian
  - Robert E. Lee → John R. Lewis
  - Stonewall Jackson → Unity Reed
  - Independence opening
  - Lightridge opening
  - Gainesville opening
  - St. Paul VI relocation
- [x] Decide whether Arlington Tech is treated as a separate analytical unit and document the choice.

Status note: `data/processed/school_roster.csv` assigns source-backed analytical
pathway buckets for public schools and TJHSST. Private-school rows are marked
`Private/homeschool unallocated` with
`pathway_status=unallocated_private_applicant` because Regulation 3355.16 places
non-public applicants in the unallocated-seat pool, and school location alone
does not identify the student's residence or admissions pathway.
Regulation 3355.16 does not make the roster's FCPS-region or jurisdiction
buckets observed admissions pathways; annual Notice 3355 materials and actual
admissions data are required for class-specific mechanism claims.
`reports/data_quality/roster_review.md` now has no pathway review rows.

### Deliverables

- `data/processed/school_roster.csv`
- `data/manual/school_aliases.csv`
- `data/manual/school_history.csv`
- `reports/data_quality/roster_review.md`

### Definition of done

- Every observation can join to one and only one canonical school ID.
- Historical aliases resolve deterministically.
- School-years before opening or after closure are represented as `not_operating`, not zero.

---

## Milestone 3 — Complete enrollment denominators

- [x] Validate public-school grade-11 enrollment for 2017-18 through 2023-24 from the workbook export.
- [x] Obtain 2024-25 grade-11 enrollment for Class of 2026.
- [x] Add a reproducible public-school enrollment ingestion path from NCES CCD and/or VDOE.
- [x] Add private-school enrollment ingestion from NCES Private School Survey.
- [x] Use `P290` for grade-11 enrollment in PSS.
- [x] Preserve PSS imputation flags when available.
- [x] Handle secondary schools and combined-grade schools consistently.
- [x] Produce an enrollment coverage report by school and class year.
- [x] Leave unavailable values blank with a machine-readable status.

Status note: `scripts/ingest_public_enrollment_2024_25.py` extracts Class
2026 public-school grade-11 denominators from the NCES CCD 2024-25 school
membership ZIP by NCES school ID and uses the grade-11 total row. H-B Woodlawn
still has `ccd_row_not_found` because the CCD membership file has no matched
grade-11 total row for its directory ID. `scripts/ingest_private_pss.py` reads
available PSS public-use CSV ZIPs, joins private schools by curated `PPIN`
values in `data/manual/private_school_pss_ids.csv`, uses `P290`, and preserves
`F_P290` as `pss_imputation_flag`. Non-survey PSS years, unresolved private
IDs, ambiguous PSS IDs, and blank source values remain blank with explicit
statuses; no adjacent-year values are estimated.

### Deliverables

- `data/processed/enrollment_panel.csv`
- `reports/data_quality/enrollment_coverage.csv`
- `reports/data_quality/enrollment_coverage.md`

### Definition of done

- Each available denominator is sourced and reproducible.
- No enrollment value is estimated from adjacent years.
- Missingness and non-operating years are distinguishable.

---

## Milestone 4 — NMSF source registry and parser framework

- [x] Define a source-manifest schema.
- [x] Store, at minimum:
  - [x] source ID
  - [x] graduating class
  - [x] geography or district covered
  - [x] source title
  - [x] publisher
  - [x] publication date
  - [x] URL
  - [x] retrieval date
  - [x] source type
  - [x] completeness scope
  - [x] local file hash when archived
  - [x] parser name and version
  - [x] notes
- [x] Define observation statuses:
  - [x] `verified_count`
  - [x] `verified_zero`
  - [x] `missing_source`
  - [x] `source_incomplete`
  - [x] `ambiguous_school`
  - [x] `not_operating`
  - [x] `not_applicable`
- [x] Build parser registry/framework entries for structured HTML, PDFs, and manually reviewed source tables.
- [x] Archive permissible source files or snapshots under `data/raw/`.
- [x] Add parser tests using fixed fixtures.
- [x] Add a validation that rejects numeric NMSF counts without source metadata.

Status note: `data/sources/source_manifest.yml` is now schema-validated by
`scripts/build_nmsf_observations.py`. The processed NMSF observation layer
stores source-backed positive counts as `verified_count`, infers
`verified_zero` only for complete manifest-declared source scopes, and leaves
all out-of-scope schools as `missing_source`. Enrollment denominators and rates
are intentionally excluded until Milestone 7 joins observations to
`data/processed/enrollment_panel.csv`. The current official FCPS, APS, LCPS,
and PWCS source entries point to count-only snapshots under `data/raw/nmsf/`;
those snapshots omit student names and are hash-validated through the manifest.

### Deliverables

- `data/sources/source_manifest.yml`
- `src/.../nmsf/` parser modules
- `tests/fixtures/nmsf/`
- `data/processed/nmsf_observations.csv`
- `reports/data_quality/nmsf_source_registry.md`
- source-provenance tests

### Definition of done

- Every numeric count traces to a source and extraction method.
- Re-running a parser produces the same output.
- Incomplete sources cannot silently create zeros.

---

## Milestone 5 — Four-year NMSF pilot

Prioritize Classes 2023-2026 to get an early pre/post view:

- Classes 2023 and 2024: pre-policy cohorts.
- Classes 2025 and 2026: first post-policy cohorts.

Tasks:

- [x] Collect official FCPS/TJHSST releases.
- [x] Collect official LCPS releases where available: school-attributed Classes
  2023, 2024, and 2026, plus the total-only Class 2025 release.
- [x] Collect official APS releases where available: Classes 2023, 2025, and
  2026.
- [x] Collect official PWCS releases.
- [ ] Collect official Falls Church City or Meridian releases.
- [ ] Collect NMSC Virginia lists where district releases are absent or incomplete.
- [ ] Add public-school observations for every rostered school-year.
- [x] Add private-school observations only when verifiable.
- [x] Reconcile school counts against complete district totals where possible.
- [x] Investigate every total mismatch.
- [x] Produce a human-review queue for ambiguous names and source gaps.

Status note: `data/processed/nmsf_observations_2023_2026.csv` and
`reports/data_quality/nmsf_reconciliation_2023_2026.md` now cover the
source-backed pilot rows available from official FCPS/TJHSST Classes 2023-2026,
APS Classes 2023 and 2025-2026, PWCS public high-school Classes 2023-2026,
LCPS public high-school Classes 2023, 2024, and 2026, a total-only official
LCPS Class 2025 release, and local Patch rows for Fairfax City, McLean,
Vienna/Oakton, Arlington, Falls Church, Ashburn/Loudoun, and Woodbridge
schools. APS/LCPS
resident TJHSST subsets, PWCS former-middle-school TJHSST references, Arlington
Tech, and the LCPS Class 2025 unattributed total are retained in count-only
snapshots for reconciliation but excluded from the observation panel to preserve
the single TJHSST row, the roster's Arlington Tech decision, and the
no-school-attribution rule. Overlapping public-school rows in the Patch articles
are retained only in source snapshots when official district rows already
cover those counts. The current pilot slice has 304 observation rows: 189
`verified_count`, 78 `verified_zero`, and 37 `missing_source`. The
reconciliation report's Source Gaps table is the authoritative remaining-gap
summary; `reports/data_quality/manual_review_queue.csv` has 140 rows because it
also includes excluded snapshot rows retained for source-total reconciliation.
After the LCPS Class 2023 bulk backfill, the remaining unresolved rows are
small jurisdiction/private-school clusters rather than a clear bulk source gap.

### Deliverables

- `data/processed/nmsf_observations_2023_2026.csv`
- `reports/data_quality/nmsf_reconciliation_2023_2026.md`
- `reports/data_quality/manual_review_queue.csv`

### Definition of done

- All available counts are source-backed.
- Unavailable counts remain explicitly missing.
- District totals reconcile whenever a complete district source exists.

---

## Milestone 6 — Optional historical NMSF backfill robustness

Do not block the first analytical panel on this milestone. Continue only when a
source has broad payoff or naturally overlaps with later validation work.

- [x] Backfill official FCPS/TJHSST Classes 2019-2022.
- [x] Search the Internet Archive for removed FCPS release pages.
- [ ] Optionally search other district archives and the Internet Archive for removed releases.
- [ ] Optionally use NMSC Virginia lists where accessible.
- [ ] Add school press releases and reputable local reporting only when the source identifies the relevant class and school clearly.
- [ ] Avoid forums, unattributed spreadsheets, and inferred counts as final sources.
- [ ] Record source coverage separately from data values.
- [ ] Reconcile totals by district and year where possible.

Status note: Stop here for the pre-analysis Task 6 slice. The first historical
slice backfills official FCPS/TJHSST
Classes 2019-2022 using archived FCPS release pages discovered through the
Internet Archive `/news/` CDX index. Count-only snapshots live under
`data/raw/nmsf/fcps/`, the school-level transcriptions are in
`data/sources/nmsf_counts.csv`, and complete FCPS scope produces source-backed
zeros for absent rostered FCPS public schools in those class years. Class 2022
is documented with a source discrepancy: the FCPS article text says 214
semifinalists, but the visible school-grouped list sums to 215, so the manifest
uses the visible named-list total and notes the mismatch. Non-FCPS historical
districts and private-school rows remain optional future robustness work;
missing rows should not be converted to zero, and Milestone 7 should proceed
using explicit observation statuses and compatible coverage.

### Deliverables

- `data/processed/nmsf_observations.csv`
- `reports/data_quality/nmsf_coverage.csv`
- `reports/data_quality/nmsf_reconciliation.md`

### Definition of done

- If pursued to completion, the panel covers Classes 2019-2026 with explicit status for every school-year.
- No guessed number appears in the final dataset.

---

## Milestone 7 — Build the analytical panel

- [x] Join the canonical roster, NMSF observations, enrollment, source metadata, and class-year mapping.
- [x] Calculate `nmsf_per_100_juniors` where both inputs are available.
- [x] Calculate pathway-level totals using only compatible coverage.
- [x] Keep raw counts, rates, and missingness indicators together.
- [x] Add the Virginia NMSF Selection Index cutoff by class year, or a documented placeholder when not reliably sourced.
- [x] Add statewide semifinalist totals when reliably sourced, or a documented placeholder when not reliably sourced.
- [x] Flag rows affected by school openings, renames, or denominator gaps.
- [x] Flag pathway buckets as analytical geographies rather than observed
  TJHSST admissions pathways unless actual pathway/offers data are sourced.
- [x] Keep grade-11 enrollment denominators separate from admissions-seat
  allocation inputs; use sourced 8th-grade populations only if an admissions
  allocation analysis is added.
- [x] Write a data dictionary.

Status note: `scripts/build_analysis_panel.py` now generates
`data/processed/analysis_panel.csv` and
`reports/data_quality/final_panel_checks.md` from the roster, NMSF observation
layer, enrollment panel, class-year mapping, and school-history file. Row-level
rates are calculated only when both `nmsf_count` and `grade11_enrollment` are
available. Pathway aggregate fields are covered-subset totals that sum only
compatible school rows and carry coverage-status columns, so partial source or
denominator coverage is visible next to the aggregate. Virginia NMSF Selection
Index cutoff and statewide semifinalist total columns are present as
`not_sourced` placeholders; no values are guessed. Pathway buckets are labeled
as analytical geographies or non-public unallocated applicant buckets, not
observed TJHSST admissions pathway outcomes. The panel also keeps
`denominator_type=grade11_enrollment_outcome_denominator` separate from
admissions-seat allocation inputs, which remain absent pending sourced
8th-grade allocation-population data.

### Deliverables

- `data/processed/analysis_panel.csv`
- `docs/data_dictionary.md`
- `reports/data_quality/final_panel_checks.md`

### Definition of done

- Every derived value can be regenerated from source-backed inputs.
- The panel passes uniqueness, range, referential-integrity, and provenance tests.

---

## Milestone 8 — Descriptive analysis and visualizations

- [x] Plot raw NMSF counts by school and year.
- [x] Plot NMSF per 100 juniors by school and year.
- [x] Create the pathway-by-class heatmap.
- [x] Plot TJHSST separately from base public schools and private schools.
- [x] Show total TJ-zone counts with and without TJHSST.
- [x] Show public-versus-private totals.
- [x] Show pre/post summaries for Classes 2023-24 versus 2025-26.
- [x] Add uncertainty or small-number warnings where appropriate.
- [x] Display data-coverage and missingness alongside substantive charts.
- [x] Document Virginia cutoff placeholders and do not annotate unsourced cutoff changes.

Status note: `scripts/build_descriptive_outputs.py` now generates dependency-light
SVG figures, CSV summary tables, and `reports/descriptive_results.md` from
`data/processed/analysis_panel.csv`. Count totals include only source-backed
numeric NMSF rows; missing rows remain visible and are not converted to zero.
Rate summaries use only rows with both NMSF counts and grade-11 denominators.
Pathway heatmap values are covered-subset aggregates and carry coverage-status
labels. The Virginia cutoff and statewide total fields remain `not_sourced`, so
the descriptive figures do not annotate cutoff changes.

### Deliverables

- `reports/figures/`
- `reports/tables/`
- `reports/descriptive_results.md`

### Definition of done

- Every chart is generated by code.
- Every chart states its denominator, coverage, and treatment of missing data.
- Raw and normalized views are both available.

---

## Milestone 9 — Robustness and interpretation

- [ ] Compare results using raw counts versus enrollment-normalized rates.
- [ ] Compare TJ-zone totals including and excluding TJHSST.
- [ ] Test sensitivity to private-school missingness.
- [ ] Test sensitivity to excluding programs that are not conventional base high schools.
- [ ] Examine whether Class of 2025 is an isolated discontinuity or part of a broader trend.
- [ ] Compare Classes 2025 and 2026 carefully because the Virginia cutoff changed.
- [ ] Document COVID-era cohort timing and other plausible confounds.
- [ ] Use Regulation 3355.16, annual Notice 3355 materials, and historical
  regulation versions, not proposal-stage materials, when interpreting the
  TJHSST admissions mechanism.
- [ ] Avoid applying Regulation 3355.16 retroactively to earlier cohorts unless
  the relevant historical regulation or notice supports the same rule.
- [ ] Avoid causal claims unsupported by the design.
- [ ] Separate findings about the extreme right tail from claims about median academic outcomes or school culture.

### Deliverables

- `reports/robustness.md`
- `reports/limitations.md`
- `reports/initial_findings.md`

### Definition of done

- Claims are proportional to the evidence.
- Alternative explanations and missing-data limitations are explicit.
- The report distinguishes description, inference, and speculation.

---

## Milestone 10 — Optional follow-on data

Do not block the NMSF analysis on these tasks.

- [ ] Draft public-records requests for school-level PSAT participation and score distributions.
- [x] Archive Regulation 3355.16 as the TJHSST admissions-policy source.
- [ ] Archive annual Notice 3355 admissions procedures and relevant historical
  Regulation 3355 versions for application years feeding Classes 2019-2026.
- [ ] Request actual TJ applicant, eligible-applicant, offer, waitpool,
  acceptance, enrolled-student, and later-grade placement counts by public
  school/division, allocated/unallocated seat pool, and class year where
  available.
- [ ] Request the 8th-grade population inputs used to allocate seats by public
  school or cooperating division for relevant admission cycles.
- [ ] Investigate SAT upper-tail measures by school.
- [ ] Investigate AP/IB participation and score distributions.
- [ ] Investigate advanced-course enrollment and completion.
- [ ] Investigate competition outcomes such as AIME, USACO, and major science competitions.
- [ ] Identify plausible comparison regions or selective-school policy changes for a later causal design.

---

## Recommended pull-request sequence

1. **PR 1:** Scaffold, workbook ingestion, tests, and CI.
2. **PR 2:** Canonical roster, aliases, and school history.
3. **PR 3:** Complete public and private enrollment denominators.
4. **PR 4:** Source manifest and NMSF parser framework.
5. **PR 5:** Classes 2023-2026 NMSF pilot.
6. **PR 6:** Optional Classes 2019-2022 historical backfill robustness; the
   current pre-analysis stopping point is official FCPS/TJHSST 2019-2022.
7. **PR 7:** Analytical panel and validation suite.
8. **PR 8:** Charts, descriptive report, and robustness checks.

## Project completion criteria

The project is complete when:

- [ ] The school roster is validated for all relevant years.
- [ ] Every school-year has an explicit NMSF status.
- [ ] Every numeric NMSF count has source provenance.
- [ ] Junior enrollment is available or explicitly missing for every school-year.
- [x] The analysis panel is reproducible from committed inputs and source manifests.
- [ ] CI checks formatting, tests, schemas, and provenance rules.
- [ ] The pathway heatmap and core trend charts are generated automatically.
- [ ] The final report clearly states what the data do and do not support.
