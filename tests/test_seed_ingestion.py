from __future__ import annotations

import csv
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.constants import CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR
from tj_psat_analysis.seed_workbook import build_seed_outputs


class SeedIngestionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        workbook = ROOT / "docs" / "source_notes" / "tj psat investigation.xlsx"
        cls.outputs = build_seed_outputs(workbook, Path(cls.tmp.name))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def _read(self, key: str) -> list[dict[str, str]]:
        with self.outputs[key].open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    def test_roster_comes_from_raw_sheet_and_keeps_one_tj_row(self) -> None:
        roster = self._read("canonical_schools")
        self.assertEqual(len(roster), 76)
        tj_rows = [
            row
            for row in roster
            if row["school"] == "Thomas Jefferson High School for Science and Technology"
        ]
        self.assertEqual(len(tj_rows), 1)

    def test_class_year_mapping_is_complete(self) -> None:
        self.assertEqual(CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR[2019], "2017-18")
        self.assertEqual(CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR[2026], "2024-25")
        self.assertEqual(len(CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR), 8)

    def test_public_enrollment_maps_unambiguous_tj_value(self) -> None:
        rows = self._read("public_grade11_enrollment")
        tj_2025 = [
            row
            for row in rows
            if row["school"] == "Thomas Jefferson High School for Science and Technology"
            and row["class_year"] == "2025"
        ][0]
        self.assertEqual(tj_2025["grade11_school_year"], "2023-24")
        self.assertEqual(tj_2025["grade11_enrollment"], "504")
        self.assertEqual(tj_2025["enrollment_status"], "reported")

    def test_duplicate_freedom_rows_are_not_guessed(self) -> None:
        rows = self._read("public_grade11_enrollment")
        freedom_2025 = [
            row
            for row in rows
            if row["school"] in {
                "Freedom High School (South Riding)",
                "Freedom High School (Woodbridge)",
            }
            and row["class_year"] == "2025"
        ]
        self.assertEqual(len(freedom_2025), 2)
        self.assertEqual({row["enrollment_status"] for row in freedom_2025}, {"ambiguous_source_name"})
        self.assertEqual({row["grade11_enrollment"] for row in freedom_2025}, {""})

    def test_class_2026_public_enrollment_waits_for_2024_25_source(self) -> None:
        rows = self._read("public_grade11_enrollment")
        class_2026_statuses = {
            row["enrollment_status"] for row in rows if row["class_year"] == "2026"
        }
        self.assertEqual(class_2026_statuses, {"source_year_not_in_seed"})


if __name__ == "__main__":
    unittest.main()
