"""Reference-profile exact Shapley values and global permutation importance."""

from __future__ import annotations

import math
from functools import lru_cache
from itertools import combinations

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.tree import DecisionTreeRegressor

from ml.config import PARAMS
from ml.data.generate import FEATURES

LABELS = {
    "experience_years": "Experience",
    "education_level": "Education",
    "job_role": "Job role",
    "industry": "Industry",
    "city": "City",
    "certifications": "Certifications",
}


def reference_profile(x: pd.DataFrame) -> dict:
    return {
        col: (
            float(x[col].median())
            if col in {"experience_years", "certifications"}
            else str(x[col].mode().iloc[0])
        )
        for col in FEATURES
    }


def exact_shapley(model, candidate: dict, reference: dict) -> dict:
    """Exact six-feature Shapley game using one explicit reference profile.

    Values explain the prediction relative to that profile, not a population average.
    """
    n = len(FEATURES)
    coalitions = []
    masks = []
    for size in range(n + 1):
        for chosen in combinations(range(n), size):
            mask = sum(1 << i for i in chosen)
            masks.append(mask)
            coalitions.append(
                {
                    feature: candidate[feature] if mask & (1 << i) else reference[feature]
                    for i, feature in enumerate(FEATURES)
                }
            )
    predictions = dict(zip(masks, model.predict(pd.DataFrame(coalitions)), strict=True))
    values = []
    for i, feature in enumerate(FEATURES):
        contribution = 0.0
        for mask in masks:
            if mask & (1 << i):
                continue
            k = mask.bit_count()
            weight = math.factorial(k) * math.factorial(n - k - 1) / math.factorial(n)
            contribution += weight * (predictions[mask | (1 << i)] - predictions[mask])
        values.append(
            {
                "feature": feature,
                "display_name": LABELS[feature],
                "contribution": float(contribution),
            }
        )
    return {
        "baseline": float(predictions[0]),
        "prediction": float(predictions[(1 << n) - 1]),
        "contributions": sorted(values, key=lambda item: abs(item["contribution"]), reverse=True),
        "method": "exact Shapley values against a fixed reference profile",
    }


@lru_cache(maxsize=1)
def shap_module():
    try:
        import shap
    except (ImportError, SyntaxError):
        return None
    return shap


def local_explanation(model, candidate: dict, reference: dict) -> dict:
    """Use Tree SHAP for supported champions, exact raw-feature Shapley otherwise."""
    estimator = model.named_steps["estimator"]
    shap = shap_module()
    if shap is None or not isinstance(
        estimator, (DecisionTreeRegressor, RandomForestRegressor, GradientBoostingRegressor)
    ):
        return exact_shapley(model, candidate, reference)

    preprocessor = model.named_steps["preprocess"]
    frame = pd.DataFrame([candidate])
    transformed = preprocessor.transform(frame)
    explainer = shap.TreeExplainer(estimator)
    values = np.asarray(explainer.shap_values(transformed)).reshape(-1)
    baseline = float(np.asarray(explainer.expected_value).reshape(-1)[0])
    names = preprocessor.get_feature_names_out()
    grouped = dict.fromkeys(FEATURES, 0.0)
    for name, value in zip(names, values, strict=True):
        feature = next(
            (
                key
                for key in FEATURES
                if name == key or name.startswith(key + "_") or name.startswith(key + "^")
            ),
            None,
        )
        if feature is None:
            raise ValueError(f"Cannot map transformed feature {name} to a raw input")
        grouped[feature] += float(value)
    prediction = float(model.predict(frame)[0])
    if not np.isclose(baseline + sum(grouped.values()), prediction, atol=1e-4):
        raise ValueError("Tree SHAP contributions do not sum to the pipeline prediction")
    contributions = [
        {"feature": key, "display_name": LABELS[key], "contribution": grouped[key]}
        for key in FEATURES
    ]
    return {
        "baseline": baseline,
        "prediction": prediction,
        "contributions": sorted(
            contributions, key=lambda item: abs(item["contribution"]), reverse=True
        ),
        "method": "Tree SHAP grouped by raw feature",
    }


def global_importance(model, x: pd.DataFrame, y: pd.Series) -> list[dict]:
    result = permutation_importance(
        model,
        x,
        y,
        n_repeats=3,
        random_state=PARAMS["seed"],
        scoring="neg_root_mean_squared_error",
        n_jobs=1,
    )
    return sorted(
        (
            {
                "feature": name,
                "display_name": LABELS[name],
                "rmse_increase_inr": float(importance),
                "std": float(std),
            }
            for name, importance, std in zip(
                FEATURES, result.importances_mean, result.importances_std, strict=True
            )
        ),
        key=lambda item: item["rmse_increase_inr"],
        reverse=True,
    )
