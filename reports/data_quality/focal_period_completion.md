# Focal-Period Completion Report

Generated for Milestone 10 from the current focal-period observation layer and archived NMSC press-release source artifacts.

## Current Observation Coverage

| Status | Rows |
| --- | --- |
| missing_source | 37 |
| verified_count | 189 |
| verified_zero | 78 |

## Remaining Missing Source Rows

| Class | Division | Sector | Missing Rows |
| --- | --- | --- | --- |
| 2023 | FCPS | private | 8 |
| 2023 | Falls Church City | public | 1 |
| 2023 | LCPS | private | 2 |
| 2023 | PWCS | private | 2 |
| 2024 | APS | public | 1 |
| 2024 | FCPS | private | 7 |
| 2024 | LCPS | private | 2 |
| 2024 | PWCS | private | 2 |
| 2025 | Falls Church City | public | 1 |
| 2025 | LCPS | public | 4 |
| 2026 | FCPS | private | 4 |
| 2026 | Falls Church City | public | 1 |
| 2026 | LCPS | private | 1 |
| 2026 | PWCS | private | 1 |

| Class | Division | School | Sector | Pathway |
| --- | --- | --- | --- | --- |
| 2024 | APS | Wakefield High School | public | Arlington |
| 2023 | Falls Church City | Meridian High School | public | Falls Church City |
| 2025 | Falls Church City | Meridian High School | public | Falls Church City |
| 2026 | Falls Church City | Meridian High School | public | Falls Church City |
| 2025 | LCPS | Loudoun Valley High School | public | Loudoun |
| 2025 | LCPS | Park View High School | public | Loudoun |
| 2025 | LCPS | Tuscarora High School | public | Loudoun |
| 2025 | LCPS | Woodgrove High School | public | Loudoun |
| 2023 | FCPS | BASIS Independent McLean | private | Private/homeschool unallocated |
| 2023 | FCPS | Oakcrest School | private | Private/homeschool unallocated |
| 2024 | FCPS | Oakcrest School | private | Private/homeschool unallocated |
| 2023 | FCPS | Trinity Christian School | private | Private/homeschool unallocated |
| 2024 | FCPS | Trinity Christian School | private | Private/homeschool unallocated |
| 2023 | FCPS | Trinity School at Meadow View | private | Private/homeschool unallocated |
| 2024 | FCPS | Trinity School at Meadow View | private | Private/homeschool unallocated |
| 2026 | FCPS | Trinity School at Meadow View | private | Private/homeschool unallocated |
| 2023 | FCPS | Immanuel Christian High School | private | Private/homeschool unallocated |
| 2024 | FCPS | Immanuel Christian High School | private | Private/homeschool unallocated |
| 2026 | FCPS | Immanuel Christian High School | private | Private/homeschool unallocated |
| 2023 | FCPS | Ideaventions Academy for Mathematics & Science | private | Private/homeschool unallocated |
| 2024 | FCPS | Ideaventions Academy for Mathematics & Science | private | Private/homeschool unallocated |
| 2026 | FCPS | Ideaventions Academy for Mathematics & Science | private | Private/homeschool unallocated |
| 2023 | FCPS | New School of Northern Virginia | private | Private/homeschool unallocated |
| 2024 | FCPS | New School of Northern Virginia | private | Private/homeschool unallocated |
| 2023 | FCPS | Pinnacle Academy | private | Private/homeschool unallocated |
| 2024 | FCPS | Pinnacle Academy | private | Private/homeschool unallocated |
| 2026 | FCPS | Pinnacle Academy | private | Private/homeschool unallocated |
| 2023 | LCPS | Loudoun School for Advanced Studies | private | Private/homeschool unallocated |
| 2024 | LCPS | Loudoun School for Advanced Studies | private | Private/homeschool unallocated |
| 2026 | LCPS | Loudoun School for Advanced Studies | private | Private/homeschool unallocated |
| 2023 | LCPS | St. Paul VI Catholic High School | private | Private/homeschool unallocated |
| 2024 | LCPS | St. Paul VI Catholic High School | private | Private/homeschool unallocated |
| 2023 | PWCS | Seton School (Manassas) | private | Private/homeschool unallocated |
| 2024 | PWCS | Seton School (Manassas) | private | Private/homeschool unallocated |
| 2026 | PWCS | Seton School (Manassas) | private | Private/homeschool unallocated |
| 2023 | PWCS | St. John Paul the Great Catholic High School | private | Private/homeschool unallocated |
| 2024 | PWCS | St. John Paul the Great Catholic High School | private | Private/homeschool unallocated |

## NMSC Press-Release Audit

The archived NMSC PDFs are official press releases, not school-by-school or Virginia-list source tables. Visual inspection confirmed that the releases describe the annual program and state that the named Semifinalist list was distributed to news media but is not posted on the NMSC website. Because these PDFs do not identify Virginia schools or students, this pass does not create `verified_count`, `verified_zero`, or Virginia-share rows from them.

| Class | Date | Archived File | SHA-256 | Finding |
| --- | --- | --- | --- | --- |
| 2023 | 2022-09-14 | data/raw/nmsf/virginia/nmsc_2023_semifinalist_press_release.pdf | 61f19101190b89a1910bf06c005952e7e394538817add727426fd6c5757c7040 | Official press release only; no school-by-school list. |
| 2024 | 2023-09-13 | data/raw/nmsf/virginia/nmsc_2024_semifinalist_press_release.pdf | e1c36aa0a430b3b77ffdf6ec57a9863d913863fd508990ba8cbe4e0fe5b06bd8 | Official press release only; no school-by-school list. |
| 2025 | 2024-09-11 | data/raw/nmsf/virginia/nmsc_2025_semifinalist_press_release.pdf | ae3d9dfed1fb0a38643375312e2d42cf9b68d81b7ee110a38568f2645c73d54f | Official press release only; no school-by-school list. |
| 2026 | 2025-09-10 | data/raw/nmsf/virginia/nmsc_2026_semifinalist_press_release.pdf | f3f6eace78866181724dd003975113b56ec0594476a013ae89b1efd73a7527d4 | Official press release only; no school-by-school list. |

## Broad Source-Discovery Log

A follow-up public-source sweep looked for complete Virginia school-by-school lists or authoritative mirrors for Classes 2023-2026. It did not locate a complete list. These searches are documented as reproducible limitation evidence; they do not establish zeros for missing schools.

| Workflow | Query Or Source | Result | Finding | Action |
| --- | --- | --- | --- | --- |
| Internet Archive CDX | NMSC editor-document PDF index, focal window 2022-09 through 2025-09 (`www.nationalmerit.org/s/1758/images/gid2/editor_documents/*`) | Returned annual press releases, scholarship-recipient PDFs, annual reports, and guide PDFs; the focal semifinalist artifacts were `23_meritsemi.pdf` through `26_meritsemi.pdf`. | No state-list or Virginia-list filename was exposed in the NMSC PDF index. | Retain the archived press releases as discovery evidence only; do not create counts or zeros. |
| Internet Archive CDX | NMSC broad semifinalist URL wildcard (`www.nationalmerit.org/*national*merit*semifinal*`) | Returned an empty CDX result for the focal window. | No alternate NMSC-hosted complete-list URL was found. | Keep Priority A dependent on a public media mirror or other complete source. |
| Public web search | Class-year phrase searches for `National Merit Semifinalists Virginia` and `National Merit Scholarship Semifinalists Virginia`, Classes 2023-2026 | Did not surface a complete statewide school-by-school list; visible results were irrelevant, school pages, or local/school-area articles already handled as incomplete sources. | No complete public Virginia mirror was located through broad web search. | Do not change observation counts; keep remaining rows `missing_source`. |
| Common Crawl URL index | Wildcard URL probes including `*national*merit*semifinal*virginia*` and `*national-merit-semifinalists*virginia*` in 2023-2025 indexes | Returned no captures for the tested URL patterns. | No broad web-crawl URL evidence of a public Virginia list mirror was found. | Use this only as search-limitation evidence, not as evidence of zero semifinalists. |
| Internet Archive CDX | Major Virginia/DC media URL patterns under Richmond Times-Dispatch, Roanoke Times, Daily Press, The Virginian-Pilot, Daily Progress, News & Advance, AP, WTOP, InsideNoVa, and FFXnow | Responsive domain patterns returned empty result sets; the Fredericksburg.com wildcard timed out rather than producing usable candidates. | No complete statewide media mirror was found in these broad media-domain URL indexes. | Document the limitation and avoid continuing lower-yield school-by-school scraping. |
| Internet Archive CDX | Patch Virginia URL patterns (`patch.com/virginia/*national-merit*` variants) | The broad archive URL patterns returned empty, while the project already has relevant Patch articles discovered through community topic feeds and local searches. | Patch coverage remains local or school-area coverage, not a complete Virginia list. | Keep Patch-derived rows positive-only; never use Patch absence for zero inference. |

## Source-Discovery Decision

- Do not add these NMSC press releases to `data/sources/source_manifest.yml` as numeric count sources because they do not provide school-level Virginia counts.
- Do not infer zeros for missing public or private rows from these press releases.
- Continue Priority A only from a public media mirror or other source that exposes a complete Virginia school-by-school list for the relevant class year.
- Leave Virginia statewide-share metrics blocked until a complete list or exact statewide semifinalist total is source-backed.
