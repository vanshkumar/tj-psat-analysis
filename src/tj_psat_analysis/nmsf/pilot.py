"""Milestone 5 four-year NMSF pilot outputs."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path

from tj_psat_analysis.nmsf.observations import OBSERVATION_FIELDNAMES
from tj_psat_analysis.nmsf.schema import NmsfSource

PILOT_CLASS_YEARS = {"2023", "2024", "2025", "2026"}

MANUAL_REVIEW_FIELDNAMES = (
    "class_year",
    "division",
    "school_id",
    "school",
    "sector",
    "issue_type",
    "nmsf_status",
    "nmsf_count",
    "source_id",
    "source_title",
    "source_url",
    "source_date",
    "source_hash",
    "notes",
)


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_pilot_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OBSERVATION_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_manual_review_queue(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANUAL_REVIEW_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def pilot_rows(observation_rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    return [dict(row) for row in observation_rows if row["class_year"] in PILOT_CLASS_YEARS]


def build_manual_review_queue(
    rows: Sequence[Mapping[str, str]],
    *,
    sources: Mapping[str, NmsfSource],
    root: Path,
) -> list[dict[str, str]]:
    review_rows: list[dict[str, str]] = []
    for row in rows:
        if row["nmsf_status"] != "missing_source":
            continue
        review_rows.append(
            {
                "class_year": row["class_year"],
                "division": row["division"],
                "school_id": row["school_id"],
                "school": row["school"],
                "sector": row["sector"],
                "issue_type": "missing_school_year_source",
                "nmsf_status": row["nmsf_status"],
                "nmsf_count": "",
                "source_id": "",
                "source_title": "",
                "source_url": "",
                "source_date": "",
                "source_hash": "",
                "notes": (
                    "Collect an official district release, NMSC Virginia list, or "
                    "school release; do not infer zero."
                ),
            }
        )

    for source, snapshot_row in _excluded_snapshot_rows(sources=sources, root=root):
        review_rows.append(
            {
                "class_year": snapshot_row.get("class_year", str(source.graduating_class)),
                "division": _division_for_provider(source.provider),
                "school_id": "",
                "school": snapshot_row.get("school_name_source", ""),
                "sector": "",
                "issue_type": snapshot_row.get("snapshot_record_type", "excluded_source_count"),
                "nmsf_status": "not_applicable",
                "nmsf_count": snapshot_row.get("nmsf_count", ""),
                "source_id": source.source_id,
                "source_title": source.source_title,
                "source_url": source.source_url,
                "source_date": source.publication_date,
                "source_hash": source.archived_file_sha256,
                "notes": snapshot_row.get("snapshot_notes", ""),
            }
        )

    return sorted(
        review_rows,
        key=lambda item: (
            item["class_year"],
            item["division"],
            item["issue_type"],
            item["school"],
            item["source_id"],
        ),
    )


def build_reconciliation_report(
    rows: Sequence[Mapping[str, str]],
    *,
    sources: Mapping[str, NmsfSource],
    root: Path,
) -> str:
    status_counts = Counter(row["nmsf_status"] for row in rows)
    coverage_rows = _coverage_rows(rows)
    source_rows = _source_reconciliation_rows(rows, sources=sources, root=root)
    gap_rows = _source_gap_rows(rows)

    lines = [
        "# NMSF Reconciliation 2023-2026",
        "",
        "This report is generated for Milestone 5 from the source-backed NMSF observation layer.",
        (
            "TJHSST is kept as one school row; jurisdictional TJHSST subsets in "
            "APS/LCPS releases are excluded from the panel and retained only for "
            "reconciliation notes."
        ),
        "",
        "## Output Summary",
        "",
        _markdown_table(
            ["Output", "Rows"],
            [
                ["data/processed/nmsf_observations_2023_2026.csv", len(rows)],
                [
                    "reports/data_quality/manual_review_queue.csv",
                    len(build_manual_review_queue(rows, sources=sources, root=root)),
                ],
            ],
        ),
        "",
        "## Observation Status Counts",
        "",
        _markdown_table(["Status", "Rows"], _counter_rows(status_counts)),
        "",
        "## Coverage By Division And Class",
        "",
        _markdown_table(
            [
                "Class",
                "Division",
                "Rows",
                "Verified Count",
                "Verified Zero",
                "Missing Source",
                "Not Operating",
            ],
            coverage_rows,
        ),
        "",
        "## Source Reconciliation",
        "",
        _markdown_table(
            [
                "Source ID",
                "Class",
                "Reported Total",
                "In-Panel Count Total",
                "Excluded Snapshot Total",
                "Reconciled Total",
                "Status",
                "Notes",
            ],
            source_rows,
        ),
        "",
        "## Source Gaps",
        "",
        _markdown_table(["Class", "Division", "Missing Rows"], gap_rows),
        "",
        "## Source Rules",
        "",
        "- Positive counts are imported only from manifest-backed school-level source transcriptions.",
        "- Verified zeros are inferred only from manifest entries marked complete for the division scope.",
        "- Source-incomplete district totals may reconcile a source without creating school observations.",
        (
            "- APS/LCPS resident TJHSST subsets are not imported as separate TJHSST "
            "observations because the panel keeps TJHSST as one row."
        ),
        "- Missing rows remain missing; incomplete or inaccessible source searches do not become zeros.",
    ]
    return "\n".join(lines)


def _excluded_snapshot_rows(
    *,
    sources: Mapping[str, NmsfSource],
    root: Path,
) -> list[tuple[NmsfSource, dict[str, str]]]:
    output: list[tuple[NmsfSource, dict[str, str]]] = []
    for source in sources.values():
        if not source.archived_file_path:
            continue
        snapshot_path = root / source.archived_file_path
        if not snapshot_path.exists():
            continue
        for row in load_csv_rows(snapshot_path):
            record_type = row.get("snapshot_record_type", "observation_count")
            if record_type != "observation_count":
                output.append((source, row))
    return output


def _coverage_rows(rows: Sequence[Mapping[str, str]]) -> list[list[object]]:
    grouped: dict[tuple[str, str], list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["class_year"], row["division"])].append(row)

    output: list[list[object]] = []
    for (class_year, division), group in sorted(grouped.items()):
        statuses = Counter(row["nmsf_status"] for row in group)
        output.append(
            [
                class_year,
                division or "(blank)",
                len(group),
                statuses["verified_count"],
                statuses["verified_zero"],
                statuses["missing_source"],
                statuses["not_operating"],
            ]
        )
    return output


def _source_reconciliation_rows(
    rows: Sequence[Mapping[str, str]],
    *,
    sources: Mapping[str, NmsfSource],
    root: Path,
) -> list[list[object]]:
    in_panel_totals: Counter[str] = Counter()
    for row in rows:
        if row["nmsf_status"] == "verified_count" and row["source_id"]:
            in_panel_totals[row["source_id"]] += int(row["nmsf_count"])

    excluded_totals: Counter[str] = Counter()
    excluded_notes: dict[str, list[str]] = defaultdict(list)
    for source, row in _excluded_snapshot_rows(sources=sources, root=root):
        count = int(row.get("nmsf_count") or 0)
        excluded_totals[source.source_id] += count
        school_name = row.get("school_name_source", "excluded source row")
        record_type = row.get("snapshot_record_type", "")
        excluded_notes[source.source_id].append(f"{school_name}: {count} {record_type}")

    source_ids = sorted({row["source_id"] for row in rows if row.get("source_id")} | set(excluded_totals))
    output: list[list[object]] = []
    for source_id in source_ids:
        source = sources[source_id]
        reported = int(source.reported_total) if source.reported_total else None
        in_panel = in_panel_totals[source_id]
        excluded = excluded_totals[source_id]
        reconciled = in_panel + excluded
        if reported is None:
            status = "not_checked"
        elif reported == reconciled:
            status = "reconciled"
        else:
            status = "needs_review"
        notes = "; ".join(excluded_notes[source_id]) or source.reported_total_scope or ""
        output.append(
            [
                source_id,
                source.graduating_class,
                reported if reported is not None else "",
                in_panel,
                excluded,
                reconciled,
                status,
                notes,
            ]
        )
    return output


def _source_gap_rows(rows: Sequence[Mapping[str, str]]) -> list[list[object]]:
    gaps: Counter[tuple[str, str]] = Counter()
    for row in rows:
        if row["nmsf_status"] == "missing_source":
            gaps[(row["class_year"], row["division"] or "(blank)")] += 1
    return [[class_year, division, count] for (class_year, division), count in sorted(gaps.items())]


def _division_for_provider(provider: str) -> str:
    return {
        "aps": "APS",
        "fcps": "FCPS",
        "fccps": "Falls Church City",
        "lcps": "LCPS",
        "pwcs": "PWCS",
    }.get(provider, "")


def _counter_rows(counter: Counter[str]) -> list[list[object]]:
    return [[key, value] for key, value in sorted(counter.items())]


def _markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    rendered = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        rendered.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(rendered)
