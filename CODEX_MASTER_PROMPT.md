# Codex Master Prompt — CompLens

You are building a complete machine-learning product named **CompLens**.

Before touching code, read:

1. `AGENTS.md`
2. `MASTER_SPEC.md`
3. `DATA_SPEC.md`
4. `ML_SPEC.md`
5. `DESIGN_SYSTEM.md`
6. `API_SPEC.md`
7. `TASKS.md`
8. `QA_CHECKLIST.md`

Your task is not to generate a demo mockup.

Your task is to build a reproducible, production-style academic ML system satisfying the Employee Salary Prediction case study.

## Operating behavior

- Work phase-by-phase using `TASKS.md`.
- Do not skip ahead.
- At the start of each phase, inspect the existing repository.
- At the end of each phase:
  - run tests
  - run lint/type checks as relevant
  - verify artifacts
  - update documentation if architecture changed
- Fix failures before starting the next phase.

## Critical requirement

Never fabricate:
- model metrics
- predictions
- prediction intervals
- feature importance
- SHAP values
- experiment runs
- dataset statistics

If artifacts are unavailable, implement an explicit unavailable state.

## ML rules

Use exactly these required model families:

1. Linear Regression
2. Polynomial Regression
3. Decision Tree Regressor
4. Random Forest Regressor
5. Gradient Boosting Regressor

Use 5-fold cross-validation.

Compare:
- R²
- MSE
- RMSE
- MAE

Residual analysis is mandatory.

The final champion must come from the required models.

## Product rule

The web application is a client of the FastAPI backend.

The browser must never implement salary logic.

## Design rule

The interface must use the visual language in `DESIGN_SYSTEM.md`.

Do not substitute a generic dashboard template.

## First action

Inspect the repo and create a concise implementation status matrix for phases 00–26.

Then begin with the earliest incomplete phase.

Do not ask for approval between phases unless a genuine external dependency blocks progress.
