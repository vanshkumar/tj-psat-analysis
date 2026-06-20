from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.nmsf.virginia_list import parse_virginia_list_text  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
