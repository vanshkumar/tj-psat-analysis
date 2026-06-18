#!/usr/bin/env python3
"""Stub for ingesting 2024-25 public grade 11 enrollment for Class 2026.

Expected input is a downloaded NCES/ELSI or CCD CSV with school names and a
grade-11 2024-25 column. This script fails closed when the file is absent or
the column is not explicit.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", type=Path, required=True)
    parser.add_argument(
        "--grade11-column",
        default="Grade 11 Students [Public School] 2024-25",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=ROOT / "data" / "interim" / "public_grade11_enrollment_2024_25.csv",
    )
    args = parser.parse_args()

    if not args.input_csv.exists():
        raise SystemExit(f"Input CSV not found: {args.input_csv}")

    with args.input_csv.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or args.grade11_column not in reader.fieldnames:
            raise SystemExit(
                f"Expected explicit 2024-25 grade 11 column {args.grade11_column!r}; "
                "refusing to infer it."
            )
        rows = list(reader)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
