"""Build focal-period completion and source-discovery reporting."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class NmscPressRelease:
    class_year: int
    announcement_date: str
    source_title: str
    official_url: str
    archive_url: str
    archived_file_path: str


@dataclass(frozen=True)
class SourceDiscoveryAttempt:
    workflow: str
    query_or_source: str
    result: str
    finding: str
    action: str


@dataclass(frozen=True)
class TargetedMissingRowSearch:
    class_year: int
    division: str
    school: str
    sources_checked: str
    result: str
    action: str


@dataclass(frozen=True)
class NmscVirginiaListSnapshot:
    class_year: int
    source_id: str
    source_title: str
    source_url: str
    source_date: str
    archived_file_path: str


NMSC_PRESS_RELEASES = (
    NmscPressRelease(
        class_year=2023,
        announcement_date="2022-09-14",
        source_title="Semifinalists in the 2023 National Merit Scholarship Program",
        official_url=(
            "https://www.nationalmerit.org/s/1758/images/gid2/editor_documents/23_meritsemi.pdf?gid=2&pgid=61"
        ),
        archive_url=(
            "https://web.archive.org/web/20230124063310id_/https://www.nationalmerit.org/"
            "s/1758/images/gid2/editor_documents/23_meritsemi.pdf?gid=2&pgid=61"
            "&sessionid=1cbdcec5-78b1-40af-8c1e-8ca2e984aa02&cc=1"
        ),
        archived_file_path="data/raw/nmsf/virginia/nmsc_2023_semifinalist_press_release.pdf",
    ),
    NmscPressRelease(
        class_year=2024,
        announcement_date="2023-09-13",
        source_title="Semifinalists in the 2024 National Merit Scholarship Program",
        official_url=(
            "https://www.nationalmerit.org/s/1758/images/gid2/editor_documents/24_meritsemi.pdf?gid=2&pgid=61"
        ),
        archive_url=(
            "https://web.archive.org/web/20230924154603id_/https://www.nationalmerit.org/"
            "s/1758/images/gid2/editor_documents/24_meritsemi.pdf?gid=2&pgid=61"
            "&sessionid=74ca8d4c-9df3-411f-b636-a00d334a70a5&cc=1"
        ),
        archived_file_path="data/raw/nmsf/virginia/nmsc_2024_semifinalist_press_release.pdf",
    ),
    NmscPressRelease(
        class_year=2025,
        announcement_date="2024-09-11",
        source_title="Semifinalists in the 2025 National Merit Scholarship Program",
        official_url=(
            "https://www.nationalmerit.org/s/1758/images/gid2/editor_documents/25_meritsemi.pdf?gid=2&pgid=61"
        ),
        archive_url=(
            "https://web.archive.org/web/20240920184740id_/https://www.nationalmerit.org/"
            "s/1758/images/gid2/editor_documents/25_meritsemi.pdf?gid=2&pgid=61"
            "&sessionid=3a45cc2f-8977-4f28-a856-912b68b11652&cc=1"
        ),
        archived_file_path="data/raw/nmsf/virginia/nmsc_2025_semifinalist_press_release.pdf",
    ),
    NmscPressRelease(
        class_year=2026,
        announcement_date="2025-09-10",
        source_title="Semifinalists in the 2026 National Merit Scholarship Program",
        official_url=(
            "https://www.nationalmerit.org/s/1758/images/gid2/editor_documents/26_meritsemi.pdf?gid=2&pgid=61"
        ),
        archive_url=(
            "https://web.archive.org/web/20250911030211id_/https://www.nationalmerit.org/"
            "s/1758/images/gid2/editor_documents/26_meritsemi.pdf?gid=2&pgid=61"
            "&sessionid=9cf294fc-696d-4aca-a359-289d4d9ef48d&cc=1"
        ),
        archived_file_path="data/raw/nmsf/virginia/nmsc_2026_semifinalist_press_release.pdf",
    ),
)

NMSC_VIRGINIA_LIST_SNAPSHOTS = (
    NmscVirginiaListSnapshot(
        class_year=2023,
        source_id="nmsc_virginia_2023_semifinalists",
        source_title="Semifinalists in the 2023 National Merit Scholarship Program - Virginia list",
        source_url="https://drive.google.com/file/d/1lukNgBPkoLPTaAptU7YrhkG8YtauqYqa/view",
        source_date="2022-09-14",
        archived_file_path="data/raw/nmsf/virginia/virginia_2023_semifinalists_snapshot.csv",
    ),
    NmscVirginiaListSnapshot(
        class_year=2024,
        source_id="nmsc_virginia_2024_semifinalists",
        source_title="Semifinalists in the 2024 National Merit Scholarship Program - Virginia list",
        source_url="https://web.archive.org/web/20230915001040if_/https%3A//litter.catbox.moe/5lujlt.pdf",
        source_date="2023-09-13",
        archived_file_path="data/raw/nmsf/virginia/virginia_2024_semifinalists_snapshot.csv",
    ),
    NmscVirginiaListSnapshot(
        class_year=2026,
        source_id="nmsc_virginia_2026_semifinalists",
        source_title="Semifinalists in the 2026 National Merit Scholarship Program - Virginia list",
        source_url="https://drive.google.com/file/d/1xCdjpoXII9oTmu_hWYFqeWl5XWmTblSu/view",
        source_date="2025-09-10",
        archived_file_path="data/raw/nmsf/virginia/virginia_2026_semifinalists_snapshot.csv",
    ),
)

SOURCE_DISCOVERY_ATTEMPTS = (
    SourceDiscoveryAttempt(
        workflow="Internet Archive CDX",
        query_or_source=(
            "NMSC editor-document PDF index, focal window 2022-09 through 2025-09 "
            "(`www.nationalmerit.org/s/1758/images/gid2/editor_documents/*`)"
        ),
        result=(
            "Returned annual press releases, scholarship-recipient PDFs, annual reports, and guide PDFs; "
            "the focal semifinalist artifacts were `23_meritsemi.pdf` through `26_meritsemi.pdf`."
        ),
        finding="No state-list or Virginia-list filename was exposed in the NMSC PDF index.",
        action=(
            "Retain the archived press releases as discovery evidence only; do not create counts or zeros."
        ),
    ),
    SourceDiscoveryAttempt(
        workflow="Internet Archive CDX",
        query_or_source=(
            "NMSC broad semifinalist URL wildcard (`www.nationalmerit.org/*national*merit*semifinal*`)"
        ),
        result="Returned an empty CDX result for the focal window.",
        finding="No alternate NMSC-hosted complete-list URL was found.",
        action=(
            "Treat complete Class 2025 Virginia list recovery as optional future work; "
            "do not make it a prerequisite for closing the focal-period cleanup."
        ),
    ),
    SourceDiscoveryAttempt(
        workflow="Public web search",
        query_or_source=(
            "Class-year phrase searches for `National Merit Semifinalists Virginia` and "
            "`National Merit Scholarship Semifinalists Virginia`, Classes 2023-2026"
        ),
        result=(
            "Did not surface a complete statewide school-by-school list; visible results were irrelevant, "
            "school pages, or local/school-area articles already handled as incomplete sources."
        ),
        finding="No complete public Virginia mirror was located through broad web search.",
        action=(
            "Do not change Class 2025 observations from search absence; keep remaining rows `missing_source`."
        ),
    ),
    SourceDiscoveryAttempt(
        workflow="Common Crawl URL index",
        query_or_source=(
            "Wildcard URL probes including `*national*merit*semifinal*virginia*` and "
            "`*national-merit-semifinalists*virginia*` in 2023-2025 indexes"
        ),
        result="Returned no captures for the tested URL patterns.",
        finding="No broad web-crawl URL evidence of a public Virginia list mirror was found.",
        action="Use this only as search-limitation evidence, not as evidence of zero semifinalists.",
    ),
    SourceDiscoveryAttempt(
        workflow="Internet Archive CDX",
        query_or_source=(
            "Major Virginia/DC media URL patterns under Richmond Times-Dispatch, Roanoke Times, "
            "Daily Press, The Virginian-Pilot, Daily Progress, News & Advance, AP, WTOP, "
            "InsideNoVa, and FFXnow"
        ),
        result=(
            "Responsive domain patterns returned empty result sets; the Fredericksburg.com wildcard "
            "timed out rather than producing usable candidates."
        ),
        finding="No complete statewide media mirror was found in these broad media-domain URL indexes.",
        action="Document the limitation and avoid continuing lower-yield school-by-school scraping.",
    ),
    SourceDiscoveryAttempt(
        workflow="Internet Archive CDX",
        query_or_source="Patch Virginia URL patterns (`patch.com/virginia/*national-merit*` variants)",
        result=(
            "The broad archive URL patterns returned empty, while the project already has relevant "
            "Patch articles discovered through community topic feeds and local searches."
        ),
        finding="Patch coverage remains local or school-area coverage, not a complete Virginia list.",
        action="Keep Patch-derived rows positive-only; never use Patch absence for zero inference.",
    ),
)

LCPS_2025_TARGETED_SOURCES = (
    "NMSC 2025 press release; official LCPS 57-student total-only release; "
    "Ashburn Patch positive school-grouped article; LCPS school sites/APIs; "
    "LCPS, Patch, Loudoun Now, and Loudoun Times targeted web/CDX checks"
)

TARGETED_CLASS_2025_ROW_SEARCHES = (
    TargetedMissingRowSearch(
        class_year=2025,
        division="Falls Church City",
        school="Meridian High School",
        sources_checked=(
            "NMSC 2025 press release; FCCPS/Meridian Apptegy news, live-feed, "
            "and search surfaces; Falls Church News-Press issue-week checks; "
            "Patch Falls Church/Fairfax City checks; FCCPS/Meridian/Patch CDX checks"
        ),
        result=("No Meridian school-level count and no complete Class 2025 Virginia list were found."),
        action="Retain as `missing_source`; no zero inference.",
    ),
    TargetedMissingRowSearch(
        class_year=2025,
        division="LCPS",
        school="Loudoun Valley High School",
        sources_checked=LCPS_2025_TARGETED_SOURCES,
        result=(
            "No school-level count found; LCPS total-only coverage and Patch omission "
            "cannot support zero inference."
        ),
        action="Retain as `missing_source`; no zero inference.",
    ),
    TargetedMissingRowSearch(
        class_year=2025,
        division="LCPS",
        school="Park View High School",
        sources_checked=LCPS_2025_TARGETED_SOURCES,
        result=(
            "No school-level count found; LCPS total-only coverage and Patch omission "
            "cannot support zero inference."
        ),
        action="Retain as `missing_source`; no zero inference.",
    ),
    TargetedMissingRowSearch(
        class_year=2025,
        division="LCPS",
        school="Tuscarora High School",
        sources_checked=LCPS_2025_TARGETED_SOURCES,
        result=(
            "No school-level count found; LCPS total-only coverage and Patch omission "
            "cannot support zero inference."
        ),
        action="Retain as `missing_source`; no zero inference.",
    ),
    TargetedMissingRowSearch(
        class_year=2025,
        division="LCPS",
        school="Woodgrove High School",
        sources_checked=LCPS_2025_TARGETED_SOURCES,
        result=(
            "No school-level count found; LCPS total-only coverage and Patch omission "
            "cannot support zero inference."
        ),
        action="Retain as `missing_source`; no zero inference.",
    ),
)


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_focal_period_completion_report(
    *,
    observations_csv: Path,
    root: Path,
) -> str:
    rows = load_csv_rows(observations_csv)
    status_counts = Counter(row["nmsf_status"] for row in rows)
    missing_rows = [row for row in rows if row["nmsf_status"] == "missing_source"]
    missing_summary = Counter((row["class_year"], row["division"], row["sector"]) for row in missing_rows)

    lines = [
        "# Focal-Period Completion Report",
        "",
        "Generated from the current focal-period observation layer, archived "
        "NMSC press-release source artifacts, and count-only complete Virginia list snapshots "
        "where available.",
        "",
        "## Current Observation Coverage",
        "",
        _markdown_table(
            ["Status", "Rows"],
            [[status, str(count)] for status, count in sorted(status_counts.items())],
        ),
        "",
        "## Remaining Missing Source Rows",
        "",
        _markdown_table(
            ["Class", "Division", "Sector", "Missing Rows"],
            [
                [class_year, division, sector, str(count)]
                for (class_year, division, sector), count in sorted(missing_summary.items())
            ],
        ),
        "",
        _markdown_table(
            ["Class", "Division", "School", "Sector", "Pathway"],
            [
                [
                    row["class_year"],
                    row["division"],
                    row["school"],
                    row["sector"],
                    row["tj_pathway"],
                ]
                for row in missing_rows
            ],
        ),
        "",
        "## NMSC Virginia List Integration",
        "",
        "User-supplied NMSC media packets expose complete Virginia school-by-school lists for "
        "Classes 2023, 2024, and 2026. The repo archives count-only snapshots that omit student "
        "names, imports only still-missing positive roster rows from those lists, and uses the "
        "complete Virginia scope to infer verified zeros for absent operating roster schools in "
        "those class years. Class 2025 lacks a comparable complete list, so statewide-share metrics "
        "remain blank there; the remaining row-level gaps are handled individually below.",
        "",
        _markdown_table(
            ["Class", "Source ID", "Statewide Total", "Snapshot", "SHA-256"],
            _virginia_list_table_rows(root),
        ),
        "",
        (
            "Statewide-share caveat: the Class 2026 supplied-list snapshot totals 494, while "
            "the public NMSC 2026 guide cross-check lists Virginia at 489 semifinalists. This "
            "does not change local school counts or zero-inference coverage, but 2026 "
            "statewide-share denominators should be reconciled before final use."
        ),
        "",
        "## Targeted Class 2025 Row Search",
        "",
        "The remaining focal-period gaps are five public Class 2025 rows. Each was targeted "
        "directly after the 2023, 2024, and 2026 complete-list integration. None has a "
        "source-backed positive count, and none has a complete source scope that can support "
        "a verified zero. Recovering the full Class 2025 statewide packet would improve "
        "supplemental statewide-share metrics, but it is not required to close this "
        "public-source cleanup pass.",
        "",
        _markdown_table(
            ["Class", "Division", "School", "Sources Checked", "Result", "Action"],
            [
                [
                    str(search.class_year),
                    search.division,
                    search.school,
                    search.sources_checked,
                    search.result,
                    search.action,
                ]
                for search in TARGETED_CLASS_2025_ROW_SEARCHES
            ],
        ),
        "",
        "## NMSC Press-Release Audit",
        "",
        "The archived NMSC PDFs are official press releases, not school-by-school or Virginia-list "
        "source tables. Visual inspection confirmed that the releases describe the annual program "
        "and state that the named Semifinalist list was distributed to news media but is not posted "
        "on the NMSC website. Because these PDFs do not identify Virginia schools or students, this "
        "pass does not create `verified_count`, `verified_zero`, or Virginia-share rows from them.",
        "",
        _markdown_table(
            ["Class", "Date", "Archived File", "SHA-256", "Finding"],
            [
                [
                    str(source.class_year),
                    source.announcement_date,
                    source.archived_file_path,
                    _sha256(root / source.archived_file_path),
                    "Official press release only; no school-by-school list.",
                ]
                for source in NMSC_PRESS_RELEASES
            ],
        ),
        "",
        "## Broad Source-Discovery Log",
        "",
        "An earlier public-source sweep looked for complete Virginia school-by-school lists or "
        "authoritative mirrors for Classes 2023-2026. It did not locate the now-supplied 2023, "
        "2024, and 2026 list files, and it remains useful limitation evidence for the unsourced "
        "Class 2025 statewide list/total. These searches do not establish zeros for missing "
        "schools.",
        "",
        _markdown_table(
            ["Workflow", "Query Or Source", "Result", "Finding", "Action"],
            [
                [
                    attempt.workflow,
                    attempt.query_or_source,
                    attempt.result,
                    attempt.finding,
                    attempt.action,
                ]
                for attempt in SOURCE_DISCOVERY_ATTEMPTS
            ],
        ),
        "",
        "## Source-Discovery Decision",
        "",
        "- Do not add the NMSC press-release-only PDFs to `data/sources/source_manifest.yml` as "
        "numeric count sources because they do not provide school-level Virginia counts.",
        "- Use the supplied complete NMSC Virginia lists for Classes 2023, 2024, and 2026 as "
        "source-backed count, zero-inference, and statewide-total sources.",
        "- Do not infer zeros for missing public or private rows from these press releases.",
        "- Treat a complete Class 2025 Virginia school-by-school list as optional future work, not "
        "a prerequisite for closing the public-source cleanup pass.",
        "- Retain the five targeted Class 2025 rows as `missing_source` unless a school-attributed "
        "count source or complete zero-inference scope appears.",
        "- Publish Virginia statewide-share metrics for source-backed complete-list years only; "
        "leave Class 2025 shares blank until a source-backed statewide total is added.",
        "",
    ]
    return "\n".join(lines)


def _virginia_list_table_rows(root: Path) -> list[list[str]]:
    totals_path = root / "data" / "sources" / "virginia_statewide_totals.csv"
    totals = {row["source_id"]: row for row in load_csv_rows(totals_path)} if totals_path.exists() else {}
    rows: list[list[str]] = []
    for source in NMSC_VIRGINIA_LIST_SNAPSHOTS:
        total = totals.get(source.source_id, {}).get("statewide_nmsf_semifinalist_total", "")
        rows.append(
            [
                str(source.class_year),
                source.source_id,
                total,
                source.archived_file_path,
                _sha256(root / source.archived_file_path),
            ]
        )
    return rows


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    table = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    table.extend("| " + " | ".join(_escape_cell(cell) for cell in row) + " |" for row in rows)
    return "\n".join(table)


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|")
