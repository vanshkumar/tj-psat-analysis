"""Milestone 10 focal-period completion and source-discovery reporting."""

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
        action="Retain the archived press releases as discovery evidence only; do not create counts or zeros.",
    ),
    SourceDiscoveryAttempt(
        workflow="Internet Archive CDX",
        query_or_source=(
            "NMSC broad semifinalist URL wildcard (`www.nationalmerit.org/*national*merit*semifinal*`)"
        ),
        result="Returned an empty CDX result for the focal window.",
        finding="No alternate NMSC-hosted complete-list URL was found.",
        action="Keep Priority A dependent on a public media mirror or other complete source.",
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
        action="Do not change observation counts; keep remaining rows `missing_source`.",
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
        "Generated for Milestone 10 from the current focal-period observation layer and archived "
        "NMSC press-release source artifacts.",
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
        "A follow-up public-source sweep looked for complete Virginia school-by-school lists or "
        "authoritative mirrors for Classes 2023-2026. It did not locate a complete list. These "
        "searches are documented as reproducible limitation evidence; they do not establish zeros "
        "for missing schools.",
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
        "- Do not add these NMSC press releases to `data/sources/source_manifest.yml` as numeric "
        "count sources because they do not provide school-level Virginia counts.",
        "- Do not infer zeros for missing public or private rows from these press releases.",
        "- Continue Priority A only from a public media mirror or other source that exposes a "
        "complete Virginia school-by-school list for the relevant class year.",
        "- Leave Virginia statewide-share metrics blocked until a complete list or exact statewide "
        "semifinalist total is source-backed.",
        "",
    ]
    return "\n".join(lines)


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
