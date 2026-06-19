from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tj_psat_analysis.descriptive import (  # noqa: E402
    FIGURE_FILENAMES,
    TABLE_SPECS,
    build_descriptive_outputs,
    load_csv_rows,
)


class DescriptiveOutputsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        cls.outputs = build_descriptive_outputs(
            analysis_panel_csv=ROOT / "data" / "processed" / "analysis_panel.csv",
            figures_dir=root / "figures",
            tables_dir=root / "tables",
            report_path=root / "descriptive_results.md",
        )
        cls.panel = load_csv_rows(ROOT / "data" / "processed" / "analysis_panel.csv")
        cls.tables = {
            table_key: load_csv_rows(cls.outputs[f"table_{table_key}"]) for table_key in TABLE_SPECS
        }

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def test_generates_expected_tables_figures_and_report(self) -> None:
        for table_key in TABLE_SPECS:
            path = self.outputs[f"table_{table_key}"]
            self.assertTrue(path.exists(), table_key)
            with path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames, list(TABLE_SPECS[table_key][1]))

        for figure_key in FIGURE_FILENAMES:
            path = self.outputs[f"figure_{figure_key}"]
            self.assertTrue(path.exists(), figure_key)
            self.assertIn("<svg", path.read_text(encoding="utf-8"))

        report = self.outputs["descriptive_report"].read_text(encoding="utf-8")
        self.assertIn("Missing observations are displayed as missing, not zero.", report)
        self.assertIn("covered-subset aggregates", report)

    def test_group_totals_preserve_observed_count_semantics(self) -> None:
        base_public_2026 = [
            row
            for row in self.tables["school_group_totals_by_class"]
            if row["class_year"] == "2026" and row["school_group"] == "Base public schools"
        ][0]
        source_rows = [
            row
            for row in self.panel
            if row["class_year"] == "2026"
            and row["sector"] == "public"
            and row["tj_pathway"] != "TJHSST"
            and row["nmsf_count_available"] == "true"
        ]
        compatible_rows = [row for row in source_rows if row["rate_input_compatible"] == "true"]
        self.assertEqual(
            base_public_2026["nmsf_count_observed_total"],
            str(sum(int(row["nmsf_count"]) for row in source_rows)),
        )
        self.assertEqual(
            base_public_2026["compatible_nmsf_count_total"],
            str(sum(int(row["nmsf_count"]) for row in compatible_rows)),
        )
        self.assertEqual(base_public_2026["nmsf_count_coverage_status"], "partial_nmsf_count_coverage")

    def test_missing_nmsf_rows_remain_blank_in_school_tables(self) -> None:
        wakefield_2024 = [
            row
            for row in self.tables["school_counts_by_year"]
            if row["school_id"] == "wakefield_high_school" and row["class_year"] == "2024"
        ][0]
        self.assertEqual(wakefield_2024["nmsf_status"], "missing_source")
        self.assertEqual(wakefield_2024["nmsf_count"], "")
        self.assertIn("not treated as zero", wakefield_2024["count_missingness_note"])

        rate_row = [
            row
            for row in self.tables["school_rates_by_year"]
            if row["school_id"] == "wakefield_high_school" and row["class_year"] == "2024"
        ][0]
        self.assertEqual(rate_row["nmsf_per_100_juniors"], "")
        self.assertEqual(rate_row["rate_status"], "missing_nmsf_count")

    def test_pathway_heatmap_uses_covered_subset_fields(self) -> None:
        arlington_2026 = [
            row
            for row in self.tables["pathway_by_class_heatmap"]
            if row["tj_pathway"] == "Arlington" and row["class_year"] == "2026"
        ][0]
        representative = [
            row for row in self.panel if row["tj_pathway"] == "Arlington" and row["class_year"] == "2026"
        ][0]
        self.assertEqual(
            arlington_2026["pathway_nmsf_count_covered"],
            representative["pathway_nmsf_count_covered"],
        )
        self.assertEqual(arlington_2026["pathway_coverage_status"], "partial_compatible_coverage")
        self.assertIn("covered subset only", arlington_2026["pathway_interpretation_note"])

    def test_unsourced_cutoff_placeholders_are_not_annotated_in_figures(self) -> None:
        report = self.outputs["descriptive_report"].read_text(encoding="utf-8")
        self.assertIn("Virginia cutoff statuses in the analysis panel: `not_sourced`", report)
        self.assertIn("No Virginia Selection Index cutoff change is annotated", report)
        for figure_key in FIGURE_FILENAMES:
            figure_text = self.outputs[f"figure_{figure_key}"].read_text(encoding="utf-8")
            self.assertNotIn("Selection Index", figure_text)
            self.assertNotIn("cutoff", figure_text.lower())


if __name__ == "__main__":
    unittest.main()
