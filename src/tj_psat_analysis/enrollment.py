"""Build source-backed grade-11 enrollment denominators."""

from __future__ import annotations

import csv
import hashlib
import io
import subprocess
import tempfile
import zipfile
from collections import Counter
from collections.abc import Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from .constants import CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR
from .seed_workbook import parse_nces_value, write_csv, write_text

PUBLIC_CCD_2024_25_SOURCE_TITLE = (
    "NCES CCD 2024-25 Public Elementary/Secondary School Universe Survey Data, v.2a, School Membership"
)
PUBLIC_CCD_2024_25_SOURCE_URL = "https://nces.ed.gov/ccd/Data/zip/ccd_sch_052_2425_l_1a_073025.zip"
PUBLIC_CCD_2024_25_SOURCE_DATE = "2025-07-30"

PSS_SOURCE_TITLE_BY_SCHOOL_YEAR = {
    "2017-18": "NCES Private School Universe Survey (PSS) 2017-18 Public-Use CSV",
    "2019-20": "NCES Private School Universe Survey (PSS) 2019-20 Public-Use CSV",
    "2021-22": "NCES Private School Universe Survey (PSS) 2021-22 Public-Use CSV",
}

PSS_SOURCE_URL_BY_SCHOOL_YEAR = {
    "2017-18": "https://nces.ed.gov/surveys/pss/zip/pss1718_pu_csv.zip",
    "2019-20": "https://nces.ed.gov/surveys/pss/zip/pss1920_pu_csv.zip",
    "2021-22": "https://nces.ed.gov/surveys/pss/zip/pss2122_pu_csv.zip",
}

PSS_SOURCE_VARIABLE = "P290"
PSS_IMPUTATION_FLAG_VARIABLE = "F_P290"
PSS_SURVEY_SCHOOL_YEARS = frozenset(PSS_SOURCE_TITLE_BY_SCHOOL_YEAR)
PSS_LOCATOR_2023_24_SOURCE_TITLE = "NCES Private School Search locator (PSS 2023-24)"
PSS_LOCATOR_2023_24_SOURCE_DATE = "2023-24"
PSS_LOCATOR_2023_24_SOURCE_VARIABLE = "PSS_ENROLL_11"
PSS_LOCATOR_IMPUTATION_FLAG_STATUS = "not_available_locator"

PANEL_FIELDS = [
    "school_id",
    "school",
    "sector",
    "tj_pathway",
    "division",
    "district_name",
    "class_year",
    "grade11_school_year",
    "grade11_enrollment",
    "enrollment_status",
    "enrollment_source_title",
    "enrollment_source_url",
    "enrollment_source_date",
    "enrollment_source_hash",
    "enrollment_source_file",
    "enrollment_source_rows",
    "enrollment_source_variable",
    "nces_school_id",
    "pss_ppin",
    "pss_imputation_flag",
    "notes",
]

COVERAGE_FIELDS = [
    "school_id",
    "school",
    "sector",
    "class_year",
    "grade11_school_year",
    "enrollment_status",
    "has_grade11_enrollment",
    "enrollment_source_title",
    "enrollment_source_url",
    "enrollment_source_hash",
    "notes",
]


@dataclass(frozen=True)
class PssZipSource:
    school_year: str
    zip_path: Path


@dataclass(frozen=True)
class PublicCcdMembershipSource:
    school_year: str
    zip_path: Path
    source_title: str
    source_url: str
    source_date: str


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _single_csv_member(archive: zipfile.ZipFile, zip_path: Path) -> str:
    csv_names = [name for name in archive.namelist() if name.lower().endswith(".csv")]
    if len(csv_names) != 1:
        raise ValueError(f"Expected exactly one CSV in {zip_path}, found {csv_names}")
    return csv_names[0]


@contextmanager
def _single_csv_text_from_zip(zip_path: Path):
    with zipfile.ZipFile(zip_path) as archive:
        csv_names = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if len(csv_names) == 1:
            member_name = csv_names[0]
            with _zip_member_text(zip_path, member_name) as handle:
                yield member_name, handle
            return

        nested_csv_zips = [
            name
            for name in archive.namelist()
            if name.lower().endswith(".zip") and "csv" in Path(name).name.lower()
        ]
        if csv_names or len(nested_csv_zips) != 1:
            raise ValueError(
                f"Expected one CSV or nested CSV ZIP in {zip_path}, found CSVs={csv_names}, "
                f"nested CSV ZIPs={nested_csv_zips}"
            )

        nested_name = nested_csv_zips[0]
        with tempfile.NamedTemporaryFile(suffix=".zip") as nested_file:
            nested_file.write(archive.read(nested_name))
            nested_file.flush()
            nested_path = Path(nested_file.name)
            with zipfile.ZipFile(nested_path) as nested_archive:
                nested_csv_names = [
                    name for name in nested_archive.namelist() if name.lower().endswith(".csv")
                ]
                if len(nested_csv_names) != 1:
                    raise ValueError(
                        f"Expected exactly one CSV in {zip_path}!{nested_name}, found {nested_csv_names}"
                    )
                nested_csv_name = nested_csv_names[0]
                try:
                    binary_handle = nested_archive.open(nested_csv_name)
                except NotImplementedError:
                    process = subprocess.Popen(
                        ["unzip", "-p", str(nested_path), nested_csv_name],
                        stdout=subprocess.PIPE,
                    )
                    if process.stdout is None:
                        raise RuntimeError(
                            f"Could not stream {nested_csv_name} from {zip_path}!{nested_name}"
                        ) from None
                    text_handle = io.TextIOWrapper(process.stdout, encoding="utf-8-sig", newline="")
                    try:
                        yield f"{nested_name}!{nested_csv_name}", text_handle
                    finally:
                        text_handle.close()
                        return_code = process.wait()
                        if return_code:
                            raise RuntimeError(
                                f"unzip exited with {return_code} for {zip_path}!{nested_name}"
                            )
                else:
                    with binary_handle:
                        text_handle = io.TextIOWrapper(binary_handle, encoding="utf-8-sig", newline="")
                        try:
                            yield f"{nested_name}!{nested_csv_name}", text_handle
                        finally:
                            text_handle.close()
            return


def _zip_member_date(archive: zipfile.ZipFile, member_name: str) -> str:
    info = archive.getinfo(member_name)
    year, month, day = info.date_time[:3]
    return f"{year:04d}-{month:02d}-{day:02d}"


@contextmanager
def _zip_member_text(zip_path: Path, member_name: str):
    with zipfile.ZipFile(zip_path) as archive:
        try:
            binary_handle = archive.open(member_name)
        except NotImplementedError:
            process = subprocess.Popen(
                ["unzip", "-p", str(zip_path), member_name],
                stdout=subprocess.PIPE,
            )
            if process.stdout is None:
                raise RuntimeError(f"Could not stream {member_name} from {zip_path}") from None
            text_handle = io.TextIOWrapper(process.stdout, encoding="utf-8-sig", newline="")
            try:
                yield text_handle
            finally:
                text_handle.close()
                return_code = process.wait()
                if return_code:
                    raise RuntimeError(f"unzip exited with {return_code} for {zip_path}")
        else:
            with binary_handle:
                text_handle = io.TextIOWrapper(binary_handle, encoding="utf-8-sig", newline="")
                yield text_handle


def _index_by_school_year(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, int], Mapping[str, str]]:
    output: dict[tuple[str, int], Mapping[str, str]] = {}
    for row in rows:
        school_id = (row.get("school_id") or "").strip()
        class_year = (row.get("class_year") or "").strip()
        if school_id and class_year:
            output[(school_id, int(class_year))] = row
    return output


def _roster_context(row: Mapping[str, str], class_year: int, school_year: str) -> dict[str, object]:
    return {
        "school_id": row["school_id"],
        "school": row["school"],
        "sector": row["sector"],
        "tj_pathway": row["tj_pathway"],
        "division": row["division"],
        "district_name": row.get("district_name", ""),
        "class_year": class_year,
        "grade11_school_year": school_year,
        "grade11_enrollment": "",
        "enrollment_status": "",
        "enrollment_source_title": "",
        "enrollment_source_url": "",
        "enrollment_source_date": "",
        "enrollment_source_hash": "",
        "enrollment_source_file": "",
        "enrollment_source_rows": "",
        "enrollment_source_variable": "",
        "nces_school_id": row.get("nces_school_id", ""),
        "pss_ppin": "",
        "pss_imputation_flag": "",
        "notes": row.get("notes", ""),
    }


def _copy_enrollment_fields(target: dict[str, object], source: Mapping[str, str]) -> None:
    for field in (
        "grade11_enrollment",
        "enrollment_status",
        "enrollment_source_title",
        "enrollment_source_url",
        "enrollment_source_date",
        "enrollment_source_hash",
        "enrollment_source_file",
        "enrollment_source_rows",
        "enrollment_source_variable",
        "pss_ppin",
        "pss_imputation_flag",
    ):
        if field in source:
            target[field] = source[field]


def _is_not_operating(roster_row: Mapping[str, str], class_year: int) -> bool:
    first_year_text = (roster_row.get("first_operating_class_year") or "").strip()
    return bool(first_year_text and class_year < int(first_year_text))


def build_enrollment_panel_rows(
    school_roster_rows: Sequence[Mapping[str, str]],
    public_seed_rows: Sequence[Mapping[str, str]],
    public_supplement_rows: Sequence[Mapping[str, str]],
    public_2024_25_rows: Sequence[Mapping[str, str]],
    private_pss_rows: Sequence[Mapping[str, str]],
    private_pss_locator_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, object]]:
    public_seed_index = _index_by_school_year(public_seed_rows)
    public_supplement_index = _index_by_school_year(public_supplement_rows)
    public_2024_25_index = _index_by_school_year(public_2024_25_rows)
    private_pss_index = _index_by_school_year(private_pss_rows)
    private_pss_locator_index = _index_by_school_year(private_pss_locator_rows)
    has_private_sources = bool(private_pss_rows)

    output: list[dict[str, object]] = []
    for roster_row in school_roster_rows:
        sector = roster_row["sector"]
        for class_year, school_year in CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR.items():
            row = _roster_context(roster_row, class_year, school_year)
            key = (roster_row["school_id"], class_year)

            if _is_not_operating(roster_row, class_year):
                row["enrollment_status"] = "not_operating"
            elif sector == "public":
                source_row = (
                    public_2024_25_index.get(key)
                    if school_year == "2024-25"
                    else public_supplement_index.get(key) or public_seed_index.get(key)
                )
                if source_row:
                    _copy_enrollment_fields(row, source_row)
                elif school_year == "2024-25":
                    row["enrollment_status"] = "public_2024_25_source_missing"
                else:
                    row["enrollment_status"] = "public_enrollment_not_ingested"
            elif sector == "private":
                source_row = private_pss_locator_index.get(key) or private_pss_index.get(key)
                if source_row:
                    _copy_enrollment_fields(row, source_row)
                elif school_year in PSS_SURVEY_SCHOOL_YEARS:
                    row["enrollment_status"] = (
                        "pss_source_missing" if not has_private_sources else "pss_row_not_found"
                    )
                else:
                    row["enrollment_status"] = "private_pss_not_survey_year"
            else:
                row["enrollment_status"] = "enrollment_not_applicable"

            output.append({field: row.get(field, "") for field in PANEL_FIELDS})
    return output


def _public_grade11_value_from_rows(rows: list[tuple[int, Mapping[str, str]]]) -> tuple[str, str, str]:
    total_rows = [(row_number, row) for row_number, row in rows if _is_total_membership_row(row)]
    if len(total_rows) != 1:
        return "", "ccd_total_row_not_found", ";".join(str(row_number) for row_number, _ in rows)
    row_number, row = total_rows[0]
    count_text = _first_present(row, ("STUDENT_COUNT", "STUDENTCOUNT", "MEMBER", "MEMBERSHIP"))
    value, status = parse_nces_value(count_text)
    return str(value) if value is not None else "", status, str(row_number)


def _first_present(row: Mapping[str, str], names: Sequence[str]) -> str:
    for name in names:
        value = row.get(name)
        if value is not None:
            return str(value).strip()
    return ""


def _is_grade11(row: Mapping[str, str]) -> bool:
    grade = _first_present(row, ("GRADE", "GRADE_LEVEL", "GLEVEL", "GRADELEVEL")).upper()
    return grade in {"11", "GRADE 11", "GRADE 11 STUDENTS", "11TH GRADE", "G11", "UGRADE11"}


def _is_total_value(value: str) -> bool:
    normalized = value.strip().upper()
    return normalized in {"", "TOTAL", "TOT", "99", "TOTAL STUDENTS", "ALL", "NO CATEGORY CODES"}


def _is_total_membership_row(row: Mapping[str, str]) -> bool:
    race = _first_present(row, ("RACE_ETHNICITY", "RACE_ETHNICITY_ID", "RACE", "RACEETHNICITY"))
    sex = _first_present(row, ("SEX", "SEX_ID", "GENDER"))
    return _is_total_value(race) and _is_total_value(sex)


def extract_public_ccd_grade11_rows(
    school_roster_rows: Sequence[Mapping[str, str]],
    membership_zip: Path,
    class_year: int = 2026,
    school_year: str = "2024-25",
) -> list[dict[str, object]]:
    source_hash = sha256_file(membership_zip)
    public_rows = [row for row in school_roster_rows if row["sector"] == "public"]
    target_ids = {row["nces_school_id"]: row for row in public_rows if row.get("nces_school_id")}
    grouped: dict[str, list[tuple[int, Mapping[str, str]]]] = {nces_id: [] for nces_id in target_ids}

    with _single_csv_text_from_zip(membership_zip) as (_member_name, handle):
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "NCESSCH" not in reader.fieldnames:
            raise ValueError(f"{membership_zip} membership CSV is missing NCESSCH")
        for row_number, row in enumerate(reader, start=2):
            nces_school_id = (row.get("NCESSCH") or "").strip()
            if nces_school_id in grouped and _is_grade11(row):
                grouped[nces_school_id].append((row_number, row))

    output: list[dict[str, object]] = []
    for roster_row in public_rows:
        nces_school_id = roster_row.get("nces_school_id", "")
        value = ""
        status = "ccd_row_not_found"
        source_rows = ""
        if nces_school_id:
            matches = grouped.get(nces_school_id, [])
            if matches:
                value, status, source_rows = _public_grade11_value_from_rows(matches)
        output.append(
            {
                "school_id": roster_row["school_id"],
                "school": roster_row["school"],
                "class_year": class_year,
                "grade11_school_year": school_year,
                "grade11_enrollment": value,
                "enrollment_status": status,
                "enrollment_source_title": PUBLIC_CCD_2024_25_SOURCE_TITLE,
                "enrollment_source_url": PUBLIC_CCD_2024_25_SOURCE_URL,
                "enrollment_source_date": PUBLIC_CCD_2024_25_SOURCE_DATE,
                "enrollment_source_hash": source_hash,
                "enrollment_source_file": membership_zip.name,
                "enrollment_source_rows": source_rows,
                "enrollment_source_variable": "GRADE=11 total STUDENT_COUNT",
                "nces_school_id": nces_school_id,
            }
        )
    return output


def extract_public_ccd_membership_grade11_rows(
    school_roster_rows: Sequence[Mapping[str, str]],
    sources: Sequence[PublicCcdMembershipSource],
    target_school_ids: set[str],
) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    target_rows = [
        row
        for row in school_roster_rows
        if row["sector"] == "public" and row["school_id"] in target_school_ids
    ]

    for source in sources:
        class_year = _class_year_for_school_year(source.school_year)
        source_hash = sha256_file(source.zip_path)
        target_ids = {row["nces_school_id"]: row for row in target_rows if row.get("nces_school_id")}
        grouped: dict[str, list[tuple[int, Mapping[str, str]]]] = {nces_id: [] for nces_id in target_ids}

        with _single_csv_text_from_zip(source.zip_path) as (_member_name, handle):
            reader = csv.DictReader(handle)
            if not reader.fieldnames or "NCESSCH" not in reader.fieldnames:
                raise ValueError(f"{source.zip_path} membership CSV is missing NCESSCH")
            for row_number, row in enumerate(reader, start=2):
                nces_school_id = (row.get("NCESSCH") or "").strip()
                if nces_school_id in grouped and _is_grade11(row):
                    grouped[nces_school_id].append((row_number, row))

        for roster_row in target_rows:
            nces_school_id = roster_row.get("nces_school_id", "")
            value = ""
            status = "ccd_row_not_found"
            source_rows = ""
            if nces_school_id:
                matches = grouped.get(nces_school_id, [])
                if matches:
                    value, status, source_rows = _public_grade11_value_from_rows(matches)
            output.append(
                {
                    "school_id": roster_row["school_id"],
                    "school": roster_row["school"],
                    "class_year": class_year,
                    "grade11_school_year": source.school_year,
                    "grade11_enrollment": value,
                    "enrollment_status": status,
                    "enrollment_source_title": source.source_title,
                    "enrollment_source_url": source.source_url,
                    "enrollment_source_date": source.source_date,
                    "enrollment_source_hash": source_hash,
                    "enrollment_source_file": source.zip_path.name,
                    "enrollment_source_rows": source_rows,
                    "enrollment_source_variable": "GRADE=11 total STUDENT_COUNT",
                    "nces_school_id": nces_school_id,
                }
            )

    return output


def _parse_pss_value(value: str) -> tuple[str, str]:
    text = (value or "").strip()
    if not text:
        return "", "blank"
    try:
        parsed = int(float(text.replace(",", "")))
    except ValueError:
        return "", f"unparsed:{text}"
    if parsed < 0:
        return "", f"missing_code:{parsed}"
    return str(parsed), "reported"


def _read_private_pss_id_rows(path: Path) -> dict[str, Mapping[str, str]]:
    rows = load_csv_rows(path)
    output: dict[str, Mapping[str, str]] = {}
    for row_number, row in enumerate(rows, start=2):
        school_id = (row.get("school_id") or "").strip()
        if not school_id:
            raise ValueError(f"{path} row {row_number} missing school_id")
        output[school_id] = row
    return output


def extract_private_pss_grade11_rows(
    school_roster_rows: Sequence[Mapping[str, str]],
    pss_id_csv: Path,
    pss_sources: Sequence[PssZipSource],
) -> list[dict[str, object]]:
    pss_id_by_school_id = _read_private_pss_id_rows(pss_id_csv)
    private_rows = [row for row in school_roster_rows if row["sector"] == "private"]
    output: list[dict[str, object]] = []

    for source in pss_sources:
        class_year = _class_year_for_school_year(source.school_year)
        source_hash = sha256_file(source.zip_path)
        source_title = PSS_SOURCE_TITLE_BY_SCHOOL_YEAR[source.school_year]
        source_url = PSS_SOURCE_URL_BY_SCHOOL_YEAR[source.school_year]
        rows_by_ppin: dict[str, tuple[int, Mapping[str, str]]] = {}
        with zipfile.ZipFile(source.zip_path) as archive:
            member_name = _single_csv_member(archive, source.zip_path)
            source_date = _zip_member_date(archive, member_name)
            with _zip_member_text(source.zip_path, member_name) as handle:
                reader = csv.DictReader(handle)
                required = {"PPIN", "PINST", PSS_SOURCE_VARIABLE, PSS_IMPUTATION_FLAG_VARIABLE}
                missing = required.difference(reader.fieldnames or [])
                if missing:
                    raise ValueError(f"{source.zip_path} missing PSS columns: {', '.join(sorted(missing))}")
                for row_number, row in enumerate(reader, start=2):
                    ppin = (row.get("PPIN") or "").strip()
                    if ppin:
                        rows_by_ppin[ppin] = (row_number, row)

        for roster_row in private_rows:
            pss_id = pss_id_by_school_id.get(roster_row["school_id"], {})
            ppin = (pss_id.get("pss_ppin") or "").strip()
            match_status = (pss_id.get("pss_match_status") or "private_pss_id_pending").strip()
            value = ""
            status = match_status if match_status != "matched" else "pss_row_not_found"
            source_rows = ""
            pss_name = ""
            pss_city = ""
            pss_zip = ""
            imputation_flag = ""
            if ppin and match_status == "matched":
                matched = rows_by_ppin.get(ppin)
                if matched:
                    source_row, pss_row = matched
                    value, status = _parse_pss_value(pss_row.get(PSS_SOURCE_VARIABLE, ""))
                    source_rows = str(source_row)
                    pss_name = pss_row.get("PINST", "")
                    pss_city = pss_row.get("PCITY", "")
                    pss_zip = pss_row.get("PZIP", "")
                    imputation_flag = pss_row.get(PSS_IMPUTATION_FLAG_VARIABLE, "")

            output.append(
                {
                    "school_id": roster_row["school_id"],
                    "school": roster_row["school"],
                    "class_year": class_year,
                    "grade11_school_year": source.school_year,
                    "grade11_enrollment": value,
                    "enrollment_status": status,
                    "enrollment_source_title": source_title,
                    "enrollment_source_url": source_url,
                    "enrollment_source_date": source_date,
                    "enrollment_source_hash": source_hash,
                    "enrollment_source_file": source.zip_path.name,
                    "enrollment_source_rows": source_rows,
                    "enrollment_source_variable": PSS_SOURCE_VARIABLE,
                    "pss_ppin": ppin,
                    "pss_name": pss_name,
                    "pss_city": pss_city,
                    "pss_zip": pss_zip,
                    "pss_imputation_flag": imputation_flag,
                }
            )
    return output


def _class_year_for_school_year(school_year: str) -> int:
    for class_year, candidate in CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR.items():
        if candidate == school_year:
            return class_year
    raise ValueError(f"No class-year mapping for school year {school_year!r}")


def build_enrollment_coverage_rows(panel_rows: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for row in panel_rows:
        output.append(
            {
                "school_id": row["school_id"],
                "school": row["school"],
                "sector": row["sector"],
                "class_year": row["class_year"],
                "grade11_school_year": row["grade11_school_year"],
                "enrollment_status": row["enrollment_status"],
                "has_grade11_enrollment": (
                    "true" if str(row.get("grade11_enrollment", "")).strip() else "false"
                ),
                "enrollment_source_title": row["enrollment_source_title"],
                "enrollment_source_url": row["enrollment_source_url"],
                "enrollment_source_hash": row["enrollment_source_hash"],
                "notes": row["notes"],
            }
        )
    return output


def _markdown_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    rendered = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        rendered.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(rendered)


def _counter_rows(counter: Counter[str]) -> list[list[object]]:
    return [[key or "(blank)", value] for key, value in sorted(counter.items())]


def _class_year_summary(panel_rows: Sequence[Mapping[str, object]]) -> list[list[object]]:
    rows: list[list[object]] = []
    for class_year, school_year in CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR.items():
        class_rows = [row for row in panel_rows if int(str(row["class_year"])) == class_year]
        rows.append(
            [
                class_year,
                school_year,
                sum(1 for row in class_rows if str(row.get("grade11_enrollment", "")).strip()),
                sum(1 for row in class_rows if row["enrollment_status"] == "not_operating"),
                len(class_rows),
            ]
        )
    return rows


def build_enrollment_coverage_report(panel_rows: Sequence[Mapping[str, object]]) -> str:
    source_rows = sorted(
        {
            (
                str(row.get("enrollment_source_title", "")),
                str(row.get("enrollment_source_url", "")),
                str(row.get("enrollment_source_date", "")),
                str(row.get("enrollment_source_hash", "")),
            )
            for row in panel_rows
            if str(row.get("enrollment_source_title", "")).strip()
        }
    )
    lines = [
        "# Enrollment Coverage Report",
        "",
        "This report is generated by the Milestone 3 enrollment builder. It keeps",
        "reported denominators, unavailable source rows, and not-operating years",
        "separate. No enrollment value is estimated from adjacent years.",
        "",
        "## Output Summary",
        "",
        _markdown_table(
            ["Output", "Rows"],
            [
                ["data/processed/enrollment_panel.csv", len(panel_rows)],
                ["reports/data_quality/enrollment_coverage.csv", len(panel_rows)],
            ],
        ),
        "",
        "## Status Counts",
        "",
        _markdown_table(
            ["Enrollment status", "Rows"],
            _counter_rows(Counter(str(row["enrollment_status"]) for row in panel_rows)),
        ),
        "",
        "## Class-Year Coverage",
        "",
        _markdown_table(
            ["Class year", "Grade-11 school year", "Rows with denominator", "Not operating", "Total rows"],
            _class_year_summary(panel_rows),
        ),
        "",
        "## Source Files",
        "",
    ]
    if source_rows:
        lines.append(
            _markdown_table(
                ["Source title", "URL", "Date", "SHA-256"],
                source_rows,
            )
        )
    else:
        lines.append("No source-backed enrollment rows were available.")

    lines.extend(
        [
            "",
            "## Source Rules",
            "",
            "- Public Classes 2019-2025 are carried from the seed workbook export after deterministic "
            "roster joins, with exact-NCES-ID CCD membership supplements used for documented ambiguous "
            "seed rows.",
            "- Public Class 2026 comes from the NCES CCD 2024-25 school membership file when an "
            "extracted row is available.",
            "- Private-school PSS rows use `P290` for grade-11 enrollment and preserve `F_P290` "
            "as `pss_imputation_flag`.",
            "- The 2023-24 NCES Private School Search locator supplement is an official interim "
            "Class 2025 denominator source. It uses the locator file-layout field "
            "`PSS_ENROLL_11` and records `pss_imputation_flag` as `not_available_locator` "
            "because the detail pages do not expose `F_P290`.",
            "- PSS non-survey years without a public-use or locator source row remain blank with "
            "`private_pss_not_survey_year` rather than borrowing adjacent survey years.",
            "",
        ]
    )
    return "\n".join(lines)


def build_enrollment_outputs(
    school_roster_csv: Path,
    public_seed_csv: Path,
    public_supplement_csv: Path,
    public_2024_25_csv: Path,
    private_pss_csv: Path,
    private_pss_locator_csv: Path,
    processed_dir: Path,
    report_dir: Path,
) -> dict[str, Path]:
    school_roster_rows = load_csv_rows(school_roster_csv)
    public_seed_rows = load_csv_rows(public_seed_csv)
    public_supplement_rows = load_csv_rows(public_supplement_csv)
    public_2024_25_rows = load_csv_rows(public_2024_25_csv)
    private_pss_rows = load_csv_rows(private_pss_csv)
    private_pss_locator_rows = load_csv_rows(private_pss_locator_csv)
    panel_rows = build_enrollment_panel_rows(
        school_roster_rows=school_roster_rows,
        public_seed_rows=public_seed_rows,
        public_supplement_rows=public_supplement_rows,
        public_2024_25_rows=public_2024_25_rows,
        private_pss_rows=private_pss_rows,
        private_pss_locator_rows=private_pss_locator_rows,
    )
    coverage_rows = build_enrollment_coverage_rows(panel_rows)

    outputs = {
        "enrollment_panel": processed_dir / "enrollment_panel.csv",
        "enrollment_coverage_csv": report_dir / "enrollment_coverage.csv",
        "enrollment_coverage_md": report_dir / "enrollment_coverage.md",
    }
    write_csv(outputs["enrollment_panel"], panel_rows)
    write_csv(outputs["enrollment_coverage_csv"], coverage_rows)
    write_text(outputs["enrollment_coverage_md"], build_enrollment_coverage_report(panel_rows))
    return outputs
