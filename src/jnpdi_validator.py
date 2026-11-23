"""JNPDI 12-Point Data Quality & Governance Validator."""

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

REQUIRED_COLUMNS = [
    "record_id",
    "indicator_id",
    "domain_id",
    "jurisdiction",
    "year",
    "value",
    "unit",
    "source_id",
    "classification",
    "is_synthetic",
    "publication_status",
]

VALID_CLASSIFICATIONS = {"P1", "P2", "P3", "P4", "P5"}
BLOCKED_CLASSIFICATIONS = {"P3", "P4"}
VALID_PUBLICATION_STATUSES = {"approved", "test_only", "pending", "blocked"}


@dataclass
class ValidationReport:
    dataset_path: str
    passed: bool = True
    row_count: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    checks_run: List[str] = field(default_factory=list)

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)
        self.passed = False

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)


def load_indicators(indicators_csv: Path) -> Dict[str, Dict[str, str]]:
    indicators: Dict[str, Dict[str, str]] = {}
    with open(indicators_csv, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            indicators[row["indicator_id"].strip()] = row
    return indicators


def load_sources(sources_csv: Path) -> Set[str]:
    sources: Set[str] = set()
    with open(sources_csv, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            sid = row.get("source_id", "").strip()
            if sid:
                sources.add(sid)
    return sources


def validate_dataset(
    data_csv: Path,
    indicators_csv: Path,
    sources_csv: Path,
    require_public_safe: bool = True,
) -> ValidationReport:
    report = ValidationReport(dataset_path=str(data_csv))
    report.checks_run = [
        "1_required_csv_columns",
        "2_unique_record_ids",
        "3_valid_indicator_ids",
        "4_valid_domain_assignments",
        "5_numeric_values",
        "6_missing_source_ids",
        "7_source_provenance",
        "8_duplicate_observations",
        "9_invalid_classifications",
        "10_publication_approval_status",
        "11_synthetic_data_identification",
        "12_indicator_formula_consistency",
    ]

    if not data_csv.exists():
        report.add_error(f"Dataset file not found: {data_csv}")
        return report

    indicators = load_indicators(indicators_csv)
    valid_sources = load_sources(sources_csv)

    with open(data_csv, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        # 1. Required CSV columns
        missing_cols = [c for c in REQUIRED_COLUMNS if c not in fieldnames]
        if missing_cols:
            report.add_error(f"Check 1 (Required Columns): Missing {missing_cols}")
            return report

        seen_record_ids: Set[str] = set()
        seen_observations: Set[Tuple[str, str, str]] = set()

        for idx, row in enumerate(reader, start=2):
            report.row_count += 1
            rec_id = (row.get("record_id") or "").strip()
            ind_id = (row.get("indicator_id") or "").strip()
            dom_id = (row.get("domain_id") or "").strip()
            jurisdiction = (row.get("jurisdiction") or "").strip()
            year = (row.get("year") or "").strip()
            raw_val = (row.get("value") or "").strip()
            unit = (row.get("unit") or "").strip()
            src_id = (row.get("source_id") or "").strip()
            classification = (row.get("classification") or "").strip()
            is_synth = (row.get("is_synthetic") or "").strip().lower()
            pub_status = (row.get("publication_status") or "").strip()

            # 2. Unique record IDs
            if not rec_id:
                report.add_error(f"Row {idx} Check 2: Empty record_id")
            elif rec_id in seen_record_ids:
                report.add_error(f"Row {idx} Check 2: Duplicate record_id '{rec_id}'")
            else:
                seen_record_ids.add(rec_id)

            # 3. Valid indicator IDs
            if ind_id not in indicators:
                report.add_error(f"Row {idx} Check 3: Unknown indicator_id '{ind_id}'")
            else:
                expected_dom = indicators[ind_id]["domain_id"].strip()
                expected_unit = indicators[ind_id]["unit"].strip()
                # 4. Valid domain assignments
                if dom_id != expected_dom:
                    report.add_error(
                        f"Row {idx} Check 4: Domain mismatch for '{ind_id}': got '{dom_id}', expected '{expected_dom}'"
                    )
                # 12. Indicator formula & unit consistency
                if unit != expected_unit:
                    report.add_error(
                        f"Row {idx} Check 12: Unit mismatch for '{ind_id}': got '{unit}', expected '{expected_unit}'"
                    )

            # 5. Numeric values (allow empty for zero-imputation policy, otherwise must be finite float)
            numeric_val: Optional[float] = None
            if raw_val != "":
                try:
                    numeric_val = float(raw_val)
                    if not math.isfinite(numeric_val):
                        report.add_error(f"Row {idx} Check 5: Non-finite value '{raw_val}'")
                        numeric_val = None
                except ValueError:
                    report.add_error(f"Row {idx} Check 5: Non-numeric value '{raw_val}'")

            # 12b. Range consistency for bounded units
            if numeric_val is not None:
                if unit == "percentage" and not (0.0 <= numeric_val <= 100.0):
                    report.add_error(f"Row {idx} Check 12: Percentage out of [0, 100] bounds: {numeric_val}")
                elif unit == "score_0_100" and not (0.0 <= numeric_val <= 100.0):
                    report.add_error(f"Row {idx} Check 12: Score_0_100 out of [0, 100] bounds: {numeric_val}")
                elif unit == "score_1_to_4" and not (1.0 <= numeric_val <= 4.0):
                    report.add_error(f"Row {idx} Check 12: Score_1_to_4 out of [1, 4] bounds: {numeric_val}")
                elif unit == "days" and numeric_val < 0.0:
                    report.add_error(f"Row {idx} Check 12: Negative days value: {numeric_val}")

            # 6. Missing source IDs & 7. Source provenance
            if not src_id:
                report.add_error(f"Row {idx} Check 6: Missing source_id")
            elif src_id not in valid_sources:
                report.add_error(f"Row {idx} Check 7: Unregistered source_id '{src_id}'")

            # 8. Duplicate observations
            obs_key = (ind_id, jurisdiction, year)
            if obs_key in seen_observations:
                report.add_error(f"Row {idx} Check 8: Duplicate observation {obs_key}")
            else:
                seen_observations.add(obs_key)

            # 9. Invalid classifications
            if classification not in VALID_CLASSIFICATIONS:
                report.add_error(f"Row {idx} Check 9: Invalid classification '{classification}'")
            elif require_public_safe and classification in BLOCKED_CLASSIFICATIONS:
                report.add_error(f"Row {idx} Check 9: Blocked classification '{classification}' in public dataset")

            # 10. Publication approval status
            if pub_status not in VALID_PUBLICATION_STATUSES:
                report.add_error(f"Row {idx} Check 10: Invalid publication_status '{pub_status}'")
            elif require_public_safe and pub_status == "blocked":
                report.add_error(f"Row {idx} Check 10: Blocked publication_status on row '{rec_id}'")

            # 11. Synthetic data identification
            if is_synth == "true" or classification == "P5" or pub_status == "test_only":
                if not (classification == "P5" and is_synth == "true" and pub_status == "test_only"):
                    report.add_error(
                        f"Row {idx} Check 11: Synthetic record must have classification=P5, is_synthetic=true, publication_status=test_only (got {classification}, {is_synth}, {pub_status})"
                    )

    return report


def validate_all_datasets(repo_root: Path) -> Tuple[bool, List[ValidationReport]]:
    indicators_csv = repo_root / "metadata/indicators_50.csv"
    global_sources_csv = repo_root / "metadata/sources.csv"
    datasets_dir = repo_root / "datasets"
    reports: List[ValidationReport] = []
    all_passed = True

    for ds_dir in sorted(datasets_dir.iterdir()):
        if ds_dir.is_dir():
            data_csv = ds_dir / "data.csv"
            local_sources = ds_dir / "sources.csv"
            sources_to_use = local_sources if local_sources.exists() else global_sources_csv
            rep = validate_dataset(data_csv, indicators_csv, sources_to_use, require_public_safe=True)
            reports.append(rep)
            if not rep.passed:
                all_passed = False

    return all_passed, reports


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    ok, reps = validate_all_datasets(root)
    for r in reps:
        status = "PASS" if r.passed else "FAIL"
        print(f"[{status}] {r.dataset_path} ({r.row_count} rows, {len(r.errors)} errors)")
        for err in r.errors:
            print(f"  ERROR: {err}")
    raise SystemExit(0 if ok else 1)
