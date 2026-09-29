# Cifra Master Specification

## 1. Problem

A recruitment consultancy wants to estimate an appropriate annual salary for a candidate based on:

- years of experience
- education level
- job role
- industry
- city
- number of relevant certifications

The estimate supports salary benchmarking during negotiation.

The system must output:

- point salary estimate
- estimated salary range
- expected error/uncertainty information
- model identity/version
- explanation where appropriate

---

# 2. Academic objectives

The project must demonstrate:

- exploratory data analysis
- salary survey analysis
- missing-value handling
- categorical encoding
- investigation of experience vs salary linearity
- training of required regression models
- comparison with proper metrics
- k-fold cross-validation
- residual analysis
- justified model selection
- interactive deployment
- limitation analysis
- fairness analysis

---

# 3. Research questions

The report and app must answer:

1. Which attributes have the greatest effect on salary?
2. Which of the required algorithms performs best under cross-validation?
3. Is salary growth with experience linear?
4. Does city contribute meaningful independent predictive value?
5. What fairness concerns exist in automated salary estimation?
6. How uncertain is an individual prediction?
7. Where does the champion model fail?

---

# 4. Architecture

```text
Browser
  |
  v
Next.js Application
  |
  | HTTPS / JSON
  v
FastAPI
  |
  +--> Champion sklearn Pipeline
  |
  +--> Prediction Interval Calibrator
  |
  +--> Explainability Service
  |
  +--> Metrics / Artifact Reader
            |
            v
       Generated artifacts

Training system:
Raw Data
  -> Validation
  -> Split
  -> Preprocessing
  -> 5 Required Models
  -> K-Fold CV
  -> Optuna Tuning
  -> Final Evaluation
  -> Residual Analysis
  -> Explainability
  -> Fairness / Ablation
  -> Conformal Calibration
  -> Champion Model
  -> Artifacts
```

---

# 5. Repository architecture

```text
cifra/
│
├── apps/
│   ├── web/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   ├── lib/
│   │   ├── public/
│   │   └── styles/
│   │
│   └── api/
│       ├── main.py
│       ├── config.py
│       ├── routes/
│       ├── schemas/
│       ├── services/
│       └── tests/
│
├── ml/
│   ├── config/
│   ├── data/
│   │   ├── generate.py
│   │   ├── validate.py
│   │   ├── split.py
│   │   └── preprocess.py
│   │
│   ├── features/
│   │   └── schema.py
│   │
│   ├── models/
│   │   ├── definitions.py
│   │   ├── train.py
│   │   ├── tune.py
│   │   ├── evaluate.py
│   │   ├── select.py
│   │   └── registry.py
│   │
│   ├── evaluation/
│   │   ├── metrics.py
│   │   ├── residuals.py
│   │   ├── importance.py
│   │   ├── explainability.py
│   │   ├── fairness.py
│   │   ├── ablation.py
│   │   └── uncertainty.py
│   │
│   └── inference/
│       └── predictor.py
│
├── notebooks/
│   ├── 01_eda.ipynb
│   └── 02_model_analysis.ipynb
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── splits/
│
├── artifacts/
│   ├── champion/
│   ├── candidate_models/
│   ├── plots/
│   └── reports/
│
├── tests/
│   ├── ml/
│   └── integration/
│
├── params.yaml
├── dvc.yaml
├── pyproject.toml
├── package.json
├── .env.example
├── MODEL_CARD.md
├── AGENTS.md
└── README.md
```

---

# 6. ML lifecycle

## Stage A — data

1. Generate deterministic synthetic dataset.
2. Validate schema and constraints.
3. Introduce controlled missingness and noise.
4. Store raw dataset.
5. Version dataset using DVC.

## Stage B — exploration

Produce:

- dataset shape
- missing-value table
- salary distribution
- salary vs experience scatter
- salary by education
- salary by role
- salary by industry
- salary by city
- certification distribution
- correlation analysis for numeric values
- category counts
- outlier analysis

## Stage C — split

Use:

- 70% train
- 15% calibration
- 15% test

Use a deterministic seed.

No preprocessing before split.

## Stage D — baseline

Train all five required models.

Use 5-fold CV on training data.

## Stage E — tuning

Tune only:

- Decision Tree
- Random Forest
- Gradient Boosting
- optionally polynomial degree

Use Optuna.

Primary optimization metric:

RMSE via cross-validation.

## Stage F — model selection

Primary:
- mean CV RMSE

Secondary:
- mean CV MAE
- CV R²
- generalization gap
- residual structure
- stability across folds

Do not use test set to choose.

## Stage G — final evaluation

Evaluate selected candidate(s) once on held-out test set.

Compute:

- R²
- MSE
- RMSE
- MAE
- residual statistics

## Stage H — uncertainty

Use calibration split for conformal prediction interval construction.

Expose a target coverage level, default 90%.

## Stage I — explainability

Create:

- permutation importance
- SHAP/local contribution where technically valid
- partial dependence or response curve for experience
- counterfactual city sensitivity

## Stage J — fairness

Evaluate error and prediction interval coverage by city.

Perform city-ablation experiment.

State clearly that demographic fairness cannot be established without protected-class labels.

---

# 7. Product behavior

## Estimate

Input:

- experience
- education
- role
- industry
- city
- certifications

Output:

- predicted salary
- prediction interval
- model name/version
- explanation
- compact reliability/context note

## Explore

Interactive research views:

- salary vs experience
- linear vs polynomial fit
- salary distributions
- role / city / industry comparisons

## Model Lab

Real comparison of the five required algorithms.

Never display fake results.

## Explain

Show:

- global feature importance
- local explanation
- experience response
- prediction sensitivity

## Fairness

Show:

- MAE by city
- RMSE by city if useful
- sample count by city
- interval coverage by city
- city counterfactual
- city ablation result
- documented limitations

## Methodology

Explain:

- dataset construction
- preprocessing
- split
- CV
- tuning
- model selection
- uncertainty method
- limitations

---

# 8. Presentation quality standard

The final project should be defensible in a viva.

A student must be able to explain:

- why preprocessing is fit only on training folds
- why CV is superior to one validation split
- why test data is kept untouched
- why RMSE and MAE tell different stories
- what residual structure means
- why nonlinear salary growth matters
- why model importance is not causality
- why city sensitivity does not prove discrimination
- why a prediction interval is not the same thing as classification confidence
