#!/usr/bin/env python3
"""Build first-milestone roster and public enrollment outputs from the seed workbook."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

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
        help="Directory for generated CSV outputs.",
    )
    args = parser.parse_args()

    outputs = build_seed_outputs(args.workbook, args.output_dir)
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
