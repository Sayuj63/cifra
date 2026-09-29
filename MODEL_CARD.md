# CompLens Model Card

## Model identity

- Version: 1.0.0
- Champion: Gradient Boosting
- Dataset SHA-256: `4c4608134b8e0c1e80e7ef1b409236adc3ef515406914ac3a6de435082b5c965`
- Training timestamp (UTC): 2026-09-29T04:05:58.733641+00:00
- Task: annual salary regression in INR/year

## Intended use

Demonstrate reproducible salary estimation for an academic case study using synthetic Indian candidate profiles. The output is an educational benchmark, not a real compensation offer or market quote.

## Inputs and training data

Features: experience years, education level, job role, industry, city, and certification count. The deterministic generator creates 7,500 rows with nonlinear experience growth, role interactions, salary-dependent noise, and controlled missingness. It is not a real survey.

## Evaluation

One deterministic 70/15/15 train/calibration/test split, seed 42. Model selection uses five shuffled training folds and lowest mean CV RMSE. The test partition is held out from selection.

| Model | CV R² | CV RMSE (INR/year) | CV MAE (INR/year) |
|---|---:|---:|---:|
| Gradient Boosting | 0.847 | ₹1.26L | ₹0.96L |
| Polynomial Regression | 0.845 | ₹1.27L | ₹0.97L |
| Random Forest | 0.823 | ₹1.35L | ₹1.04L |
| Linear Regression | 0.776 | ₹1.52L | ₹1.18L |
| Decision Tree | 0.774 | ₹1.53L | ₹1.19L |

Champion held-out test: R² 0.850; MSE 15,642,917,410 INR²; RMSE ₹1.25L/year; MAE ₹0.97L/year.

## Prediction uncertainty

The interval uses the finite-sample split-conformal absolute residual quantile on 1,125 separate calibration rows. Nominal coverage is 90%; observed held-out test coverage is 90.1%. Marginal coverage does not guarantee coverage for every individual or city subgroup.

## Explainability and fairness

Global importance is measured by permutation RMSE increase. Tree-based champions use Tree SHAP on transformed features, grouped back to six raw inputs. Other champions use exact six-feature Shapley values against a fixed reference profile. City ablation compares the same model family and folds with and without city. Geographic error and coverage are evaluated on the held-out test set with subgroup counts.

## Limitations and failure modes

- Synthetic salary relationships may not reflect real compensation markets.
- The input omits company size, seniority, negotiation, equity, and local market shifts.
- Missing values use fold-local median imputation; unusual incomplete profiles may be less reliable.
- Protected-class labels are absent, so demographic fairness cannot be established.
- Feature importance and city sensitivity are predictive associations, not causal effects.
- A 90% marginal interval can have lower coverage for an individual subgroup.

## Reproduction

Run `python -m ml.data.generate`, `python -m ml.evaluation.eda`, and `python -m ml.models.train --trials 3`, or `dvc repro`. Training produces the model, metadata, reports, plots, and calibration radius. No test labels enter hyperparameter selection.
