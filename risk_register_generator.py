"""Risk register automation for an insurance company portfolio artifact."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd

from synthetic_data_generator import generate_synthetic_risks


@dataclass
class RiskSummary:
    total_risks: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int


def adjust_risk_score(base_score: int, control_exists: str, effectiveness: str) -> float:
    """Adjust risk score based on control effectiveness."""

    if control_exists != "Yes":
        return float(base_score)

    reduction_map = {"High": 0.5, "Medium": 0.3, "Low": 0.1}
    reduction = reduction_map.get(effectiveness, 0.0)
    return round(base_score * (1 - reduction), 2)


def risk_level(score: float) -> str:
    if score <= 5:
        return "Low"
    if score <= 12:
        return "Medium"
    return "High"


def build_risk_register(count: int = 40) -> pd.DataFrame:
    """Build a calculated risk register dataframe."""

    raw_records = generate_synthetic_risks(count=count)
    raw_df = pd.DataFrame(raw_records)

    raw_df["Base_Risk_Score"] = raw_df["Likelihood"] * raw_df["Impact"]
    raw_df["Adjusted_Risk_Score"] = raw_df.apply(
        lambda row: adjust_risk_score(
            row["Base_Risk_Score"], row["Control_Exists"], row["Control_Effectiveness"]
        ),
        axis=1,
    )
    raw_df["Risk_Level"] = raw_df["Adjusted_Risk_Score"].apply(risk_level)

    return raw_df


def summarize_risks(df: pd.DataFrame) -> RiskSummary:
    counts = df["Risk_Level"].value_counts()
    return RiskSummary(
        total_risks=len(df),
        high_risk_count=int(counts.get("High", 0)),
        medium_risk_count=int(counts.get("Medium", 0)),
        low_risk_count=int(counts.get("Low", 0)),
    )


def build_executive_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = summarize_risks(df)

    summary_rows: List[Dict[str, str | int]] = [
        {"Metric": "Total Risks", "Value": summary.total_risks},
        {"Metric": "High Risk Count", "Value": summary.high_risk_count},
        {"Metric": "Medium Risk Count", "Value": summary.medium_risk_count},
        {"Metric": "Low Risk Count", "Value": summary.low_risk_count},
    ]

    top_risks = (
        df.sort_values(by="Adjusted_Risk_Score", ascending=False)
        .head(5)
        .loc[:, ["Risk_ID", "Risk_Name", "Adjusted_Risk_Score", "Risk_Level"]]
    )

    summary_df = pd.DataFrame(summary_rows)

    return summary_df, top_risks


def save_risk_distribution_chart(df: pd.DataFrame, output_path: Path) -> None:
    counts = df["Risk_Level"].value_counts().reindex(["High", "Medium", "Low"]).fillna(0)

    plt.figure(figsize=(6, 4))
    bars = plt.bar(counts.index, counts.values, color=["#d9534f", "#f0ad4e", "#5cb85c"])
    plt.title("Risk Distribution by Level")
    plt.xlabel("Risk Level")
    plt.ylabel("Count")
    plt.bar_label(bars)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def export_to_excel(raw_df: pd.DataFrame, output_file: Path) -> None:
    calculated_df = raw_df.copy()
    summary_df, top_risks_df = build_executive_summary(calculated_df)

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        raw_df.drop(columns=["Base_Risk_Score", "Adjusted_Risk_Score", "Risk_Level"]).to_excel(
            writer, sheet_name="Raw_Risks", index=False
        )
        calculated_df.to_excel(writer, sheet_name="Calculated_Risks", index=False)
        summary_df.to_excel(writer, sheet_name="Executive_Summary", index=False)

        start_row = len(summary_df) + 2
        top_risks_df.to_excel(writer, sheet_name="Executive_Summary", index=False, startrow=start_row)


def main() -> None:
    output_file = Path("Insurance_Risk_Register.xlsx")
    chart_file = Path("risk_distribution.png")

    risk_register_df = build_risk_register(count=40)
    export_to_excel(risk_register_df, output_file)
    save_risk_distribution_chart(risk_register_df, chart_file)

    print("Risk register generated:")
    print(f"- Excel workbook: {output_file.resolve()}")
    print(f"- Chart: {chart_file.resolve()}")


if __name__ == "__main__":
    main()
