"""Build the canonical school roster, aliases, and history deliverables."""

from __future__ import annotations

import csv
import zipfile
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

from .constants import (
    CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR,
    FIRST_OPERATING_CLASS_YEAR_BY_SCHOOL_ID,
)
from .normalize import normalize_school_name
from .seed_workbook import SchoolRecord, read_roster, sha256_file, write_csv, write_text

PRIVATE_UNALLOCATED_PATHWAY = "Private/homeschool unallocated"

ALLOWED_TJ_PATHWAYS = {
    "Arlington",
    "Falls Church City",
    "Loudoun",
    "Prince William",
    "FCPS Region 1",
    "FCPS Region 2",
    "FCPS Region 3",
    "FCPS Region 4",
    "FCPS Region 5",
    "TJHSST",
    PRIVATE_UNALLOCATED_PATHWAY,
}

PATHWAY_RENAMES = {
    "Falls Church": "Falls Church City",
}

PUBLIC_LEA_NAME_BY_DIVISION = {
    "APS": "Arlington County Public Schools",
    "Falls Church City": "Falls Church City Public Schools",
    "LCPS": "Loudoun County Public Schools",
    "PWCS": "Prince William County Public Schools",
    "FCPS": "Fairfax County Public Schools",
}

CCD_DIRECTORY_SOURCE_TITLE = (
    "NCES CCD 2023-24 Public Elementary/Secondary School Universe Survey Directory, v.1a"
)
CCD_DIRECTORY_SOURCE_URL = "https://nces.ed.gov/ccd/Data/zip/ccd_sch_029_2324_w_1a_073124.zip"
CCD_DIRECTORY_RETRIEVAL_DATE = "2026-06-18"

ADMISSIONS_POLICY_RELATIVE_PATH = "docs/source_notes/FCPS Regulation 3355.16 TJHSST Admissions.pdf"
ADMISSIONS_POLICY_SOURCE_TITLE = "FCPS Regulation 3355.16 TJHSST Admissions"
ADMISSIONS_POLICY_SOURCE_DATE = "2022-05-17"

ARLINGTON_TECH_DECISION = (
    "Arlington Tech is not treated as a separate analytical unit for this roster. "
    "The seed workbook does not include it as an independent school row, and APS/NCES "
    "directory treatment does not provide a grade-11 denominator comparable to the "
    "base high-school rows. Add it later only if a source reports NMSF counts and "
    "enrollment as a separate high-school unit."
)

EXTRA_ALIASES_BY_SCHOOL_ID: dict[str, tuple[tuple[str, str, str], ...]] = {
    "h_b_woodlawn_secondary_program": (
        ("HB Woodlawn Secondary Program", "nces_name_variant", "Matches CCD directory spelling."),
        ("HB Woodlawn Secondary", "short_name", "Variant without hyphen."),
        ("H-B Woodlawn", "short_name", "Common program shorthand."),
        ("HB Woodlawn", "short_name", "Common program shorthand without hyphen."),
    ),
    "washington_liberty_high_school": (
        ("Washington-Lee High School", "historical_name", "Prior name through the 2018-19 school year."),
        ("Washington-Lee High", "historical_short_name", "Prior short name."),
    ),
    "lewis_high_school": (
        ("John R. Lewis High School", "formal_name", "Formal current name used by FCPS."),
        ("John R. Lewis High", "formal_short_name", "Formal current short name."),
    ),
    "thomas_jefferson_high_school_for_science_and_technology": (
        ("TJHSST", "abbreviation", "Common abbreviation."),
        ("Thomas Jefferson HSST", "abbreviation", "Common list abbreviation."),
        ("Thomas Jefferson High School", "short_name", "Common shortened form; keep TJHSST row intact."),
    ),
    "freedom_high_school_south_riding": (
        ("Freedom High School (Loudoun)", "district_qualified", "Disambiguates the LCPS school."),
        ("Freedom High School South Riding", "location_qualified", "Disambiguates the LCPS school."),
        ("Freedom High School - South Riding", "location_qualified", "Disambiguates the LCPS school."),
        ("Freedom High School, South Riding", "location_qualified", "Disambiguates the LCPS school."),
        ("Freedom High School LCPS", "district_qualified", "Disambiguates the LCPS school."),
    ),
    "freedom_high_school_woodbridge": (
        ("Freedom High School (Prince William)", "district_qualified", "Disambiguates the PWCS school."),
        ("Freedom High School Woodbridge", "location_qualified", "Disambiguates the PWCS school."),
        ("Freedom High School - Woodbridge", "location_qualified", "Disambiguates the PWCS school."),
        ("Freedom High School, Woodbridge", "location_qualified", "Disambiguates the PWCS school."),
        ("Freedom High School PWCS", "district_qualified", "Disambiguates the PWCS school."),
    ),
}

# Source-specific spellings discovered after the original roster build.  Keep
# these in code rather than hand-editing the generated alias CSV so a clean
# pipeline rebuild preserves the same matching surface.
SOURCE_ALIASES_BY_SCHOOL_ID: dict[str, tuple[tuple[str, str, str], ...]] = {
    "h_b_woodlawn_secondary_program": (
        ("H.B. Woodlawn Program", "source_name_variant", "Patch Arlington articles use this program name."),
        (
            "The H. B. Woodlawn Program",
            "source_name_variant",
            "Patch Arlington 2026 uses this program name.",
        ),
    ),
    "immanuel_christian_high_school": (
        (
            "Immanuel Christian School",
            "source_name_variant",
            "Patch Vienna 2025 omits High from the school name.",
        ),
    ),
    "ideaventions_academy_for_mathematics_science": (
        (
            "Ideaventions Academy of Math and Science",
            "source_name_variant",
            "Patch Vienna 2025 uses this wording.",
        ),
    ),
}

HISTORY_EVENTS: tuple[dict[str, object], ...] = (
    {
        "school_id": "washington_liberty_high_school",
        "event_type": "rename",
        "event_school_year": "2019-20",
        "first_affected_class_year": 2021,
        "prior_name": "Washington-Lee High School",
        "current_name": "Washington-Liberty High School",
        "source_title": "TASKS.md Milestone 2 school-history requirement",
        "source_url": "TASKS.md",
        "source_date": "",
        "source_note": "Task plan requires preserving the Washington-Lee to Washington-Liberty rename.",
    },
    {
        "school_id": "meridian_high_school",
        "event_type": "rename",
        "event_school_year": "2021-22",
        "first_affected_class_year": 2023,
        "prior_name": "George Mason High School",
        "current_name": "Meridian High School",
        "source_title": "Seed workbook raw roster note",
        "source_url": "docs/source_notes/tj psat investigation.xlsx",
        "source_date": "",
        "source_note": "Seed note: Renamed from George Mason HS in 2021.",
    },
    {
        "school_id": "lewis_high_school",
        "event_type": "rename",
        "event_school_year": "2020-21",
        "first_affected_class_year": 2022,
        "prior_name": "Robert E. Lee High School",
        "current_name": "John R. Lewis High School",
        "source_title": "Seed workbook raw roster note",
        "source_url": "docs/source_notes/tj psat investigation.xlsx",
        "source_date": "",
        "source_note": "Seed note: Renamed from Robert E. Lee HS (2020-21).",
    },
    {
        "school_id": "unity_reed_high_school",
        "event_type": "rename",
        "event_school_year": "2020-21",
        "first_affected_class_year": 2022,
        "prior_name": "Stonewall Jackson High School",
        "current_name": "Unity Reed High School",
        "source_title": "Seed workbook raw roster note",
        "source_url": "docs/source_notes/tj psat investigation.xlsx",
        "source_date": "",
        "source_note": "Seed note: Renamed from Stonewall Jackson HS (2020).",
    },
    {
        "school_id": "independence_high_school",
        "event_type": "opening",
        "event_school_year": "2019-20",
        "first_affected_class_year": 2021,
        "prior_name": "",
        "current_name": "Independence High School",
        "source_title": "Seed workbook raw roster note",
        "source_url": "docs/source_notes/tj psat investigation.xlsx",
        "source_date": "",
        "source_note": "Seed note: Opened 2019-20.",
    },
    {
        "school_id": "lightridge_high_school",
        "event_type": "opening",
        "event_school_year": "2020-21",
        "first_affected_class_year": 2022,
        "prior_name": "",
        "current_name": "Lightridge High School",
        "source_title": "Seed workbook raw roster note",
        "source_url": "docs/source_notes/tj psat investigation.xlsx",
        "source_date": "",
        "source_note": "Seed note: Opened 2020-21.",
    },
    {
        "school_id": "gainesville_high_school",
        "event_type": "opening",
        "event_school_year": "2021-22",
        "first_affected_class_year": 2023,
        "prior_name": "",
        "current_name": "Gainesville High School",
        "source_title": "Seed workbook raw roster note",
        "source_url": "docs/source_notes/tj psat investigation.xlsx",
        "source_date": "",
        "source_note": "Seed note: Opened 2021-22.",
    },
    {
        "school_id": "st_paul_vi_catholic_high_school",
        "event_type": "relocation",
        "event_school_year": "2020-21",
        "first_affected_class_year": 2022,
        "prior_name": "Fairfax City campus",
        "current_name": "Loudoun campus",
        "source_title": "Seed workbook raw roster note",
        "source_url": "docs/source_notes/tj psat investigation.xlsx",
        "source_date": "",
        "source_note": "Seed note: Campus moved from Fairfax City to Loudoun in 2020.",
    },
)


def _school_year_for_class_year(class_year: int) -> str:
    return CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR[class_year]


def _class_year_for_school_year(school_year: str) -> int:
    for class_year, grade11_school_year in CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR.items():
        if grade11_school_year == school_year:
            return class_year
    raise ValueError(f"No class-year mapping for school year {school_year!r}")


def _standard_tj_pathway(record: SchoolRecord) -> str:
    if record.sector == "Private":
        return PRIVATE_UNALLOCATED_PATHWAY
    return PATHWAY_RENAMES.get(record.pathway, record.pathway)


def _pathway_status(record: SchoolRecord) -> str:
    if record.sector == "Private":
        return "unallocated_private_applicant"
    pathway = _standard_tj_pathway(record)
    if pathway in ALLOWED_TJ_PATHWAYS:
        return "assigned"
    return "invalid_pathway"


def _pathway_assignment_method(record: SchoolRecord) -> str:
    if record.sector == "Private":
        return "nonpublic_unallocated_seats"
    if record.pathway.startswith("FCPS Region"):
        return "base_school_region"
    if record.school_id == "thomas_jefferson_high_school_for_science_and_technology":
        return "single_tjhsst_row"
    return "participating_jurisdiction"


def _pathway_source_note(record: SchoolRecord) -> str:
    if record.sector == "Private":
        return (
            "Regulation 3355.16 requires private-school applicants to prove residency "
            "in a cooperating division and places non-public applicants in the "
            "unallocated-seat pool; do not assign private schools by school location."
        )
    if record.pathway.startswith("FCPS Region"):
        return (
            "Regulation 3355.16 allocates seats by each public school's 8th-grade "
            "population; the seed workbook supplies FCPS high-school-region analytical rows."
        )
    if record.school_id == "thomas_jefferson_high_school_for_science_and_technology":
        return "TJHSST remains one canonical school row per project data rules."
    return (
        "Regulation 3355.16 defines annual cooperating-division participation; the seed "
        "workbook supplies high-school-to-jurisdiction analytical rows."
    )


def _analytical_unit_type(record: SchoolRecord) -> str:
    if record.sector == "Private":
        return "private_school"
    if record.school_id == "thomas_jefferson_high_school_for_science_and_technology":
        return "public_governor_school"
    if "Secondary Program" in record.school:
        return "public_secondary_program"
    return "public_high_school"


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _nces_lookup(nces_rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {row["school_id"]: row for row in nces_rows if row.get("school_id")}


def _alias_candidates(record: SchoolRecord) -> Iterable[tuple[str, str, str, str]]:
    for alias in record.aliases:
        alias_type = "seed_alias"
        if alias == record.school:
            alias_type = "canonical_name"
        elif "High School" not in alias and "Secondary" not in alias:
            alias_type = "short_name"
        yield alias, alias_type, "seed_workbook_raw", record.notes

    for alias, alias_type, note in EXTRA_ALIASES_BY_SCHOOL_ID.get(record.school_id, ()):
        yield alias, alias_type, "task2_manual_alias_rule", note

    for alias, alias_type, note in SOURCE_ALIASES_BY_SCHOOL_ID.get(record.school_id, ()):
        yield alias, alias_type, "task5_patch_local_media", note


def build_alias_rows(roster: Sequence[SchoolRecord]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for record in roster:
        for alias, alias_type, source, note in _alias_candidates(record):
            normalized = normalize_school_name(alias)
            key = (record.school_id, normalized)
            if not normalized or key in seen:
                continue
            seen.add(key)
            rows.append(
                {
                    "school_id": record.school_id,
                    "school": record.school,
                    "alias": alias,
                    "normalized_alias": normalized,
                    "alias_type": alias_type,
                    "join_allowed": "",
                    "conflict_school_ids": "",
                    "source": source,
                    "notes": note,
                }
            )

    grouped: dict[str, set[str]] = {}
    for row in rows:
        grouped.setdefault(str(row["normalized_alias"]), set()).add(str(row["school_id"]))
    for row in rows:
        school_ids = sorted(grouped[str(row["normalized_alias"])])
        row["join_allowed"] = "true" if len(school_ids) == 1 else "false"
        row["conflict_school_ids"] = "|".join(school_ids) if len(school_ids) > 1 else ""
    return rows


def read_public_nces_id_rows(path: Path) -> list[dict[str, str]]:
    rows = _read_csv(path)
    required = {
        "school_id",
        "nces_school_id",
        "nces_lea_id",
        "nces_school_name",
        "nces_lea_name",
        "source_file_sha256",
    }
    for row_number, row in enumerate(rows, start=2):
        missing = [field for field in required if not (row.get(field) or "").strip()]
        if missing:
            raise ValueError(f"{path} row {row_number} missing {', '.join(missing)}")
    return rows


def _ccd_rows(ccd_directory_zip: Path) -> list[dict[str, str]]:
    with zipfile.ZipFile(ccd_directory_zip) as archive:
        csv_names = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if len(csv_names) != 1:
            raise ValueError(f"Expected exactly one CSV in {ccd_directory_zip}, found {csv_names}")
        with archive.open(csv_names[0]) as handle:
            text_rows = (line.decode("utf-8-sig", errors="replace") for line in handle)
            return list(csv.DictReader(text_rows))


def extract_public_nces_id_rows(
    roster: Sequence[SchoolRecord],
    ccd_directory_zip: Path,
) -> list[dict[str, object]]:
    ccd_hash = sha256_file(ccd_directory_zip)
    ccd_index: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in _ccd_rows(ccd_directory_zip):
        if row.get("LSTATE") != "VA":
            continue
        key = (row.get("LEA_NAME", ""), normalize_school_name(row.get("SCH_NAME", "")))
        ccd_index.setdefault(key, []).append(row)

    output: list[dict[str, object]] = []
    for record in roster:
        if record.sector != "Public":
            continue
        lea_name = PUBLIC_LEA_NAME_BY_DIVISION.get(record.division, "")
        matches: list[dict[str, str]] = []
        for alias, _, _, _ in _alias_candidates(record):
            key = (lea_name, normalize_school_name(alias))
            for candidate in ccd_index.get(key, []):
                if candidate not in matches:
                    matches.append(candidate)

        if len(matches) != 1:
            details = "; ".join(
                f"{candidate.get('SCH_NAME')} ({candidate.get('NCESSCH')})" for candidate in matches
            )
            raise ValueError(
                f"Expected one NCES match for {record.school} in {lea_name}, "
                f"found {len(matches)}: {details or '(none)'}"
            )

        match = matches[0]
        output.append(
            {
                "school_id": record.school_id,
                "school": record.school,
                "nces_school_id": match["NCESSCH"],
                "nces_lea_id": match["LEAID"],
                "nces_school_name": match["SCH_NAME"],
                "nces_lea_name": match["LEA_NAME"],
                "nces_city": match.get("LCITY", ""),
                "nces_zip": match.get("LZIP", ""),
                "nces_grade_low": match.get("GSLO", ""),
                "nces_grade_high": match.get("GSHI", ""),
                "nces_level": match.get("LEVEL", ""),
                "nces_school_type": match.get("SCH_TYPE_TEXT", ""),
                "nces_operational_status": match.get("SY_STATUS_TEXT", ""),
                "source_title": CCD_DIRECTORY_SOURCE_TITLE,
                "source_url": CCD_DIRECTORY_SOURCE_URL,
                "source_retrieval_date": CCD_DIRECTORY_RETRIEVAL_DATE,
                "source_file_sha256": ccd_hash,
            }
        )
    return output


def build_school_roster_rows(
    roster: Sequence[SchoolRecord],
    nces_rows: Sequence[Mapping[str, str]],
    admissions_policy_pdf_path: str,
    admissions_policy_pdf_hash: str,
) -> list[dict[str, object]]:
    nces_by_school_id = _nces_lookup(nces_rows)
    output: list[dict[str, object]] = []
    for record in roster:
        first_class_year = FIRST_OPERATING_CLASS_YEAR_BY_SCHOOL_ID.get(
            record.school_id,
            min(CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR),
        )
        nces = nces_by_school_id.get(record.school_id, {})
        if record.sector == "Public":
            identifier_status = "matched_2023_24_ccd" if nces else "public_nces_id_pending"
            district_name = nces.get(
                "nces_lea_name",
                PUBLIC_LEA_NAME_BY_DIVISION.get(record.division, ""),
            )
        else:
            identifier_status = "private_pss_id_not_ingested"
            district_name = ""
        output.append(
            {
                "school_id": record.school_id,
                "school": record.school,
                "tj_pathway": _standard_tj_pathway(record),
                "pathway_status": _pathway_status(record),
                "pathway_assignment_method": _pathway_assignment_method(record),
                "pathway_source_title": ADMISSIONS_POLICY_SOURCE_TITLE,
                "pathway_source_path": admissions_policy_pdf_path,
                "pathway_source_date": ADMISSIONS_POLICY_SOURCE_DATE,
                "pathway_source_hash": admissions_policy_pdf_hash,
                "pathway_source_note": _pathway_source_note(record),
                "division": record.division,
                "district_name": district_name,
                "sector": record.sector.lower(),
                "analytical_unit_type": _analytical_unit_type(record),
                "nces_school_id": nces.get("nces_school_id", ""),
                "nces_lea_id": nces.get("nces_lea_id", ""),
                "identifier_status": identifier_status,
                "first_operating_class_year": first_class_year,
                "first_operating_grade11_school_year": _school_year_for_class_year(first_class_year),
                "last_operating_class_year": "",
                "last_operating_grade11_school_year": "",
                "source_workbook": record.source_workbook,
                "source_sheet": record.source_sheet,
                "source_row": record.source_row,
                "notes": record.notes,
            }
        )
    return output


def build_school_history_rows(roster: Sequence[SchoolRecord]) -> list[dict[str, object]]:
    roster_by_id = {record.school_id: record for record in roster}
    rows: list[dict[str, object]] = []
    for event in HISTORY_EVENTS:
        school_id = str(event["school_id"])
        record = roster_by_id[school_id]
        first_class_year = int(str(event["first_affected_class_year"]))
        rows.append(
            {
                "school_id": school_id,
                "school": record.school,
                "event_type": event["event_type"],
                "event_school_year": event["event_school_year"],
                "first_affected_class_year": first_class_year,
                "first_affected_grade11_school_year": _school_year_for_class_year(first_class_year),
                "prior_name": event["prior_name"],
                "current_name": event["current_name"],
                "source_title": event["source_title"],
                "source_url": event["source_url"],
                "source_date": event["source_date"],
                "source_note": event["source_note"],
            }
        )
    return rows


def _markdown_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    rendered = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        rendered.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(rendered)


def _counter_rows(values: Iterable[str]) -> list[list[object]]:
    return [[key or "(blank)", value] for key, value in sorted(Counter(values).items())]


def build_roster_review_report(
    school_roster_rows: Sequence[Mapping[str, object]],
    alias_rows: Sequence[Mapping[str, object]],
    history_rows: Sequence[Mapping[str, object]],
    nces_rows: Sequence[Mapping[str, str]],
    admissions_policy_pdf_path: str,
    admissions_policy_pdf_hash: str,
) -> str:
    blocked_alias_rows = [row for row in alias_rows if row["join_allowed"] == "false"]
    invalid_pathway_rows = [row for row in school_roster_rows if row["pathway_status"] == "invalid_pathway"]
    public_rows = [row for row in school_roster_rows if row["sector"] == "public"]
    public_nces_matched = [row for row in public_rows if row["identifier_status"] == "matched_2023_24_ccd"]
    not_operating_rows: list[list[object]] = []
    for row in school_roster_rows:
        first_class_year = int(str(row["first_operating_class_year"]))
        for class_year in CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR:
            if class_year < first_class_year:
                not_operating_rows.append(
                    [
                        row["school"],
                        class_year,
                        _school_year_for_class_year(class_year),
                        "not_operating",
                    ]
                )

    lines = [
        "# Canonical Roster Review",
        "",
        "This report is generated by the Milestone 2 roster builder. It records",
        "deterministic joins and review queues rather than guessing through missing",
        "or ambiguous school metadata.",
        "",
        "## Output Summary",
        "",
        _markdown_table(
            ["Output", "Rows"],
            [
                ["data/processed/school_roster.csv", len(school_roster_rows)],
                ["data/manual/school_aliases.csv", len(alias_rows)],
                ["data/manual/school_history.csv", len(history_rows)],
                ["data/manual/public_school_nces_ids.csv", len(nces_rows)],
            ],
        ),
        "",
        "## Roster Coverage",
        "",
        _markdown_table(
            ["Sector", "Schools"],
            _counter_rows(str(row["sector"]) for row in school_roster_rows),
        ),
        "",
        _markdown_table(
            ["TJ pathway", "Schools"],
            _counter_rows(str(row["tj_pathway"]) for row in school_roster_rows),
        ),
        "",
        _markdown_table(
            ["Pathway assignment method", "Schools"],
            _counter_rows(str(row["pathway_assignment_method"]) for row in school_roster_rows),
        ),
        "",
        "## Admissions Pathway Source",
        "",
        _markdown_table(
            ["Field", "Value"],
            [
                ["Source title", ADMISSIONS_POLICY_SOURCE_TITLE],
                ["Source path", admissions_policy_pdf_path],
                ["Source date", ADMISSIONS_POLICY_SOURCE_DATE],
                ["Source SHA-256", admissions_policy_pdf_hash],
            ],
        ),
        "",
        "Regulation 3355.16 is the admissions-policy source used here. It describes",
        "ninth-grade eligibility and evaluation, allocates seats by public schools'",
        "8th-grade populations, leaves remaining seats unallocated, and places",
        "non-public applicants in the unallocated-seat pool. It also points to annual",
        "Notice 3355 materials for implementation details, so high-school NMSF",
        "observations by pathway remain analytical geography buckets, not observed",
        "TJHSST admissions-pathway counts.",
        "",
        "## Identifier Coverage",
        "",
        _markdown_table(
            ["Identifier status", "Schools"],
            _counter_rows(str(row["identifier_status"]) for row in school_roster_rows),
        ),
        "",
        f"Public NCES IDs matched: {len(public_nces_matched)} of {len(public_rows)}.",
        "",
        "Public NCES source: "
        f"{CCD_DIRECTORY_SOURCE_TITLE}; {CCD_DIRECTORY_SOURCE_URL}; "
        f"retrieved {CCD_DIRECTORY_RETRIEVAL_DATE}.",
        "",
        "## Alias Join Validation",
        "",
        f"Join-allowed aliases are unique by normalized alias. Blocked aliases: {len(blocked_alias_rows)}.",
    ]

    if blocked_alias_rows:
        lines.extend(
            [
                "",
                _markdown_table(
                    ["Alias", "Normalized alias", "Conflicting school IDs"],
                    [
                        [row["alias"], row["normalized_alias"], row["conflict_school_ids"]]
                        for row in blocked_alias_rows
                    ],
                ),
            ]
        )

    lines.extend(["", "## Pathway Review Queue", ""])
    if invalid_pathway_rows:
        lines.append(
            _markdown_table(
                ["School", "Current pathway", "Status"],
                [[row["school"], row["tj_pathway"], row["pathway_status"]] for row in invalid_pathway_rows],
            )
        )
    else:
        lines.append("No pathway review rows.")

    lines.extend(
        [
            "",
            "## Operational History",
            "",
            _markdown_table(
                ["Event type", "School", "Event school year", "Prior name", "Current name"],
                [
                    [
                        row["event_type"],
                        row["school"],
                        row["event_school_year"],
                        row["prior_name"] or "(none)",
                        row["current_name"] or "(none)",
                    ]
                    for row in history_rows
                ],
            ),
            "",
            "## Not-Operating Class-Years",
            "",
        ]
    )
    if not_operating_rows:
        lines.append(
            _markdown_table(
                ["School", "Class year", "Grade-11 school year", "Panel status"],
                not_operating_rows,
            )
        )
    else:
        lines.append("No not-operating class-years in the 2019-2026 panel.")

    lines.extend(
        [
            "",
            "## Arlington Tech Decision",
            "",
            ARLINGTON_TECH_DECISION,
            "",
        ]
    )
    return "\n".join(lines)


def build_school_roster_outputs(
    workbook_path: Path,
    processed_dir: Path,
    manual_dir: Path,
    report_dir: Path,
    nces_id_csv: Path,
    ccd_directory_zip: Path | None = None,
    admissions_policy_pdf: Path | None = None,
) -> dict[str, Path]:
    try:
        source_workbook_label = str(workbook_path.resolve().relative_to(Path.cwd()))
    except ValueError:
        source_workbook_label = str(workbook_path)
    roster = read_roster(workbook_path, source_workbook_label)
    admissions_policy_pdf = admissions_policy_pdf or Path(ADMISSIONS_POLICY_RELATIVE_PATH)
    if not admissions_policy_pdf.exists():
        raise ValueError(f"Admissions policy PDF not found: {admissions_policy_pdf}")
    admissions_policy_pdf_hash = sha256_file(admissions_policy_pdf)
    try:
        admissions_policy_pdf_label = str(admissions_policy_pdf.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        admissions_policy_pdf_label = str(admissions_policy_pdf)

    outputs: dict[str, Path] = {}
    if ccd_directory_zip:
        extracted_nces_rows = extract_public_nces_id_rows(roster, ccd_directory_zip)
        write_csv(nces_id_csv, extracted_nces_rows)
        outputs["public_school_nces_ids"] = nces_id_csv
    nces_rows = read_public_nces_id_rows(nces_id_csv)

    school_roster_rows = build_school_roster_rows(
        roster,
        nces_rows,
        admissions_policy_pdf_path=admissions_policy_pdf_label,
        admissions_policy_pdf_hash=admissions_policy_pdf_hash,
    )
    alias_rows = build_alias_rows(roster)
    history_rows = build_school_history_rows(roster)

    school_roster_path = processed_dir / "school_roster.csv"
    aliases_path = manual_dir / "school_aliases.csv"
    history_path = manual_dir / "school_history.csv"
    report_path = report_dir / "roster_review.md"

    write_csv(school_roster_path, school_roster_rows)
    write_csv(aliases_path, alias_rows)
    write_csv(history_path, history_rows)
    write_text(
        report_path,
        build_roster_review_report(
            school_roster_rows=school_roster_rows,
            alias_rows=alias_rows,
            history_rows=history_rows,
            nces_rows=nces_rows,
            admissions_policy_pdf_path=admissions_policy_pdf_label,
            admissions_policy_pdf_hash=admissions_policy_pdf_hash,
        ),
    )
    outputs.update(
        {
            "school_roster": school_roster_path,
            "school_aliases": aliases_path,
            "school_history": history_path,
            "roster_review": report_path,
        }
    )
    return outputs
