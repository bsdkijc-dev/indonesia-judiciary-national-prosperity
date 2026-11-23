# Judiciary & National Prosperity Data Initiative (JNPDI) — Indonesia

**Justice Creates Trust. Trust Enables Prosperity.**

An evidence-based research initiative exploring the contribution of Indonesia's judiciary to national prosperity through judicial performance, access to justice, economic justice, digital transformation, and institutional accountability.

> **SYNTHETIC DATA NOTICE:** All datasets currently included in `datasets/` carry `classification = P5`, `is_synthetic = true`, and `publication_status = test_only`. They are synthetic benchmark demonstrations for pipeline testing and must **not** be presented as official Mahkamah Agung RI statistics.

## Repository Structure
- `config/` — Governance schema & classification rules (`governance.yaml`).
- `data/` — 20-sheet Master Governance Workbook (`JNPDI_Master_Governance_Workbook.xlsx`).
- `datasets/` — Five thematic Kaggle-ready datasets (`01_judicial_performance` through `05_judicial_integrity`).
- `metadata/` — 50 standardized indicators (`indicators_50.csv`), `sources.csv`, and `publication_approval_register.csv`.
- `notebooks/` — Five analytical research notebooks (`01` through `05`).
- `src/` — 12-point data quality validator (`jnpdi_validator.py`) and fail-closed publication gate (`governance_gate.py`).
- `tests/` — Automated unit tests (`test_jnpdi_validator.py`).
- `docs/` — Data governance and release policy documentation.
- `website/` — Responsive static GitHub Pages research portal.
- `.github/workflows/` — CI/CD workflows (`validate-data.yml`, `test-python.yml`, `deploy-pages.yml`, `publish-kaggle.yml`).

## Quick Start
```bash
python3 src/jnpdi_validator.py
python3 src/governance_gate.py
python3 -m unittest discover -s tests -v
```
