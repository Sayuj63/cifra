"""Fold-local preprocessing for each candidate estimator."""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler


def preprocess(polynomial: bool = False, include_city: bool = True) -> ColumnTransformer:
    experience_steps = [("impute", SimpleImputer(strategy="median"))]
    if polynomial:
        experience_steps.append(("polynomial", PolynomialFeatures(degree=2, include_bias=False)))
    experience_steps.append(("scale", StandardScaler()))
    categories = ["education_level", "job_role", "industry"] + (["city"] if include_city else [])
    return ColumnTransformer(
        [
            ("experience", Pipeline(experience_steps), ["experience_years"]),
            (
                "certifications",
                Pipeline(
                    [("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
                ),
                ["certifications"],
            ),
            (
                "categories",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                    ]
                ),
                categories,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
