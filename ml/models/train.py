"""Reproduce model selection, evaluation, calibration, and deployable artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import UTC, datetime

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import optuna
import pandas as pd
from sklearn.model_selection import train_test_split

from ml.common import ARTIFACTS, RAW, write_json
from ml.config import PARAMS
from ml.data.generate import CITY, EDUCATION, FEATURES, INDUSTRY, ROLE
from ml.data.validate import validate
from ml.evaluation.explainability import global_importance, reference_profile
from ml.evaluation.metrics import cv_metrics, metrics
from ml.models.definitions import NAMES, SEED, make_model


def split(frame: pd.DataFrame):
    train_rows = round(len(frame) * PARAMS["train_fraction"])
    test_rows = round(len(frame) * PARAMS["test_fraction"])
    train, holdout = train_test_split(frame, test_size=len(frame) - train_rows, random_state=SEED)
    calibration, test = train_test_split(holdout, test_size=test_rows, random_state=SEED)
    return train, calibration, test


def suggest(trial: optuna.Trial, name: str) -> dict:
    if name == "Decision Tree":
        return {
            "max_depth": trial.suggest_int("max_depth", 5, 18),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 3, 25),
            "min_samples_split": trial.suggest_int("min_samples_split", 6, 35),
        }
    if name == "Random Forest":
        return {
            "n_estimators": trial.suggest_int("n_estimators", 60, 140, step=40),
            "max_depth": trial.suggest_int("max_depth", 8, 18),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 2, 8),
            "min_samples_split": trial.suggest_int("min_samples_split", 4, 20),
        }
    return {
        "n_estimators": trial.suggest_int("n_estimators", 80, 180, step=50),
        "learning_rate": trial.suggest_float("learning_rate", 0.04, 0.16),
        "max_depth": trial.suggest_int("max_depth", 2, 4),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 2, 12),
        "min_samples_split": trial.suggest_int("min_samples_split", 4, 20),
        "subsample": trial.suggest_float("subsample", 0.75, 1.0),
    }


def residual_plots(y, prediction, experience) -> dict:
    residual = np.asarray(y) - prediction
    plots = ARTIFACTS / "plots"
    plots.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {"figure.figsize": (7, 4.5), "axes.spines.top": False, "axes.spines.right": False}
    )
    for label, x, xlabel in [
        ("residual_vs_predicted", prediction, "Predicted salary (INR/year)"),
        ("residual_vs_experience", experience, "Experience (years)"),
    ]:
        fig, ax = plt.subplots()
        ax.scatter(x, residual, s=8, alpha=0.35, color="#171717")
        ax.axhline(0, color="#FF5A1F", linewidth=1.5)
        ax.set(xlabel=xlabel, ylabel="Residual: actual - predicted (INR/year)")
        fig.tight_layout()
        fig.savefig(plots / f"{label}.png")
        plt.close(fig)
    fig, ax = plt.subplots()
    ax.hist(residual, bins=35, color="#FF5A1F")
    ax.set(xlabel="Residual (INR/year)", ylabel="Test candidates (count)")
    fig.tight_layout()
    fig.savefig(plots / "residual_histogram.png")
    plt.close(fig)
    return {
        "mean": float(np.mean(residual)),
        "std": float(np.std(residual)),
        "median": float(np.median(residual)),
        "p05": float(np.quantile(residual, 0.05)),
        "p95": float(np.quantile(residual, 0.95)),
        "correlation_abs_error_predicted": float(np.corrcoef(np.abs(residual), prediction)[0, 1]),
        "definition": "actual salary minus predicted salary, INR/year",
    }


def run(trials: int = 3) -> None:
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    frame = pd.read_csv(RAW)
    validate(frame)
    train, calibration, test = split(frame)
    x_train, y_train = train[FEATURES], train.salary
    x_cal, y_cal = calibration[FEATURES], calibration.salary
    x_test, y_test = test[FEATURES], test.salary
    schema = {
        "numeric": {
            "experience_years": {"min": 0, "max": 45},
            "certifications": {"min": 0, "max": 15},
        },
        "categorical": {
            "education_level": list(EDUCATION),
            "job_role": list(ROLE),
            "industry": list(INDUSTRY),
            "city": list(CITY),
        },
        "features": FEATURES,
        "target": "salary",
        "unit": "INR/year",
    }
    write_json(ARTIFACTS / "champion" / "feature_schema.json", schema)
    write_json(
        ARTIFACTS / "reports" / "split.json",
        {
            "train": len(train),
            "calibration": len(calibration),
            "test": len(test),
            "seed": SEED,
            "test_used_for_selection": False,
        },
    )
    comparison = []
    tuning = {}
    for name in NAMES:
        print(f"Cross-validating {name}", flush=True)
        baseline = cv_metrics(make_model(name), x_train, y_train)
        best_params = {}
        selected = baseline
        if name in {"Decision Tree", "Random Forest", "Gradient Boosting"} and trials > 0:
            study = optuna.create_study(
                direction="minimize", sampler=optuna.samplers.TPESampler(seed=SEED), study_name=name
            )

            def objective(trial: optuna.Trial, model_name: str = name) -> float:
                candidate = make_model(model_name, suggest(trial, model_name))
                return cv_metrics(candidate, x_train, y_train)["mean"]["rmse"]

            study.optimize(objective, n_trials=trials, show_progress_bar=False)
            tuning[name] = {
                "trials": trials,
                "best_params": study.best_params,
                "best_cv_rmse": study.best_value,
                "history": [
                    {"number": t.number, "rmse": t.value, "params": t.params} for t in study.trials
                ],
            }
            if study.best_value < baseline["mean"]["rmse"]:
                best_params = study.best_params
                selected = cv_metrics(make_model(name, best_params), x_train, y_train)
        comparison.append(
            {
                "model": name,
                "baseline": baseline,
                "cv": selected,
                "params": best_params,
                "status": "candidate",
            }
        )
    comparison.sort(
        key=lambda item: (item["cv"]["mean"]["rmse"], item["cv"]["mean"]["mae"], item["model"])
    )
    winner = comparison[0]
    winner["status"] = "champion"
    write_json(
        ARTIFACTS / "reports" / "model_comparison.json",
        {
            "selection": "lowest 5-fold training CV RMSE; ties by MAE then model name",
            "models": comparison,
            "champion": winner["model"],
        },
    )
    write_json(ARTIFACTS / "reports" / "tuning.json", tuning)
    print(f"Selected {winner['model']} on training CV", flush=True)
    model = make_model(winner["model"], winner["params"])
    model.fit(x_train, y_train)
    cal_pred = model.predict(x_cal)
    errors = np.abs(y_cal.to_numpy() - cal_pred)
    coverage_target = PARAMS["nominal_interval_coverage"]
    rank = int(np.ceil((len(errors) + 1) * coverage_target))
    radius = float(np.sort(errors)[min(rank - 1, len(errors) - 1)])
    test_pred = model.predict(x_test)
    test_metrics = metrics(y_test, test_pred)
    lower, upper = test_pred - radius, test_pred + radius
    coverage = float(np.mean((y_test >= lower) & (y_test <= upper)))
    residual = residual_plots(y_test, test_pred, test.experience_years)
    write_json(ARTIFACTS / "reports" / "residual_summary.json", residual)
    groups = []
    for city, group in test.groupby("city"):
        idx = test.index.get_indexer(group.index)
        observed = y_test.iloc[idx].to_numpy()
        predicted = test_pred[idx]
        groups.append(
            {
                "city": city,
                "n": len(group),
                **metrics(observed, predicted),
                "mean_residual": float(np.mean(observed - predicted)),
                "coverage": float(np.mean((observed >= lower[idx]) & (observed <= upper[idx]))),
            }
        )
    without_city = cv_metrics(
        make_model(winner["model"], winner["params"], include_city=False), x_train, y_train
    )
    ablation = {
        "with_city_cv_rmse": winner["cv"]["mean"]["rmse"],
        "without_city_cv_rmse": without_city["mean"]["rmse"],
        "delta_rmse": without_city["mean"]["rmse"] - winner["cv"]["mean"]["rmse"],
        "without_city_cv_mae": without_city["mean"]["mae"],
    }
    write_json(
        ARTIFACTS / "reports" / "fairness.json",
        {
            "by_city": groups,
            "ablation": ablation,
            "limitation": (
                "City diagnostics do not establish demographic fairness; "
                "protected-class labels are unavailable."
            ),
        },
    )
    reference = reference_profile(x_train)
    importance = global_importance(model, x_test, y_test)
    write_json(ARTIFACTS / "reports" / "importance.json", importance)
    experience_values = np.arange(0, 30.5, 0.5)
    curve = pd.DataFrame(
        [{**reference, "experience_years": float(year)} for year in experience_values]
    )
    linear = make_model("Linear Regression").fit(x_train, y_train)
    polynomial = make_model("Polynomial Regression").fit(x_train, y_train)
    growth = {
        "experience_years": experience_values.tolist(),
        "champion_inr": model.predict(curve).tolist(),
        "linear_inr": linear.predict(curve).tolist(),
        "polynomial_inr": polynomial.predict(curve).tolist(),
        "reference_profile": reference,
    }
    write_json(ARTIFACTS / "reports" / "growth_curve.json", growth)
    linear_row = next(item for item in comparison if item["model"] == "Linear Regression")
    poly_row = next(item for item in comparison if item["model"] == "Polynomial Regression")
    linearity = {
        "linear_cv_rmse": linear_row["cv"]["mean"]["rmse"],
        "polynomial_cv_rmse": poly_row["cv"]["mean"]["rmse"],
        "rmse_improvement_pct": 100
        * (linear_row["cv"]["mean"]["rmse"] - poly_row["cv"]["mean"]["rmse"])
        / linear_row["cv"]["mean"]["rmse"],
    }
    linearity["conclusion"] = (
        "A quadratic experience term improves CV RMSE over linear experience."
        if linearity["rmse_improvement_pct"] > 0
        else "The quadratic experience term does not improve CV RMSE."
    )
    write_json(ARTIFACTS / "reports" / "linearity.json", linearity)
    source_hash = hashlib.sha256(RAW.read_bytes()).hexdigest()
    metadata = {
        "model_family": winner["model"],
        "model_version": "1.0.0",
        "dataset_version": source_hash[:12],
        "dataset_sha256": source_hash,
        "trained_at": datetime.now(UTC).isoformat(),
        "features": FEATURES,
        "target": "salary",
        "currency": "INR/year",
        "random_seed": SEED,
        "calibration_method": "split conformal absolute residual quantile",
        "nominal_coverage": coverage_target,
        "calibration_rows": len(calibration),
        "interval_radius_inr": radius,
        "reference_profile": reference,
        "selected_params": winner["params"],
    }
    champion = ARTIFACTS / "champion"
    champion.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, champion / "model.joblib")
    write_json(champion / "metadata.json", metadata)
    write_json(
        champion / "metrics.json",
        {
            "test": test_metrics,
            "cross_validation": winner["cv"],
            "interval": {
                "nominal_coverage": coverage_target,
                "test_coverage": coverage,
                "radius_inr": radius,
            },
        },
    )
    write_json(
        ARTIFACTS / "reports" / "test_predictions.json",
        [
            {
                "actual_inr": float(a),
                "predicted_inr": float(p),
                "experience_years": None if pd.isna(e) else float(e),
            }
            for a, p, e in zip(y_test, test_pred, test.experience_years, strict=True)
        ],
    )
    if os.getenv("COMPLENS_WANDB") == "1":
        import wandb

        for item in comparison:
            slug = item["model"].lower().replace(" ", "-")
            with wandb.init(
                project=os.getenv("WANDB_PROJECT", "complens"),
                name=slug + "-v1",
                config={
                    "seed": SEED,
                    "dataset_hash": source_hash,
                    "model": item["model"],
                    "features": FEATURES,
                    "train_rows": len(train),
                    "calibration_rows": len(calibration),
                    "test_rows": len(test),
                    "cv_folds": PARAMS["cv_folds"],
                    "params": item["params"],
                    "tuning": tuning.get(item["model"]),
                },
            ) as run:
                run.log(
                    {
                        "cv_rmse": item["cv"]["mean"]["rmse"],
                        "cv_mse": item["cv"]["mean"]["mse"],
                        "cv_mae": item["cv"]["mean"]["mae"],
                        "cv_r2": item["cv"]["mean"]["r2"],
                        "cv_rmse_folds": item["cv"]["folds"]["rmse"],
                        "cv_mae_folds": item["cv"]["folds"]["mae"],
                        "cv_r2_folds": item["cv"]["folds"]["r2"],
                        "train_rmse": item["cv"]["train_rmse_mean"],
                        "fit_seconds_mean": item["cv"]["fit_seconds_mean"],
                    }
                )
                if item["status"] == "champion":
                    run.log(
                        {
                            "test_rmse": test_metrics["rmse"],
                            "test_mse": test_metrics["mse"],
                            "test_mae": test_metrics["mae"],
                            "test_r2": test_metrics["r2"],
                            "interval_coverage": coverage,
                            "residual_vs_predicted": wandb.Image(
                                str(ARTIFACTS / "plots" / "residual_vs_predicted.png")
                            ),
                            "residual_histogram": wandb.Image(
                                str(ARTIFACTS / "plots" / "residual_histogram.png")
                            ),
                            "predictions": wandb.Table(
                                columns=["actual_inr", "predicted_inr"],
                                data=[list(pair) for pair in zip(y_test, test_pred, strict=True)],
                            ),
                        }
                    )
                    artifact = wandb.Artifact("complens-champion", type="model", metadata=metadata)
                    artifact.add_dir(str(champion))
                    run.log_artifact(artifact)
                else:
                    candidates_dir = ARTIFACTS / "candidate_models"
                    candidates_dir.mkdir(parents=True, exist_ok=True)
                    candidate_path = candidates_dir / f"{slug}.joblib"
                    joblib.dump(
                        make_model(item["model"], item["params"]).fit(x_train, y_train),
                        candidate_path,
                    )
                    artifact = wandb.Artifact(
                        f"complens-{slug}",
                        type="model",
                        metadata={"dataset_sha256": source_hash, "cv": item["cv"]["mean"]},
                    )
                    artifact.add_file(str(candidate_path))
                    run.log_artifact(artifact)
    print(
        json.dumps(
            {"champion": winner["model"], "test": test_metrics, "coverage": coverage}, indent=2
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=PARAMS["optuna_trials_per_tree_family"])
    run(parser.parse_args().trials)
