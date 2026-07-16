"""Build source-backed NMSF observation rows."""

from __future__ import annotations

import csv
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path

from tj_psat_analysis.constants import CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR
from tj_psat_analysis.nmsf.manual_counts import (
    ManualNmsfCount,
    read_manual_nmsf_counts,
    source_hashes,
)
from tj_psat_analysis.nmsf.schema import NmsfSource, read_source_manifest
from tj_psat_analysis.normalize import normalize_school_name

OBSERVATION_FIELDNAMES = (
    "school_id",
    "school",
    "sector",
    "tj_pathway",
    "division",
    "class_year",
    "grade11_school_year",
    "nmsf_count",
    "nmsf_status",
    "source_id",
    "nmsf_source_title",
    "nmsf_source_url",
    "nmsf_source_date",
    "nmsf_source_hash",
    "nmsf_source_scope",
    "source_completeness",
    "observation_basis",
    "notes",
)

ZERO_INFERENCE_DIVISION_BY_SCOPE = {
    "aps_public_high_schools_in_roster": "APS",
    "fcps_public_high_schools_in_roster": "FCPS",
    "falls_church_city_public_high_schools_in_roster": "Falls Church City",
    "lcps_public_high_schools_in_roster": "LCPS",
    "pwcs_public_high_schools_in_roster": "PWCS",
}
ALL_ROSTER_ZERO_INFERENCE_SCOPES = {"virginia_rostered_schools"}

PROVIDER_TO_DIVISION = {
    "aps": "APS",
    "fcps": "FCPS",
    "fccps": "Falls Church City",
    "lcps": "LCPS",
    "pwcs": "PWCS",
}


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OBSERVATION_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_nmsf_observations(
    *,
    school_roster_csv: Path,
    school_aliases_csv: Path,
    counts_csv: Path,
    source_manifest_yml: Path,
) -> tuple[list[dict[str, str]], list[str]]:
    roster_rows = load_csv_rows(school_roster_csv)
    alias_rows = load_csv_rows(school_aliases_csv)
    records = read_manual_nmsf_counts(counts_csv)
    sources = read_source_manifest(source_manifest_yml)

    _validate_counts_against_manifest(records, sources, source_manifest_yml)
    matched_records = _match_records(records, roster_rows, alias_rows)
    source_hash_by_id = source_hashes(records)

    observations: dict[tuple[str, int], dict[str, str]] = {}
    for roster_row in roster_rows:
        for class_year, school_year in CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR.items():
            observations[(roster_row["school_id"], class_year)] = _base_observation(
                roster_row,
                class_year,
                school_year,
            )

    for key, record in matched_records.items():
        source = sources[record.source_id]
        observations[key] = _sourced_observation(
            observations[key],
            record=record,
            source=source,
            source_hash=source_hash_by_id[record.source_id],
            observation_basis="manual_transcription",
        )

    for source in sources.values():
        if source.complete_for_zero_inference:
            _apply_verified_zeros(
                observations=observations,
                roster_rows=roster_rows,
                source=source,
                source_hash=source_hash_by_id[source.source_id],
            )

    output_rows = [
        observations[(roster_row["school_id"], class_year)]
        for roster_row in roster_rows
        for class_year in CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR
    ]
    warnings = _coverage_warnings(output_rows)
    return output_rows, warnings


def _base_observation(
    roster_row: dict[str, str],
    class_year: int,
    grade11_school_year: str,
) -> dict[str, str]:
    status = "missing_source"
    basis = "no_source_recorded"
    if not _is_operating(roster_row, class_year):
        status = "not_operating"
        basis = "school_not_operating"
    return {
        "school_id": roster_row["school_id"],
        "school": roster_row["school"],
        "sector": roster_row["sector"],
        "tj_pathway": roster_row["tj_pathway"],
        "division": roster_row["division"],
        "class_year": str(class_year),
        "grade11_school_year": grade11_school_year,
        "nmsf_count": "",
        "nmsf_status": status,
        "source_id": "",
        "nmsf_source_title": "",
        "nmsf_source_url": "",
        "nmsf_source_date": "",
        "nmsf_source_hash": "",
        "nmsf_source_scope": "",
        "source_completeness": "",
        "observation_basis": basis,
        "notes": roster_row.get("notes", ""),
    }


def _is_operating(roster_row: dict[str, str], class_year: int) -> bool:
    first = roster_row.get("first_operating_class_year", "")
    last = roster_row.get("last_operating_class_year", "")
    if first and class_year < int(first):
        return False
    if last and class_year > int(last):
        return False
    return True


def _match_records(
    records: list[ManualNmsfCount],
    roster_rows: list[dict[str, str]],
    alias_rows: list[dict[str, str]],
) -> dict[tuple[str, int], ManualNmsfCount]:
    roster_by_id = {row["school_id"]: row for row in roster_rows}
    alias_index: dict[str, str] = {}
    blocked_aliases: dict[str, set[str]] = {}
    for row in alias_rows:
        normalized = row["normalized_alias"] or normalize_school_name(row["alias"])
        if not normalized:
            continue
        if row.get("join_allowed", "").lower() == "true":
            existing = alias_index.get(normalized)
            if existing and existing != row["school_id"]:
                blocked_aliases[normalized] = {existing, row["school_id"]}
                alias_index.pop(normalized, None)
            else:
                alias_index[normalized] = row["school_id"]
        else:
            blocked_aliases[normalized] = {
                school_id for school_id in row.get("conflict_school_ids", "").split("|") if school_id
            }

    matched: dict[tuple[str, int], ManualNmsfCount] = {}
    for record in records:
        normalized = normalize_school_name(record.school_name_source)
        school_id: str | None
        if normalized in blocked_aliases:
            school_id = _resolve_blocked_alias_for_provider(
                normalized=normalized,
                provider=record.provider,
                candidate_school_ids=blocked_aliases[normalized],
                roster_by_id=roster_by_id,
            )
        else:
            school_id = alias_index.get(normalized)
        if not school_id or school_id not in roster_by_id:
            raise ValueError(
                f"NMSF source row {record.source_id}/{record.school_name_source} "
                "does not match a join-allowed roster alias"
            )
        key = (school_id, record.class_year)
        if key in matched:
            raise ValueError(f"Duplicate NMSF observation for {school_id} class {record.class_year}")
        matched[key] = record
    return matched


def _resolve_blocked_alias_for_provider(
    *,
    normalized: str,
    provider: str,
    candidate_school_ids: set[str],
    roster_by_id: dict[str, dict[str, str]],
) -> str:
    division = PROVIDER_TO_DIVISION.get(provider)
    if division:
        provider_matches = [
            school_id
            for school_id in candidate_school_ids
            if roster_by_id.get(school_id, {}).get("division") == division
        ]
        if len(provider_matches) == 1:
            return provider_matches[0]
    candidates = "|".join(sorted(candidate_school_ids))
    raise ValueError(f"NMSF source row matches blocked or ambiguous alias {normalized}: {candidates}")


def _sourced_observation(
    base: dict[str, str],
    *,
    record: ManualNmsfCount,
    source: NmsfSource,
    source_hash: str,
    observation_basis: str,
) -> dict[str, str]:
    if base["nmsf_status"] == "not_operating":
        raise ValueError(f"{base['school']} class {base['class_year']} has source count while not operating")
    output = dict(base)
    output.update(
        {
            "nmsf_count": str(record.nmsf_count),
            "nmsf_status": record.nmsf_status,
            "source_id": source.source_id,
            "nmsf_source_title": source.source_title,
            "nmsf_source_url": source.source_url,
            "nmsf_source_date": source.publication_date,
            "nmsf_source_hash": source_hash,
            "nmsf_source_scope": source.source_scope,
            "source_completeness": source.completeness_scope,
            "observation_basis": observation_basis,
        }
    )
    return output


def _apply_verified_zeros(
    *,
    observations: dict[tuple[str, int], dict[str, str]],
    roster_rows: list[dict[str, str]],
    source: NmsfSource,
    source_hash: str,
) -> None:
    division = ZERO_INFERENCE_DIVISION_BY_SCOPE.get(source.zero_inference_scope)
    all_rostered_scope = source.zero_inference_scope in ALL_ROSTER_ZERO_INFERENCE_SCOPES
    if not division and not all_rostered_scope:
        raise ValueError(
            f"Unsupported zero inference scope for {source.source_id}: {source.zero_inference_scope}"
        )
    for roster_row in roster_rows:
        if division and (roster_row["division"] != division or roster_row["sector"] != "public"):
            continue
        if not _is_operating(roster_row, source.graduating_class):
            continue
        key = (roster_row["school_id"], source.graduating_class)
        observation = observations[key]
        if observation["nmsf_count"]:
            continue
        zero_record = ManualNmsfCount(
            source_id=source.source_id,
            provider=source.provider,
            class_year=source.graduating_class,
            school_name_source=roster_row["school"],
            nmsf_count=0,
            nmsf_status="verified_zero",
            source_title=source.source_title,
            source_url=source.source_url,
            source_date=source.publication_date,
            source_scope=source.source_scope,
            source_completeness=source.completeness_scope,
            source_notes=source.notes,
        )
        observations[key] = _sourced_observation(
            observation,
            record=zero_record,
            source=source,
            source_hash=source_hash,
            observation_basis="complete_source_zero_inference",
        )


def _validate_counts_against_manifest(
    records: list[ManualNmsfCount],
    sources: dict[str, NmsfSource],
    manifest_path: Path,
) -> None:
    computed_hashes = source_hashes(records)
    for source_id, computed_hash in computed_hashes.items():
        if source_id not in sources:
            raise ValueError(f"{manifest_path} missing source_id {source_id} used by NMSF counts")
        source = sources[source_id]
        if source.source_hash != computed_hash:
            raise ValueError(
                f"{manifest_path} source {source_id} hash {source.source_hash} "
                f"does not match computed hash {computed_hash}"
            )
    for record in records:
        source = sources[record.source_id]
        mismatches = []
        if record.provider != source.provider:
            mismatches.append("provider")
        if record.source_title != source.source_title:
            mismatches.append("source_title")
        if record.source_url != source.source_url:
            mismatches.append("source_url")
        if record.source_date != source.publication_date:
            mismatches.append("source_date")
        if record.source_scope != source.source_scope:
            mismatches.append("source_scope")
        if record.source_completeness != source.completeness_scope:
            mismatches.append("source_completeness")
        if mismatches:
            raise ValueError(
                f"NMSF count row {record.source_id}/{record.school_name_source} "
                f"differs from manifest fields: {', '.join(mismatches)}"
            )


def _coverage_warnings(rows: list[dict[str, str]]) -> list[str]:
    status_counts = Counter(row["nmsf_status"] for row in rows)
    warnings = [f"{status}: {count}" for status, count in sorted(status_counts.items())]
    return warnings


def build_nmsf_source_report(
    rows: list[dict[str, str]],
    warnings: list[str],
    *,
    sources: Mapping[str, NmsfSource] | None = None,
) -> str:
    status_counts = Counter(row["nmsf_status"] for row in rows)
    basis_counts = Counter(row["observation_basis"] for row in rows)
    source_counts = Counter(row["source_id"] or "(none)" for row in rows)

    lines = [
        "# NMSF Source Registry Report",
        "",
        "This report is generated from the NMSF observation builder.",
        "Counts and verified zeros are stored separately from enrollment denominators.",
        "",
        "## Output Summary",
        "",
        _markdown_table(
            ["Output", "Rows"],
            [["data/processed/nmsf_observations.csv", len(rows)]],
        ),
        "",
        "## Observation Status Counts",
        "",
        _markdown_table(["Status", "Rows"], _counter_rows(status_counts)),
        "",
        "## Observation Basis Counts",
        "",
        _markdown_table(["Basis", "Rows"], _counter_rows(basis_counts)),
        "",
        "## Source Coverage Counts",
        "",
        _markdown_table(["Source ID", "Rows"], _counter_rows(source_counts)),
        "",
        "## Archived Sources",
        "",
        _source_archive_table(sources),
        "",
        "## Source Rules",
        "",
        "- Positive NMSF counts use `verified_count` and require source metadata.",
        "- Inferred zeros use `verified_zero` only for manifest sources marked complete for the scope.",
        "- Missing schools outside a complete source scope remain `missing_source`.",
        "- Enrollment denominators and rates are intentionally excluded from this observation layer.",
        "",
        "## Machine Summary",
        "",
    ]
    lines.extend(f"- {warning}" for warning in warnings)
    return "\n".join(lines)


def _source_archive_table(sources: Mapping[str, NmsfSource] | None) -> str:
    if not sources:
        return "_No source manifest archive data was provided to this report._"
    return _markdown_table(
        ["Source ID", "Archived File", "SHA-256"],
        [
            [source.source_id, source.archived_file_path or "(none)", source.archived_file_sha256 or "(none)"]
            for source in sorted(sources.values(), key=lambda item: item.source_id)
        ],
    )


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
