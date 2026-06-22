# Task 9 Completion Record

Generated: 2026-06-22

## Deliverables

- `reports/robustness.md`
- `reports/limitations.md`
- `reports/initial_findings.md`
- `reports/conclusions.md`
- `reports/tables/task9_*.csv`
- `docs/source_notes/task9_web_research_sources.md`

## Headline descriptive results

- TJHSST pooled NMSF rate: 32.927 per 100 juniors in Classes 2023-2024 versus 18.890 in Classes 2025-2026 (-42.6%).
- Balanced 53-school conventional public base panel: 0.582 versus 0.674 (+15.8%).
- Balanced 54-school public panel including TJHSST: 1.094 versus 0.989 (-9.6%).
- TJHSST's share of balanced public NMSFs falls from 49.8% in Class 2024 to 32.3% in Class 2025 and 33.5% in Class 2026.
- Raw pooled counts imply that base-school gains offset 65.0% of TJHSST's decline; the enrollment-standardized decomposition reduces the offset to 37.3% and leaves a 90.4-student combined-public shortfall relative to component-specific baseline rates.
- Private-school counts are complete for the focal period, but private-school denominator and eligibility context remain too limited to establish an offset.

These are descriptive results, not causal estimates or measures of median achievement or school culture.

## Reproduction

Run:

```bash
UV_CACHE_DIR=.uv-cache uv run --no-sync python scripts/build_task9_outputs.py
```

The script rebuilds this completion record, Task 9 reports, source notes, and supporting tables from `data/processed/analysis_panel.csv`.

## Integrity

- Canonical panel rows: 608
- Canonical schools: 76
- Class years: 2019-2026
- Canonical panel SHA-256: `85ff777243e6ddfe4d176e47d816f6f9002e4b64c158a200bb1bd67a7ddc6184`
- Balanced count schools: 71
- Balanced public rate schools: 54
- Balanced private count schools: 16

## Stopping decision

The public-data phase is complete at the documented stopping point. After the broad complete-list and denominator pass, do not continue low-yield school-by-school scraping unless a new source can resolve multiple rows or a whole class-year scope.

Class 2026 statewide-denominator caveat: the committed supplied-list snapshot totals 494, while the public 2026 NMSC guide lists Virginia at 489 semifinalists. Treat statewide shares using the 2026 denominator as provisional until reconciled; local school counts and focal coverage are unchanged.

## Source boundary

Historical Regulations 3355.14 and 3355.15, Regulation 3355.16, official FCPS Class 2025 and Class 2026 bulletins, Board minutes, NMSC materials, College Board documentation, and FCPS COVID-era instructional records were reviewed. The annual Notice 3355 documents themselves were not recovered. Reports state that limitation and do not infer unrecovered procedural details.
