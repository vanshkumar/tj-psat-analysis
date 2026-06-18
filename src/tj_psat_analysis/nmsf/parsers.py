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

    def parse(self, content: str, *, class_year: int, metadata: dict[str, str]) -> list[ParsedNmsfRecord]:
        raise NotImplementedError(f"{self.provider} parser is a source-safe stub")


class FcpsParser(SourceParser):
    provider = "fcps"


class LcpsParser(SourceParser):
    provider = "lcps"


class ApsParser(SourceParser):
    provider = "aps"


class PwcsParser(SourceParser):
    provider = "pwcs"


class FccpsParser(SourceParser):
    provider = "fccps"


class SchoolReleaseParser(SourceParser):
    provider = "school_release"


class LocalMediaParser(SourceParser):
    provider = "local_media"


class NmscVirginiaListParser(SourceParser):
    provider = "nmsc_virginia_list"


PARSER_REGISTRY: dict[str, type[SourceParser]] = {
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
