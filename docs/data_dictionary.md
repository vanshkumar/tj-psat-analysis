# Data Dictionary

## Data Products and Reports

- `data/interim/canonical_schools.csv`: canonical roster from the workbook `raw` sheet.
- `data/interim/public_enrollment_raw.csv`: long-form transcription of public enrollment rows from `Sheet6`.
- `data/interim/public_grade11_enrollment.csv`: canonical public-school grade 11 enrollment by class year.
- `data/interim/public_grade11_enrollment_2024_25.csv`: Class 2026 public-school grade 11 enrollment extracted from the NCES CCD 2024-25 school membership file by NCES school ID.
- `data/interim/private_grade11_enrollment.csv`: private-school PSS survey-year grade 11 enrollment extract using `P290`, with `F_P290` preserved as `pss_imputation_flag`.
- `data/interim/private_grade11_enrollment_pss_locator_2023_24.csv`: interim Class 2025 private-school denominator supplement parsed from archived NCES Private School Search 2023-24 locator pages using `PSS_ENROLL_11`; unresolved locator searches remain blank.
- `data/sources/targeted_grade11_enrollment.csv`: exact mapped-year Grade 11 supplements with source metadata and hashes. It supplies H-B Woodlawn for Classes 2023-2026 (109, 109, 115, and 110), Loudoun School for Advanced Studies for Class 2023 (11), and BASIS Independent McLean for Classes 2025-2026 (29 and 40).
- `data/interim/panel_seed.csv`: school-by-class-year panel with blank NMSF counts and source-pending statuses.
- `data/interim/panel_nmsf.csv`: legacy interim seed panel plus source-backed NMSF count transcriptions from `data/sources/nmsf_counts.csv`; it is not the final analytical panel because it is seed-based and does not include all processed denominator updates.
- `data/processed/analysis_panel.csv`: analytical panel joining the canonical roster, class-year mapping, NMSF observations, enrollment denominators, school-history flags, row-level rates, and covered-subset pathway aggregates.
- `data/processed/nmsf_observations.csv`: NMSF observation layer with one row per school/class year, source-backed positive counts, source-backed complete-list zeros, explicit missingness, and no enrollment denominators or rates.
- `data/processed/nmsf_observations_2023_2026.csv`: focal-period slice filtered from `data/processed/nmsf_observations.csv` for Classes 2023-2026.
- `data/processed/school_roster.csv`: roster with canonical school IDs, pathway status, pathway assignment method, pathway source metadata, sector, district, NCES IDs where source-backed, and operating-year boundaries.
- `data/processed/enrollment_panel.csv`: school-by-class-year grade-11 enrollment denominator panel for public and private schools, with source metadata and explicit missingness statuses.
- `data/manual/school_aliases.csv`: deterministic alias table. Rows with `join_allowed=false` are known ambiguous aliases and must not be used for automatic observation joins.
- `data/manual/school_history.csv`: source-noted rename, opening, and relocation events used to keep historical names and not-operating years explicit.
- `data/manual/public_school_nces_ids.csv`: source-backed public-school NCES IDs matched from the NCES CCD 2023-24 directory by division and normalized alias.
- `data/manual/private_school_pss_ids.csv`: curated private-school PSS `PPIN` match table used to prevent name-only private-school joins.
- `data/manual/private_school_pss_locator_2023_24.csv`: curated NCES Private School Search locator detail/search URLs for Class 2025 private-school denominator extraction.
- `reports/data_quality/roster_review.md`: roster coverage, alias conflicts, history review, admissions-pathway source summary, and pathway review status.
- `reports/data_quality/enrollment_coverage.csv`: one coverage row for each school and class year in `data/processed/enrollment_panel.csv`.
- `reports/data_quality/enrollment_coverage.md`: denominator coverage summary, source list, and no-estimation rules.
- `reports/data_quality/nmsf_source_registry.md`: source-registry summary for NMSF observations, including status counts, source counts, and zero-inference rules.
- `reports/data_quality/nmsf_reconciliation_2023_2026.md`: focal-period reconciliation summary, including source reported totals, in-panel totals, excluded count-only snapshot totals, and remaining source gaps.
- `reports/data_quality/manual_review_queue.csv`: review queue for missing school-year sources plus source rows excluded from the panel, such as jurisdictional TJHSST subsets and non-roster schools. Use the reconciliation report's Source Gaps table, not the raw queue length, for the true unresolved-observation count.
- `reports/data_quality/final_panel_checks.md`: validation summary for the analytical panel, including uniqueness, source-provenance, rate-null, pathway-flag, and placeholder checks.
- `reports/descriptive_results.md`: descriptive report generated from `analysis_panel.csv`, with figure/table inventory, source-status summaries, TJ-zone count summaries, pre/post summaries, small-number warnings, and the unsourced Virginia-cutoff placeholder note.
- `reports/tables/school_counts_by_year.csv`: school-by-class raw NMSF counts, count statuses, source metadata, and count-missingness notes.
- `reports/tables/school_rates_by_year.csv`: school-by-class NMSF per 100 juniors, grade-11 denominators, rate statuses, and missingness notes.
- `reports/tables/pathway_by_class_heatmap.csv`: source table for the pathway heatmap; all values are covered-subset aggregates with pathway coverage-status fields.
- `reports/tables/school_group_totals_by_class.csv`: class-year totals for TJHSST, base public schools, and private schools, keeping observed NMSF totals separate from rate-compatible count/enrollment totals.
- `reports/tables/tj_zone_counts_by_class.csv`: observed source-backed totals with and without TJHSST, plus missing-row counts.
- `reports/tables/data_coverage_by_class.csv`: class-year row counts by rate-compatible coverage, NMSF gaps, denominator gaps, combined gaps, not-operating rows, and missing NMSF sources.
- `reports/tables/pre_post_summary_2023_2024_vs_2025_2026.csv`: pre/post summaries for Classes 2023-2024 versus 2025-2026 by comparison group, with coverage and small-number flags.
- `reports/figures/*.svg`: dependency-light SVG charts generated by `scripts/build_descriptive_outputs.py`.
- `reports/analysis.md`: consolidated findings, robustness, limitations, and integrity report generated by `scripts/build_analysis_reports.py`.
- `reports/conclusion_graphic.svg`: README infographic generated from committed analysis tables by `scripts/build_conclusion_graphic.py`; the PNG beside it is a raster snapshot.
- `reports/tables/analysis_*.csv`: supporting analysis and robustness tables generated by `scripts/build_analysis_reports.py`; supplemental cutoff/statewide fields in these tables are not written back to the canonical panel.
- `reports/tables/analysis_psat_participation_benchmark.csv`: source-backed Virginia Class 2023-2026 PSAT/NMSQT participation benchmark from College Board state reports; these statewide values are sensitivity inputs, not school-level estimates.
- `reports/tables/analysis_participation_sensitivity.csv`: pooled TJHSST/base-public results under the Virginia benchmark and a group-specific ±10% post/pre participation grid, including participant-yield proxies, standardized offsets, and public shortfalls.
- `reports/tables/analysis_participation_break_even.csv`: relative participation changes required to eliminate or reverse selected pooled and annual findings; thresholds are mechanical break-even checks, not observed participation estimates.
- `reports/tables/analysis_state_normalization_supplemental.csv`: supplemental Virginia-normalization table that preserves location-based and state-selection-unit totals separately and records numerator adjustments and scope-compatibility statuses.
- `reports/tables/virginia_share_by_class.csv`: descriptive shares using the Virginia school-location media-packet denominator, which matches the location-based school counts; official state-selection-unit totals are included as separate context fields.

## Source Notes

- `docs/source_notes/tj psat investigation.xlsx`: seed workbook for roster and enrollment data.
- `docs/source_notes/FCPS Regulation 3355.16 TJHSST Admissions.pdf`: admissions-policy source used by `data/processed/school_roster.csv` for current roster/pathway treatment. It supports not assigning private-school observations from school location alone because non-public applicants are considered for unallocated seats, and high-school pathway buckets are analytical geographies rather than observed admissions-pathway counts. It points to annual Notice 3355 materials for implementation details and does not by itself supply class-specific admissions outcomes. The analysis does not apply it retroactively as the governing regulation for focal Classes 2025 or 2026.
- `docs/source_notes/FCPS Regulation 3355.15 TJHSST Admissions.pdf`: archived historical regulation used for interpretation of the Class 2026 admissions cycle; the annual Notice 3355 files were not recovered.
- `docs/source_notes/analysis_research_sources.md`: external interpretation and supplemental-check source list; those sources do not modify canonical NMSF counts or panel placeholders except when explicitly represented in source-backed local data files.

## Source CSVs

- `data/sources/nmsf_counts.csv`: manual NMSF count transcriptions from named public sources. Each row must include source ID, provider, class year, school name, count, status, title, URL, date, scope, and completeness notes.
- `data/sources/source_manifest.yml`: source-level registry with publisher, publication date, URL, retrieval date, source type, completeness scope, zero-inference scope, parser name/version, notes, and computed source hashes for NMSF count sources.
- `data/sources/targeted_grade11_enrollment.csv`: official local-membership, private-school-profile, and identity-reconciled PSS Grade 11 supplements applied only to the exact mapped school year.
- `data/sources/virginia_statewide_totals.csv`: canonical dual-scope source table. Its primary statewide fields contain official NMSC Guide state-selection-unit totals of 397, 467, and 489, while its `virginia_location_*` fields preserve media-packet school-location totals of 400, 470, and 494 for Classes 2023, 2024, and 2026. It also carries the scope-reconciliation metadata; Class 2025 has no source-backed row.
- `data/sources/virginia_state_selection_unit_totals.csv`: official NMSC Guide input table used to build the state-selection-unit side of the canonical dual-scope table, including boarding-location and unresolved-difference reconciliation fields. Class 2025 has no source-backed row.
- `data/raw/nmsf/*/*_snapshot.csv`: count-only archived snapshots for source-backed NMSF releases. Student names are intentionally omitted. Rows with `snapshot_record_type=observation_count` feed `data/sources/nmsf_counts.csv`; rows with other record types are retained only for reconciliation or review.
- `data/raw/enrollment/pss_locator_2023_24/*.html`: archived NCES Private School Search locator pages used by the interim Class 2025 private-school denominator supplement. They are enrollment sources only, not NMSF count sources.
- `data/raw/enrollment/targeted_grade11/`: archived APS membership summaries and BASIS high-school profiles supporting the targeted Grade 11 supplements. The LSAS Class 2023 value comes from the separately referenced official NCES PSS ZIP.

## NMSF Source Rules

- `nmsf_count` must remain blank until a source-backed count is parsed, entered, or inferred as zero from a complete named source for the relevant scope.
- Any numeric `nmsf_count`, including zero, must have `nmsf_source_title`, `nmsf_source_url`, `nmsf_source_date`, and `nmsf_source_hash`.
- Use `verified_count` for positive source-backed NMSF counts.
- Use `verified_zero` only when the source is a complete named list for the relevant geography and year.
- Missing schools in incomplete articles remain blank with an explanatory status.
- `missing_source` means no source-backed observation has been recorded for that school/class year.
- `source_incomplete` means a source exists but cannot establish a count or zero for the observation.
- `ambiguous_school` means a source row cannot be joined safely to one canonical school.
- `not_operating` means the school was not operating for that class-year; it is not a zero NMSF count.
- `not_applicable` is reserved for rows outside the relevant observation scope.
- `source_hash` values for manual transcriptions are computed from the source metadata plus sorted transcribed count rows.
- APS and LCPS releases may list resident students attending TJHSST, and PWCS releases may list former PWCS middle-school students attending TJHSST. Those TJHSST subset references are retained in count-only snapshots for source-total reconciliation, but they are not imported as separate observations because TJHSST remains one school row.
- A total-only or unattributed district release, such as the official LCPS Class 2025 release, can be archived for reconciliation as `source_incomplete` but cannot create school-level observations or verified zeros.

## Analysis Panel Variables

`data/processed/analysis_panel.csv` has one row per canonical `school_id` and
`class_year`. It is regenerated by `scripts/build_analysis_panel.py`.

- Roster fields: `school_id`, `school`, `sector`, `analytical_unit_type`, `division`, `district_name`, `tj_pathway`, `pathway_status`, and `pathway_assignment_method` come from `data/processed/school_roster.csv`.
- `pathway_bucket_interpretation` marks public pathway buckets as analytical geographies rather than observed TJHSST admissions pathways. Private-school rows are marked as non-public unallocated applicant buckets, and TJHSST remains one unsplit school row.
- Class-year fields: `class_year`, `qualifying_psat_year`, and `grade11_school_year` come from `data/processed/class_year_mapping.csv`.
- NMSF fields: `nmsf_count`, `nmsf_status`, `nmsf_count_available`, `nmsf_source_id`, `nmsf_source_title`, `nmsf_source_url`, `nmsf_source_date`, `nmsf_source_hash`, `nmsf_source_scope`, `source_completeness`, and `observation_basis` come from `data/processed/nmsf_observations.csv`.
- Enrollment fields: `grade11_enrollment`, `enrollment_status`, `grade11_enrollment_available`, `enrollment_source_title`, `enrollment_source_url`, `enrollment_source_date`, `enrollment_source_hash`, `enrollment_source_file`, `enrollment_source_rows`, `enrollment_source_variable`, `nces_school_id`, `pss_ppin`, and `pss_imputation_flag` come from `data/processed/enrollment_panel.csv`.
- `nmsf_per_100_juniors` is calculated as `100 * nmsf_count / grade11_enrollment` only when both inputs are available and the denominator is greater than zero.
- `rate_status` explains why the row-level rate is calculated or blank: `calculated`, `missing_nmsf_count`, `missing_grade11_enrollment`, `missing_nmsf_and_grade11_enrollment`, or `not_operating`.
- `rate_input_compatible` is `true` only when the row has both a numeric NMSF count and a valid grade-11 denominator.
- `row_coverage_status`, `denominator_gap_flag`, and `nmsf_missingness_flag` keep raw missingness next to the derived rate.
- School-history fields: `school_history_event_types`, `row_history_flags`, `has_school_opening_flag`, `has_school_rename_flag`, and `has_school_relocation_flag` are derived from `data/manual/school_history.csv`.
- Pathway aggregate fields are repeated on every row in a pathway/class-year group. `pathway_nmsf_count_covered`, `pathway_grade11_enrollment_covered`, and `pathway_nmsf_per_100_juniors_covered` use only rows where `rate_input_compatible=true`.
- `pathway_operating_school_rows`, `pathway_compatible_school_rows`, `pathway_missing_nmsf_school_rows`, `pathway_missing_enrollment_school_rows`, `pathway_incompatible_school_rows`, `pathway_coverage_status`, and `pathway_has_complete_compatible_coverage` describe whether those pathway aggregates cover the full operating bucket.
- Virginia NMSF Selection Index cutoff fields are placeholders: `va_nmsf_selection_index_cutoff` is blank and `va_nmsf_selection_index_cutoff_status=not_sourced` until reliable class-year sources are added.
- `statewide_nmsf_semifinalist_total` and its status/source fields contain official NMSC state-selection-unit totals for Classes 2023, 2024, and 2026: 397, 467, and 489. They are blank with `statewide_nmsf_semifinalist_total_status=not_sourced` for Class 2025 and other unsourced years.
- `virginia_location_nmsf_semifinalist_total` and its status/source fields contain the school-location media-packet totals for Classes 2023, 2024, and 2026: 400, 470, and 494. They are blank with `virginia_location_nmsf_semifinalist_total_status=not_sourced` for Class 2025 and other unsourced years.
- `nmsc_guide_virginia_school_count`, `known_boarding_location_count`, `unresolved_location_difference`, `state_selection_unit_reconciliation_status`, and `state_selection_unit_reconciliation_notes` preserve the evidence connecting the two scopes. Boarding-school blocks reconcile Classes 2023 and 2026; two Class 2024 students remain scope-unresolved. Location-based shares must use the location total, while a state-unit share requires a scope-compatible numerator.
- `denominator_type=grade11_enrollment_outcome_denominator` and `admissions_seat_allocation_input_status=not_included_requires_sourced_8th_grade_population` make clear that this panel does not use grade-11 enrollment as an admissions-seat allocation input.

## Descriptive Output Rules

- Observed NMSF count totals include only rows where `nmsf_count_available=true`; missing-source rows remain blank rather than zero.
- Covered rates use only rows where `rate_input_compatible=true`; a count with a missing denominator contributes to observed count totals but not to covered-rate numerators.
- `school_group=Base public schools` excludes the single TJHSST row; TJHSST is shown as its own group.
- Private-school rows remain `Private/homeschool unallocated` analytical buckets and are not allocated to public pathways by school location.
- Pathway heatmap values come from the repeated covered-subset pathway fields in `analysis_panel.csv`; check `pathway_coverage_status` before treating them as complete pathway totals.
- Virginia cutoff placeholders and source-backed statewide-total coverage are documented in `reports/descriptive_results.md`; descriptive figures do not annotate cutoff changes until those fields are source-backed.

## Enrollment Statuses

- `reported`: the seed source reports a numeric grade 11 count.
- `not_operating`: the school was not operating for that class-year and the denominator remains blank.
- `not_applicable`: NCES marks the value with a dagger.
- `missing`: NCES marks the value missing.
- `failed_quality_standard`: NCES marks the value as failing data quality standards.
- `source_row_not_found`: no source row matched the canonical school aliases.
- `ambiguous_source_name`: multiple source rows matched and the seed source lacks identifiers needed to disambiguate.
- `source_year_not_in_seed`: the seed workbook does not include the school year required for the class year.
- `private_pss_not_ingested`: private school enrollment is pending NCES PSS ingestion.
- `public_2024_25_source_missing`: the public Class 2026 CCD source extract has not been generated.
- `ccd_row_not_found`: the CCD membership file did not contain a grade-11 total row for the roster row's NCES school ID.
- `private_pss_not_survey_year`: the grade-11 school year is not covered by an available PSS survey file; no adjacent-year value is substituted.
- `private_pss_id_pending`: no unique curated PSS `PPIN` has been assigned for the private-school row.
- `ambiguous_pss_id`: PSS contains multiple plausible private-school identifiers, including locator search duplicates, and the denominator remains blank until independently resolved.
- `locator_search_not_found`: the 2023-24 NCES Private School Search locator returned no current row for the documented school-name search, so the Class 2025 denominator remains blank.
- `pss_row_not_found`: the curated PSS `PPIN` was not present in that survey year's public-use file.
- `blank`: the source row exists, but the grade-11 variable is blank.

After targeted supplements, the unresolved focal private denominators are:

- Class 2023: Flint Hill, Oakcrest, Potomac, Pinnacle Academy, and Seton School.
- Class 2024: all 16 rostered private schools.
- Class 2025: Flint Hill, Oakcrest, Potomac, Loudoun School for Advanced Studies, and Seton School.
- Class 2026: all 15 rostered private schools other than BASIS Independent McLean.

## Enrollment Source Variables

- Public Class 2026 CCD rows use the `Grade 11` total membership row where race and sex are `No Category Codes`.
- Private PSS rows use `P290` for grade-11 enrollment.
- Private PSS rows preserve `F_P290` in `pss_imputation_flag` when present.
- The interim 2023-24 NCES Private School Search locator supplement uses `PSS_ENROLL_11` for Class 2025 private-school grade-11 enrollment and records `pss_imputation_flag=not_available_locator` because locator detail pages do not expose `F_P290`.
- Exact targeted supplements override an unavailable default CCD/PSS row only for the documented school/class-year key. H-B Woodlawn uses the official APS Grade 11 membership row; LSAS Class 2023 uses the common `P290=11` reported by both same-address PSS identities with no imputation; BASIS Classes 2025-2026 use the Grade 11 boxes in official school profiles.
- No enrollment value is estimated from adjacent school years.

## Roster Statuses

- `pathway_status=assigned`: the public-school or TJHSST roster row has a source-backed analytical pathway assignment.
- `pathway_status=unallocated_private_applicant`: the private-school row is intentionally not assigned to an FCPS region or participating-jurisdiction pathway by school location because Regulation 3355.16 places non-public applicants in the unallocated-seat pool.
- `pathway_assignment_method=base_school_region`: an FCPS public-school row is assigned from a seed-workbook high-school-to-region analytical bucket; Regulation 3355.16 allocates admissions seats by each public school's 8th-grade population.
- `pathway_assignment_method=participating_jurisdiction`: a public-school row is assigned from the seed workbook to Arlington, Falls Church City, Loudoun, or Prince William as an analytical bucket; annual cooperating-division participation and actual admissions outcomes require separate sources.
- `pathway_assignment_method=single_tjhsst_row`: TJHSST remains one canonical school row.
- `pathway_assignment_method=nonpublic_unallocated_seats`: a private-school row is marked as non-public/unallocated because the school location alone does not determine the applicant's TJ pathway.
- `pathway_source_title`, `pathway_source_path`, `pathway_source_date`, and `pathway_source_hash`: source metadata for the admissions-pathway rule applied to the roster row.
- `identifier_status=matched_2023_24_ccd`: a public roster row matched exactly one 2023-24 NCES CCD school directory row within its division.
- `identifier_status=private_pss_id_not_ingested`: private-school identifiers are pending NCES PSS ingestion.
