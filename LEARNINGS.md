# Learnings

## What Has Worked

**2026-06-18 — Seed roster/enrollment ingestion**
- Observation: The workbook `raw` sheet yields 76 canonical roster rows and keeps TJHSST as exactly one school row.
- Action: Build canonical school outputs from `raw`; do not add schools from `nsmf 2019` unless independently source-backed and intentionally added to the roster.
- Confidence: high

**2026-06-18 — Public enrollment matching**
- Observation: `Sheet6` contains two `FREEDOM HIGH` rows without district names or NCES IDs, so the seed workbook alone cannot distinguish South Riding from Woodbridge.
- Action: Leave both canonical Freedom High enrollment values blank with `ambiguous_source_name` until an enrollment source with district or NCES identifiers resolves the rows.
- Confidence: high

**2026-06-18 — Rename alias parsing**
- Observation: Roster notes such as `Renamed from George Mason HS in 2021` include date text after the prior school abbreviation.
- Action: Strip trailing date phrases when deriving aliases from rename notes so aliases remain school names, not school-name-plus-year strings.
- Confidence: high

## Patterns and Preferences

**2026-06-18 — Local test invocation**
- Observation: The reliable project test target is unittest discovery, but this workspace has no bare `python` and system `python3` lacks the project dependencies.
- Action: Use `UV_CACHE_DIR=.uv-cache uv run python -m unittest discover -s tests` when syncing is acceptable, or add `--no-sync` after the uv environment is already synced.
- Confidence: high

**2026-06-18 - Hypothesis framing**
- Observation: The project handoff frames the work as a testable right-tail outcome study, not as a direct measurement of culture or a value judgment on TJHSST admissions policy.
- Action: Keep future narrative docs explicit that NMSF is a narrow source-backed signal, and require regional offset tests before making claims from TJHSST-only changes.
- Confidence: high

**2026-06-18 — Source-note preservation**
- Observation: Raw ChatGPT/source-note text files live under `docs/source_notes/` alongside the seed workbook, separate from generated CSV outputs.
- Action: When asked to push everything, preserve these files as source notes rather than folding their contents into canonical data.
- Confidence: high

**2026-06-18 — Repo handoff status review**
- Observation: The current scaffold already has the first-milestone roster/enrollment seed in place, with an empty NMSF source manifest and all 608 panel rows still marked `source_pending`.
- Action: Treat the next major milestone as source-backed NMSF manifest/parsers rather than recreating the repo scaffold or public-enrollment seed outputs.
- Confidence: high

**2026-06-18 - Manual NMSF ingestion**
- Observation: `scripts/apply_nmsf_counts.py` overlays source-backed transcriptions from `data/sources/nmsf_counts.csv` onto `panel_seed.csv`, leaving the seed panel blank and computing source hashes from each source's metadata plus transcribed count rows.
- Action: Add future district or private-school NMSF slices to `data/sources/nmsf_counts.csv` and regenerate `data/interim/panel_nmsf.csv`; do not hand-edit `panel_nmsf.csv` counts directly.
- Confidence: high

**2026-06-18 - Source-note deletion**
- Observation: The exported ChatGPT source-note text files under `docs/source_notes/` were intentionally removed by the user, while the seed workbook remains in place.
- Action: Preserve source notes by default, but stage these specific deletions when publishing this repo state because the user explicitly confirmed them.
- Confidence: high

**2026-06-18 - Task plan status review**
- Observation: `TASKS.md` is newly added with unchecked boxes, while the repo already contains tested first-milestone seed outputs and a partial FCPS NMSF pilot under `data/interim/` and `data/sources/`.
- Action: Treat `TASKS.md` checkboxes as unsynced planning state until they are reconciled against repository artifacts and tests.
- Confidence: high

**2026-06-18 - Milestone 1 completion**
- Observation: `scripts/build_seed_data.py` now emits both legacy interim files and milestone deliverables under `data/processed/`, plus `reports/data_quality/workbook_ingestion.md` and a byte-identical workbook copy under `data/manual/`.
- Action: Use `python scripts/build_seed_data.py` as the single regeneration command for Milestone 1; keep `docs/source_notes/tj psat investigation.xlsx` and `data/manual/tj psat investigation.xlsx` hash-identical.
- Confidence: high

**2026-06-18 - Main-branch publishing**
- Observation: The repository's active branch is `main` tracking `origin/main`, and the user's "merge & push everything" request applies directly to that branch rather than a feature branch PR.
- Action: For this repo state, commit the confirmed Milestone 1 scope on `main` and push `origin/main`; do not create an extra `codex/` branch unless the user asks for PR-style review.
- Confidence: high

**2026-06-18 - TJ pathway assignment**
- Observation: `docs/source_notes/FCPS Regulation 3355.16 TJHSST Admissions.pdf` places non-public applicants in the unallocated-seat pool after residency eligibility, while public-school seat allocation is based on each public school's 8th-grade population.
- Action: Keep private-school rows as `Private/homeschool unallocated`/`nonpublic_unallocated_seats`; do not allocate private-school NMSF observations to FCPS regions or participating jurisdictions from school location alone.
- Confidence: high

**2026-06-18 - Admissions policy source review**
- Observation: The September 15, 2020 merit-lottery deck was a proposal source and has been replaced in `docs/source_notes/` by Regulation 3355.16, effective 2022-05-17.
- Action: Use Regulation 3355.16 for admissions-mechanism claims; label high-school pathway NMSF buckets as analytical geographies unless actual pathway/offers data are sourced.
- Confidence: high

**2026-06-18 - Regulation 3355.16 scope**
- Observation: Regulation 3355.16 points to annual Notice 3355 for implementation details and uses 8th-grade populations for admissions-seat allocation, while this project's NMSF rates use grade-11 enrollment as an outcome denominator.
- Action: Archive annual notices and historical regulation versions before making class-specific admissions-mechanism claims; do not use grade-11 enrollment as a proxy for allocated-seat inputs.
- Confidence: high

**2026-06-18 - Generated CSV line endings**
- Observation: Python's default `csv.DictWriter` line endings caused generated CSVs to trip `git diff --check` as trailing whitespace.
- Action: Set `lineterminator="\n"` in project CSV writers and regenerate CSV outputs before publishing.
- Confidence: high

**2026-06-18 - Milestone 2 roster matching**
- Observation: The NCES CCD data-file API exposes the 2023-24 school directory ZIP, and matching public roster rows by LEA name plus normalized aliases resolves both Freedom High Schools. H-B Woodlawn needs the CCD spelling `HB Woodlawn Secondary Program`.
- Action: Refresh `data/manual/public_school_nces_ids.csv` with `scripts/build_school_roster.py --ccd-directory-zip ...`; avoid name-only NCES matching for duplicated school names.
- Confidence: high

**2026-06-18 — NMSF panel integration**
- Observation: `data/interim/panel_nmsf.csv` is built from `data/interim/panel_seed.csv`, so it does not include Milestone 3 denominators from `data/processed/enrollment_panel.csv`; Class 2026 parsed NMSF rows still have blank rates there.
- Action: Use `data/processed/enrollment_panel.csv` when auditing post-Milestone-3 rates, and build the future analysis panel by joining NMSF observations to that processed enrollment panel rather than relying on `panel_nmsf.csv` alone.
- Confidence: high

**2026-06-18 — NMSF observation layer**
- Observation: `scripts/build_nmsf_observations.py` validates `data/sources/source_manifest.yml`, emits `data/processed/nmsf_observations.csv`, and keeps NMSF observations separate from enrollment/rate calculations.
- Action: Add future NMSF sources to both the manifest and `data/sources/nmsf_counts.csv`, then regenerate observations; use `verified_zero` only through manifest-declared complete source scopes.
- Confidence: high

**2026-06-18 - NMSF source archiving**
- Observation: FCPS NMSF release pages list individual student names, while Task 4 only needs source-backed school-level counts and archive hashes.
- Action: Archive FCPS releases as count-only snapshots under `data/raw/nmsf/fcps/`, record their SHA-256 hashes in `data/sources/source_manifest.yml`, and let manifest validation reject missing or changed archive files.
- Confidence: high

**2026-06-18 - Operating-year roster status**
- Observation: Independence, Lightridge, and Gainesville have in-panel opening years, so pre-opening class-years should be blank `not_operating` rows rather than `source_pending` NMSF rows or NCES dagger-style `not_applicable` enrollment rows.
- Action: Keep first operating class years in `FIRST_OPERATING_CLASS_YEAR_BY_SCHOOL_ID` and regenerate seed outputs after changing school-history rules.
- Confidence: high

**2026-06-18 - CCD membership ingestion**
- Observation: The NCES CCD 2024-25 school membership ZIP can be listed by Python `zipfile`, but its CSV member uses a compression method that `zipfile.open()` cannot stream; the system `unzip -p` handles it. Grade-11 totals are the `Grade 11` rows where race and sex are `No Category Codes`.
- Action: Use the `enrollment.py` streaming ZIP fallback for CCD membership files, and extract the grade-11 total row rather than summing race/sex detail rows.
- Confidence: high

**2026-06-18 - Private PSS matching**
- Observation: PSS has locality-sensitive duplicate/private-name pitfalls, including `TRINITY CHRISTIAN SCHOOL` rows outside the TJ area and a separate Fairfax row keyed by `PPIN=K9306124`.
- Action: Match private-school PSS denominators through curated `PPIN` values in `data/manual/private_school_pss_ids.csv`; do not join private PSS rows by normalized school name alone.
- Confidence: high

**2026-06-18 - Enrollment coverage gaps**
- Observation: H-B Woodlawn has a matched 2023-24 CCD directory ID, but the 2024-25 CCD membership file did not contain a grade-11 total row for that ID; several private schools also have blank, missing, ambiguous, or non-survey-year PSS denominator rows.
- Action: Keep these rows blank with machine-readable enrollment statuses in `enrollment_panel.csv`; do not backfill from adjacent years or similar schools.
- Confidence: high

## What Has Failed
