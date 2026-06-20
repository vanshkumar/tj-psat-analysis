# Task 9 Completion Record

Completed: 2026-06-19

## Deliverables

- `reports/robustness.md`
- `reports/limitations.md`
- `reports/initial_findings.md`


## Headline descriptive results

- TJHSST pooled NMSF rate: 32.927 per 100 juniors in Classes 2023-2024
  versus 18.890 in Classes 2025-2026 (-42.6%).
- Balanced 52-school conventional public base panel: 0.593 versus 0.687
  (+16.0%).
- Balanced 53-school public panel including TJHSST: 1.116 versus 1.009
  (-9.6%).
- Class 2025 is the sharp break; Class 2026 shows a partial TJHSST rebound and
  a heterogeneous base-school increase. Private-school offset remains unresolved.

These are descriptive results, not causal estimates or measures of median
achievement or school culture.

## Reproduction

Run:

```bash
python scripts/build_task9_outputs.py
```

The script rebuilds all Task 9 reports and supporting tables from
`data/processed/analysis_panel.csv`.

## Integrity

- Canonical panel rows: 608
- Canonical schools: 76
- Class years: 2019-2026
- Canonical panel SHA-256:
  `279606efc11e373bb69f8c1457364157b61d27190c7abfa3982bef66f2ff0333`
- Input panel reflects the Milestone 10 Freedom High denominator supplement.
- Independent Task 9 validation assertions passed.

## Source boundary

Historical Regulations 3355.14 and 3355.15, Regulation 3355.16, official FCPS
Class 2025 and Class 2026 bulletins, Board minutes, NMSC materials, College
Board documentation, and FCPS COVID-era instructional records were reviewed.
The annual Notice 3355 documents themselves were not recovered. Reports state
that limitation and do not infer unrecovered procedural details.
