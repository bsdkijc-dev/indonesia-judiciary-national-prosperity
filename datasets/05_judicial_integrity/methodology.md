# Methodology: Indonesian Judicial Integrity Dataset

## Scope & Indicators (Institutional Integrity)
- **IND-05-01** (LHKPN Wealth Disclosure Compliance Rate): `submitted_lhkpn / obligated_officials * 100` [percentage]
- **IND-05-02** (WBK / WBBM Integrity Zone Certification Share): `certified_satkers / total_satkers * 100` [percentage]
- **IND-05-03** (Public Complaint (SIWAS) Resolution Rate): `resolved_complaints / received_complaints * 100` [percentage]
- **IND-05-04** (Average Complaint Investigation Turnaround): `sum(investigation_days) / resolved_complaints` [days]
- **IND-05-05** (BPK Financial Audit Opinion Score): `wtp_4_wdp_3_tw_2_tmp_1` [score_1_to_4]
- **IND-05-06** (Budget Realization & Transparency Index): `realized_budget / allocated_budget * 100` [percentage]
- **IND-05-07** (Ethics & Code of Conduct Training Coverage): `trained_personnel / total_personnel * 100` [percentage]
- **IND-05-08** (Disciplinary Sanction Enforcement Rate): `enforced_sanctions / recommended_sanctions * 100` [percentage]
- **IND-05-09** (Public Satisfaction Index (IKM) Score): `weighted_survey_score` [score_0_100]
- **IND-05-10** (Anti-Corruption Perception Index (IPK) Score): `weighted_integrity_survey_score` [score_0_100]

## Data Hygiene & Governance
- **Zero-Imputation Policy:** Missing observations are preserved as empty cells rather than imputed as zero.
- **Zero-PII Policy:** Only aggregate national/provincial indicators are included; no litigant, judge, or staff identifiers.
- **Fail-Closed Gate:** Automated 12-point validation blocks P3/P4 records and enforces `classification=P5`, `is_synthetic=true`, `publication_status=test_only` on synthetic demonstrations.
