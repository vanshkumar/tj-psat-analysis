# Workbook Ingestion Data Quality Report

This report is generated from the seed workbook parser. It is deterministic
and records review queues rather than guessing through ambiguous data.

## Source workbook

| Field | Value |
| --- | --- |
| Workbook path | docs/source_notes/tj psat investigation.xlsx |
| Workbook SHA-256 | a7e041846b405a3a54c18c69e80918d375229f1c0423a98bfd3b6fb414ba157f |
| Manual copy path | data/manual/tj psat investigation.xlsx |
| Sheets read | raw, Sheet6 |
| Sheets ignored | seats, nsmf 2019, Sheet7 |

The parser reads only `raw` and `Sheet6`. It does not read values from
`nsmf 2019`, and the generated seed panel contains no numeric NMSF counts.

## Output summary

| Output | Rows |
| --- | --- |
| canonical school roster | 76 |
| public enrollment raw long rows | 420 |
| public grade-11 enrollment rows | 480 |
| class-year mapping rows | 8 |
| seed panel rows | 608 |
| numeric NMSF rows in seed panel | 0 |

## Roster coverage

| Sector | Schools |
| --- | --- |
| Private | 16 |
| Public | 60 |

| Pathway | Schools |
| --- | --- |
| Arlington | 5 |
| FCPS Region 1 | 5 |
| FCPS Region 2 | 5 |
| FCPS Region 3 | 5 |
| FCPS Region 4 | 5 |
| FCPS Region 5 | 4 |
| Fairfax | 11 |
| Falls Church | 1 |
| Loudoun | 19 |
| Prince William | 15 |
| TJHSST | 1 |

## Enrollment status counts

| Enrollment status | Rows |
| --- | --- |
| ambiguous_source_name | 14 |
| not_operating | 9 |
| reported | 390 |
| source_row_not_found | 7 |
| source_year_not_in_seed | 60 |

## Missing required roster fields

No missing required roster fields.

## Duplicate roster names

No duplicate normalized roster school names.

## Duplicate public enrollment source names

| Normalized source name | Rows | Source row IDs | Source names |
| --- | --- | --- | --- |
| FREEDOM HIGH | 2 | sheet6_row_022; sheet6_row_023 | FREEDOM HIGH; FREEDOM HIGH |

## Enrollment review queue

| School | Review status | Source rows | Source names |
| --- | --- | --- | --- |
| H-B Woodlawn Secondary Program | source_row_not_found | (none) | (none) |
| Freedom High School (South Riding) | ambiguous_source_name | sheet6_row_022; sheet6_row_023 | FREEDOM HIGH; FREEDOM HIGH |
| Freedom High School (Woodbridge) | ambiguous_source_name | sheet6_row_022; sheet6_row_023 | FREEDOM HIGH; FREEDOM HIGH |

## NMSF exclusion check

| Check | Result |
| --- | --- |
| `nsmf 2019` read by parser | no |
| Numeric NMSF rows in seed panel | 0 |
| Default NMSF status | source_pending |
