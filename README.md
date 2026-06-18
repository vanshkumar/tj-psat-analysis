# tj-psat-analysis

Reproducible data pipeline for a TJHSST admissions-change analysis.

The first milestone builds a canonical school roster and grade 11 enrollment
panel from `docs/source_notes/tj psat investigation.xlsx`. National Merit
Semifinalist counts are intentionally blank in the seed panel until each count
has source metadata.

## First-Milestone Build

```bash
python scripts/build_seed_data.py
python scripts/build_school_roster.py
python scripts/apply_nmsf_counts.py
python scripts/validate_nmsf_sources.py data/interim/panel_nmsf.csv
python -m unittest discover -s tests
```

Generated first- and second-milestone outputs:

- `data/manual/tj psat investigation.xlsx`
- `data/interim/canonical_schools.csv`
- `data/interim/public_enrollment_raw.csv`
- `data/interim/public_grade11_enrollment.csv`
- `data/interim/panel_seed.csv`
- `data/interim/panel_nmsf.csv`
- `data/processed/schools.csv`
- `data/processed/school_roster.csv`
- `data/processed/public_enrollment.csv`
- `data/processed/class_year_mapping.csv`
- `data/manual/public_school_nces_ids.csv`
- `data/manual/school_aliases.csv`
- `data/manual/school_history.csv`
- `reports/data_quality/workbook_ingestion.md`
- `reports/data_quality/roster_review.md`

The build command reads the seed workbook from
`docs/source_notes/tj psat investigation.xlsx`, preserves it unchanged, and
creates a byte-identical copy under `data/manual/` for the manual source
inventory required by the task plan.

`scripts/build_school_roster.py` builds the Milestone 2 roster deliverables
from the seed roster and curated source files. To refresh public-school NCES
IDs from the official CCD directory ZIP, run:

```bash
python scripts/build_school_roster.py --ccd-directory-zip /path/to/ccd_sch_029_2324_w_1a_073124.zip
```

## Development Checks

```bash
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m unittest discover -s tests
```

## NMSF Count Ingestion

`data/sources/nmsf_counts.csv` stores source-backed count transcriptions. The
first source slice covers official FCPS National Merit Semifinalist releases
for Classes 2024, 2025, and 2026. The importer computes source hashes from the
source metadata plus transcribed count rows, matches schools against the
canonical roster, and writes `data/interim/panel_nmsf.csv`.

The importer does not infer zeros from complete source lists yet. Schools not
explicitly transcribed remain `source_pending` until zero-generation is added as
a separate audited step.

## Source Discipline

- Do not use the workbook `nsmf 2019` sheet as evidence for NMSF counts.
- Numeric NMSF counts require URL, title, date, and source hash.
- Missing schools in incomplete articles are blank, not zero.
- `verified_zero` is only valid for complete named lists for the geography and year.
- TJHSST stays as a single school row.
