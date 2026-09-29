"""Common metric and cross-validation definitions."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate

from ml.config import PARAMS
from ml.models.definitions import SEED

CV = KFold(n_splits=PARAMS["cv_folds"], shuffle=True, random_state=SEED)
SCORING = {
    "r2": "r2",
    "mse": "neg_mean_squared_error",
    "rmse": "neg_root_mean_squared_error",
    "mae": "neg_mean_absolute_error",
}


def metrics(y_true, prediction) -> dict[str, float]:
    mse = mean_squared_error(y_true, prediction)
    return {
        "r2": float(r2_score(y_true, prediction)),
        "mse": float(mse),
        "rmse": float(np.sqrt(mse)),
        "mae": float(mean_absolute_error(y_true, prediction)),
    }


def cv_metrics(model, x, y) -> dict:
    result = cross_validate(
        model, x, y, cv=CV, scoring=SCORING, n_jobs=1, return_train_score=True, error_score="raise"
    )
    output = {"folds": {}, "mean": {}, "std": {}}
    for key in SCORING:
        values = result[f"test_{key}"] * (-1 if key != "r2" else 1)
        output["folds"][key] = [float(v) for v in values]
        output["mean"][key] = float(np.mean(values))
        output["std"][key] = float(np.std(values))
    output["train_rmse_mean"] = float(np.mean(-result["train_rmse"]))
    output["generalization_gap"] = output["mean"]["rmse"] - output["train_rmse_mean"]
    output["fit_seconds_mean"] = float(np.mean(result["fit_time"]))
    return output
