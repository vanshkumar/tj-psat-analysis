from __future__ import annotations

import csv
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
                "aps_2023_semifinalists",
                "aps_2025_semifinalists",
                "aps_2026_semifinalists",
                "fcps_2023_semifinalists",
                "fcps_2024_semifinalists",
                "fcps_2025_semifinalists",
                "fcps_2026_semifinalists",
                "lcps_2025_semifinalists",
                "lcps_2026_semifinalists",
                "patch_fairfax_city_2025_semifinalists",
                "patch_fairfax_city_2026_semifinalists",
                "patch_mclean_2025_semifinalists",
                "pwcs_2023_semifinalists",
                "pwcs_2024_semifinalists",
                "pwcs_2025_semifinalists",
                "pwcs_2026_semifinalists",
            },
        )
        for source in self.sources.values():
            self.assertIn(source.parser_name, PARSER_REGISTRY_BY_NAME)
            self.assertEqual(source.parser_name, "manual_reviewed_table")
            if source.complete_for_zero_inference:
                self.assertTrue(source.zero_inference_scope.endswith("_public_high_schools_in_roster"))
            else:
                self.assertIn(
                    source.source_id,
                    {
                        "lcps_2025_semifinalists",
                        "patch_fairfax_city_2025_semifinalists",
                        "patch_fairfax_city_2026_semifinalists",
                        "patch_mclean_2025_semifinalists",
                    },
                )
                self.assertEqual(source.zero_inference_scope, "none")
            self.assertEqual(len(source.source_hash), 64)
            self.assertTrue(source.reported_total)
        self.assertIn("verified_count", NMSF_OBSERVATION_STATUSES)
        self.assertIn("missing_source", NMSF_OBSERVATION_STATUSES)

    def test_manifest_sources_have_archived_snapshots(self) -> None:
        count_records = read_manual_nmsf_counts(ROOT / "data" / "sources" / "nmsf_counts.csv")
        records_by_source = {
            source_id: sorted(
                (record.school_name_source, record.nmsf_count)
                for record in count_records
                if record.source_id == source_id
            )
            for source_id in self.sources
        }

        for source in self.sources.values():
            self.assertTrue(source.archived_file_path.startswith("data/raw/nmsf/"))
            self.assertEqual(len(source.archived_file_sha256), 64)

            snapshot_path = ROOT / source.archived_file_path
            self.assertTrue(snapshot_path.is_file())
            with snapshot_path.open(newline="", encoding="utf-8") as handle:
                snapshot_rows = list(csv.DictReader(handle))
            observation_snapshot_rows = [
                row
                for row in snapshot_rows
                if row.get("snapshot_record_type", "observation_count") == "observation_count"
            ]

            self.assertEqual({row["source_id"] for row in snapshot_rows}, {source.source_id})
            self.assertEqual({row["class_year"] for row in snapshot_rows}, {str(source.graduating_class)})
            self.assertEqual(
                sorted(
                    (row["school_name_source"], int(row["nmsf_count"])) for row in observation_snapshot_rows
                ),
                records_by_source[source.source_id],
            )
            if observation_snapshot_rows:
                self.assertEqual(
                    {row["snapshot_notes"] for row in observation_snapshot_rows},
                    {"student names intentionally omitted"},
                )
            else:
                self.assertEqual(source.source_id, "lcps_2025_semifinalists")

            if source.source_id == "lcps_2025_semifinalists":
                source_only_rows = [
                    row
                    for row in snapshot_rows
                    if row.get("snapshot_record_type") == "source_incomplete_unattributed_total"
                ]
                self.assertEqual(len(source_only_rows), 1)
                self.assertEqual(
                    source_only_rows[0]["school_name_source"], "LCPS unattributed semifinalist total"
                )
                self.assertEqual(source_only_rows[0]["nmsf_count"], "57")

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
        self.assertEqual(statuses["verified_count"], 115)
        self.assertEqual(statuses["verified_zero"], 73)
        self.assertEqual(statuses["not_operating"], 9)

        tj_2023 = self._lookup("thomas_jefferson_high_school_for_science_and_technology", 2023)
        self.assertEqual(tj_2023["nmsf_count"], "132")
        self.assertEqual(tj_2023["nmsf_status"], "verified_count")
        self.assertEqual(tj_2023["source_id"], "fcps_2023_semifinalists")

        annandale_2023 = self._lookup("annandale_high_school", 2023)
        self.assertEqual(annandale_2023["nmsf_count"], "0")
        self.assertEqual(annandale_2023["nmsf_status"], "verified_zero")
        self.assertEqual(annandale_2023["source_id"], "fcps_2023_semifinalists")

        tj_2026 = self._lookup("thomas_jefferson_high_school_for_science_and_technology", 2026)
        self.assertEqual(tj_2026["nmsf_count"], "113")
        self.assertEqual(tj_2026["nmsf_status"], "verified_count")
        self.assertEqual(tj_2026["source_id"], "fcps_2026_semifinalists")

        robinson_2026 = self._lookup("robinson_secondary_school_hs", 2026)
        self.assertEqual(robinson_2026["nmsf_count"], "0")
        self.assertEqual(robinson_2026["nmsf_status"], "verified_zero")
        self.assertEqual(robinson_2026["observation_basis"], "complete_source_zero_inference")
        self.assertEqual(robinson_2026["source_id"], "fcps_2026_semifinalists")

    def test_aps_and_lcps_counts_and_verified_zero_inference(self) -> None:
        washington_liberty_2023 = self._lookup("washington_liberty_high_school", 2023)
        self.assertEqual(washington_liberty_2023["nmsf_count"], "7")
        self.assertEqual(washington_liberty_2023["nmsf_status"], "verified_count")
        self.assertEqual(washington_liberty_2023["source_id"], "aps_2023_semifinalists")

        washington_liberty_2026 = self._lookup("washington_liberty_high_school", 2026)
        self.assertEqual(washington_liberty_2026["nmsf_count"], "9")
        self.assertEqual(washington_liberty_2026["nmsf_status"], "verified_count")
        self.assertEqual(washington_liberty_2026["source_id"], "aps_2026_semifinalists")

        wakefield_2026 = self._lookup("wakefield_high_school", 2026)
        self.assertEqual(wakefield_2026["nmsf_count"], "0")
        self.assertEqual(wakefield_2026["nmsf_status"], "verified_zero")
        self.assertEqual(wakefield_2026["source_id"], "aps_2026_semifinalists")

        freedom_lcps_2026 = self._lookup("freedom_high_school_south_riding", 2026)
        self.assertEqual(freedom_lcps_2026["nmsf_count"], "7")
        self.assertEqual(freedom_lcps_2026["nmsf_status"], "verified_count")
        self.assertEqual(freedom_lcps_2026["source_id"], "lcps_2026_semifinalists")

        loudoun_county_2026 = self._lookup("loudoun_county_high_school", 2026)
        self.assertEqual(loudoun_county_2026["nmsf_count"], "0")
        self.assertEqual(loudoun_county_2026["nmsf_status"], "verified_zero")
        self.assertEqual(loudoun_county_2026["source_id"], "lcps_2026_semifinalists")

    def test_pwcs_counts_and_verified_zero_inference(self) -> None:
        osbourn_park_2023 = self._lookup("osbourn_park_high_school", 2023)
        self.assertEqual(osbourn_park_2023["nmsf_count"], "2")
        self.assertEqual(osbourn_park_2023["nmsf_status"], "verified_count")
        self.assertEqual(osbourn_park_2023["source_id"], "pwcs_2023_semifinalists")

        battlefield_2025 = self._lookup("battlefield_high_school", 2025)
        self.assertEqual(battlefield_2025["nmsf_count"], "2")
        self.assertEqual(battlefield_2025["nmsf_status"], "verified_count")
        self.assertEqual(battlefield_2025["source_id"], "pwcs_2025_semifinalists")

        hylton_2026 = self._lookup("c_d_hylton_high_school", 2026)
        self.assertEqual(hylton_2026["nmsf_count"], "1")
        self.assertEqual(hylton_2026["nmsf_status"], "verified_count")
        self.assertEqual(hylton_2026["source_id"], "pwcs_2026_semifinalists")

        brentsville_2026 = self._lookup("brentsville_district_high_school", 2026)
        self.assertEqual(brentsville_2026["nmsf_count"], "0")
        self.assertEqual(brentsville_2026["nmsf_status"], "verified_zero")
        self.assertEqual(brentsville_2026["source_id"], "pwcs_2026_semifinalists")

    def test_local_media_private_school_counts_do_not_create_zeros(self) -> None:
        new_school_2025 = self._lookup("new_school_of_northern_virginia", 2025)
        self.assertEqual(new_school_2025["nmsf_count"], "2")
        self.assertEqual(new_school_2025["nmsf_status"], "verified_count")
        self.assertEqual(new_school_2025["source_id"], "patch_fairfax_city_2025_semifinalists")

        trinity_2025 = self._lookup("trinity_christian_school", 2025)
        self.assertEqual(trinity_2025["nmsf_count"], "1")
        self.assertEqual(trinity_2025["nmsf_status"], "verified_count")
        self.assertEqual(trinity_2025["source_id"], "patch_fairfax_city_2025_semifinalists")

        basis_mclean_2025 = self._lookup("basis_independent_mclean", 2025)
        self.assertEqual(basis_mclean_2025["nmsf_count"], "4")
        self.assertEqual(basis_mclean_2025["nmsf_status"], "verified_count")
        self.assertEqual(basis_mclean_2025["source_id"], "patch_mclean_2025_semifinalists")

        madeira_2025 = self._lookup("the_madeira_school", 2025)
        self.assertEqual(madeira_2025["nmsf_count"], "3")
        self.assertEqual(madeira_2025["nmsf_status"], "verified_count")
        self.assertEqual(madeira_2025["source_id"], "patch_mclean_2025_semifinalists")

        potomac_2025 = self._lookup("potomac_school", 2025)
        self.assertEqual(potomac_2025["nmsf_count"], "9")
        self.assertEqual(potomac_2025["nmsf_status"], "verified_count")
        self.assertEqual(potomac_2025["source_id"], "patch_mclean_2025_semifinalists")

        new_school_2026 = self._lookup("new_school_of_northern_virginia", 2026)
        self.assertEqual(new_school_2026["nmsf_count"], "1")
        self.assertEqual(new_school_2026["nmsf_status"], "verified_count")
        self.assertEqual(new_school_2026["source_id"], "patch_fairfax_city_2026_semifinalists")

        trinity_2026 = self._lookup("trinity_christian_school", 2026)
        self.assertEqual(trinity_2026["nmsf_count"], "1")
        self.assertEqual(trinity_2026["nmsf_status"], "verified_count")
        self.assertEqual(trinity_2026["source_id"], "patch_fairfax_city_2026_semifinalists")

        flint_hill_2025 = self._lookup("flint_hill_school", 2025)
        self.assertEqual(flint_hill_2025["nmsf_count"], "")
        self.assertEqual(flint_hill_2025["nmsf_status"], "missing_source")
        self.assertEqual(flint_hill_2025["source_id"], "")

    def test_unsourced_rows_remain_missing_until_sourced(self) -> None:
        seton_2026 = self._lookup("seton_school_manassas", 2026)
        self.assertEqual(seton_2026["nmsf_count"], "")
        self.assertEqual(seton_2026["nmsf_status"], "missing_source")
        self.assertEqual(seton_2026["source_id"], "")


if __name__ == "__main__":
    unittest.main()
