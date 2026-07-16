# Focal-Period Completion Report

Generated from the current focal-period observation layer, archived NMSC press-release source artifacts, and count-only complete Virginia list snapshots where available.

## Current Observation Coverage

| Status | Rows |
| --- | --- |
| missing_source | 5 |
| verified_count | 199 |
| verified_zero | 100 |

## Remaining Missing Source Rows

| Class | Division | Sector | Missing Rows |
| --- | --- | --- | --- |
| 2025 | Falls Church City | public | 1 |
| 2025 | LCPS | public | 4 |

| Class | Division | School | Sector | Pathway |
| --- | --- | --- | --- | --- |
| 2025 | Falls Church City | Meridian High School | public | Falls Church City |
| 2025 | LCPS | Loudoun Valley High School | public | Loudoun |
| 2025 | LCPS | Park View High School | public | Loudoun |
| 2025 | LCPS | Tuscarora High School | public | Loudoun |
| 2025 | LCPS | Woodgrove High School | public | Loudoun |

## NMSC Virginia List Integration

User-supplied NMSC media packets expose complete Virginia school-by-school lists for Classes 2023, 2024, and 2026. The repo archives count-only snapshots that omit student names, imports only still-missing positive roster rows from those lists, and uses the complete Virginia scope to infer verified zeros for absent operating roster schools in those class years. Class 2025 lacks a comparable complete list, so statewide-share metrics remain blank there; the remaining row-level gaps are handled individually below.

| Class | Source ID | Statewide Total | Snapshot | SHA-256 |
| --- | --- | --- | --- | --- |
| 2023 | nmsc_virginia_2023_semifinalists | 400 | data/raw/nmsf/virginia/virginia_2023_semifinalists_snapshot.csv | 390c4de436745814d47db4905b197a9d476d73116c7de765039100ea6f3b85cf |
| 2024 | nmsc_virginia_2024_semifinalists | 470 | data/raw/nmsf/virginia/virginia_2024_semifinalists_snapshot.csv | 9bf0580a9cc7fc5a3d661606e0895e1d454395b3e340df0be81f6bd0e816d5d8 |
| 2026 | nmsc_virginia_2026_semifinalists | 494 | data/raw/nmsf/virginia/virginia_2026_semifinalists_snapshot.csv | 84b7384aa4beb85c315bc2f1ea21aec6d09f0aed4d6f96d2a4017298737863dc |

Statewide-share caveat: the Class 2026 supplied-list snapshot totals 494, while the public NMSC 2026 guide cross-check lists Virginia at 489 semifinalists. This does not change local school counts or zero-inference coverage, but 2026 statewide-share denominators should be reconciled before final use.

## Targeted Class 2025 Row Search

The remaining focal-period gaps are five public Class 2025 rows. Each was targeted directly after the 2023, 2024, and 2026 complete-list integration. None has a source-backed positive count, and none has a complete source scope that can support a verified zero. Recovering the full Class 2025 statewide packet would improve supplemental statewide-share metrics, but it is not required to close this public-source cleanup pass.

| Class | Division | School | Sources Checked | Result | Action |
| --- | --- | --- | --- | --- | --- |
| 2025 | Falls Church City | Meridian High School | NMSC 2025 press release; FCCPS/Meridian Apptegy news, live-feed, and search surfaces; Falls Church News-Press issue-week checks; Patch Falls Church/Fairfax City checks; FCCPS/Meridian/Patch CDX checks | No Meridian school-level count and no complete Class 2025 Virginia list were found. | Retain as `missing_source`; no zero inference. |
| 2025 | LCPS | Loudoun Valley High School | NMSC 2025 press release; official LCPS 57-student total-only release; Ashburn Patch positive school-grouped article; LCPS school sites/APIs; LCPS, Patch, Loudoun Now, and Loudoun Times targeted web/CDX checks | No school-level count found; LCPS total-only coverage and Patch omission cannot support zero inference. | Retain as `missing_source`; no zero inference. |
| 2025 | LCPS | Park View High School | NMSC 2025 press release; official LCPS 57-student total-only release; Ashburn Patch positive school-grouped article; LCPS school sites/APIs; LCPS, Patch, Loudoun Now, and Loudoun Times targeted web/CDX checks | No school-level count found; LCPS total-only coverage and Patch omission cannot support zero inference. | Retain as `missing_source`; no zero inference. |
| 2025 | LCPS | Tuscarora High School | NMSC 2025 press release; official LCPS 57-student total-only release; Ashburn Patch positive school-grouped article; LCPS school sites/APIs; LCPS, Patch, Loudoun Now, and Loudoun Times targeted web/CDX checks | No school-level count found; LCPS total-only coverage and Patch omission cannot support zero inference. | Retain as `missing_source`; no zero inference. |
| 2025 | LCPS | Woodgrove High School | NMSC 2025 press release; official LCPS 57-student total-only release; Ashburn Patch positive school-grouped article; LCPS school sites/APIs; LCPS, Patch, Loudoun Now, and Loudoun Times targeted web/CDX checks | No school-level count found; LCPS total-only coverage and Patch omission cannot support zero inference. | Retain as `missing_source`; no zero inference. |

## NMSC Press-Release Audit

The archived NMSC PDFs are official press releases, not school-by-school or Virginia-list source tables. Visual inspection confirmed that the releases describe the annual program and state that the named Semifinalist list was distributed to news media but is not posted on the NMSC website. Because these PDFs do not identify Virginia schools or students, this pass does not create `verified_count`, `verified_zero`, or Virginia-share rows from them.

| Class | Date | Archived File | SHA-256 | Finding |
| --- | --- | --- | --- | --- |
| 2023 | 2022-09-14 | data/raw/nmsf/virginia/nmsc_2023_semifinalist_press_release.pdf | 61f19101190b89a1910bf06c005952e7e394538817add727426fd6c5757c7040 | Official press release only; no school-by-school list. |
| 2024 | 2023-09-13 | data/raw/nmsf/virginia/nmsc_2024_semifinalist_press_release.pdf | e1c36aa0a430b3b77ffdf6ec57a9863d913863fd508990ba8cbe4e0fe5b06bd8 | Official press release only; no school-by-school list. |
| 2025 | 2024-09-11 | data/raw/nmsf/virginia/nmsc_2025_semifinalist_press_release.pdf | ae3d9dfed1fb0a38643375312e2d42cf9b68d81b7ee110a38568f2645c73d54f | Official press release only; no school-by-school list. |
| 2026 | 2025-09-10 | data/raw/nmsf/virginia/nmsc_2026_semifinalist_press_release.pdf | f3f6eace78866181724dd003975113b56ec0594476a013ae89b1efd73a7527d4 | Official press release only; no school-by-school list. |

## Broad Source-Discovery Log

An earlier public-source sweep looked for complete Virginia school-by-school lists or authoritative mirrors for Classes 2023-2026. It did not locate the now-supplied 2023, 2024, and 2026 list files, and it remains useful limitation evidence for the unsourced Class 2025 statewide list/total. These searches do not establish zeros for missing schools.

| Workflow | Query Or Source | Result | Finding | Action |
| --- | --- | --- | --- | --- |
| Internet Archive CDX | NMSC editor-document PDF index, focal window 2022-09 through 2025-09 (`www.nationalmerit.org/s/1758/images/gid2/editor_documents/*`) | Returned annual press releases, scholarship-recipient PDFs, annual reports, and guide PDFs; the focal semifinalist artifacts were `23_meritsemi.pdf` through `26_meritsemi.pdf`. | No state-list or Virginia-list filename was exposed in the NMSC PDF index. | Retain the archived press releases as discovery evidence only; do not create counts or zeros. |
| Internet Archive CDX | NMSC broad semifinalist URL wildcard (`www.nationalmerit.org/*national*merit*semifinal*`) | Returned an empty CDX result for the focal window. | No alternate NMSC-hosted complete-list URL was found. | Treat complete Class 2025 Virginia list recovery as optional future work; do not make it a prerequisite for closing the focal-period cleanup. |
| Public web search | Class-year phrase searches for `National Merit Semifinalists Virginia` and `National Merit Scholarship Semifinalists Virginia`, Classes 2023-2026 | Did not surface a complete statewide school-by-school list; visible results were irrelevant, school pages, or local/school-area articles already handled as incomplete sources. | No complete public Virginia mirror was located through broad web search. | Do not change Class 2025 observations from search absence; keep remaining rows `missing_source`. |
| Common Crawl URL index | Wildcard URL probes including `*national*merit*semifinal*virginia*` and `*national-merit-semifinalists*virginia*` in 2023-2025 indexes | Returned no captures for the tested URL patterns. | No broad web-crawl URL evidence of a public Virginia list mirror was found. | Use this only as search-limitation evidence, not as evidence of zero semifinalists. |
| Internet Archive CDX | Major Virginia/DC media URL patterns under Richmond Times-Dispatch, Roanoke Times, Daily Press, The Virginian-Pilot, Daily Progress, News & Advance, AP, WTOP, InsideNoVa, and FFXnow | Responsive domain patterns returned empty result sets; the Fredericksburg.com wildcard timed out rather than producing usable candidates. | No complete statewide media mirror was found in these broad media-domain URL indexes. | Document the limitation and avoid continuing lower-yield school-by-school scraping. |
| Internet Archive CDX | Patch Virginia URL patterns (`patch.com/virginia/*national-merit*` variants) | The broad archive URL patterns returned empty, while the project already has relevant Patch articles discovered through community topic feeds and local searches. | Patch coverage remains local or school-area coverage, not a complete Virginia list. | Keep Patch-derived rows positive-only; never use Patch absence for zero inference. |

## Source-Discovery Decision

- Do not add the NMSC press-release-only PDFs to `data/sources/source_manifest.yml` as numeric count sources because they do not provide school-level Virginia counts.
- Use the supplied complete NMSC Virginia lists for Classes 2023, 2024, and 2026 as source-backed count, zero-inference, and statewide-total sources.
- Do not infer zeros for missing public or private rows from these press releases.
- Treat a complete Class 2025 Virginia school-by-school list as optional future work, not a prerequisite for closing the public-source cleanup pass.
- Retain the five targeted Class 2025 rows as `missing_source` unless a school-attributed count source or complete zero-inference scope appears.
- Publish Virginia statewide-share metrics for source-backed complete-list years only; leave Class 2025 shares blank until a source-backed statewide total is added.
