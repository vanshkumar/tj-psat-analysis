"""Parse the FCPS-origin TJHSST Class 2025 source-school workbook."""

from __future__ import annotations

import csv
import hashlib
import re
import zipfile
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from xml.etree import ElementTree

SHEET_NAMESPACE = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NAMESPACE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
EXPECTED_SOURCE_HASH = "948c91238520afab9ffe21af28d60b6c65fe11f5533428cd692b7f6698566911"
EXPECTED_SHEET_NAME = "2025 by Middle School"
PRIVACY_NOTE = 'Values represented as "TS" reference 10 or fewer students to protect student privacy'

ROW_FIELDNAMES = (
    "source_id",
    "class_year",
    "source_row_id",
    "source_school_name",
    "applicants",
    "applicants_status",
    "applicants_lower_bound",
    "applicants_upper_bound",
    "waitpool",
    "waitpool_status",
    "waitpool_lower_bound",
    "waitpool_upper_bound",
    "offered",
    "offered_status",
    "offered_lower_bound",
    "offered_upper_bound",
    "source_sheet",
    "source_row",
    "source_url",
    "source_modified_date",
    "source_file",
    "source_hash",
)

SUMMARY_FIELDNAMES = (
    "source_id",
    "class_year",
    "metric",
    "value",
    "value_status",
    "exact_rows",
    "suppressed_rows",
    "sum_of_exact_cells",
    "source_cell",
    "source_url",
    "source_hash",
    "notes",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_source_metadata(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError(f"Expected one TJHSST admissions source row in {path}, found {len(rows)}")
    return rows[0]


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
    namespace = {"x": SHEET_NAMESPACE}
    output: list[str] = []
    for item in root.findall("x:si", namespace):
        output.append("".join(node.text or "" for node in item.findall(".//x:t", namespace)))
    return output


def _sheet_name(archive: zipfile.ZipFile) -> str:
    root = ElementTree.fromstring(archive.read("xl/workbook.xml"))
    namespace = {"x": SHEET_NAMESPACE, "r": REL_NAMESPACE}
    sheets = root.findall("x:sheets/x:sheet", namespace)
    if len(sheets) != 1:
        raise ValueError(f"Expected one workbook sheet, found {len(sheets)}")
    return sheets[0].attrib["name"]


def _cell_value(cell: ElementTree.Element, shared_strings: Sequence[str]) -> str:
    namespace = {"x": SHEET_NAMESPACE}
    value_node = cell.find("x:v", namespace)
    if value_node is None or value_node.text is None:
        return ""
    value = value_node.text
    if cell.attrib.get("t") == "s":
        return shared_strings[int(value)]
    return _clean_numeric(value)


def _clean_numeric(value: str) -> str:
    number = float(value)
    if number.is_integer():
        return str(int(number))
    return format(number, ".10g")


def _column(reference: str) -> str:
    match = re.match(r"([A-Z]+)", reference)
    if match is None:
        raise ValueError(f"Invalid cell reference: {reference}")
    return match.group(1)


def _count_fields(value: str) -> tuple[str, str, str, str]:
    if value == "TS":
        return "", "suppressed_10_or_fewer", "0", "10"
    if value:
        parsed = int(value)
        return str(parsed), "reported_exact", str(parsed), str(parsed)
    return "", "not_reported", "", ""


def parse_workbook_rows(
    workbook_path: Path,
    source: Mapping[str, str],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    source_hash = sha256_file(workbook_path)
    if source_hash != EXPECTED_SOURCE_HASH or source_hash != source["source_hash"]:
        raise ValueError(f"Unexpected TJHSST admissions workbook hash: {source_hash}")

    with zipfile.ZipFile(workbook_path) as archive:
        shared_strings = _shared_strings(archive)
        sheet_name = _sheet_name(archive)
        if sheet_name != EXPECTED_SHEET_NAME or sheet_name != source["source_sheet"]:
            raise ValueError(f"Unexpected TJHSST admissions sheet: {sheet_name}")
        if not any(PRIVACY_NOTE in value for value in shared_strings):
            raise ValueError("Workbook FERPA suppression note was not found")

        root = ElementTree.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        namespace = {"x": SHEET_NAMESPACE}
        raw_rows: dict[int, dict[str, str]] = {}
        for row in root.findall("x:sheetData/x:row", namespace):
            row_number = int(row.attrib["r"])
            raw_rows[row_number] = {
                _column(cell.attrib["r"]): _cell_value(cell, shared_strings)
                for cell in row.findall("x:c", namespace)
            }

    headers = raw_rows.get(1, {})
    expected_headers = {"A": "School", "B": "Applicants", "C": "Waitpool", "D": "Offered"}
    if any(headers.get(column) != label for column, label in expected_headers.items()):
        raise ValueError(f"Unexpected admissions headers: {headers}")

    rows: list[dict[str, str]] = []
    for row_number in sorted(raw_rows):
        if row_number == 1:
            continue
        values = raw_rows[row_number]
        school = values.get("A", "").strip()
        if not school:
            continue
        applicants = _count_fields(values.get("B", ""))
        waitpool = _count_fields(values.get("C", ""))
        offered = _count_fields(values.get("D", ""))
        rows.append(
            {
                "source_id": source["source_id"],
                "class_year": source["class_year"],
                "source_row_id": f"row_{row_number:03d}",
                "source_school_name": school,
                "applicants": applicants[0],
                "applicants_status": applicants[1],
                "applicants_lower_bound": applicants[2],
                "applicants_upper_bound": applicants[3],
                "waitpool": waitpool[0],
                "waitpool_status": waitpool[1],
                "waitpool_lower_bound": waitpool[2],
                "waitpool_upper_bound": waitpool[3],
                "offered": offered[0],
                "offered_status": offered[1],
                "offered_lower_bound": offered[2],
                "offered_upper_bound": offered[3],
                "source_sheet": sheet_name,
                "source_row": str(row_number),
                "source_url": source["source_url"],
                "source_modified_date": source["source_date"],
                "source_file": source["source_file"],
                "source_hash": source_hash,
            }
        )

    summary_rows: list[dict[str, str]] = []
    for metric in ("applicants", "waitpool", "offered"):
        statuses = Counter(row[f"{metric}_status"] for row in rows)
        exact_sum = sum(int(row[metric]) for row in rows if row[metric])
        summary_rows.append(
            {
                "source_id": source["source_id"],
                "class_year": source["class_year"],
                "metric": metric,
                "value": "",
                "value_status": "cell_coverage_summary",
                "exact_rows": str(statuses["reported_exact"]),
                "suppressed_rows": str(statuses["suppressed_10_or_fewer"]),
                "sum_of_exact_cells": str(exact_sum),
                "source_cell": "",
                "source_url": source["source_url"],
                "source_hash": source_hash,
                "notes": "Sum covers unsuppressed cells only and is not the full admissions total.",
            }
        )

    for metric, cell, raw_value in (
        ("waitpool_gpa_average", "H2", raw_rows.get(2, {}).get("H", "")),
        ("not_offered_gpa_average", "J2", raw_rows.get(2, {}).get("J", "")),
    ):
        summary_rows.append(
            {
                "source_id": source["source_id"],
                "class_year": source["class_year"],
                "metric": metric,
                "value": raw_value,
                "value_status": "reported_workbook_summary",
                "exact_rows": "",
                "suppressed_rows": "",
                "sum_of_exact_cells": "",
                "source_cell": cell,
                "source_url": source["source_url"],
                "source_hash": source_hash,
                "notes": "Workbook-level summary; not attributed to the source school in row 2.",
            }
        )
    return rows, summary_rows


def write_csv(path: Path, rows: Sequence[Mapping[str, str]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_report(
    rows: Sequence[Mapping[str, str]],
    summary_rows: Sequence[Mapping[str, str]],
    source: Mapping[str, str],
) -> str:
    coverage = [row for row in summary_rows if row["value_status"] == "cell_coverage_summary"]
    lines = [
        "# TJHSST Class 2025 Admissions By Source School",
        "",
        "This report is generated from the archived FCPS-origin FOIA workbook mirrored by FCAG.",
        "It preserves source-school labels verbatim and does not join them to the high-school NMSF panel.",
        "",
        f"- Source rows: {len(rows)}",
        f"- Source sheet: `{source['source_sheet']}`",
        f"- Source URL: {source['source_url']}",
        f"- Source SHA-256: `{source['source_hash']}`",
        "",
        "## Cell Coverage",
        "",
        "| Metric | Exact rows | TS rows | Sum of exact cells |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in coverage:
        lines.append(
            f"| {row['metric']} | {row['exact_rows']} | {row['suppressed_rows']} | "
            f"{row['sum_of_exact_cells']} |"
        )
    lines.extend(
        [
            "",
            "The exact-cell sums are lower-bound accounting summaries, not full admissions totals.",
            "`TS` means 10 or fewer students; suppressed cells remain blank and are never imputed.",
            "School-level offer rates are not calculated because disclosure-threshold selection makes",
            "the visible exact cells non-comparable to suppressed cells.",
            "",
            "## Remaining Gaps",
            "",
            "This source supplies partial Class 2025 applicants, waitpool, and offers by source school.",
            "It does not supply complete exact rows, acceptances, enrollment, allocation-pool status,",
            "attendance counterfactuals, or a comparable Class 2026 source-school file.",
            "",
        ]
    )
    return "\n".join(lines)


def build_admissions_outputs(
    *,
    workbook_path: Path,
    source_metadata_csv: Path,
    processed_dir: Path,
    report_dir: Path,
) -> dict[str, Path]:
    source = load_source_metadata(source_metadata_csv)
    rows, summary_rows = parse_workbook_rows(workbook_path, source)
    outputs = {
        "source_school_csv": processed_dir / "tjhsst_class_2025_admissions_by_source_school.csv",
        "summary_csv": processed_dir / "tjhsst_class_2025_admissions_summary.csv",
        "coverage_csv": report_dir.parent / "tables" / "analysis_tjhsst_class_2025_admissions_coverage.csv",
        "report_md": report_dir / "tjhsst_class_2025_admissions.md",
    }
    write_csv(outputs["source_school_csv"], rows, ROW_FIELDNAMES)
    write_csv(outputs["summary_csv"], summary_rows, SUMMARY_FIELDNAMES)
    coverage = [row for row in summary_rows if row["value_status"] == "cell_coverage_summary"]
    write_csv(outputs["coverage_csv"], coverage, SUMMARY_FIELDNAMES)
    outputs["report_md"].parent.mkdir(parents=True, exist_ok=True)
    outputs["report_md"].write_text(build_report(rows, summary_rows, source), encoding="utf-8")
    return outputs
