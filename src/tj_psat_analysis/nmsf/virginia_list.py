"""Parse NMSC Virginia semifinalist list PDFs into count-only records."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from tj_psat_analysis.normalize import normalize_school_name

SNAPSHOT_FIELDNAMES = (
    "source_id",
    "class_year",
    "city",
    "school_name_source",
    "matched_school_id",
    "matched_school",
    "nmsf_count",
    "snapshot_record_type",
    "snapshot_notes",
)

STATEWIDE_TOTAL_FIELDNAMES = (
    "class_year",
    "statewide_nmsf_semifinalist_total",
    "statewide_nmsf_semifinalist_total_status",
    "source_id",
    "source_title",
    "source_url",
    "source_date",
    "source_hash",
)

SCHOOLISH_RE = re.compile(
    r"(\bH\.?\s*S\.?\b|HIGH|SCHOOL|SCHOOLS|ACADEMY|PROGRAM|SECONDARY|COLLEGIATE|"
    r"BASIS|INDEPENDENT|HOMESCHOOL|CATHOLIC|CHRISTIAN|SEMINARY|INSTITUTE)"
)

EXTRA_NMSC_ALIASES = {
    "W T WOODSON HIGH": "woodson_high_school",
    "JAMES W ROBINSON SECONDARY": "robinson_secondary_school_hs",
    "LAKE BRADDOCK SECONDARY": "lake_braddock_secondary_school_hs",
    "THOMAS A EDISON HIGH": "edison_high_school",
    "MCLEAN HIGH": "mclean_high_school",
    "BASIS INDEPENDENT": "basis_independent_mclean",
    "CHARLES J COLGAN SENIOR HIGH": "charles_j_colgan_sr_high_school",
    "C D HYLTON HIGH": "c_d_hylton_high_school",
    "HB WOODLAWN PROGRAM": "h_b_woodlawn_secondary_program",
    "THE H B WOODLAWN PROGRAM": "h_b_woodlawn_secondary_program",
    "WASHINGTON LIBERTY HIGH": "washington_liberty_high_school",
    "JOHN R LEWIS HIGH": "lewis_high_school",
    "ROBERT E LEE HIGH": "lewis_high_school",
    "ST PAUL VI CATHOLIC HIGH": "st_paul_vi_catholic_high_school",
    "ST JOHN PAUL THE GREAT CATHOLIC HIGH": "st_john_paul_the_great_catholic_high_school",
}


@dataclass(frozen=True)
class VirginiaListCount:
    city: str
    school_name_source: str
    matched_school_id: str
    matched_school: str
    nmsf_count: int


def parse_virginia_list_text(
    *,
    lines: Iterable[str],
    class_year: int,
    school_roster_rows: Sequence[Mapping[str, str]],
    school_alias_rows: Sequence[Mapping[str, str]],
) -> tuple[list[VirginiaListCount], int]:
    """Parse extracted NMSC Virginia-list lines into count-only school totals."""

    matcher = VirginiaListMatcher(school_roster_rows, school_alias_rows)
    started = False
    current_city = ""
    current_school = ""
    current_school_id = ""
    current_school_name = ""
    heading_buffer: list[str] = []
    raw_counts: Counter[tuple[str, str, str, str]] = Counter()

    def flush_heading_buffer() -> None:
        nonlocal current_city, current_school, current_school_id, current_school_name, heading_buffer
        cleaned = [
            line
            for line in heading_buffer
            if not (
                line.startswith("Semifinalists:")
                or line in {"Merit Scholarship Program", "Virginia (continued)", "VIRGINIA"}
                or re.fullmatch(r"\d+", line)
            )
        ]
        heading_buffer = []
        if not cleaned:
            return

        resolved = matcher.resolve_heading(cleaned, current_city)
        if resolved is not None:
            city, school, school_id, school_name = resolved
            if city:
                current_city = city
            current_school = school
            current_school_id = school_id
            current_school_name = school_name
            return

        city, school = _fallback_city_school(cleaned, current_city)
        current_city = city
        current_school = school
        current_school_id = ""
        current_school_name = ""

    for raw_line in lines:
        line = _clean_line(raw_line)
        if not line:
            continue
        if _is_report_header(line):
            continue
        if not started:
            if line == "VIRGINIA":
                started = True
            continue

        if _is_student_line(line, class_year):
            flush_heading_buffer()
            key = (current_city, current_school, current_school_id, current_school_name)
            raw_counts[key] += 1
        else:
            heading_buffer.append(line)

    rows = [
        VirginiaListCount(
            city=city,
            school_name_source=school,
            matched_school_id=school_id,
            matched_school=school_name,
            nmsf_count=count,
        )
        for (city, school, school_id, school_name), count in raw_counts.items()
    ]
    rows.sort(key=lambda row: (_normalize_nmsc_name(row.city), _normalize_nmsc_name(row.school_name_source)))
    return rows, sum(row.nmsf_count for row in rows)


def read_pdf_lines(path: Path) -> list[str]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - dependency guard for manual ingest use.
        raise RuntimeError("pypdf is required to parse NMSC Virginia list PDFs") from exc

    reader = PdfReader(str(path))
    lines: list[str] = []
    for index, page in enumerate(reader.pages):
        if index < 2:
            continue
        text = page.extract_text() or ""
        lines.extend(text.splitlines())
    return lines


def snapshot_rows(
    *,
    source_id: str,
    class_year: int,
    counts: Sequence[VirginiaListCount],
) -> list[dict[str, str]]:
    return [
        {
            "source_id": source_id,
            "class_year": str(class_year),
            "city": count.city,
            "school_name_source": count.school_name_source,
            "matched_school_id": count.matched_school_id,
            "matched_school": count.matched_school,
            "nmsf_count": str(count.nmsf_count),
            "snapshot_record_type": "observation_count" if count.matched_school_id else "out_of_roster_count",
            "snapshot_notes": (
                "matched to canonical roster; student names omitted"
                if count.matched_school_id
                else "outside canonical roster or unmatched; student names omitted"
            ),
        }
        for count in counts
    ]


def statewide_total_row(
    *,
    class_year: int,
    total: int,
    source_id: str,
    source_title: str,
    source_url: str,
    source_date: str,
    source_hash: str,
) -> dict[str, str]:
    return {
        "class_year": str(class_year),
        "statewide_nmsf_semifinalist_total": str(total),
        "statewide_nmsf_semifinalist_total_status": "source_backed_total",
        "source_id": source_id,
        "source_title": source_title,
        "source_url": source_url,
        "source_date": source_date,
        "source_hash": source_hash,
    }


def write_snapshot_csv(path: Path, rows: Sequence[Mapping[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SNAPSHOT_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_statewide_totals_csv(path: Path, rows: Sequence[Mapping[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=STATEWIDE_TOTAL_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class VirginiaListMatcher:
    def __init__(
        self,
        school_roster_rows: Sequence[Mapping[str, str]],
        school_alias_rows: Sequence[Mapping[str, str]],
    ) -> None:
        self.school_by_id = {row["school_id"]: row["school"] for row in school_roster_rows}
        alias_to_ids: dict[str, set[str]] = defaultdict(set)
        for row in school_alias_rows:
            if row.get("join_allowed", "").lower() != "true":
                continue
            alias_to_ids[_normalize_nmsc_name(row["alias"])].add(row["school_id"])
        for alias, school_id in EXTRA_NMSC_ALIASES.items():
            alias_to_ids[alias].add(school_id)
        self.alias_to_ids = alias_to_ids

    def resolve_heading(
        self,
        heading_lines: Sequence[str],
        current_city: str,
    ) -> tuple[str, str, str, str] | None:
        best: tuple[tuple[int, int, int], str, str, str] | None = None
        for index in range(len(heading_lines)):
            candidate = " ".join(heading_lines[index:])
            city = " ".join(heading_lines[:index]) if index > 0 else current_city
            school_id = self.match_school(candidate, city)
            if not school_id:
                continue
            score = (len(candidate), -index, 1)
            if best is None or score > best[0]:
                best = (score, city, candidate, school_id)
        if best is None:
            return None
        _, city, school, school_id = best
        return city, school, school_id, self.school_by_id[school_id]

    def match_school(self, raw_school: str, city: str) -> str:
        normalized = _normalize_nmsc_name(raw_school)
        city_normalized = _normalize_nmsc_name(city)

        if normalized == "FREEDOM HIGH":
            if city_normalized == "SOUTH RIDING":
                return "freedom_high_school_south_riding"
            if city_normalized == "WOODBRIDGE":
                return "freedom_high_school_woodbridge"
            return ""
        if normalized == "HERITAGE HIGH":
            if city_normalized == "LEESBURG":
                return "heritage_high_school_leesburg"
            return ""
        if normalized == "BASIS INDEPENDENT":
            if city_normalized == "MCLEAN":
                return "basis_independent_mclean"
            return ""

        exact = self.alias_to_ids.get(normalized, set())
        if len(exact) == 1:
            return next(iter(exact))

        suffix_matches: list[tuple[int, str]] = []
        for alias, school_ids in self.alias_to_ids.items():
            if len(school_ids) != 1:
                continue
            if normalized == alias or normalized.endswith(f" {alias}"):
                suffix_matches.append((len(alias), next(iter(school_ids))))
        if not suffix_matches:
            return ""
        suffix_matches.sort(reverse=True)
        longest = suffix_matches[0][0]
        matches = {school_id for length, school_id in suffix_matches if length == longest}
        if len(matches) == 1:
            return next(iter(matches))
        return ""


def _clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def _is_report_header(line: str) -> bool:
    return (
        line.startswith("Semifinalists:")
        or line in {"Merit Scholarship Program", "Virginia (continued)"}
        or re.fullmatch(r"\d+", line) is not None
    )


def _is_student_line(line: str, class_year: int) -> bool:
    if class_year in {2023, 2024}:
        return re.match(r"^\d{3}\s+", line) is not None
    return "," in line and not line.isupper()


def _fallback_city_school(heading_lines: Sequence[str], current_city: str) -> tuple[str, str]:
    city = current_city
    school_start = 0
    if (
        len(heading_lines) > 1
        and not SCHOOLISH_RE.search(heading_lines[0])
        and SCHOOLISH_RE.search(" ".join(heading_lines[1:]))
        and not heading_lines[0].startswith(("ST.", "THE "))
        and not heading_lines[0].endswith(("VALLEY", "COUNTY"))
    ):
        city = heading_lines[0]
        school_start = 1
    return city, " ".join(heading_lines[school_start:])


def _normalize_nmsc_name(value: str) -> str:
    cleaned = value.upper().replace("&", " AND ")
    cleaned = re.sub(r"\bMC\s+LEAN\b", "MCLEAN", cleaned)
    cleaned = re.sub(r"\bH\s*\.\s*S\s*\.?\b", "HIGH", cleaned)
    cleaned = re.sub(r"\bH\.S\.\b", "HIGH", cleaned)
    cleaned = re.sub(r"\bSR\b\.?", "SENIOR", cleaned)
    return normalize_school_name(cleaned)
