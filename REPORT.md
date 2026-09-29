# Cifra — Employee Salary Prediction Case Study

## Problem and data

Estimate annual salary in INR/year from six candidate attributes for a recruitment consultancy scenario. The project uses 7,500 deterministic synthetic profiles because the required attributes are not consistently available together in one public survey. SHA-256: `4c4608134b8e0c1e80e7ef1b409236adc3ef515406914ac3a6de435082b5c965`. Missing experience: 1.97%; missing certifications: 4.01%. The data is educational and is not a live salary benchmark.

## Method

The generator combines role, education, industry, city, certifications, a saturating experience function, role-by-experience interaction, and heteroscedastic noise. Data is split before any preprocessing: 70% training (5,250), 15% calibration, 15% testing. Each sklearn pipeline imputes numeric values with training-fold medians, imputes categorical values with training-fold modes, one-hot encodes categories, and ignores unknown categories. Polynomial regression adds only an experience-squared term.

Five required algorithms are compared with 5-fold shuffled cross-validation on the training partition. Optuna searches tree-family hyperparameters using CV RMSE. Selection uses mean CV RMSE, then MAE and model name for ties. The held-out test is evaluated once after selection.

## Cross-validation results

| Model | CV R² | CV RMSE (INR/year) | CV MAE (INR/year) |
|---|---:|---:|---:|
| Gradient Boosting | 0.847 | ₹1.26L | ₹0.96L |
| Polynomial Regression | 0.845 | ₹1.27L | ₹0.97L |
| Random Forest | 0.823 | ₹1.35L | ₹1.04L |
| Linear Regression | 0.776 | ₹1.52L | ₹1.18L |
| Decision Tree | 0.774 | ₹1.53L | ₹1.19L |

Selected champion: **Gradient Boosting**. Test R² 0.850, MSE 15,642,917,410 INR², RMSE ₹1.25L/year, MAE ₹0.97L/year. Residual plots are stored in `artifacts/plots/`.

## Research questions

**Is salary growth with experience linear?** A quadratic experience term improves CV RMSE over linear experience. Linear CV RMSE is ₹1.52L versus polynomial ₹1.27L, an improvement of 16.9%. The generator itself contains a saturating experience term.

**Does city contribute predictive information?** With-city CV RMSE is ₹1.26L versus without-city ₹1.30L. Delta: ₹0.04L. This is an ablation, not a causal claim.

**How uncertain is an estimate?** A separate calibration set sets a 90% split-conformal interval; test coverage is 90.1%. The interval targets marginal coverage, not individual certainty.

**What attributes matter?** `artifacts/reports/importance.json` records permutation RMSE increases from held-out data; the Explain page visualizes the actual ranking. Importance is predictive, not causal.

**What fairness limits remain?** Test MAE, RMSE, mean residual, sample count, and interval coverage are reported for each city. No protected-class labels exist, so demographic fairness cannot be established.

## System and limitations

FastAPI loads the serialized pipeline and artifact metadata. Next.js calls the API and never computes salary in JavaScript. DVC records generate → EDA/train dependencies; optional W&B logging records metrics and the champion artifact when credentials are supplied. Synthetic data, omitted compensation drivers, and geographic subgroup variation limit real-world applicability. See `MODEL_CARD.md` for failure modes and retraining steps.
