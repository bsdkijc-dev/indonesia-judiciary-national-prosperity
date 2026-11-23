# Methodology: Indonesian Digital Judiciary Dataset

## Scope & Indicators (Digital Judiciary)
- **IND-04-01** (e-Court Civil Filing Penetration): `ecourt_filings / total_civil_filings * 100` [percentage]
- **IND-04-02** (e-Litigation Full-Cycle Adoption Rate): `elitigation_cases / ecourt_filings * 100` [percentage]
- **IND-04-03** (SIPP Real-Time Data Sync Compliance): `synced_courts / total_courts * 100` [percentage]
- **IND-04-04** (Direktori Putusan Publication Rate): `published_decisions / decided_cases * 100` [percentage]
- **IND-04-05** (Electronic Summons (e-Summons) Share): `esummons_sent / total_summons * 100` [percentage]
- **IND-04-06** (Digital Payment (e-Payment) Adoption): `epayment_tx / total_fee_tx * 100` [percentage]
- **IND-04-07** (Average Days from Decision to Online Upload): `sum(upload_lag_days) / published_decisions` [days]
- **IND-04-08** (Machine-Readable Decision Metadata Coverage): `structured_decisions / published_decisions * 100` [percentage]
- **IND-04-09** (Virtual Hearing (Teleconference) Utilization): `virtual_hearings / total_hearings * 100` [percentage]
- **IND-04-10** (Court Website & Open Data Uptime): `uptime_hours / total_hours * 100` [percentage]

## Data Hygiene & Governance
- **Zero-Imputation Policy:** Missing observations are preserved as empty cells rather than imputed as zero.
- **Zero-PII Policy:** Only aggregate national/provincial indicators are included; no litigant, judge, or staff identifiers.
- **Fail-Closed Gate:** Automated 12-point validation blocks P3/P4 records and enforces `classification=P5`, `is_synthetic=true`, `publication_status=test_only` on synthetic demonstrations.
