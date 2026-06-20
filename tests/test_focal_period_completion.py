from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.nmsf.completion import (  # noqa: E402
    NMSC_PRESS_RELEASES,
    SOURCE_DISCOVERY_ATTEMPTS,
    build_focal_period_completion_report,
)


class FocalPeriodCompletionTest(unittest.TestCase):
    def test_report_preserves_missing_rows_and_nmsc_limitation(self) -> None:
        report = build_focal_period_completion_report(
            observations_csv=ROOT / "data" / "processed" / "nmsf_observations_2023_2026.csv",
            root=ROOT,
        )

        self.assertIn("| missing_source | 37 |", report)
        self.assertIn("| 2025 | LCPS | public | 4 |", report)
        self.assertIn("| 2026 | FCPS | Trinity School at Meadow View | private |", report)
        self.assertIn("Official press release only; no school-by-school list.", report)
        self.assertIn("does not create `verified_count`, `verified_zero`, or Virginia-share rows", report)
        self.assertIn("## Broad Source-Discovery Log", report)
        self.assertIn("No complete public Virginia mirror was located through broad web search.", report)
        self.assertIn("never use Patch absence for zero inference", report)

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
