"""Deterministic educational salary survey generator."""

from __future__ import annotations

import argparse
import hashlib

import numpy as np
import pandas as pd

from ml.common import ARTIFACTS, RAW, write_json
from ml.config import PARAMS

EDUCATION = {"High School": -50_000, "Bachelor's": 0, "Master's": 120_000, "PhD": 180_000}
ROLE = {
    "Data Analyst": 500_000,
    "Business Analyst": 550_000,
    "Software Engineer": 650_000,
    "DevOps Engineer": 700_000,
    "Cybersecurity Engineer": 720_000,
    "Data Scientist": 750_000,
    "ML Engineer": 800_000,
    "Product Manager": 850_000,
}
INDUSTRY = {
    "Technology": 40_000,
    "FinTech": 110_000,
    "Healthcare": 0,
    "E-commerce": 55_000,
    "Consulting": 30_000,
    "Manufacturing": -45_000,
    "Telecom": -10_000,
}
CITY = {
    "Bengaluru": 100_000,
    "Mumbai": 90_000,
    "Delhi NCR": 70_000,
    "Hyderabad": 50_000,
    "Pune": 40_000,
    "Chennai": 25_000,
    "Kolkata": 0,
    "Ahmedabad": -15_000,
}
FEATURES = ["experience_years", "education_level", "job_role", "industry", "city", "certifications"]


def generate(n: int = PARAMS["rows"], seed: int = PARAMS["seed"]) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    groups = rng.choice(3, n, p=[0.69, 0.25, 0.06])
    experience = np.where(
        groups == 0,
        rng.beta(1.6, 2.0, n) * 12,
        np.where(groups == 1, 12 + rng.beta(1.3, 2.5, n) * 10, 22 + rng.beta(1.2, 2.0, n) * 13),
    ).round(1)
    education = rng.choice(list(EDUCATION), n, p=[0.08, 0.52, 0.34, 0.06])
    role = rng.choice(list(ROLE), n, p=[0.17, 0.11, 0.20, 0.11, 0.09, 0.14, 0.10, 0.08])
    industry = rng.choice(list(INDUSTRY), n)
    city = rng.choice(list(CITY), n, p=[0.21, 0.17, 0.13, 0.15, 0.12, 0.10, 0.07, 0.05])
    certificates = np.clip(rng.poisson(1.8, n), 0, 8).astype(float)
    role_growth = {
        name: gain
        for name, gain in zip(ROLE, [0.85, 0.90, 1.08, 1.05, 1.04, 1.13, 1.18, 1.12], strict=True)
    }
    base = np.array([ROLE[x] for x in role], dtype=float)
    expected = (
        base
        + np.array([EDUCATION[x] for x in education])
        + np.array([INDUSTRY[x] for x in industry])
        + np.array([CITY[x] for x in city])
        + certificates * 24_000
        + 920_000 * (1 - np.exp(-experience / 8.5)) * np.array([role_growth[x] for x in role])
    )
    noise = rng.normal(0, 40_000 + 0.05 * expected)
    outliers = rng.random(n) < 0.015
    noise[outliers] += rng.normal(0, 260_000, outliers.sum())
    salary = np.maximum(150_000, expected + noise).round().astype(int)
    # Missingness is applied only after salary is generated from clean features.
    experience[rng.random(n) < 0.02] = np.nan
    certificates[rng.random(n) < 0.04] = np.nan
    return pd.DataFrame(
        {
            "experience_years": experience,
            "education_level": education,
            "job_role": role,
            "industry": industry,
            "city": city,
            "certifications": certificates,
            "salary": salary,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=PARAMS["rows"])
    parser.add_argument("--seed", type=int, default=PARAMS["seed"])
    args = parser.parse_args()
    frame = generate(args.rows, args.seed)
    RAW.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(RAW, index=False, float_format="%.3f")
    digest = hashlib.sha256(RAW.read_bytes()).hexdigest()
    profile = {
        "rows": len(frame),
        "features": FEATURES,
        "target": "salary",
        "currency": "INR/year",
        "seed": args.seed,
        "sha256": digest,
        "missing_pct": (100 * frame.isna().mean()).round(2).to_dict(),
        "salary_summary": frame.salary.describe().round(2).to_dict(),
        "provenance": "Deterministic synthetic educational data; not market benchmarks.",
    }
    write_json(ARTIFACTS / "reports" / "data_profile.json", profile)
    write_json(ARTIFACTS / "reports" / "missingness.json", profile["missing_pct"])
    print(f"Generated {len(frame)} rows; SHA256 {digest}")


if __name__ == "__main__":
    main()
