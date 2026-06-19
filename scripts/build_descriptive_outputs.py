#!/usr/bin/env python3
"""Build Milestone 8 descriptive tables, figures, and report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.descriptive import build_descriptive_outputs  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--analysis-panel-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "analysis_panel.csv",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=ROOT / "reports" / "figures",
    )
    parser.add_argument(
        "--tables-dir",
        type=Path,
        default=ROOT / "reports" / "tables",
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        default=ROOT / "reports" / "descriptive_results.md",
    )
    args = parser.parse_args()

    outputs = build_descriptive_outputs(
        analysis_panel_csv=args.analysis_panel_csv,
        figures_dir=args.figures_dir,
        tables_dir=args.tables_dir,
        report_path=args.report_path,
    )
    for label, path in sorted(outputs.items()):
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
