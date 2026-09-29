"""The five required regressors, all with fold-local preprocessing."""

from __future__ import annotations

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor

from ml.config import PARAMS
from ml.data.preprocess import preprocess

SEED = PARAMS["seed"]


def make_model(name: str, params: dict | None = None, include_city: bool = True) -> Pipeline:
    params = params or {}
    estimators = {
        "Linear Regression": LinearRegression,
        "Polynomial Regression": LinearRegression,
        "Decision Tree": DecisionTreeRegressor,
        "Random Forest": RandomForestRegressor,
        "Gradient Boosting": GradientBoostingRegressor,
    }
    if name not in estimators:
        raise ValueError(f"unknown model: {name}")
    if name in {"Decision Tree", "Random Forest", "Gradient Boosting"}:
        params = {"random_state": SEED, **params}
    return Pipeline(
        [
            ("preprocess", preprocess(name == "Polynomial Regression", include_city)),
            ("estimator", estimators[name](**params)),
        ]
    )


NAMES = [
    "Linear Regression",
    "Polynomial Regression",
    "Decision Tree",
    "Random Forest",
    "Gradient Boosting",
]
