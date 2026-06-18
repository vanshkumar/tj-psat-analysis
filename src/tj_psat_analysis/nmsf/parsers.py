"""Parser registry for National Merit Semifinalist sources.

These parser classes intentionally do not return counts until source-specific
logic is implemented and verified. This prevents scratch workbook numbers from
becoming data by accident.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedNmsfRecord:
    school_name: str
    class_year: int
    nmsf_count: int | None
    status: str
    source_title: str
    source_url: str
    source_date: str
    source_hash: str
    source_scope: str


class SourceParser:
    provider = "generic"
    parser_name = "generic"
    parser_version = "0"

    def parse(self, content: str, *, class_year: int, metadata: dict[str, str]) -> list[ParsedNmsfRecord]:
        raise NotImplementedError(f"{self.provider} parser is a source-safe stub")


class ManualReviewedTableParser(SourceParser):
    provider = "manual"
    parser_name = "manual_reviewed_table"
    parser_version = "1"


class StructuredHtmlParser(SourceParser):
    provider = "html"
    parser_name = "structured_html"
    parser_version = "1"


class PdfTextParser(SourceParser):
    provider = "pdf"
    parser_name = "pdf_text"
    parser_version = "1"


class FcpsParser(SourceParser):
    provider = "fcps"
    parser_name = "fcps_source_safe_stub"


class LcpsParser(SourceParser):
    provider = "lcps"
    parser_name = "lcps_source_safe_stub"


class ApsParser(SourceParser):
    provider = "aps"
    parser_name = "aps_source_safe_stub"


class PwcsParser(SourceParser):
    provider = "pwcs"
    parser_name = "pwcs_source_safe_stub"


class FccpsParser(SourceParser):
    provider = "fccps"
    parser_name = "fccps_source_safe_stub"


class SchoolReleaseParser(SourceParser):
    provider = "school_release"
    parser_name = "school_release_source_safe_stub"


class LocalMediaParser(SourceParser):
    provider = "local_media"
    parser_name = "local_media_source_safe_stub"


class NmscVirginiaListParser(SourceParser):
    provider = "nmsc_virginia_list"
    parser_name = "nmsc_virginia_list_source_safe_stub"


PARSER_REGISTRY_BY_PROVIDER: dict[str, type[SourceParser]] = {
    parser.provider: parser
    for parser in (
        FcpsParser,
        LcpsParser,
        ApsParser,
        PwcsParser,
        FccpsParser,
        SchoolReleaseParser,
        LocalMediaParser,
        NmscVirginiaListParser,
    )
}

PARSER_REGISTRY_BY_NAME: dict[str, type[SourceParser]] = {
    parser.parser_name: parser
    for parser in (
        ManualReviewedTableParser,
        StructuredHtmlParser,
        PdfTextParser,
        FcpsParser,
        LcpsParser,
        ApsParser,
        PwcsParser,
        FccpsParser,
        SchoolReleaseParser,
        LocalMediaParser,
        NmscVirginiaListParser,
    )
}

PARSER_REGISTRY = PARSER_REGISTRY_BY_PROVIDER
