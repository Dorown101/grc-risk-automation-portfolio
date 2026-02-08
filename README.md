# GRC Risk Register Automation Portfolio

This mini project demonstrates a realistic, insurance-focused GRC risk register automation workflow. It generates synthetic risks, applies risk scoring logic aligned with ISO 27001 and NIST CSF practices, and exports an executive-ready Excel workbook with summary metrics and a visualization.

## Features
- Synthetic risk generation tailored to a mid-size insurance company.
- Risk scoring with control effectiveness adjustments.
- Executive summary with top risks and counts by risk level.
- Excel export with three sheets and an embedded chart.

## Requirements
- Python 3.9+
- Dependencies: `pandas`, `openpyxl`, `matplotlib`

Install dependencies:
```bash
pip install pandas openpyxl matplotlib
```

## How to Run
```bash
python risk_register_generator.py
```

This will create:
- `Insurance_Risk_Register.xlsx`
- `risk_distribution.png`

## Sample Dataset Preview (first 5 rows)

| Risk_ID | Risk_Name | Risk_Category | Asset_Name | Threat_Description | Vulnerability_Description | Likelihood | Impact | Control_Exists | Control_Effectiveness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RISK-001 | Hardware failure impacting Policy Administration Server | Infrastructure | Policy Administration Server | hardware failure | unsupported operating system | 3 | 3 | Yes | Medium |
| RISK-002 | Credential stuffing impacting Okta SSO | IAM | Okta SSO | credential stuffing | weak MFA enforcement | 4 | 4 | Yes | High |
| RISK-003 | Data exfiltration impacting Azure Storage Accounts | Cloud | Azure Storage Accounts | data exfiltration | publicly exposed storage | 5 | 4 | Yes | Medium |
| RISK-004 | Vendor data breach impacting Email Marketing Platform | Third Party | Email Marketing Platform | vendor data breach | limited vendor oversight | 3 | 4 | No | Low |
| RISK-005 | Unauthorized access impacting Customer PII Repository | Privacy | Customer PII Repository | unauthorized access | insufficient data classification | 4 | 5 | Yes | High |
