#!/usr/bin/env python3
"""Build the source-backed NMSF observation layer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.nmsf.observations import (  # noqa: E402
    build_nmsf_observations,
    build_nmsf_source_report,
    write_csv,
)
from tj_psat_analysis.nmsf.schema import read_source_manifest  # noqa: E402
from tj_psat_analysis.validation import nmsf_source_violations  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--school-roster-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "school_roster.csv",
    )
    parser.add_argument(
        "--school-aliases-csv",
        type=Path,
        default=ROOT / "data" / "manual" / "school_aliases.csv",
    )
    parser.add_argument(
        "--counts-csv",
        type=Path,
        default=ROOT / "data" / "sources" / "nmsf_counts.csv",
    )
    parser.add_argument(
        "--source-manifest-yml",
        type=Path,
        default=ROOT / "data" / "sources" / "source_manifest.yml",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "nmsf_observations.csv",
    )
    parser.add_argument(
        "--report-md",
        type=Path,
        default=ROOT / "reports" / "data_quality" / "nmsf_source_registry.md",
    )
    args = parser.parse_args()

    rows, warnings = build_nmsf_observations(
        school_roster_csv=args.school_roster_csv,
        school_aliases_csv=args.school_aliases_csv,
        counts_csv=args.counts_csv,
        source_manifest_yml=args.source_manifest_yml,
    )
    violations = nmsf_source_violations(rows)
    if violations:
        for violation in violations:
            print(violation, file=sys.stderr)
        return 1

    write_csv(args.output_csv, rows)
    sources = read_source_manifest(args.source_manifest_yml)
    args.report_md.parent.mkdir(parents=True, exist_ok=True)
    args.report_md.write_text(build_nmsf_source_report(rows, warnings, sources=sources), encoding="utf-8")
    print(f"wrote {args.output_csv}")
    print(f"wrote {args.report_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
