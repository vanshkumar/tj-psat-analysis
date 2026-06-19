"""Source-manifest schema for NMSF observations."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tj_psat_analysis.nmsf.parsers import PARSER_REGISTRY_BY_NAME

NMSF_OBSERVATION_STATUSES = frozenset(
    {
        "verified_count",
        "verified_zero",
        "missing_source",
        "source_incomplete",
        "ambiguous_school",
        "not_operating",
        "not_applicable",
    }
)

NUMERIC_NMSF_STATUSES = frozenset({"verified_count", "verified_zero"})

REQUIRED_SOURCE_FIELDS = (
    "source_id",
    "provider",
    "graduating_class",
    "geography_or_district",
    "source_title",
    "publisher",
    "publication_date",
    "source_url",
    "retrieval_date",
    "source_type",
    "completeness_scope",
    "complete_for_zero_inference",
    "zero_inference_scope",
    "parser_name",
    "parser_version",
    "source_hash",
    "hash_basis",
)


@dataclass(frozen=True)
class NmsfSource:
    source_id: str
    provider: str
    graduating_class: int
    geography_or_district: str
    source_title: str
    publisher: str
    publication_date: str
    source_url: str
    retrieval_date: str
    source_type: str
    completeness_scope: str
    complete_for_zero_inference: bool
    zero_inference_scope: str
    parser_name: str
    parser_version: str
    source_hash: str
    hash_basis: str
    archived_file_path: str
    archived_file_sha256: str
    reported_total: str
    reported_total_scope: str
    notes: str

    @property
    def source_scope(self) -> str:
        return self.geography_or_district


def read_source_manifest(path: Path) -> dict[str, NmsfSource]:
    data = _parse_manifest_yaml(path)
    _validate_statuses(data, path)
    raw_sources = data.get("sources", [])
    if not isinstance(raw_sources, list):
        raise ValueError(f"{path} sources must be a list")

    sources: dict[str, NmsfSource] = {}
    for index, raw_source in enumerate(raw_sources, start=1):
        if not isinstance(raw_source, dict):
            raise ValueError(f"{path} source entry {index} must be a mapping")
        missing = [field for field in REQUIRED_SOURCE_FIELDS if _blank(raw_source.get(field))]
        if missing:
            source_id = raw_source.get("source_id", f"entry {index}")
            raise ValueError(f"{path} source {source_id} missing {', '.join(missing)}")
        source = _source_from_mapping(raw_source, path)
        if source.source_id in sources:
            raise ValueError(f"{path} has duplicate source_id {source.source_id}")
        if source.complete_for_zero_inference and not source.zero_inference_scope:
            raise ValueError(f"{path} source {source.source_id} has blank zero inference scope")
        _validate_archived_file(source, path)
        if source.parser_name not in PARSER_REGISTRY_BY_NAME:
            raise ValueError(f"{path} source {source.source_id} has unknown parser {source.parser_name}")
        sources[source.source_id] = source
    return sources


def _validate_archived_file(source: NmsfSource, manifest_path: Path) -> None:
    if source.archived_file_path and not source.archived_file_sha256:
        raise ValueError(f"{manifest_path} source {source.source_id} has archived file without hash")
    if source.archived_file_sha256 and not source.archived_file_path:
        raise ValueError(f"{manifest_path} source {source.source_id} has archived hash without file")
    if not source.archived_file_path:
        return

    archive_path = Path(source.archived_file_path)
    if archive_path.is_absolute():
        raise ValueError(f"{manifest_path} source {source.source_id} archive path must be relative")

    candidates = [manifest_path.parent / archive_path]
    if len(manifest_path.parents) >= 3:
        candidates.append(manifest_path.parents[2] / archive_path)

    archive_file = next((candidate for candidate in candidates if candidate.exists()), None)
    if archive_file is None:
        raise ValueError(
            f"{manifest_path} source {source.source_id} archive file not found: {source.archived_file_path}"
        )

    digest = hashlib.sha256(archive_file.read_bytes()).hexdigest()
    if digest != source.archived_file_sha256:
        raise ValueError(
            f"{manifest_path} source {source.source_id} archive hash {source.archived_file_sha256} "
            f"does not match computed hash {digest}"
        )


def _source_from_mapping(raw: dict[str, Any], path: Path) -> NmsfSource:
    try:
        graduating_class = int(str(raw["graduating_class"]))
    except ValueError as exc:
        raise ValueError(
            f"{path} source {raw.get('source_id', '<unknown>')} has invalid graduating_class"
        ) from exc
    return NmsfSource(
        source_id=str(raw["source_id"]),
        provider=str(raw["provider"]),
        graduating_class=graduating_class,
        geography_or_district=str(raw["geography_or_district"]),
        source_title=str(raw["source_title"]),
        publisher=str(raw["publisher"]),
        publication_date=str(raw["publication_date"]),
        source_url=str(raw["source_url"]),
        retrieval_date=str(raw["retrieval_date"]),
        source_type=str(raw["source_type"]),
        completeness_scope=str(raw["completeness_scope"]),
        complete_for_zero_inference=_parse_bool(raw["complete_for_zero_inference"]),
        zero_inference_scope=str(raw["zero_inference_scope"]),
        parser_name=str(raw["parser_name"]),
        parser_version=str(raw["parser_version"]),
        source_hash=str(raw["source_hash"]),
        hash_basis=str(raw["hash_basis"]),
        archived_file_path=str(raw.get("archived_file_path") or ""),
        archived_file_sha256=str(raw.get("archived_file_sha256") or ""),
        reported_total=str(raw.get("reported_total") or ""),
        reported_total_scope=str(raw.get("reported_total_scope") or ""),
        notes=str(raw.get("notes") or ""),
    )


def _validate_statuses(data: dict[str, Any], path: Path) -> None:
    raw_statuses = data.get("observation_statuses", [])
    if not isinstance(raw_statuses, list):
        raise ValueError(f"{path} observation_statuses must be a list")
    statuses = set(str(status) for status in raw_statuses)
    if statuses != set(NMSF_OBSERVATION_STATUSES):
        missing = sorted(set(NMSF_OBSERVATION_STATUSES) - statuses)
        extra = sorted(statuses - set(NMSF_OBSERVATION_STATUSES))
        raise ValueError(f"{path} observation_statuses mismatch; missing={missing} extra={extra}")


def _parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text == "true":
        return True
    if text == "false":
        return False
    raise ValueError(f"Expected boolean value, got {value!r}")


def _blank(value: object) -> bool:
    return value is None or str(value).strip() == ""


def _parse_manifest_yaml(path: Path) -> dict[str, Any]:
    """Parse the constrained manifest YAML shape used by this repository."""

    data: dict[str, Any] = {}
    current_key = ""
    current_source: dict[str, Any] | None = None
    in_block_scalar = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if in_block_scalar and line.startswith(" "):
            continue
        in_block_scalar = False

        if not line.startswith(" "):
            key, value = _split_yaml_pair(stripped, path)
            current_key = key
            current_source = None
            if value == ">":
                data[key] = ""
                in_block_scalar = True
            elif value == "":
                data[key] = []
            else:
                data[key] = _parse_scalar(value)
            continue

        if current_key == "sources":
            if stripped.startswith("- "):
                current_source = {}
                data.setdefault("sources", []).append(current_source)
                remainder = stripped[2:].strip()
                if remainder:
                    key, value = _split_yaml_pair(remainder, path)
                    current_source[key] = _parse_scalar(value)
                continue
            if current_source is None:
                raise ValueError(f"{path} has source metadata before a source_id entry")
            key, value = _split_yaml_pair(stripped, path)
            current_source[key] = _parse_scalar(value)
        elif stripped.startswith("- "):
            data.setdefault(current_key, []).append(_parse_scalar(stripped[2:].strip()))
        else:
            raise ValueError(f"{path} has unsupported YAML line: {line}")
    return data


def _split_yaml_pair(text: str, path: Path) -> tuple[str, str]:
    if ":" not in text:
        raise ValueError(f"{path} has unsupported YAML line: {text}")
    key, value = text.split(":", 1)
    return key.strip(), value.strip()


def _parse_scalar(value: str) -> object:
    if value == "":
        return ""
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value
