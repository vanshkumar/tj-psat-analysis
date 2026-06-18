#!/usr/bin/env python3
"""Fail if NMSF counts are numeric without required source metadata."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.validation import load_csv_rows, nmsf_source_violations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "panel_csv",
        type=Path,
        nargs="?",
        default=ROOT / "data" / "interim" / "panel_seed.csv",
    )
    args = parser.parse_args()

    violations = nmsf_source_violations(load_csv_rows(args.panel_csv))
    if violations:
        for violation in violations:
            print(violation, file=sys.stderr)
        return 1
    print("NMSF source metadata validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
