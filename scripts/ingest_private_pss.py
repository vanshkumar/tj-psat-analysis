#!/usr/bin/env python3
"""Extract private-school grade-11 denominators from NCES PSS public-use CSVs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.enrollment import (
    PssZipSource,
    extract_private_pss_grade11_rows,
    load_csv_rows,
)
from tj_psat_analysis.seed_workbook import write_csv


def _parse_pss_zip_arg(value: str) -> PssZipSource:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Expected SCHOOL_YEAR=/path/to/pss.zip")
    school_year, path = value.split("=", 1)
    return PssZipSource(school_year=school_year.strip(), zip_path=Path(path).expanduser())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pss-zip",
        action="append",
        type=_parse_pss_zip_arg,
        required=True,
        help="Repeatable SCHOOL_YEAR=/path/to/pss public-use CSV ZIP, e.g. 2021-22=/tmp/pss2122.zip.",
    )
    parser.add_argument(
        "--school-roster-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "school_roster.csv",
    )
    parser.add_argument(
        "--pss-id-csv",
        type=Path,
        default=ROOT / "data" / "manual" / "private_school_pss_ids.csv",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=ROOT / "data" / "interim" / "private_grade11_enrollment.csv",
    )
    args = parser.parse_args()

    rows = extract_private_pss_grade11_rows(
        school_roster_rows=load_csv_rows(args.school_roster_csv),
        pss_id_csv=args.pss_id_csv,
        pss_sources=args.pss_zip,
    )
    write_csv(args.output_csv, rows)
    print(f"wrote {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
