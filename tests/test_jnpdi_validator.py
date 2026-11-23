"""Unit tests for JNPDI 12-point data quality validator and governance gate."""

import csv
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from jnpdi_validator import REQUIRED_COLUMNS, validate_all_datasets, validate_dataset
from governance_gate import check_publication_gate


class TestJNPDIValidator(unittest.TestCase):
    def setUp(self):
        self.indicators_csv = REPO_ROOT / "metadata/indicators_50.csv"
        self.sources_csv = REPO_ROOT / "metadata/sources.csv"
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def _write_csv(self, name: str, rows: list, headers=None) -> Path:
        p = self.tmp / name
        with open(p, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(headers or REQUIRED_COLUMNS)
            for r in rows:
                w.writerow(r)
        return p

    def test_valid_synthetic_row_passes(self):
        p = self._write_csv(
            "valid.csv",
            [["REC-001", "IND-01-01", "DOM-01", "ID-NAT", "2025", "92.5", "percentage", "SRC-SYN-001", "P5", "true", "test_only"]],
        )
        rep = validate_dataset(p, self.indicators_csv, self.sources_csv)
        self.assertTrue(rep.passed, rep.errors)

    def test_missing_columns_fails(self):
        p = self._write_csv("missing_col.csv", [["REC-001"]], headers=["record_id"])
        rep = validate_dataset(p, self.indicators_csv, self.sources_csv)
        self.assertFalse(rep.passed)

    def test_duplicate_record_id_fails(self):
        p = self._write_csv(
            "dup_id.csv",
            [
                ["REC-001", "IND-01-01", "DOM-01", "ID-NAT", "2025", "90.0", "percentage", "SRC-SYN-001", "P5", "true", "test_only"],
                ["REC-001", "IND-01-01", "DOM-01", "ID-JK", "2025", "88.0", "percentage", "SRC-SYN-001", "P5", "true", "test_only"],
            ],
        )
        rep = validate_dataset(p, self.indicators_csv, self.sources_csv)
        self.assertFalse(rep.passed)
        self.assertTrue(any("Duplicate record_id" in e for e in rep.errors))

    def test_invalid_indicator_and_domain_fails(self):
        p = self._write_csv(
            "bad_ind.csv",
            [
                ["REC-001", "IND-99-99", "DOM-01", "ID-NAT", "2025", "90.0", "percentage", "SRC-SYN-001", "P5", "true", "test_only"],
                ["REC-002", "IND-01-01", "DOM-02", "ID-NAT", "2025", "90.0", "percentage", "SRC-SYN-001", "P5", "true", "test_only"],
            ],
        )
        rep = validate_dataset(p, self.indicators_csv, self.sources_csv)
        self.assertFalse(rep.passed)
        self.assertTrue(any("Unknown indicator_id" in e for e in rep.errors))
        self.assertTrue(any("Domain mismatch" in e for e in rep.errors))

    def test_non_numeric_and_out_of_bounds_fails(self):
        p = self._write_csv(
            "bad_val.csv",
            [
                ["REC-001", "IND-01-01", "DOM-01", "ID-NAT", "2025", "abc", "percentage", "SRC-SYN-001", "P5", "true", "test_only"],
                ["REC-002", "IND-01-01", "DOM-01", "ID-JK", "2025", "150.0", "percentage", "SRC-SYN-001", "P5", "true", "test_only"],
            ],
        )
        rep = validate_dataset(p, self.indicators_csv, self.sources_csv)
        self.assertFalse(rep.passed)
        self.assertTrue(any("Non-numeric" in e for e in rep.errors))
        self.assertTrue(any("out of [0, 100]" in e for e in rep.errors))

    def test_missing_or_unknown_source_fails(self):
        p = self._write_csv(
            "bad_src.csv",
            [
                ["REC-001", "IND-01-01", "DOM-01", "ID-NAT", "2025", "90.0", "percentage", "", "P5", "true", "test_only"],
                ["REC-002", "IND-01-01", "DOM-01", "ID-JK", "2025", "90.0", "percentage", "SRC-UNKNOWN", "P5", "true", "test_only"],
            ],
        )
        rep = validate_dataset(p, self.indicators_csv, self.sources_csv)
        self.assertFalse(rep.passed)
        self.assertTrue(any("Missing source_id" in e for e in rep.errors))
        self.assertTrue(any("Unregistered source_id" in e for e in rep.errors))

    def test_blocked_p3_p4_classification_fails(self):
        p = self._write_csv(
            "p4.csv",
            [["REC-001", "IND-01-01", "DOM-01", "ID-NAT", "2025", "90.0", "percentage", "SRC-SYN-001", "P4", "false", "approved"]],
        )
        rep = validate_dataset(p, self.indicators_csv, self.sources_csv)
        self.assertFalse(rep.passed)
        self.assertTrue(any("Blocked classification" in e for e in rep.errors))

    def test_synthetic_mismatch_fails(self):
        p = self._write_csv(
            "bad_synth.csv",
            [["REC-001", "IND-01-01", "DOM-01", "ID-NAT", "2025", "90.0", "percentage", "SRC-SYN-001", "P1", "true", "approved"]],
        )
        rep = validate_dataset(p, self.indicators_csv, self.sources_csv)
        self.assertFalse(rep.passed)
        self.assertTrue(any("Check 11" in e for e in rep.errors))

    def test_all_repository_datasets_and_gate(self):
        ok, reports = validate_all_datasets(REPO_ROOT)
        self.assertEqual(len(reports), 5)
        self.assertTrue(ok, [r.errors for r in reports if not r.passed])
        gate_ok, issues = check_publication_gate(REPO_ROOT)
        self.assertTrue(gate_ok, issues)


if __name__ == "__main__":
    unittest.main()
