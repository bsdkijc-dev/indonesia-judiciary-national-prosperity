"""Fail-Closed Publication & Security Governance Gate for JNPDI."""

import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple

from jnpdi_validator import BLOCKED_CLASSIFICATIONS, validate_dataset


def check_publication_gate(repo_root: Path) -> Tuple[bool, List[str]]:
    """Verify all 5 datasets pass classification, privacy, provenance, and metadata gates."""
    issues: List[str] = []
    register_path = repo_root / "metadata/publication_approval_register.csv"
    indicators_csv = repo_root / "metadata/indicators_50.csv"

    if not register_path.exists():
        return False, ["Missing metadata/publication_approval_register.csv"]

    register: Dict[str, Dict[str, str]] = {}
    with open(register_path, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            register[row["dataset_id"].strip()] = row

    datasets_dir = repo_root / "datasets"
    required_files = [
        "data.csv",
        "data_dictionary.csv",
        "sources.csv",
        "README.md",
        "methodology.md",
        "dataset-metadata.json",
    ]

    for ds_dir in sorted(datasets_dir.iterdir()):
        if not ds_dir.is_dir():
            continue
        ds_id = ds_dir.name
        if ds_id not in register:
            issues.append(f"{ds_id}: Not registered in publication_approval_register.csv")
            continue

        reg_row = register[ds_id]
        if reg_row.get("classification", "").strip() in BLOCKED_CLASSIFICATIONS:
            issues.append(f"{ds_id}: Classification {reg_row.get('classification')} is BLOCKED")
        if reg_row.get("privacy_check", "").strip() != "PASSED":
            issues.append(f"{ds_id}: Privacy check not PASSED")
        if reg_row.get("provenance_check", "").strip() != "PASSED":
            issues.append(f"{ds_id}: Provenance check not PASSED")

        for fname in required_files:
            if not (ds_dir / fname).exists():
                issues.append(f"{ds_id}: Missing required Kaggle file '{fname}'")

        meta_path = ds_dir / "dataset-metadata.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                for key in ("title", "id", "licenses"):
                    if key not in meta:
                        issues.append(f"{ds_id}: dataset-metadata.json missing '{key}'")
            except json.JSONDecodeError as exc:
                issues.append(f"{ds_id}: Invalid dataset-metadata.json ({exc})")

        rep = validate_dataset(ds_dir / "data.csv", indicators_csv, ds_dir / "sources.csv", require_public_safe=True)
        if not rep.passed:
            issues.extend([f"{ds_id}: {e}" for e in rep.errors])

    return len(issues) == 0, issues


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    ok, probs = check_publication_gate(root)
    if ok:
        print("GOVERNANCE GATE: PASSED (Fail-Closed Checks Verified)")
    else:
        print("GOVERNANCE GATE: BLOCKED")
        for p in probs:
            print(f"  - {p}")
    raise SystemExit(0 if ok else 1)
