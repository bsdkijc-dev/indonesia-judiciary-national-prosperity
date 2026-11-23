# Methodology: Indonesian Judicial Performance Dataset

## Scope & Indicators (Judicial Performance)
- **IND-01-01** (Case Clearance Rate): `decided_cases / incoming_cases * 100` [percentage]
- **IND-01-02** (Average Case Disposition Time (Days)): `sum(disposition_days) / decided_cases` [days]
- **IND-01-03** (Pending Case Backlog Ratio): `pending_cases / total_caseload * 100` [percentage]
- **IND-01-04** (First-Instance On-Time Decision Rate): `ontime_decisions / total_decisions * 100` [percentage]
- **IND-01-05** (Appeal Rate): `appealed_cases / decided_cases * 100` [percentage]
- **IND-01-06** (Cassation Affirmation Rate): `affirmed_cassations / total_cassations * 100` [percentage]
- **IND-01-07** (Judicial Workload per Judge): `total_caseload / active_judges` [cases_per_judge]
- **IND-01-08** (Minute-Taking & File Completion Rate): `completed_minutasi / decided_cases * 100` [percentage]
- **IND-01-09** (Mediation Success Rate): `successful_mediations / total_mediations * 100` [percentage]
- **IND-01-10** (Execution of Civil Judgments Rate): `executed_judgments / executable_judgments * 100` [percentage]

## Data Hygiene & Governance
- **Zero-Imputation Policy:** Missing observations are preserved as empty cells rather than imputed as zero.
- **Zero-PII Policy:** Only aggregate national/provincial indicators are included; no litigant, judge, or staff identifiers.
- **Fail-Closed Gate:** Automated 12-point validation blocks P3/P4 records and enforces `classification=P5`, `is_synthetic=true`, `publication_status=test_only` on synthetic demonstrations.
