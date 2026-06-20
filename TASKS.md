# TJ PSAT Analysis — Task List

## Goal

Build a reproducible dataset and analysis of National Merit Semifinalist (NMSF) outcomes across the TJHSST geographic area before and after the admissions-policy change.

The first analytical output should be a pathway-by-year view of NMSF counts normalized by junior-class enrollment, with every numeric value traceable to a public source.

Current status and sequencing note:

- Milestones 1-4, 7, 8, and 9 are complete.
- Milestone 5 is complete to the documented analysis-ready stopping point; its
  remaining school-year source gaps are preserved as missing and carried into
  the targeted public-data cleanup in Milestone 10.
- Milestone 6 remains numbered for continuity but is an optional, deferred
  historical-backfill branch. The active core sequence skips from Milestone 5
  to Milestone 7.
- Milestone 10 is the next recommended work: a narrow, public-source cleanup
  focused on complete Virginia lists, the remaining focal-period school rows,
  a small denominator backfill, and a rerun of the completed analysis.
- Milestone 11 contains optional external-records and broader-outcome work and
  does not block the NMSF analysis.

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

## Milestone 5 — Four-year NMSF pilot — analysis-ready stopping point

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

Accepted stopping point: the pilot is sufficient for the analytical panel and
Task 9, but it is not coverage-complete. The 37 remaining focal-period
`missing_source` rows consist of 8 public-school rows and 29 private-school
rows. The public gaps are Meridian (Classes 2023, 2025, and 2026), Wakefield
(Class 2024), and Loudoun Valley, Park View, Tuscarora, and Woodgrove (Class
2025). Do not infer zeros. The broad-source work most likely to resolve these
rows has been consolidated in Milestone 10 rather than continuing open-ended
school-by-school searching here.

### Deliverables

- `data/processed/nmsf_observations_2023_2026.csv`
- `reports/data_quality/nmsf_reconciliation_2023_2026.md`
- `reports/data_quality/manual_review_queue.csv`

### Definition of done

- All available counts are source-backed.
- Unavailable counts remain explicitly missing.
- District totals reconcile whenever a complete district source exists.

---

## Milestone 6 — Optional and deferred historical NMSF backfill

This milestone is outside the active critical path. The completed FCPS/TJHSST
Classes 2019-2022 slice is retained, but no additional school-by-school
historical search is required for the core project. Continue only when a source
has broad payoff or naturally overlaps with Milestone 10 validation work.

- [x] Backfill official FCPS/TJHSST Classes 2019-2022.
- [x] Search the Internet Archive for removed FCPS release pages.
- [ ] As the highest-value optional extension, obtain a complete Virginia Class
  2022 state-by-school list; add Class 2021 only if it is readily available from
  the same source or archive.
- [ ] Treat Classes 2019-2020 and other district-by-district historical work as
  opportunistic only; do not resume broad school-by-school scraping.
- [ ] Optionally search other district archives and the Internet Archive for
  removed releases when a broad source cannot be found.
- [ ] Add school press releases and reputable local reporting only when the
  source identifies the relevant class and school clearly.
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
missing rows should not be converted to zero. Milestones 7-9 have already
proceeded using explicit observation statuses and compatible coverage. A
complete Virginia Class 2022 or Class 2021 list may still be added under this
optional milestone if it is found through the same broad-source workflow used
for Classes 2023-2026, but broad 2019-2020 backfill remains deferred.

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

## Milestone 9 — Robustness and interpretation — complete

- [x] Compare results using raw counts versus enrollment-normalized rates.
- [x] Compare TJ-zone totals including and excluding TJHSST.
- [x] Test sensitivity to private-school missingness.
- [x] Test sensitivity to excluding programs that are not conventional base high schools.
- [x] Examine Class of 2025 as a distinct discontinuity and compare it with the broader available trend.
- [x] Analyze Classes 2025 and 2026 separately rather than treating them as one uniform post-policy period.
- [x] Treat Virginia cutoff and statewide-total information as supplemental when it is not source-backed in the canonical panel.
- [x] Document COVID-era cohort timing, the digital-PSAT transition, and other plausible confounds.
- [x] Use adopted regulation versions, class-specific official bulletins, and Board materials rather than proposal-stage descriptions when interpreting the TJHSST admissions mechanism.
- [x] Search for annual Notice 3355 materials; document that they were not recovered and do not infer unrecovered procedural details.
- [x] Avoid applying Regulation 3355.16 retroactively when the relevant historical regulation does not support the same rule.
- [x] Avoid causal claims unsupported by the design.
- [x] Separate findings about the extreme right tail from claims about median academic outcomes or school culture.

Status note: completed on 2026-06-19. `scripts/build_task9_outputs.py`
rebuilds the Task 9 reports from `data/processed/analysis_panel.csv`, and the
independent validation assertions passed. The canonical panel remains 608 rows
covering 76 schools and Classes 2019-2026.

Headline descriptive results:

- TJHSST pooled NMSF rate fell from 32.927 per 100 juniors in Classes 2023-2024
  to 18.890 in Classes 2025-2026 (-42.6%).
- The balanced 50-school conventional public-base panel rose from 0.596 to
  0.696 per 100 juniors (+16.7%).
- The balanced 51-school public panel including TJHSST fell from 1.138 to
  1.029 (-9.6%).
- Class 2025 is the sharp break. Class 2026 shows a partial TJHSST rebound and
  a heterogeneous base-school increase.
- The public-school evidence is robust to the documented coverage limitations;
  the private-school offset and therefore the complete whole-region net change
  remain unresolved.

Policy-source boundary: Regulations 3355.14, 3355.15, and 3355.16, official
class-specific FCPS materials, Board minutes, NMSC materials, College Board
documentation, and FCPS COVID-era records were reviewed. The annual Notice 3355
documents themselves were not recovered. The reports state that limitation and
do not fill the gap from memory or proposal-stage materials.

### Deliverables

- `scripts/build_task9_outputs.py`
- `reports/robustness.md`
- `reports/limitations.md`
- `reports/initial_findings.md`
- `reports/tables/task9_*.csv`
- `TASK9_COMPLETION.md`

### Definition of done

- Claims are proportional to the evidence.
- Alternative explanations and missing-data limitations are explicit.
- The report distinguishes description, inference, and speculation.
- Every numerical Task 9 claim is reproducible from the canonical panel or is clearly labeled as supplemental context.

---

## Milestone 10 — Targeted public-data completion and Task 9 refresh

This is the next recommended work. It is intentionally narrow, uses publicly
obtainable data only, and does not require records requests. The current TJHSST
and base-public conclusions are already sufficiently robust for descriptive
reporting. This milestone is mainly intended to resolve the whole-region and
private-school interpretation, strengthen statewide normalization, and close a
few inexpensive denominator gaps.

### Priority A — Complete focal-period Virginia lists

- [ ] Locate complete Virginia NMSF school-by-school lists for Classes 2023, 2024, 2025, and 2026 from public sources, prioritizing NMSC/media materials or complete authoritative mirrors.
- [ ] Archive permissible originals or create count-only snapshots that omit student names; record source scope, retrieval date, hash, and parser/transcription method in the source manifest.
- [ ] Build a deterministic parser or reviewed transcription workflow for the
  Virginia-list format, with fixed fixtures and reconciliation tests.
- [ ] Parse every in-scope TJ-zone public, private, and program entry from each complete list using the canonical roster and alias table; retain homeschool entries separately when their geography is identifiable.
- [ ] Create `verified_zero` only when the complete list's scope establishes that the school had no semifinalists; otherwise retain `missing_source`.
- [ ] Resolve the 37 focal-period missing rows where the list scope permits, including the 8 public-school rows and 29 private-school rows.
- [ ] Reconcile parsed list counts against existing district, school, and local-news sources; investigate every mismatch and do not silently overwrite a higher-quality source.
- [ ] Keep private-school and homeschool totals labeled as location-based or otherwise scope-limited; do not treat school location as proof of TJ eligibility, residence, or displacement from TJHSST.
- [ ] Add source-backed Virginia statewide semifinalist totals when the complete lists support them.
- [ ] Compute and publish, by class year:
  - TJ-zone NMSFs as a share of Virginia NMSFs
  - TJHSST NMSFs as a share of Virginia NMSFs
  - conventional base-public NMSFs as a share of Virginia NMSFs
  - private/homeschool TJ-zone NMSFs as a share of Virginia NMSFs
  - TJ-zone excluding TJHSST as a share of Virginia NMSFs
  - the remainder of Virginia outside the TJ zone

Status note: The official NMSC `23_meritsemi.pdf`, `24_meritsemi.pdf`,
`25_meritsemi.pdf`, and `26_meritsemi.pdf` files were located through the
Internet Archive and archived under `data/raw/nmsf/virginia/`. Visual PDF
inspection confirmed that these are annual press releases, not the
school-by-school lists distributed to news media. They explicitly do not post
the named Semifinalist list on the NMSC website, so this pass adds no
school-level NMSF counts, no `verified_zero` rows, and no Virginia-share series.
The current source-discovery decision and remaining 37 focal-period missing
rows are documented in `reports/data_quality/focal_period_completion.md`.
A follow-up broad-source sweep checked NMSC archive indexes, class-year web
searches, Common Crawl URL indexes, and major Virginia/DC media CDX patterns;
it did not locate a complete public Virginia school-by-school mirror. This
adds search-limitation evidence only: no counts, zeros, or Virginia-share
metrics are created from the sweep.

### Priority B — Minimal denominator cleanup

- [ ] Ingest the NCES PSS 2023-24 public-use file for rostered private schools when available, using `P290` for grade-11 enrollment and preserving `F_P290` imputation flags.
- [ ] Use the 2023-24 PSS data only for the corresponding Class 2025 denominator; do not interpolate Classes 2024 or 2026.
- [x] Fill Classes 2023-2025 grade-11 enrollment for Freedom High School (South Riding) and Freedom High School (Woodbridge) from NCES CCD and/or VDOE using their exact school identifiers.
- [x] Regenerate enrollment-coverage reports and verify that the two Freedom schools join to the intended canonical IDs.

Status note: `scripts/ingest_public_enrollment_nces_supplement.py` now
extracts the two Freedom High School rows for Classes 2023-2025 from official
NCES CCD school membership ZIPs using exact NCES IDs. The generated supplement
is `data/interim/public_grade11_enrollment_nces_supplement.csv`; the enrollment
panel prefers those rows over the ambiguous workbook seed rows. On 2026-06-20,
`scripts/ingest_private_pss_locator_2023_24.py` added an official interim NCES
Private School Search locator supplement for Class 2025 private denominators.
It archived 16 locator detail/search pages under
`data/raw/enrollment/pss_locator_2023_24/` and generated
`data/interim/private_grade11_enrollment_pss_locator_2023_24.csv`: 10 private
rows have source-backed grade-11 denominators, five current locator searches
returned no row, and Loudoun School for Advanced Studies remains ambiguous
because the locator returns two same-address candidates. The official public-use
PSS 2023-24 ZIP is still preferred when NCES posts it because the locator does
not expose `F_P290` imputation flags.

### Rebuild and reassess

- [ ] Rebuild the source manifest, NMSF observation tables, enrollment panel, analytical panel, data-quality reports, descriptive outputs, and Task 9 reports.
- [ ] Recompute balanced panels and missingness sensitivity checks after the new rows are incorporated.
- [ ] Add the Virginia-share series to the descriptive tables and Task 9 interpretation.
- [ ] Add a focal-period completion report comparing old and new counts,
  coverage, balanced panels, statewide shares, and private-school sensitivity.
- [ ] State explicitly whether complete private-school counts and the Class 2025 private denominator materially alter the present conclusion.
- [ ] Update `TASK9_COMPLETION.md` and record a final stopping decision: after
  this broad-source pass, do not continue low-yield school-by-school scraping
  unless a new source can resolve multiple rows at once.

Explicitly out of scope for this pass:

- Public-records requests or direct requests to districts, NMSC, College Board, or schools.
- Estimating missing counts or treating absent names in an incomplete source as zero.
- A stand-alone effort to reconstruct every historical Virginia cutoff.
- Extensive work on the H-B Woodlawn denominator.
- School-by-school private enrollment searches for Classes 2024 and 2026.
- Broad Classes 2019-2020 backfill before a complete-list source is found.

### Deliverables

- updated `data/sources/source_manifest.yml`
- updated `data/sources/nmsf_counts.csv`
- updated count-only source snapshots under `data/raw/nmsf/virginia/`
- updated `data/processed/nmsf_observations_2023_2026.csv`
- updated `data/processed/enrollment_panel.csv`
- updated `data/processed/analysis_panel.csv`
- updated reconciliation and coverage reports under `reports/data_quality/`
- `reports/data_quality/focal_period_completion.md`
- `reports/tables/virginia_share_by_class.csv`
- refreshed `reports/descriptive_results.md`
- refreshed `reports/robustness.md`
- refreshed `reports/limitations.md`
- refreshed `reports/initial_findings.md`
- refreshed `TASK9_COMPLETION.md`

### Definition of done

- Each focal-period missing row is either resolved from a complete public list or remains explicitly missing with the list/search limitation documented.
- State-share metrics are reproducible and have source provenance.
- Private-school conclusions reflect complete count coverage where achieved and use denominators only where directly observed.
- The refreshed reports state whether any substantive conclusion changed.
- No external records request is required to close this milestone.

---

## Milestone 11 — Optional external and broader follow-on data

Do not block the NMSF analysis or Milestone 10 on these tasks. Begin only after
the targeted public-data cleanup is complete and only if a broader causal or
school-culture study is desired.

- [ ] Draft public-records requests for school-level PSAT participation and score distributions.
- [x] Archive Regulation 3355.16 as the TJHSST admissions-policy source.
- [x] Review Regulations 3355.14 and 3355.15 and class-specific official materials for the completed Task 9 interpretation.
- [ ] Archive annual Notice 3355 admissions procedures and relevant historical Regulation 3355 versions for application years feeding Classes 2019-2026.
- [ ] Request actual TJ applicant, eligible-applicant, offer, waitpool, acceptance, enrolled-student, and later-grade placement counts by public school/division, allocated/unallocated seat pool, and class year where available.
- [ ] Request the 8th-grade population inputs used to allocate seats by public school or cooperating division for relevant admission cycles.
- [ ] Investigate SAT upper-tail measures by school.
- [ ] Investigate AP/IB participation and score distributions.
- [ ] Investigate advanced-course enrollment and completion.
- [ ] Investigate competition outcomes such as AIME, USACO, and major science competitions.
- [ ] Identify plausible comparison regions or selective-school policy changes for a later causal design.

Status note: the annual Notice 3355 documents were not recovered during Task 9.
That gap is documented and does not invalidate the descriptive NMSF analysis;
it matters only for finer-grained claims about the exact class-specific
admissions mechanism.

---

## Recommended pull-request sequence

1. **PR 1:** Scaffold, workbook ingestion, tests, and CI.
2. **PR 2:** Canonical roster, aliases, and school history.
3. **PR 3:** Public and available private enrollment denominators.
4. **PR 4:** Source manifest and NMSF parser framework.
5. **PR 5:** Classes 2023-2026 NMSF pilot to the documented analysis-ready stopping point.
6. **Optional/deferred PR 6:** Historical backfill beyond the completed official FCPS/TJHSST Classes 2019-2022 slice; this is not on the critical path.
7. **PR 7:** Analytical panel and validation suite.
8. **PR 8:** Charts, descriptive results, and completed robustness/interpretation reports.
9. **Next PR — Milestone 10:** Complete focal-period Virginia lists, perform the minimal denominator cleanup, add Virginia-share measures, and rerun Milestones 7-9.
10. **Optional later PR — Milestone 11:** External-records requests and broader outcomes for a later causal or culture-focused design.

## Core project completion criteria

The core descriptive NMSF project is complete at the current documented
coverage level when:

- [x] The school roster is validated for all relevant years.
- [x] Every school-year has an explicit NMSF status, including `missing_source`, `not_operating`, and other nonnumeric statuses.
- [x] Every numeric NMSF count has source provenance.
- [x] Junior enrollment is available or explicitly missing for every school-year.
- [x] The analysis panel is reproducible from committed inputs and source manifests.
- [x] CI checks formatting, tests, schemas, and provenance rules.
- [x] The pathway heatmap and core trend charts are generated automatically.
- [x] The Task 9 reports clearly state what the data do and do not support.

## Recommended public-data completion criteria

Milestone 10 is complete when:

- [ ] Complete public Virginia-list sources for Classes 2023-2026 have been parsed where obtainable, with unresolved gaps documented rather than guessed.
- [ ] The Class 2025 private-school denominator update and the two Freedom High School denominator histories have been attempted reproducibly.
- [ ] Virginia-share measures are added with source provenance.
- [ ] The analytical panel, descriptive outputs, and Task 9 reports are rebuilt.
- [ ] The project records whether the private-school and whole-region conclusions changed.

Milestones 6 and 11 are optional and are not required for completion of the
current descriptive regional-NMSF analysis.
