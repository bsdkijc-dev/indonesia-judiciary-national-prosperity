# Changelog

## [1.0.0] - 2026-11-23
- Initial JNPDI v1.0 public research infrastructure.
- Added 20-sheet Master Governance Workbook (`data/JNPDI_Master_Governance_Workbook.xlsx`).
- Defined 50 standardized indicators across 5 thematic domains (`metadata/indicators_50.csv`).
- Implemented 12-point automated data quality engine (`src/jnpdi_validator.py`) and fail-closed publication gate (`src/governance_gate.py`).
- Added 9 unit tests (`tests/test_jnpdi_validator.py`).
- Prepared 5 Kaggle-ready synthetic demonstration datasets (`datasets/01_*` to `05_*`) and 5 analytical notebooks (`notebooks/01_*` to `05_*`).
- Built responsive static GitHub Pages website (`website/`) and 4 GitHub Actions CI/CD workflows (`.github/workflows/`).
