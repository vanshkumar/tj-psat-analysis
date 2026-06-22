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

**2026-06-19 - FCPS archive discovery**
- Observation: Direct FCPS search did not expose the Class 2023 NMSF release, but the Internet Archive `/news/` prefix index found both the 237-student and later 238-student official FCPS URLs.
- Action: When an older FCPS release is missing from current search, download the archived `www.fcps.edu/news/` CDX prefix index and filter locally for `national-merit` before treating the source as absent.
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

**2026-06-19 - Milestone 5 readiness review**
- Observation: At the start of Milestone 5, the NMSF manifest and observation framework passed tests, but the four-year pilot had source-backed rows only for FCPS Classes 2024-2026; Class 2023 and non-FCPS/public-private coverage remained `missing_source`.
- Action: Start Milestone 5 with source collection and archival for Class 2023 FCPS plus LCPS, APS, PWCS, Falls Church City/Meridian, and verifiable private-school sources before building reconciliation outputs.
- Confidence: high

**2026-06-19 - Milestone 5 jurisdictional source handling**
- Observation: APS and LCPS NMSF releases list resident students attending TJHSST separately from base-school lists, while the project panel treats TJHSST as one school row sourced from the FCPS/TJHSST release.
- Action: Keep jurisdictional TJHSST subsets in count-only snapshots for source-total reconciliation, but exclude them from `nmsf_observations.csv` to avoid double counting or splitting TJHSST by residence.
- Confidence: high

**2026-06-19 - LCPS 2025 NMSF source**
- Observation: The official LCPS Class 2025 semifinalist release lists 57 LCPS students but does not list school affiliations.
- Action: Archive it as a `source_incomplete_unattributed_total` for reconciliation only; do not add school rows to `nmsf_counts.csv` or infer LCPS Class 2025 zeros from it.
- Confidence: high

**2026-06-19 - APS archive discovery**
- Observation: APS's current WordPress API returned only recent NMSF semifinalist posts, while the Internet Archive `www.apsva.us/post/` prefix index exposed the archived Class 2023 `17 Seniors Named...` release.
- Action: For missing older APS NMSF releases, filter the archived `/post/` CDX prefix index locally before concluding APS has no official source.
- Confidence: high

**2026-06-19 - Shared NMSF count CSV compatibility**
- Observation: `data/sources/nmsf_counts.csv` is read by both the Milestone 4 observation builder with `school_aliases.csv` and the legacy interim panel applier with seed-workbook aliases only.
- Action: Use canonical-compatible source school names for rows like H-B Woodlawn, and keep provider-aware ambiguity resolution for duplicated public names such as Freedom High School.
- Confidence: high

**2026-06-19 - Milestone 5 queue interpretation**
- Observation: `reports/data_quality/manual_review_queue.csv` includes 175 true `missing_school_year_source` rows plus six intentional non-observation snapshot rows used for APS/LCPS TJHSST, Arlington Tech, and LCPS 2025 unattributed-total reconciliation.
- Action: Use the reconciliation report's Source Gaps table, not the raw manual-review queue row count, when summarizing unresolved Milestone 5 source coverage.
- Confidence: high

**2026-06-19 - PWCS NMSF source handling**
- Observation: PWCS's live site can be blocked by Cloudflare, but the Internet Archive `www.pwcs.edu/news/` index exposes the official Classes 2023-2026 semifinalist releases; those releases list PWCS-enrolled high-school students separately from former PWCS middle-school students attending TJHSST.
- Action: For PWCS NMSF backfill, filter the archived `/news/` CDX index locally, import only PWCS high-school rows into observations, keep TJHSST former-PWCS rows as excluded snapshot counts, and do not infer zeros for PWCS-located private schools from PWCS public releases.
- Confidence: high

**2026-06-19 - Local-media NMSF overlap handling**
- Observation: Patch local NMSF articles can provide private-school rows absent from district releases, but their school lists may overlap public rows already covered by official FCPS sources.
- Action: Import only still-missing roster rows from local-media articles, keep overlapping public rows as excluded snapshot counts for source-total reconciliation, and do not use local-area articles for zero inference.
- Confidence: high

**2026-06-19 - Patch archive discovery**
- Observation: Patch site-wide or slug wildcard CDX searches may miss National Merit articles, while community-prefix CDX queries such as `patch.com/virginia/fairfaxcity/*` and `patch.com/virginia/mclean/*` expose archived local school articles for filtering.
- Action: For missing Patch/local-media NMSF rows, fetch community-prefix CDX indexes and filter locally for `national-merit`, `semifinalist`, and target school names before treating Patch coverage as absent.
- Confidence: medium

**2026-06-19 - Shared NMSF source-name compatibility**
- Observation: `scripts/apply_nmsf_counts.py` matches `nmsf_counts.csv` against `data/interim/canonical_schools.csv` aliases, while `scripts/build_nmsf_observations.py` can also use `data/manual/school_aliases.csv`; exact Patch names such as `Immanuel Christian School` can pass the observation layer but fail the legacy interim panel.
- Action: Use canonical-compatible school names in `data/sources/nmsf_counts.csv` when a source wording variant is absent from the interim roster aliases, and record the source wording variant in `data/manual/school_aliases.csv` or source snapshots instead.
- Confidence: high

**2026-06-19 - Patch headline/list mismatch**
- Observation: The Patch McLean Class 2026 article headline and body say 66 semifinalists, but the visible school-grouped list sums to 65 and does not expose a source-backed location for the missing student.
- Action: Reconcile Patch snapshots to the visible transcribed school-list total when the headline disagrees, document the discrepancy in manifest notes, and do not allocate the unlisted student to any school.
- Confidence: high

**2026-06-19 - Patch article parsing**
- Observation: Patch live article pages can expose the full article body in the embedded Next.js `__NEXT_DATA__.props.pageProps.mainContent.item.body` payload, including school-grouped NMSF lists.
- Action: Parse that embedded payload for local count transcription when available, but archive only count-level snapshots and omit student names from repo data.
- Confidence: high

**2026-06-19 - Patch topic feed discovery**
- Observation: Recent Patch school-topic pages expose article titles, dates, and canonical URLs in `__NEXT_DATA__.props.pageProps.mainContent.topicFeed`, and this surfaced 2026 Loudoun and Prince William/Manassas NMSF articles that community CDX indexes did not expose.
- Action: When Patch CDX or search is dry for recent NMSF gaps, fetch `/virginia/{community}/schools` and parse `topicFeed` before treating the source as absent.
- Confidence: high

**2026-06-19 - Patch topic pagination**
- Observation: Older Patch NMSF articles can be buried on paginated school-topic feeds such as `/virginia/mclean/schools?page=2` and `/virginia/mclean/schools?page=3`, while the first topic page only shows recent articles.
- Action: When using Patch topic feeds for older class years, walk the `?page=N` results far enough to cover the target publication month before concluding the article is absent.
- Confidence: high

**2026-06-19 - Patch locality-grouped articles**
- Observation: The Patch Loudoun and Prince William/Manassas Class 2026 articles grouped semifinalists by town/locality while individual list items carried the school attribution.
- Action: Count school-level observations from list-item school text when Patch headings are localities; do not treat locality headings as school rows.
- Confidence: high

**2026-06-19 - LCPS 2025 local attribution**
- Observation: The official LCPS Class 2025 release is total-only, but the Ashburn Patch Class 2025 article provides school-grouped positive Loudoun counts plus a nonroster Evergreen Christian row.
- Action: Use the Ashburn Patch source for positive LCPS Class 2025 roster observations, retain Evergreen only as an excluded snapshot row, and continue leaving absent LCPS schools missing rather than zero.
- Confidence: high

**2026-06-19 - LCPS pre-Apptegy archive discovery**
- Observation: LCPS official Class 2024 school-attributed NMSF coverage was not in the current Apptegy/Thrillshare API, but the Internet Archive `www.lcps.org/site/default.aspx` Blackboard index exposed it under `ModuleInstanceID=274904` and `FlexDataID=467748`.
- Action: For older LCPS official releases, filter archived Blackboard `site/default.aspx` rows by `PageType=3`, `DomainID=1`, `ModuleInstanceID=274904`, and first-capture windows around September before treating LCPS official coverage as absent.
- Confidence: high

**2026-06-19 - LCPS Blackboard list-page discovery**
- Observation: The archived LCPS `PageType=14` more-expanded Blackboard module list for `ModuleInstanceID=274904` exposed article titles/descriptions and revealed the Class 2023 NMSF `FlexDataID=441768` page when a narrower CDX wildcard query returned empty.
- Action: For older LCPS Blackboard NMSF searches, fetch a September `PageType=14` module list page and search its titles before downloading individual `PageType=3` article pages.
- Confidence: high

**2026-06-19 - Task 6 sequencing**
- Observation: Historical NMSF backfill beyond the official FCPS/TJHSST Classes 2019-2022 slice is optional robustness work, not a prerequisite for the analytical panel.
- Action: Start Milestone 7 from the current observation statuses and compatible coverage; leave non-FCPS historical gaps as missing unless a high-payoff source appears later.
- Confidence: high

**2026-06-19 - Historical FCPS NMSF backfill**
- Observation: The official FCPS Class 2022 NMSF article text says 214 semifinalists, but the visible school-grouped list sums to 215 while its TJHSST line still matches the stated TJHSST subtotal of 144.
- Action: For FCPS Class 2022, transcribe school counts from the visible named list, set the manifest reported total to the visible-list total, and keep the stated-total mismatch in source notes rather than forcing reconciliation to the article prose.
- Confidence: high

**2026-06-19 - Analysis panel pathway aggregates**
- Observation: `analysis_panel.csv` repeats pathway aggregate fields on each school row, but those aggregates are covered-subset totals based only on rows with both source-backed NMSF counts and grade-11 denominators.
- Action: In future descriptive tables or figures, check `pathway_coverage_status` and avoid treating `pathway_*_covered` fields as full-pathway totals unless the status is `complete_compatible_coverage`.
- Confidence: high

**2026-06-19 - Descriptive output aggregation**
- Observation: Task 8 summaries can have source-backed observed NMSF counts without compatible rate denominators, especially for private-school rows and historical coverage gaps.
- Action: Keep observed count totals separate from rate-compatible count/enrollment totals in future descriptive or robustness outputs; do not reuse observed count totals as normalized-rate numerators when denominators are missing.
- Confidence: high

**2026-06-20 - Targeted Class 2025 NMSF gaps**
- Observation: After complete-list integration, the remaining focal NMSF gaps are five Class 2025 public rows; the official LCPS release is total-only, known Patch/local articles remain positive-only, and targeted searches did not find school-attributed counts for Meridian, Loudoun Valley, Park View, Tuscarora, or Woodgrove.
- Action: Treat Class 2025 statewide packet recovery as optional future work; keep those rows `missing_source` unless a school-attributed count source or complete zero-inference scope appears.
- Confidence: high

**2026-06-19 - Task 9 handoff**
- Observation: Robustness and interpretation can be handed off from `data/processed/analysis_panel.csv`, `reports/descriptive_results.md`, `reports/tables/`, and coverage/provenance reports; raw source snapshots are only needed for provenance audit or source-row disputes.
- Action: For Task 9 drafting, provide the final panel, data dictionary, task/hypothesis framing, descriptive tables, final panel checks, NMSF reconciliation, and Regulation 3355.16; avoid substituting raw source archives for the generated coverage/status fields.
- Confidence: high

**2026-06-19 - Task 9 upload package**
- Observation: A ChatGPT Web handoff package is most usable when it preserves project-relative paths and includes a top-level README with the exact drafting prompt and interpretation guardrails.
- Action: Put future upload bundles under `handoff/`, include `README_TASK*_HANDOFF.md`, and zip the whole task folder rather than flattening CSV/report filenames.
- Confidence: high

**2026-06-19 - Task 9 integration**
- Observation: The web-completed Task 9 package included reproducible outputs plus package-only metadata; the durable repo artifacts are `scripts/build_task9_outputs.py`, `reports/robustness.md`, `reports/limitations.md`, `reports/initial_findings.md`, `reports/tables/task9_*.csv`, and Task 9 source notes.
- Action: Integrate completed task packages by copying repo-relative deliverables, regenerating outputs from the checked-in script, and deleting package metadata/folders after validation.
- Confidence: high

**2026-06-19 - Task 9 dependencies**
- Observation: `scripts/build_task9_outputs.py` uses `pandas` and `numpy`, which were not in the original project dependency list; syncing those dependencies also creates `uv.lock`.
- Action: Keep `pandas` and `numpy` declared in `pyproject.toml` and retain `uv.lock` so Task 9 regeneration works from a fresh environment.
- Confidence: high

**2026-06-20 - Private NMSF coverage audit**
- Observation: After integrating complete NMSC Virginia lists for Classes 2023, 2024, and 2026, all 16 private-school roster rows have source-backed focal-period NMSF counts or zeros, while private denominator coverage remains unavailable for Classes 2024 and 2026.
- Action: Treat focal private-school count coverage as complete, but keep private offset claims unresolved unless denominator, residence/eligibility, and counterfactual-placement evidence are added.
- Confidence: high

**2026-06-19 - ProPublica private-school demographics source**
- Observation: ProPublica's private-school demographics app is a derivative 2021-22 PSS-based presentation and notes exclusions/nonresponse; it does not expose the project-required `P290` grade-11 denominator workflow.
- Action: Use it only for discovery or context, not as the canonical private-school enrollment source; ingest denominators from official NCES PSS public-use files by curated `PPIN`.
- Confidence: high

**2026-06-19 - Milestone 10 denominator cleanup**
- Observation: The NCES CCD file-tool API exposes school membership ZIP URLs for Classes 2023-2025, but the 2021-22 membership download nests a `*_CSV.zip` whose CSV may require the system `unzip -p` fallback.
- Action: Use `scripts/ingest_public_enrollment_nces_supplement.py` for targeted exact-NCES-ID public denominator backfills, and keep the nested-CSV streaming fallback in `enrollment.py`.
- Confidence: high

**2026-06-19 - PSS 2023-24 availability**
- Observation: The official NCES PSS data page stated that 2023-24 data were being finalized and did not list a public-use CSV download on 2026-06-19; the guessed `pss2324_pu_csv.zip` URL returned 404.
- Action: Leave Class 2025 private-school PSS denominators open until NCES lists the official 2023-24 public-use file; do not use guessed filenames or secondary copies.
- Confidence: high

**2026-06-19 - PSS 2023-24 locator route**
- Observation: The NCES Private School Search locator is backed by 2023-24 PSS data and its file layout exposes `PSS_ENROLL_11` for eleventh-grade enrollment, but the locator layout does not expose `F_P290` or other imputation flags. The linked `State=47` URL is Tennessee, not Virginia.
- Action: Treat the locator as a possible official interim source for Class 2025 private denominators only after archiving detail/download evidence, curating current school IDs or name matches, mapping `PSS_ENROLL_11` to the grade-11 denominator, and recording imputation flags as unavailable; still prefer the official public-use ZIP when NCES posts it.
- Confidence: high

**2026-06-19 - PSS 2023-24 Virginia grade-11 locator**
- Observation: The NCES locator query `State=51&IncGrade=12` returns 262 Virginia private schools and includes grade spans ending in 11, so `IncGrade=12` is the locator's internal grade-11 filter rather than a twelfth-grade-only filter.
- Action: Use that query as the candidate universe for Class 2025 private denominator matching, but extract denominators from the locator download/detail `PSS_ENROLL_11` field rather than from the visible search-result `Students` total.
- Confidence: high

**2026-06-19 - NMSC semifinalist press releases**
- Observation: The archived NMSC `23_meritsemi.pdf` through `26_meritsemi.pdf` files are official annual press releases, but they state that named Semifinalist lists were distributed to media and are not posted on the NMSC website.
- Action: Archive these PDFs only as source-discovery evidence; continue searching for complete public media mirrors before creating Virginia-list counts, zeros, or statewide-share metrics.
- Confidence: high

**2026-06-19 - Milestone 10 complete-list search**
- Observation: A broad public-source sweep did not locate complete Virginia school-by-school NMSF mirrors, but user-supplied NMSC Virginia media lists later resolved Classes 2023, 2024, and 2026; Class 2025 remains the only focal complete-list gap.
- Action: Keep the search attempts in `reports/data_quality/focal_period_completion.md` as Class 2025 limitation evidence, and use `scripts/ingest_nmsc_virginia_lists.py` plus count-only snapshots for the supplied complete-list years.
- Confidence: high

**2026-06-20 - PSS locator denominator ingestion**
- Observation: The archived NCES 2023-24 Private School Search locator detail pages resolved 10 of 16 rostered private Class 2025 grade-11 denominators; BASIS Independent McLean, Flint Hill, Oakcrest, Potomac, and Seton returned no current locator row, and Loudoun School for Advanced Studies returned two same-address candidates. Locator detail pages expose `PSS_ENROLL_11` but not `F_P290`.
- Action: Use `scripts/ingest_private_pss_locator_2023_24.py` against archived locator HTML for interim Class 2025 private denominators, keep unresolved locator rows blank, and replace or reconcile this supplement when the official 2023-24 public-use PSS ZIP is posted.
- Confidence: high

**2026-06-20 - NMSC Virginia complete-list ingestion**
- Observation: User-supplied NMSC Virginia media-list PDFs for Classes 2023, 2024, and 2026 parse into complete count-only snapshots with statewide totals of 400, 470, and 494; the PDFs include student names, while the snapshots omit them.
- Action: Keep source PDFs only in the ignored `data/raw/nmsf/virginia/supplied_lists/` local directory, commit the count-only snapshots and `data/sources/virginia_statewide_totals.csv`, and leave Class 2025 unresolved until an equivalent complete list is found.
- Confidence: high

**2026-06-20 - Task 10 rerun handoff**
- Observation: The Milestone 10 Web rerun package needs the `src/tj_psat_analysis/` package as well as the scripts, because the rebuild scripts import local package modules; raw supplied NMSC PDFs are unnecessary when count-only snapshots and source manifests are included.
- Action: For future rerun handoffs, include `src/`, selected scripts, processed panels, source manifests, count-only snapshots, and key reports under repo-relative paths, but exclude raw supplied-list PDFs and student-name files.
- Confidence: high

**2026-06-22 - Full rebuild reproducibility audit**
- Observation: A clean full-pipeline rebuild exposed a stale committed `data/interim/panel_nmsf.csv`, four source-name aliases that were present only in the generated CSV rather than roster code, and tied Task 9 rankings whose row order depended on pandas sort behavior.
- Action: Regenerate the interim panel after every count-source update, keep source-specific aliases in `SOURCE_ALIASES_BY_SCHOOL_ID`, and use explicit secondary sort keys plus stable sorting for committed analytical tables.
- Confidence: high

**2026-06-22 - Raw versus enrollment-standardized offset**
- Observation: Pooling Classes 2023-2024 against 2025-2026, raw base-school gains offset about 65% of TJHSST's count decline, but applying prior group-specific rates to actual post-period enrollment reduces the offset to about 37% and leaves a material combined-public shortfall.
- Action: Report the raw decomposition only as a generous arithmetic upper view and pair it with `task9_rate_standardized_offset_decomposition.csv`; do not describe the raw 65% figure as measured student redistribution.
- Confidence: high

**2026-06-22 - Branch merge workflow**
- Observation: Merging `analysis-refresh-2026-06-22` into `main` was a clean fast-forward to `a5ea42a`, leaving local `main` ahead of `origin/main` until an explicit push.
- Action: For future merge-only requests in this repo, verify the worktree is clean, fast-forward when possible, and do not push `origin/main` unless the user asks.
- Confidence: high

**2026-06-22 - Documentation cleanup and generated reports**
- Observation: Task 9 conclusions, source caveats, and completion summaries are partly generated from `scripts/build_task9_outputs.py`, while descriptive and data-quality wording comes from package modules.
- Action: Update generator-owned report wording before regenerating reports, and keep static docs such as `README.md` and `TASKS.md` as concise status summaries rather than duplicating computed numeric claims.
- Confidence: high

## What Has Failed

**2026-06-19 - CI formatting check**
- Observation: CI runs `python -m ruff format --check .`, and unittest plus `git diff --check` can pass while Ruff still wants formatting changes.
- Action: Run `UV_CACHE_DIR=.uv-cache uv run --no-sync python -m ruff format --check .` before publishing, or run Ruff format on touched Python files after edits.
- Confidence: high

**2026-06-19 - CI type check**
- Observation: CI runs `python -m mypy`, and formatting, lint, and unittest checks can pass while mypy still catches type-inference issues.
- Action: Include `UV_CACHE_DIR=.uv-cache uv run --no-sync python -m mypy` in pre-push verification for source changes.
- Confidence: high

**2026-06-22 - CI mypy target**
- Observation: Fresh CI installs can resolve NumPy stubs that use Python 3.12 `type` statement syntax, while `pyproject.toml` previously configured mypy with `python_version = "3.10"` despite CI running Python 3.12.
- Action: Keep `[tool.mypy].python_version` aligned with the GitHub Actions Python runner unless dependency pins are tightened to stubs compatible with an older type-check target.
- Confidence: high

**2026-06-22 - NMSC Virginia statewide total cross-check**
- Observation: The public 2026 NMSC Guide lists Virginia with 489 semifinalists, while the current supplied-list snapshot/parser totals 494 name-like Class 2026 Virginia lines and carries 494 into statewide-share tables.
- Action: Reconcile supplied-list totals against the NMSC Guide table before treating statewide-normalized shares as final; do not let the discrepancy affect school-level local conclusions without checking whether any rostered school counts are implicated.
- Confidence: medium
