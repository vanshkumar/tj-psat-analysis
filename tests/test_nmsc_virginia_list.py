from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.nmsf.virginia_list import (  # noqa: E402
    parse_virginia_list_text,
    selection_unit_only_statewide_total_row,
)


class NmscVirginiaListParserTest(unittest.TestCase):
    def test_parser_counts_students_and_disambiguates_city_sensitive_schools(self) -> None:
        roster_rows = [
            {
                "school_id": "freedom_high_school_south_riding",
                "school": "Freedom High School (South Riding)",
            },
            {
                "school_id": "freedom_high_school_woodbridge",
                "school": "Freedom High School (Woodbridge)",
            },
            {
                "school_id": "basis_independent_mclean",
                "school": "BASIS Independent McLean",
            },
        ]
        rows, total = parse_virginia_list_text(
            lines=[
                "SEMIFINALISTS IN THE 2026 NATIONAL MERIT SCHOLARSHIP PROGRAM",
                "VIRGINIA",
                "SOUTH RIDING",
                "FREEDOM HIGH",
                "Example, Ada",
                "Sample, Grace",
                "WOODBRIDGE",
                "FREEDOM HIGH",
                "Example, Alan",
                "MCLEAN",
                "BASIS INDEPENDENT",
                "Example, Katherine",
            ],
            class_year=2026,
            school_roster_rows=roster_rows,
            school_alias_rows=[],
        )

        counts = {row.matched_school_id: row.nmsf_count for row in rows}
        self.assertEqual(total, 4)
        self.assertEqual(counts["freedom_high_school_south_riding"], 2)
        self.assertEqual(counts["freedom_high_school_woodbridge"], 1)
        self.assertEqual(counts["basis_independent_mclean"], 1)

    def test_selection_unit_only_row_preserves_missing_location_scope(self) -> None:
        row = selection_unit_only_statewide_total_row(
            {
                "class_year": "2025",
                "va_nmsf_selection_index_cutoff": "222",
                "va_nmsf_selection_index_cutoff_status": "source_backed_nmsc_guide",
                "statewide_nmsf_semifinalist_total": "394",
                "statewide_nmsf_semifinalist_total_status": "source_backed_state_selection_unit_total",
                "source_title": "Guide to the National Merit Scholarship Program - 2025 Program",
                "source_url": "https://example.com/guide.pdf",
                "source_date": "2025-01-18",
                "source_hash": "a" * 64,
                "nmsc_guide_virginia_school_count": "110",
                "reconciliation_status": "location_total_not_sourced",
                "reconciliation_notes": "No location list.",
            }
        )
        self.assertEqual(row["va_nmsf_selection_index_cutoff"], "222")
        self.assertEqual(row["statewide_nmsf_semifinalist_total"], "394")
        self.assertEqual(row["nmsc_guide_virginia_school_count"], "110")
        self.assertEqual(row["virginia_location_nmsf_semifinalist_total"], "")
        self.assertEqual(row["virginia_location_nmsf_semifinalist_total_status"], "not_sourced")


if __name__ == "__main__":
    unittest.main()
