#!/usr/bin/env python3
"""Stub ingestion for NCES PSS private-school grade 11 enrollment.

The NCES PSS grade 11 variable is `P290`. This script preserves the raw value
and does not estimate missing or suppressed records.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.normalize import normalize_school_name


def _parse_int(value: str) -> tuple[str, str]:
    text = (value or "").strip()
    if not text:
        return "", "blank"
    try:
        return str(int(float(text.replace(",", "")))), "reported"
    except ValueError:
        return "", f"unparsed:{text}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", type=Path, required=True)
    parser.add_argument("--school-year", required=True, help="Example: 2023-24")
    parser.add_argument("--class-year", type=int, required=True)
    parser.add_argument("--name-column", default="SCH_NAME")
    parser.add_argument("--grade11-column", default="P290")
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=ROOT / "data" / "interim" / "private_grade11_enrollment.csv",
    )
    args = parser.parse_args()

    if not args.input_csv.exists():
        raise SystemExit(f"Input CSV not found: {args.input_csv}")

    with args.input_csv.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {args.name_column, args.grade11_column}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"Missing required PSS columns: {', '.join(sorted(missing))}")
        output_rows = []
        for row_number, row in enumerate(reader, start=2):
            value, status = _parse_int(row.get(args.grade11_column, ""))
            output_rows.append(
                {
                    "school_name_source": row.get(args.name_column, ""),
                    "normalized_school_name": normalize_school_name(row.get(args.name_column, "")),
                    "class_year": args.class_year,
                    "grade11_school_year": args.school_year,
                    "grade11_enrollment": value,
                    "enrollment_status": status,
                    "source_variable": args.grade11_column,
                    "source_row": row_number,
                }
            )

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0].keys()) if output_rows else [])
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"wrote {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
