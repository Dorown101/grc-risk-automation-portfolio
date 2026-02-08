# GRC Risk Register Automation Portfolio

This mini project generates a realistic risk register for a mid-size insurance company operating in a hybrid (on-prem + Azure) environment. It creates synthetic risks, calculates adjusted risk scores, exports an Excel workbook, and generates a risk distribution chart.

## Features

- Synthetic data generation for 40+ insurance-focused IT and security risks.
- Risk score calculation based on likelihood x impact with control effectiveness adjustments.
- Risk level classification (Low/Medium/High).
- Excel workbook output with raw data, calculated risks, and an executive summary.
- Risk distribution chart saved as a PNG image.

## Sample Dataset Preview (first 5 rows)

| Risk_ID | Risk_Name | Risk_Category | Asset_Name | Threat_Description | Vulnerability_Description | Likelihood | Impact | Control_Exists | Control_Effectiveness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RISK-001 | Insider data export via USB | Privacy | Claims Operations Workstations | Unauthorized data extraction | USB device controls not enforced | 2 | 5 | Yes | High |
| RISK-002 | Endpoint encryption gaps | Infrastructure | Underwriter Laptops | Loss or theft of devices | Full-disk encryption not enforced | 4 | 4 | No | Low |
| RISK-003 | Ransomware infection via phishing | Infrastructure | Employee Endpoints | Encryption of shared drives | Inconsistent endpoint detection coverage | 3 | 2 | Yes | High |
| RISK-004 | Cloud workload logging gaps | Cloud | Azure Monitor | Delayed detection of suspicious activity | Incomplete diagnostic settings | 3 | 4 | Yes | Low |
| RISK-005 | Orphaned contractor accounts | IAM | Identity Governance Platform | Unauthorized access via unused accounts | Incomplete offboarding workflow | 2 | 5 | Yes | Medium |

## How It Works

1. **Synthetic Data Generation**: `synthetic_data_generator.py` produces realistic insurance-sector risks across infrastructure, IAM, network, cloud, third party, and privacy.
2. **Risk Calculation**: `risk_register_generator.py` calculates base risk scores, adjusts them based on controls, assigns risk levels, and prepares the executive summary.
3. **Excel Output**: The script exports `Insurance_Risk_Register.xlsx` with:
   - `Raw_Risks`
   - `Calculated_Risks`
   - `Executive_Summary`
4. **Visualization**: `risk_distribution.png` shows the risk level distribution.

## How to Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas openpyxl matplotlib
python risk_register_generator.py
```

### Outputs

- `Insurance_Risk_Register.xlsx`
- `risk_distribution.png`

## Notes

- Likelihood and impact are scored 1-5, with risk score = likelihood x impact.
- Controls reduce the score by:
  - High: 50%
  - Medium: 30%
  - Low: 10%
