# Data Dictionary

## Generated CSVs

- `data/interim/canonical_schools.csv`: canonical roster from the workbook `raw` sheet.
- `data/interim/public_enrollment_raw.csv`: long-form transcription of public enrollment rows from `Sheet6`.
- `data/interim/public_grade11_enrollment.csv`: canonical public-school grade 11 enrollment by class year.
- `data/interim/panel_seed.csv`: school-by-class-year panel with blank NMSF counts and source-pending statuses.
- `data/interim/panel_nmsf.csv`: `panel_seed.csv` plus source-backed NMSF count transcriptions from `data/sources/nmsf_counts.csv`.

## Source CSVs

- `data/sources/nmsf_counts.csv`: manual NMSF count transcriptions from named public sources. Each row must include source ID, provider, class year, school name, count, status, title, URL, date, scope, and completeness notes.
- `data/sources/source_manifest.yml`: source-level metadata and computed source hashes for NMSF count sources.

## NMSF Source Rules

- `nmsf_count` must remain blank until a source-backed count is parsed or entered.
- Any numeric `nmsf_count`, including zero, must have `nmsf_source_title`, `nmsf_source_url`, `nmsf_source_date`, and `nmsf_source_hash`.
- Use `verified_zero` only when the source is a complete named list for the relevant geography and year.
- Missing schools in incomplete articles remain blank with an explanatory status.
- `parsed` means the count was transcribed from a named source row or list and matched to the canonical roster.
- `source_hash` values for manual transcriptions are computed from the source metadata plus sorted transcribed count rows.

## Enrollment Statuses

- `reported`: the seed source reports a numeric grade 11 count.
- `not_applicable`: NCES marks the value with a dagger.
- `missing`: NCES marks the value missing.
- `failed_quality_standard`: NCES marks the value as failing data quality standards.
- `source_row_not_found`: no source row matched the canonical school aliases.
- `ambiguous_source_name`: multiple source rows matched and the seed source lacks identifiers needed to disambiguate.
- `source_year_not_in_seed`: the seed workbook does not include the school year required for the class year.
- `private_pss_not_ingested`: private school enrollment is pending NCES PSS ingestion.
