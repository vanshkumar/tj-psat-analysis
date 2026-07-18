#!/usr/bin/env python3
"""Ingest the FCPS-origin Class 2025 admissions-by-source-school workbook."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.tjhsst_admissions import build_admissions_outputs  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workbook",
        type=Path,
        default=ROOT / "data" / "raw" / "admissions" / "fcps" / "tjhsst_class_2025_by_middle_school.xlsx",
    )
    parser.add_argument(
        "--source-metadata-csv",
        type=Path,
        default=ROOT / "data" / "sources" / "tjhsst_admissions_sources.csv",
    )
    parser.add_argument("--processed-dir", type=Path, default=ROOT / "data" / "processed")
    parser.add_argument("--report-dir", type=Path, default=ROOT / "reports" / "data_quality")
    args = parser.parse_args()
    outputs = build_admissions_outputs(
        workbook_path=args.workbook,
        source_metadata_csv=args.source_metadata_csv,
        processed_dir=args.processed_dir,
        report_dir=args.report_dir,
    )
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
