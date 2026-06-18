# Data Dictionary

## Generated CSVs

- `data/interim/canonical_schools.csv`: canonical roster from the workbook `raw` sheet.
- `data/interim/public_enrollment_raw.csv`: long-form transcription of public enrollment rows from `Sheet6`.
- `data/interim/public_grade11_enrollment.csv`: canonical public-school grade 11 enrollment by class year.
- `data/interim/panel_seed.csv`: school-by-class-year panel with blank NMSF counts and source-pending statuses.
- `data/interim/panel_nmsf.csv`: `panel_seed.csv` plus source-backed NMSF count transcriptions from `data/sources/nmsf_counts.csv`.
- `data/processed/school_roster.csv`: Milestone 2 roster with canonical school IDs, pathway status, pathway assignment method, pathway source metadata, sector, district, NCES IDs where source-backed, and operating-year boundaries.
- `data/manual/school_aliases.csv`: deterministic alias table. Rows with `join_allowed=false` are known ambiguous aliases and must not be used for automatic observation joins.
- `data/manual/school_history.csv`: source-noted rename, opening, and relocation events used to keep historical names and not-operating years explicit.
- `data/manual/public_school_nces_ids.csv`: source-backed public-school NCES IDs matched from the NCES CCD 2023-24 directory by division and normalized alias.
- `reports/data_quality/roster_review.md`: Milestone 2 roster coverage, alias conflicts, history review, admissions-pathway source summary, and pathway review status.

## Source Notes

- `docs/source_notes/tj psat investigation.xlsx`: seed workbook for roster and enrollment data.
- `docs/source_notes/TJHSST Admissions Merit Lottery Proposal.pdf`: admissions-pathway source used by `data/processed/school_roster.csv`. It establishes that FCPS regional placement is based on the student's base school, and private-school applicants are assigned by residency rather than by the private school's location.

## Source CSVs

- `data/sources/nmsf_counts.csv`: manual NMSF count transcriptions from named public sources. Each row must include source ID, provider, class year, school name, count, status, title, URL, date, scope, and completeness notes.
- `data/sources/source_manifest.yml`: source-level metadata and computed source hashes for NMSF count sources.

## NMSF Source Rules

- `nmsf_count` must remain blank until a source-backed count is parsed or entered.
- Any numeric `nmsf_count`, including zero, must have `nmsf_source_title`, `nmsf_source_url`, `nmsf_source_date`, and `nmsf_source_hash`.
- Use `verified_zero` only when the source is a complete named list for the relevant geography and year.
- Missing schools in incomplete articles remain blank with an explanatory status.
- `parsed` means the count was transcribed from a named source row or list and matched to the canonical roster.
- `not_operating` means the school was not operating for that class-year; it is not a zero NMSF count.
- `source_hash` values for manual transcriptions are computed from the source metadata plus sorted transcribed count rows.

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

## Roster Statuses

- `pathway_status=assigned`: the public-school or TJHSST roster row has a source-backed task-plan pathway.
- `pathway_status=residency_based_private_applicant`: the private-school row is intentionally not assigned to an FCPS region or participating-jurisdiction pathway by school location; the admissions proposal says private-school applicants are assigned by residency.
- `pathway_assignment_method=base_school_region`: an FCPS public-school row is assigned from the student's base-school region.
- `pathway_assignment_method=participating_jurisdiction`: a public-school row is assigned to Arlington, Falls Church City, Loudoun, or Prince William.
- `pathway_assignment_method=single_tjhsst_row`: TJHSST remains one canonical school row.
- `pathway_assignment_method=applicant_residency`: a private-school row is marked as residency-based because the school location alone does not determine the applicant's TJ pathway.
- `pathway_source_title`, `pathway_source_path`, `pathway_source_date`, and `pathway_source_hash`: source metadata for the admissions-pathway rule applied to the roster row.
- `identifier_status=matched_2023_24_ccd`: a public roster row matched exactly one 2023-24 NCES CCD school directory row within its division.
- `identifier_status=private_pss_id_not_ingested`: private-school identifiers are pending NCES PSS ingestion.
