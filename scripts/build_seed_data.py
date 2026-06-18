#!/usr/bin/env python3
"""Build first-milestone roster and public enrollment outputs from the seed workbook."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.constants import SEED_WORKBOOK_RELATIVE_PATH
from tj_psat_analysis.seed_workbook import build_seed_outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workbook",
        type=Path,
        default=ROOT / SEED_WORKBOOK_RELATIVE_PATH,
        help="Path to the seed workbook.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "data" / "interim",
        help="Directory for interim generated CSV outputs.",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=ROOT / "data" / "processed",
        help="Directory for milestone deliverable CSV outputs.",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=ROOT / "reports" / "data_quality",
        help="Directory for generated data-quality reports.",
    )
    parser.add_argument(
        "--manual-dir",
        type=Path,
        default=ROOT / "data" / "manual",
        help="Directory for the byte-identical manual workbook copy.",
    )
    args = parser.parse_args()

    outputs = build_seed_outputs(
        workbook_path=args.workbook,
        output_dir=args.output_dir,
        processed_dir=args.processed_dir,
        report_dir=args.report_dir,
        manual_dir=args.manual_dir,
    )
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
