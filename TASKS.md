# Codex Execution Plan

Codex must complete phases in order.

Each phase has acceptance criteria.

---

# PHASE 00 — Repository foundation

Create project structure.

Add:

- Python environment
- frontend workspace
- linting
- formatting
- tests
- environment examples
- Makefile or task runner

Acceptance:

- Python import checks pass
- frontend typecheck passes
- empty test suite command succeeds
- README has setup instructions

---

# PHASE 01 — Synthetic dataset generator

Implement deterministic dataset generation following `DATA_SPEC.md`.

Acceptance:

- 7500 rows by default
- same seed -> same dataset hash
- all required fields exist
- target nonlinear behavior is present by construction
- missingness introduced after target generation
- validation tests pass

Artifacts:

- raw CSV
- data profile JSON

---

# PHASE 02 — EDA

Create reproducible EDA module/notebook.

Required outputs:

- missingness table
- salary distribution
- salary vs experience
- salary by education
- salary by role
- salary by city
- salary by industry
- certifications distribution
- descriptive statistics

Acceptance:

- charts render without manual edits
- every axis has label/unit
- observations are evidence-based

---

# PHASE 03 — Split and preprocessing

Implement deterministic 70/15/15 split.

Implement sklearn preprocessing.

Acceptance:

- no transformer is fit on calibration/test before final evaluation
- unknown categories do not crash inference
- missing values handled
- tests prove data leakage is avoided

---

# PHASE 04 — Required baseline models

Implement:

- Linear Regression
- Polynomial Regression
- Decision Tree
- Random Forest
- Gradient Boosting

Acceptance:

- all train successfully
- all produce metrics
- all use common split/CV methodology

---

# PHASE 05 — Cross-validation engine

Implement 5-fold CV.

Acceptance:

- per-fold values stored
- mean/std stored
- R²/MSE/RMSE/MAE computed
- results serialized to JSON

---

# PHASE 06 — Hyperparameter optimization

Use Optuna.

Tune tree-based models.

Acceptance:

- optimization objective is CV RMSE
- test set is untouched
- best params serialized
- runs reproducible enough for project context

---

# PHASE 07 — Model comparison and champion selection

Build model comparison artifact.

Acceptance:

- champion selected programmatically
- primary criterion documented
- no hardcoded champion family
- tie-breaking logic documented
- test set not used for initial selection

---

# PHASE 08 — Final test evaluation

Evaluate champion.

Acceptance:

- R²
- MSE
- RMSE
- MAE

stored in artifacts.

Do not retrain repeatedly against test feedback.

---

# PHASE 09 — Residual analysis

Generate:

- residual vs predicted
- residual histogram
- residual vs experience
- optional Q-Q

Acceptance:

- residual stats JSON
- plots stored
- report detects possible systematic structure

---

# PHASE 10 — Linearity analysis

Compare Linear and Polynomial models.

Acceptance:

- visual curve comparison
- CV metric comparison
- residual comparison
- final conclusion generated from actual results

---

# PHASE 11 — Explainability

Implement:

- permutation importance
- experience response curve
- local SHAP if valid

Acceptance:

- no fabricated explanation values
- transformed features map back to readable labels where possible
- app-safe JSON output exists

---

# PHASE 12 — City ablation and subgroup analysis

Implement city ablation.

Compute test subgroup metrics by city.

Acceptance:

- with-city vs without-city CV comparison
- MAE by city
- RMSE by city
- sample counts
- mean residual by city

---

# PHASE 13 — Prediction intervals

Implement conformal prediction using calibration data.

Acceptance:

- interval generation works
- nominal 90% coverage supported
- empirical coverage measured on test
- coverage by city computed
- terminology uses "prediction interval"

---

# PHASE 14 — W&B + DVC

Add experiment tracking and pipeline versioning.

Acceptance:

- training works without W&B credentials
- with credentials, runs/logs are created
- DVC pipeline captures major stages
- dataset/model lineage documented

---

# PHASE 15 — Champion artifact and model card

Save deployable model + metadata.

Create `MODEL_CARD.md`.

Acceptance:

- fresh process can load artifact and predict
- metadata version included
- known limitations documented

---

# PHASE 16 — FastAPI

Implement endpoints in `API_SPEC.md`.

Acceptance:

- `/health`
- `/model`
- `/model/metrics`
- `/features`
- `/predict`
- reports endpoints

Tests:

- valid prediction
- invalid category
- invalid numeric range
- missing model artifact
- model metadata correctness

---

# PHASE 17 — Design system

Implement tokens/components before application pages.

Components:

- Button
- Input
- Select
- Field
- Badge/Status
- Tooltip
- Popover
- Table
- Section header
- metric text
- chart frame
- error/empty/loading states

Acceptance:

- follows `DESIGN_SYSTEM.md`
- no gradients
- no arbitrary decorative UI
- keyboard focus visible
- mobile behavior correct

---

# PHASE 18 — Estimate experience

Build product prediction flow.

Acceptance:

- inputs generated from feature schema
- backend prediction only
- loading/error/success states
- point estimate
- interval
- model/version
- local explanation when available
- responsive

---

# PHASE 19 — Explore

Build research-oriented data exploration.

Acceptance:

- all values come from real dataset/artifacts
- linearity section prominent
- charts readable mobile/desktop

---

# PHASE 20 — Model Lab

Build comparison UI.

Acceptance:

- five models present
- metrics accurate
- CV mean/std shown
- champion indicated without fake scoring
- residual section linked

---

# PHASE 21 — Explain

Build:

- global importance
- salary growth curve
- local explanation
- counterfactual explorer

Acceptance:

- no fake values
- tooltips explain interpretation limits

---

# PHASE 22 — Fairness

Build:

- subgroup performance
- interval coverage
- city ablation
- city counterfactual
- limitations

Acceptance:

- never claims demographic fairness
- sample size always visible with subgroup metrics

---

# PHASE 23 — Methodology

Build polished methodology page.

Explain:

- synthetic generation
- preprocessing
- split
- CV
- tuning
- test evaluation
- uncertainty
- explainability
- fairness limitations

---

# PHASE 24 — End-to-end testing

Add:

- unit tests
- API tests
- model serialization test
- Playwright happy path
- malformed request tests
- mobile viewport smoke tests

Acceptance:

- clean test run
- no type errors
- no lint errors

---

# PHASE 25 — Final QA

Follow `QA_CHECKLIST.md`.

No feature work after final QA unless fixing defects.

---

# PHASE 26 — Deployment

Deploy:

- frontend
- backend

Acceptance:

- health endpoint works
- prediction works remotely
- no CORS failures
- no secrets exposed
- model loads on cold start
