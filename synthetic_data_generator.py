"""Synthetic data generator for insurance-focused IT and security risks."""

from __future__ import annotations

import random
from typing import Dict, List

import pandas as pd


RISK_CATEGORIES: Dict[str, Dict[str, List[str]]] = {
    "Infrastructure": {
        "assets": [
            "Policy Administration Server",
            "Claims Processing Database",
            "VMware Cluster",
            "Backup Storage Array",
            "On-Prem Data Center Power Systems",
            "Enterprise File Server",
        ],
        "threats": [
            "hardware failure",
            "ransomware encryption",
            "unauthorized configuration change",
            "capacity exhaustion",
            "fire or environmental damage",
        ],
        "vulnerabilities": [
            "single points of failure",
            "unsupported operating system",
            "insufficient patch management",
            "lack of immutable backups",
            "inadequate environmental monitoring",
        ],
    },
    "IAM": {
        "assets": [
            "Active Directory",
            "Okta SSO",
            "Privileged Access Workstations",
            "Service Account Vault",
            "HR Joiner/Mover/Leaver Workflow",
            "Password Reset Portal",
        ],
        "threats": [
            "credential stuffing",
            "privilege escalation",
            "insider misuse",
            "orphaned accounts",
            "phishing-based account takeover",
        ],
        "vulnerabilities": [
            "weak MFA enforcement",
            "over-privileged role assignments",
            "manual access reviews",
            "inconsistent deprovisioning",
            "shared administrative credentials",
        ],
    },
    "Network": {
        "assets": [
            "Core Firewall",
            "Remote Access VPN Gateway",
            "MPLS Connectivity",
            "Branch Office Network",
            "DNS Infrastructure",
            "Load Balancer Cluster",
        ],
        "threats": [
            "DDoS attack",
            "man-in-the-middle interception",
            "route hijacking",
            "malware propagation",
            "unauthorized network access",
        ],
        "vulnerabilities": [
            "insufficient network segmentation",
            "outdated firmware",
            "misconfigured firewall rules",
            "lack of anomaly monitoring",
            "unencrypted administrative access",
        ],
    },
    "Cloud": {
        "assets": [
            "Azure Active Directory",
            "Azure Storage Accounts",
            "Azure Kubernetes Service",
            "Azure Key Vault",
            "Azure SQL Database",
            "Azure API Management",
        ],
        "threats": [
            "cloud misconfiguration",
            "data exfiltration",
            "token compromise",
            "service outage",
            "malicious container image",
        ],
        "vulnerabilities": [
            "publicly exposed storage",
            "excessive permissions",
            "insufficient logging",
            "unreviewed infrastructure as code",
            "stale access keys",
        ],
    },
    "Third Party": {
        "assets": [
            "TPA Claims Processor",
            "Credit Scoring Vendor",
            "Email Marketing Platform",
            "Payment Processing Gateway",
            "Managed SOC",
            "Document Imaging Vendor",
        ],
        "threats": [
            "vendor data breach",
            "service-level agreement failure",
            "data mishandling",
            "subprocessor security incident",
            "unexpected service termination",
        ],
        "vulnerabilities": [
            "limited vendor oversight",
            "incomplete contract security clauses",
            "lack of continuous monitoring",
            "insufficient exit planning",
            "infrequent assurance reviews",
        ],
    },
    "Privacy": {
        "assets": [
            "Customer PII Repository",
            "GDPR Consent Records",
            "Call Center Recordings",
            "Claims Imaging Archive",
            "Analytics Data Lake",
            "Policyholder Portal",
        ],
        "threats": [
            "unauthorized access",
            "accidental disclosure",
            "data retention violation",
            "data subject request mishandling",
            "cross-border transfer non-compliance",
        ],
        "vulnerabilities": [
            "insufficient data classification",
            "manual redaction processes",
            "inconsistent retention schedules",
            "limited access monitoring",
            "incomplete privacy impact assessments",
        ],
    },
}


def _weighted_choice(rng: random.Random, options: List[int], weights: List[float]) -> int:
    """Return a weighted random choice from options."""

    return rng.choices(options, weights=weights, k=1)[0]


def generate_synthetic_risks(count: int = 50, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic insurance-sector IT and security risks."""

    rng = random.Random(seed)
    risk_rows: List[Dict[str, str | int]] = []

    categories = list(RISK_CATEGORIES.keys())
    likelihood_weights = [0.1, 0.2, 0.3, 0.25, 0.15]
    impact_weights = [0.05, 0.2, 0.3, 0.3, 0.15]

    for index in range(1, count + 1):
        category = rng.choice(categories)
        assets = RISK_CATEGORIES[category]["assets"]
        threats = RISK_CATEGORIES[category]["threats"]
        vulnerabilities = RISK_CATEGORIES[category]["vulnerabilities"]

        asset = rng.choice(assets)
        threat = rng.choice(threats)
        vulnerability = rng.choice(vulnerabilities)

        risk_name = f"{threat.capitalize()} impacting {asset}"
        likelihood = _weighted_choice(rng, [1, 2, 3, 4, 5], likelihood_weights)
        impact = _weighted_choice(rng, [1, 2, 3, 4, 5], impact_weights)
        control_exists = "Yes" if rng.random() < 0.7 else "No"
        control_effectiveness = (
            rng.choice(["Low", "Medium", "High"]) if control_exists == "Yes" else "Low"
        )

        risk_rows.append(
            {
                "Risk_ID": f"RISK-{index:03d}",
                "Risk_Name": risk_name,
                "Risk_Category": category,
                "Asset_Name": asset,
                "Threat_Description": threat,
                "Vulnerability_Description": vulnerability,
                "Likelihood": likelihood,
                "Impact": impact,
                "Control_Exists": control_exists,
                "Control_Effectiveness": control_effectiveness,
            }
        )

    return pd.DataFrame(risk_rows)


if __name__ == "__main__":
    data = generate_synthetic_risks()
    print(data.head(10).to_string(index=False))
