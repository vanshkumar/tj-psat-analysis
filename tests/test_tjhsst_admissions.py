from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.tjhsst_admissions import build_admissions_outputs, sha256_file  # noqa: E402


class TjhsstAdmissionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        cls.workbook = (
            ROOT / "data" / "raw" / "admissions" / "fcps" / "tjhsst_class_2025_by_middle_school.xlsx"
        )
        cls.before_hash = sha256_file(cls.workbook)
        cls.outputs = build_admissions_outputs(
            workbook_path=cls.workbook,
            source_metadata_csv=ROOT / "data" / "sources" / "tjhsst_admissions_sources.csv",
            processed_dir=root / "processed",
            report_dir=root / "reports" / "data_quality",
        )
        with cls.outputs["source_school_csv"].open(newline="", encoding="utf-8") as handle:
            cls.rows = list(csv.DictReader(handle))
        with cls.outputs["summary_csv"].open(newline="", encoding="utf-8") as handle:
            cls.summary = list(csv.DictReader(handle))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def _school(self, name: str) -> dict[str, str]:
        return [row for row in self.rows if row["source_school_name"] == name][0]

    def test_source_integrity_and_row_count(self) -> None:
        self.assertEqual(self.before_hash, "948c91238520afab9ffe21af28d60b6c65fe11f5533428cd692b7f6698566911")
        self.assertEqual(sha256_file(self.workbook), self.before_hash)
        self.assertEqual(len(self.rows), 125)
        self.assertEqual(len({row["source_row_id"] for row in self.rows}), 125)

    def test_exact_and_suppressed_cells_are_distinct(self) -> None:
        carson = self._school("Carson Middle School")
        self.assertEqual((carson["applicants"], carson["waitpool"], carson["offered"]), ("245", "121", "42"))
        self.assertEqual(carson["offered_status"], "reported_exact")

        basis = self._school("BASIS McLean")
        self.assertEqual(basis["applicants"], "12")
        self.assertEqual(basis["waitpool"], "")
        self.assertEqual(basis["waitpool_status"], "suppressed_10_or_fewer")
        self.assertEqual(basis["waitpool_lower_bound"], "0")
        self.assertEqual(basis["waitpool_upper_bound"], "10")

    def test_coverage_and_gpa_summaries(self) -> None:
        coverage = {
            row["metric"]: row for row in self.summary if row["value_status"] == "cell_coverage_summary"
        }
        self.assertEqual(
            [
                (
                    coverage[key]["exact_rows"],
                    coverage[key]["suppressed_rows"],
                    coverage[key]["sum_of_exact_cells"],
                )
                for key in ("applicants", "waitpool", "offered")
            ],
            [("58", "67", "2832"), ("32", "93", "1083"), ("10", "115", "189")],
        )
        summaries = {row["metric"]: row for row in self.summary}
        self.assertEqual(summaries["waitpool_gpa_average"]["value"], "3.9302")
        self.assertEqual(summaries["waitpool_gpa_average"]["source_cell"], "H2")
        self.assertEqual(summaries["not_offered_gpa_average"]["value"], "3.8646")
        self.assertIn("not attributed", summaries["not_offered_gpa_average"]["notes"])


if __name__ == "__main__":
    unittest.main()
