from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.enrollment import build_enrollment_outputs, load_csv_rows  # noqa: E402


class EnrollmentPanelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        cls.outputs = build_enrollment_outputs(
            school_roster_csv=ROOT / "data" / "processed" / "school_roster.csv",
            public_seed_csv=ROOT / "data" / "processed" / "public_enrollment.csv",
            public_supplement_csv=ROOT / "data" / "interim" / "public_grade11_enrollment_nces_supplement.csv",
            public_2024_25_csv=ROOT / "data" / "interim" / "public_grade11_enrollment_2024_25.csv",
            private_pss_csv=ROOT / "data" / "interim" / "private_grade11_enrollment.csv",
            private_pss_locator_csv=ROOT
            / "data"
            / "interim"
            / "private_grade11_enrollment_pss_locator_2023_24.csv",
            targeted_supplement_csv=ROOT / "data" / "sources" / "targeted_grade11_enrollment.csv",
            processed_dir=root / "processed",
            report_dir=root / "reports" / "data_quality",
        )
        cls.panel = load_csv_rows(cls.outputs["enrollment_panel"])
        cls.coverage = load_csv_rows(cls.outputs["enrollment_coverage_csv"])

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def _lookup(self, school_id: str, class_year: int) -> dict[str, str]:
        return [
            row
            for row in self.panel
            if row["school_id"] == school_id and row["class_year"] == str(class_year)
        ][0]

    def test_panel_has_one_row_per_roster_school_class_year(self) -> None:
        self.assertEqual(len(self.panel), 76 * 8)
        self.assertEqual(len(self.coverage), len(self.panel))
        self.assertEqual(len({(row["school_id"], row["class_year"]) for row in self.panel}), len(self.panel))

    def test_public_seed_and_2024_25_ccd_rows_are_preserved(self) -> None:
        tj_2025 = self._lookup("thomas_jefferson_high_school_for_science_and_technology", 2025)
        self.assertEqual(tj_2025["grade11_enrollment"], "504")
        self.assertEqual(tj_2025["enrollment_status"], "reported")
        self.assertEqual(tj_2025["enrollment_source_file"], "")

        tj_2026 = self._lookup("thomas_jefferson_high_school_for_science_and_technology", 2026)
        self.assertEqual(tj_2026["enrollment_status"], "reported")
        self.assertTrue(tj_2026["grade11_enrollment"].isdigit())
        self.assertIn("ccd_sch_052_2425", tj_2026["enrollment_source_url"])
        self.assertEqual(len(tj_2026["enrollment_source_hash"]), 64)

    def test_public_supplement_resolves_freedom_high_ambiguity(self) -> None:
        south_riding_2025 = self._lookup("freedom_high_school_south_riding", 2025)
        self.assertEqual(south_riding_2025["enrollment_status"], "reported")
        self.assertTrue(south_riding_2025["grade11_enrollment"].isdigit())
        self.assertEqual(south_riding_2025["nces_school_id"], "510225002447")
        self.assertIn("ccd_sch_052_2324", south_riding_2025["enrollment_source_url"])

        woodbridge_2025 = self._lookup("freedom_high_school_woodbridge", 2025)
        self.assertEqual(woodbridge_2025["enrollment_status"], "reported")
        self.assertTrue(woodbridge_2025["grade11_enrollment"].isdigit())
        self.assertEqual(woodbridge_2025["nces_school_id"], "510313002458")
        self.assertIn("ccd_sch_052_2324", woodbridge_2025["enrollment_source_url"])

    def test_private_pss_uses_p290_and_preserves_imputation_flag(self) -> None:
        trinity_2023 = self._lookup("trinity_christian_school", 2023)
        self.assertEqual(trinity_2023["grade11_enrollment"], "65")
        self.assertEqual(trinity_2023["enrollment_status"], "reported")
        self.assertEqual(trinity_2023["enrollment_source_variable"], "P290")
        self.assertEqual(trinity_2023["pss_imputation_flag"], "0")
        self.assertEqual(trinity_2023["pss_ppin"], "K9306124")

        flint_2024 = self._lookup("flint_hill_school", 2024)
        self.assertEqual(flint_2024["grade11_enrollment"], "")
        self.assertEqual(flint_2024["enrollment_status"], "private_pss_not_survey_year")

    def test_private_pss_locator_supplies_class_2025_denominators(self) -> None:
        trinity_2025 = self._lookup("trinity_christian_school", 2025)
        self.assertEqual(trinity_2025["grade11_enrollment"], "67")
        self.assertEqual(trinity_2025["enrollment_status"], "reported")
        self.assertEqual(trinity_2025["enrollment_source_variable"], "PSS_ENROLL_11")
        self.assertIn("school_detail.asp", trinity_2025["enrollment_source_url"])
        self.assertEqual(len(trinity_2025["enrollment_source_hash"]), 64)
        self.assertEqual(trinity_2025["pss_imputation_flag"], "not_available_locator")

        loudoun_private_2025 = self._lookup("loudoun_school_for_advanced_studies", 2025)
        self.assertEqual(loudoun_private_2025["grade11_enrollment"], "")
        self.assertEqual(loudoun_private_2025["enrollment_status"], "ambiguous_pss_id")

        flint_hill_2025 = self._lookup("flint_hill_school", 2025)
        self.assertEqual(flint_hill_2025["grade11_enrollment"], "")
        self.assertEqual(flint_hill_2025["enrollment_status"], "locator_search_not_found")

    def test_targeted_supplements_fill_exact_mapped_year_denominators(self) -> None:
        expected = {
            ("h_b_woodlawn_secondary_program", 2023): "109",
            ("h_b_woodlawn_secondary_program", 2024): "109",
            ("h_b_woodlawn_secondary_program", 2025): "115",
            ("h_b_woodlawn_secondary_program", 2026): "110",
            ("loudoun_school_for_advanced_studies", 2023): "11",
            ("basis_independent_mclean", 2025): "29",
            ("basis_independent_mclean", 2026): "40",
            ("trinity_christian_school", 2024): "91",
            ("immanuel_christian_high_school", 2026): "49",
        }
        for (school_id, class_year), count in expected.items():
            row = self._lookup(school_id, class_year)
            self.assertEqual(row["grade11_enrollment"], count)
            self.assertEqual(row["enrollment_status"], "reported")
            self.assertEqual(len(row["enrollment_source_hash"]), 64)

        self.assertEqual(
            self._lookup("loudoun_school_for_advanced_studies", 2023)["pss_ppin"],
            "A1703674;A1992096",
        )
        self.assertIn(
            "basisindependent.com",
            self._lookup("basis_independent_mclean", 2026)["enrollment_source_url"],
        )
        self.assertIn(
            "tcsfairfax.org",
            self._lookup("trinity_christian_school", 2024)["enrollment_source_url"],
        )
        self.assertIn(
            "icsva.org",
            self._lookup("immanuel_christian_high_school", 2026)["enrollment_source_url"],
        )

    def test_missingness_and_not_operating_are_distinct(self) -> None:
        gainesville_2022 = self._lookup("gainesville_high_school", 2022)
        self.assertEqual(gainesville_2022["grade11_enrollment"], "")
        self.assertEqual(gainesville_2022["enrollment_status"], "not_operating")

        loudoun_private_2023 = self._lookup("loudoun_school_for_advanced_studies", 2023)
        self.assertEqual(loudoun_private_2023["grade11_enrollment"], "11")
        self.assertEqual(loudoun_private_2023["enrollment_status"], "reported")

    def test_reports_document_no_adjacent_year_estimates(self) -> None:
        report = self.outputs["enrollment_coverage_md"].read_text(encoding="utf-8")
        self.assertIn("No enrollment value is estimated from adjacent years.", report)
        self.assertIn("PSS non-survey years without a public-use or locator source row remain blank", report)
        self.assertIn("PSS_ENROLL_11", report)
        self.assertIn("Status Counts", report)

    def test_generated_coverage_csv_has_expected_columns(self) -> None:
        with self.outputs["enrollment_coverage_csv"].open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            self.assertIn("has_grade11_enrollment", reader.fieldnames or [])
            self.assertIn("enrollment_status", reader.fieldnames or [])


if __name__ == "__main__":
    unittest.main()
