# NMSF Reconciliation 2023-2026

This report is generated from the source-backed focal-period NMSF observation layer.
TJHSST is kept as one school row; jurisdictional or former-school TJHSST references in APS/LCPS/PWCS releases are excluded from the panel and retained only for reconciliation notes.

## Output Summary

| Output | Rows |
| --- | --- |
| data/processed/nmsf_observations_2023_2026.csv | 304 |
| reports/data_quality/manual_review_queue.csv | 104 |

## Observation Status Counts

| Status | Rows |
| --- | --- |
| missing_source | 1 |
| verified_count | 201 |
| verified_zero | 102 |

## Coverage By Division And Class

| Class | Division | Rows | Verified Count | Verified Zero | Missing Source | Not Operating |
| --- | --- | --- | --- | --- | --- | --- |
| 2023 | APS | 5 | 5 | 0 | 0 | 0 |
| 2023 | FCPS | 36 | 25 | 11 | 0 | 0 |
| 2023 | Falls Church City | 1 | 0 | 1 | 0 | 0 |
| 2023 | LCPS | 19 | 16 | 3 | 0 | 0 |
| 2023 | PWCS | 15 | 2 | 13 | 0 | 0 |
| 2024 | APS | 5 | 4 | 1 | 0 | 0 |
| 2024 | FCPS | 36 | 21 | 15 | 0 | 0 |
| 2024 | Falls Church City | 1 | 1 | 0 | 0 | 0 |
| 2024 | LCPS | 19 | 15 | 4 | 0 | 0 |
| 2024 | PWCS | 15 | 3 | 12 | 0 | 0 |
| 2025 | APS | 5 | 5 | 0 | 0 | 0 |
| 2025 | FCPS | 36 | 30 | 6 | 0 | 0 |
| 2025 | Falls Church City | 1 | 0 | 0 | 1 | 0 |
| 2025 | LCPS | 19 | 15 | 4 | 0 | 0 |
| 2025 | PWCS | 15 | 7 | 8 | 0 | 0 |
| 2026 | APS | 5 | 4 | 1 | 0 | 0 |
| 2026 | FCPS | 36 | 27 | 9 | 0 | 0 |
| 2026 | Falls Church City | 1 | 1 | 0 | 0 | 0 |
| 2026 | LCPS | 19 | 14 | 5 | 0 | 0 |
| 2026 | PWCS | 15 | 6 | 9 | 0 | 0 |

## Source Reconciliation

| Source ID | Class | Reported Total | In-Panel Count Total | Excluded Snapshot Total | Reconciled Total | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| aps_2023_semifinalists | 2023 | 17 | 15 | 2 | 17 | reconciled | Thomas Jefferson High School for Science and Technology: 2 excluded_tjhsst_resident_subset |
| aps_2025_semifinalists | 2025 | 22 | 15 | 7 | 22 | reconciled | Thomas Jefferson High School for Science and Technology: 7 excluded_tjhsst_resident_subset |
| aps_2026_semifinalists | 2026 | 30 | 20 | 10 | 30 | reconciled | Arlington Tech: 1 excluded_nonroster_school; Thomas Jefferson High School for Science and Technology: 9 excluded_tjhsst_resident_subset |
| fcps_2023_semifinalists | 2023 | 238 | 238 | 0 | 238 | reconciled | FCPS high schools including TJHSST |
| fcps_2024_semifinalists | 2024 | 264 | 264 | 0 | 264 | reconciled | FCPS high schools including TJHSST |
| fcps_2025_semifinalists | 2025 | 191 | 191 | 0 | 191 | reconciled | FCPS high schools including TJHSST |
| fcps_2026_semifinalists | 2026 | 262 | 262 | 0 | 262 | reconciled | FCPS high schools including TJHSST |
| lcps_2023_semifinalists | 2023 | 62 | 44 | 18 | 62 | reconciled | Thomas Jefferson High School for Science and Technology: 18 excluded_tjhsst_resident_subset |
| lcps_2024_semifinalists | 2024 | 82 | 57 | 25 | 82 | reconciled | Thomas Jefferson High School for Science and Technology: 25 excluded_tjhsst_resident_subset |
| lcps_2025_named_list_reconciliation | 2025 | 0 | 0 | 0 | 0 | reconciled | Sum of the four explicit verified-zero school observations; the reconciliation evidence covers all 57 official LCPS identities. |
| lcps_2025_semifinalists | 2025 | 57 | 0 | 57 | 57 | reconciled | LCPS unattributed semifinalist total: 57 source_incomplete_unattributed_total |
| lcps_2026_semifinalists | 2026 | 69 | 57 | 12 | 69 | reconciled | Thomas Jefferson High School for Science and Technology: 12 excluded_tjhsst_resident_subset |
| nmsc_virginia_2023_semifinalists | 2023 | 400 | 13 | 387 | 400 | reconciled | Complete Virginia count-only snapshot total; only still-missing positive roster rows are imported from this source. This is a Virginia school-location total; official NMSC state-selection-unit totals are stored separately. |
| nmsc_virginia_2024_semifinalists | 2024 | 470 | 8 | 462 | 470 | reconciled | Complete Virginia count-only snapshot total; only still-missing positive roster rows are imported from this source. This is a Virginia school-location total; official NMSC state-selection-unit totals are stored separately. |
| nmsc_virginia_2026_semifinalists | 2026 | 494 | 6 | 488 | 494 | reconciled | Complete Virginia count-only snapshot total; only still-missing positive roster rows are imported from this source. This is a Virginia school-location total; official NMSC state-selection-unit totals are stored separately. |
| patch_arlington_2023_semifinalists | 2023 | 17 | 1 | 16 | 17 | reconciled | Wakefield High School: 2 excluded_duplicate_public_school_count; Washington-Liberty High School: 7 excluded_duplicate_public_school_count; H.B. Woodlawn: 3 excluded_duplicate_public_school_count; Yorktown High School: 3 excluded_duplicate_public_school_count; Arlington homeschooled semifinalist: 1 excluded_nonroster_school |
| patch_arlington_2024_semifinalists | 2024 | 23 | 16 | 7 | 23 | reconciled | Thomas Jefferson High School for Science and Technology: 7 excluded_tjhsst_resident_subset |
| patch_arlington_2025_semifinalists | 2025 | 16 | 1 | 15 | 16 | reconciled | Wakefield High School: 2 excluded_duplicate_public_school_count; Washington-Liberty High School: 7 excluded_duplicate_public_school_count; The H.B. Woodlawn Program: 3 excluded_duplicate_public_school_count; Yorktown High School: 3 excluded_duplicate_public_school_count |
| patch_arlington_2026_semifinalists | 2026 | 22 | 1 | 21 | 22 | reconciled | Arlington Career Center: 1 excluded_nonroster_school; Washington-Liberty High School: 9 excluded_duplicate_public_school_count; The H. B. Woodlawn Program: 6 excluded_duplicate_public_school_count; Yorktown High School: 5 excluded_duplicate_public_school_count |
| patch_ashburn_2025_semifinalists | 2025 | 46 | 45 | 1 | 46 | reconciled | Evergreen Christian School: 1 excluded_nonroster_school |
| patch_ashburn_2026_semifinalists | 2026 | 59 | 1 | 58 | 59 | reconciled | John Champe High School: 3 excluded_duplicate_public_school_count; Lightridge High School: 5 excluded_duplicate_public_school_count; Briar Woods High School: 8 excluded_duplicate_public_school_count; Broad Run High School: 3 excluded_duplicate_public_school_count; Independence High School: 8 excluded_duplicate_public_school_count; Rock Ridge High School: 7 excluded_duplicate_public_school_count; Stone Bridge High School: 4 excluded_duplicate_public_school_count; Heritage High School: 1 excluded_duplicate_public_school_count; Homeschool/Online School: 1 excluded_nonroster_school; Riverside High School: 5 excluded_duplicate_public_school_count; Potomac Falls High School: 1 excluded_duplicate_public_school_count; Woodgrove High School: 2 excluded_duplicate_public_school_count; Freedom High School: 7 excluded_duplicate_public_school_count; Dominion High School: 3 excluded_duplicate_public_school_count |
| patch_fairfax_city_2025_semifinalists | 2025 | 17 | 3 | 14 | 17 | reconciled | Fairfax High School: 4 excluded_duplicate_public_school_count; James W. Robinson Secondary School: 4 excluded_duplicate_public_school_count; W. T. Woodson High School: 6 excluded_duplicate_public_school_count |
| patch_fairfax_city_2026_semifinalists | 2026 | 15 | 2 | 13 | 15 | reconciled | Fairfax High School: 5 excluded_duplicate_public_school_count; Carter G. Woodson High School: 8 excluded_duplicate_public_school_count |
| patch_falls_church_2024_semifinalists | 2024 | 11 | 5 | 6 | 11 | reconciled | Marshall High School: 6 excluded_duplicate_public_school_count |
| patch_manassas_2026_semifinalists | 2026 | 10 | 3 | 7 | 10 | reconciled | Gainesville High School: 1 excluded_duplicate_public_school_count; Battlefield High School: 2 excluded_duplicate_public_school_count; Charles Colgan High School: 1 excluded_duplicate_public_school_count; Osbourn High School: 1 excluded_nonroster_school; Patriot High School: 1 excluded_duplicate_public_school_count; C.D. Hylton High School: 1 excluded_duplicate_public_school_count |
| patch_mclean_2023_semifinalists | 2023 | 46 | 10 | 36 | 46 | reconciled | McLean High School: 22 excluded_duplicate_public_school_count; Langley High School: 14 excluded_duplicate_public_school_count |
| patch_mclean_2024_semifinalists | 2024 | 40 | 11 | 29 | 40 | reconciled | Homeschool: 1 excluded_nonroster_school; Langley High School: 13 excluded_duplicate_public_school_count; McLean High School: 15 excluded_duplicate_public_school_count |
| patch_mclean_2025_semifinalists | 2025 | 52 | 16 | 36 | 52 | reconciled | Homeschool/Online School: 1 excluded_nonroster_school; Langley High School: 19 excluded_duplicate_public_school_count; McLean High School: 16 excluded_duplicate_public_school_count |
| patch_mclean_2026_semifinalists | 2026 | 65 | 22 | 43 | 65 | reconciled | Langley High School: 23 excluded_duplicate_public_school_count; McLean High School: 20 excluded_duplicate_public_school_count |
| patch_vienna_2023_semifinalists | 2023 | 31 | 2 | 29 | 31 | reconciled | James Madison High School: 11 excluded_duplicate_public_school_count; Oakton High School: 11 excluded_duplicate_public_school_count; Marshall High School: 7 excluded_duplicate_public_school_count |
| patch_vienna_2024_semifinalists | 2024 | 31 | 4 | 27 | 31 | reconciled | James Madison High School: 7 excluded_duplicate_public_school_count; Oakton High School: 14 excluded_duplicate_public_school_count; Marshall High School: 6 excluded_duplicate_public_school_count |
| patch_vienna_2025_semifinalists | 2025 | 221 | 9 | 212 | 221 | reconciled | Homeschool/Online School: 1 excluded_nonroster_school; James Madison High School: 9 excluded_duplicate_public_school_count; Oakton High School: 11 excluded_duplicate_public_school_count; Thomas Edison High School: 2 excluded_duplicate_public_school_count; Hayfield Secondary School: 1 excluded_duplicate_public_school_count; West Potomac High School: 1 excluded_duplicate_public_school_count; Thomas Jefferson High School for Science and Technology: 81 excluded_duplicate_public_school_count; Lake Braddock Secondary School: 9 excluded_duplicate_public_school_count; Chantilly High School: 10 excluded_duplicate_public_school_count; Westfield High School: 3 excluded_duplicate_public_school_count; Centreville High School: 3 excluded_duplicate_public_school_count; Fairfax High School: 4 excluded_duplicate_public_school_count; New School of Northern Virginia: 1 excluded_duplicate_private_school_count; Robinson Secondary School: 4 excluded_duplicate_public_school_count; Trinity Christian School: 1 excluded_duplicate_private_school_count; Woodson High School: 6 excluded_duplicate_public_school_count; Marshall High School: 5 excluded_duplicate_public_school_count; Dominion School: 1 excluded_nonroster_school; Herndon High School: 1 excluded_duplicate_public_school_count; BASIS Independent McLean: 4 excluded_duplicate_private_school_count; Homeschool/Online School: 1 excluded_nonroster_school; Langley High School: 19 excluded_duplicate_public_school_count; The Madeira School: 3 excluded_duplicate_private_school_count; McLean High School: 16 excluded_duplicate_public_school_count; The Potomac School: 9 excluded_duplicate_private_school_count; South Lakes High School: 3 excluded_duplicate_public_school_count; West Springfield High School: 3 excluded_duplicate_public_school_count |
| patch_vienna_2026_semifinalists | 2026 | 53 | 5 | 48 | 53 | reconciled | James Madison High School: 8 excluded_duplicate_public_school_count; Oakton High School: 25 excluded_duplicate_public_school_count; Marshall High School: 15 excluded_duplicate_public_school_count |
| patch_woodbridge_2025_semifinalists | 2025 | 8 | 2 | 6 | 8 | reconciled | Forest Park High School: 1 excluded_duplicate_public_school_count; Battlefield High School: 2 excluded_duplicate_public_school_count; Charles Colgan High School: 1 excluded_duplicate_public_school_count; Osbourn Park High School: 1 excluded_duplicate_public_school_count; Patriot High School: 1 excluded_duplicate_public_school_count |
| pwcs_2023_semifinalists | 2023 | 3 | 2 | 1 | 3 | reconciled | Thomas Jefferson High School for Science and Technology: 1 excluded_tjhsst_former_pwcs_student |
| pwcs_2024_semifinalists | 2024 | 6 | 2 | 4 | 6 | reconciled | Thomas Jefferson High School for Science and Technology: 4 excluded_tjhsst_former_pwcs_student |
| pwcs_2025_semifinalists | 2025 | 7 | 6 | 1 | 7 | reconciled | Thomas Jefferson High School for Science and Technology: 1 excluded_tjhsst_former_pwcs_student |
| pwcs_2026_semifinalists | 2026 | 6 | 6 | 0 | 6 | reconciled | PWCS high-school students |

## Source Gaps

| Class | Division | Missing Rows |
| --- | --- | --- |
| 2025 | Falls Church City | 1 |

## Source Rules

- Positive counts are imported only from manifest-backed school-level source transcriptions.
- Verified zeros are inferred only from manifest entries marked complete for the division scope.
- Source-incomplete district totals may reconcile a source without creating school observations.
- APS/LCPS/PWCS TJHSST subset rows are not imported as separate TJHSST observations because the panel keeps TJHSST as one row.
- Missing rows remain missing; incomplete or inaccessible source searches do not become zeros.