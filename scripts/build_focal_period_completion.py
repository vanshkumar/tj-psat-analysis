#!/usr/bin/env python3
"""Build the focal-period completion report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.nmsf.completion import build_focal_period_completion_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--observations-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "nmsf_observations_2023_2026.csv",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=ROOT / "reports" / "data_quality" / "focal_period_completion.md",
    )
    args = parser.parse_args()

    report = build_focal_period_completion_report(observations_csv=args.observations_csv, root=ROOT)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(report, encoding="utf-8")
    print(f"wrote {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
