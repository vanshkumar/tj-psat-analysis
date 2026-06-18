# tj-psat-analysis

Reproducible data pipeline for a TJHSST admissions-change analysis.

The first milestone builds a canonical school roster and grade 11 enrollment
panel from `docs/source_notes/tj psat investigation.xlsx`. National Merit
Semifinalist counts are intentionally blank in the seed panel until each count
has source metadata.

The second milestone adds canonical aliases, school-history events, public
NCES identifiers, and admissions-policy caveats from
`docs/source_notes/FCPS Regulation 3355.16 TJHSST Admissions.pdf`. That
regulation supports treating private-school rows as non-public applicants for
unallocated seats rather than assigning them from school location alone. High
school NMSF pathway buckets remain analytical geographies unless actual TJHSST
pathway/offers data are sourced later. Annual Notice 3355 materials and older
regulation versions are still needed before making class-specific admissions
mechanism claims.

## First-Milestone Build

```bash
python scripts/build_seed_data.py
python scripts/build_school_roster.py
python scripts/apply_nmsf_counts.py
python scripts/build_nmsf_observations.py
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
- `data/processed/nmsf_observations.csv`
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

`scripts/build_nmsf_observations.py` builds the Milestone 4 count-observation
layer at `data/processed/nmsf_observations.csv`. It validates
`data/sources/source_manifest.yml`, keeps NMSF observations separate from
enrollment denominators, and uses `verified_zero` only for manifest sources
marked complete for the relevant scope. The current FCPS 2024-2026 sources are
complete named FCPS lists, so absent rostered FCPS public schools receive
source-backed zero observations for those classes. Schools outside the source
scope remain `missing_source`.

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
