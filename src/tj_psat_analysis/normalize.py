"""School-name normalization and alias helpers."""

from __future__ import annotations

import re
import unicodedata


def ascii_fold(value: str) -> str:
    """Return a simple ASCII representation for stable IDs and matching."""

    normalized = unicodedata.normalize("NFKD", value)
    return normalized.encode("ascii", "ignore").decode("ascii")


def slugify(value: str) -> str:
    folded = ascii_fold(value).lower()
    folded = re.sub(r"[^a-z0-9]+", "_", folded).strip("_")
    return folded or "unknown"


def normalize_school_name(value: str) -> str:
    """Normalize school names for conservative exact-style matching."""

    folded = ascii_fold(value).upper()
    folded = folded.replace("&", " AND ")
    folded = re.sub(r"\bSR\b", "SENIOR", folded)
    folded = re.sub(r"\bHS\b", "HIGH SCHOOL", folded)
    folded = re.sub(r"\bHIGH SCHOOL\b", "HIGH", folded)
    folded = re.sub(r"\bSECONDARY SCHOOL\b", "SECONDARY", folded)
    folded = re.sub(r"\bSENIOR HIGH\b", "HIGH", folded)
    folded = re.sub(r"[^A-Z0-9]+", " ", folded)
    return re.sub(r"\s+", " ", folded).strip()


def strip_parenthetical(value: str) -> str:
    return re.sub(r"\s*\([^)]*\)", "", value).strip()


def _expand_hs(value: str) -> str:
    return re.sub(r"\bHS\b\.?", "High School", value, flags=re.IGNORECASE)


def aliases_for_school(school: str, notes: str = "") -> list[str]:
    """Build auditable aliases without using them to invent data."""

    aliases: list[str] = []

    def add(candidate: str) -> None:
        cleaned = re.sub(r"\s+", " ", candidate).strip()
        if cleaned and cleaned not in aliases:
            aliases.append(cleaned)

    add(school)

    no_parens = strip_parenthetical(school)
    add(no_parens)

    if "High School" in no_parens:
        add(no_parens.replace("High School", "High"))

    if "Senior High School" in no_parens:
        add(no_parens.replace("Senior High School", "High School"))
        add(no_parens.replace("Senior High School", "High"))

    if "Secondary School" in no_parens:
        add(no_parens.replace("Secondary School", "Secondary"))

    if "Secondary Program" in no_parens:
        add(no_parens.replace("Secondary Program", "Secondary"))

    renamed = re.search(
        r"Renamed from\s+(.+?)(?:\s+in\s+\d{4}|\s*\(|$)",
        notes or "",
        re.IGNORECASE,
    )
    if renamed:
        prior = _expand_hs(renamed.group(1).strip())
        add(prior)
        if "High School" in prior:
            add(prior.replace("High School", "High"))

    return aliases
