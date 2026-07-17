#!/usr/bin/env python3
"""Build the README conclusion graphic from committed analytical tables."""

from __future__ import annotations

import csv
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "reports" / "tables"
OUTPUT = ROOT / "reports" / "conclusion_graphic.svg"
YEARS = (2023, 2024, 2025, 2026)


def read_rows(name: str) -> list[dict[str, str]]:
    with (TABLES / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def esc(value: object) -> str:
    return html.escape(str(value))


def text(x: float, y: float, value: object, *, size: int, weight: int = 400, fill: str = "#10213d") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter, Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(value)}</text>'
    )


def rounded_rect(x: float, y: float, width: float, height: float, *, fill: str, stroke: str) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" rx="18" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    )


def line_chart(
    *,
    x: float,
    y: float,
    width: float,
    height: float,
    title: str,
    subtitle: str,
    values: list[float],
    color: str,
    digits: int,
) -> str:
    left = x + 54
    right = x + width - 24
    top = y + 104
    bottom = y + height - 54
    lower = min(values)
    upper = max(values)
    padding = max((upper - lower) * 0.22, upper * 0.06, 0.03)
    ymin = max(0.0, lower - padding)
    ymax = upper + padding
    xs = [left + i * (right - left) / (len(values) - 1) for i in range(len(values))]
    ys = [bottom - (value - ymin) / (ymax - ymin) * (bottom - top) for value in values]
    points = " ".join(f"{px:.1f},{py:.1f}" for px, py in zip(xs, ys, strict=True))

    parts = [rounded_rect(x, y, width, height, fill="#ffffff", stroke="#c9d7ea")]
    parts.append(text(x + 26, y + 38, title, size=25, weight=750))
    parts.append(text(x + 26, y + 69, subtitle, size=16, fill="#52627b"))
    parts.append(
        f'<line x1="{left:.1f}" y1="{bottom:.1f}" x2="{right:.1f}" y2="{bottom:.1f}" '
        'stroke="#d8e1ee" stroke-width="2"/>'
    )
    parts.append(
        f'<line x1="{left:.1f}" y1="{top:.1f}" x2="{left:.1f}" y2="{bottom:.1f}" '
        'stroke="#d8e1ee" stroke-width="2"/>'
    )
    for fraction in (0.0, 0.5, 1.0):
        gy = bottom - fraction * (bottom - top)
        label = ymin + fraction * (ymax - ymin)
        parts.append(
            f'<line x1="{left:.1f}" y1="{gy:.1f}" x2="{right:.1f}" y2="{gy:.1f}" '
            'stroke="#edf2f8" stroke-width="1"/>'
        )
        parts.append(text(left - 47, gy + 6, f"{label:.{digits}f}", size=13, fill="#6b7890"))
    parts.append(
        f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="5" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
    )
    for year, value, px, py in zip(YEARS, values, xs, ys, strict=True):
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="{color}"/>')
        parts.append(text(px - 19, bottom + 30, year, size=14, fill="#52627b"))
        parts.append(text(px - 20, py - 14, f"{value:.{digits}f}", size=15, weight=700, fill=color))
    return "\n".join(parts)


def main() -> int:
    rate_rows = read_rows("analysis_balanced_rate_panel.csv")
    rates: dict[str, dict[int, dict[str, float]]] = {}
    for row in rate_rows:
        rates.setdefault(row["group"], {})[int(row["class_year"])] = {
            "count": float(row["nmsf_count"]),
            "enrollment": float(row["grade11_enrollment"]),
            "rate": float(row["nmsf_per_100_grade11"]),
            "schools": float(row["school_count"]),
        }

    public_group = rates["Balanced public including TJHSST"]
    base_group = rates["Balanced base public including program"]
    tj_group = rates["TJHSST"]

    def pooled(group: dict[int, dict[str, float]], years: tuple[int, int]) -> float:
        count = sum(group[year]["count"] for year in years)
        enrollment = sum(group[year]["enrollment"] for year in years)
        return 100 * count / enrollment

    tj_pre = pooled(tj_group, (2023, 2024))
    tj_post = pooled(tj_group, (2025, 2026))
    base_pre = pooled(base_group, (2023, 2024))
    base_post = pooled(base_group, (2025, 2026))

    standardized = {
        row["scenario"]: row for row in read_rows("analysis_rate_standardized_offset_decomposition.csv")
    }["common_2023_2024_baseline"]
    standardized_offset = float(standardized["base_excess_as_pct_of_tjhsst_shortfall"])
    public_shortfall = float(standardized["balanced_public_shortfall_vs_component_baseline"])

    count_rows = read_rows("analysis_balanced_count_panel.csv")
    private_rows = [row for row in count_rows if row["group"] == "Balanced private schools"]
    private_by_year = {int(row["class_year"]): float(row["nmsf_count"]) for row in private_rows}
    private_pre = sum(private_by_year[year] for year in (2023, 2024))
    private_post = sum(private_by_year[year] for year in (2025, 2026))

    state_rows = read_rows("analysis_state_normalization_supplemental.csv")
    public_state = {
        int(row["class_year"]): row
        for row in state_rows
        if row["group"] == "Balanced public including TJHSST"
    }
    public_location_2024 = float(public_state[2024]["group_share_of_virginia_location_total_pct"])
    public_location_2026 = float(public_state[2026]["group_share_of_virginia_location_total_pct"])

    public_schools = int(public_group[2026]["schools"])
    base_schools = int(base_group[2026]["schools"])
    conventional_schools = base_schools - 1

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000">',
        '<rect width="1600" height="1000" fill="#f4f7fb"/>',
        '<rect x="0" y="0" width="1600" height="112" fill="#102a56"/>',
        text(48, 56, "What changed in the TJHSST-area NMSF right tail?", size=36, weight=800, fill="#ffffff"),
        text(
            49,
            89,
            f"Classes 2023–2026 · fixed {public_schools}-school public rate panel · descriptive, not causal",
            size=18,
            fill="#cfe0fb",
        ),
    ]

    cards = [
        (
            38,
            "TJHSST pooled rate",
            f"{tj_pre:.1f} → {tj_post:.1f}",
            f"{100 * (tj_post / tj_pre - 1):+.1f}% · NMSFs per 100 juniors",
            "#1c5bb6",
        ),
        (
            424,
            f"Base public · {base_schools} schools",
            f"{base_pre:.3f} → {base_post:.3f}",
            f"{100 * (base_post / base_pre - 1):+.1f}% · includes H-B Woodlawn",
            "#128354",
        ),
        (
            810,
            "Enrollment-standardized offset",
            f"{standardized_offset:.1f}%",
            f"{public_shortfall:.1f} pooled public NMSFs still below baseline",
            "#a4570a",
        ),
        (
            1196,
            "Private count reference",
            f"{private_pre:.0f} → {private_post:.0f}",
            "Counts only · no comparable balanced rate panel",
            "#7a3db3",
        ),
    ]
    for x, label, value, note, color in cards:
        parts.append(rounded_rect(x, 136, 366, 148, fill="#ffffff", stroke="#c9d7ea"))
        parts.append(text(x + 24, 171, label, size=17, weight=700, fill="#52627b"))
        parts.append(text(x + 24, 225, value, size=35, weight=800, fill=color))
        parts.append(text(x + 24, 257, note, size=15, fill="#52627b"))

    parts.append(
        line_chart(
            x=38,
            y=310,
            width=492,
            height=382,
            title="TJHSST",
            subtitle="NMSFs per 100 Grade 11 students",
            values=[tj_group[year]["rate"] for year in YEARS],
            color="#1c5bb6",
            digits=1,
        )
    )
    parts.append(
        line_chart(
            x=554,
            y=310,
            width=492,
            height=382,
            title=f"Base public · {conventional_schools} conventional + H-B",
            subtitle="NMSFs per 100 Grade 11 students",
            values=[base_group[year]["rate"] for year in YEARS],
            color="#128354",
            digits=2,
        )
    )
    parts.append(
        line_chart(
            x=1070,
            y=310,
            width=492,
            height=382,
            title=f"Combined public · {public_schools} schools",
            subtitle="TJHSST + balanced base-public panel",
            values=[public_group[year]["rate"] for year in YEARS],
            color="#a4570a",
            digits=2,
        )
    )

    parts.extend(
        [
            rounded_rect(38, 720, 994, 226, fill="#102a56", stroke="#102a56"),
            text(72, 766, "Best-supported reading", size=23, weight=800, fill="#8fc2ff"),
            text(
                72,
                812,
                "Exceptional PSAT outcomes became much less concentrated at TJHSST.",
                size=25,
                weight=750,
                fill="#ffffff",
            ),
            text(
                72,
                852,
                "Base-school gains were delayed and only partially offset the pooled",
                size=21,
                fill="#e5eefb",
            ),
            text(
                72,
                884,
                "enrollment-standardized TJHSST shortfall. The data do not establish causation.",
                size=21,
                fill="#e5eefb",
            ),
            text(
                72,
                922,
                "Class 2025 remains the trough; Class 2026 largely recovers locally, "
                "not fully in pooled context.",
                size=16,
                fill="#bcd2f1",
            ),
            rounded_rect(1056, 720, 506, 226, fill="#ffffff", stroke="#c9d7ea"),
            text(1086, 764, "Virginia scope check", size=22, weight=800, fill="#102a56"),
            text(
                1086,
                806,
                f"Public share of location list: {public_location_2024:.1f}% (2024) → "
                f"{public_location_2026:.1f}% (2026)",
                size=17,
                weight=700,
                fill="#1c5bb6",
            ),
            text(1086, 846, "Location totals: 470 / 494", size=17, fill="#52627b"),
            text(1086, 878, "Official state-unit totals: 467 / 489", size=17, fill="#52627b"),
            text(1086, 910, "Class 2024 state-unit share withheld: 2 students", size=16, fill="#a4570a"),
            text(
                1086,
                934,
                "remain scope-unresolved; Class 2025 has no primary total.",
                size=16,
                fill="#a4570a",
            ),
        ]
    )
    parts.append("</svg>")
    OUTPUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(OUTPUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
