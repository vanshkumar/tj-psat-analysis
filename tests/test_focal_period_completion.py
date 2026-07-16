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

        self.assertIn("| missing_source | 5 |", report)
        self.assertIn("| 2025 | LCPS | public | 4 |", report)
        self.assertIn("| 2025 | Falls Church City | public | 1 |", report)
        self.assertIn("| 2025 | LCPS | Woodgrove High School | public |", report)
        self.assertIn("| 2025 | Falls Church City | Meridian High School | public |", report)
        self.assertIn("## NMSC Virginia List Integration", report)
        self.assertIn("| 2023 | nmsc_virginia_2023_semifinalists | 400 |", report)
        self.assertIn("| 2024 | nmsc_virginia_2024_semifinalists | 470 |", report)
        self.assertIn("| 2026 | nmsc_virginia_2026_semifinalists | 494 |", report)
        self.assertIn("## Targeted Class 2025 Row Search", report)
        self.assertIn("Recovering the full Class 2025 statewide packet", report)
        self.assertIn("not required to close this public-source cleanup pass", report)
        self.assertIn("LCPS total-only coverage and Patch omission cannot support zero inference", report)
        self.assertIn("Official press release only; no school-by-school list.", report)
        self.assertIn("does not create `verified_count`, `verified_zero`, or Virginia-share rows", report)
        self.assertIn("## Broad Source-Discovery Log", report)
        self.assertIn("Class 2025 statewide list/total", report)
        self.assertIn("never use Patch absence for zero inference", report)
        self.assertIn(
            "optional future work, not a prerequisite for closing the public-source cleanup pass",
            report,
        )

    def test_targeted_class_2025_rows_remain_missing_source(self) -> None:
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

        combined_actions = " ".join(search.action for search in TARGETED_CLASS_2025_ROW_SEARCHES)
        self.assertIn("Retain as `missing_source`", combined_actions)
        self.assertNotIn("verified_zero", combined_actions)

    def test_nmsc_press_release_files_are_archived(self) -> None:
        for source in NMSC_PRESS_RELEASES:
            archive_path = ROOT / source.archived_file_path
            self.assertTrue(archive_path.exists(), source.archived_file_path)
            self.assertGreater(archive_path.stat().st_size, 100_000)

    def test_source_discovery_attempts_do_not_resolve_counts(self) -> None:
        self.assertGreaterEqual(len(SOURCE_DISCOVERY_ATTEMPTS), 4)

        combined_actions = " ".join(attempt.action for attempt in SOURCE_DISCOVERY_ATTEMPTS)
        self.assertIn("do not create counts or zeros", combined_actions)
        self.assertIn("not as evidence of zero semifinalists", combined_actions)


if __name__ == "__main__":
    unittest.main()
