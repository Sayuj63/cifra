"""Reject impossible survey data before training."""

from __future__ import annotations

import pandas as pd

from ml.common import RAW
from ml.data.generate import CITY, EDUCATION, INDUSTRY, ROLE


def validate(frame: pd.DataFrame) -> dict:
    required = {
        "experience_years",
        "certifications",
        "education_level",
        "job_role",
        "industry",
        "city",
        "salary",
    }
    issues = []
    if not required.issubset(frame.columns):
        issues.append(f"missing columns: {sorted(required - set(frame.columns))}")
    else:
        for column, low, high in [("experience_years", 0, 45), ("certifications", 0, 15)]:
            if not frame[column].dropna().between(low, high).all():
                issues.append(f"{column} outside [{low}, {high}]")
        if frame.salary.isna().any() or not (frame.salary > 0).all():
            issues.append("salary missing or non-positive")
        for column, allowed in [
            ("education_level", EDUCATION),
            ("job_role", ROLE),
            ("industry", INDUSTRY),
            ("city", CITY),
        ]:
            if not set(frame[column].dropna()).issubset(allowed):
                issues.append(f"unknown {column}")
        if frame.duplicated().mean() > 0.01:
            issues.append("over 1% exact duplicates")
    if issues:
        raise ValueError("; ".join(issues))
    return {
        "rows": len(frame),
        "duplicates": int(frame.duplicated().sum()),
        "missing": frame.isna().sum().to_dict(),
        "valid": True,
    }


if __name__ == "__main__":
    print(validate(pd.read_csv(RAW)))
