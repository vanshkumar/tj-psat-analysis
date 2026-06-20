#!/usr/bin/env python3
"""Extract Class 2025 private denominators from archived NCES locator pages."""

from __future__ import annotations

import argparse
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.enrollment import (  # noqa: E402
    PSS_LOCATOR_2023_24_SOURCE_DATE,
    PSS_LOCATOR_2023_24_SOURCE_TITLE,
    PSS_LOCATOR_2023_24_SOURCE_VARIABLE,
    PSS_LOCATOR_IMPUTATION_FLAG_STATUS,
    _parse_pss_value,
    load_csv_rows,
    sha256_file,
)
from tj_psat_analysis.seed_workbook import write_csv  # noqa: E402

SOURCE_DIR = ROOT / "data" / "raw" / "enrollment" / "pss_locator_2023_24"
DEFAULT_MAPPING = ROOT / "data" / "manual" / "private_school_pss_locator_2023_24.csv"
DEFAULT_OUTPUT = ROOT / "data" / "interim" / "private_grade11_enrollment_pss_locator_2023_24.csv"
REPORTED_CLASS_YEAR = 2025
REPORTED_SCHOOL_YEAR = "2023-24"

OUTPUT_FIELDS = [
    "school_id",
    "school",
    "class_year",
    "grade11_school_year",
    "grade11_enrollment",
    "enrollment_status",
    "enrollment_source_title",
    "enrollment_source_url",
    "enrollment_source_date",
    "enrollment_source_hash",
    "enrollment_source_file",
    "enrollment_source_rows",
    "enrollment_source_variable",
    "pss_ppin",
    "pss_name",
    "pss_city",
    "pss_zip",
    "pss_imputation_flag",
    "locator_retrieval_date",
    "locator_match_status",
    "locator_nces_school_id",
    "locator_page_type",
    "notes",
]


class LocatorTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tokens: list[str] = []
        self.detail_links: list[str] = []

    def handle_data(self, data: str) -> None:
        token = " ".join(data.split())
        if token:
            self.tokens.append(token)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        href = dict(attrs).get("href") or ""
        if "school_detail.asp" in href:
            self.detail_links.append(href)


def _download(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["curl", "-L", "--fail", "--silent", "--show-error", "--output", str(path), url],
        check=True,
    )


def _tokens_for(path: Path) -> tuple[list[str], list[str]]:
    parser = LocatorTextParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser.tokens, parser.detail_links


def _token_after(tokens: list[str], label: str) -> str:
    try:
        index = tokens.index(label)
    except ValueError:
        return ""
    if index + 1 >= len(tokens):
        return ""
    return tokens[index + 1]


def _grade11_value(tokens: list[str]) -> tuple[str, str]:
    try:
        start = tokens.index("Enrollment by Grade:")
        end = tokens.index("Enrollment by Race/Ethnicity:", start)
        students = tokens.index("Students", start, end)
    except ValueError:
        return "", "grade_table_not_found"

    headers = tokens[start + 1 : students]
    values = tokens[students + 1 : end]
    if len(values) < len(headers):
        return "", "grade_table_malformed"

    grade_values = dict(zip(headers, values, strict=False))
    if "11" not in grade_values:
        return "", "grade11_not_reported"
    return _parse_pss_value(grade_values["11"])


def _search_status(tokens: list[str], detail_links: list[str], expected_status: str) -> str:
    result_token = next((token for token in tokens if token.startswith("Search Results:")), "")
    if result_token == "Search Results: 0":
        return "locator_search_not_found"
    if len(detail_links) > 1:
        return "ambiguous_pss_id"
    return expected_status


def _base_output(row: dict[str, str], raw_path: Path, retrieval_date: str) -> dict[str, object]:
    return {
        "school_id": row["school_id"],
        "school": row["school"],
        "class_year": REPORTED_CLASS_YEAR,
        "grade11_school_year": REPORTED_SCHOOL_YEAR,
        "grade11_enrollment": "",
        "enrollment_status": row["locator_match_status"],
        "enrollment_source_title": PSS_LOCATOR_2023_24_SOURCE_TITLE,
        "enrollment_source_url": row["locator_url"],
        "enrollment_source_date": PSS_LOCATOR_2023_24_SOURCE_DATE,
        "enrollment_source_hash": sha256_file(raw_path),
        "enrollment_source_file": str(raw_path.relative_to(ROOT)),
        "enrollment_source_rows": "",
        "enrollment_source_variable": PSS_LOCATOR_2023_24_SOURCE_VARIABLE,
        "pss_ppin": row["locator_nces_school_id"],
        "pss_name": "",
        "pss_city": "",
        "pss_zip": "",
        "pss_imputation_flag": "",
        "locator_retrieval_date": retrieval_date,
        "locator_match_status": row["locator_match_status"],
        "locator_nces_school_id": row["locator_nces_school_id"],
        "locator_page_type": row["locator_page_type"],
        "notes": row.get("notes", ""),
    }


def _row_from_mapping(
    row: dict[str, str],
    source_dir: Path,
    retrieval_date: str,
    download: bool,
) -> dict[str, object]:
    raw_path = source_dir / row["raw_file"]
    if download:
        _download(row["locator_url"], raw_path)
    if not raw_path.exists():
        raise FileNotFoundError(f"{raw_path} is missing; rerun with --download or add the archive")

    tokens, detail_links = _tokens_for(raw_path)
    output = _base_output(row, raw_path, retrieval_date)

    if row["locator_page_type"] == "search":
        output["enrollment_status"] = _search_status(tokens, detail_links, row["locator_match_status"])
        output["locator_match_status"] = output["enrollment_status"]
        output["enrollment_source_rows"] = f"search detail links={len(detail_links)}"
        return output

    if row["locator_page_type"] != "detail":
        raise ValueError(f"Unsupported locator_page_type={row['locator_page_type']!r}")

    value, status = _grade11_value(tokens)
    output["grade11_enrollment"] = value
    output["enrollment_status"] = status
    output["enrollment_source_rows"] = "Enrollment by Grade: 11"
    output["pss_name"] = _token_after(tokens, "School Name:")
    output["pss_ppin"] = _token_after(tokens, "NCES School ID:") or row["locator_nces_school_id"]
    output["pss_imputation_flag"] = PSS_LOCATOR_IMPUTATION_FLAG_STATUS if value else ""
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping-csv", type=Path, default=DEFAULT_MAPPING)
    parser.add_argument("--source-dir", type=Path, default=SOURCE_DIR)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--retrieval-date", default="2026-06-20")
    parser.add_argument(
        "--download",
        action="store_true",
        help="Fetch locator pages before parsing. Without this, archived HTML files are reused.",
    )
    args = parser.parse_args()

    rows = [
        _row_from_mapping(row, args.source_dir, args.retrieval_date, args.download)
        for row in load_csv_rows(args.mapping_csv)
    ]
    write_csv(args.output_csv, [{field: row.get(field, "") for field in OUTPUT_FIELDS} for row in rows])
    print(f"wrote {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
