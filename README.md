# CompLens — Evidence-based salary intelligence

CompLens is a reproducible academic salary prediction system: deterministic synthetic data, five required sklearn regressors, five-fold cross-validation, Optuna tuning, residual and fairness diagnostics, a split-conformal prediction interval, a FastAPI inference service, and a Next.js product UI. Salaries are annual INR. Synthetic figures are educational and are **not** live market benchmarks.

## Quick start

Requirements: Python 3.12, Node.js 22, npm. On Windows PowerShell, run from this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev,ops]"
npm --prefix apps/web install
.\.venv\Scripts\python -m ml.data.generate
.\.venv\Scripts\python -m ml.evaluation.eda
.\.venv\Scripts\python -m ml.models.train --trials 3
.\.venv\Scripts\python -m ml.evaluation.document
```

Start two terminals:

```powershell
.\.venv\Scripts\python -m uvicorn apps.api.main:app --reload
```

```powershell
npm --prefix apps/web run dev
```

Open `http://localhost:3000`. API docs are at `http://localhost:8000/docs`.

For a reproducible DVC pipeline, run `dvc repro` after installing optional ops dependencies, then run `python -m ml.evaluation.document` to refresh the model card and report. The DVC graph is generate → EDA and train. The DVC cache may need a shorter local path on Windows when the repository lives in a deep OneDrive directory, for example `dvc config --local cache.dir C:/Users/<you>/.complens-dvc-cache`.

## Evaluation protocol

The generator writes 7,500 rows by default, seed 42. Salary combines role, education, industry, city, certifications, a saturating experience curve, role interactions, and heteroscedastic noise. Missingness is added after target construction. Validation rejects impossible values and unknown categories.

The 70/15/15 training/calibration/test split happens before preprocessing. Each candidate is a serializable sklearn pipeline with median numeric imputation and one-hot categorical encoding. Polynomial regression expands experience only. All five candidates use the same five training folds. Optuna searches tree-family settings using CV RMSE. The champion is selected by mean CV RMSE; held-out test data is used only after selection. Calibration errors create the 90% split-conformal interval.

The generated [model card](MODEL_CARD.md), [college report](REPORT.md), and [presentation outline](PRESENTATION.md) contain actual run results. The [task phases](TASKS.md), [build status](BUILD_STATUS.md), [master specification](MASTER_SPEC.md), and [QA checklist](QA_CHECKLIST.md) document scope, progress, and acceptance criteria.

## Application routes

The product has Landing, Estimate, Explore, Model Lab, Explain, Fairness, and Methodology screens. The browser calls only FastAPI for predictions. The API exposes `/api/v1/health`, `/model`, `/model/metrics`, `/features`, `/predict`, `/explain`, `/counterfactual`, `/curve`, and report/plot endpoints. FastAPI returns 422 for invalid profiles and 503 if a required artifact is unavailable.

## Artifacts and lineage

- `data/raw/salary_survey.csv`: generated survey, tracked by DVC.
- `artifacts/champion/model.joblib`: fitted sklearn pipeline.
- `artifacts/champion/metadata.json`, `metrics.json`, `feature_schema.json`: deployed model contract.
- `artifacts/reports/`: fold scores, tuning history, EDA, linearity, importance, city ablation, fairness, residuals, and provenance.
- `artifacts/plots/`: reproducible charts with labeled units.

W&B is optional so training works without an account. Set `COMPLENS_WANDB=1` and `WANDB_MODE=offline` to create five local experiment runs and model artifacts; these can be synced later with W&B credentials. Set `WANDB_API_KEY` and omit offline mode for remote tracking. Copy `.env.example` for the API/CORS and frontend URL settings. Only load trusted local joblib artifacts.

## Checks

```powershell
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python -m ruff check ml apps/api tests
npm --prefix apps/web run typecheck
npm --prefix apps/web run lint
npm --prefix apps/web run build
```

## Deployment

The source is in the private GitHub repository `Sayuj63/complens`. The API can use the free Render blueprint in `render.yaml` or the Railway service configuration in `railway.json`; both generate and train the model during the build. Set `COMPLENS_CORS_ORIGINS` to the exact deployed frontend origin. On Vercel, import the GitHub repository with root directory `apps/web`, then set `NEXT_PUBLIC_API_URL` to the backend URL ending in `/api/v1` before its production build. Verify `/api/v1/health`, `/api/v1/predict`, and browser CORS after deployment. Hosting account connection and live URL verification remain pending.
