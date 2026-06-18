from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.constants import CLASS_YEAR_TO_GRADE11_SCHOOL_YEAR
from tj_psat_analysis.seed_workbook import build_seed_outputs, sha256_file


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
            if row["school"]
            in {
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
        class_2026_statuses = {row["enrollment_status"] for row in rows if row["class_year"] == "2026"}
        self.assertEqual(class_2026_statuses, {"source_year_not_in_seed"})

    def test_pre_opening_school_years_are_not_operating(self) -> None:
        panel = self._read("panel_seed")
        independence_2020 = [
            row
            for row in panel
            if row["school_id"] == "independence_high_school" and row["class_year"] == "2020"
        ][0]
        gainesville_2022 = [
            row
            for row in panel
            if row["school_id"] == "gainesville_high_school" and row["class_year"] == "2022"
        ][0]

        self.assertEqual(independence_2020["nmsf_count"], "")
        self.assertEqual(independence_2020["nmsf_status"], "not_operating")
        self.assertEqual(independence_2020["grade11_enrollment"], "")
        self.assertEqual(independence_2020["enrollment_status"], "not_operating")
        self.assertEqual(gainesville_2022["nmsf_status"], "not_operating")
        self.assertEqual(gainesville_2022["enrollment_status"], "not_operating")

    def test_milestone_one_deliverables_are_generated_without_mutating_workbook(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workbook = ROOT / "docs" / "source_notes" / "tj psat investigation.xlsx"
            before_hash = sha256_file(workbook)
            outputs = build_seed_outputs(
                workbook_path=workbook,
                output_dir=root / "interim",
                processed_dir=root / "processed",
                report_dir=root / "reports" / "data_quality",
                manual_dir=root / "manual",
            )
            after_hash = sha256_file(workbook)

            self.assertEqual(before_hash, after_hash)
            self.assertEqual(sha256_file(outputs["manual_workbook"]), before_hash)
            self.assertTrue(outputs["schools"].exists())
            self.assertTrue(outputs["public_enrollment"].exists())
            self.assertTrue(outputs["class_year_mapping"].exists())
            self.assertTrue(outputs["workbook_ingestion_report"].exists())

            with outputs["schools"].open(newline="", encoding="utf-8") as handle:
                schools = list(csv.DictReader(handle))
            with outputs["class_year_mapping"].open(newline="", encoding="utf-8") as handle:
                mapping = list(csv.DictReader(handle))
            report = outputs["workbook_ingestion_report"].read_text(encoding="utf-8")

        self.assertEqual(len(schools), 76)
        self.assertEqual(len({row["school_id"] for row in schools}), 76)
        self.assertEqual(mapping[0]["class_year"], "2019")
        self.assertEqual(mapping[-1]["grade11_school_year"], "2024-25")
        self.assertIn("`nsmf 2019` read by parser", report)
        self.assertIn("ambiguous_source_name", report)


if __name__ == "__main__":
    unittest.main()
