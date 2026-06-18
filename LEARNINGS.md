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
- Observation: The reliable local test command for this scaffold is `python -m unittest discover -s tests`.
- Action: Use the explicit `-s tests` discovery command in README and verification runs.
- Confidence: high

## What Has Failed
