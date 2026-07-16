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
            49.848942598,
            places=6,
        )
        self.assertAlmostEqual(
            float(rows[2025]["tjhsst_share_of_balanced_public_nmsf_pct"]),
            32.270916335,
            places=6,
        )
        self.assertAlmostEqual(
            float(rows[2026]["tjhsst_share_of_balanced_public_nmsf_pct"]),
            33.531157270,
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

        self.assertAlmostEqual(raw_offset, 65.048543689, places=6)
        self.assertAlmostEqual(common_offset, 37.2820719996, places=6)
        self.assertAlmostEqual(extended_offset, 36.3269791144, places=6)
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

    def test_tied_rank_tables_have_deterministic_secondary_ordering(self) -> None:
        count_rows = read_rows(TABLES / "analysis_balanced_base_school_changes.csv")
        count_keys = [(-float(row["count_change_2025_2026"]), row["school_id"]) for row in count_rows]
        self.assertEqual(count_keys, sorted(count_keys))

        pooled_rows = read_rows(TABLES / "analysis_school_pooled_changes.csv")
        pooled_keys = [(-float(row["rate_point_change"]), row["school_id"]) for row in pooled_rows]
        self.assertEqual(pooled_keys, sorted(pooled_keys))

    def test_consolidated_report_preserves_claim_boundary(self) -> None:
        report = (ROOT / "reports" / "analysis.md").read_text(encoding="utf-8")
        self.assertIn("deconcentration away from TJHSST", report)
        self.assertIn("enrollment-standardized offset", report)
        self.assertIn("do not establish that the admissions policy caused", report)
        self.assertIn("median TJHSST student or academic culture declined", report)


if __name__ == "__main__":
    unittest.main()
