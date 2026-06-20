#!/usr/bin/env python3
"""Build Milestone 3 enrollment panel and coverage reports."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.enrollment import build_enrollment_outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--school-roster-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "school_roster.csv",
    )
    parser.add_argument(
        "--public-seed-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "public_enrollment.csv",
    )
    parser.add_argument(
        "--public-2024-25-csv",
        type=Path,
        default=ROOT / "data" / "interim" / "public_grade11_enrollment_2024_25.csv",
    )
    parser.add_argument(
        "--public-supplement-csv",
        type=Path,
        default=ROOT / "data" / "interim" / "public_grade11_enrollment_nces_supplement.csv",
    )
    parser.add_argument(
        "--private-pss-csv",
        type=Path,
        default=ROOT / "data" / "interim" / "private_grade11_enrollment.csv",
    )
    parser.add_argument(
        "--private-pss-locator-csv",
        type=Path,
        default=ROOT / "data" / "interim" / "private_grade11_enrollment_pss_locator_2023_24.csv",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=ROOT / "data" / "processed",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=ROOT / "reports" / "data_quality",
    )
    args = parser.parse_args()

    outputs = build_enrollment_outputs(
        school_roster_csv=args.school_roster_csv,
        public_seed_csv=args.public_seed_csv,
        public_supplement_csv=args.public_supplement_csv,
        public_2024_25_csv=args.public_2024_25_csv,
        private_pss_csv=args.private_pss_csv,
        private_pss_locator_csv=args.private_pss_locator_csv,
        processed_dir=args.processed_dir,
        report_dir=args.report_dir,
    )
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
