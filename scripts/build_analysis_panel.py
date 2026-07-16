#!/usr/bin/env python3
"""Build the analytical panel."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.analysis_panel import build_analysis_outputs  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--school-roster-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "school_roster.csv",
    )
    parser.add_argument(
        "--nmsf-observations-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "nmsf_observations.csv",
    )
    parser.add_argument(
        "--enrollment-panel-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "enrollment_panel.csv",
    )
    parser.add_argument(
        "--class-year-mapping-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "class_year_mapping.csv",
    )
    parser.add_argument(
        "--school-history-csv",
        type=Path,
        default=ROOT / "data" / "manual" / "school_history.csv",
    )
    parser.add_argument(
        "--statewide-totals-csv",
        type=Path,
        default=ROOT / "data" / "sources" / "virginia_statewide_totals.csv",
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

    outputs = build_analysis_outputs(
        school_roster_csv=args.school_roster_csv,
        nmsf_observations_csv=args.nmsf_observations_csv,
        enrollment_panel_csv=args.enrollment_panel_csv,
        class_year_mapping_csv=args.class_year_mapping_csv,
        school_history_csv=args.school_history_csv,
        statewide_totals_csv=args.statewide_totals_csv,
        processed_dir=args.processed_dir,
        report_dir=args.report_dir,
    )
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
