#!/usr/bin/env python3
"""Apply source-backed manual NMSF counts to the seed panel."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.nmsf.manual_counts import (  # noqa: E402
    apply_manual_counts_to_panel,
    load_csv_rows,
    read_manual_nmsf_counts,
    write_csv,
)
from tj_psat_analysis.validation import nmsf_source_violations  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--panel-csv",
        type=Path,
        default=ROOT / "data" / "interim" / "panel_seed.csv",
    )
    parser.add_argument(
        "--roster-csv",
        type=Path,
        default=ROOT / "data" / "interim" / "canonical_schools.csv",
    )
    parser.add_argument(
        "--counts-csv",
        type=Path,
        default=ROOT / "data" / "sources" / "nmsf_counts.csv",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=ROOT / "data" / "interim" / "panel_nmsf.csv",
    )
    args = parser.parse_args()

    panel_rows = load_csv_rows(args.panel_csv)
    roster_rows = load_csv_rows(args.roster_csv)
    records = read_manual_nmsf_counts(args.counts_csv)
    output_rows = apply_manual_counts_to_panel(panel_rows, roster_rows, records)

    violations = nmsf_source_violations(output_rows)
    if violations:
        for violation in violations:
            print(violation, file=sys.stderr)
        return 1

    write_csv(args.output_csv, output_rows)
    print(f"applied {len(records)} manual NMSF counts")
    print(f"wrote {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
