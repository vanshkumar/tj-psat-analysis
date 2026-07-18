from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.nmsf.completion import (  # noqa: E402
    NMSC_PRESS_RELEASES,
    SOURCE_DISCOVERY_ATTEMPTS,
    TARGETED_CLASS_2025_ROW_SEARCHES,
    build_focal_period_completion_report,
)


class FocalPeriodCompletionTest(unittest.TestCase):
    def test_report_preserves_missing_rows_and_nmsc_limitation(self) -> None:
        report = build_focal_period_completion_report(
            observations_csv=ROOT / "data" / "processed" / "nmsf_observations_2023_2026.csv",
            root=ROOT,
        )

        self.assertIn("| missing_source | 1 |", report)
        self.assertNotIn("| 2025 | LCPS | public |", report)
        self.assertIn("| 2025 | Falls Church City | public | 1 |", report)
        self.assertNotIn("| 2025 | LCPS | Woodgrove High School | public |", report)
        self.assertIn("| 2025 | Falls Church City | Meridian High School | public |", report)
        self.assertIn("## NMSC Virginia List Integration", report)
        self.assertIn("| 2023 | 400 | 397 | nmsc_virginia_2023_semifinalists |", report)
        self.assertIn("| 2024 | 470 | 467 | nmsc_virginia_2024_semifinalists |", report)
        self.assertIn("| 2025 | not sourced | 394 |", report)
        self.assertIn("| 2026 | 494 | 489 | nmsc_virginia_2026_semifinalists |", report)
        self.assertIn("Virginia-location media-list totals (400, 470, and 494)", report)
        self.assertIn("official NMSC Virginia selection-unit totals (397, 467, 394, and 489)", report)
        self.assertIn("These are different scopes, not competing estimates", report)
        self.assertIn("scope-matched numerators", report)
        self.assertIn("official Class 2025 state-selection-unit total is now source-backed", report)
        self.assertIn("## Targeted Class 2025 Row Search", report)
        self.assertIn("42 directly school-attributed LCPS-public identities", report)
        self.assertIn("15 official TJHSST identities", report)
        self.assertIn("four LCPS rows as verified zeros", report)
        self.assertIn("four reported finalists do not establish the semifinalist count", report)
        self.assertIn("Official press release only; no school-by-school list.", report)
        self.assertIn("does not create `verified_count`, `verified_zero`, or Virginia-share rows", report)
        self.assertIn("## Broad Source-Discovery Log", report)
        self.assertIn("Class 2025 has an official selection-unit denominator", report)
        self.assertIn("never use Patch absence for zero inference", report)
        self.assertIn(
            "deleted Class 2025 Virginia gallery images",
            report,
        )

    def test_targeted_class_2025_rows_record_four_lcps_zeros_and_one_meridian_gap(self) -> None:
        self.assertEqual(len(TARGETED_CLASS_2025_ROW_SEARCHES), 5)

        schools = {search.school for search in TARGETED_CLASS_2025_ROW_SEARCHES}
        self.assertEqual(
            schools,
            {
                "Meridian High School",
                "Loudoun Valley High School",
                "Park View High School",
                "Tuscarora High School",
                "Woodgrove High School",
            },
        )

        actions = {search.school: search.action for search in TARGETED_CLASS_2025_ROW_SEARCHES}
        self.assertEqual(actions["Meridian High School"], "Retain as `missing_source`; no zero inference.")
        for school in schools - {"Meridian High School"}:
            self.assertIn("verified_zero", actions[school])

    def test_nmsc_press_release_files_are_archived(self) -> None:
        for source in NMSC_PRESS_RELEASES:
            archive_path = ROOT / source.archived_file_path
            self.assertTrue(archive_path.exists(), source.archived_file_path)
            self.assertGreater(archive_path.stat().st_size, 100_000)

    def test_source_discovery_attempts_distinguish_archive_absence_from_reconciliation(self) -> None:
        self.assertGreaterEqual(len(SOURCE_DISCOVERY_ATTEMPTS), 4)

        combined_actions = " ".join(attempt.action for attempt in SOURCE_DISCOVERY_ATTEMPTS)
        self.assertIn("do not create counts or zeros", combined_actions)
        self.assertIn("not as evidence of zero semifinalists", combined_actions)
        self.assertIn("verify zero for the four absent", combined_actions)


if __name__ == "__main__":
    unittest.main()
