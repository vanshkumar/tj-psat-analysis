from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.school_roster import build_school_roster_outputs  # noqa: E402


class SchoolRosterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        cls.outputs = build_school_roster_outputs(
            workbook_path=ROOT / "docs" / "source_notes" / "tj psat investigation.xlsx",
            processed_dir=root / "processed",
            manual_dir=root / "manual",
            report_dir=root / "reports" / "data_quality",
            nces_id_csv=ROOT / "data" / "manual" / "public_school_nces_ids.csv",
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def _read(self, key: str) -> list[dict[str, str]]:
        with self.outputs[key].open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    def test_public_roster_has_nces_ids_and_distinguishes_freedom_high_schools(self) -> None:
        roster = self._read("school_roster")
        self.assertEqual(len(roster), 76)

        public_rows = [row for row in roster if row["sector"] == "public"]
        self.assertEqual(len(public_rows), 60)
        self.assertEqual({row["identifier_status"] for row in public_rows}, {"matched_2023_24_ccd"})

        freedom = {
            row["school_id"]: row
            for row in roster
            if row["school_id"] in {"freedom_high_school_south_riding", "freedom_high_school_woodbridge"}
        }
        self.assertEqual(freedom["freedom_high_school_south_riding"]["nces_lea_id"], "5102250")
        self.assertEqual(freedom["freedom_high_school_woodbridge"]["nces_lea_id"], "5103130")
        self.assertNotEqual(
            freedom["freedom_high_school_south_riding"]["nces_school_id"],
            freedom["freedom_high_school_woodbridge"]["nces_school_id"],
        )

    def test_private_school_pathways_are_residency_based_from_policy_pdf(self) -> None:
        roster = self._read("school_roster")
        private_rows = [row for row in roster if row["sector"] == "private"]
        self.assertEqual(len(private_rows), 16)
        self.assertEqual({row["tj_pathway"] for row in private_rows}, {"Residency-based private"})
        self.assertEqual(
            {row["pathway_status"] for row in private_rows},
            {"residency_based_private_applicant"},
        )
        self.assertEqual(
            {row["pathway_assignment_method"] for row in private_rows},
            {"applicant_residency"},
        )
        self.assertTrue(all(len(row["pathway_source_hash"]) == 64 for row in private_rows))
        self.assertTrue(all(row["district_name"] == "" for row in private_rows))

    def test_join_allowed_aliases_are_unique_and_generic_freedom_alias_is_blocked(self) -> None:
        aliases = self._read("school_aliases")
        normalized_to_school_ids: dict[str, set[str]] = {}
        for row in aliases:
            if row["join_allowed"] == "true":
                normalized_to_school_ids.setdefault(row["normalized_alias"], set()).add(row["school_id"])
        self.assertTrue(all(len(school_ids) == 1 for school_ids in normalized_to_school_ids.values()))

        generic_freedom = [
            row for row in aliases if row["alias"] == "Freedom High School" and row["join_allowed"] == "false"
        ]
        self.assertEqual(len(generic_freedom), 2)
        self.assertEqual(
            {row["conflict_school_ids"] for row in generic_freedom},
            {"freedom_high_school_south_riding|freedom_high_school_woodbridge"},
        )

    def test_history_and_review_report_capture_milestone_two_decisions(self) -> None:
        history = self._read("school_history")
        events = {(row["school_id"], row["event_type"]) for row in history}
        self.assertIn(("washington_liberty_high_school", "rename"), events)
        self.assertIn(("meridian_high_school", "rename"), events)
        self.assertIn(("lewis_high_school", "rename"), events)
        self.assertIn(("unity_reed_high_school", "rename"), events)
        self.assertIn(("independence_high_school", "opening"), events)
        self.assertIn(("lightridge_high_school", "opening"), events)
        self.assertIn(("gainesville_high_school", "opening"), events)
        self.assertIn(("st_paul_vi_catholic_high_school", "relocation"), events)

        report = self.outputs["roster_review"].read_text(encoding="utf-8")
        self.assertIn("Arlington Tech is not treated as a separate analytical unit", report)
        self.assertIn("private-school applicants", report)
        self.assertIn("FCPS regional placement is based on the", report)
        self.assertIn("student's base school", report)
        self.assertIn("No pathway review rows.", report)
        self.assertNotIn("needs_private_fcps_region_assignment", report)


if __name__ == "__main__":
    unittest.main()
