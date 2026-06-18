#!/usr/bin/env python3
"""Extract Class 2026 public grade-11 denominators from NCES CCD membership."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.enrollment import extract_public_ccd_grade11_rows, load_csv_rows
from tj_psat_analysis.seed_workbook import write_csv


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--membership-zip",
        type=Path,
        required=True,
        help="NCES CCD 2024-25 school membership ZIP.",
    )
    parser.add_argument(
        "--school-roster-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "school_roster.csv",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=ROOT / "data" / "interim" / "public_grade11_enrollment_2024_25.csv",
    )
    args = parser.parse_args()

    rows = extract_public_ccd_grade11_rows(
        school_roster_rows=load_csv_rows(args.school_roster_csv),
        membership_zip=args.membership_zip,
    )
    write_csv(args.output_csv, rows)
    print(f"wrote {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
