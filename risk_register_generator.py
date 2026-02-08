"""Risk register automation for a fictional insurance company."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd
from openpyxl.drawing.image import Image as ExcelImage

from synthetic_data_generator import generate_synthetic_risks


OUTPUT_FILE = "Insurance_Risk_Register.xlsx"
CHART_FILE = "risk_distribution.png"


@dataclass
class RiskSummary:
    total_risks: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int


def calculate_risk_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate raw and adjusted risk scores along with risk levels."""

    df = df.copy()
    df["Risk_Score"] = df["Likelihood"] * df["Impact"]

    adjustment_map = {
        "High": 0.5,
        "Medium": 0.7,
        "Low": 0.9,
    }

    def apply_adjustment(row: pd.Series) -> float:
        if row["Control_Exists"] == "Yes":
            return row["Risk_Score"] * adjustment_map[row["Control_Effectiveness"]]
        return float(row["Risk_Score"])

    df["Adjusted_Risk_Score"] = df.apply(apply_adjustment, axis=1).round(2)

    def classify_level(score: float) -> str:
        if score <= 5:
            return "Low"
        if score <= 12:
            return "Medium"
        return "High"

    df["Risk_Level"] = df["Adjusted_Risk_Score"].apply(classify_level)
    return df


def build_executive_summary(df: pd.DataFrame) -> Dict[str, object]:
    """Build executive summary metrics and top risks."""

    summary = RiskSummary(
        total_risks=len(df),
        high_risk_count=int((df["Risk_Level"] == "High").sum()),
        medium_risk_count=int((df["Risk_Level"] == "Medium").sum()),
        low_risk_count=int((df["Risk_Level"] == "Low").sum()),
    )

    top_risks = (
        df.sort_values(by="Adjusted_Risk_Score", ascending=False)
        .head(5)
        .loc[:, ["Risk_ID", "Risk_Name", "Risk_Category", "Adjusted_Risk_Score", "Risk_Level"]]
    )

    metrics = pd.DataFrame(
        [
            ["Total Risks", summary.total_risks],
            ["High Risk Count", summary.high_risk_count],
            ["Medium Risk Count", summary.medium_risk_count],
            ["Low Risk Count", summary.low_risk_count],
        ],
        columns=["Metric", "Value"],
    )

    return {"metrics": metrics, "top_risks": top_risks}


def create_risk_distribution_chart(df: pd.DataFrame, output_path: Path) -> None:
    """Create a simple bar chart for risk level distribution."""

    distribution = df["Risk_Level"].value_counts().reindex(["High", "Medium", "Low"]).fillna(0)
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(distribution.index, distribution.values, color=["#d62728", "#ff7f0e", "#2ca02c"])
    ax.set_title("Risk Level Distribution")
    ax.set_xlabel("Risk Level")
    ax.set_ylabel("Count")

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{int(height)}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def export_to_excel(
    raw_df: pd.DataFrame,
    calculated_df: pd.DataFrame,
    summary: Dict[str, object],
    output_file: Path,
    chart_file: Path,
) -> None:
    """Export raw, calculated, and summary data to Excel."""

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        raw_df.to_excel(writer, sheet_name="Raw_Risks", index=False)
        calculated_df.to_excel(writer, sheet_name="Calculated_Risks", index=False)
        summary["metrics"].to_excel(writer, sheet_name="Executive_Summary", index=False, startrow=0)
        summary["top_risks"].to_excel(writer, sheet_name="Executive_Summary", index=False, startrow=7)

        worksheet = writer.book["Executive_Summary"]
        worksheet["A7"] = "Top 5 Risks by Adjusted Score"

        if chart_file.exists():
            image = ExcelImage(str(chart_file))
            image.anchor = "E2"
            worksheet.add_image(image)


def main() -> None:
    """Generate risk register data and export to Excel."""

    raw_risks = generate_synthetic_risks(count=50, seed=42)
    calculated_risks = calculate_risk_scores(raw_risks)
    summary = build_executive_summary(calculated_risks)

    chart_path = Path(CHART_FILE)
    create_risk_distribution_chart(calculated_risks, chart_path)

    export_to_excel(
        raw_df=raw_risks,
        calculated_df=calculated_risks,
        summary=summary,
        output_file=Path(OUTPUT_FILE),
        chart_file=chart_path,
    )

    print(f"Excel risk register saved to {OUTPUT_FILE}")
    print(f"Risk distribution chart saved to {CHART_FILE}")


if __name__ == "__main__":
    main()
