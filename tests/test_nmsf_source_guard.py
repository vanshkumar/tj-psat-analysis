from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.seed_workbook import build_seed_outputs
from tj_psat_analysis.validation import nmsf_source_violations


class NmsfSourceGuardTest(unittest.TestCase):
    def test_seed_panel_has_statuses_and_no_unsourced_numeric_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            outputs = build_seed_outputs(
                ROOT / "docs" / "source_notes" / "tj psat investigation.xlsx",
                Path(tmp),
            )
            with outputs["panel_seed"].open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(nmsf_source_violations(rows), [])

    def test_numeric_nmsf_counts_require_source_metadata(self) -> None:
        rows = [
            {
                "school": "Example High",
                "class_year": "2025",
                "nmsf_count": "0",
                "nmsf_status": "verified_zero",
                "nmsf_source_title": "Complete List",
                "nmsf_source_url": "",
                "nmsf_source_date": "2024-09-01",
                "nmsf_source_hash": "abc123",
            }
        ]
        violations = nmsf_source_violations(rows)
        self.assertEqual(len(violations), 1)
        self.assertIn("nmsf_source_url", violations[0])


if __name__ == "__main__":
    unittest.main()
