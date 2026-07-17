# Focal-Period Completion Report

Generated from the current focal-period observation layer, archived NMSC press-release source artifacts, and count-only complete Virginia list snapshots where available. Statewide totals are reported separately for Virginia-location media lists and official NMSC Virginia selection units.

## Current Observation Coverage

| Status | Rows |
| --- | --- |
| missing_source | 1 |
| verified_count | 201 |
| verified_zero | 102 |

## Remaining Missing Source Rows

| Class | Division | Sector | Missing Rows |
| --- | --- | --- | --- |
| 2025 | Falls Church City | public | 1 |

| Class | Division | School | Sector | Pathway |
| --- | --- | --- | --- | --- |
| 2025 | Falls Church City | Meridian High School | public | Falls Church City |

## NMSC Virginia List Integration

User-supplied NMSC media packets expose complete Virginia school-by-school lists for Classes 2023, 2024, and 2026. The repo archives count-only snapshots that omit student names, imports only still-missing positive roster rows from those lists, and uses the complete Virginia scope to infer verified zeros for absent operating roster schools in those class years. These packets are location lists: their totals include Semifinalists grouped under Virginia-located schools, including students who may belong to NMSC's separate U.S. boarding-school selection unit. NMSC's guides report the Virginia state selection unit separately. Class 2025 lacks a source-backed total in either scope, so statewide-share metrics remain blank there; the remaining row-level gaps are handled individually below.

| Class | Virginia-Location Media-List Total | Official NMSC Virginia Selection-Unit Total | Location Source ID | Location Snapshot | Location SHA-256 | Official Guide Source | Official Guide Date | Official Guide SHA-256 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023 | 400 | 397 | nmsc_virginia_2023_semifinalists | data/raw/nmsf/virginia/virginia_2023_semifinalists_snapshot.csv | 1be00a4b986afdf51107ff29e3218305fcf270e31ca2bfc11b5b730d095a52ea | [Guide to the National Merit Scholarship Program - 2023 Program](https://web.archive.org/web/20230127104949id_/https://www.nationalmerit.org/s/1758/images/gid2/editor_documents/guide_to_the_national_merit_scholarship_program.pdf) | 2023-01-27 | b546bd206187309c099ca6157144563993c881ac94fc4717296c9a59fa0937ba |
| 2024 | 470 | 467 | nmsc_virginia_2024_semifinalists | data/raw/nmsf/virginia/virginia_2024_semifinalists_snapshot.csv | ed46b323666d6e2365a552b57526b80456a6cd2cbee990d748de3299a8e2a774 | [Guide to the National Merit Scholarship Program - 2024 Program](https://web.archive.org/web/20231024130754id_/https://www.nationalmerit.org/s/1758/images/gid2/editor_documents/guide_to_the_national_merit_scholarship_program.pdf) | 2023-10-24 | be3dfdd3e8349eb73a12504a73613e3e68243a0a7cc7044e0789ba8e6abfa032 |
| 2025 | not sourced | not sourced |  |  |  |  |  |  |
| 2026 | 494 | 489 | nmsc_virginia_2026_semifinalists | data/raw/nmsf/virginia/virginia_2026_semifinalists_snapshot.csv | 84b7384aa4beb85c315bc2f1ea21aec6d09f0aed4d6f96d2a4017298737863dc | [Guide to the National Merit Scholarship Program - 2026 Program](https://www.nationalmerit.org/s/1758/images/gid2/editor_documents/guide_to_the_national_merit_scholarship_program.pdf?cc=1&gid=2&pgid=61) | 2025-09-10 | f1beb4d304e1c27e33be2441fa186a59f1e4b8732d4b96ebed648b21e6e04423 |

Statewide scope rule: use the Virginia-location media-list totals (400, 470, and 494) only with location-scoped numerators. Use the official NMSC Virginia selection-unit totals (397, 467, and 489) only with numerators that exclude students assigned to other NMSC selection units. These are different scopes, not competing estimates. Do not substitute an official selection-unit denominator beneath an unadjusted location-list numerator. No source-backed statewide denominator is available for Class 2025 in either scope.

## Targeted Class 2025 Row Search

Five public Class 2025 rows were targeted directly after the 2023, 2024, and 2026 complete-list integration. Exact identity-level reconciliation closes the four LCPS rows as verified zeros without allocating the unattributed district total: 42 directly school-attributed LCPS-public identities plus 15 official TJHSST identities exhaust the official 57-name LCPS release. Meridian remains missing because the available graduation report counts finalists rather than semifinalists and the deleted statewide gallery's image bytes could not be recovered. A full Class 2025 statewide packet would still improve supplemental statewide-share metrics.

| Class | Division | School | Sources Checked | Result | Action |
| --- | --- | --- | --- | --- | --- |
| 2025 | Falls Church City | Meridian High School | NMSC 2025 press release; FCCPS/Meridian Apptegy news, live-feed, and search surfaces; Falls Church News-Press graduation report (https://www.fcnp.com/2025/05/28/meridian-graduation-noonans-farewell/); Patch Falls Church/Fairfax City checks; FCCPS/Meridian/Patch CDX checks; deleted Reddit Virginia-gallery metadata and archive checks | No source-backed Meridian semifinalist count was found. A Falls Church News-Press graduation report gives four finalists, which cannot establish the semifinalist count; the deleted statewide gallery's image bytes remain unavailable. | Retain as `missing_source`; no zero inference. |
| 2025 | LCPS | Loudoun Valley High School | NMSC 2025 press release; official LCPS 57-student total-only release; Ashburn Patch school-grouped article; official FCPS TJHSST list; U.S. Education candidate list for one spelling check; LCPS school sites/APIs; LCPS, Patch, Loudoun Now, and Loudoun Times targeted web/CDX checks | Verified zero: the official 57-name LCPS list reconciles exhaustively to 42 Patch-attributed LCPS-public identities plus 15 official TJHSST identities. | Record `verified_zero` from `lcps_2025_named_list_reconciliation`. |
| 2025 | LCPS | Park View High School | NMSC 2025 press release; official LCPS 57-student total-only release; Ashburn Patch school-grouped article; official FCPS TJHSST list; U.S. Education candidate list for one spelling check; LCPS school sites/APIs; LCPS, Patch, Loudoun Now, and Loudoun Times targeted web/CDX checks | Verified zero: the official 57-name LCPS list reconciles exhaustively to 42 Patch-attributed LCPS-public identities plus 15 official TJHSST identities. | Record `verified_zero` from `lcps_2025_named_list_reconciliation`. |
| 2025 | LCPS | Tuscarora High School | NMSC 2025 press release; official LCPS 57-student total-only release; Ashburn Patch school-grouped article; official FCPS TJHSST list; U.S. Education candidate list for one spelling check; LCPS school sites/APIs; LCPS, Patch, Loudoun Now, and Loudoun Times targeted web/CDX checks | Verified zero: the official 57-name LCPS list reconciles exhaustively to 42 Patch-attributed LCPS-public identities plus 15 official TJHSST identities. | Record `verified_zero` from `lcps_2025_named_list_reconciliation`. |
| 2025 | LCPS | Woodgrove High School | NMSC 2025 press release; official LCPS 57-student total-only release; Ashburn Patch school-grouped article; official FCPS TJHSST list; U.S. Education candidate list for one spelling check; LCPS school sites/APIs; LCPS, Patch, Loudoun Now, and Loudoun Times targeted web/CDX checks | Verified zero: the official 57-name LCPS list reconciles exhaustively to 42 Patch-attributed LCPS-public identities plus 15 official TJHSST identities. | Record `verified_zero` from `lcps_2025_named_list_reconciliation`. |

## NMSC Press-Release Audit

The archived NMSC PDFs are official press releases, not school-by-school or Virginia-list source tables. Visual inspection confirmed that the releases describe the annual program and state that the named Semifinalist list was distributed to news media but is not posted on the NMSC website. Because these PDFs do not identify Virginia schools or students, this pass does not create `verified_count`, `verified_zero`, or Virginia-share rows from them.

| Class | Date | Archived File | SHA-256 | Finding |
| --- | --- | --- | --- | --- |
| 2023 | 2022-09-14 | data/raw/nmsf/virginia/nmsc_2023_semifinalist_press_release.pdf | 61f19101190b89a1910bf06c005952e7e394538817add727426fd6c5757c7040 | Official press release only; no school-by-school list. |
| 2024 | 2023-09-13 | data/raw/nmsf/virginia/nmsc_2024_semifinalist_press_release.pdf | e1c36aa0a430b3b77ffdf6ec57a9863d913863fd508990ba8cbe4e0fe5b06bd8 | Official press release only; no school-by-school list. |
| 2025 | 2024-09-11 | data/raw/nmsf/virginia/nmsc_2025_semifinalist_press_release.pdf | ae3d9dfed1fb0a38643375312e2d42cf9b68d81b7ee110a38568f2645c73d54f | Official press release only; no school-by-school list. |
| 2026 | 2025-09-10 | data/raw/nmsf/virginia/nmsc_2026_semifinalist_press_release.pdf | f3f6eace78866181724dd003975113b56ec0594476a013ae89b1efd73a7527d4 | Official press release only; no school-by-school list. |

## Broad Source-Discovery Log

Public-source sweeps looked for complete Virginia school-by-school lists or authoritative mirrors for Classes 2023-2026. The latest pass recovered the deleted Class 2025 Reddit gallery's metadata and archived shell but not its image bytes. Separately, exact LCPS name-set reconciliation establishes the four LCPS zeros; archive or search absence alone does not establish any zero.

| Workflow | Query Or Source | Result | Finding | Action |
| --- | --- | --- | --- | --- |
| Internet Archive CDX | NMSC editor-document PDF index, focal window 2022-09 through 2025-09 (`www.nationalmerit.org/s/1758/images/gid2/editor_documents/*`) | Returned annual press releases, scholarship-recipient PDFs, annual reports, and guide PDFs; the focal semifinalist artifacts were `23_meritsemi.pdf` through `26_meritsemi.pdf`. | No state-list or Virginia-list filename was exposed in the NMSC PDF index. | Retain the archived press releases as discovery evidence only; do not create counts or zeros. |
| Internet Archive CDX | NMSC broad semifinalist URL wildcard (`www.nationalmerit.org/*national*merit*semifinal*`) | Returned an empty CDX result for the focal window. | No alternate NMSC-hosted complete-list URL was found. | Treat complete Class 2025 Virginia list recovery as optional future work; do not make it a prerequisite for closing the focal-period cleanup. |
| Public web search | Class-year phrase searches for `National Merit Semifinalists Virginia` and `National Merit Scholarship Semifinalists Virginia`, Classes 2023-2026 | Did not surface a complete statewide school-by-school list; visible results were irrelevant, school pages, or local/school-area articles already handled as incomplete sources. | No complete public Virginia mirror was located through broad web search. | Do not change Class 2025 observations from search absence; keep remaining rows `missing_source`. |
| Common Crawl URL index | Wildcard URL probes including `*national*merit*semifinal*virginia*` and `*national-merit-semifinalists*virginia*` in 2023-2025 indexes | Returned no captures for the tested URL patterns. | No broad web-crawl URL evidence of a public Virginia list mirror was found. | Use this only as search-limitation evidence, not as evidence of zero semifinalists. |
| Internet Archive CDX | Major Virginia/DC media URL patterns under Richmond Times-Dispatch, Roanoke Times, Daily Press, The Virginian-Pilot, Daily Progress, News & Advance, AP, WTOP, InsideNoVa, and FFXnow | Responsive domain patterns returned empty result sets; the Fredericksburg.com wildcard timed out rather than producing usable candidates. | No complete statewide media mirror was found in these broad media-domain URL indexes. | Document the limitation and avoid continuing lower-yield school-by-school scraping. |
| Internet Archive CDX | Patch Virginia URL patterns (`patch.com/virginia/*national-merit*` variants) | The broad archive URL patterns returned empty, while the project already has relevant Patch articles discovered through community topic feeds and local searches. | Patch coverage remains local or school-area coverage, not a complete Virginia list. | Keep Patch-derived rows positive-only; never use Patch absence for zero inference. |
| Reddit metadata APIs plus Internet Archive and Common Crawl | Deleted r/psat gallery post `1fekyi6` (`2025 NMSF Virginia`) with recovered media IDs `1xu2738au8od1`, `nwinp3feu8od1`, and `ynlabcqhu8od1`; corrected first-page post `1femf90` with media ID `wdipgaas59od1` | The archived shell preserves three page-image URLs, but the Reddit CDN objects now return 404 and neither Internet Archive nor Common Crawl has recoverable image bytes. | The strongest statewide-list lead is identifiable but its school-list images are unavailable. | Retain the media IDs as a future recovery lead; do not create counts or zeros from the deleted-gallery shell. |
| Identity-level source reconciliation | Official LCPS 57-name release against Patch's school-attributed Loudoun list and FCPS's official TJHSST list, with one spelling variant checked against a U.S. Education list | All 57 distinct LCPS identities partition exactly into 42 Patch-attributed LCPS-public students and 15 students on the official TJHSST list. | The school-attributed LCPS-public partition is exhaustive without allocating the district total or assigning TJHSST residents to base schools. | Use the archived count-only reconciliation to verify zero for the four absent operating LCPS roster schools; keep Patch alone incomplete for zero inference. |

## Source-Discovery Decision

- Do not add the NMSC press-release-only PDFs to `data/sources/source_manifest.yml` as numeric count sources because they do not provide school-level Virginia counts.
- Use the supplied complete NMSC Virginia lists for Classes 2023, 2024, and 2026 as source-backed count, zero-inference, and Virginia-location-total sources; do not label their totals as official Virginia selection-unit totals.
- Preserve the official NMSC Virginia selection-unit totals of 397, 467, and 489 as a separate statewide scope and require scope-matched numerators before calculating shares.
- Do not infer zeros for missing public or private rows from these press releases.
- Treat recovery of the deleted Class 2025 Virginia gallery images or another complete statewide list as useful future work for Meridian and statewide-share metrics.
- Use `lcps_2025_named_list_reconciliation` for the four Class 2025 LCPS verified zeros; the source exhausts the official named population and keeps TJHSST as one row.
- Retain Meridian High School Class 2025 as `missing_source`; four reported finalists do not establish the semifinalist count.
- Publish Virginia statewide-share metrics only when both numerator and denominator use the same documented scope; leave Class 2025 shares blank until a source-backed statewide total is added.
