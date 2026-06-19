#!/usr/bin/env python3
"""Build Milestone 5 four-year NMSF pilot outputs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.nmsf.pilot import (  # noqa: E402
    build_manual_review_queue,
    build_reconciliation_report,
    load_csv_rows,
    pilot_rows,
    write_manual_review_queue,
    write_pilot_csv,
)
from tj_psat_analysis.nmsf.schema import read_source_manifest  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--observations-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "nmsf_observations.csv",
    )
    parser.add_argument(
        "--source-manifest-yml",
        type=Path,
        default=ROOT / "data" / "sources" / "source_manifest.yml",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "nmsf_observations_2023_2026.csv",
    )
    parser.add_argument(
        "--manual-review-csv",
        type=Path,
        default=ROOT / "reports" / "data_quality" / "manual_review_queue.csv",
    )
    parser.add_argument(
        "--reconciliation-md",
        type=Path,
        default=ROOT / "reports" / "data_quality" / "nmsf_reconciliation_2023_2026.md",
    )
    args = parser.parse_args()

    rows = pilot_rows(load_csv_rows(args.observations_csv))
    sources = read_source_manifest(args.source_manifest_yml)
    review_rows = build_manual_review_queue(rows, sources=sources, root=ROOT)
    report = build_reconciliation_report(rows, sources=sources, root=ROOT)

    write_pilot_csv(args.output_csv, rows)
    write_manual_review_queue(args.manual_review_csv, review_rows)
    args.reconciliation_md.parent.mkdir(parents=True, exist_ok=True)
    args.reconciliation_md.write_text(report, encoding="utf-8")

    print(f"wrote {args.output_csv}")
    print(f"wrote {args.manual_review_csv}")
    print(f"wrote {args.reconciliation_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
