# TJ PSAT Analysis — Task List

## Goal

Build a reproducible dataset and analysis of National Merit Semifinalist (NMSF) outcomes across the TJHSST geographic area before and after the admissions-policy change.

The first analytical output should be a pathway-by-year view of NMSF counts normalized by junior-class enrollment, with every numeric value traceable to a public source.

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

- [ ] Validate the full set of public and private schools in scope for Classes 2019-2026.
- [ ] Assign each school to its TJ pathway:
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
- [ ] Record sector: public, private, homeschool, program, or other.
- [ ] Record district/division and NCES identifiers where available.
- [ ] Add aliases used in NMSC lists, district releases, and historical enrollment files.
- [ ] Resolve the two Freedom High Schools unambiguously.
- [ ] Record school-history events, including:
  - Washington-Lee → Washington-Liberty
  - George Mason → Meridian
  - Robert E. Lee → John R. Lewis
  - Stonewall Jackson → Unity Reed
  - Independence opening
  - Lightridge opening
  - Gainesville opening
  - St. Paul VI relocation
- [ ] Decide whether Arlington Tech is treated as a separate analytical unit and document the choice.

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

- [ ] Validate public-school grade-11 enrollment for 2017-18 through 2023-24 from the workbook export.
- [ ] Obtain 2024-25 grade-11 enrollment for Class of 2026.
- [ ] Add a reproducible public-school enrollment ingestion path from NCES CCD and/or VDOE.
- [ ] Add private-school enrollment ingestion from NCES Private School Survey.
- [ ] Use `P290` for grade-11 enrollment in PSS.
- [ ] Preserve PSS imputation flags when available.
- [ ] Handle secondary schools and combined-grade schools consistently.
- [ ] Produce an enrollment coverage report by school and class year.
- [ ] Leave unavailable values blank with a machine-readable status.

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

- [ ] Define a source-manifest schema.
- [ ] Store, at minimum:
  - source ID
  - graduating class
  - geography or district covered
  - source title
  - publisher
  - publication date
  - URL
  - retrieval date
  - source type
  - completeness scope
  - local file hash when archived
  - parser name and version
  - notes
- [ ] Define observation statuses:
  - `verified_count`
  - `verified_zero`
  - `missing_source`
  - `source_incomplete`
  - `ambiguous_school`
  - `not_operating`
  - `not_applicable`
- [ ] Build parsers for structured HTML, PDFs, and manually reviewed source tables.
- [ ] Archive permissible source files or snapshots under `data/raw/`.
- [ ] Add parser tests using fixed fixtures.
- [ ] Add a validation that rejects numeric NMSF counts without source metadata.

### Deliverables

- `data/sources/source_manifest.yml`
- `src/.../nmsf/` parser modules
- `tests/fixtures/nmsf/`
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

- [ ] Collect official FCPS/TJHSST releases.
- [ ] Collect official LCPS releases.
- [ ] Collect official APS releases.
- [ ] Collect official PWCS releases.
- [ ] Collect official Falls Church City or Meridian releases.
- [ ] Collect NMSC Virginia lists where district releases are absent or incomplete.
- [ ] Add public-school observations for every rostered school-year.
- [ ] Add private-school observations only when verifiable.
- [ ] Reconcile school counts against complete district totals where possible.
- [ ] Investigate every total mismatch.
- [ ] Produce a human-review queue for ambiguous names and source gaps.

### Deliverables

- `data/processed/nmsf_observations_2023_2026.csv`
- `reports/data_quality/nmsf_reconciliation_2023_2026.md`
- `reports/data_quality/manual_review_queue.csv`

### Definition of done

- All available counts are source-backed.
- Unavailable counts remain explicitly missing.
- District totals reconcile whenever a complete district source exists.

---

## Milestone 6 — Historical NMSF backfill

- [ ] Backfill Classes 2019-2022.
- [ ] Search district archives and the Internet Archive for removed releases.
- [ ] Use NMSC Virginia lists where accessible.
- [ ] Add school press releases and reputable local reporting only when the source identifies the relevant class and school clearly.
- [ ] Avoid forums, unattributed spreadsheets, and inferred counts as final sources.
- [ ] Record source coverage separately from data values.
- [ ] Reconcile totals by district and year where possible.

### Deliverables

- `data/processed/nmsf_observations.csv`
- `reports/data_quality/nmsf_coverage.csv`
- `reports/data_quality/nmsf_reconciliation.md`

### Definition of done

- The panel covers Classes 2019-2026 with explicit status for every school-year.
- No guessed number appears in the final dataset.

---

## Milestone 7 — Build the analytical panel

- [ ] Join the canonical roster, NMSF observations, enrollment, source metadata, and class-year mapping.
- [ ] Calculate `nmsf_per_100_juniors` where both inputs are available.
- [ ] Calculate pathway-level totals using only compatible coverage.
- [ ] Keep raw counts, rates, and missingness indicators together.
- [ ] Add the Virginia NMSF Selection Index cutoff by class year.
- [ ] Add statewide semifinalist totals when reliably sourced.
- [ ] Flag rows affected by school openings, renames, or denominator gaps.
- [ ] Write a data dictionary.

### Deliverables

- `data/processed/analysis_panel.csv`
- `docs/data_dictionary.md`
- `reports/data_quality/final_panel_checks.md`

### Definition of done

- Every derived value can be regenerated from source-backed inputs.
- The panel passes uniqueness, range, referential-integrity, and provenance tests.

---

## Milestone 8 — Descriptive analysis and visualizations

- [ ] Plot raw NMSF counts by school and year.
- [ ] Plot NMSF per 100 juniors by school and year.
- [ ] Create the pathway-by-class heatmap.
- [ ] Plot TJHSST separately from base public schools and private schools.
- [ ] Show total TJ-zone counts with and without TJHSST.
- [ ] Show public-versus-private totals.
- [ ] Show pre/post summaries for Classes 2023-24 versus 2025-26.
- [ ] Add uncertainty or small-number warnings where appropriate.
- [ ] Display data-coverage and missingness alongside substantive charts.
- [ ] Annotate Virginia cutoff changes, especially Class of 2026.

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
- [ ] Request actual TJ enrollment or offers by later pathway for relevant cohorts.
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
6. **PR 6:** Classes 2019-2022 historical backfill.
7. **PR 7:** Analytical panel and validation suite.
8. **PR 8:** Charts, descriptive report, and robustness checks.

## Project completion criteria

The project is complete when:

- [ ] The school roster is validated for all relevant years.
- [ ] Every school-year has an explicit NMSF status.
- [ ] Every numeric NMSF count has source provenance.
- [ ] Junior enrollment is available or explicitly missing for every school-year.
- [ ] The analysis panel is reproducible from committed inputs and source manifests.
- [ ] CI checks formatting, tests, schemas, and provenance rules.
- [ ] The pathway heatmap and core trend charts are generated automatically.
- [ ] The final report clearly states what the data do and do not support.
