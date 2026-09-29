# Model Card — Cifra

## Model details

Model name:
Cifra Salary Estimator

Version:
TBD

Model family:
TBD

Training date:
TBD

Dataset version:
TBD

---

## Intended use

Estimate annual salary ranges for educational demonstration of regression, model comparison, uncertainty, explainability, and responsible ML.

---

## Out-of-scope use

This model must not be used as the sole basis for:
- hiring decisions
- compensation offers
- promotion decisions
- legal employment decisions
- discrimination-sensitive decisions

Synthetic training data is not a substitute for real compensation-market data.

---

## Features

- experience years
- education level
- job role
- industry
- city
- relevant certification count

Target:
annual salary in INR

---

## Training methodology

Document:
- split strategy
- preprocessing
- CV
- tuning
- champion selection

---

## Evaluation

Populate from generated artifacts:

- R²
- MSE
- RMSE
- MAE
- CV mean/std

---

## Residual behavior

Populate after training.

---

## Prediction uncertainty

Method:
Conformal prediction / MAPIE

Nominal coverage:
90%

Empirical test coverage:
TBD

---

## Explainability

- permutation importance
- optional SHAP local explanation
- experience response analysis

---

## Fairness considerations

City-level subgroup error analysis is supported.

The dataset does not include protected demographic attributes such as gender, caste, religion, disability, or race.

Therefore demographic fairness cannot be established.

---

## Limitations

- synthetic dataset
- simplified feature set
- no company size
- no actual negotiation data
- no macroeconomic/time index
- no job-level hierarchy
- no real cost-of-living dataset
- synthetic city effects
- not suitable for actual compensation decisions

---

## Retraining

Document:
- command
- dataset version
- seed
- artifact versioning
