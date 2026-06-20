#!/usr/bin/env python3
"""Extract targeted public-school grade-11 denominators from NCES CCD membership files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.enrollment import (  # noqa: E402
    PublicCcdMembershipSource,
    extract_public_ccd_membership_grade11_rows,
    load_csv_rows,
)
from tj_psat_analysis.seed_workbook import write_csv  # noqa: E402

DEFAULT_TARGET_SCHOOL_IDS = (
    "freedom_high_school_south_riding",
    "freedom_high_school_woodbridge",
)

CCD_SOURCE_BY_SCHOOL_YEAR = {
    "2021-22": {
        "title": (
            "NCES CCD 2021-22 Public Elementary/Secondary School Universe Survey Data, "
            "v.1a, School Membership"
        ),
        "url": "https://nces.ed.gov/ccd/Data/zip/ccd_SCH_052_2122_l_1a_071722.zip",
        "date": "2022-07-17",
    },
    "2022-23": {
        "title": (
            "NCES CCD 2022-23 Public Elementary/Secondary School Universe Survey Data, "
            "v.1a, School Membership"
        ),
        "url": "https://nces.ed.gov/ccd/data/zip/ccd_sch_052_2223_l_1a_083023.zip",
        "date": "2023-08-30",
    },
    "2023-24": {
        "title": (
            "NCES CCD 2023-24 Public Elementary/Secondary School Universe Survey Data, "
            "v.1a, School Membership"
        ),
        "url": "https://nces.ed.gov/ccd/Data/zip/ccd_sch_052_2324_l_1a_073124.zip",
        "date": "2024-07-31",
    },
}


def _parse_membership_zip_arg(value: str) -> PublicCcdMembershipSource:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Expected SCHOOL_YEAR=/path/to/ccd_membership.zip")
    school_year, path = value.split("=", 1)
    school_year = school_year.strip()
    if school_year not in CCD_SOURCE_BY_SCHOOL_YEAR:
        expected = ", ".join(sorted(CCD_SOURCE_BY_SCHOOL_YEAR))
        raise argparse.ArgumentTypeError(
            f"Unsupported school year {school_year!r}; expected one of {expected}"
        )
    metadata = CCD_SOURCE_BY_SCHOOL_YEAR[school_year]
    return PublicCcdMembershipSource(
        school_year=school_year,
        zip_path=Path(path).expanduser(),
        source_title=metadata["title"],
        source_url=metadata["url"],
        source_date=metadata["date"],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--membership-zip",
        action="append",
        type=_parse_membership_zip_arg,
        required=True,
        help=(
            "Repeatable SCHOOL_YEAR=/path/to/ccd membership ZIP, "
            "e.g. 2023-24=/tmp/ccd_sch_052_2324_l_1a_073124.zip."
        ),
    )
    parser.add_argument(
        "--school-roster-csv",
        type=Path,
        default=ROOT / "data" / "processed" / "school_roster.csv",
    )
    parser.add_argument(
        "--school-id",
        action="append",
        default=[],
        help="Canonical public school_id to extract. Defaults to the two Freedom High School rows.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=ROOT / "data" / "interim" / "public_grade11_enrollment_nces_supplement.csv",
    )
    args = parser.parse_args()

    target_school_ids = set(args.school_id or DEFAULT_TARGET_SCHOOL_IDS)
    rows = extract_public_ccd_membership_grade11_rows(
        school_roster_rows=load_csv_rows(args.school_roster_csv),
        sources=args.membership_zip,
        target_school_ids=target_school_ids,
    )
    write_csv(args.output_csv, rows)
    print(f"wrote {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
