# JNPDI Data Governance & Security Policy

## 1. Classification Levels
- **P1 (Public Official Approved):** Official institutional statistics with verified provenance, privacy clearance, human approval, and formal institutional authorization.
- **P2 (Public Research Derived):** Derived research metrics with verified provenance, documented methodology, and human approval.
- **P3 (Restricted Internal):** BLOCKED from public release.
- **P4 (Confidential / PII / Sealed):** BLOCKED from public release.
- **P5 (Synthetic Demonstration):** Permitted for pipeline testing and reproducible demonstrations only; must retain `classification = P5`, `is_synthetic = true`, and `publication_status = test_only`.

## 2. Fail-Closed Release Gate
Before any dataset is published to GitHub Releases or Kaggle, `src/governance_gate.py` enforces:
1. Registration in `metadata/publication_approval_register.csv`.
2. Zero P3 or P4 records.
3. All 12 data quality checks passing in `src/jnpdi_validator.py`.
4. Complete Kaggle package files (`data.csv`, `data_dictionary.csv`, `sources.csv`, `README.md`, `methodology.md`, `dataset-metadata.json`).
5. Zero personal identifiers (PII) and strict zero-imputation policy.
