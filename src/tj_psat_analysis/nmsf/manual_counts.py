"""Import source-backed manual NMSF count transcriptions."""

from __future__ import annotations

import csv
import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from tj_psat_analysis.normalize import normalize_school_name

REQUIRED_MANUAL_COUNT_FIELDS = (
    "source_id",
    "provider",
    "class_year",
    "school_name_source",
    "nmsf_count",
    "nmsf_status",
    "source_title",
    "source_url",
    "source_date",
    "source_scope",
    "source_completeness",
)

VALID_NUMERIC_STATUSES = {"verified_count", "verified_zero"}


@dataclass(frozen=True)
class ManualNmsfCount:
    source_id: str
    provider: str
    class_year: int
    school_name_source: str
    nmsf_count: int
    nmsf_status: str
    source_title: str
    source_url: str
    source_date: str
    source_scope: str
    source_completeness: str
    source_notes: str


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_manual_nmsf_counts(path: Path) -> list[ManualNmsfCount]:
    rows = load_csv_rows(path)
    records: list[ManualNmsfCount] = []
    for row_number, row in enumerate(rows, start=2):
        missing = [field for field in REQUIRED_MANUAL_COUNT_FIELDS if not (row.get(field) or "").strip()]
        if missing:
            raise ValueError(f"{path} row {row_number} missing {', '.join(missing)}")

        status = row["nmsf_status"].strip()
        if status not in VALID_NUMERIC_STATUSES:
            raise ValueError(f"{path} row {row_number} has unsupported numeric status {status!r}")

        count_text = row["nmsf_count"].strip()
        try:
            count = int(count_text)
        except ValueError as exc:
            raise ValueError(f"{path} row {row_number} has non-integer count {count_text!r}") from exc
        if count < 0:
            raise ValueError(f"{path} row {row_number} has negative count {count}")
        if count == 0 and status != "verified_zero":
            raise ValueError(f"{path} row {row_number} uses zero without verified_zero status")

        try:
            class_year = int(row["class_year"])
        except ValueError as exc:
            raise ValueError(
                f"{path} row {row_number} has non-integer class year {row['class_year']!r}"
            ) from exc

        records.append(
            ManualNmsfCount(
                source_id=row["source_id"].strip(),
                provider=row["provider"].strip(),
                class_year=class_year,
                school_name_source=row["school_name_source"].strip(),
                nmsf_count=count,
                nmsf_status=status,
                source_title=row["source_title"].strip(),
                source_url=row["source_url"].strip(),
                source_date=row["source_date"].strip(),
                source_scope=row["source_scope"].strip(),
                source_completeness=row["source_completeness"].strip(),
                source_notes=(row.get("source_notes") or "").strip(),
            )
        )
    _validate_source_metadata_consistency(records, path)
    return records


def _validate_source_metadata_consistency(records: list[ManualNmsfCount], path: Path) -> None:
    seen: dict[str, tuple[str, str, str, str, str, str]] = {}
    for record in records:
        metadata = (
            record.provider,
            record.source_title,
            record.source_url,
            record.source_date,
            record.source_scope,
            record.source_completeness,
        )
        if record.source_id in seen and seen[record.source_id] != metadata:
            raise ValueError(f"{path} has inconsistent metadata for {record.source_id}")
        seen[record.source_id] = metadata


def source_hashes(records: list[ManualNmsfCount]) -> dict[str, str]:
    grouped: dict[str, list[ManualNmsfCount]] = {}
    for record in records:
        grouped.setdefault(record.source_id, []).append(record)

    hashes: dict[str, str] = {}
    for source_id, source_records in grouped.items():
        first = source_records[0]
        lines = [
            f"source_id={first.source_id}",
            f"provider={first.provider}",
            f"source_title={first.source_title}",
            f"source_url={first.source_url}",
            f"source_date={first.source_date}",
            f"source_scope={first.source_scope}",
            f"source_completeness={first.source_completeness}",
            "counts:",
        ]
        for record in sorted(
            source_records,
            key=lambda item: (
                item.class_year,
                normalize_school_name(item.school_name_source),
                item.nmsf_count,
            ),
        ):
            lines.append(
                "|".join(
                    [
                        str(record.class_year),
                        record.school_name_source,
                        str(record.nmsf_count),
                        record.nmsf_status,
                    ]
                )
            )
        hashes[source_id] = hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
    return hashes


def build_roster_index(
    roster_rows: list[dict[str, str]],
) -> tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]]:
    index: dict[str, list[dict[str, str]]] = {}
    for row in roster_rows:
        aliases = [row["school"]]
        aliases.extend(alias for alias in row.get("aliases", "").split("|") if alias)
        for alias in aliases:
            key = normalize_school_name(alias)
            if key:
                index.setdefault(key, []).append(row)

    unique: dict[str, dict[str, str]] = {}
    ambiguous: dict[str, list[dict[str, str]]] = {}
    for key, rows in index.items():
        distinct = {row["school_id"]: row for row in rows}
        if len(distinct) == 1:
            unique[key] = next(iter(distinct.values()))
        else:
            ambiguous[key] = list(distinct.values())
    return unique, ambiguous


def match_manual_counts(
    records: list[ManualNmsfCount],
    roster_rows: list[dict[str, str]],
) -> dict[tuple[str, int], ManualNmsfCount]:
    unique_index, ambiguous_index = build_roster_index(roster_rows)
    matched: dict[tuple[str, int], ManualNmsfCount] = {}
    for record in records:
        key = normalize_school_name(record.school_name_source)
        if key in ambiguous_index:
            schools = ", ".join(row["school"] for row in ambiguous_index[key])
            raise ValueError(
                f"Manual NMSF row {record.source_id}/{record.school_name_source} "
                f"matches multiple roster schools: {schools}"
            )
        roster_row = unique_index.get(key)
        if roster_row is None:
            raise ValueError(
                f"Manual NMSF row {record.source_id}/{record.school_name_source} "
                "does not match the canonical roster"
            )
        panel_key = (roster_row["school_id"], record.class_year)
        if panel_key in matched:
            raise ValueError(
                f"Duplicate manual NMSF count for {roster_row['school']} class {record.class_year}"
            )
        matched[panel_key] = record
    return matched


def format_rate(numerator: int, denominator: str) -> str:
    try:
        denominator_value = int(float(denominator))
    except ValueError:
        return ""
    if denominator_value <= 0:
        return ""
    value = numerator / denominator_value * 100
    return f"{value:.6f}".rstrip("0").rstrip(".")


def apply_manual_counts_to_panel(
    panel_rows: list[dict[str, str]],
    roster_rows: list[dict[str, str]],
    records: list[ManualNmsfCount],
) -> list[dict[str, str]]:
    matched_records = match_manual_counts(records, roster_rows)
    hashes = source_hashes(records)
    seen_panel_keys = {(row["school_id"], int(row["class_year"])) for row in panel_rows}
    missing_panel_keys = set(matched_records).difference(seen_panel_keys)
    if missing_panel_keys:
        details = ", ".join(f"{school_id} class {year}" for school_id, year in missing_panel_keys)
        raise ValueError(f"Manual NMSF rows did not match panel rows: {details}")

    output: list[dict[str, str]] = []
    for row in panel_rows:
        copied = dict(row)
        record = matched_records.get((row["school_id"], int(row["class_year"])))
        if record:
            copied["nmsf_count"] = str(record.nmsf_count)
            copied["nmsf_status"] = record.nmsf_status
            copied["nmsf_source_title"] = record.source_title
            copied["nmsf_source_url"] = record.source_url
            copied["nmsf_source_date"] = record.source_date
            copied["nmsf_source_hash"] = hashes[record.source_id]
            copied["nmsf_source_scope"] = record.source_scope
            copied["nmsf_per_100_grade11"] = format_rate(
                record.nmsf_count,
                row.get("grade11_enrollment", ""),
            )
        output.append(copied)
    return output
