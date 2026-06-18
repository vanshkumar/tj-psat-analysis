from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.nmsf.manual_counts import read_manual_nmsf_counts  # noqa: E402
from tj_psat_analysis.nmsf.observations import build_nmsf_observations  # noqa: E402
from tj_psat_analysis.nmsf.parsers import PARSER_REGISTRY_BY_NAME  # noqa: E402
from tj_psat_analysis.nmsf.schema import NMSF_OBSERVATION_STATUSES, read_source_manifest  # noqa: E402
from tj_psat_analysis.validation import nmsf_source_violations  # noqa: E402


class NmsfManifestAndObservationsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sources = read_source_manifest(ROOT / "data" / "sources" / "source_manifest.yml")
        cls.rows, cls.warnings = build_nmsf_observations(
            school_roster_csv=ROOT / "data" / "processed" / "school_roster.csv",
            school_aliases_csv=ROOT / "data" / "manual" / "school_aliases.csv",
            counts_csv=ROOT / "data" / "sources" / "nmsf_counts.csv",
            source_manifest_yml=ROOT / "data" / "sources" / "source_manifest.yml",
        )

    def _lookup(self, school_id: str, class_year: int) -> dict[str, str]:
        return [
            row for row in self.rows if row["school_id"] == school_id and row["class_year"] == str(class_year)
        ][0]

    def test_manifest_has_schema_fields_and_parser_names(self) -> None:
        self.assertEqual(
            set(self.sources),
            {
                "fcps_2024_semifinalists",
                "fcps_2025_semifinalists",
                "fcps_2026_semifinalists",
            },
        )
        for source in self.sources.values():
            self.assertIn(source.parser_name, PARSER_REGISTRY_BY_NAME)
            self.assertEqual(source.parser_name, "manual_reviewed_table")
            self.assertTrue(source.complete_for_zero_inference)
            self.assertEqual(source.zero_inference_scope, "fcps_public_high_schools_in_roster")
            self.assertEqual(len(source.source_hash), 64)
        self.assertIn("verified_count", NMSF_OBSERVATION_STATUSES)
        self.assertIn("missing_source", NMSF_OBSERVATION_STATUSES)

    def test_fixture_manual_counts_use_verified_count_status(self) -> None:
        records = read_manual_nmsf_counts(ROOT / "tests" / "fixtures" / "nmsf" / "manual_counts_fixture.csv")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].nmsf_status, "verified_count")

    def test_observation_layer_has_one_row_per_school_class_year(self) -> None:
        self.assertEqual(len(self.rows), 76 * 8)
        self.assertEqual(len({(row["school_id"], row["class_year"]) for row in self.rows}), len(self.rows))
        self.assertNotIn("grade11_enrollment", self.rows[0])
        self.assertNotIn("nmsf_per_100_grade11", self.rows[0])
        self.assertEqual(nmsf_source_violations(self.rows), [])

    def test_fcps_counts_and_verified_zero_inference(self) -> None:
        statuses = Counter(row["nmsf_status"] for row in self.rows)
        self.assertEqual(statuses["verified_count"], 53)
        self.assertEqual(statuses["verified_zero"], 22)
        self.assertEqual(statuses["not_operating"], 9)

        tj_2026 = self._lookup("thomas_jefferson_high_school_for_science_and_technology", 2026)
        self.assertEqual(tj_2026["nmsf_count"], "113")
        self.assertEqual(tj_2026["nmsf_status"], "verified_count")
        self.assertEqual(tj_2026["source_id"], "fcps_2026_semifinalists")

        robinson_2026 = self._lookup("robinson_secondary_school_hs", 2026)
        self.assertEqual(robinson_2026["nmsf_count"], "0")
        self.assertEqual(robinson_2026["nmsf_status"], "verified_zero")
        self.assertEqual(robinson_2026["observation_basis"], "complete_source_zero_inference")
        self.assertEqual(robinson_2026["source_id"], "fcps_2026_semifinalists")

    def test_non_fcps_rows_remain_missing_until_sourced(self) -> None:
        wakefield_2026 = self._lookup("wakefield_high_school", 2026)
        self.assertEqual(wakefield_2026["nmsf_count"], "")
        self.assertEqual(wakefield_2026["nmsf_status"], "missing_source")
        self.assertEqual(wakefield_2026["source_id"], "")


if __name__ == "__main__":
    unittest.main()
