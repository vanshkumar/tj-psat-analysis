"""Build Milestone 8 descriptive tables, figures, and report."""

from __future__ import annotations

import csv
import html
import math
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

from tj_psat_analysis.constants import CLASS_YEARS
from tj_psat_analysis.nmsf.schema import NUMERIC_NMSF_STATUSES

CLASS_YEAR_LABELS = tuple(str(year) for year in CLASS_YEARS)

SCHOOL_COUNT_FIELDNAMES = (
    "school_group",
    "tj_pathway",
    "division",
    "school_id",
    "school",
    "class_year",
    "nmsf_count",
    "nmsf_status",
    "nmsf_count_available",
    "nmsf_source_id",
    "nmsf_source_title",
    "nmsf_source_url",
    "nmsf_source_date",
    "nmsf_source_hash",
    "count_missingness_note",
)

SCHOOL_RATE_FIELDNAMES = (
    "school_group",
    "tj_pathway",
    "division",
    "school_id",
    "school",
    "class_year",
    "nmsf_count",
    "grade11_enrollment",
    "nmsf_per_100_juniors",
    "rate_status",
    "row_coverage_status",
    "nmsf_status",
    "enrollment_status",
    "denominator_gap_flag",
    "nmsf_missingness_flag",
    "rate_missingness_note",
)

PATHWAY_HEATMAP_FIELDNAMES = (
    "tj_pathway",
    "class_year",
    "pathway_nmsf_count_covered",
    "pathway_grade11_enrollment_covered",
    "pathway_nmsf_per_100_juniors_covered",
    "pathway_operating_school_rows",
    "pathway_compatible_school_rows",
    "pathway_missing_nmsf_school_rows",
    "pathway_missing_enrollment_school_rows",
    "pathway_incompatible_school_rows",
    "pathway_coverage_status",
    "pathway_has_complete_compatible_coverage",
    "pathway_interpretation_note",
)

GROUP_TOTAL_FIELDNAMES = (
    "class_year",
    "school_group",
    "operating_school_rows",
    "nmsf_count_available_rows",
    "missing_nmsf_rows",
    "grade11_enrollment_available_rows",
    "compatible_rate_rows",
    "nmsf_count_observed_total",
    "compatible_nmsf_count_total",
    "compatible_grade11_enrollment_total",
    "nmsf_per_100_juniors_covered",
    "nmsf_count_coverage_status",
    "rate_coverage_status",
    "small_number_warning",
)

TJ_ZONE_FIELDNAMES = (
    "class_year",
    "with_tjhsst_nmsf_count_observed_total",
    "with_tjhsst_nmsf_available_rows",
    "with_tjhsst_missing_nmsf_rows",
    "without_tjhsst_nmsf_count_observed_total",
    "without_tjhsst_nmsf_available_rows",
    "without_tjhsst_missing_nmsf_rows",
    "tjhsst_nmsf_count",
    "coverage_note",
)

COVERAGE_FIELDNAMES = (
    "class_year",
    "total_rows",
    "operating_rows",
    "compatible_rows",
    "nmsf_gap_rows",
    "denominator_gap_rows",
    "nmsf_and_denominator_gap_rows",
    "not_operating_rows",
    "missing_source_rows",
)

PRE_POST_FIELDNAMES = (
    "period",
    "class_years",
    "comparison_group",
    "operating_school_year_rows",
    "nmsf_count_available_rows",
    "missing_nmsf_rows",
    "compatible_rate_rows",
    "nmsf_count_observed_total",
    "annual_average_observed_nmsf_count",
    "compatible_nmsf_count_total",
    "compatible_grade11_enrollment_total",
    "nmsf_per_100_juniors_covered",
    "nmsf_count_coverage_status",
    "rate_coverage_status",
    "small_number_warning",
)

VIRGINIA_SHARE_FIELDNAMES = (
    "class_year",
    "group",
    "nmsf_count_total",
    "missing_nmsf_rows",
    "statewide_nmsf_semifinalist_total",
    "share_of_statewide_total_pct",
    "statewide_total_status",
    "statewide_total_source_url",
    "coverage_note",
)

TABLE_SPECS = {
    "school_counts_by_year": ("school_counts_by_year.csv", SCHOOL_COUNT_FIELDNAMES),
    "school_rates_by_year": ("school_rates_by_year.csv", SCHOOL_RATE_FIELDNAMES),
    "pathway_by_class_heatmap": ("pathway_by_class_heatmap.csv", PATHWAY_HEATMAP_FIELDNAMES),
    "school_group_totals_by_class": ("school_group_totals_by_class.csv", GROUP_TOTAL_FIELDNAMES),
    "tj_zone_counts_by_class": ("tj_zone_counts_by_class.csv", TJ_ZONE_FIELDNAMES),
    "virginia_share_by_class": ("virginia_share_by_class.csv", VIRGINIA_SHARE_FIELDNAMES),
    "data_coverage_by_class": ("data_coverage_by_class.csv", COVERAGE_FIELDNAMES),
    "pre_post_summary": ("pre_post_summary_2023_2024_vs_2025_2026.csv", PRE_POST_FIELDNAMES),
}

FIGURE_FILENAMES = {
    "raw_nmsf_counts_by_school_year": "raw_nmsf_counts_by_school_year.svg",
    "nmsf_rates_by_school_year": "nmsf_rates_by_school_year.svg",
    "pathway_by_class_heatmap": "pathway_by_class_heatmap.svg",
    "tjhsst_vs_base_public_private_counts": "tjhsst_vs_base_public_private_counts.svg",
    "tj_zone_counts_with_without_tjhsst": "tj_zone_counts_with_without_tjhsst.svg",
    "public_private_counts_by_class": "public_private_counts_by_class.svg",
    "pre_post_summary": "pre_post_summary.svg",
    "data_coverage_by_class": "data_coverage_by_class.svg",
}

GROUP_ORDER = {
    "TJHSST": 0,
    "Base public schools": 1,
    "Private schools": 2,
    "Other": 3,
}

PATHWAY_ORDER = {
    "TJHSST": 0,
    "Arlington": 1,
    "Falls Church City": 2,
    "Loudoun": 3,
    "Prince William": 4,
    "FCPS Region 1": 5,
    "FCPS Region 2": 6,
    "FCPS Region 3": 7,
    "FCPS Region 4": 8,
    "FCPS Region 5": 9,
    "Private/homeschool unallocated": 10,
}

SERIES_COLORS = {
    "TJHSST": "#1d4ed8",
    "Base public schools": "#0f766e",
    "Private schools": "#b45309",
    "All schools including TJHSST": "#4f46e5",
    "All schools excluding TJHSST": "#64748b",
    "Public schools including TJHSST": "#7c3aed",
}


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_descriptive_outputs(
    *,
    analysis_panel_csv: Path,
    figures_dir: Path,
    tables_dir: Path,
    report_path: Path,
) -> dict[str, Path]:
    rows = load_csv_rows(analysis_panel_csv)
    table_rows = descriptive_table_rows(rows)

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    outputs: dict[str, Path] = {}
    table_paths: dict[str, Path] = {}
    for table_key, (filename, fieldnames) in TABLE_SPECS.items():
        path = tables_dir / filename
        write_csv(path, table_rows[table_key], fieldnames)
        outputs[f"table_{table_key}"] = path
        table_paths[table_key] = path

    figure_paths = build_figures(rows, table_rows, figures_dir)
    for figure_key, path in figure_paths.items():
        outputs[f"figure_{figure_key}"] = path

    report_path.write_text(
        build_descriptive_report(
            rows=rows,
            table_rows=table_rows,
            table_paths=table_paths,
            figure_paths=figure_paths,
        ),
        encoding="utf-8",
    )
    outputs["descriptive_report"] = report_path
    return outputs


def descriptive_table_rows(
    rows: Sequence[Mapping[str, str]],
) -> dict[str, list[dict[str, str]]]:
    return {
        "school_counts_by_year": school_count_rows(rows),
        "school_rates_by_year": school_rate_rows(rows),
        "pathway_by_class_heatmap": pathway_heatmap_rows(rows),
        "school_group_totals_by_class": school_group_total_rows(rows),
        "tj_zone_counts_by_class": tj_zone_count_rows(rows),
        "virginia_share_by_class": virginia_share_rows(rows),
        "data_coverage_by_class": data_coverage_rows(rows),
        "pre_post_summary": pre_post_summary_rows(rows),
    }


def write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Sequence[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def school_count_rows(rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in sorted(rows, key=_school_year_sort_key):
        output.append(
            {
                "school_group": school_group(row),
                "tj_pathway": row["tj_pathway"],
                "division": row["division"],
                "school_id": row["school_id"],
                "school": row["school"],
                "class_year": row["class_year"],
                "nmsf_count": row["nmsf_count"],
                "nmsf_status": row["nmsf_status"],
                "nmsf_count_available": row["nmsf_count_available"],
                "nmsf_source_id": row["nmsf_source_id"],
                "nmsf_source_title": row["nmsf_source_title"],
                "nmsf_source_url": row["nmsf_source_url"],
                "nmsf_source_date": row["nmsf_source_date"],
                "nmsf_source_hash": row["nmsf_source_hash"],
                "count_missingness_note": _count_missingness_note(row),
            }
        )
    return output


def school_rate_rows(rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in sorted(rows, key=_school_year_sort_key):
        output.append(
            {
                "school_group": school_group(row),
                "tj_pathway": row["tj_pathway"],
                "division": row["division"],
                "school_id": row["school_id"],
                "school": row["school"],
                "class_year": row["class_year"],
                "nmsf_count": row["nmsf_count"],
                "grade11_enrollment": row["grade11_enrollment"],
                "nmsf_per_100_juniors": row["nmsf_per_100_juniors"],
                "rate_status": row["rate_status"],
                "row_coverage_status": row["row_coverage_status"],
                "nmsf_status": row["nmsf_status"],
                "enrollment_status": row["enrollment_status"],
                "denominator_gap_flag": row["denominator_gap_flag"],
                "nmsf_missingness_flag": row["nmsf_missingness_flag"],
                "rate_missingness_note": _rate_missingness_note(row),
            }
        )
    return output


def pathway_heatmap_rows(rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    representatives: dict[tuple[str, str], Mapping[str, str]] = {}
    for row in rows:
        key = (row["tj_pathway"], row["class_year"])
        representatives.setdefault(key, row)

    output: list[dict[str, str]] = []
    for key in sorted(representatives, key=lambda item: (PATHWAY_ORDER.get(item[0], 99), item[1])):
        row = representatives[key]
        output.append(
            {
                "tj_pathway": row["tj_pathway"],
                "class_year": row["class_year"],
                "pathway_nmsf_count_covered": row["pathway_nmsf_count_covered"],
                "pathway_grade11_enrollment_covered": row["pathway_grade11_enrollment_covered"],
                "pathway_nmsf_per_100_juniors_covered": row["pathway_nmsf_per_100_juniors_covered"],
                "pathway_operating_school_rows": row["pathway_operating_school_rows"],
                "pathway_compatible_school_rows": row["pathway_compatible_school_rows"],
                "pathway_missing_nmsf_school_rows": row["pathway_missing_nmsf_school_rows"],
                "pathway_missing_enrollment_school_rows": row["pathway_missing_enrollment_school_rows"],
                "pathway_incompatible_school_rows": row["pathway_incompatible_school_rows"],
                "pathway_coverage_status": row["pathway_coverage_status"],
                "pathway_has_complete_compatible_coverage": row["pathway_has_complete_compatible_coverage"],
                "pathway_interpretation_note": (
                    "covered subset only; analytical geography, not observed admissions pathway"
                ),
            }
        )
    return output


def school_group_total_rows(rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    groups = sorted({school_group(row) for row in rows}, key=lambda group: GROUP_ORDER.get(group, 99))
    for class_year in CLASS_YEAR_LABELS:
        year_rows = [row for row in rows if row["class_year"] == class_year]
        for group in groups:
            summary = summarize_rows([row for row in year_rows if school_group(row) == group])
            output.append(
                {
                    "class_year": class_year,
                    "school_group": group,
                    **summary,
                }
            )
    return output


def tj_zone_count_rows(rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for class_year in CLASS_YEAR_LABELS:
        year_rows = [row for row in rows if row["class_year"] == class_year]
        with_tj = summarize_rows(year_rows)
        without_tj = summarize_rows([row for row in year_rows if not is_tjhsst(row)])
        tj_rows = [row for row in year_rows if is_tjhsst(row)]
        tj_count = ""
        if tj_rows and has_numeric_nmsf(tj_rows[0]):
            tj_count = str(_int_or_none(tj_rows[0]["nmsf_count"]) or 0)
        output.append(
            {
                "class_year": class_year,
                "with_tjhsst_nmsf_count_observed_total": with_tj["nmsf_count_observed_total"],
                "with_tjhsst_nmsf_available_rows": with_tj["nmsf_count_available_rows"],
                "with_tjhsst_missing_nmsf_rows": with_tj["missing_nmsf_rows"],
                "without_tjhsst_nmsf_count_observed_total": without_tj["nmsf_count_observed_total"],
                "without_tjhsst_nmsf_available_rows": without_tj["nmsf_count_available_rows"],
                "without_tjhsst_missing_nmsf_rows": without_tj["missing_nmsf_rows"],
                "tjhsst_nmsf_count": tj_count,
                "coverage_note": (
                    "observed totals include only source-backed numeric NMSF rows; missing rows are not zero"
                ),
            }
        )
    return output


def virginia_share_rows(rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for class_year in CLASS_YEAR_LABELS:
        year_rows = [row for row in rows if row["class_year"] == class_year and is_operating(row)]
        representative = year_rows[0] if year_rows else {}
        statewide_total = _int_or_none(representative.get("statewide_nmsf_semifinalist_total", ""))
        status = representative.get("statewide_nmsf_semifinalist_total_status", "not_sourced")
        source_url = representative.get("statewide_nmsf_semifinalist_total_source_url", "")
        all_summary = summarize_rows(year_rows)
        group_specs = [
            ("TJ-zone including TJHSST", year_rows),
            ("TJHSST", [row for row in year_rows if is_tjhsst(row)]),
            (
                "Conventional base public",
                [
                    row
                    for row in year_rows
                    if row["sector"] == "public" and row["analytical_unit_type"] == "public_high_school"
                ],
            ),
            ("Private/homeschool unallocated", [row for row in year_rows if row["sector"] == "private"]),
            ("TJ-zone excluding TJHSST", [row for row in year_rows if not is_tjhsst(row)]),
        ]
        for group, group_rows in group_specs:
            output.append(
                _virginia_share_row(
                    class_year=class_year,
                    group=group,
                    group_rows=group_rows,
                    statewide_total=statewide_total,
                    statewide_status=status,
                    statewide_source_url=source_url,
                )
            )
        output.append(
            _virginia_remainder_row(
                class_year=class_year,
                all_summary=all_summary,
                statewide_total=statewide_total,
                statewide_status=status,
                statewide_source_url=source_url,
            )
        )
    return output


def _virginia_share_row(
    *,
    class_year: str,
    group: str,
    group_rows: Sequence[Mapping[str, str]],
    statewide_total: int | None,
    statewide_status: str,
    statewide_source_url: str,
) -> dict[str, str]:
    summary = summarize_rows(group_rows)
    count = _int_or_none(summary["nmsf_count_observed_total"])
    missing = int(summary["missing_nmsf_rows"])
    share = _share_text(count, statewide_total) if missing == 0 else ""
    return {
        "class_year": class_year,
        "group": group,
        "nmsf_count_total": str(count) if count is not None and missing == 0 else "",
        "missing_nmsf_rows": str(missing),
        "statewide_nmsf_semifinalist_total": str(statewide_total) if statewide_total is not None else "",
        "share_of_statewide_total_pct": share,
        "statewide_total_status": statewide_status,
        "statewide_total_source_url": statewide_source_url,
        "coverage_note": _virginia_share_note(missing, statewide_total),
    }


def _virginia_remainder_row(
    *,
    class_year: str,
    all_summary: Mapping[str, str],
    statewide_total: int | None,
    statewide_status: str,
    statewide_source_url: str,
) -> dict[str, str]:
    count = _int_or_none(all_summary["nmsf_count_observed_total"])
    missing = int(all_summary["missing_nmsf_rows"])
    remainder = (
        statewide_total - count
        if statewide_total is not None and count is not None and missing == 0
        else None
    )
    return {
        "class_year": class_year,
        "group": "Virginia outside TJ-zone",
        "nmsf_count_total": str(remainder) if remainder is not None else "",
        "missing_nmsf_rows": str(missing),
        "statewide_nmsf_semifinalist_total": str(statewide_total) if statewide_total is not None else "",
        "share_of_statewide_total_pct": _share_text(remainder, statewide_total)
        if remainder is not None
        else "",
        "statewide_total_status": statewide_status,
        "statewide_total_source_url": statewide_source_url,
        "coverage_note": _virginia_share_note(missing, statewide_total),
    }


def data_coverage_rows(rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for class_year in CLASS_YEAR_LABELS:
        year_rows = [row for row in rows if row["class_year"] == class_year]
        statuses = Counter(row["row_coverage_status"] for row in year_rows)
        nmsf_statuses = Counter(row["nmsf_status"] for row in year_rows)
        operating_rows = [row for row in year_rows if is_operating(row)]
        output.append(
            {
                "class_year": class_year,
                "total_rows": str(len(year_rows)),
                "operating_rows": str(len(operating_rows)),
                "compatible_rows": str(statuses["compatible"]),
                "nmsf_gap_rows": str(statuses["nmsf_gap"]),
                "denominator_gap_rows": str(statuses["denominator_gap"]),
                "nmsf_and_denominator_gap_rows": str(statuses["nmsf_and_denominator_gap"]),
                "not_operating_rows": str(statuses["not_operating"]),
                "missing_source_rows": str(nmsf_statuses["missing_source"]),
            }
        )
    return output


def pre_post_summary_rows(rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    periods = (
        ("pre_2023_2024", ("2023", "2024")),
        ("post_2025_2026", ("2025", "2026")),
    )
    groups: tuple[tuple[str, Callable[[Mapping[str, str]], bool]], ...] = (
        ("All schools including TJHSST", lambda row: True),
        ("All schools excluding TJHSST", lambda row: not is_tjhsst(row)),
        ("Public schools including TJHSST", lambda row: row["sector"] == "public"),
        ("Base public schools", lambda row: school_group(row) == "Base public schools"),
        ("Private schools", lambda row: school_group(row) == "Private schools"),
        ("TJHSST", is_tjhsst),
    )

    output: list[dict[str, str]] = []
    for period, years in periods:
        period_rows = [row for row in rows if row["class_year"] in years]
        for group, predicate in groups:
            filtered = [row for row in period_rows if predicate(row)]
            summary = summarize_rows(filtered)
            observed_total = _int_or_none(summary["nmsf_count_observed_total"])
            annual_average = "" if observed_total is None else f"{observed_total / len(years):.6f}"
            output.append(
                {
                    "period": period,
                    "class_years": "|".join(years),
                    "comparison_group": group,
                    "operating_school_year_rows": summary["operating_school_rows"],
                    "nmsf_count_available_rows": summary["nmsf_count_available_rows"],
                    "missing_nmsf_rows": summary["missing_nmsf_rows"],
                    "compatible_rate_rows": summary["compatible_rate_rows"],
                    "nmsf_count_observed_total": summary["nmsf_count_observed_total"],
                    "annual_average_observed_nmsf_count": annual_average,
                    "compatible_nmsf_count_total": summary["compatible_nmsf_count_total"],
                    "compatible_grade11_enrollment_total": summary["compatible_grade11_enrollment_total"],
                    "nmsf_per_100_juniors_covered": summary["nmsf_per_100_juniors_covered"],
                    "nmsf_count_coverage_status": summary["nmsf_count_coverage_status"],
                    "rate_coverage_status": summary["rate_coverage_status"],
                    "small_number_warning": summary["small_number_warning"],
                }
            )
    return output


def summarize_rows(rows: Sequence[Mapping[str, str]]) -> dict[str, str]:
    operating_rows = [row for row in rows if is_operating(row)]
    nmsf_rows = [row for row in operating_rows if has_numeric_nmsf(row)]
    enrollment_rows = [row for row in operating_rows if row["grade11_enrollment_available"] == "true"]
    compatible_rows = [row for row in operating_rows if row["rate_input_compatible"] == "true"]
    missing_nmsf_rows = [row for row in operating_rows if row["nmsf_missingness_flag"] == "true"]

    observed_total = sum(_int_or_none(row["nmsf_count"]) or 0 for row in nmsf_rows)
    compatible_count = sum(_int_or_none(row["nmsf_count"]) or 0 for row in compatible_rows)
    compatible_enrollment = sum(_int_or_none(row["grade11_enrollment"]) or 0 for row in compatible_rows)
    small_number = bool(nmsf_rows) and observed_total < 10

    return {
        "operating_school_rows": str(len(operating_rows)),
        "nmsf_count_available_rows": str(len(nmsf_rows)),
        "missing_nmsf_rows": str(len(missing_nmsf_rows)),
        "grade11_enrollment_available_rows": str(len(enrollment_rows)),
        "compatible_rate_rows": str(len(compatible_rows)),
        "nmsf_count_observed_total": str(observed_total) if nmsf_rows else "",
        "compatible_nmsf_count_total": str(compatible_count) if compatible_rows else "",
        "compatible_grade11_enrollment_total": str(compatible_enrollment) if compatible_rows else "",
        "nmsf_per_100_juniors_covered": _rate_text(compatible_count, compatible_enrollment)
        if compatible_rows
        else "",
        "nmsf_count_coverage_status": _coverage_status(
            operating_count=len(operating_rows),
            covered_count=len(nmsf_rows),
            covered_label="nmsf_count",
        ),
        "rate_coverage_status": _coverage_status(
            operating_count=len(operating_rows),
            covered_count=len(compatible_rows),
            covered_label="compatible_rate",
        ),
        "small_number_warning": _bool_text(small_number),
    }


def build_figures(
    rows: Sequence[Mapping[str, str]],
    table_rows: Mapping[str, Sequence[Mapping[str, str]]],
    figures_dir: Path,
) -> dict[str, Path]:
    outputs = {key: figures_dir / filename for key, filename in FIGURE_FILENAMES.items()}

    write_school_heatmap(
        rows=rows,
        path=outputs["raw_nmsf_counts_by_school_year"],
        value_kind="count",
        title="Raw NMSF counts by school and class",
        subtitle=(
            "Numeric cells are source-backed counts, including verified zeros; missing sources stay blank."
        ),
        legend_label="NMSF count",
    )
    write_school_heatmap(
        rows=rows,
        path=outputs["nmsf_rates_by_school_year"],
        value_kind="rate",
        title="NMSF per 100 juniors by school and class",
        subtitle="Rates require both a source-backed NMSF count and a grade 11 enrollment denominator.",
        legend_label="NMSF per 100 juniors",
    )
    write_pathway_heatmap(
        rows=table_rows["pathway_by_class_heatmap"],
        path=outputs["pathway_by_class_heatmap"],
    )
    write_line_chart(
        path=outputs["tjhsst_vs_base_public_private_counts"],
        title="TJHSST, base public, and private observed NMSF counts",
        subtitle="Observed totals only; missing school-year sources are not counted as zero.",
        y_label="Observed NMSF count",
        series=_series_from_group_totals(
            table_rows["school_group_totals_by_class"],
            ("TJHSST", "Base public schools", "Private schools"),
        ),
        footnote=(
            "Base public excludes the TJHSST row. Private rows are unallocated non-public applicant buckets."
        ),
    )
    write_line_chart(
        path=outputs["tj_zone_counts_with_without_tjhsst"],
        title="TJ-zone observed counts with and without TJHSST",
        subtitle="The without-TJHSST line keeps all other source-backed public and private rows.",
        y_label="Observed NMSF count",
        series=_tj_zone_series(table_rows["tj_zone_counts_by_class"]),
        footnote="Totals are incomplete when source-backed NMSF rows are missing.",
    )
    write_line_chart(
        path=outputs["public_private_counts_by_class"],
        title="Base public versus private observed NMSF counts",
        subtitle="TJHSST is shown separately in the TJHSST comparison figure.",
        y_label="Observed NMSF count",
        series=_series_from_group_totals(
            table_rows["school_group_totals_by_class"],
            ("Base public schools", "Private schools"),
        ),
        footnote="Public/private totals are observed covered rows, not full totals under missing coverage.",
    )
    write_pre_post_chart(
        rows=table_rows["pre_post_summary"],
        path=outputs["pre_post_summary"],
    )
    write_coverage_chart(
        rows=table_rows["data_coverage_by_class"],
        path=outputs["data_coverage_by_class"],
    )

    return outputs


def build_descriptive_report(
    *,
    rows: Sequence[Mapping[str, str]],
    table_rows: Mapping[str, Sequence[Mapping[str, str]]],
    table_paths: Mapping[str, Path],
    figure_paths: Mapping[str, Path],
) -> str:
    cutoff_statuses = sorted({row["va_nmsf_selection_index_cutoff_status"] for row in rows})
    statewide_statuses = sorted({row["statewide_nmsf_semifinalist_total_status"] for row in rows})
    status_counts = Counter(row["nmsf_status"] for row in rows)
    rate_counts = Counter(row["rate_status"] for row in rows)
    coverage_counts = Counter(row["pathway_coverage_status"] for row in rows)

    selected_pre_post = [
        row
        for row in table_rows["pre_post_summary"]
        if row["comparison_group"] in {"TJHSST", "Base public schools", "Private schools"}
    ]

    lines = [
        "# Descriptive Results",
        "",
        "This report is generated from `data/processed/analysis_panel.csv`.",
        (
            "Numeric NMSF counts remain limited to source-backed `verified_count` and "
            "`verified_zero` rows. Missing observations are displayed as missing, not zero."
        ),
        (
            "Rates use grade 11 enrollment as an outcome denominator and are calculated only "
            "when both the NMSF count and denominator are available."
        ),
        (
            "Pathway heatmap values are covered-subset aggregates. Treat them as full pathway "
            "totals only when coverage is marked `complete_compatible_coverage`."
        ),
        "",
        "## Figures",
        "",
        _markdown_table(
            ["Figure", "Purpose"],
            [[f"`{_relative(path)}`", _figure_purpose(key)] for key, path in sorted(figure_paths.items())],
        ),
        "",
        "## Tables",
        "",
        _markdown_table(
            ["Table", "Purpose"],
            [[f"`{_relative(path)}`", _table_purpose(key)] for key, path in sorted(table_paths.items())],
        ),
        "",
        "## Source And Coverage Status",
        "",
        _markdown_table(["NMSF status", "Rows"], _counter_rows(status_counts)),
        "",
        _markdown_table(["Rate status", "Rows"], _counter_rows(rate_counts)),
        "",
        _markdown_table(["Pathway coverage status", "Rows"], _counter_rows(coverage_counts)),
        "",
        "## TJ-Zone Count Summary",
        "",
        _markdown_table(
            [
                "Class",
                "With TJHSST observed",
                "With TJHSST missing rows",
                "Without TJHSST observed",
                "Without TJHSST missing rows",
                "TJHSST",
            ],
            [
                [
                    row["class_year"],
                    row["with_tjhsst_nmsf_count_observed_total"] or "(missing)",
                    row["with_tjhsst_missing_nmsf_rows"],
                    row["without_tjhsst_nmsf_count_observed_total"] or "(missing)",
                    row["without_tjhsst_missing_nmsf_rows"],
                    row["tjhsst_nmsf_count"] or "(missing)",
                ]
                for row in table_rows["tj_zone_counts_by_class"]
            ],
        ),
        "",
        "## Virginia Statewide Shares",
        "",
        (
            "Shares are calculated only when the class year has a source-backed statewide total "
            "and the group has no missing NMSF rows."
        ),
        "",
        _markdown_table(
            ["Class", "Group", "Count", "VA total", "Share %", "Coverage note"],
            [
                [
                    row["class_year"],
                    row["group"],
                    row["nmsf_count_total"] or "(missing)",
                    row["statewide_nmsf_semifinalist_total"] or "(missing)",
                    row["share_of_statewide_total_pct"] or "(missing)",
                    row["coverage_note"],
                ]
                for row in table_rows["virginia_share_by_class"]
                if row["class_year"] in {"2023", "2024", "2025", "2026"}
            ],
        ),
        "",
        "## Pre/Post Summary",
        "",
        (
            "The pre period is Classes 2023-2024 and the post period is Classes 2025-2026. "
            "Observed count totals are not adjusted for missing rows."
        ),
        "",
        _markdown_table(
            [
                "Period",
                "Group",
                "Observed total",
                "Annual average",
                "Missing NMSF rows",
                "Covered rate",
                "Small-number warning",
            ],
            [
                [
                    row["period"],
                    row["comparison_group"],
                    row["nmsf_count_observed_total"] or "(missing)",
                    row["annual_average_observed_nmsf_count"] or "(missing)",
                    row["missing_nmsf_rows"],
                    row["nmsf_per_100_juniors_covered"] or "(missing)",
                    row["small_number_warning"],
                ]
                for row in selected_pre_post
            ],
        ),
        "",
        "## Warnings",
        "",
        (
            "- Small-number warnings in the tables flag observed totals below 10, where one-student "
            "changes can dominate the apparent trend."
        ),
        (
            "- Private-school and historical non-FCPS rows have important NMSF and denominator gaps; "
            "the figures show available coverage rather than imputing missing schools."
        ),
        ("- TJHSST is kept as one school row and is not split back to base public schools."),
        (
            "- Public pathway buckets are analytical geographies, not observed TJHSST admissions "
            "pathway outcomes."
        ),
        "",
        "## Cutoff And Statewide Placeholder Gap",
        "",
        (
            f"Virginia cutoff statuses in the analysis panel: `{', '.join(cutoff_statuses)}`. "
            f"Statewide total statuses: `{', '.join(statewide_statuses)}`."
        ),
        (
            "No Virginia Selection Index cutoff change is annotated in the figures because the "
            "cutoff fields are not sourced in the current panel."
        ),
        "",
    ]
    return "\n".join(lines)


def write_school_heatmap(
    *,
    rows: Sequence[Mapping[str, str]],
    path: Path,
    value_kind: str,
    title: str,
    subtitle: str,
    legend_label: str,
) -> None:
    row_lookup = {(row["school_id"], row["class_year"]): row for row in rows}
    school_rows = _unique_school_rows(rows)
    values: list[float] = []
    for row in rows:
        value = _school_value(row, value_kind)
        if value is not None:
            values.append(value)
    max_value = max(values) if values else 1.0
    left = 330
    top = 92
    cell_w = 62
    row_h = 17
    width = left + cell_w * len(CLASS_YEAR_LABELS) + 42
    height = top + row_h * len(school_rows) + 94
    elements: list[str] = [_svg_defs()]

    elements.extend(_svg_title(title, subtitle, width))
    for index, class_year in enumerate(CLASS_YEAR_LABELS):
        x = left + index * cell_w + cell_w / 2
        elements.append(_text(x, 70, class_year, size=11, anchor="middle", weight="700"))

    for row_index, school_row in enumerate(school_rows):
        y = top + row_index * row_h
        group = school_group(school_row)
        elements.append(
            f'<rect x="8" y="{y + 2}" width="7" height="{row_h - 4}" fill="{_group_color(group)}" />'
        )
        label = _truncate_label(school_row["school"], 43)
        elements.append(_text(left - 10, y + 12, label, size=9, anchor="end"))
        for col_index, class_year in enumerate(CLASS_YEAR_LABELS):
            x = left + col_index * cell_w
            cell_row = row_lookup[(school_row["school_id"], class_year)]
            value = _school_value(cell_row, value_kind)
            is_not_operating_cell = not_operating_for_value(cell_row, value_kind)
            if is_not_operating_cell:
                fill = "#f3f4f6"
                label_text = "n/a"
                text_color = "#64748b"
            elif value is None:
                fill = "url(#missingPattern)"
                label_text = ""
                text_color = "#475569"
            else:
                scaled = math.sqrt(value / max_value) if max_value else 0.0
                fill = _interpolate_color("#eff6ff", "#1d4ed8", scaled)
                label_text = _format_cell_value(value, value_kind)
                text_color = "#ffffff" if scaled > 0.58 else "#0f172a"
            elements.append(
                f'<rect x="{x}" y="{y}" width="{cell_w - 2}" height="{row_h - 2}" '
                f'rx="1" fill="{fill}" stroke="#cbd5e1" stroke-width="0.5" />'
            )
            if label_text:
                elements.append(
                    _text(
                        x + (cell_w - 2) / 2, y + 11.5, label_text, size=8, anchor="middle", fill=text_color
                    )
                )

    legend_y = height - 58
    elements.append(_legend_gradient(24, legend_y, legend_label, max_value, value_kind))
    elements.append(_missing_legend(320, legend_y))
    elements.append(
        _text(
            24,
            height - 18,
            "Missing cells are unsourced or lack a denominator; missing rows are not imputed.",
            size=10,
            fill="#475569",
        )
    )
    path.write_text(_svg(width, height, elements), encoding="utf-8")


def write_pathway_heatmap(rows: Sequence[Mapping[str, str]], path: Path) -> None:
    pathways = sorted({row["tj_pathway"] for row in rows}, key=lambda pathway: PATHWAY_ORDER.get(pathway, 99))
    lookup = {(row["tj_pathway"], row["class_year"]): row for row in rows}
    values = [
        value
        for value in (_float_or_none(row["pathway_nmsf_per_100_juniors_covered"]) for row in rows)
        if value is not None
    ]
    max_value = max(values) if values else 1.0
    left = 230
    top = 95
    cell_w = 102
    cell_h = 48
    width = left + cell_w * len(CLASS_YEAR_LABELS) + 36
    height = top + cell_h * len(pathways) + 92
    elements: list[str] = [_svg_defs()]
    elements.extend(
        _svg_title(
            "Pathway-by-class covered-rate heatmap",
            "Cells use compatible covered rows only; partial coverage is labeled in each cell.",
            width,
        )
    )
    for index, class_year in enumerate(CLASS_YEAR_LABELS):
        elements.append(
            _text(left + index * cell_w + cell_w / 2, 72, class_year, size=11, anchor="middle", weight="700")
        )

    for row_index, pathway in enumerate(pathways):
        y = top + row_index * cell_h
        elements.append(_text(left - 12, y + 27, pathway, size=10, anchor="end", weight="700"))
        for col_index, class_year in enumerate(CLASS_YEAR_LABELS):
            x = left + col_index * cell_w
            row = lookup[(pathway, class_year)]
            value = _float_or_none(row["pathway_nmsf_per_100_juniors_covered"])
            if value is None:
                fill = "url(#missingPattern)"
                text_color = "#475569"
                label_lines: Sequence[str] = ("no rate", row["pathway_coverage_status"].replace("_", " "))
            else:
                scaled = math.sqrt(value / max_value) if max_value else 0.0
                fill = _interpolate_color("#ecfeff", "#0e7490", scaled)
                text_color = "#ffffff" if scaled > 0.58 else "#0f172a"
                label_lines = (
                    f"{value:.2f}",
                    f"{row['pathway_nmsf_count_covered']}/{row['pathway_grade11_enrollment_covered']}",
                    _short_coverage(row["pathway_coverage_status"]),
                )
            elements.append(
                f'<rect x="{x}" y="{y}" width="{cell_w - 3}" height="{cell_h - 3}" rx="2" '
                f'fill="{fill}" stroke="#cbd5e1" stroke-width="0.6" />'
            )
            for line_index, label_text in enumerate(label_lines):
                elements.append(
                    _text(
                        x + (cell_w - 3) / 2,
                        y + 16 + line_index * 13,
                        label_text,
                        size=9,
                        anchor="middle",
                        fill=text_color,
                    )
                )

    elements.append(_legend_gradient(24, height - 60, "Covered NMSF per 100 juniors", max_value, "rate"))
    elements.append(
        _text(
            24,
            height - 18,
            "Count/enrollment labels use covered compatible rows; partial cells are not full pathway totals.",
            size=10,
            fill="#475569",
        )
    )
    path.write_text(_svg(width, height, elements), encoding="utf-8")


def write_line_chart(
    *,
    path: Path,
    title: str,
    subtitle: str,
    y_label: str,
    series: Mapping[str, Sequence[float | None]],
    footnote: str,
) -> None:
    width = 920
    height = 520
    left = 78
    right = 36
    top = 98
    bottom = 82
    plot_w = width - left - right
    plot_h = height - top - bottom
    all_values = [value for values in series.values() for value in values if value is not None]
    max_value = _nice_max(max(all_values) if all_values else 1.0)
    elements: list[str] = []
    elements.extend(_svg_title(title, subtitle, width))
    elements.extend(_axis_elements(left, top, plot_w, plot_h, max_value, y_label))
    x_positions = [
        left + (plot_w * index / (len(CLASS_YEAR_LABELS) - 1)) for index, _ in enumerate(CLASS_YEAR_LABELS)
    ]
    for index, class_year in enumerate(CLASS_YEAR_LABELS):
        elements.append(_text(x_positions[index], top + plot_h + 26, class_year, size=11, anchor="middle"))

    legend_x = left
    for series_index, (label, values) in enumerate(series.items()):
        color = SERIES_COLORS.get(label, f"hsl({series_index * 57 % 360}, 58%, 42%)")
        elements.append(f'<rect x="{legend_x}" y="68" width="12" height="12" fill="{color}" />')
        elements.append(_text(legend_x + 18, 78, label, size=10))
        legend_x += 18 + len(label) * 6 + 22
        path_segments = _line_path(values, x_positions, top, plot_h, max_value)
        for segment in path_segments:
            elements.append(
                f'<polyline points="{segment}" fill="none" stroke="{color}" stroke-width="2.5" '
                'stroke-linejoin="round" stroke-linecap="round" />'
            )
        for x, value in zip(x_positions, values, strict=True):
            if value is None:
                continue
            y = top + plot_h - (value / max_value * plot_h)
            elements.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="{color}" stroke="#ffffff" />')
            elements.append(_text(x, y - 8, _format_axis_value(value), size=9, anchor="middle", fill=color))

    elements.append(_text(24, height - 22, footnote, size=10, fill="#475569"))
    path.write_text(_svg(width, height, elements), encoding="utf-8")


def write_pre_post_chart(rows: Sequence[Mapping[str, str]], path: Path) -> None:
    groups = ("TJHSST", "Base public schools", "Private schools", "All schools excluding TJHSST")
    periods = ("pre_2023_2024", "post_2025_2026")
    lookup = {(row["comparison_group"], row["period"]): row for row in rows}
    values = [
        _float_or_none(lookup[(group, period)]["annual_average_observed_nmsf_count"])
        for group in groups
        for period in periods
    ]
    max_value = _nice_max(max(value for value in values if value is not None))
    width = 940
    height = 520
    left = 76
    right = 30
    top = 100
    bottom = 106
    plot_w = width - left - right
    plot_h = height - top - bottom
    group_w = plot_w / len(groups)
    bar_w = 34
    elements: list[str] = []
    elements.extend(
        _svg_title(
            "Pre/post observed annual-average NMSF counts",
            "Pre is Classes 2023-2024; post is Classes 2025-2026. Missing rows are not zero.",
            width,
        )
    )
    elements.extend(_axis_elements(left, top, plot_w, plot_h, max_value, "Annual average observed count"))
    period_colors = {"pre_2023_2024": "#64748b", "post_2025_2026": "#0f766e"}
    legend_x = left
    for period in periods:
        elements.append(
            f'<rect x="{legend_x}" y="70" width="12" height="12" fill="{period_colors[period]}" />'
        )
        elements.append(_text(legend_x + 18, 80, period.replace("_", " "), size=10))
        legend_x += 150

    for group_index, group in enumerate(groups):
        center = left + group_w * group_index + group_w / 2
        elements.append(
            _text(center, top + plot_h + 34, _truncate_label(group, 24), size=10, anchor="middle")
        )
        for period_index, period in enumerate(periods):
            row = lookup[(group, period)]
            value = _float_or_none(row["annual_average_observed_nmsf_count"])
            x = center + (period_index - 0.5) * (bar_w + 7)
            if value is None:
                bar_h = 0.0
            else:
                bar_h = value / max_value * plot_h
            y = top + plot_h - bar_h
            elements.append(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_w}" height="{bar_h:.2f}" '
                f'fill="{period_colors[period]}" />'
            )
            if value is not None:
                elements.append(
                    _text(x + bar_w / 2, y - 7, _format_axis_value(value), size=9, anchor="middle")
                )
            if row["small_number_warning"] == "true":
                elements.append(
                    _text(x + bar_w / 2, y - 20, "small n", size=8, anchor="middle", fill="#b45309")
                )

    elements.append(
        _text(
            24,
            height - 24,
            (
                "Bars use observed source-backed counts; see the pre/post CSV "
                "for missing-row and rate coverage flags."
            ),
            size=10,
            fill="#475569",
        )
    )
    path.write_text(_svg(width, height, elements), encoding="utf-8")


def write_coverage_chart(rows: Sequence[Mapping[str, str]], path: Path) -> None:
    width = 920
    height = 500
    left = 90
    right = 40
    top = 102
    plot_w = width - left - right
    bar_h = 24
    row_gap = 12
    colors = {
        "compatible_rows": "#0f766e",
        "nmsf_gap_rows": "#dc2626",
        "denominator_gap_rows": "#b45309",
        "nmsf_and_denominator_gap_rows": "#7c2d12",
        "not_operating_rows": "#94a3b8",
    }
    labels = {
        "compatible_rows": "compatible",
        "nmsf_gap_rows": "NMSF gap",
        "denominator_gap_rows": "denominator gap",
        "nmsf_and_denominator_gap_rows": "both gaps",
        "not_operating_rows": "not operating",
    }
    elements: list[str] = []
    elements.extend(
        _svg_title(
            "Data coverage by class",
            "Coverage is row-level compatibility for rates, not a source-completeness claim.",
            width,
        )
    )
    legend_x = left
    for key in colors:
        elements.append(f'<rect x="{legend_x}" y="70" width="12" height="12" fill="{colors[key]}" />')
        elements.append(_text(legend_x + 18, 80, labels[key], size=10))
        legend_x += 18 + len(labels[key]) * 6 + 26

    max_total = max(_int_or_none(row["total_rows"]) or 0 for row in rows)
    for index, row in enumerate(rows):
        y = top + index * (bar_h + row_gap)
        x = float(left)
        elements.append(_text(left - 16, y + 17, row["class_year"], size=11, anchor="end", weight="700"))
        for key in colors:
            count = _int_or_none(row[key]) or 0
            width_part = 0 if max_total == 0 else plot_w * count / max_total
            elements.append(
                f'<rect x="{x:.2f}" y="{y}" width="{width_part:.2f}" height="{bar_h}" fill="{colors[key]}" />'
            )
            if width_part > 26:
                elements.append(
                    _text(x + width_part / 2, y + 16, str(count), size=9, anchor="middle", fill="#ffffff")
                )
            x += width_part
        elements.append(_text(left + plot_w + 8, y + 17, row["total_rows"], size=10, fill="#475569"))

    elements.append(
        _text(
            24,
            height - 24,
            "A compatible row has a numeric NMSF count and grade 11 enrollment; gaps remain visible.",
            size=10,
            fill="#475569",
        )
    )
    path.write_text(_svg(width, height, elements), encoding="utf-8")


def school_group(row: Mapping[str, str]) -> str:
    if is_tjhsst(row):
        return "TJHSST"
    if row["sector"] == "private":
        return "Private schools"
    if row["sector"] == "public":
        return "Base public schools"
    return "Other"


def is_tjhsst(row: Mapping[str, str]) -> bool:
    return row["pathway_assignment_method"] == "single_tjhsst_row" or row["tj_pathway"] == "TJHSST"


def is_operating(row: Mapping[str, str]) -> bool:
    return row["nmsf_status"] != "not_operating" and row["enrollment_status"] != "not_operating"


def has_numeric_nmsf(row: Mapping[str, str]) -> bool:
    return row["nmsf_status"] in NUMERIC_NMSF_STATUSES and _int_or_none(row["nmsf_count"]) is not None


def not_operating_for_value(row: Mapping[str, str], value_kind: str) -> bool:
    if value_kind == "count":
        return row["nmsf_status"] == "not_operating"
    return row["rate_status"] == "not_operating"


def _school_value(row: Mapping[str, str], value_kind: str) -> float | None:
    if value_kind == "count":
        if not has_numeric_nmsf(row):
            return None
        return float(_int_or_none(row["nmsf_count"]) or 0)
    if row["rate_status"] != "calculated":
        return None
    return _float_or_none(row["nmsf_per_100_juniors"])


def _unique_school_rows(rows: Sequence[Mapping[str, str]]) -> list[Mapping[str, str]]:
    by_school: dict[str, Mapping[str, str]] = {}
    for row in rows:
        by_school.setdefault(row["school_id"], row)
    return sorted(by_school.values(), key=_school_sort_key)


def _school_year_sort_key(row: Mapping[str, str]) -> tuple[int, int, str, str, int]:
    return (*_school_sort_key(row), int(row["class_year"]))


def _school_sort_key(row: Mapping[str, str]) -> tuple[int, int, str, str]:
    return (
        GROUP_ORDER.get(school_group(row), 99),
        PATHWAY_ORDER.get(row["tj_pathway"], 99),
        row["division"],
        row["school"],
    )


def _coverage_status(*, operating_count: int, covered_count: int, covered_label: str) -> str:
    if operating_count == 0:
        return "no_operating_rows"
    if covered_count == 0:
        return f"no_{covered_label}_coverage"
    if covered_count == operating_count:
        return f"complete_{covered_label}_coverage"
    return f"partial_{covered_label}_coverage"


def _count_missingness_note(row: Mapping[str, str]) -> str:
    if has_numeric_nmsf(row):
        return "source-backed numeric count"
    if row["nmsf_status"] == "not_operating":
        return "school not operating for class year"
    return "missing NMSF source; not treated as zero"


def _rate_missingness_note(row: Mapping[str, str]) -> str:
    if row["rate_status"] == "calculated":
        return "calculated from source-backed count and grade 11 enrollment"
    if row["rate_status"] == "not_operating":
        return "school not operating for class year"
    if row["rate_status"] == "missing_nmsf_count":
        return "missing NMSF count"
    if row["rate_status"] == "missing_grade11_enrollment":
        return "missing grade 11 denominator"
    if row["rate_status"] == "missing_nmsf_and_grade11_enrollment":
        return "missing NMSF count and grade 11 denominator"
    return "rate not calculated"


def _series_from_group_totals(
    rows: Sequence[Mapping[str, str]], groups: Sequence[str]
) -> dict[str, list[float | None]]:
    lookup = {(row["school_group"], row["class_year"]): row for row in rows}
    output: dict[str, list[float | None]] = {}
    for group in groups:
        values: list[float | None] = []
        for class_year in CLASS_YEAR_LABELS:
            row = lookup[(group, class_year)]
            values.append(_float_or_none(row["nmsf_count_observed_total"]))
        output[group] = values
    return output


def _tj_zone_series(rows: Sequence[Mapping[str, str]]) -> dict[str, list[float | None]]:
    return {
        "All schools including TJHSST": [
            _float_or_none(row["with_tjhsst_nmsf_count_observed_total"]) for row in rows
        ],
        "All schools excluding TJHSST": [
            _float_or_none(row["without_tjhsst_nmsf_count_observed_total"]) for row in rows
        ],
        "TJHSST": [_float_or_none(row["tjhsst_nmsf_count"]) for row in rows],
    }


def _line_path(
    values: Sequence[float | None],
    x_positions: Sequence[float],
    top: float,
    plot_h: float,
    max_value: float,
) -> list[str]:
    segments: list[list[str]] = []
    current: list[str] = []
    for x, value in zip(x_positions, values, strict=True):
        if value is None:
            if current:
                segments.append(current)
                current = []
            continue
        y = top + plot_h - (value / max_value * plot_h)
        current.append(f"{x:.2f},{y:.2f}")
    if current:
        segments.append(current)
    return [" ".join(segment) for segment in segments if len(segment) > 1]


def _axis_elements(
    left: float,
    top: float,
    plot_w: float,
    plot_h: float,
    max_value: float,
    y_label: str,
) -> list[str]:
    elements = [
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#334155" />',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#334155" />',
    ]
    for tick_index in range(6):
        value = max_value * tick_index / 5
        y = top + plot_h - (value / max_value * plot_h)
        elements.append(
            f'<line x1="{left - 5}" y1="{y:.2f}" x2="{left + plot_w}" y2="{y:.2f}" stroke="#e2e8f0" />'
        )
        elements.append(_text(left - 10, y + 4, _format_axis_value(value), size=10, anchor="end"))
    elements.append(_text(22, top + plot_h / 2, y_label, size=11, anchor="middle", rotate=-90))
    return elements


def _svg_title(title: str, subtitle: str, width: float) -> list[str]:
    return [
        _text(24, 30, title, size=18, weight="700"),
        _text(24, 52, subtitle, size=11, fill="#475569"),
        f'<line x1="24" y1="60" x2="{width - 24}" y2="60" stroke="#e2e8f0" />',
    ]


def _legend_gradient(x: float, y: float, label: str, max_value: float, value_kind: str) -> str:
    steps = []
    for index in range(6):
        scaled = index / 5
        fill = _interpolate_color("#eff6ff", "#1d4ed8", scaled)
        steps.append(f'<rect x="{x + index * 22}" y="{y}" width="22" height="12" fill="{fill}" />')
    max_label = _format_cell_value(max_value, value_kind)
    return (
        "".join(steps)
        + _text(x, y - 6, label, size=9, fill="#475569")
        + _text(x, y + 28, "0", size=9, fill="#475569")
        + _text(x + 132, y + 28, max_label, size=9, fill="#475569", anchor="end")
    )


def _missing_legend(x: float, y: float) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="22" height="12" fill="url(#missingPattern)" stroke="#cbd5e1" />'
        + _text(x + 30, y + 10, "missing", size=9, fill="#475569")
        + f'<rect x="{x + 96}" y="{y}" width="22" height="12" fill="#f3f4f6" stroke="#cbd5e1" />'
        + _text(x + 126, y + 10, "not operating", size=9, fill="#475569")
    )


def _svg_defs() -> str:
    return (
        "<defs>"
        '<pattern id="missingPattern" patternUnits="userSpaceOnUse" width="6" height="6">'
        '<rect width="6" height="6" fill="#f8fafc" />'
        '<path d="M0,6 L6,0" stroke="#cbd5e1" stroke-width="1" />'
        "</pattern>"
        "</defs>"
    )


def _svg(width: float, height: float, elements: Sequence[str]) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" role="img">'
        '<rect width="100%" height="100%" fill="#ffffff" />' + "".join(elements) + "</svg>\n"
    )


def _text(
    x: float,
    y: float,
    text: object,
    *,
    size: int = 10,
    fill: str = "#0f172a",
    anchor: str = "start",
    weight: str = "400",
    rotate: int | None = None,
) -> str:
    transform = f' transform="rotate({rotate} {x:.2f} {y:.2f})"' if rotate is not None else ""
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{transform}>'
        f"{html.escape(str(text))}</text>"
    )


def _interpolate_color(start: str, end: str, ratio: float) -> str:
    ratio = max(0.0, min(1.0, ratio))
    start_rgb = _hex_to_rgb(start)
    end_rgb = _hex_to_rgb(end)
    rgb = tuple(round(start_rgb[index] + (end_rgb[index] - start_rgb[index]) * ratio) for index in range(3))
    return "#" + "".join(f"{component:02x}" for component in rgb)


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    text = value.lstrip("#")
    return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16)


def _group_color(group: str) -> str:
    return {
        "TJHSST": "#1d4ed8",
        "Base public schools": "#0f766e",
        "Private schools": "#b45309",
    }.get(group, "#64748b")


def _short_coverage(status: str) -> str:
    return {
        "complete_compatible_coverage": "complete",
        "partial_compatible_coverage": "partial",
        "no_compatible_rows": "no compatible rows",
        "no_operating_rows": "not operating",
    }.get(status, status.replace("_", " "))


def _format_cell_value(value: float, value_kind: str) -> str:
    if value_kind == "count":
        return str(int(round(value)))
    if value >= 10:
        return f"{value:.1f}"
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _format_axis_value(value: float) -> str:
    if value >= 100:
        return str(int(round(value)))
    if value >= 10:
        return f"{value:.0f}"
    return f"{value:.1f}".rstrip("0").rstrip(".")


def _nice_max(value: float) -> float:
    if value <= 0:
        return 1.0
    magnitude = 10 ** math.floor(math.log10(value))
    normalized = value / magnitude
    if normalized <= 2:
        nice = 2
    elif normalized <= 5:
        nice = 5
    else:
        nice = 10
    return nice * magnitude


def _truncate_label(value: str, max_chars: int) -> str:
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3] + "..."


def _rate_text(nmsf_count: int | None, grade11_enrollment: int | None) -> str:
    if nmsf_count is None or grade11_enrollment is None or grade11_enrollment <= 0:
        return ""
    return f"{(nmsf_count / grade11_enrollment) * 100:.6f}"


def _int_or_none(value: object) -> int | None:
    text = str(value or "").strip().replace(",", "")
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _float_or_none(value: object) -> float | None:
    text = str(value or "").strip().replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def _share_text(count: int | None, statewide_total: int | None) -> str:
    if count is None or statewide_total is None or statewide_total <= 0:
        return ""
    return f"{100 * count / statewide_total:.6f}"


def _virginia_share_note(missing_rows: int, statewide_total: int | None) -> str:
    if statewide_total is None:
        return "statewide total not source-backed for this class year"
    if missing_rows:
        return "group count has missing NMSF rows; share not calculated"
    return "source-backed count and complete Virginia list statewide denominator"


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


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def _figure_purpose(key: str) -> str:
    return {
        "raw_nmsf_counts_by_school_year": "School-by-class source-backed raw counts heatmap.",
        "nmsf_rates_by_school_year": "School-by-class NMSF per 100 juniors heatmap.",
        "pathway_by_class_heatmap": "Covered-subset pathway rate heatmap with coverage labels.",
        "tjhsst_vs_base_public_private_counts": (
            "TJHSST plotted separately from base public and private rows."
        ),
        "tj_zone_counts_with_without_tjhsst": "Observed TJ-zone totals with and without TJHSST.",
        "public_private_counts_by_class": "Observed base-public versus private totals.",
        "pre_post_summary": "Classes 2023-2024 versus 2025-2026 observed count summary.",
        "data_coverage_by_class": "Row-level rate compatibility and missingness display.",
    }.get(key, "Generated descriptive figure.")


def _table_purpose(key: str) -> str:
    return {
        "school_counts_by_year": "Raw source-backed counts and count missingness by school/class.",
        "school_rates_by_year": "Rates, denominators, and rate missingness by school/class.",
        "pathway_by_class_heatmap": "Source table for pathway heatmap values and coverage.",
        "school_group_totals_by_class": "TJHSST, base-public, and private observed totals by class.",
        "tj_zone_counts_by_class": "Observed counts with and without TJHSST by class.",
        "virginia_share_by_class": "TJ-zone group counts as shares of source-backed Virginia totals.",
        "data_coverage_by_class": "Coverage and missingness counts by class.",
        "pre_post_summary": "Pre/post summaries for Classes 2023-2024 versus 2025-2026.",
    }.get(key, "Generated descriptive table.")
