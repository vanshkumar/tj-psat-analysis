#!/usr/bin/env python3
"""Create count-only snapshots from complete NMSC Virginia list PDFs."""

from __future__ import annotations

import argparse
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.nmsf.observations import load_csv_rows  # noqa: E402
from tj_psat_analysis.nmsf.virginia_list import (  # noqa: E402
    combine_statewide_total_rows,
    parse_virginia_list_text,
    read_pdf_lines,
    selection_unit_only_statewide_total_row,
    snapshot_rows,
    statewide_total_row,
    write_snapshot_csv,
    write_statewide_totals_csv,
)


@dataclass(frozen=True)
class VirginiaListSource:
    class_year: int
    source_id: str
    pdf_path: Path
    snapshot_path: Path
    source_title: str
    source_url: str
    source_date: str


SOURCES = (
    VirginiaListSource(
        class_year=2023,
        source_id="nmsc_virginia_2023_semifinalists",
        pdf_path=ROOT
        / "data"
        / "raw"
        / "nmsf"
        / "virginia"
        / "supplied_lists"
        / "virginia_2023_supplied_list.pdf",
        snapshot_path=ROOT
        / "data"
        / "raw"
        / "nmsf"
        / "virginia"
        / "virginia_2023_semifinalists_snapshot.csv",
        source_title="Semifinalists in the 2023 National Merit Scholarship Program - Virginia list",
        source_url="https://drive.google.com/file/d/1lukNgBPkoLPTaAptU7YrhkG8YtauqYqa/view",
        source_date="2022-09-14",
    ),
    VirginiaListSource(
        class_year=2024,
        source_id="nmsc_virginia_2024_semifinalists",
        pdf_path=ROOT
        / "data"
        / "raw"
        / "nmsf"
        / "virginia"
        / "supplied_lists"
        / "virginia_2024_supplied_list.pdf",
        snapshot_path=ROOT
        / "data"
        / "raw"
        / "nmsf"
        / "virginia"
        / "virginia_2024_semifinalists_snapshot.csv",
        source_title="Semifinalists in the 2024 National Merit Scholarship Program - Virginia list",
        source_url="https://web.archive.org/web/20230915001040if_/https%3A//litter.catbox.moe/5lujlt.pdf",
        source_date="2023-09-13",
    ),
    VirginiaListSource(
        class_year=2026,
        source_id="nmsc_virginia_2026_semifinalists",
        pdf_path=ROOT
        / "data"
        / "raw"
        / "nmsf"
        / "virginia"
        / "supplied_lists"
        / "virginia_2026_supplied_list.pdf",
        snapshot_path=ROOT
        / "data"
        / "raw"
        / "nmsf"
        / "virginia"
        / "virginia_2026_semifinalists_snapshot.csv",
        source_title="Semifinalists in the 2026 National Merit Scholarship Program - Virginia list",
        source_url="https://drive.google.com/file/d/1xCdjpoXII9oTmu_hWYFqeWl5XWmTblSu/view",
        source_date="2025-09-10",
    ),
)


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
        "--statewide-totals-csv",
        type=Path,
        default=ROOT / "data" / "sources" / "virginia_statewide_totals.csv",
    )
    parser.add_argument(
        "--selection-unit-totals-csv",
        type=Path,
        default=ROOT / "data" / "sources" / "virginia_state_selection_unit_totals.csv",
    )
    args = parser.parse_args()

    school_rows = load_csv_rows(args.school_roster_csv)
    alias_rows = load_csv_rows(args.school_aliases_csv)
    selection_rows = {row["class_year"]: row for row in load_csv_rows(args.selection_unit_totals_csv)}
    statewide_rows = []
    location_years: set[str] = set()
    for source in SOURCES:
        if not source.pdf_path.exists():
            raise FileNotFoundError(
                f"Missing source PDF for Class {source.class_year}: {source.pdf_path}. "
                "Place the user-supplied NMSC Virginia list PDF at this ignored local path "
                "before regenerating the count-only snapshot."
            )
        lines = read_pdf_lines(source.pdf_path)
        counts, statewide_total = parse_virginia_list_text(
            lines=lines,
            class_year=source.class_year,
            school_roster_rows=school_rows,
            school_alias_rows=alias_rows,
        )
        rows = snapshot_rows(source_id=source.source_id, class_year=source.class_year, counts=counts)
        write_snapshot_csv(source.snapshot_path, rows)
        digest = hashlib.sha256(source.snapshot_path.read_bytes()).hexdigest()
        location_row = statewide_total_row(
            class_year=source.class_year,
            total=statewide_total,
            source_id=source.source_id,
            source_title=source.source_title,
            source_url=source.source_url,
            source_date=source.source_date,
            source_hash=digest,
        )
        selection_row = selection_rows.get(str(source.class_year))
        if selection_row is None:
            raise ValueError(f"Missing state-selection-unit total for Class {source.class_year}")
        statewide_rows.append(
            combine_statewide_total_rows(
                location_row=location_row,
                selection_unit_row=selection_row,
            )
        )
        location_years.add(str(source.class_year))
        print(
            f"{source.class_year}: wrote {source.snapshot_path} "
            f"({len(rows)} schools, statewide total {statewide_total}, sha256 {digest})"
        )

    for class_year, selection_row in selection_rows.items():
        if class_year not in location_years:
            statewide_rows.append(selection_unit_only_statewide_total_row(selection_row))

    statewide_rows.sort(key=lambda row: int(row["class_year"]))
    write_statewide_totals_csv(args.statewide_totals_csv, statewide_rows)
    print(f"wrote {args.statewide_totals_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
