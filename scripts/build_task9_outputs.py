#!/usr/bin/env python3
"""Build Milestone 9 robustness tables and interpretation reports.

Inputs
------
data/processed/analysis_panel.csv

Outputs
-------
reports/robustness.md
reports/limitations.md
reports/initial_findings.md
reports/tables/task9_*.csv
docs/source_notes/task9_web_research_sources.md

The canonical panel remains unchanged. Virginia cutoff and statewide-total values
used here are explicitly labeled supplemental secondary-source checks and are not
written back into the panel's not_sourced placeholder fields.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PANEL_PATH = ROOT / "data" / "processed" / "analysis_panel.csv"
MANUAL_REVIEW_PATH = ROOT / "reports" / "data_quality" / "manual_review_queue.csv"
REPORTS = ROOT / "reports"
TABLES = REPORTS / "tables"
SOURCE_NOTES = ROOT / "docs" / "source_notes"

TJ_ID = "thomas_jefferson_high_school_for_science_and_technology"
FOCAL_YEARS = [2023, 2024, 2025, 2026]
TODAY = "2026-06-20"

# Supplemental values are intentionally NOT imported into analysis_panel.csv.
VA_CUTOFF = {2023: 221, 2024: 219, 2025: 222, 2026: 224}
VA_STATE_TOTAL = {2023: 397, 2024: 467, 2025: 394, 2026: 489}
CUTOFF_SOURCE = "https://www.compassprep.com/historical-national-merit-cutoffs/"
STATE_TOTAL_SOURCE = "https://www.compassprep.com/national-merit-semifinalists-by-state/"

URLS = {
    "nmsc_2026": "https://www.nationalmerit.org/s/1758/images/gid2/editor_documents/guide_to_the_national_merit_scholarship_program.pdf?gid=2&pgid=61",
    "nmsc_release": "https://www.nationalmerit.org/s/1758/images/gid2/editor_documents/26_meritsemi.pdf",
    "fcps_current": "https://www.fcps.edu/about-fcps/registration/tjhsst-admissions/freshman-application-process",
    "board_minutes_2020": "https://go.boarddocs.com/vsba/fairfax/Board.nsf/files/BY5JH34D3388/%24file/12-17-20%20ERM%20FINAL.pdf",
    "reg3355_15": "https://valor-dictus.com/wp-content/uploads/2022/05/R3355.pdf",
    "class2025_notice": "https://content.govdelivery.com/accounts/VAEDUFCPS/bulletins/2bd3a3b",
    "class2026_notice": "https://content.govdelivery.com/accounts/VAEDUFCPS/bulletins/2f77379",
    "fcps_index": "https://insys.fcps.edu/schoolboardapps/report_policy/cache/numeric-3000.htm",
    "court_filing": "https://www.ffxnow.com/files/2022/03/FCPS-Brief-in-Support-of-Motion-to-Stay-Pending-Appeal.pdf",
    "tj_profile_2021": "https://tjhsst.fcps.edu/sites/default/files/media/inline-files/school-profile%202021-22_0.pdf",
    "collegeboard_digital": "https://blog.collegeboard.org/how-get-ready-digital-psat-nmsqt",
    "fcps_virtual_eval": "https://www.fcps.edu/sites/default/files/media/pdf/FCPS_2020_21_Evaluation_Report_0.pdf",
    "fcps_in_person_2021": "https://www.fcps.edu/sites/default/files/2022-02/Award%20Vax%20Up%20FCPS%20This%20Week%20-%20August%2025%2C%202021.pdf",
    "cutoffs": CUTOFF_SOURCE,
    "state_totals": STATE_TOTAL_SOURCE,
}


def as_bool(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    return s.astype(str).str.strip().str.lower().eq("true")


def pct_change(new: float, old: float) -> float:
    return np.nan if pd.isna(old) or old == 0 else 100.0 * (new - old) / old


def fmt_int(value: float | int | None) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{int(round(float(value))):,}"


def fmt_rate(value: float | int | None, digits: int = 3) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):.{digits}f}"


def fmt_pct(value: float | int | None, digits: int = 1, sign: bool = False) -> str:
    if value is None or pd.isna(value):
        return "—"
    prefix = "+" if sign and float(value) > 0 else ""
    return f"{prefix}{float(value):.{digits}f}%"


def join_with_and(parts: list[str]) -> str:
    if len(parts) <= 1:
        return "".join(parts)
    return ", ".join(parts[:-1]) + f", and {parts[-1]}"


def md_table(headers: list[str], rows: Iterable[Iterable[object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(out)


def group_year_summary(df: pd.DataFrame, mask: pd.Series, group: str) -> list[dict]:
    rows: list[dict] = []
    sub = df.loc[mask & df["class_year"].isin(FOCAL_YEARS)].copy()
    for year in FOCAL_YEARS:
        y = sub[sub["class_year"] == year]
        operating = y[y["nmsf_status"] != "not_operating"]
        observed = operating[operating["nmsf_count_available"]]
        compatible = operating[operating["rate_input_compatible"]]
        count = observed["nmsf_count"].sum(min_count=1)
        compatible_count = compatible["nmsf_count"].sum(min_count=1)
        enrollment = compatible["grade11_enrollment"].sum(min_count=1)
        rate = 100 * compatible_count / enrollment if pd.notna(enrollment) and enrollment > 0 else np.nan
        rows.append(
            {
                "group": group,
                "class_year": year,
                "operating_school_rows": len(operating),
                "observed_count_rows": len(observed),
                "missing_count_rows": len(operating) - len(observed),
                "observed_nmsf_total": count,
                "rate_compatible_rows": len(compatible),
                "rate_compatible_nmsf_count": compatible_count,
                "rate_compatible_grade11_enrollment": enrollment,
                "covered_nmsf_per_100_grade11": rate,
            }
        )
    return rows


def ids_complete(
    df: pd.DataFrame, flag_col: str, years: list[int], mask: pd.Series | None = None
) -> list[str]:
    x = df[df["class_year"].isin(years)].copy()
    if mask is not None:
        x = x[mask.loc[x.index]]
    grouped = x.groupby("school_id", sort=True)
    ids = []
    for school_id, g in grouped:
        if set(g["class_year"]) == set(years) and len(g) == len(years) and as_bool(g[flag_col]).all():
            ids.append(school_id)
    return ids


def balanced_count_summary(df: pd.DataFrame, ids: list[str], group: str) -> list[dict]:
    rows = []
    sub = df[df["school_id"].isin(ids) & df["class_year"].isin(FOCAL_YEARS)]
    for year in FOCAL_YEARS:
        y = sub[sub["class_year"] == year]
        rows.append(
            {
                "group": group,
                "class_year": year,
                "school_count": y["school_id"].nunique(),
                "nmsf_count": y["nmsf_count"].sum(),
            }
        )
    return rows


def balanced_rate_summary(df: pd.DataFrame, ids: list[str], group: str) -> list[dict]:
    rows = []
    sub = df[df["school_id"].isin(ids) & df["class_year"].isin(FOCAL_YEARS)]
    for year in FOCAL_YEARS:
        y = sub[sub["class_year"] == year]
        count = y["nmsf_count"].sum()
        enrollment = y["grade11_enrollment"].sum()
        rows.append(
            {
                "group": group,
                "class_year": year,
                "school_count": y["school_id"].nunique(),
                "nmsf_count": count,
                "grade11_enrollment": enrollment,
                "nmsf_per_100_grade11": 100 * count / enrollment,
            }
        )
    return rows


def lookup(table: pd.DataFrame, group: str, year: int, col: str) -> float:
    return table.loc[(table["group"] == group) & (table["class_year"] == year), col].iloc[0]


def pooled_rate(table: pd.DataFrame, group: str, years: list[int]) -> tuple[float, float, float]:
    x = table[(table["group"] == group) & table["class_year"].isin(years)]
    count = x["nmsf_count"].sum()
    enrollment = x["grade11_enrollment"].sum()
    return float(count), float(enrollment), float(100 * count / enrollment)


def write_csv(df: pd.DataFrame, name: str) -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    df.to_csv(TABLES / name, index=False, float_format="%.6f")


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    # Remove stale Task 9 artifacts from earlier drafts before regenerating.
    for pattern in ("task9_*.csv", "task9_*.json"):
        for old_path in TABLES.glob(pattern):
            old_path.unlink()

    df = pd.read_csv(PANEL_PATH)
    df["class_year"] = pd.to_numeric(df["class_year"], errors="raise").astype(int)
    for col in ["nmsf_count", "grade11_enrollment", "nmsf_per_100_juniors"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["nmsf_count_available", "rate_input_compatible", "grade11_enrollment_available"]:
        df[col] = as_bool(df[col])

    assert len(df) == 608, f"Unexpected panel row count: {len(df)}"
    assert df[["school_id", "class_year"]].drop_duplicates().shape[0] == len(df), "Duplicate school-year rows"
    assert set(df["class_year"]) == set(range(2019, 2027)), "Unexpected class-year coverage"

    is_tj = df["school_id"].eq(TJ_ID)
    is_private = df["analytical_unit_type"].eq("private_school")
    is_program = df["analytical_unit_type"].eq("public_secondary_program")
    is_conventional_public = df["analytical_unit_type"].eq("public_high_school")
    is_base_public = is_conventional_public | is_program
    is_public_any = is_base_public | df["analytical_unit_type"].eq("public_governor_school")

    # Full-sample focal-year group summaries.
    summary_rows: list[dict] = []
    groups = [
        (pd.Series(True, index=df.index), "All TJ-zone roster rows"),
        (~is_tj, "TJ-zone excluding TJHSST"),
        (is_public_any, "All public including TJHSST"),
        (is_base_public, "Base public including secondary program"),
        (is_conventional_public, "Conventional base public high schools"),
        (is_private, "Private schools"),
        (is_tj, "TJHSST"),
    ]
    for mask, name in groups:
        summary_rows.extend(group_year_summary(df, mask, name))
    group_summary = pd.DataFrame(summary_rows)
    group_summary["count_coverage_pct"] = (
        100 * group_summary["observed_count_rows"] / group_summary["operating_school_rows"]
    )
    group_summary["rate_coverage_pct"] = (
        100 * group_summary["rate_compatible_rows"] / group_summary["operating_school_rows"]
    )
    write_csv(group_summary, "task9_group_year_summary.csv")

    coverage = group_summary[group_summary["group"] == "All TJ-zone roster rows"].copy()
    coverage = coverage[
        [
            "class_year",
            "operating_school_rows",
            "observed_count_rows",
            "missing_count_rows",
            "count_coverage_pct",
            "rate_compatible_rows",
            "rate_coverage_pct",
            "observed_nmsf_total",
            "rate_compatible_nmsf_count",
            "rate_compatible_grade11_enrollment",
            "covered_nmsf_per_100_grade11",
        ]
    ]
    write_csv(coverage, "task9_coverage_2023_2026.csv")

    # Balanced panels.
    balanced_count_ids = ids_complete(df, "nmsf_count_available", FOCAL_YEARS)
    private_balanced_ids = sorted(set(balanced_count_ids) & set(df.loc[is_private, "school_id"]))
    base_balanced_ids = sorted(set(balanced_count_ids) & set(df.loc[is_base_public, "school_id"]))
    conventional_balanced_ids = sorted(
        set(balanced_count_ids) & set(df.loc[is_conventional_public, "school_id"])
    )
    excl_tj_balanced_ids = sorted(set(balanced_count_ids) - {TJ_ID})

    bc_rows: list[dict] = []
    for ids, name in [
        (balanced_count_ids, "All balanced count schools"),
        (excl_tj_balanced_ids, "Balanced count schools excluding TJHSST"),
        (base_balanced_ids, "Balanced base public including program"),
        (conventional_balanced_ids, "Balanced conventional base public"),
        (private_balanced_ids, "Balanced private schools"),
        ([TJ_ID], "TJHSST"),
    ]:
        bc_rows.extend(balanced_count_summary(df, ids, name))
    balanced_counts = pd.DataFrame(bc_rows)
    write_csv(balanced_counts, "task9_balanced_count_panel.csv")

    public_rate_mask = is_public_any
    balanced_public_rate_ids = ids_complete(df, "rate_input_compatible", FOCAL_YEARS, public_rate_mask)
    balanced_base_rate_ids = sorted(set(balanced_public_rate_ids) - {TJ_ID})
    # By construction these are conventional public high schools; H-B lacks all denominators.
    br_rows: list[dict] = []
    for ids, name in [
        (balanced_public_rate_ids, "Balanced public including TJHSST"),
        (balanced_base_rate_ids, "Balanced conventional base public"),
        ([TJ_ID], "TJHSST"),
    ]:
        br_rows.extend(balanced_rate_summary(df, ids, name))
    balanced_rates = pd.DataFrame(br_rows)
    write_csv(balanced_rates, "task9_balanced_rate_panel.csv")

    # Membership audit.
    schools = df[df["class_year"] == 2026][
        ["school_id", "school", "sector", "analytical_unit_type", "division", "tj_pathway"]
    ].copy()
    schools["balanced_count_2023_2026"] = schools["school_id"].isin(balanced_count_ids)
    schools["balanced_public_rate_2023_2026"] = schools["school_id"].isin(balanced_public_rate_ids)
    schools["balanced_private_count_2023_2026"] = schools["school_id"].isin(private_balanced_ids)
    write_csv(schools.sort_values(["analytical_unit_type", "school"]), "task9_balanced_panel_membership.csv")

    # Private missingness sensitivity.
    private_rows = []
    for year in FOCAL_YEARS:
        y = df[is_private & df["class_year"].eq(year) & ~df["nmsf_status"].eq("not_operating")]
        obs = y[y["nmsf_count_available"]]
        comp = y[y["rate_input_compatible"]]
        bal = y[y["school_id"].isin(private_balanced_ids)]
        private_rows.append(
            {
                "class_year": year,
                "private_operating_rows": len(y),
                "private_observed_count_rows": len(obs),
                "private_missing_count_rows": len(y) - len(obs),
                "full_observed_private_nmsf_total": obs["nmsf_count"].sum(),
                "balanced_private_school_rows": len(bal),
                "balanced_private_nmsf_total": bal["nmsf_count"].sum(),
                "rate_compatible_private_rows": len(comp),
                "rate_compatible_private_nmsf_count": comp["nmsf_count"].sum() if len(comp) else np.nan,
                "rate_compatible_private_grade11_enrollment": comp["grade11_enrollment"].sum()
                if len(comp)
                else np.nan,
                "covered_private_rate_per_100": (
                    100 * comp["nmsf_count"].sum() / comp["grade11_enrollment"].sum()
                )
                if len(comp) and comp["grade11_enrollment"].sum() > 0
                else np.nan,
            }
        )
    private_sens = pd.DataFrame(private_rows)
    write_csv(private_sens, "task9_private_sensitivity.csv")
    private_rate_coverage_text = join_with_and(
        [
            f"{int(row['rate_compatible_private_rows'])}/{int(row['private_operating_rows'])} schools in {int(row['class_year'])}"
            for _, row in private_sens.iterrows()
        ]
    )
    private_2025_rate_rows = int(
        private_sens.loc[
            private_sens["class_year"].eq(2025),
            "rate_compatible_private_rows",
        ].iloc[0]
    )

    # Program sensitivity.
    program_rows = []
    for year in FOCAL_YEARS:
        incl = group_summary[
            (group_summary["group"] == "Base public including secondary program")
            & (group_summary["class_year"] == year)
        ].iloc[0]
        excl = group_summary[
            (group_summary["group"] == "Conventional base public high schools")
            & (group_summary["class_year"] == year)
        ].iloc[0]
        prog = df[is_program & df["class_year"].eq(year)].iloc[0]
        program_rows.append(
            {
                "class_year": year,
                "program_school": prog["school"],
                "program_nmsf_count": prog["nmsf_count"],
                "program_grade11_enrollment": prog["grade11_enrollment"],
                "program_rate_input_compatible": prog["rate_input_compatible"],
                "base_public_observed_count_including_program": incl["observed_nmsf_total"],
                "base_public_observed_count_excluding_program": excl["observed_nmsf_total"],
                "count_difference_due_to_program": incl["observed_nmsf_total"] - excl["observed_nmsf_total"],
                "covered_rate_including_program": incl["covered_nmsf_per_100_grade11"],
                "covered_rate_excluding_program": excl["covered_nmsf_per_100_grade11"],
            }
        )
    program_sens = pd.DataFrame(program_rows)
    write_csv(program_sens, "task9_program_sensitivity.csv")

    # Manual-review queue audit. Rows remain excluded; this table only summarizes why.
    manual_review = pd.read_csv(MANUAL_REVIEW_PATH)
    manual_issue_counts = (
        manual_review.groupby("issue_type", dropna=False)
        .agg(rows=("issue_type", "size"), listed_nmsf_count=("nmsf_count", "sum"))
        .reset_index()
        .sort_values(["rows", "issue_type"], ascending=[False, True])
    )
    write_csv(manual_issue_counts, "task9_manual_review_issue_counts.csv")

    # Supplemental state normalization.
    state_rows = []
    state_groups = [
        (balanced_count_ids, "Balanced count all schools"),
        (balanced_public_rate_ids, "Balanced public including TJHSST"),
        (balanced_base_rate_ids, "Balanced conventional base public"),
        ([TJ_ID], "TJHSST"),
        (private_balanced_ids, "Balanced private schools"),
    ]
    for year in FOCAL_YEARS:
        for ids, name in state_groups:
            y = df[df["school_id"].isin(ids) & df["class_year"].eq(year)]
            count = y["nmsf_count"].sum()
            state_rows.append(
                {
                    "class_year": year,
                    "group": name,
                    "group_nmsf_count": count,
                    "virginia_selection_index_cutoff": VA_CUTOFF[year],
                    "virginia_statewide_semifinalist_total": VA_STATE_TOTAL[year],
                    "group_share_of_statewide_total_pct": 100 * count / VA_STATE_TOTAL[year],
                    "source_status": "supplemental_secondary_not_imported_to_canonical_panel",
                    "cutoff_source_url": CUTOFF_SOURCE,
                    "state_total_source_url": STATE_TOTAL_SOURCE,
                }
            )
    state_sens = pd.DataFrame(state_rows)
    write_csv(state_sens, "task9_state_normalization_supplemental.csv")

    # Cohort timing and measurement changes.
    unique_map = df[["class_year", "qualifying_psat_year"]].drop_duplicates().sort_values("class_year")
    timing_rows = []
    covid_context = {
        2017: "Pre-COVID; paper PSAT/NMSQT",
        2018: "Pre-COVID; paper PSAT/NMSQT",
        2019: "Pre-COVID; paper PSAT/NMSQT",
        2020: "Acute pandemic disruption; national PSAT participation sharply reduced",
        2021: "Pandemic-recovery year with uneven return to in-person schooling",
        2022: "Later recovery; paper PSAT/NMSQT",
        2023: "First digital PSAT/NMSQT administration",
        2024: "Second digital PSAT/NMSQT administration",
    }
    for _, r in unique_map.iterrows():
        year = int(r["class_year"])
        psat_match = re.search(r"(20\d{2})", str(r["qualifying_psat_year"]))
        if not psat_match:
            raise ValueError(f"Could not parse qualifying_psat_year: {r['qualifying_psat_year']!r}")
        psat = int(psat_match.group(1))
        timing_rows.append(
            {
                "class_year": year,
                "qualifying_psat_year": psat,
                "tjhsst_admissions_regime": "Post-2020 holistic/allocation process"
                if year >= 2025
                else "Pre-change test-based admissions process",
                "policy_exposure": "First affected class"
                if year == 2025
                else ("Second affected class" if year == 2026 else "Pre-policy class"),
                "psat_format": "Digital" if psat >= 2023 else "Paper",
                "timing_context": covid_context.get(psat, ""),
                "virginia_cutoff_supplemental": VA_CUTOFF.get(year, np.nan),
                "cutoff_source_status": "supplemental_secondary" if year in VA_CUTOFF else "not_added",
            }
        )
    timing = pd.DataFrame(timing_rows)
    write_csv(timing, "task9_cohort_timing.csv")

    # School-level changes within balanced conventional public rate panel.
    base = df[df["school_id"].isin(balanced_base_rate_ids) & df["class_year"].isin(FOCAL_YEARS)].copy()
    count_wide = base.pivot(
        index=["school_id", "school", "tj_pathway"], columns="class_year", values="nmsf_count"
    )
    rate_wide = base.pivot(
        index=["school_id", "school", "tj_pathway"], columns="class_year", values="nmsf_per_100_juniors"
    )
    school_changes = count_wide.reset_index()
    school_changes.columns = ["school_id", "school", "tj_pathway"] + [f"nmsf_{y}" for y in FOCAL_YEARS]
    rate_reset = rate_wide.reset_index()
    rate_reset.columns = ["school_id", "school", "tj_pathway"] + [f"rate_{y}" for y in FOCAL_YEARS]
    school_changes = school_changes.merge(rate_reset, on=["school_id", "school", "tj_pathway"], how="left")
    school_changes["count_change_2024_2025"] = school_changes["nmsf_2025"] - school_changes["nmsf_2024"]
    school_changes["count_change_2025_2026"] = school_changes["nmsf_2026"] - school_changes["nmsf_2025"]
    school_changes["count_change_2024_2026"] = school_changes["nmsf_2026"] - school_changes["nmsf_2024"]
    school_changes["rate_change_2024_2025"] = school_changes["rate_2025"] - school_changes["rate_2024"]
    school_changes["rate_change_2025_2026"] = school_changes["rate_2026"] - school_changes["rate_2025"]
    school_changes["rate_change_2024_2026"] = school_changes["rate_2026"] - school_changes["rate_2024"]
    write_csv(
        school_changes.sort_values("count_change_2025_2026", ascending=False),
        "task9_balanced_base_school_changes.csv",
    )

    # Pooled school-level and pathway-level distribution checks.
    pooled_school_rows = []
    for (school_id, school, pathway), g in base.groupby(["school_id", "school", "tj_pathway"], sort=True):
        pre = g[g["class_year"].isin([2023, 2024])]
        post = g[g["class_year"].isin([2025, 2026])]
        pre_rate = 100 * pre["nmsf_count"].sum() / pre["grade11_enrollment"].sum()
        post_rate = 100 * post["nmsf_count"].sum() / post["grade11_enrollment"].sum()
        change = post_rate - pre_rate
        pooled_school_rows.append(
            {
                "school_id": school_id,
                "school": school,
                "tj_pathway": pathway,
                "nmsf_2023_2024": pre["nmsf_count"].sum(),
                "grade11_2023_2024": pre["grade11_enrollment"].sum(),
                "rate_2023_2024": pre_rate,
                "nmsf_2025_2026": post["nmsf_count"].sum(),
                "grade11_2025_2026": post["grade11_enrollment"].sum(),
                "rate_2025_2026": post_rate,
                "rate_point_change": change,
                "direction": "increase"
                if change > 1e-12
                else ("decrease" if change < -1e-12 else "unchanged"),
            }
        )
    pooled_school = pd.DataFrame(pooled_school_rows).sort_values("rate_point_change", ascending=False)
    write_csv(pooled_school, "task9_school_pooled_changes.csv")

    pathway_rows = []
    pathway_order = [
        "Arlington",
        "FCPS Region 1",
        "FCPS Region 2",
        "FCPS Region 3",
        "FCPS Region 4",
        "FCPS Region 5",
        "Loudoun",
        "Prince William",
    ]
    for pathway in pathway_order:
        for year in FOCAL_YEARS:
            y = base[(base["tj_pathway"] == pathway) & (base["class_year"] == year)]
            count = y["nmsf_count"].sum()
            enrollment = y["grade11_enrollment"].sum()
            pathway_rows.append(
                {
                    "tj_pathway": pathway,
                    "class_year": year,
                    "school_count": y["school_id"].nunique(),
                    "nmsf_count": count,
                    "grade11_enrollment": enrollment,
                    "nmsf_per_100_grade11": 100 * count / enrollment,
                }
            )
    pathway_sens = pd.DataFrame(pathway_rows)
    write_csv(pathway_sens, "task9_pathway_rate_sensitivity.csv")

    # Change summary.
    change_rows = []
    for group in ["Balanced public including TJHSST", "Balanced conventional base public", "TJHSST"]:
        for metric, col in [("raw_count", "nmsf_count"), ("rate_per_100_grade11", "nmsf_per_100_grade11")]:
            vals = {y: lookup(balanced_rates, group, y, col) for y in FOCAL_YEARS}
            for start, end in [(2024, 2025), (2025, 2026), (2024, 2026)]:
                change_rows.append(
                    {
                        "group": group,
                        "metric": metric,
                        "comparison": f"{start}_to_{end}",
                        "start_value": vals[start],
                        "end_value": vals[end],
                        "absolute_change": vals[end] - vals[start],
                        "percent_change": pct_change(vals[end], vals[start]),
                    }
                )
    for group in ["Balanced private schools"]:
        vals = {y: lookup(balanced_counts, group, y, "nmsf_count") for y in FOCAL_YEARS}
        for start, end in [(2024, 2025), (2025, 2026), (2024, 2026)]:
            change_rows.append(
                {
                    "group": group,
                    "metric": "raw_count",
                    "comparison": f"{start}_to_{end}",
                    "start_value": vals[start],
                    "end_value": vals[end],
                    "absolute_change": vals[end] - vals[start],
                    "percent_change": pct_change(vals[end], vals[start]),
                }
            )
    change_summary = pd.DataFrame(change_rows)
    write_csv(change_summary, "task9_change_summary.csv")

    # Metrics used in reports.
    obs_all = group_summary[group_summary["group"] == "All TJ-zone roster rows"]
    obs_ex_tj = group_summary[group_summary["group"] == "TJ-zone excluding TJHSST"]
    obs_private = group_summary[group_summary["group"] == "Private schools"]
    tj_count = {y: lookup(balanced_rates, "TJHSST", y, "nmsf_count") for y in FOCAL_YEARS}
    tj_enroll = {y: lookup(balanced_rates, "TJHSST", y, "grade11_enrollment") for y in FOCAL_YEARS}
    tj_rate = {y: lookup(balanced_rates, "TJHSST", y, "nmsf_per_100_grade11") for y in FOCAL_YEARS}
    base_count = {
        y: lookup(balanced_rates, "Balanced conventional base public", y, "nmsf_count") for y in FOCAL_YEARS
    }
    base_enroll = {
        y: lookup(balanced_rates, "Balanced conventional base public", y, "grade11_enrollment")
        for y in FOCAL_YEARS
    }
    base_rate = {
        y: lookup(balanced_rates, "Balanced conventional base public", y, "nmsf_per_100_grade11")
        for y in FOCAL_YEARS
    }
    pub_count = {
        y: lookup(balanced_rates, "Balanced public including TJHSST", y, "nmsf_count") for y in FOCAL_YEARS
    }
    pub_rate = {
        y: lookup(balanced_rates, "Balanced public including TJHSST", y, "nmsf_per_100_grade11")
        for y in FOCAL_YEARS
    }
    priv_bal = {y: lookup(balanced_counts, "Balanced private schools", y, "nmsf_count") for y in FOCAL_YEARS}

    # Full TJ history for trend context.
    tj_history = df[is_tj].sort_values("class_year")
    pre_tj = tj_history[tj_history["class_year"].between(2019, 2024)]
    pre_tj_rate_weighted = 100 * pre_tj["nmsf_count"].sum() / pre_tj["grade11_enrollment"].sum()
    pre_tj_min_rate = pre_tj["nmsf_per_100_juniors"].min()
    pre_tj_min_count = pre_tj["nmsf_count"].min()

    pre_pub_count, pre_pub_enroll, pre_pub_rate = pooled_rate(
        balanced_rates, "Balanced public including TJHSST", [2023, 2024]
    )
    post_pub_count, post_pub_enroll, post_pub_rate = pooled_rate(
        balanced_rates, "Balanced public including TJHSST", [2025, 2026]
    )
    pre_base_count, pre_base_enroll, pre_base_rate = pooled_rate(
        balanced_rates, "Balanced conventional base public", [2023, 2024]
    )
    post_base_count, post_base_enroll, post_base_rate = pooled_rate(
        balanced_rates, "Balanced conventional base public", [2025, 2026]
    )
    pre_tj_count, pre_tj_enroll, pre_tj_rate = pooled_rate(balanced_rates, "TJHSST", [2023, 2024])
    post_tj_count, post_tj_enroll, post_tj_rate = pooled_rate(balanced_rates, "TJHSST", [2025, 2026])

    base_pooled_gain = post_base_count - pre_base_count
    tj_pooled_change = post_tj_count - pre_tj_count
    public_pooled_change = post_pub_count - pre_pub_count
    offset_pct = 100 * base_pooled_gain / abs(tj_pooled_change)
    offset = pd.DataFrame(
        [
            {
                "comparison": "classes_2023_2024_vs_2025_2026",
                "balanced_base_public_count_change": base_pooled_gain,
                "tjhsst_count_change": tj_pooled_change,
                "balanced_public_including_tj_count_change": public_pooled_change,
                "base_gain_as_pct_of_tj_decline": offset_pct,
                "interpretation": "arithmetic decomposition only; not a causal displacement estimate",
            }
        ]
    )
    write_csv(offset, "task9_offset_decomposition.csv")

    # Internal checks for the canonical focal panels.
    assert len(balanced_count_ids) == 58
    assert len(balanced_public_rate_ids) == 53
    assert len(balanced_base_rate_ids) == 52
    assert len(private_balanced_ids) == 4
    assert (tj_count[2024], tj_count[2025], tj_count[2026]) == (165, 81, 113)
    assert (base_count[2023], base_count[2024], base_count[2025], base_count[2026]) == (159, 166, 168, 224)

    # Markdown table rows.
    coverage_md_rows = []
    for _, r in coverage.iterrows():
        coverage_md_rows.append(
            [
                int(r["class_year"]),
                f"{int(r['observed_count_rows'])}/{int(r['operating_school_rows'])} ({fmt_pct(r['count_coverage_pct'])})",
                f"{int(r['rate_compatible_rows'])}/{int(r['operating_school_rows'])} ({fmt_pct(r['rate_coverage_pct'])})",
                fmt_int(r["observed_nmsf_total"]),
                fmt_rate(r["covered_nmsf_per_100_grade11"]),
            ]
        )

    core_md_rows = []
    for y in FOCAL_YEARS:
        all_row = obs_all[obs_all["class_year"] == y].iloc[0]
        ex_row = obs_ex_tj[obs_ex_tj["class_year"] == y].iloc[0]
        core_md_rows.append(
            [
                y,
                fmt_int(all_row["observed_nmsf_total"]),
                fmt_int(ex_row["observed_nmsf_total"]),
                f"{fmt_int(tj_count[y])} / {fmt_rate(tj_rate[y])}",
                f"{fmt_int(base_count[y])} / {fmt_rate(base_rate[y])}",
                f"{fmt_int(pub_count[y])} / {fmt_rate(pub_rate[y])}",
            ]
        )

    private_md_rows = []
    for _, r in private_sens.iterrows():
        private_md_rows.append(
            [
                int(r["class_year"]),
                f"{int(r['private_observed_count_rows'])}/16",
                int(r["private_missing_count_rows"]),
                fmt_int(r["full_observed_private_nmsf_total"]),
                fmt_int(r["balanced_private_nmsf_total"]),
                int(r["rate_compatible_private_rows"]),
            ]
        )

    state_md_rows = []
    public_state_share: dict[int, float] = {}
    tj_state_share: dict[int, float] = {}
    for y in FOCAL_YEARS:
        pub_share = state_sens[
            (state_sens["class_year"] == y) & (state_sens["group"] == "Balanced public including TJHSST")
        ]["group_share_of_statewide_total_pct"].iloc[0]
        public_state_share[y] = pub_share
        base_share = state_sens[
            (state_sens["class_year"] == y) & (state_sens["group"] == "Balanced conventional base public")
        ]["group_share_of_statewide_total_pct"].iloc[0]
        tj_share = state_sens[(state_sens["class_year"] == y) & (state_sens["group"] == "TJHSST")][
            "group_share_of_statewide_total_pct"
        ].iloc[0]
        tj_state_share[y] = tj_share
        state_md_rows.append(
            [y, VA_CUTOFF[y], VA_STATE_TOTAL[y], fmt_pct(pub_share), fmt_pct(base_share), fmt_pct(tj_share)]
        )

    program_md_rows = []
    for _, r in program_sens.iterrows():
        program_md_rows.append(
            [
                int(r["class_year"]),
                fmt_int(r["program_nmsf_count"]),
                fmt_int(r["base_public_observed_count_including_program"]),
                fmt_int(r["base_public_observed_count_excluding_program"]),
                fmt_rate(r["covered_rate_excluding_program"]),
            ]
        )

    pooled_direction_counts = pooled_school["direction"].value_counts().to_dict()
    pooled_school_median_change = pooled_school["rate_point_change"].median()
    pathway_md_rows = []
    for pathway in pathway_order:
        p = pathway_sens[pathway_sens["tj_pathway"] == pathway].set_index("class_year")
        pathway_md_rows.append(
            [
                pathway,
                int(p.loc[2026, "school_count"]),
                fmt_rate(p.loc[2024, "nmsf_per_100_grade11"]),
                fmt_rate(p.loc[2025, "nmsf_per_100_grade11"]),
                fmt_rate(p.loc[2026, "nmsf_per_100_grade11"]),
            ]
        )

    pooled_md_rows = [
        [
            "Balanced public including TJHSST",
            fmt_int(pre_pub_count),
            fmt_int(post_pub_count),
            fmt_int(public_pooled_change),
            fmt_rate(pre_pub_rate),
            fmt_rate(post_pub_rate),
            fmt_pct(pct_change(post_pub_rate, pre_pub_rate), sign=True),
        ],
        [
            "Balanced conventional base public",
            fmt_int(pre_base_count),
            fmt_int(post_base_count),
            f"+{fmt_int(base_pooled_gain)}",
            fmt_rate(pre_base_rate),
            fmt_rate(post_base_rate),
            fmt_pct(pct_change(post_base_rate, pre_base_rate), sign=True),
        ],
        [
            "TJHSST",
            fmt_int(pre_tj_count),
            fmt_int(post_tj_count),
            fmt_int(tj_pooled_change),
            fmt_rate(pre_tj_rate),
            fmt_rate(post_tj_rate),
            fmt_pct(pct_change(post_tj_rate, pre_tj_rate), sign=True),
        ],
    ]

    robustness = f"""# Task 9 Robustness Checks

Generated: {TODAY}

## Scope and analysis rules

This report recomputes every numerical result from `data/processed/analysis_panel.csv` rather than copying the Milestone 8 descriptive report. It treats `missing_source` as missing, never as zero. Two distinct estimands are kept separate:

1. **Observed-count totals** sum all source-backed counts, even where enrollment is unavailable.
2. **Covered rates** sum NMSF counts and grade-11 enrollment only over rows with both inputs, then calculate `100 × NMSF / grade-11 enrollment`.

The primary robustness window is Classes 2023-2026. Full-zone count coverage is too incomplete in Classes 2019-2022 for direct zone-wide pre/post comparisons: those years have 48-50 missing NMSF rows each. TJHSST's own 2019-2026 series is complete and is used separately for trend context.

## 1. Coverage

{md_table(["Class", "Count coverage", "Rate-compatible coverage", "Observed total", "Covered rate /100"], coverage_md_rows)}

Coverage improved sharply for counts by Class 2025, but rate-compatible coverage did not: private-school denominators remain sparse and several public denominators or school-year observations are unavailable. This is why the balanced panels below are the cleanest like-for-like checks.

## 2. Raw counts, normalized rates, and TJHSST inclusion

The table gives `count / rate per 100 grade-11 students` for balanced public panels. Full observed totals in the first two columns are not rate-compatible totals.

{md_table(["Class", "Observed zone incl. TJ", "Observed zone excl. TJ", "TJHSST count / rate", "Balanced base-public count / rate", "Balanced public incl. TJ count / rate"], core_md_rows)}

The principal discontinuity is not an enrollment artifact. From Class 2024 to Class 2025, TJHSST fell from **{fmt_int(tj_count[2024])} to {fmt_int(tj_count[2025])} semifinalists ({fmt_pct(pct_change(tj_count[2025], tj_count[2024]))})** and from **{fmt_rate(tj_rate[2024])} to {fmt_rate(tj_rate[2025])} per 100 juniors ({fmt_pct(pct_change(tj_rate[2025], tj_rate[2024]))})**. Class 2026 rebounded to **{fmt_int(tj_count[2026])}** and **{fmt_rate(tj_rate[2026])} per 100**, but remained below Class 2024 by **{fmt_pct(pct_change(tj_count[2026], tj_count[2024]))} in count** and **{fmt_pct(pct_change(tj_rate[2026], tj_rate[2024]))} in rate**.

Excluding TJHSST reverses the raw-count direction: observed non-TJ counts rise from {fmt_int(obs_ex_tj.loc[obs_ex_tj.class_year.eq(2024), "observed_nmsf_total"].iloc[0])} in Class 2024 to {fmt_int(obs_ex_tj.loc[obs_ex_tj.class_year.eq(2025), "observed_nmsf_total"].iloc[0])} in Class 2025 and {fmt_int(obs_ex_tj.loc[obs_ex_tj.class_year.eq(2026), "observed_nmsf_total"].iloc[0])} in Class 2026. Because private and other source coverage changes, that raw reversal is not itself a clean time trend. In the balanced {len(balanced_base_rate_ids)}-school conventional public rate panel, the immediate Class 2025 change is nearly flat: **{fmt_rate(base_rate[2024])} to {fmt_rate(base_rate[2025])} per 100 ({fmt_pct(pct_change(base_rate[2025], base_rate[2024]), sign=True)})**. The larger increase appears in Class 2026, to **{fmt_rate(base_rate[2026])} ({fmt_pct(pct_change(base_rate[2026], base_rate[2025]), sign=True)} versus 2025)**.

## 3. Balanced-panel sensitivity

The balanced count panel includes **{len(balanced_count_ids)} schools** with source-backed counts in every focal year: {len(conventional_balanced_ids)} conventional public high schools, one public secondary program, {len(private_balanced_ids)} private schools, and TJHSST. The balanced public rate panel includes **{len(balanced_public_rate_ids)} schools** with both counts and enrollment in every year: {len(balanced_base_rate_ids)} conventional base public schools plus TJHSST.

Pooled 2023-2024 versus 2025-2026 rates are secondary summaries because they conceal the very different 2025 and 2026 patterns:

{md_table(["Balanced group", "2023-24 count", "2025-26 count", "Count change", "2023-24 pooled rate", "2025-26 pooled rate", "Rate change"], pooled_md_rows)}

On this fixed {len(balanced_public_rate_ids)}-school public panel, base-school counts rise by **{fmt_int(base_pooled_gain)}**, arithmetically offsetting **{fmt_pct(offset_pct)}** of TJHSST's **{fmt_int(abs(tj_pooled_change))}-student decline**. The combined public count still falls by **{fmt_int(abs(public_pooled_change))}**. This is an accounting decomposition, not proof that the base-school gains consist of students displaced from TJHSST, and it should not replace the year-by-year results.

The base-school increase is heterogeneous rather than universal. Comparing pooled 2023-2024 and 2025-2026 school rates, **{pooled_direction_counts.get("increase", 0)} of {len(balanced_base_rate_ids)} schools increase, {pooled_direction_counts.get("decrease", 0)} decrease, and {pooled_direction_counts.get("unchanged", 0)} are unchanged**; the median school change is only **{fmt_rate(pooled_school_median_change)} NMSF per 100 juniors**. Pathway aggregates also vary:

{md_table(["Pathway", "Balanced schools", "2024 rate", "2025 rate", "2026 rate"], pathway_md_rows)}

The Class 2026 increase is strongest in FCPS Regions 1, 2, and 5. FCPS Region 3 remains low, Region 4 falls from its 2025 spike, and Loudoun is close to its 2024 rate. The aggregate base-school gain should therefore not be described as a uniform zone-wide shift.

## 4. Private-school missingness

{md_table(["Class", "Private count rows observed", "Missing rows", "Full observed total", f"Balanced {len(private_balanced_ids)}-school total", "Rate-compatible rows"], private_md_rows)}

The four complete private schools are Bishop O'Connell, Flint Hill, The Potomac School, and The Madeira School. Their total is **{fmt_int(priv_bal[2024])} in 2024, {fmt_int(priv_bal[2025])} in 2025, and {fmt_int(priv_bal[2026])} in 2026**. The apparent full-observed increase from {fmt_int(obs_private.loc[obs_private.class_year.eq(2024), "observed_nmsf_total"].iloc[0])} to {fmt_int(obs_private.loc[obs_private.class_year.eq(2025), "observed_nmsf_total"].iloc[0])} coincides with coverage expanding from 5 to 16 private schools. It therefore cannot be interpreted as a measured private-school offset. No rate-compatible private panel exists for Classes 2024-2026.

## 5. Excluding non-conventional programs

H-B Woodlawn is the only `public_secondary_program` row. It has no grade-11 denominator in the panel, so it never contributes to a covered rate.

{md_table(["Class", "H-B count", "Base-public count incl. program", "Count excl. program", "Covered conventional-public rate"], program_md_rows)}

Excluding it changes the observed base-public count by only 1-6 students per year and leaves every covered rate unchanged. The main findings are not driven by the program row.

The 140-row manual-review queue includes 76 duplicate public-school source rows, 37 unresolved school-year source gaps, 11 non-roster rows, 7 TJHSST resident subsets, 5 duplicate private-school rows, 3 former-PWCS TJHSST subsets, and 1 unattributed total. They are not added because doing so could double count schools or TJHSST, turn source gaps into zeros, or mix resident totals with school totals.

## 6. Is Class 2025 isolated?

At TJHSST, Class 2025 is the sharpest break, but Class 2026 is not a return to the earlier range. Across Classes 2019-2024, TJHSST averaged **{fmt_rate(pre_tj_rate_weighted)} NMSF per 100 juniors** on a pooled denominator and never fell below **{fmt_rate(pre_tj_min_rate)}** or **{fmt_int(pre_tj_min_count)} semifinalists**. Class 2026's **{fmt_rate(tj_rate[2026])} per 100** and **{fmt_int(tj_count[2026])} semifinalists** remain below both pre-policy minima.

For the balanced base-public panel, by contrast, 2023-2025 are nearly flat ({fmt_rate(base_rate[2023])}, {fmt_rate(base_rate[2024])}, {fmt_rate(base_rate[2025])}), followed by a distinct 2026 increase to {fmt_rate(base_rate[2026])}. Thus, the evidence does **not** show a smooth post-policy trend. It shows a TJHSST break in 2025, a partial TJHSST rebound in 2026, and a base-school rise concentrated in 2026.

## 7. Virginia cutoff and statewide normalization

More than 16,000 Semifinalists represent less than 1% of U.S. graduating seniors nationally and are named on a state-representational basis.[^nmsc] The canonical panel correctly leaves Virginia cutoff and statewide-total fields as `not_sourced`. For this robustness check only, the following secondary Compass figures are used and kept outside the panel:[^cutoffs][^state]

{md_table(["Class", "VA cutoff", "VA total", "Balanced public share", "Base-public share", "TJHSST share"], state_md_rows)}

The Class 2026 Virginia cutoff was two Selection Index points higher than Class 2025 (224 versus 222), while the reported statewide semifinalist total rose from 394 to 489. A cutoff-only adjustment is therefore inadequate. On the supplemental statewide denominator, the balanced public share falls from **{fmt_pct(public_state_share[2024])} in 2024** to **{fmt_pct(public_state_share[2025])} in 2025** and recovers only to **{fmt_pct(public_state_share[2026])} in 2026**. TJHSST's share remains far below 2024 ({fmt_pct(tj_state_share[2024])} to {fmt_pct(tj_state_share[2025])} to {fmt_pct(tj_state_share[2026])}). These figures strengthen the conclusion that 2026 is a partial, not complete, recovery relative to Virginia, but they remain secondary-source checks.

## 8. COVID, digital testing, and cohort timing

- FCPS provided virtual instruction in spring and fall 2020, then phased in concurrent instruction beginning in February 2021.[^virtual]
- FCPS reopened all schools for five-day in-person learning in August 2021, with 99.5% of students returning in person.[^inperson]
- Class 2025 qualified in fall 2023, the first digital PSAT/NMSQT administration.[^digital]
- Class 2026 qualified in fall 2024, the second digital administration.

The assessment-format break occurs at the same Class 2025 boundary as the TJHSST admissions-policy exposure. Without school-level PSAT participation and score-distribution data, the policy effect cannot be separated cleanly from test-format, participation, cutoff, and cohort-composition changes.

## 9. Admissions mechanism interpretation

The adopted process should not be described as random selection. On December 17, 2020, the Board rejected the proposed “Hybrid Merit Lottery” motion and adopted a holistic-review motion effective for the class entering in fall 2021.[^board] For the Class of 2025, FCPS replaced the prior admissions tests and teacher recommendations, raised the minimum GPA, used essays/holistic review and experience factors, expanded the class toward 550, and provided a 1.5% public-middle-school allocation with remaining seats unallocated.[^court][^profile] An official January 2021 application bulletin confirms the Class 2025 application, eligibility, Student Portrait Sheet, essay, and calendar details.[^class25]

Regulation 3355.14, effective April 28, 2021, is reproduced in the court filing. Regulation 3355.15, effective November 9, 2021, is the best recovered governing regulation for the Class 2026 cycle and explicitly references that class; an official October 2021 bulletin confirms the application window, January 2022 writing administration, and April 29 notification deadline.[^reg15][^class26] The included Regulation 3355.16 became effective May 17, 2022—after the Class 2026 bulletin’s final-notification date—so it should not be applied retroactively to either focal class. The current FCPS process retains holistic evaluation, a 1.5% presumptive allocation, and an unallocated pool.[^current]

The archived annual Notice 3355 documents themselves were not recovered. The official class-specific bulletins recover key calendar and assessment details, while the FCPS index confirms that N3355 exists.[^index] The analysis therefore describes the broad class-specific regimes but does not claim that every implementation detail has been reconstructed or estimate the effect of any single component.

## Robustness conclusion

The TJHSST decline in the first affected class is large in both raw counts and enrollment-normalized rates, and it is not explained by the H-B Woodlawn program or simple enrollment growth. Conventional base-school rates do not show an immediate offset in Class 2025; a substantial increase appears in Class 2026. Combining TJHSST and base schools produces a near return to the 2024 local rate by 2026, but only a partial recovery after supplemental statewide normalization. Private-school data are too incomplete to establish the remaining offset. These are descriptive findings, not causal estimates.

## Generated supporting tables

- `reports/tables/task9_group_year_summary.csv`
- `reports/tables/task9_coverage_2023_2026.csv`
- `reports/tables/task9_balanced_count_panel.csv`
- `reports/tables/task9_balanced_rate_panel.csv`
- `reports/tables/task9_balanced_panel_membership.csv`
- `reports/tables/task9_private_sensitivity.csv`
- `reports/tables/task9_program_sensitivity.csv`
- `reports/tables/task9_manual_review_issue_counts.csv`
- `reports/tables/task9_offset_decomposition.csv`
- `reports/tables/task9_state_normalization_supplemental.csv`
- `reports/tables/task9_cohort_timing.csv`
- `reports/tables/task9_change_summary.csv`
- `reports/tables/task9_balanced_base_school_changes.csv`
- `reports/tables/task9_school_pooled_changes.csv`
- `reports/tables/task9_pathway_rate_sensitivity.csv`

[^nmsc]: National Merit Scholarship Corporation, *Information about the 2026 National Merit Scholarship Competition*, {URLS["nmsc_2026"]}.
[^cutoffs]: Compass Education Group, *Historical National Merit Cutoffs 2008 to Present*, {URLS["cutoffs"]}. Secondary source; not written into the canonical panel.
[^state]: Compass Education Group, *National Merit Semifinalists and Commended Students by State*, {URLS["state_totals"]}. Secondary source; not written into the canonical panel.
[^virtual]: Fairfax County Public Schools, *FCPS 2020-21 Evaluation Report*, {URLS["fcps_virtual_eval"]}.
[^inperson]: Fairfax County Public Schools, *FCPS This Week — August 25, 2021*, {URLS["fcps_in_person_2021"]}.
[^digital]: College Board, *How to Get Ready for the Digital PSAT/NMSQT*, {URLS["collegeboard_digital"]}.
[^board]: Fairfax County School Board, December 17, 2020 minutes, {URLS["board_minutes_2020"]}.
[^court]: Fairfax County School Board court filing with the Jeremy Shughart declaration and Regulation 3355.14 exhibit, March 4, 2022, {URLS["court_filing"]}.
[^reg15]: Archived copy of Fairfax County Public Schools Regulation 3355.15, effective November 9, 2021, {URLS["reg3355_15"]}. A local copy is archived at `docs/source_notes/FCPS Regulation 3355.15 TJHSST Admissions.pdf`.
[^class25]: Fairfax County Public Schools, *Invitation to Apply to TJHSST—Class of 2025*, January 29, 2021, {URLS["class2025_notice"]}.
[^class26]: Fairfax County Public Schools, *TJ Admissions—Freshman Application Window Opening—Class of 2026*, October 26, 2021, {URLS["class2026_notice"]}.
[^profile]: TJHSST, *School Profile 2021-22*, {URLS["tj_profile_2021"]}.
[^current]: Fairfax County Public Schools, *TJHSST Freshman Application Process*, {URLS["fcps_current"]}.
[^index]: Fairfax County School Board, numeric policy index listing R3355 and N3355, {URLS["fcps_index"]}.
"""

    limitations = f"""# Task 9 Limitations

Generated: {TODAY}

## 1. NMSF measures only the extreme right tail

National Merit Semifinalist status identifies a very small group of high scorers: more than 16,000 students, representing less than 1% of U.S. graduating seniors nationally, selected on a state-representational basis.[^nmsc] The outcome is useful for studying the extreme academic right tail, but it does not measure median achievement, classroom engagement, research productivity, student well-being, peer norms, or school culture as a whole.

NMSC itself cautions that its qualifying data do not measure the quality or effectiveness of education within a school, district, or state.[^nmsc] A decline in NMSF cannot by itself establish a decline in “academic culture.” It may be consistent with a change in the concentration or production of very high PSAT Selection Index scores, and nothing broader should be inferred without additional outcomes.

## 2. School-level PSAT participation is missing

The denominator is grade-11 enrollment, not the number of eligible juniors who actually took the PSAT/NMSQT. Schools and districts can differ in test-day participation, absenteeism, alternative testing, and whether all juniors are tested. COVID disrupted schooling and test access, and the panel has no school-year PSAT participation control.[^virtual]

Therefore, `NMSF per 100 juniors` is an outcome-rate proxy, not a direct qualification rate among test takers. A school could change its measured rate because participation changed even if the score distribution among test takers did not.

## 3. Virginia cutoff and test-form changes

Virginia's canonical cutoff and statewide-total columns remain blank with `not_sourced` status. Task 9 uses Compass values only as a clearly labeled supplemental check, not as canonical data. NMSC does not publish a convenient official historical cutoff table, and secondary reports may be revised.

The focal policy boundary also coincides with the 2023 move to the digital PSAT/NMSQT.[^digital] Class 2025 is the first policy-affected TJHSST class and the first digital-PSAT NMSF class. That coincidence makes it impossible, with these data alone, to attribute the break uniquely to admissions policy.

A state cutoff does not fully standardize cohorts. The supplemental data show Virginia's cutoff rising from 222 to 224 between Classes 2025 and 2026 while the reported statewide total also rises markedly. Score-distribution and tie effects can change the number of semifinalists at a given cutoff.

## 4. Incomplete and changing source coverage

The panel is explicit about missingness, but the remaining gaps matter:

- In Classes 2019-2022, 48-50 of 76 rows lack source-backed NMSF counts. Full-zone historical totals are therefore not comparable with 2023-2026.
- Private count coverage is 4/16 schools in 2023, 5/16 in 2024, 16/16 in 2025, and 10/16 in 2026.
- Rate-compatible private coverage is {private_rate_coverage_text}.
- The official LCPS Class 2025 release is total-only and cannot establish school-level counts or zeros; some LCPS school rows remain missing.

The balanced panels improve comparability by holding schools fixed, but they answer a narrower question about continuously observed schools and may not represent omitted schools.

## 5. Private-school inference is especially weak

Private-school location does not prove that a student resided in the TJHSST service area, was eligible for TJHSST, applied to TJHSST, or would otherwise have attended a particular base school. The admissions rule places non-public applicants in the unallocated pool rather than assigning them by the private school's location. The private-school analysis is therefore a geographic outcome bucket, not a measured displacement channel.

Four private schools have complete 2023-2026 counts. The 2023-24 NCES locator pass adds rate-compatible Class 2025 denominators for {private_2025_rate_rows} private rows, but no balanced private rate panel spans Classes 2023-2026. The project cannot estimate a complete private-school offset.

## 6. Grade-11 enrollment is not an admissions allocation denominator

The rate denominator measures the size of the outcome cohort at the high school. TJHSST admissions allocations are based on public schools' eighth-grade populations under the post-2020 process, not on high-school grade-11 enrollment.[^current] These denominators serve different purposes and must not be conflated.

The panel also lacks applicants, eligible applicants, offers, waitpool outcomes, acceptances, enrolled students, allocated/unallocated seat status, and the eighth-grade population inputs used in each admissions cycle. Without those data, the analysis cannot quantify how many high scorers were actually redistributed by the policy.

## 7. TJHSST cannot be reassigned to base schools

TJHSST is one regional school row. District announcements sometimes identify TJ students by residence, former middle school, or cooperating division. Adding those subsets to base-school or district counts would double count the same TJHSST students. The manual-review queue correctly excludes such rows.

Likewise, non-roster programs, homeschool/online categories, and duplicate source snapshots are not added unless their scope and duplication can be resolved.

## 8. Program and school-structure differences

H-B Woodlawn is a public secondary program rather than a conventional base high school and lacks a grade-11 denominator. Excluding it barely changes raw counts and does not change covered rates, but the broader roster still mixes school types with different selection, attendance, and program structures.

School openings, renames, relocations, boundary changes, and grade configurations can affect both counts and denominators. History flags are present, but no model adjusts for every local structural change.

## 9. Admissions-policy history is incomplete

The Class 2025 process is documented through the December 2020 Board minutes, an official January 2021 application bulletin, an FCPS court filing containing Regulation 3355.14, contemporaneous FCPS materials, and the 2021-22 TJHSST profile.[^board][^class25][^court][^profile] The best recovered governing regulation for the Class 2026 process is Regulation 3355.15, supplemented by an official October 2021 application bulletin.[^reg15][^class26]

The included Regulation 3355.16 took effect May 17, 2022, after the posted final-notification date for the Class 2026 cycle, and should not be treated as the governing source for either focal class. Archived annual Notice 3355 documents themselves were not recovered. The class-specific bulletins establish key dates and assessment steps, but not necessarily every implementation detail.

The adopted process was not random selection. The Board rejected the proposed hybrid merit-lottery motion and adopted holistic review; applicants were evaluated and ranked within allocated and unallocated pools.[^board]

## 10. The design is descriptive, not causal

There is no untreated comparison region, no student-level counterfactual, and only two policy-exposed cohorts. The analysis cannot separate:

- admissions-policy effects;
- digital-PSAT and scaling effects;
- Virginia cutoff and statewide score-distribution changes;
- PSAT participation changes;
- COVID and recovery effects;
- enrollment and migration changes;
- base-school program changes; or
- ordinary year-to-year sampling variation.

A causal design would require credible comparison schools/regions, pre-trend assessment, consistent outcomes, participation controls, and preferably student-level or applicant-level data.

## 11. Small numbers and uncertainty

Many schools have zero to a few semifinalists. Percentage changes from a small base are unstable, and school-level rankings can be dominated by one or two students. The reports emphasize pooled groups and fixed-school panels, but they do not calculate formal confidence intervals because the data are not a simple random sample and the main uncertainties are measurement and missingness rather than binomial sampling alone.

## 12. Claim boundary

The defensible claim is narrow: the data describe changes in source-backed NMSF counts and NMSF-per-grade-11-enrollment rates across TJHSST, continuously observed public base schools, and a limited private-school subset. They do not establish changes in median academic performance, student quality, teaching quality, school culture, policy merit, or causation.

[^nmsc]: National Merit Scholarship Corporation, *Information about the 2026 National Merit Scholarship Competition*, {URLS["nmsc_2026"]}.
[^virtual]: Fairfax County Public Schools, *FCPS 2020-21 Evaluation Report*, {URLS["fcps_virtual_eval"]}.
[^digital]: College Board, *How to Get Ready for the Digital PSAT/NMSQT*, {URLS["collegeboard_digital"]}.
[^current]: Fairfax County Public Schools, *TJHSST Freshman Application Process*, {URLS["fcps_current"]}.
[^board]: Fairfax County School Board, December 17, 2020 minutes, {URLS["board_minutes_2020"]}.
[^court]: Fairfax County School Board court filing with Regulation 3355.14 and declarations, March 4, 2022, {URLS["court_filing"]}.
[^reg15]: Archived copy of Fairfax County Public Schools Regulation 3355.15, effective November 9, 2021, {URLS["reg3355_15"]}.
[^class25]: Fairfax County Public Schools, *Invitation to Apply to TJHSST—Class of 2025*, January 29, 2021, {URLS["class2025_notice"]}.
[^class26]: Fairfax County Public Schools, *TJ Admissions—Freshman Application Window Opening—Class of 2026*, October 26, 2021, {URLS["class2026_notice"]}.
[^profile]: TJHSST, *School Profile 2021-22*, {URLS["tj_profile_2021"]}.
"""

    initial_findings = f"""# Task 9 Initial Findings

Generated: {TODAY}

## Bottom line

The strongest descriptive finding is a large, enrollment-adjusted decline in TJHSST's National Merit Semifinalist right tail beginning with the first class admitted under the post-2020 process. The first affected class, 2025, is the sharpest break. Class 2026 rebounds, but TJHSST remains below every pre-policy class in the available 2019-2024 TJ series.

Continuously observed conventional public base schools do **not** show an immediate offset in Class 2025: their aggregate rate is nearly unchanged from 2024. They rise substantially in Class 2026. When TJHSST and those base schools are combined, the local grade-11-normalized rate nearly returns to its 2024 level by 2026; a supplemental Virginia-wide normalization shows only a partial recovery. Private-school data are not complete enough to determine the remaining offset.

This pattern is consistent with a reduction in the concentration of the extreme PSAT right tail at TJHSST and some later increase at base schools. It does not prove that the admissions change caused either pattern or that broader academic culture declined.

## Descriptive findings

### 1. The TJHSST break survives enrollment normalization

- Class 2024: **{fmt_int(tj_count[2024])} NMSF / {fmt_int(tj_enroll[2024])} juniors = {fmt_rate(tj_rate[2024])} per 100**.
- Class 2025: **{fmt_int(tj_count[2025])} / {fmt_int(tj_enroll[2025])} = {fmt_rate(tj_rate[2025])} per 100**.
- Class 2026: **{fmt_int(tj_count[2026])} / {fmt_int(tj_enroll[2026])} = {fmt_rate(tj_rate[2026])} per 100**.

The 2024-to-2025 changes are **{fmt_pct(pct_change(tj_count[2025], tj_count[2024]))} in count** and **{fmt_pct(pct_change(tj_rate[2025], tj_rate[2024]))} in rate**. Enrollment expansion therefore does not explain the decline. The 2026 rate remains **{fmt_pct(pct_change(tj_rate[2026], tj_rate[2024]))} below 2024**.

### 2. Class 2025 is not merely a comparison to an ordinary single year

Class 2024 was a high TJHSST year, so the one-year drop overstates the comparison with a longer baseline. Even so, Classes 2019-2024 pooled to **{fmt_rate(pre_tj_rate_weighted)} NMSF per 100 juniors**, and the lowest pre-policy annual TJ rate was **{fmt_rate(pre_tj_min_rate)}**. Class 2025 ({fmt_rate(tj_rate[2025])}) and Class 2026 ({fmt_rate(tj_rate[2026])}) are both below that pre-policy range.

Thus, 2025 is an exceptional discontinuity, while 2026 provides evidence of persistence with partial recovery rather than complete reversion.

### 3. The immediate base-public offset is small; the 2026 increase is large

In the balanced {len(balanced_base_rate_ids)}-school conventional public panel:

- Class 2023: **{fmt_int(base_count[2023])} / {fmt_int(base_enroll[2023])} = {fmt_rate(base_rate[2023])} per 100**.
- Class 2024: **{fmt_int(base_count[2024])} / {fmt_int(base_enroll[2024])} = {fmt_rate(base_rate[2024])}**.
- Class 2025: **{fmt_int(base_count[2025])} / {fmt_int(base_enroll[2025])} = {fmt_rate(base_rate[2025])}**.
- Class 2026: **{fmt_int(base_count[2026])} / {fmt_int(base_enroll[2026])} = {fmt_rate(base_rate[2026])}**.

The rate changes only **{fmt_pct(pct_change(base_rate[2025], base_rate[2024]), sign=True)}** from 2024 to 2025, then **{fmt_pct(pct_change(base_rate[2026], base_rate[2025]), sign=True)}** from 2025 to 2026. A simple story in which the first policy-affected cohort immediately reappears as NMSF gains at base schools is not supported by the aggregate 2025 data.

Pooling 2023-2024 against 2025-2026, base-school counts increase by **{fmt_int(base_pooled_gain)}** while TJHSST declines by **{fmt_int(abs(tj_pooled_change))}**. The base gain therefore offsets **{fmt_pct(offset_pct)}** of the TJ decline arithmetically, leaving the balanced public panel down **{fmt_int(abs(public_pooled_change))}** semifinalists. The gain is heterogeneous: {pooled_direction_counts.get("increase", 0)} of {len(balanced_base_rate_ids)} school rates rise, {pooled_direction_counts.get("decrease", 0)} fall, and {pooled_direction_counts.get("unchanged", 0)} are unchanged. This is not evidence that the gains are displaced TJHSST students.

### 4. The combined public-zone result falls in 2025 and nearly recovers locally in 2026

For the balanced {len(balanced_public_rate_ids)}-school public panel including TJHSST, the rate is **{fmt_rate(pub_rate[2024])} in 2024, {fmt_rate(pub_rate[2025])} in 2025, and {fmt_rate(pub_rate[2026])} in 2026**. The 2026 value is **{fmt_pct(pct_change(pub_rate[2026], pub_rate[2024]))}** relative to 2024.

This local near-recovery does not mean the regional right tail fully recovered relative to Virginia. Using secondary statewide totals, the balanced public panel's share is approximately **{fmt_pct(public_state_share[2024])} in 2024, {fmt_pct(public_state_share[2025])} in 2025, and {fmt_pct(public_state_share[2026])} in 2026**. TJHSST's own share falls from **{fmt_pct(tj_state_share[2024])} to {fmt_pct(tj_state_share[2025])} to {fmt_pct(tj_state_share[2026])}**.[^state]

### 5. Private schools do not provide a measurable complete offset

The full observed private total rises from 18 in 2024 to 34 in 2025, but count coverage simultaneously expands from 5 of 16 schools to 16 of 16. In the four-school balanced private panel, the totals are **{fmt_int(priv_bal[2023])}, {fmt_int(priv_bal[2024])}, {fmt_int(priv_bal[2025])}, and {fmt_int(priv_bal[2026])}** for Classes 2023-2026. The 2023-24 NCES locator pass adds Class 2025 denominators for {private_2025_rate_rows} private rows, but Classes 2024 and 2026 still lack private denominator coverage, so there is no balanced private denominator panel across Classes 2023-2026.

The defensible conclusion is “private offset unresolved,” not “private offset observed.”

### 6. Non-conventional programs do not drive the result

Removing H-B Woodlawn changes base-public raw counts by 3, 1, 3, and 6 in Classes 2023-2026 and changes no rate because its grade-11 denominator is unavailable. Excluded manual-review rows cannot be safely added without resolving duplicates and scope.

## Plausible interpretations, not established causes

1. **Concentration interpretation.** The post-2020 admissions process may have reduced the concentration of exceptionally high PSAT scorers at TJHSST. The persistent TJ rate gap is consistent with this, but the panel does not observe applicants' prior ability or attendance counterfactuals.
2. **Redistribution interpretation.** Some extreme-right-tail performance may have shifted to base schools, especially by Class 2026. The delayed timing, statewide surge, and digital-test changes prevent treating the entire increase as displaced former TJ students.
3. **Context/peer interpretation.** TJHSST's environment could affect whether already-strong students cross the NMSF threshold. The regional shortfall in 2025 is consistent with such an effect, but no student-level design identifies it.

## What is not established

- That the admissions change caused the NMSF decline.
- That students were selected randomly. The adopted process used holistic evaluation, a 1.5% public-school allocation, and an unallocated pool.[^policy]
- That admitted students were less capable, less interested in STEM, or changed TJHSST's median academic culture.
- That gains at a named base or private school came from students who otherwise would have attended TJHSST.
- That NMSF trends measure overall academic outcomes or policy quality. NMSC explicitly cautions that its qualifying data do not measure educational quality or effectiveness at the school, district, or state level.[^nmsc]

## Assessment of the working hypothesis

The evidence **supports a narrow descriptive version** of the hypothesis: the first two post-policy cohorts show a large reduction in TJHSST's NMSF rate, and the first affected cohort does not show a full same-year offset at continuously observed conventional public base schools. The second affected cohort shows a material base-school increase and a partial combined-zone recovery.

The evidence **does not yet support the causal context-effect version**. The analysis needs school-level PSAT participation and distributions, complete private-school data, sourced historical Virginia benchmarks, actual applicant/offer/enrollment data by allocation pool, and a credible comparison design before attributing the net regional pattern to TJHSST peer effects or the admissions policy.

## Priority next evidence

The highest-value follow-on is not more NMSF name counting. It is obtaining: (1) school-level PSAT participation and score distributions; (2) TJ applicant, offer, waitpool, acceptance, and enrollment counts by source school and allocated/unallocated pool; and (3) one or more broader upper-tail measures such as SAT threshold rates, AP 5 rates, or contest outcomes. Those data would distinguish score-production changes from participation, threshold, and redistribution effects.

[^nmsc]: National Merit Scholarship Corporation, *Information about the 2026 National Merit Scholarship Competition*, {URLS["nmsc_2026"]}.
[^state]: Supplemental secondary-source values from Compass Education Group: {URLS["cutoffs"]} and {URLS["state_totals"]}. The canonical panel retains `not_sourced` placeholders.
[^policy]: Fairfax County School Board, December 17, 2020 minutes, {URLS["board_minutes_2020"]}; FCPS Class 2025/2026 documentation in the March 4, 2022 court filing and Regulation 3355.14 exhibit, {URLS["court_filing"]}; Regulation 3355.15, {URLS["reg3355_15"]}.
"""

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "robustness.md").write_text(robustness, encoding="utf-8")
    (REPORTS / "limitations.md").write_text(limitations, encoding="utf-8")
    (REPORTS / "initial_findings.md").write_text(initial_findings, encoding="utf-8")

    source_notes = f"""# Task 9 Web Research Sources

Generated: {TODAY}

This file records external sources used only for Task 9 interpretation and supplemental checks. The canonical panel was not modified.

## Primary sources

- National Merit Scholarship Corporation, *Information about the 2026 National Merit Scholarship Competition*: {URLS["nmsc_2026"]}
- National Merit Scholarship Corporation, 2026 Semifinalist press release: {URLS["nmsc_release"]}
- Fairfax County School Board court filing containing the Jeremy Shughart declaration and Regulation 3355.14 exhibit: {URLS["court_filing"]}
- TJHSST, *School Profile 2021-22*: {URLS["tj_profile_2021"]}
- Fairfax County Public Schools, current freshman application and seat-allocation process: {URLS["fcps_current"]}
- Fairfax County School Board numeric index listing R3355 and N3355: {URLS["fcps_index"]}
- College Board, digital PSAT/NMSQT transition: {URLS["collegeboard_digital"]}
- FCPS, 2020-21 virtual-learning evaluation: {URLS["fcps_virtual_eval"]}
- FCPS, five-day in-person reopening update, August 25, 2021: {URLS["fcps_in_person_2021"]}
- Fairfax County School Board, December 17, 2020 admissions vote minutes: {URLS["board_minutes_2020"]}
- Archived copy of FCPS Regulation 3355.15 (best recovered governing regulation for the Class 2026 cycle): {URLS["reg3355_15"]}
- Official Class 2025 application bulletin: {URLS["class2025_notice"]}
- Official Class 2026 application bulletin: {URLS["class2026_notice"]}
- Archived local copy: `docs/source_notes/FCPS Regulation 3355.15 TJHSST Admissions.pdf` (SHA-256 `0d8bf64824f5f9755acaabf377939999e9afb1def2b941736bb5920539885003`).
- Included local source: `docs/source_notes/FCPS Regulation 3355.16 TJHSST Admissions.pdf` (effective May 17, 2022).

## Supplemental secondary sources

- Compass historical state cutoffs: {URLS["cutoffs"]}
- Compass semifinalist totals by state: {URLS["state_totals"]}

These values are written only to `task9_state_normalization_supplemental.csv`; the panel's Virginia fields remain `not_sourced`. NMSC's official guide is the source for the Class 2026 Virginia cutoff and total and for its warning that program data do not measure school, district, or state educational quality; Compass is used only to supply a consistent four-class historical series.

## Unresolved source gap

Archived annual Notice 3355 documents for the Class of 2025 and Class of 2026 admissions cycles were not recovered through web search. Official FCPS bulletins do establish the main application windows, writing-administration dates, and posted notification timing for those classes. The reports combine those bulletins with the historical regulation versions and court exhibits, while explicitly avoiding claims that every class-specific procedural detail has been reconstructed.
"""
    SOURCE_NOTES.mkdir(parents=True, exist_ok=True)
    (SOURCE_NOTES / "task9_web_research_sources.md").write_text(source_notes, encoding="utf-8")

    # Compact machine-readable validation summary.
    validation = {
        "panel_rows": len(df),
        "unique_school_year_rows": df[["school_id", "class_year"]].drop_duplicates().shape[0],
        "balanced_count_schools": len(balanced_count_ids),
        "balanced_public_rate_schools": len(balanced_public_rate_ids),
        "balanced_base_rate_schools": len(balanced_base_rate_ids),
        "balanced_private_schools": len(private_balanced_ids),
        "tj_2024_count": tj_count[2024],
        "tj_2025_count": tj_count[2025],
        "tj_2026_count": tj_count[2026],
        "tj_2024_rate": tj_rate[2024],
        "tj_2025_rate": tj_rate[2025],
        "tj_2026_rate": tj_rate[2026],
        "base_2024_rate": base_rate[2024],
        "base_2025_rate": base_rate[2025],
        "base_2026_rate": base_rate[2026],
        "public_2024_rate": pub_rate[2024],
        "public_2025_rate": pub_rate[2025],
        "public_2026_rate": pub_rate[2026],
    }
    pd.DataFrame([validation]).to_csv(
        REPORTS / "tables" / "task9_validation_summary.csv", index=False, float_format="%.9f"
    )

    print("Task 9 outputs generated")
    for path in [REPORTS / "robustness.md", REPORTS / "limitations.md", REPORTS / "initial_findings.md"]:
        print(path.relative_to(ROOT))
    print(f"Balanced count schools: {len(balanced_count_ids)}")
    print(f"Balanced public rate schools: {len(balanced_public_rate_ids)}")


if __name__ == "__main__":
    main()
