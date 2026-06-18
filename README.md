# tj-psat-analysis

Reproducible data pipeline for a TJHSST admissions-change analysis.

The first milestone builds a canonical school roster and grade 11 enrollment
panel from `docs/source_notes/tj psat investigation.xlsx`. National Merit
Semifinalist counts are intentionally blank in the seed panel until each count
has source metadata.

## First-Milestone Build

```bash
python scripts/build_seed_data.py
python scripts/validate_nmsf_sources.py
python -m unittest discover -s tests
```

Generated first-milestone outputs:

- `data/interim/canonical_schools.csv`
- `data/interim/public_enrollment_raw.csv`
- `data/interim/public_grade11_enrollment.csv`
- `data/interim/panel_seed.csv`

## Source Discipline

- Do not use the workbook `nsmf 2019` sheet as evidence for NMSF counts.
- Numeric NMSF counts require URL, title, date, and source hash.
- Missing schools in incomplete articles are blank, not zero.
- `verified_zero` is only valid for complete named lists for the geography and year.
- TJHSST stays as a single school row.
