# Methodology: Indonesian Business & Economic Justice Dataset

## Scope & Indicators (Business & Economic Justice)
- **IND-03-01** (Commercial Contract Dispute Resolution Time): `sum(commercial_days) / decided_commercial` [days]
- **IND-03-02** (Bankruptcy & PKPU Clearance Rate): `decided_pkpu_bankruptcy / incoming_pkpu_bankruptcy * 100` [percentage]
- **IND-03-03** (Intellectual Property Dispute Disposition Time): `sum(ip_days) / decided_ip_cases` [days]
- **IND-03-04** (Industrial Relations Dispute Settlement Rate): `settled_phi_cases / total_phi_cases * 100` [percentage]
- **IND-03-05** (Tax Court Dispute Clearance Rate): `decided_tax_cases / incoming_tax_cases * 100` [percentage]
- **IND-03-06** (MSME Small Claims Recovery Rate): `recovered_value / claimed_value * 100` [percentage]
- **IND-03-07** (Arbitration Award Enforcement Timeliness): `avg_days_to_exequatur` [days]
- **IND-03-08** (Land & Property Dispute Resolution Duration): `sum(land_case_days) / decided_land_cases` [days]
- **IND-03-09** (Judicial Predictability in Commercial Rulings): `consistency_score_across_circuits` [index_0_100]
- **IND-03-10** (Court-Annexed Commercial Mediation Rate): `mediated_commercial / total_commercial * 100` [percentage]

## Data Hygiene & Governance
- **Zero-Imputation Policy:** Missing observations are preserved as empty cells rather than imputed as zero.
- **Zero-PII Policy:** Only aggregate national/provincial indicators are included; no litigant, judge, or staff identifiers.
- **Fail-Closed Gate:** Automated 12-point validation blocks P3/P4 records and enforces `classification=P5`, `is_synthetic=true`, `publication_status=test_only` on synthetic demonstrations.
