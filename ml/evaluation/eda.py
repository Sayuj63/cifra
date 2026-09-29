"""Reproducible EDA assets with labeled INR/year axes."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from ml.common import ARTIFACTS, RAW, write_json
from ml.config import PARAMS


def build() -> None:
    df = pd.read_csv(RAW)
    plots = ARTIFACTS / "plots"
    plots.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "figure.figsize": (8, 4.5),
            "axes.spines.top": False,
            "axes.spines.right": False,
            "font.size": 10,
        }
    )
    fig, ax = plt.subplots()
    ax.hist(df.salary, bins=40, color="#FF5A1F")
    ax.set(
        xlabel="Annual salary (INR/year)", ylabel="Candidates (count)", title="Salary distribution"
    )
    fig.tight_layout()
    fig.savefig(plots / "salary_distribution.png")
    plt.close(fig)
    fig, ax = plt.subplots()
    sample = df.sample(min(2500, len(df)), random_state=PARAMS["seed"])
    ax.scatter(sample.experience_years, sample.salary, s=6, alpha=0.22, color="#171717")
    ax.set(
        xlabel="Experience (years)", ylabel="Annual salary (INR/year)", title="Salary vs experience"
    )
    fig.tight_layout()
    fig.savefig(plots / "salary_vs_experience.png")
    plt.close(fig)
    for column in ["education_level", "job_role", "industry", "city"]:
        group = df.groupby(column).salary.median().sort_values()
        fig, ax = plt.subplots()
        group.plot.barh(ax=ax, color="#FF5A1F")
        ax.set(xlabel="Median annual salary (INR/year)", ylabel=column.replace("_", " ").title())
        fig.tight_layout()
        fig.savefig(plots / f"salary_by_{column}.png")
        plt.close(fig)
    fig, ax = plt.subplots()
    df.certifications.hist(ax=ax, bins=9, color="#FF5A1F")
    ax.set(xlabel="Certifications (count)", ylabel="Candidates (count)")
    fig.tight_layout()
    fig.savefig(plots / "certifications.png")
    plt.close(fig)
    report = {
        "rows": len(df),
        "missing_pct": (100 * df.isna().mean()).round(2).to_dict(),
        "salary_by_role": df.groupby("job_role").salary.median().to_dict(),
        "salary_by_city": df.groupby("city").salary.median().to_dict(),
        "salary_by_industry": df.groupby("industry").salary.median().to_dict(),
        "salary_by_education": df.groupby("education_level").salary.median().to_dict(),
        "salary_summary": df.salary.describe().to_dict(),
        "experience_salary_correlation": float(
            df[["experience_years", "salary"]].corr().iloc[0, 1]
        ),
    }
    write_json(ARTIFACTS / "reports" / "eda.json", report)


if __name__ == "__main__":
    build()
