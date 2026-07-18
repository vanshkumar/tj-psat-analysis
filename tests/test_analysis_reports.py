from __future__ import annotations

import csv
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "reports" / "tables"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class AnalysisReportsTest(unittest.TestCase):
    def test_public_concentration_quantifies_deconcentration(self) -> None:
        rows = {
            int(row["class_year"]): row for row in read_rows(TABLES / "analysis_public_concentration.csv")
        }

        self.assertAlmostEqual(
            float(rows[2024]["tjhsst_share_of_balanced_public_nmsf_pct"]),
            49.107143,
            places=6,
        )
        self.assertAlmostEqual(
            float(rows[2025]["tjhsst_share_of_balanced_public_nmsf_pct"]),
            31.889764,
            places=6,
        )
        self.assertAlmostEqual(
            float(rows[2026]["tjhsst_share_of_balanced_public_nmsf_pct"]),
            32.753623,
            places=6,
        )

    def test_rate_standardized_offset_is_smaller_than_raw_count_offset(self) -> None:
        standardized = {
            row["scenario"]: row
            for row in read_rows(TABLES / "analysis_rate_standardized_offset_decomposition.csv")
        }
        raw = read_rows(TABLES / "analysis_offset_decomposition.csv")[0]
        common = standardized["common_2023_2024_baseline"]
        extended = standardized["extended_tjhsst_2019_2024_baseline"]

        raw_offset = float(raw["base_gain_as_pct_of_tj_decline"])
        common_offset = float(common["base_excess_as_pct_of_tjhsst_shortfall"])
        extended_offset = float(extended["base_excess_as_pct_of_tjhsst_shortfall"])

        self.assertAlmostEqual(raw_offset, 65.048544, places=6)
        self.assertAlmostEqual(common_offset, 37.432683, places=6)
        self.assertAlmostEqual(extended_offset, 36.473732, places=6)
        self.assertLess(common_offset, raw_offset)
        self.assertGreater(
            float(common["balanced_public_shortfall_vs_component_baseline"]),
            0,
        )

    def test_standardized_decomposition_reconciles(self) -> None:
        rows = read_rows(TABLES / "analysis_rate_standardized_offset_decomposition.csv")
        for row in rows:
            expected_public = float(row["component_standardized_public_expected_post_nmsf"])
            observed_public = float(row["balanced_public_observed_post_nmsf"])
            shortfall = float(row["balanced_public_shortfall_vs_component_baseline"])
            self.assertTrue(math.isclose(expected_public - observed_public, shortfall, abs_tol=1e-6))

    def test_virginia_participation_benchmark_is_source_backed_and_nearly_flat(self) -> None:
        rows = read_rows(TABLES / "analysis_psat_participation_benchmark.csv")
        self.assertEqual([int(row["class_year"]) for row in rows], [2023, 2024, 2025, 2026])
        self.assertEqual(
            [int(row["reported_participation_rate_pct"]) for row in rows],
            [50, 50, 49, 49],
        )
        self.assertTrue(
            all(row["source_url"].startswith("https://reports.collegeboard.org/") for row in rows)
        )

        pre_takers = sum(int(row["virginia_psat_nmsqt_takers"]) for row in rows[:2])
        pre_enrollment = sum(int(row["virginia_grade11_enrollment"]) for row in rows[:2])
        post_takers = sum(int(row["virginia_psat_nmsqt_takers"]) for row in rows[2:])
        post_enrollment = sum(int(row["virginia_grade11_enrollment"]) for row in rows[2:])
        ratio = (post_takers / post_enrollment) / (pre_takers / pre_enrollment)
        self.assertAlmostEqual(ratio, 0.975900581, places=6)

    def test_participation_grid_preserves_pooled_qualitative_findings(self) -> None:
        rows = read_rows(TABLES / "analysis_participation_sensitivity.csv")
        benchmark = [row for row in rows if row["scenario_family"] == "statewide_benchmark"]
        grid = [row for row in rows if row["scenario_family"] == "plus_or_minus_10pct_group_specific_grid"]
        self.assertEqual(len(benchmark), 1)
        self.assertEqual(len(grid), 25)
        for row in grid:
            self.assertEqual(row["tjhsst_participant_yield_below_pre"], "True")
            self.assertEqual(row["base_public_participant_yield_above_pre"], "True")
            self.assertEqual(row["partial_offset"], "True")
            self.assertEqual(row["balanced_public_shortfall_positive"], "True")

        offsets = [float(row["base_excess_as_pct_of_tjhsst_shortfall"]) for row in grid]
        self.assertAlmostEqual(min(offsets), 10.596271, places=6)
        self.assertAlmostEqual(max(offsets), 80.717783, places=6)
        self.assertAlmostEqual(
            float(benchmark[0]["base_excess_as_pct_of_tjhsst_shortfall"]),
            45.895610,
            places=6,
        )

    def test_participation_break_even_thresholds_identify_fragile_claims(self) -> None:
        rows = {row["finding"]: row for row in read_rows(TABLES / "analysis_participation_break_even.csv")}
        self.assertAlmostEqual(
            float(
                rows["TJHSST pooled participant-yield decline eliminated"][
                    "required_relative_participation_change_pct"
                ]
            ),
            -42.630459,
            places=6,
        )
        self.assertAlmostEqual(
            float(
                rows["Combined-public component-standardized shortfall eliminated"][
                    "required_relative_participation_change_pct"
                ]
            ),
            -13.087150,
            places=6,
        )
        self.assertAlmostEqual(
            float(
                rows["Combined-public Class 2026 gap from Class 2024 eliminated"][
                    "required_relative_participation_change_pct"
                ]
            ),
            -0.995798,
            places=6,
        )

    def test_tied_rank_tables_have_deterministic_secondary_ordering(self) -> None:
        count_rows = read_rows(TABLES / "analysis_balanced_base_school_changes.csv")
        count_keys = [(-float(row["count_change_2025_2026"]), row["school_id"]) for row in count_rows]
        self.assertEqual(count_keys, sorted(count_keys))

        pooled_rows = read_rows(TABLES / "analysis_school_pooled_changes.csv")
        pooled_keys = [(-float(row["rate_point_change"]), row["school_id"]) for row in pooled_rows]
        self.assertEqual(pooled_keys, sorted(pooled_keys))

    def test_class_2025_state_normalization_uses_official_nmsc_guide(self) -> None:
        rows = [
            row
            for row in read_rows(TABLES / "analysis_state_normalization_supplemental.csv")
            if row["class_year"] == "2025"
        ]
        public = [row for row in rows if row["group"] == "Balanced public including TJHSST"][0]
        private = [row for row in rows if row["group"] == "Balanced private schools"][0]
        self.assertEqual(public["virginia_statewide_semifinalist_total"], "394.000000")
        self.assertEqual(public["state_total_status"], "source_backed_state_selection_unit_total")
        self.assertIn("web.archive.org", public["state_total_source_url"])
        self.assertTrue(public["group_share_of_statewide_total_pct"])
        self.assertEqual(private["group_share_of_statewide_total_pct"], "")
        self.assertEqual(
            private["selection_unit_numerator_scope_status"],
            "boarding_adjustment_not_reconciled_without_location_list",
        )

    def test_partial_class_2025_admissions_source_is_documented(self) -> None:
        rows = {
            row["metric"]: row
            for row in read_rows(TABLES / "analysis_tjhsst_class_2025_admissions_coverage.csv")
        }
        self.assertEqual(rows["applicants"]["exact_rows"], "58")
        self.assertEqual(rows["offered"]["suppressed_rows"], "115")
        report = (ROOT / "reports" / "analysis.md").read_text(encoding="utf-8")
        self.assertIn("FCPS-origin source-school workbook", report)
        self.assertIn("suppressed as 10 or fewer", report)

    def test_consolidated_report_preserves_claim_boundary(self) -> None:
        report = (ROOT / "reports" / "analysis.md").read_text(encoding="utf-8")
        self.assertIn("deconcentration away from TJHSST", report)
        self.assertIn("enrollment-standardized offset", report)
        self.assertIn("PSAT participation sensitivity", report)
        self.assertIn("Every combination in the wider group-specific ±10% grid", report)
        self.assertIn("do not establish that the admissions policy caused", report)
        self.assertIn("median TJHSST student or academic culture declined", report)

    def test_conclusion_graphic_is_png_only(self) -> None:
        graphic = ROOT / "reports" / "conclusion_graphic.png"
        self.assertTrue(graphic.is_file())
        self.assertTrue(graphic.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertFalse((ROOT / "reports" / "conclusion_graphic.svg").exists())


if __name__ == "__main__":
    unittest.main()
