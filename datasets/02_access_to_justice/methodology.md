# Methodology: Indonesian Access to Justice Dataset

## Scope & Indicators (Access to Justice)
- **IND-02-01** (Prodeo (Fee-Waiver) Case Share): `prodeo_cases / total_eligible_cases * 100` [percentage]
- **IND-02-02** (Posbakum (Legal Aid Post) Utilization Rate): `posbakum_beneficiaries / population * 100000` [cases_per_100k]
- **IND-02-03** (Mobile Court (Sidang Keliling) Coverage): `mobile_sessions / districts_served` [sessions_per_district]
- **IND-02-04** (Court Geographic Accessibility Index): `weighted_distance_population_score` [index_0_100]
- **IND-02-05** (Disability-Accessible Courtroom Ratio): `accessible_courts / total_courts * 100` [percentage]
- **IND-02-06** (Small Claims (Gugatan Sederhana) Adoption): `small_claims / eligible_civil_cases * 100` [percentage]
- **IND-02-07** (Language & Sign Interpreter Availability): `courts_with_interpreter / total_courts * 100` [percentage]
- **IND-02-08** (Women & Vulnerable Group Legal Aid Share): `vulnerable_aid_cases / total_aid_cases * 100` [percentage]
- **IND-02-09** (Average Out-of-Pocket Court Fee Ratio): `avg_court_fee / provincial_monthly_wage * 100` [percentage_of_gdp_pc]
- **IND-02-10** (Public Legal Information Inquiry Resolution): `resolved_inquiries / total_inquiries * 100` [percentage]

## Data Hygiene & Governance
- **Zero-Imputation Policy:** Missing observations are preserved as empty cells rather than imputed as zero.
- **Zero-PII Policy:** Only aggregate national/provincial indicators are included; no litigant, judge, or staff identifiers.
- **Fail-Closed Gate:** Automated 12-point validation blocks P3/P4 records and enforces `classification=P5`, `is_synthetic=true`, `publication_status=test_only` on synthetic demonstrations.
