"""Shared constants for panel construction."""

from __future__ import annotations

CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR: dict[int, str] = {
    2019: "2017-18",
    2020: "2018-19",
    2021: "2019-20",
    2022: "2020-21",
    2023: "2021-22",
    2024: "2022-23",
    2025: "2023-24",
    2026: "2024-25",
}

CLASS_YEARS: tuple[int, ...] = tuple(CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR)

SEED_WORKBOOK_RELATIVE_PATH = "docs/source_notes/tj psat investigation.xlsx"
ROSTER_SHEET = "raw"
PUBLIC_ENROLLMENT_SHEET = "Sheet6"

PUBLIC_ENROLLMENT_SOURCE_TITLE = "NCES CCD Public Elementary/Secondary School Universe Survey via ELSI export"
PUBLIC_ENROLLMENT_SOURCE_URL = "http://nces.ed.gov/ccd/elsi/"
