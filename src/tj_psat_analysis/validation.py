"""Validation helpers for source-backed panel data."""

from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_NMSF_SOURCE_FIELDS = (
    "nmsf_source_title",
    "nmsf_source_url",
    "nmsf_source_date",
    "nmsf_source_hash",
)


def _is_numeric(value: str) -> bool:
    if value is None or str(value).strip() == "":
        return False
    try:
        float(str(value))
    except ValueError:
        return False
    return True


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def nmsf_source_violations(rows: list[dict[str, str]]) -> list[str]:
    violations: list[str] = []
    for index, row in enumerate(rows, start=2):
        nmsf_count = row.get("nmsf_count", "")
        status = row.get("nmsf_status", "")
        if _is_numeric(nmsf_count):
            missing = [field for field in REQUIRED_NMSF_SOURCE_FIELDS if not row.get(field, "").strip()]
            if missing:
                school = row.get("school", "<unknown school>")
                class_year = row.get("class_year", "<unknown class>")
                violations.append(
                    f"row {index}: {school} class {class_year} numeric NMSF count "
                    f"missing {', '.join(missing)}"
                )
        elif not status.strip():
            school = row.get("school", "<unknown school>")
            class_year = row.get("class_year", "<unknown class>")
            violations.append(f"row {index}: {school} class {class_year} blank NMSF count missing status")
    return violations
