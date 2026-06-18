from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.nmsf.manual_counts import (  # noqa: E402
    ManualNmsfCount,
    apply_manual_counts_to_panel,
    load_csv_rows,
    read_manual_nmsf_counts,
    source_hashes,
)
from tj_psat_analysis.seed_workbook import build_seed_outputs  # noqa: E402
from tj_psat_analysis.validation import nmsf_source_violations  # noqa: E402


class ManualNmsfCountsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.outputs = build_seed_outputs(
            ROOT / "docs" / "source_notes" / "tj psat investigation.xlsx",
            Path(cls.tmp.name),
        )
        cls.roster = load_csv_rows(cls.outputs["canonical_schools"])
        cls.panel = load_csv_rows(cls.outputs["panel_seed"])
        cls.records = read_manual_nmsf_counts(ROOT / "data" / "sources" / "nmsf_counts.csv")
        cls.applied = apply_manual_counts_to_panel(cls.panel, cls.roster, cls.records)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def _lookup(self, school_id: str, class_year: int) -> dict[str, str]:
        return [
            row
            for row in self.applied
            if row["school_id"] == school_id and row["class_year"] == str(class_year)
        ][0]

    def test_fcps_source_totals_match_release_titles(self) -> None:
        totals: dict[str, int] = {}
        for record in self.records:
            totals[record.source_id] = totals.get(record.source_id, 0) + record.nmsf_count

        self.assertEqual(totals["fcps_2024_semifinalists"], 264)
        self.assertEqual(totals["fcps_2025_semifinalists"], 191)
        self.assertEqual(totals["fcps_2026_semifinalists"], 262)

    def test_applied_counts_have_required_source_metadata_and_rates(self) -> None:
        tj_2025 = self._lookup("thomas_jefferson_high_school_for_science_and_technology", 2025)
        self.assertEqual(tj_2025["nmsf_count"], "81")
        self.assertEqual(tj_2025["nmsf_status"], "verified_count")
        self.assertEqual(
            tj_2025["nmsf_source_url"],
            "https://www.fcps.edu/news/191-fcps-students-named-2025-national-merit-semifinalists",
        )
        self.assertEqual(len(tj_2025["nmsf_source_hash"]), 64)
        self.assertEqual(tj_2025["nmsf_per_100_grade11"], "16.071429")

        langley_2025 = self._lookup("langley_high_school", 2025)
        self.assertEqual(langley_2025["nmsf_count"], "19")
        self.assertEqual(langley_2025["nmsf_per_100_grade11"], "3.531599")
        self.assertEqual(nmsf_source_violations(self.applied), [])

    def test_source_hashes_are_shared_by_rows_from_same_source(self) -> None:
        expected_hashes = source_hashes(self.records)
        tj_2024 = self._lookup("thomas_jefferson_high_school_for_science_and_technology", 2024)
        westfield_2024 = self._lookup("westfield_high_school", 2024)

        self.assertEqual(
            tj_2024["nmsf_source_hash"],
            expected_hashes["fcps_2024_semifinalists"],
        )
        self.assertEqual(tj_2024["nmsf_source_hash"], westfield_2024["nmsf_source_hash"])

    def test_unmatched_manual_school_name_fails_closed(self) -> None:
        bad_record = ManualNmsfCount(
            source_id="example_source",
            provider="fcps",
            class_year=2025,
            school_name_source="Not A Real TJ Area School",
            nmsf_count=1,
            nmsf_status="verified_count",
            source_title="Example Source",
            source_url="https://example.test/source",
            source_date="2025-09-01",
            source_scope="example",
            source_completeness="test only",
            source_notes="",
        )

        with self.assertRaisesRegex(ValueError, "does not match the canonical roster"):
            apply_manual_counts_to_panel(self.panel, self.roster, [bad_record])

    def test_manual_counts_csv_has_expected_columns(self) -> None:
        with (ROOT / "data" / "sources" / "nmsf_counts.csv").open(
            newline="",
            encoding="utf-8",
        ) as handle:
            reader = csv.DictReader(handle)
            self.assertIn("source_id", reader.fieldnames or [])
            self.assertIn("source_completeness", reader.fieldnames or [])


if __name__ == "__main__":
    unittest.main()
