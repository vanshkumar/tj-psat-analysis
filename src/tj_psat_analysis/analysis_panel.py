"""Build the analytical panel."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path

from tj_psat_analysis.nmsf.schema import NUMERIC_NMSF_STATUSES

ANALYSIS_PANEL_FIELDNAMES = (
    "school_id",
    "school",
    "sector",
    "analytical_unit_type",
    "division",
    "district_name",
    "tj_pathway",
    "pathway_status",
    "pathway_assignment_method",
    "pathway_bucket_interpretation",
    "class_year",
    "qualifying_psat_year",
    "grade11_school_year",
    "nmsf_count",
    "nmsf_status",
    "nmsf_count_available",
    "nmsf_source_id",
    "nmsf_source_title",
    "nmsf_source_url",
    "nmsf_source_date",
    "nmsf_source_hash",
    "nmsf_source_scope",
    "source_completeness",
    "observation_basis",
    "grade11_enrollment",
    "enrollment_status",
    "grade11_enrollment_available",
    "enrollment_source_title",
    "enrollment_source_url",
    "enrollment_source_date",
    "enrollment_source_hash",
    "enrollment_source_file",
    "enrollment_source_rows",
    "enrollment_source_variable",
    "nmsf_per_100_juniors",
    "rate_status",
    "rate_input_compatible",
    "row_coverage_status",
    "denominator_gap_flag",
    "nmsf_missingness_flag",
    "school_history_event_types",
    "row_history_flags",
    "has_school_opening_flag",
    "has_school_rename_flag",
    "has_school_relocation_flag",
    "pathway_operating_school_rows",
    "pathway_compatible_school_rows",
    "pathway_missing_nmsf_school_rows",
    "pathway_missing_enrollment_school_rows",
    "pathway_incompatible_school_rows",
    "pathway_nmsf_count_covered",
    "pathway_grade11_enrollment_covered",
    "pathway_nmsf_per_100_juniors_covered",
    "pathway_coverage_status",
    "pathway_has_complete_compatible_coverage",
    "va_nmsf_selection_index_cutoff",
    "va_nmsf_selection_index_cutoff_status",
    "va_nmsf_selection_index_cutoff_source_title",
    "va_nmsf_selection_index_cutoff_source_url",
    "va_nmsf_selection_index_cutoff_source_date",
    "va_nmsf_selection_index_cutoff_source_hash",
    "statewide_nmsf_semifinalist_total",
    "statewide_nmsf_semifinalist_total_status",
    "statewide_nmsf_semifinalist_total_source_title",
    "statewide_nmsf_semifinalist_total_source_url",
    "statewide_nmsf_semifinalist_total_source_date",
    "statewide_nmsf_semifinalist_total_source_hash",
    "denominator_type",
    "admissions_seat_allocation_input",
    "admissions_seat_allocation_input_status",
    "nces_school_id",
    "pss_ppin",
    "pss_imputation_flag",
    "notes",
)

FINAL_CHECK_FIELDNAMES = (
    "check",
    "status",
    "detail",
)


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_analysis_panel(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ANALYSIS_PANEL_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_analysis_outputs(
    *,
    school_roster_csv: Path,
    nmsf_observations_csv: Path,
    enrollment_panel_csv: Path,
    class_year_mapping_csv: Path,
    school_history_csv: Path,
    statewide_totals_csv: Path | None = None,
    processed_dir: Path,
    report_dir: Path,
) -> dict[str, Path]:
    roster_rows = load_csv_rows(school_roster_csv)
    nmsf_rows = load_csv_rows(nmsf_observations_csv)
    enrollment_rows = load_csv_rows(enrollment_panel_csv)
    class_year_rows = load_csv_rows(class_year_mapping_csv)
    history_rows = load_csv_rows(school_history_csv)
    statewide_total_rows = (
        load_csv_rows(statewide_totals_csv) if statewide_totals_csv and statewide_totals_csv.exists() else []
    )

    panel_rows = build_analysis_panel_rows(
        roster_rows=roster_rows,
        nmsf_rows=nmsf_rows,
        enrollment_rows=enrollment_rows,
        class_year_rows=class_year_rows,
        history_rows=history_rows,
        statewide_total_rows=statewide_total_rows,
    )
    checks = final_panel_checks(panel_rows)

    outputs = {
        "analysis_panel": processed_dir / "analysis_panel.csv",
        "final_panel_checks_md": report_dir / "final_panel_checks.md",
    }
    write_analysis_panel(outputs["analysis_panel"], panel_rows)
    outputs["final_panel_checks_md"].parent.mkdir(parents=True, exist_ok=True)
    outputs["final_panel_checks_md"].write_text(
        build_final_panel_report(panel_rows, checks), encoding="utf-8"
    )
    return outputs


def build_analysis_panel_rows(
    *,
    roster_rows: Sequence[Mapping[str, str]],
    nmsf_rows: Sequence[Mapping[str, str]],
    enrollment_rows: Sequence[Mapping[str, str]],
    class_year_rows: Sequence[Mapping[str, str]],
    history_rows: Sequence[Mapping[str, str]],
    statewide_total_rows: Sequence[Mapping[str, str]] = (),
) -> list[dict[str, object]]:
    roster_by_school_id = _index_unique(roster_rows, ("school_id",), "school roster")
    nmsf_by_key = _index_unique(nmsf_rows, ("school_id", "class_year"), "NMSF observations")
    enrollment_by_key = _index_unique(enrollment_rows, ("school_id", "class_year"), "enrollment panel")
    class_year_by_year = _index_unique(class_year_rows, ("class_year",), "class-year mapping")
    statewide_total_by_year = _index_unique(
        statewide_total_rows,
        ("class_year",),
        "Virginia statewide NMSF totals",
        allow_empty=True,
    )
    class_years = [row["class_year"] for row in class_year_rows]
    history_by_school_id = _history_by_school_id(history_rows)

    expected_keys: set[tuple[str, ...]] = {
        (roster_row["school_id"], class_year) for roster_row in roster_rows for class_year in class_years
    }
    _validate_keys("NMSF observations", set(nmsf_by_key), expected_keys)
    _validate_keys("enrollment panel", set(enrollment_by_key), expected_keys)

    rows: list[dict[str, object]] = []
    for roster_row in roster_rows:
        school_id = roster_row["school_id"]
        history_events = history_by_school_id.get(school_id, [])
        for class_year in class_years:
            key = (school_id, class_year)
            nmsf_row = nmsf_by_key[key]
            enrollment_row = enrollment_by_key[key]
            class_year_row = class_year_by_year[(class_year,)]
            _validate_grade11_mapping(key, nmsf_row, enrollment_row, class_year_row)
            rows.append(
                _analysis_row(
                    roster_row=roster_by_school_id[(school_id,)],
                    nmsf_row=nmsf_row,
                    enrollment_row=enrollment_row,
                    class_year_row=class_year_row,
                    history_events=history_events,
                    statewide_total_row=statewide_total_by_year.get((class_year,), {}),
                )
            )

    _apply_pathway_aggregates(rows)
    return [{field: row.get(field, "") for field in ANALYSIS_PANEL_FIELDNAMES} for row in rows]


def final_panel_checks(rows: Sequence[Mapping[str, object]]) -> list[dict[str, str]]:
    keys = [(str(row["school_id"]), str(row["class_year"])) for row in rows]
    duplicate_count = len(keys) - len(set(keys))
    nmsf_source_violations = [
        row
        for row in rows
        if _int_or_none(str(row.get("nmsf_count", ""))) is not None
        and not all(
            str(row.get(field, "")).strip()
            for field in (
                "nmsf_source_title",
                "nmsf_source_url",
                "nmsf_source_date",
                "nmsf_source_hash",
            )
        )
    ]
    invalid_rates = [
        row
        for row in rows
        if str(row.get("nmsf_per_100_juniors", "")).strip() and row.get("rate_status") != "calculated"
    ]
    pathway_observed_flags = [
        row
        for row in rows
        if "observed_admissions_pathway" not in str(row.get("pathway_bucket_interpretation", ""))
        and str(row.get("pathway_bucket_interpretation", "")) != "single_tjhsst_row_not_split_to_base_schools"
    ]
    checks = [
        _check_row("unique_school_class_year", duplicate_count == 0, f"duplicate rows: {duplicate_count}"),
        _check_row(
            "nmsf_numeric_source_metadata", not nmsf_source_violations, _count_detail(nmsf_source_violations)
        ),
        _check_row("rate_null_behavior", not invalid_rates, _count_detail(invalid_rates)),
        _check_row("pathway_bucket_flags", not pathway_observed_flags, _count_detail(pathway_observed_flags)),
        _check_row(
            "selection_index_placeholder",
            {str(row["va_nmsf_selection_index_cutoff_status"]) for row in rows} == {"not_sourced"},
            "Virginia cutoff columns are documented placeholders.",
        ),
        _check_row(
            "statewide_total_source_metadata",
            not _statewide_total_source_violations(rows),
            "Sourced statewide total rows include source metadata; unsourced years remain placeholders.",
        ),
    ]
    return checks


def _statewide_total_source_violations(rows: Sequence[Mapping[str, object]]) -> list[Mapping[str, object]]:
    violations: list[Mapping[str, object]] = []
    for row in rows:
        total = str(row.get("statewide_nmsf_semifinalist_total", "")).strip()
        status = str(row.get("statewide_nmsf_semifinalist_total_status", "")).strip()
        if not total:
            if status != "not_sourced":
                violations.append(row)
            continue
        if status != "source_backed_total":
            violations.append(row)
            continue
        if not all(
            str(row.get(field, "")).strip()
            for field in (
                "statewide_nmsf_semifinalist_total_source_title",
                "statewide_nmsf_semifinalist_total_source_url",
                "statewide_nmsf_semifinalist_total_source_date",
                "statewide_nmsf_semifinalist_total_source_hash",
            )
        ):
            violations.append(row)
    return violations


def build_final_panel_report(
    rows: Sequence[Mapping[str, object]],
    checks: Sequence[Mapping[str, str]],
) -> str:
    status_counts = Counter(str(row["nmsf_status"]) for row in rows)
    enrollment_counts = Counter(str(row["enrollment_status"]) for row in rows)
    rate_counts = Counter(str(row["rate_status"]) for row in rows)
    pathway_counts = Counter(str(row["pathway_coverage_status"]) for row in rows)
    source_placeholder_counts = Counter(str(row["va_nmsf_selection_index_cutoff_status"]) for row in rows)
    statewide_placeholder_counts = Counter(
        str(row["statewide_nmsf_semifinalist_total_status"]) for row in rows
    )

    lines = [
        "# Final Panel Checks",
        "",
        "This report is generated by the analysis panel builder.",
        (
            "Rates are calculated only when a source-backed NMSF count and "
            "grade-11 enrollment are both available."
        ),
        "Pathway aggregates are covered-subset totals and carry coverage flags.",
        "",
        "## Output Summary",
        "",
        _markdown_table(
            ["Output", "Rows"],
            [["data/processed/analysis_panel.csv", len(rows)]],
        ),
        "",
        "## Validation Checks",
        "",
        _markdown_table(
            ["Check", "Status", "Detail"], [[row["check"], row["status"], row["detail"]] for row in checks]
        ),
        "",
        "## NMSF Status Counts",
        "",
        _markdown_table(["NMSF status", "Rows"], _counter_rows(status_counts)),
        "",
        "## Enrollment Status Counts",
        "",
        _markdown_table(["Enrollment status", "Rows"], _counter_rows(enrollment_counts)),
        "",
        "## Rate Status Counts",
        "",
        _markdown_table(["Rate status", "Rows"], _counter_rows(rate_counts)),
        "",
        "## Pathway Coverage Status Counts",
        "",
        _markdown_table(["Pathway coverage status", "Rows"], _counter_rows(pathway_counts)),
        "",
        "## Placeholder Source Gaps",
        "",
        _markdown_table(
            ["Placeholder", "Status", "Rows"],
            [
                ["Virginia NMSF Selection Index cutoff", status, count]
                for status, count in sorted(source_placeholder_counts.items())
            ]
            + [
                ["Statewide semifinalist total", status, count]
                for status, count in sorted(statewide_placeholder_counts.items())
            ],
        ),
        "",
        "## Source Rules",
        "",
        "- `nmsf_per_100_juniors` is blank unless `nmsf_count` and `grade11_enrollment` are both present.",
        "- Pathway totals sum only rows with compatible NMSF and denominator coverage.",
        "- `missing_source` remains missing and is not converted to zero.",
        "- Grade-11 enrollment is an outcome denominator, not an admissions-seat allocation input.",
        "- Virginia cutoff fields remain `not_sourced` until reliable sources are added.",
        (
            "- Statewide total fields are populated only when a complete source-backed "
            "Virginia list is available."
        ),
        (
            "- The Class 2026 supplied-list statewide total is source-backed in the panel "
            "but pending reconciliation against the public NMSC guide total before final "
            "statewide-share use."
        ),
        "",
    ]
    return "\n".join(lines)


def _analysis_row(
    *,
    roster_row: Mapping[str, str],
    nmsf_row: Mapping[str, str],
    enrollment_row: Mapping[str, str],
    class_year_row: Mapping[str, str],
    history_events: Sequence[Mapping[str, str]],
    statewide_total_row: Mapping[str, str],
) -> dict[str, object]:
    nmsf_count = _int_or_none(nmsf_row.get("nmsf_count", ""))
    grade11_enrollment = _int_or_none(enrollment_row.get("grade11_enrollment", ""))
    nmsf_available = nmsf_count is not None and nmsf_row.get("nmsf_status") in NUMERIC_NMSF_STATUSES
    enrollment_available = grade11_enrollment is not None and grade11_enrollment > 0
    rate_status = _rate_status(
        nmsf_available=nmsf_available,
        enrollment_available=enrollment_available,
        nmsf_status=nmsf_row.get("nmsf_status", ""),
        enrollment_status=enrollment_row.get("enrollment_status", ""),
    )
    compatible = rate_status == "calculated"
    class_year = int(class_year_row["class_year"])
    history_flags = _row_history_flags(history_events, class_year)
    denominator_gap = not enrollment_available and enrollment_row.get("enrollment_status", "") not in {
        "not_operating",
        "enrollment_not_applicable",
    }
    nmsf_missing = not nmsf_available and nmsf_row.get("nmsf_status", "") not in {
        "not_operating",
        "not_applicable",
    }
    row_coverage_status = _row_coverage_status(
        compatible=compatible,
        nmsf_missing=nmsf_missing,
        denominator_gap=denominator_gap,
        nmsf_status=nmsf_row.get("nmsf_status", ""),
        enrollment_status=enrollment_row.get("enrollment_status", ""),
    )

    return {
        "school_id": roster_row["school_id"],
        "school": roster_row["school"],
        "sector": roster_row["sector"],
        "analytical_unit_type": roster_row.get("analytical_unit_type", ""),
        "division": roster_row["division"],
        "district_name": roster_row.get("district_name", ""),
        "tj_pathway": roster_row["tj_pathway"],
        "pathway_status": roster_row.get("pathway_status", ""),
        "pathway_assignment_method": roster_row.get("pathway_assignment_method", ""),
        "pathway_bucket_interpretation": _pathway_bucket_interpretation(roster_row),
        "class_year": str(class_year),
        "qualifying_psat_year": class_year_row["qualifying_psat_year"],
        "grade11_school_year": class_year_row["grade11_school_year"],
        "nmsf_count": nmsf_row.get("nmsf_count", ""),
        "nmsf_status": nmsf_row.get("nmsf_status", ""),
        "nmsf_count_available": _bool_text(nmsf_available),
        "nmsf_source_id": nmsf_row.get("source_id", ""),
        "nmsf_source_title": nmsf_row.get("nmsf_source_title", ""),
        "nmsf_source_url": nmsf_row.get("nmsf_source_url", ""),
        "nmsf_source_date": nmsf_row.get("nmsf_source_date", ""),
        "nmsf_source_hash": nmsf_row.get("nmsf_source_hash", ""),
        "nmsf_source_scope": nmsf_row.get("nmsf_source_scope", ""),
        "source_completeness": nmsf_row.get("source_completeness", ""),
        "observation_basis": nmsf_row.get("observation_basis", ""),
        "grade11_enrollment": enrollment_row.get("grade11_enrollment", ""),
        "enrollment_status": enrollment_row.get("enrollment_status", ""),
        "grade11_enrollment_available": _bool_text(enrollment_available),
        "enrollment_source_title": enrollment_row.get("enrollment_source_title", ""),
        "enrollment_source_url": enrollment_row.get("enrollment_source_url", ""),
        "enrollment_source_date": enrollment_row.get("enrollment_source_date", ""),
        "enrollment_source_hash": enrollment_row.get("enrollment_source_hash", ""),
        "enrollment_source_file": enrollment_row.get("enrollment_source_file", ""),
        "enrollment_source_rows": enrollment_row.get("enrollment_source_rows", ""),
        "enrollment_source_variable": enrollment_row.get("enrollment_source_variable", ""),
        "nmsf_per_100_juniors": _rate_text(nmsf_count, grade11_enrollment) if compatible else "",
        "rate_status": rate_status,
        "rate_input_compatible": _bool_text(compatible),
        "row_coverage_status": row_coverage_status,
        "denominator_gap_flag": _bool_text(denominator_gap),
        "nmsf_missingness_flag": _bool_text(nmsf_missing),
        "school_history_event_types": _history_event_types(history_events),
        "row_history_flags": "|".join(history_flags),
        "has_school_opening_flag": _bool_text(_has_event(history_events, "opening")),
        "has_school_rename_flag": _bool_text(_has_event(history_events, "rename")),
        "has_school_relocation_flag": _bool_text(_has_event(history_events, "relocation")),
        "va_nmsf_selection_index_cutoff": "",
        "va_nmsf_selection_index_cutoff_status": "not_sourced",
        "va_nmsf_selection_index_cutoff_source_title": "",
        "va_nmsf_selection_index_cutoff_source_url": "",
        "va_nmsf_selection_index_cutoff_source_date": "",
        "va_nmsf_selection_index_cutoff_source_hash": "",
        "statewide_nmsf_semifinalist_total": statewide_total_row.get("statewide_nmsf_semifinalist_total", ""),
        "statewide_nmsf_semifinalist_total_status": statewide_total_row.get(
            "statewide_nmsf_semifinalist_total_status", "not_sourced"
        ),
        "statewide_nmsf_semifinalist_total_source_title": statewide_total_row.get("source_title", ""),
        "statewide_nmsf_semifinalist_total_source_url": statewide_total_row.get("source_url", ""),
        "statewide_nmsf_semifinalist_total_source_date": statewide_total_row.get("source_date", ""),
        "statewide_nmsf_semifinalist_total_source_hash": statewide_total_row.get("source_hash", ""),
        "denominator_type": "grade11_enrollment_outcome_denominator",
        "admissions_seat_allocation_input": "",
        "admissions_seat_allocation_input_status": "not_included_requires_sourced_8th_grade_population",
        "nces_school_id": enrollment_row.get("nces_school_id") or roster_row.get("nces_school_id", ""),
        "pss_ppin": enrollment_row.get("pss_ppin", ""),
        "pss_imputation_flag": enrollment_row.get("pss_imputation_flag", ""),
        "notes": _combined_notes(roster_row, nmsf_row, enrollment_row, history_events),
    }


def _apply_pathway_aggregates(rows: list[dict[str, object]]) -> None:
    groups: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[(str(row["tj_pathway"]), str(row["class_year"]))].append(row)

    for group in groups.values():
        operating_rows = [
            row
            for row in group
            if row["nmsf_status"] != "not_operating" and row["enrollment_status"] != "not_operating"
        ]
        compatible_rows = [row for row in operating_rows if row["rate_input_compatible"] == "true"]
        missing_nmsf = sum(1 for row in operating_rows if row["nmsf_count_available"] != "true")
        missing_enrollment = sum(1 for row in operating_rows if row["grade11_enrollment_available"] != "true")
        nmsf_total = sum(int(str(row["nmsf_count"])) for row in compatible_rows)
        enrollment_total = sum(int(str(row["grade11_enrollment"])) for row in compatible_rows)
        pathway_rate = _rate_text(nmsf_total, enrollment_total) if enrollment_total else ""
        coverage_status = _pathway_coverage_status(
            operating_count=len(operating_rows),
            compatible_count=len(compatible_rows),
        )
        for row in group:
            row.update(
                {
                    "pathway_operating_school_rows": str(len(operating_rows)),
                    "pathway_compatible_school_rows": str(len(compatible_rows)),
                    "pathway_missing_nmsf_school_rows": str(missing_nmsf),
                    "pathway_missing_enrollment_school_rows": str(missing_enrollment),
                    "pathway_incompatible_school_rows": str(len(operating_rows) - len(compatible_rows)),
                    "pathway_nmsf_count_covered": str(nmsf_total) if compatible_rows else "",
                    "pathway_grade11_enrollment_covered": str(enrollment_total) if compatible_rows else "",
                    "pathway_nmsf_per_100_juniors_covered": pathway_rate,
                    "pathway_coverage_status": coverage_status,
                    "pathway_has_complete_compatible_coverage": _bool_text(
                        coverage_status == "complete_compatible_coverage"
                    ),
                }
            )


def _index_unique(
    rows: Sequence[Mapping[str, str]],
    fields: Sequence[str],
    label: str,
    *,
    allow_empty: bool = False,
) -> dict[tuple[str, ...], Mapping[str, str]]:
    output: dict[tuple[str, ...], Mapping[str, str]] = {}
    for row_number, row in enumerate(rows, start=2):
        key = tuple(str(row.get(field, "")).strip() for field in fields)
        if not all(key):
            if allow_empty and not any(str(value).strip() for value in row.values()):
                continue
            raise ValueError(f"{label} row {row_number} has blank key field in {fields}")
        if key in output:
            raise ValueError(f"{label} has duplicate key {key}")
        output[key] = row
    return output


def _validate_keys(label: str, actual: set[tuple[str, ...]], expected: set[tuple[str, ...]]) -> None:
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise ValueError(f"{label} key mismatch; missing={missing[:5]} extra={extra[:5]}")


def _validate_grade11_mapping(
    key: tuple[str, str],
    nmsf_row: Mapping[str, str],
    enrollment_row: Mapping[str, str],
    class_year_row: Mapping[str, str],
) -> None:
    expected = class_year_row["grade11_school_year"]
    if nmsf_row["grade11_school_year"] != expected:
        raise ValueError(f"NMSF row {key} has grade11_school_year {nmsf_row['grade11_school_year']}")
    if enrollment_row["grade11_school_year"] != expected:
        raise ValueError(
            f"Enrollment row {key} has grade11_school_year {enrollment_row['grade11_school_year']}"
        )


def _history_by_school_id(
    rows: Sequence[Mapping[str, str]],
) -> dict[str, list[Mapping[str, str]]]:
    output: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        school_id = row.get("school_id", "").strip()
        if school_id:
            output[school_id].append(row)
    return output


def _pathway_bucket_interpretation(roster_row: Mapping[str, str]) -> str:
    method = roster_row.get("pathway_assignment_method", "")
    if method == "single_tjhsst_row":
        return "single_tjhsst_row_not_split_to_base_schools"
    if method == "nonpublic_unallocated_seats":
        return "nonpublic_unallocated_bucket_not_observed_admissions_pathway"
    return "analytical_geography_not_observed_admissions_pathway"


def _rate_status(
    *,
    nmsf_available: bool,
    enrollment_available: bool,
    nmsf_status: str,
    enrollment_status: str,
) -> str:
    if nmsf_available and enrollment_available:
        return "calculated"
    if nmsf_status == "not_operating" or enrollment_status == "not_operating":
        return "not_operating"
    if not nmsf_available and not enrollment_available:
        return "missing_nmsf_and_grade11_enrollment"
    if not nmsf_available:
        return "missing_nmsf_count"
    return "missing_grade11_enrollment"


def _row_coverage_status(
    *,
    compatible: bool,
    nmsf_missing: bool,
    denominator_gap: bool,
    nmsf_status: str,
    enrollment_status: str,
) -> str:
    if compatible:
        return "compatible"
    if nmsf_status == "not_operating" or enrollment_status == "not_operating":
        return "not_operating"
    if nmsf_missing and denominator_gap:
        return "nmsf_and_denominator_gap"
    if nmsf_missing:
        return "nmsf_gap"
    if denominator_gap:
        return "denominator_gap"
    return "incompatible"


def _pathway_coverage_status(*, operating_count: int, compatible_count: int) -> str:
    if operating_count == 0:
        return "no_operating_rows"
    if compatible_count == 0:
        return "no_compatible_rows"
    if compatible_count == operating_count:
        return "complete_compatible_coverage"
    return "partial_compatible_coverage"


def _history_event_types(events: Sequence[Mapping[str, str]]) -> str:
    return "|".join(sorted({event.get("event_type", "") for event in events if event.get("event_type")}))


def _row_history_flags(events: Sequence[Mapping[str, str]], class_year: int) -> list[str]:
    flags: list[str] = []
    for event in events:
        event_type = event.get("event_type", "")
        first_affected = _int_or_none(event.get("first_affected_class_year", ""))
        if event_type == "opening" and first_affected is not None and class_year < first_affected:
            flags.append("pre_opening")
        if first_affected is not None and class_year >= first_affected:
            flags.append(event_type)
    return sorted(set(flags))


def _has_event(events: Sequence[Mapping[str, str]], event_type: str) -> bool:
    return any(event.get("event_type") == event_type for event in events)


def _combined_notes(
    roster_row: Mapping[str, str],
    nmsf_row: Mapping[str, str],
    enrollment_row: Mapping[str, str],
    history_events: Sequence[Mapping[str, str]],
) -> str:
    notes = [
        roster_row.get("notes", ""),
        nmsf_row.get("notes", ""),
        enrollment_row.get("notes", ""),
        *[event.get("source_note", "") for event in history_events],
    ]
    return " | ".join(note.strip() for note in notes if note and note.strip())


def _int_or_none(value: object) -> int | None:
    text = str(value or "").strip().replace(",", "")
    if not text:
        return None
    try:
        parsed = int(text)
    except ValueError:
        return None
    return parsed


def _rate_text(nmsf_count: int | None, grade11_enrollment: int | None) -> str:
    if nmsf_count is None or grade11_enrollment is None or grade11_enrollment <= 0:
        return ""
    return f"{(nmsf_count / grade11_enrollment) * 100:.6f}"


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def _check_row(check: str, passed: bool, detail: str) -> dict[str, str]:
    return {"check": check, "status": "pass" if passed else "fail", "detail": detail}


def _count_detail(rows: Sequence[Mapping[str, object]]) -> str:
    return f"affected rows: {len(rows)}"


def _counter_rows(counter: Counter[str]) -> list[list[object]]:
    return [[key or "(blank)", value] for key, value in sorted(counter.items())]


def _markdown_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    rendered = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        rendered.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(rendered)
