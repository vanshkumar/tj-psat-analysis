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

FOCAL_CLASS_YEARS = (2023, 2024, 2025, 2026)

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
    SourceDiscoveryAttempt(
        workflow="Reddit metadata APIs plus Internet Archive and Common Crawl",
        query_or_source=(
            "Deleted r/psat gallery post `1fekyi6` (`2025 NMSF Virginia`) with recovered media IDs "
            "`1xu2738au8od1`, `nwinp3feu8od1`, and `ynlabcqhu8od1`; corrected first-page post "
            "`1femf90` with media ID `wdipgaas59od1`"
        ),
        result=(
            "The archived shell preserves three page-image URLs, but the Reddit CDN objects now return "
            "404 and neither Internet Archive nor Common Crawl has recoverable image bytes."
        ),
        finding=(
            "The strongest statewide-list lead is identifiable but its school-list images are unavailable."
        ),
        action=(
            "Retain the media IDs as a future recovery lead; do not create counts or zeros from the "
            "deleted-gallery shell."
        ),
    ),
    SourceDiscoveryAttempt(
        workflow="Identity-level source reconciliation",
        query_or_source=(
            "Official LCPS 57-name release against Patch's school-attributed Loudoun list and FCPS's "
            "official TJHSST list, with one spelling variant checked against a U.S. Education list"
        ),
        result=(
            "All 57 distinct LCPS identities partition exactly into 42 Patch-attributed LCPS-public "
            "students and 15 students on the official TJHSST list."
        ),
        finding=(
            "The school-attributed LCPS-public partition is exhaustive without allocating the district "
            "total or assigning TJHSST residents to base schools."
        ),
        action=(
            "Use the archived count-only reconciliation to verify zero for the four absent operating "
            "LCPS roster schools; keep Patch alone incomplete for zero inference."
        ),
    ),
)

LCPS_2025_TARGETED_SOURCES = (
    "NMSC 2025 press release; official LCPS 57-student total-only release; "
    "Ashburn Patch school-grouped article; official FCPS TJHSST list; U.S. Education "
    "candidate list for one spelling check; LCPS school sites/APIs; LCPS, Patch, "
    "Loudoun Now, and Loudoun Times targeted web/CDX checks"
)

TARGETED_CLASS_2025_ROW_SEARCHES = (
    TargetedMissingRowSearch(
        class_year=2025,
        division="Falls Church City",
        school="Meridian High School",
        sources_checked=(
            "NMSC 2025 press release; FCCPS/Meridian Apptegy news, live-feed, "
            "and search surfaces; Falls Church News-Press graduation report "
            "(https://www.fcnp.com/2025/05/28/meridian-graduation-noonans-farewell/); "
            "Patch Falls Church/Fairfax City checks; FCCPS/Meridian/Patch CDX checks; "
            "deleted Reddit Virginia-gallery metadata and archive checks"
        ),
        result=(
            "No source-backed Meridian semifinalist count was found. A Falls Church News-Press "
            "graduation report gives four finalists, which cannot establish the semifinalist count; "
            "the deleted statewide gallery's image bytes remain unavailable."
        ),
        action="Retain as `missing_source`; no zero inference.",
    ),
    TargetedMissingRowSearch(
        class_year=2025,
        division="LCPS",
        school="Loudoun Valley High School",
        sources_checked=LCPS_2025_TARGETED_SOURCES,
        result=(
            "Verified zero: the official 57-name LCPS list reconciles exhaustively to 42 "
            "Patch-attributed LCPS-public identities plus 15 official TJHSST identities."
        ),
        action="Record `verified_zero` from `lcps_2025_named_list_reconciliation`.",
    ),
    TargetedMissingRowSearch(
        class_year=2025,
        division="LCPS",
        school="Park View High School",
        sources_checked=LCPS_2025_TARGETED_SOURCES,
        result=(
            "Verified zero: the official 57-name LCPS list reconciles exhaustively to 42 "
            "Patch-attributed LCPS-public identities plus 15 official TJHSST identities."
        ),
        action="Record `verified_zero` from `lcps_2025_named_list_reconciliation`.",
    ),
    TargetedMissingRowSearch(
        class_year=2025,
        division="LCPS",
        school="Tuscarora High School",
        sources_checked=LCPS_2025_TARGETED_SOURCES,
        result=(
            "Verified zero: the official 57-name LCPS list reconciles exhaustively to 42 "
            "Patch-attributed LCPS-public identities plus 15 official TJHSST identities."
        ),
        action="Record `verified_zero` from `lcps_2025_named_list_reconciliation`.",
    ),
    TargetedMissingRowSearch(
        class_year=2025,
        division="LCPS",
        school="Woodgrove High School",
        sources_checked=LCPS_2025_TARGETED_SOURCES,
        result=(
            "Verified zero: the official 57-name LCPS list reconciles exhaustively to 42 "
            "Patch-attributed LCPS-public identities plus 15 official TJHSST identities."
        ),
        action="Record `verified_zero` from `lcps_2025_named_list_reconciliation`.",
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
        "where available. Statewide totals are reported separately for Virginia-location media "
        "lists and official NMSC Virginia selection units.",
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
        "those class years. These packets are location lists: their totals include Semifinalists "
        "grouped under Virginia-located schools, including students who may belong to NMSC's "
        "separate U.S. boarding-school selection unit. NMSC's guides report the Virginia state "
        "selection unit separately. Class 2025 lacks a source-backed total in either scope, so "
        "statewide-share metrics remain blank there; the remaining row-level gaps are handled "
        "individually below.",
        "",
        _markdown_table(
            [
                "Class",
                "Virginia-Location Media-List Total",
                "Official NMSC Virginia Selection-Unit Total",
                "Location Source ID",
                "Location Snapshot",
                "Location SHA-256",
                "Official Guide Source",
                "Official Guide Date",
                "Official Guide SHA-256",
            ],
            _virginia_list_table_rows(root),
        ),
        "",
        (
            "Statewide scope rule: use the Virginia-location media-list totals (400, 470, and "
            "494) only with location-scoped numerators. Use the official NMSC Virginia "
            "selection-unit totals (397, 467, and 489) only with numerators that exclude students "
            "assigned to other NMSC selection units. These are different scopes, not competing "
            "estimates. Do not substitute an official selection-unit denominator beneath an "
            "unadjusted location-list numerator. No source-backed statewide denominator is "
            "available for Class 2025 in either scope."
        ),
        "",
        "## Targeted Class 2025 Row Search",
        "",
        "Five public Class 2025 rows were targeted directly after the 2023, 2024, and 2026 "
        "complete-list integration. Exact identity-level reconciliation closes the four LCPS "
        "rows as verified zeros without allocating the unattributed district total: 42 directly "
        "school-attributed LCPS-public identities plus 15 official TJHSST identities exhaust the "
        "official 57-name LCPS release. Meridian remains missing because the available graduation "
        "report counts finalists rather than semifinalists and the deleted statewide gallery's "
        "image bytes could not be recovered. A full Class 2025 statewide packet would still improve "
        "supplemental statewide-share metrics.",
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
        "Public-source sweeps looked for complete Virginia school-by-school lists or authoritative "
        "mirrors for Classes 2023-2026. The latest pass recovered the deleted Class 2025 Reddit "
        "gallery's metadata and archived shell but not its image bytes. Separately, exact LCPS "
        "name-set reconciliation establishes the four LCPS zeros; archive or search absence alone "
        "does not establish any zero.",
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
        "source-backed count, zero-inference, and Virginia-location-total sources; do not label "
        "their totals as official Virginia selection-unit totals.",
        "- Preserve the official NMSC Virginia selection-unit totals of 397, 467, and 489 as a "
        "separate statewide scope and require scope-matched numerators before calculating shares.",
        "- Do not infer zeros for missing public or private rows from these press releases.",
        "- Treat recovery of the deleted Class 2025 Virginia gallery images or another complete "
        "statewide list as useful future work for Meridian and statewide-share metrics.",
        "- Use `lcps_2025_named_list_reconciliation` for the four Class 2025 LCPS verified zeros; "
        "the source exhausts the official named population and keeps TJHSST as one row.",
        "- Retain Meridian High School Class 2025 as `missing_source`; four reported finalists do "
        "not establish the semifinalist count.",
        "- Publish Virginia statewide-share metrics only when both numerator and denominator use "
        "the same documented scope; leave Class 2025 shares blank until a source-backed statewide "
        "total is added.",
        "",
    ]
    return "\n".join(lines)


def _virginia_list_table_rows(root: Path) -> list[list[str]]:
    totals_path = root / "data" / "sources" / "virginia_statewide_totals.csv"
    totals = (
        {int(row["class_year"]): row for row in load_csv_rows(totals_path)} if totals_path.exists() else {}
    )
    snapshots = {source.class_year: source for source in NMSC_VIRGINIA_LIST_SNAPSHOTS}
    rows: list[list[str]] = []
    for class_year in FOCAL_CLASS_YEARS:
        snapshot = snapshots.get(class_year)
        total_row = totals.get(class_year, {})
        location_total = total_row.get("virginia_location_nmsf_semifinalist_total", "")
        selection_total = total_row.get("statewide_nmsf_semifinalist_total", "")
        guide_title = total_row.get("source_title", "")
        guide_url = total_row.get("source_url", "")
        rows.append(
            [
                str(class_year),
                location_total or "not sourced",
                selection_total or "not sourced",
                snapshot.source_id if snapshot is not None else "",
                snapshot.archived_file_path if snapshot is not None else "",
                _sha256(root / snapshot.archived_file_path) if snapshot is not None else "",
                f"[{guide_title}]({guide_url})" if guide_title and guide_url else "",
                total_row.get("source_date", ""),
                total_row.get("source_hash", ""),
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
