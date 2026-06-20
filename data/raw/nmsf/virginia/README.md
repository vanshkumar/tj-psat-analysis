# Virginia NMSF Source Artifacts

This directory stores Virginia-list discovery artifacts for Milestone 10.

The archived NMSC PDFs are official annual Semifinalist press releases. They do
not contain student names or school-by-school Virginia lists; they state that
the named list was distributed to news media and was not posted on the NMSC
website. Therefore they are preserved as source-discovery evidence only and are
not numeric source-manifest entries.

The `virginia_2023_semifinalists_snapshot.csv`,
`virginia_2024_semifinalists_snapshot.csv`, and
`virginia_2026_semifinalists_snapshot.csv` files are count-only snapshots
derived from user-supplied complete NMSC Virginia media lists. They intentionally
omit student names and are the archived source-manifest artifacts for count,
zero-inference, and statewide-total use.

The local `supplied_lists/` directory is ignored by git. To regenerate the
count-only snapshots, place the source PDFs at the paths expected by
`scripts/ingest_nmsc_virginia_lists.py` and run that script.
