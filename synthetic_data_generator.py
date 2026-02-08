"""Synthetic risk data generator for insurance-focused GRC portfolio."""

from __future__ import annotations

import random
from typing import Dict, List


RISK_SCENARIOS = [
    {
        "Risk_Name": "Claims processing system outage",
        "Risk_Category": "Infrastructure",
        "Asset_Name": "Claims Processing Platform",
        "Threat_Description": "Data center power disruption or hardware failure",
        "Vulnerability_Description": "Single-site dependency without failover",
    },
    {
        "Risk_Name": "Policy administration database corruption",
        "Risk_Category": "Infrastructure",
        "Asset_Name": "Policy Administration Database",
        "Threat_Description": "Storage array failure or logical corruption",
        "Vulnerability_Description": "Backups not tested for full recovery",
    },
    {
        "Risk_Name": "Legacy underwriting server patch backlog",
        "Risk_Category": "Infrastructure",
        "Asset_Name": "Underwriting Application Server",
        "Threat_Description": "Exploitation of unpatched operating system",
        "Vulnerability_Description": "Delayed patch cycles for legacy systems",
    },
    {
        "Risk_Name": "Privileged account misuse",
        "Risk_Category": "IAM",
        "Asset_Name": "Privileged Access Management Vault",
        "Threat_Description": "Insider abuse of elevated access",
        "Vulnerability_Description": "Limited session monitoring",
    },
    {
        "Risk_Name": "Orphaned contractor accounts",
        "Risk_Category": "IAM",
        "Asset_Name": "Identity Governance Platform",
        "Threat_Description": "Unauthorized access via unused accounts",
        "Vulnerability_Description": "Incomplete offboarding workflow",
    },
    {
        "Risk_Name": "Multi-factor authentication bypass",
        "Risk_Category": "IAM",
        "Asset_Name": "Customer Service Portal",
        "Threat_Description": "Credential stuffing with legacy login endpoints",
        "Vulnerability_Description": "MFA not enforced for all user groups",
    },
    {
        "Risk_Name": "Internal network segmentation gaps",
        "Risk_Category": "Network",
        "Asset_Name": "Corporate LAN",
        "Threat_Description": "Lateral movement after phishing compromise",
        "Vulnerability_Description": "Flat network zones for back-office systems",
    },
    {
        "Risk_Name": "VPN concentrator capacity overload",
        "Risk_Category": "Network",
        "Asset_Name": "Remote Access VPN",
        "Threat_Description": "Denial of service during peak remote work",
        "Vulnerability_Description": "Limited redundancy for VPN gateways",
    },
    {
        "Risk_Name": "DNS service misconfiguration",
        "Risk_Category": "Network",
        "Asset_Name": "Corporate DNS",
        "Threat_Description": "Spoofing leading to traffic interception",
        "Vulnerability_Description": "Change control gaps for DNS updates",
    },
    {
        "Risk_Name": "Azure storage account exposure",
        "Risk_Category": "Cloud",
        "Asset_Name": "Azure Blob Storage",
        "Threat_Description": "Public access to policy documents",
        "Vulnerability_Description": "Misconfigured access policies",
    },
    {
        "Risk_Name": "Cloud key vault access drift",
        "Risk_Category": "Cloud",
        "Asset_Name": "Azure Key Vault",
        "Threat_Description": "Unauthorized secret access",
        "Vulnerability_Description": "Role assignments not reviewed",
    },
    {
        "Risk_Name": "Cloud workload logging gaps",
        "Risk_Category": "Cloud",
        "Asset_Name": "Azure Monitor",
        "Threat_Description": "Delayed detection of suspicious activity",
        "Vulnerability_Description": "Incomplete diagnostic settings",
    },
    {
        "Risk_Name": "Third-party claims adjuster breach",
        "Risk_Category": "Third Party",
        "Asset_Name": "Claims Adjuster API",
        "Threat_Description": "Vendor system compromise",
        "Vulnerability_Description": "Limited security assurance reporting",
    },
    {
        "Risk_Name": "Vendor data transfer encryption failure",
        "Risk_Category": "Third Party",
        "Asset_Name": "SFTP Data Exchange",
        "Threat_Description": "Interception of claims data",
        "Vulnerability_Description": "Legacy cipher suites in use",
    },
    {
        "Risk_Name": "Third-party business continuity gaps",
        "Risk_Category": "Third Party",
        "Asset_Name": "Outsourced Call Center",
        "Threat_Description": "Service disruption during regional outage",
        "Vulnerability_Description": "No contractual recovery time objectives",
    },
    {
        "Risk_Name": "GDPR data subject request delays",
        "Risk_Category": "Privacy",
        "Asset_Name": "Data Subject Request Workflow",
        "Threat_Description": "Regulatory penalties for missed deadlines",
        "Vulnerability_Description": "Manual tracking of requests",
    },
    {
        "Risk_Name": "PII leakage via email",
        "Risk_Category": "Privacy",
        "Asset_Name": "Email Gateway",
        "Threat_Description": "Accidental disclosure of customer data",
        "Vulnerability_Description": "Data loss prevention rules not tuned",
    },
    {
        "Risk_Name": "Customer portal session hijack",
        "Risk_Category": "IAM",
        "Asset_Name": "Customer Self-Service Portal",
        "Threat_Description": "Session token theft",
        "Vulnerability_Description": "Inadequate session timeout policies",
    },
    {
        "Risk_Name": "Claims analytics model drift",
        "Risk_Category": "Infrastructure",
        "Asset_Name": "Claims Analytics Platform",
        "Threat_Description": "Incorrect claim triage decisions",
        "Vulnerability_Description": "Model monitoring not implemented",
    },
    {
        "Risk_Name": "Ransomware infection via phishing",
        "Risk_Category": "Infrastructure",
        "Asset_Name": "Employee Endpoints",
        "Threat_Description": "Encryption of shared drives",
        "Vulnerability_Description": "Inconsistent endpoint detection coverage",
    },
    {
        "Risk_Name": "API rate limiting absent",
        "Risk_Category": "Network",
        "Asset_Name": "Claims Submission API",
        "Threat_Description": "Abuse leading to degraded service",
        "Vulnerability_Description": "No throttling controls",
    },
    {
        "Risk_Name": "Backup retention noncompliance",
        "Risk_Category": "Infrastructure",
        "Asset_Name": "Backup Vault",
        "Threat_Description": "Inability to recover historical data",
        "Vulnerability_Description": "Retention policies not aligned to policy",
    },
    {
        "Risk_Name": "Shadow IT SaaS usage",
        "Risk_Category": "Cloud",
        "Asset_Name": "Unsanctioned SaaS Apps",
        "Threat_Description": "Data leakage to unmanaged services",
        "Vulnerability_Description": "Limited cloud access security broker coverage",
    },
    {
        "Risk_Name": "Endpoint encryption gaps",
        "Risk_Category": "Infrastructure",
        "Asset_Name": "Underwriter Laptops",
        "Threat_Description": "Loss or theft of devices",
        "Vulnerability_Description": "Full-disk encryption not enforced",
    },
    {
        "Risk_Name": "Cloud workload patching gaps",
        "Risk_Category": "Cloud",
        "Asset_Name": "Azure VM Fleet",
        "Threat_Description": "Exploitation of known vulnerabilities",
        "Vulnerability_Description": "Patch schedules not automated",
    },
    {
        "Risk_Name": "Insider data export via USB",
        "Risk_Category": "Privacy",
        "Asset_Name": "Claims Operations Workstations",
        "Threat_Description": "Unauthorized data extraction",
        "Vulnerability_Description": "USB device controls not enforced",
    },
    {
        "Risk_Name": "Active Directory replication issues",
        "Risk_Category": "IAM",
        "Asset_Name": "Active Directory",
        "Threat_Description": "Authentication failures",
        "Vulnerability_Description": "Aging domain controllers",
    },
    {
        "Risk_Name": "Telephony system outage",
        "Risk_Category": "Infrastructure",
        "Asset_Name": "Call Center Telephony",
        "Threat_Description": "Service disruption impacting customer support",
        "Vulnerability_Description": "Single vendor dependency",
    },
    {
        "Risk_Name": "Zero trust network initiative delay",
        "Risk_Category": "Network",
        "Asset_Name": "Network Security Program",
        "Threat_Description": "Expanded attack surface",
        "Vulnerability_Description": "Project resource constraints",
    },
    {
        "Risk_Name": "Data retention policy mismatch",
        "Risk_Category": "Privacy",
        "Asset_Name": "Document Management System",
        "Threat_Description": "Regulatory noncompliance for record retention",
        "Vulnerability_Description": "Retention rules inconsistently applied",
    },
    {
        "Risk_Name": "SOC alert fatigue",
        "Risk_Category": "Infrastructure",
        "Asset_Name": "Security Operations Center",
        "Threat_Description": "Delayed incident response",
        "Vulnerability_Description": "High volume of low-fidelity alerts",
    },
    {
        "Risk_Name": "Cloud service provider outage",
        "Risk_Category": "Cloud",
        "Asset_Name": "Azure App Services",
        "Threat_Description": "Service disruption of customer portals",
        "Vulnerability_Description": "Limited multi-region deployment",
    },
    {
        "Risk_Name": "Third-party software supply chain",
        "Risk_Category": "Third Party",
        "Asset_Name": "Vendor Software Updates",
        "Threat_Description": "Malicious update insertion",
        "Vulnerability_Description": "Lack of code signing validation",
    },
    {
        "Risk_Name": "Data warehouse access over-provisioned",
        "Risk_Category": "IAM",
        "Asset_Name": "Enterprise Data Warehouse",
        "Threat_Description": "Unauthorized analytics access",
        "Vulnerability_Description": "Role-based access not reviewed",
    },
    {
        "Risk_Name": "Email spoofing attacks",
        "Risk_Category": "Network",
        "Asset_Name": "Email Infrastructure",
        "Threat_Description": "Business email compromise",
        "Vulnerability_Description": "DMARC not enforced",
    },
    {
        "Risk_Name": "Customer identity verification failures",
        "Risk_Category": "IAM",
        "Asset_Name": "KYC Verification Service",
        "Threat_Description": "Fraudulent claims submission",
        "Vulnerability_Description": "Automated checks lack manual review",
    },
    {
        "Risk_Name": "Claims file transfer delay",
        "Risk_Category": "Network",
        "Asset_Name": "Secure File Transfer Gateway",
        "Threat_Description": "Delayed processing due to network congestion",
        "Vulnerability_Description": "Bandwidth allocation not optimized",
    },
    {
        "Risk_Name": "Disaster recovery test gaps",
        "Risk_Category": "Infrastructure",
        "Asset_Name": "Disaster Recovery Site",
        "Threat_Description": "Failure to recover critical systems",
        "Vulnerability_Description": "Incomplete recovery testing",
    },
    {
        "Risk_Name": "Cloud cost governance drift",
        "Risk_Category": "Cloud",
        "Asset_Name": "Azure Subscription Management",
        "Threat_Description": "Uncontrolled cloud spend",
        "Vulnerability_Description": "Tagging standards not enforced",
    },
    {
        "Risk_Name": "Third-party privacy breach notification",
        "Risk_Category": "Third Party",
        "Asset_Name": "Marketing Analytics Vendor",
        "Threat_Description": "Delayed breach notification",
        "Vulnerability_Description": "Contract lacks notification SLA",
    },
    {
        "Risk_Name": "Unencrypted data at rest",
        "Risk_Category": "Privacy",
        "Asset_Name": "Claims Archive Storage",
        "Threat_Description": "Data exposure from storage compromise",
        "Vulnerability_Description": "Encryption controls not enabled",
    },
    {
        "Risk_Name": "Network firewall rule sprawl",
        "Risk_Category": "Network",
        "Asset_Name": "Perimeter Firewalls",
        "Threat_Description": "Unauthorized access through legacy rules",
        "Vulnerability_Description": "Rule base not reviewed",
    },
    {
        "Risk_Name": "IAM logging gaps",
        "Risk_Category": "IAM",
        "Asset_Name": "Identity and Access Logs",
        "Threat_Description": "Inability to detect anomalous access",
        "Vulnerability_Description": "Log retention below policy",
    },
    {
        "Risk_Name": "Cloud backup misconfiguration",
        "Risk_Category": "Cloud",
        "Asset_Name": "Azure Backup",
        "Threat_Description": "Data loss during recovery",
        "Vulnerability_Description": "Backup schedules not validated",
    },
    {
        "Risk_Name": "Third-party API authentication weakness",
        "Risk_Category": "Third Party",
        "Asset_Name": "Partner API Gateway",
        "Threat_Description": "Unauthorized API access",
        "Vulnerability_Description": "API keys shared across clients",
    },
    {
        "Risk_Name": "Privacy notice update delays",
        "Risk_Category": "Privacy",
        "Asset_Name": "Customer Communication Templates",
        "Threat_Description": "Regulatory scrutiny",
        "Vulnerability_Description": "Manual legal review backlog",
    },
    {
        "Risk_Name": "Insufficient log aggregation",
        "Risk_Category": "Infrastructure",
        "Asset_Name": "SIEM Platform",
        "Threat_Description": "Delayed detection of threat campaigns",
        "Vulnerability_Description": "Not all critical sources onboarded",
    },
    {
        "Risk_Name": "Network device firmware lag",
        "Risk_Category": "Network",
        "Asset_Name": "Core Routers",
        "Threat_Description": "Exploitation of known firmware vulnerabilities",
        "Vulnerability_Description": "Firmware updates deferred",
    },
    {
        "Risk_Name": "IAM role explosion in cloud",
        "Risk_Category": "IAM",
        "Asset_Name": "Azure AD Roles",
        "Threat_Description": "Excess permissions across subscriptions",
        "Vulnerability_Description": "Lack of role design standards",
    },
]


def _risk_id(index: int) -> str:
    return f"RISK-{index:03d}"


def generate_synthetic_risks(count: int = 40, seed: int = 42) -> List[Dict[str, str]]:
    """Generate a list of synthetic insurance risk records."""

    random.seed(seed)
    scenarios = RISK_SCENARIOS.copy()
    random.shuffle(scenarios)

    records = []
    for index, scenario in enumerate(scenarios[:count], start=1):
        likelihood = random.randint(2, 5)
        impact = random.randint(2, 5)
        control_exists = random.choice(["Yes", "Yes", "No"])
        control_effectiveness = "Low"
        if control_exists == "Yes":
            control_effectiveness = random.choice(["Low", "Medium", "High"])

        records.append(
            {
                "Risk_ID": _risk_id(index),
                **scenario,
                "Likelihood": likelihood,
                "Impact": impact,
                "Control_Exists": control_exists,
                "Control_Effectiveness": control_effectiveness,
            }
        )

    return records


if __name__ == "__main__":
    generated = generate_synthetic_risks()
    for record in generated[:5]:
        print(record)
