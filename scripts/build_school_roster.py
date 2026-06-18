#!/usr/bin/env python3
"""Build Milestone 2 canonical roster, aliases, and history outputs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.constants import SEED_WORKBOOK_RELATIVE_PATH
from tj_psat_analysis.school_roster import (
    ADMISSIONS_POLICY_RELATIVE_PATH,
    build_school_roster_outputs,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workbook",
        type=Path,
        default=ROOT / SEED_WORKBOOK_RELATIVE_PATH,
        help="Path to the seed workbook.",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=ROOT / "data" / "processed",
        help="Directory for processed roster outputs.",
    )
    parser.add_argument(
        "--manual-dir",
        type=Path,
        default=ROOT / "data" / "manual",
        help="Directory for manual roster support outputs.",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=ROOT / "reports" / "data_quality",
        help="Directory for roster review reports.",
    )
    parser.add_argument(
        "--nces-id-csv",
        type=Path,
        default=ROOT / "data" / "manual" / "public_school_nces_ids.csv",
        help="Curated public-school NCES ID source CSV.",
    )
    parser.add_argument(
        "--ccd-directory-zip",
        type=Path,
        default=None,
        help="Optional NCES CCD directory ZIP used to regenerate the NCES ID CSV.",
    )
    parser.add_argument(
        "--admissions-policy-pdf",
        type=Path,
        default=ROOT / ADMISSIONS_POLICY_RELATIVE_PATH,
        help="Path to the TJHSST admissions pathway source PDF.",
    )
    args = parser.parse_args()

    outputs = build_school_roster_outputs(
        workbook_path=args.workbook,
        processed_dir=args.processed_dir,
        manual_dir=args.manual_dir,
        report_dir=args.report_dir,
        nces_id_csv=args.nces_id_csv,
        ccd_directory_zip=args.ccd_directory_zip,
        admissions_policy_pdf=args.admissions_policy_pdf,
    )
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
