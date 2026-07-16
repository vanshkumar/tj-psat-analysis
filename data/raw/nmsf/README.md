# NMSF Source Snapshots

This directory contains count-only source snapshots used by the NMSF
observation layer. Student names are intentionally omitted. The source manifest
records each numeric snapshot's URL, title, publication and retrieval dates,
scope, completeness rules, and SHA-256 hash.

Provider notes:

- `fcps/`, `aps/`, and `pwcs/` contain school-attributed counts transcribed from
  official school-division releases. Jurisdictional or former-school references
  to students attending TJHSST are retained for reconciliation only; TJHSST
  remains one canonical row.
- `lcps/` contains school-attributed official snapshots where available. The
  Class 2025 release is total-only and source-incomplete, so it cannot create
  school-level observations or verified zeros.
- `local_media/` contains positive school-attributed counts used only where an
  official division release did not resolve a roster row. Overlapping public
  rows and non-roster schools are retained for reconciliation rather than added
  to the panel.
- `virginia/` contains official NMSC press releases and count-only snapshots
  derived from complete Virginia media lists for Classes 2023, 2024, and 2026.
  The press releases are discovery evidence only because they do not contain the
  named Virginia lists. Complete-list snapshots support positive counts,
  verified zeros, and statewide totals.

The local `virginia/supplied_lists/` directory is ignored by git because the
source PDFs contain student names. To regenerate the count-only Virginia
snapshots, place the source PDFs at the paths expected by
`scripts/ingest_nmsc_virginia_lists.py` and run that script.
