# Data Dictionary

## Generated CSVs

- `data/interim/canonical_schools.csv`: canonical roster from the workbook `raw` sheet.
- `data/interim/public_enrollment_raw.csv`: long-form transcription of public enrollment rows from `Sheet6`.
- `data/interim/public_grade11_enrollment.csv`: canonical public-school grade 11 enrollment by class year.
- `data/interim/public_grade11_enrollment_2024_25.csv`: Class 2026 public-school grade 11 enrollment extracted from the NCES CCD 2024-25 school membership file by NCES school ID.
- `data/interim/private_grade11_enrollment.csv`: private-school PSS survey-year grade 11 enrollment extract using `P290`, with `F_P290` preserved as `pss_imputation_flag`.
- `data/interim/panel_seed.csv`: school-by-class-year panel with blank NMSF counts and source-pending statuses.
- `data/interim/panel_nmsf.csv`: legacy interim seed panel plus source-backed NMSF count transcriptions from `data/sources/nmsf_counts.csv`; it should not be treated as the final analytical panel because it is seed-based and does not include all Milestone 3 denominator updates.
- `data/processed/nmsf_observations.csv`: Milestone 4 NMSF observation layer with one row per school/class year, source-backed positive counts, source-backed complete-list zeros, explicit missingness, and no enrollment denominators or rates.
- `data/processed/nmsf_observations_2023_2026.csv`: Milestone 5 four-year pilot slice filtered from `data/processed/nmsf_observations.csv` for Classes 2023-2026.
- `data/processed/school_roster.csv`: Milestone 2 roster with canonical school IDs, pathway status, pathway assignment method, pathway source metadata, sector, district, NCES IDs where source-backed, and operating-year boundaries.
- `data/processed/enrollment_panel.csv`: Milestone 3 school-by-class-year grade 11 enrollment denominator panel for public and private schools, with source metadata and explicit missingness statuses.
- `data/manual/school_aliases.csv`: deterministic alias table. Rows with `join_allowed=false` are known ambiguous aliases and must not be used for automatic observation joins.
- `data/manual/school_history.csv`: source-noted rename, opening, and relocation events used to keep historical names and not-operating years explicit.
- `data/manual/public_school_nces_ids.csv`: source-backed public-school NCES IDs matched from the NCES CCD 2023-24 directory by division and normalized alias.
- `data/manual/private_school_pss_ids.csv`: curated private-school PSS `PPIN` match table used to prevent name-only private-school joins.
- `reports/data_quality/roster_review.md`: Milestone 2 roster coverage, alias conflicts, history review, admissions-pathway source summary, and pathway review status.
- `reports/data_quality/enrollment_coverage.csv`: one coverage row for each school and class year in `data/processed/enrollment_panel.csv`.
- `reports/data_quality/enrollment_coverage.md`: Milestone 3 denominator coverage summary, source list, and no-estimation rules.
- `reports/data_quality/nmsf_source_registry.md`: Milestone 4 source-registry summary for NMSF observations, including status counts, source counts, and zero-inference rules.
- `reports/data_quality/nmsf_reconciliation_2023_2026.md`: Milestone 5 reconciliation summary for the four-year pilot, including source reported totals, in-panel totals, excluded count-only snapshot totals, and remaining source gaps.
- `reports/data_quality/manual_review_queue.csv`: Milestone 5 review queue for missing school-year sources plus source rows excluded from the panel, such as jurisdictional TJHSST subsets and non-roster schools.

## Source Notes

- `docs/source_notes/tj psat investigation.xlsx`: seed workbook for roster and enrollment data.
- `docs/source_notes/FCPS Regulation 3355.16 TJHSST Admissions.pdf`: admissions-policy source used by `data/processed/school_roster.csv`. It supports not assigning private-school observations from school location alone because non-public applicants are considered for unallocated seats, and high-school pathway buckets are analytical geographies rather than observed admissions-pathway counts. It points to annual Notice 3355 materials for implementation details and does not by itself supply class-specific admissions outcomes.

## Source CSVs

- `data/sources/nmsf_counts.csv`: manual NMSF count transcriptions from named public sources. Each row must include source ID, provider, class year, school name, count, status, title, URL, date, scope, and completeness notes.
- `data/sources/source_manifest.yml`: source-level registry with publisher, publication date, URL, retrieval date, source type, completeness scope, zero-inference scope, parser name/version, notes, and computed source hashes for NMSF count sources.
- `data/raw/nmsf/*/*_snapshot.csv`: count-only archived snapshots for source-backed NMSF releases. Student names are intentionally omitted. Rows with `snapshot_record_type=observation_count` feed `data/sources/nmsf_counts.csv`; rows with other record types are retained only for reconciliation or review.

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
- APS and LCPS releases may list resident students attending TJHSST. Those resident subsets are retained in count-only snapshots for source-total reconciliation, but they are not imported as separate observations because TJHSST remains one school row.

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
- `ambiguous_pss_id`: PSS contains multiple plausible private-school identifiers and the denominator remains blank until independently resolved.
- `pss_row_not_found`: the curated PSS `PPIN` was not present in that survey year's public-use file.
- `blank`: the source row exists, but the grade-11 variable is blank.

## Enrollment Source Variables

- Public Class 2026 CCD rows use the `Grade 11` total membership row where race and sex are `No Category Codes`.
- Private PSS rows use `P290` for grade-11 enrollment.
- Private PSS rows preserve `F_P290` in `pss_imputation_flag` when present.
- No enrollment value is estimated from adjacent school years.

## Roster Statuses

- `pathway_status=assigned`: the public-school or TJHSST roster row has a source-backed task-plan pathway.
- `pathway_status=unallocated_private_applicant`: the private-school row is intentionally not assigned to an FCPS region or participating-jurisdiction pathway by school location because Regulation 3355.16 places non-public applicants in the unallocated-seat pool.
- `pathway_assignment_method=base_school_region`: an FCPS public-school row is assigned from a seed-workbook high-school-to-region analytical bucket; Regulation 3355.16 allocates admissions seats by each public school's 8th-grade population.
- `pathway_assignment_method=participating_jurisdiction`: a public-school row is assigned from the seed workbook to Arlington, Falls Church City, Loudoun, or Prince William as an analytical bucket; annual cooperating-division participation and actual admissions outcomes require separate sources.
- `pathway_assignment_method=single_tjhsst_row`: TJHSST remains one canonical school row.
- `pathway_assignment_method=nonpublic_unallocated_seats`: a private-school row is marked as non-public/unallocated because the school location alone does not determine the applicant's TJ pathway.
- `pathway_source_title`, `pathway_source_path`, `pathway_source_date`, and `pathway_source_hash`: source metadata for the admissions-pathway rule applied to the roster row.
- `identifier_status=matched_2023_24_ccd`: a public roster row matched exactly one 2023-24 NCES CCD school directory row within its division.
- `identifier_status=private_pss_id_not_ingested`: private-school identifiers are pending NCES PSS ingestion.
