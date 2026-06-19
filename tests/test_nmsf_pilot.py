from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.nmsf.pilot import (  # noqa: E402
    build_manual_review_queue,
    build_reconciliation_report,
    load_csv_rows,
    pilot_rows,
)
from tj_psat_analysis.nmsf.schema import read_source_manifest  # noqa: E402


class NmsfPilotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sources = read_source_manifest(ROOT / "data" / "sources" / "source_manifest.yml")
        cls.rows = pilot_rows(load_csv_rows(ROOT / "data" / "processed" / "nmsf_observations.csv"))
        cls.review_rows = build_manual_review_queue(cls.rows, sources=cls.sources, root=ROOT)
        cls.report = build_reconciliation_report(cls.rows, sources=cls.sources, root=ROOT)

    def test_pilot_filters_four_class_years(self) -> None:
        self.assertEqual(len(self.rows), 76 * 4)
        self.assertEqual({row["class_year"] for row in self.rows}, {"2023", "2024", "2025", "2026"})

    def test_review_queue_contains_missing_and_excluded_rows(self) -> None:
        issue_types = {row["issue_type"] for row in self.review_rows}
        self.assertIn("missing_school_year_source", issue_types)
        self.assertIn("excluded_tjhsst_resident_subset", issue_types)
        self.assertIn("excluded_tjhsst_former_pwcs_student", issue_types)
        self.assertIn("excluded_nonroster_school", issue_types)
        self.assertIn("source_incomplete_unattributed_total", issue_types)

        arlington_tech = [
            row
            for row in self.review_rows
            if row["school"] == "Arlington Tech" and row["source_id"] == "aps_2026_semifinalists"
        ][0]
        self.assertEqual(arlington_tech["nmsf_count"], "1")
        self.assertEqual(arlington_tech["nmsf_status"], "not_applicable")

        lcps_2025_total = [row for row in self.review_rows if row["source_id"] == "lcps_2025_semifinalists"][
            0
        ]
        self.assertEqual(lcps_2025_total["school"], "LCPS unattributed semifinalist total")
        self.assertEqual(lcps_2025_total["nmsf_count"], "57")
        self.assertEqual(lcps_2025_total["issue_type"], "source_incomplete_unattributed_total")

    def test_reconciliation_accounts_for_excluded_tj_subsets(self) -> None:
        self.assertIn("| aps_2023_semifinalists | 2023 | 17 | 15 | 2 | 17 | reconciled |", self.report)
        self.assertIn("| aps_2026_semifinalists | 2026 | 30 | 20 | 10 | 30 | reconciled |", self.report)
        self.assertIn("| fcps_2023_semifinalists | 2023 | 238 | 238 | 0 | 238 | reconciled |", self.report)
        self.assertIn("| lcps_2025_semifinalists | 2025 | 57 | 0 | 57 | 57 | reconciled |", self.report)
        self.assertIn("| lcps_2026_semifinalists | 2026 | 69 | 57 | 12 | 69 | reconciled |", self.report)
        self.assertIn("| pwcs_2023_semifinalists | 2023 | 3 | 2 | 1 | 3 | reconciled |", self.report)
        self.assertIn("| pwcs_2024_semifinalists | 2024 | 6 | 2 | 4 | 6 | reconciled |", self.report)
        self.assertIn("| pwcs_2025_semifinalists | 2025 | 7 | 6 | 1 | 7 | reconciled |", self.report)
        self.assertIn("| pwcs_2026_semifinalists | 2026 | 6 | 6 | 0 | 6 | reconciled |", self.report)
        self.assertIn(
            "| patch_fairfax_city_2025_semifinalists | 2025 | 17 | 3 | 14 | 17 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_mclean_2025_semifinalists | 2025 | 52 | 16 | 36 | 52 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_mclean_2026_semifinalists | 2026 | 65 | 22 | 43 | 65 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_fairfax_city_2026_semifinalists | 2026 | 15 | 2 | 13 | 15 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_vienna_2023_semifinalists | 2023 | 31 | 2 | 29 | 31 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_vienna_2024_semifinalists | 2024 | 31 | 4 | 27 | 31 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_vienna_2025_semifinalists | 2025 | 221 | 9 | 212 | 221 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_vienna_2026_semifinalists | 2026 | 53 | 5 | 48 | 53 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_arlington_2023_semifinalists | 2023 | 17 | 1 | 16 | 17 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_arlington_2024_semifinalists | 2024 | 23 | 16 | 7 | 23 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_arlington_2025_semifinalists | 2025 | 16 | 1 | 15 | 16 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_arlington_2026_semifinalists | 2026 | 22 | 1 | 21 | 22 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_ashburn_2025_semifinalists | 2025 | 46 | 45 | 1 | 46 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_ashburn_2026_semifinalists | 2026 | 59 | 1 | 58 | 59 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_falls_church_2024_semifinalists | 2024 | 11 | 5 | 6 | 11 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_manassas_2026_semifinalists | 2026 | 10 | 3 | 7 | 10 | reconciled |",
            self.report,
        )
        self.assertIn(
            "| patch_woodbridge_2025_semifinalists | 2025 | 8 | 2 | 6 | 8 | reconciled |",
            self.report,
        )


if __name__ == "__main__":
    unittest.main()
