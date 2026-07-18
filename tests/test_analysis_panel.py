from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.analysis_panel import (  # noqa: E402
    build_analysis_outputs,
    final_panel_checks,
    load_csv_rows,
)


class AnalysisPanelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        cls.outputs = build_analysis_outputs(
            school_roster_csv=ROOT / "data" / "processed" / "school_roster.csv",
            nmsf_observations_csv=ROOT / "data" / "processed" / "nmsf_observations.csv",
            enrollment_panel_csv=ROOT / "data" / "processed" / "enrollment_panel.csv",
            class_year_mapping_csv=ROOT / "data" / "processed" / "class_year_mapping.csv",
            school_history_csv=ROOT / "data" / "manual" / "school_history.csv",
            statewide_totals_csv=ROOT / "data" / "sources" / "virginia_statewide_totals.csv",
            processed_dir=root / "processed",
            report_dir=root / "reports" / "data_quality",
        )
        cls.panel = load_csv_rows(cls.outputs["analysis_panel"])

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
        self.assertEqual(len({(row["school_id"], row["class_year"]) for row in self.panel}), len(self.panel))
        with self.outputs["analysis_panel"].open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            self.assertIn("nmsf_per_100_juniors", reader.fieldnames or [])
            self.assertIn("pathway_nmsf_per_100_juniors_covered", reader.fieldnames or [])

    def test_rate_calculation_uses_only_available_inputs(self) -> None:
        tj_2026 = self._lookup("thomas_jefferson_high_school_for_science_and_technology", 2026)
        expected = (int(tj_2026["nmsf_count"]) / int(tj_2026["grade11_enrollment"])) * 100
        self.assertEqual(tj_2026["rate_status"], "calculated")
        self.assertEqual(tj_2026["rate_input_compatible"], "true")
        self.assertEqual(tj_2026["nmsf_per_100_juniors"], f"{expected:.6f}")

        wakefield_2024 = self._lookup("wakefield_high_school", 2024)
        self.assertEqual(wakefield_2024["nmsf_status"], "verified_zero")
        self.assertEqual(wakefield_2024["nmsf_count"], "0")
        self.assertEqual(wakefield_2024["nmsf_source_id"], "nmsc_virginia_2024_semifinalists")
        self.assertEqual(wakefield_2024["rate_status"], "calculated")
        self.assertEqual(wakefield_2024["nmsf_missingness_flag"], "false")

        loudoun_private_2025 = self._lookup("loudoun_school_for_advanced_studies", 2025)
        self.assertEqual(loudoun_private_2025["nmsf_count"], "1")
        self.assertEqual(loudoun_private_2025["grade11_enrollment"], "")
        self.assertEqual(loudoun_private_2025["nmsf_per_100_juniors"], "")
        self.assertEqual(loudoun_private_2025["rate_status"], "missing_grade11_enrollment")
        self.assertEqual(loudoun_private_2025["denominator_gap_flag"], "true")

    def test_numeric_nmsf_counts_keep_source_provenance(self) -> None:
        numeric_rows = [row for row in self.panel if row["nmsf_count"]]
        self.assertGreater(len(numeric_rows), 0)
        for row in numeric_rows:
            self.assertTrue(row["nmsf_source_title"])
            self.assertTrue(row["nmsf_source_url"])
            self.assertTrue(row["nmsf_source_date"])
            self.assertEqual(len(row["nmsf_source_hash"]), 64)

    def test_pathway_aggregates_use_compatible_covered_rows(self) -> None:
        arlington_2026 = [
            row
            for row in self.panel
            if row["tj_pathway"] == "Arlington"
            and row["class_year"] == "2026"
            and row["nmsf_status"] != "not_operating"
            and row["enrollment_status"] != "not_operating"
        ]
        compatible = [row for row in arlington_2026 if row["rate_input_compatible"] == "true"]
        expected_count = sum(int(row["nmsf_count"]) for row in compatible)
        expected_enrollment = sum(int(row["grade11_enrollment"]) for row in compatible)
        expected_rate = (expected_count / expected_enrollment) * 100

        wakefield_2026 = self._lookup("wakefield_high_school", 2026)
        self.assertEqual(wakefield_2026["pathway_operating_school_rows"], str(len(arlington_2026)))
        self.assertEqual(wakefield_2026["pathway_compatible_school_rows"], str(len(compatible)))
        self.assertEqual(wakefield_2026["pathway_nmsf_count_covered"], str(expected_count))
        self.assertEqual(wakefield_2026["pathway_grade11_enrollment_covered"], str(expected_enrollment))
        self.assertEqual(wakefield_2026["pathway_nmsf_per_100_juniors_covered"], f"{expected_rate:.6f}")
        self.assertEqual(wakefield_2026["pathway_coverage_status"], "complete_compatible_coverage")
        self.assertEqual(wakefield_2026["pathway_has_complete_compatible_coverage"], "true")

    def test_history_pathway_and_placeholder_flags_are_explicit(self) -> None:
        meridian_2024 = self._lookup("meridian_high_school", 2024)
        self.assertEqual(meridian_2024["has_school_rename_flag"], "true")
        self.assertIn("rename", meridian_2024["row_history_flags"])
        self.assertEqual(
            meridian_2024["pathway_bucket_interpretation"],
            "analytical_geography_not_observed_admissions_pathway",
        )

        gainesville_2022 = self._lookup("gainesville_high_school", 2022)
        self.assertEqual(gainesville_2022["nmsf_status"], "not_operating")
        self.assertIn("pre_opening", gainesville_2022["row_history_flags"])

        potomac_2026 = self._lookup("potomac_school", 2026)
        self.assertEqual(
            potomac_2026["pathway_bucket_interpretation"],
            "nonpublic_unallocated_bucket_not_observed_admissions_pathway",
        )

        self.assertEqual(
            {row["va_nmsf_selection_index_cutoff_status"] for row in self.panel},
            {"not_sourced", "source_backed_nmsc_guide"},
        )
        self.assertEqual(self._lookup("wakefield_high_school", 2025)["va_nmsf_selection_index_cutoff"], "222")
        self.assertEqual(
            {row["statewide_nmsf_semifinalist_total_status"] for row in self.panel},
            {"not_sourced", "source_backed_state_selection_unit_total"},
        )
        self.assertEqual(
            self._lookup("wakefield_high_school", 2024)["statewide_nmsf_semifinalist_total"], "467"
        )
        self.assertEqual(
            self._lookup("wakefield_high_school", 2024)["virginia_location_nmsf_semifinalist_total"],
            "470",
        )
        self.assertEqual(
            self._lookup("wakefield_high_school", 2024)["state_selection_unit_reconciliation_status"],
            "partial_scope_reconciliation",
        )
        wakefield_2025 = self._lookup("wakefield_high_school", 2025)
        self.assertEqual(wakefield_2025["statewide_nmsf_semifinalist_total"], "394")
        self.assertEqual(wakefield_2025["nmsc_guide_virginia_school_count"], "110")
        self.assertEqual(wakefield_2025["virginia_location_nmsf_semifinalist_total"], "")
        self.assertEqual(wakefield_2025["virginia_location_nmsf_semifinalist_total_status"], "not_sourced")
        self.assertEqual(
            wakefield_2025["statewide_nmsf_semifinalist_total_source_hash"],
            "908235a4c5311ec23aed1d9a42d4835d29b860d0575f23912b2dc1a784c5328b",
        )
        self.assertEqual(
            {row["denominator_type"] for row in self.panel},
            {"grade11_enrollment_outcome_denominator"},
        )
        self.assertEqual(
            {row["admissions_seat_allocation_input_status"] for row in self.panel},
            {"not_included_requires_sourced_8th_grade_population"},
        )

    def test_final_checks_report_passes(self) -> None:
        checks = final_panel_checks(self.panel)
        self.assertEqual({row["status"] for row in checks}, {"pass"})
        report = self.outputs["final_panel_checks_md"].read_text(encoding="utf-8")
        self.assertIn("Pathway aggregates are covered-subset totals", report)
        self.assertIn("Virginia NMSF Selection Index cutoff", report)
        self.assertIn("Grade-11 enrollment is an outcome denominator", report)


if __name__ == "__main__":
    unittest.main()
