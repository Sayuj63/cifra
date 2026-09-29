# CompLens build status

The implementation followed the phase gates in [TASKS.md](TASKS.md). Phases 00–25 are implemented and verified locally. Phase 26 has deployable configuration but no public deployment because no cloud account, URL, or credentials are configured in this workspace.

| Phase group | Delivered evidence |
|---|---|
| 00–03 · foundation and data | Python and Next.js workspaces; deterministic 7,500-row generator; validation; EDA; 70/15/15 split; sklearn preprocessing pipelines |
| 04–10 · model science | Five required regressors; shared five-fold CV; Optuna tree tuning; training-fold model selection; final test metrics; residual and linearity reports |
| 11–15 · interpretation and operations | Tree SHAP for local predictions; permutation importance; city ablation; city error and coverage; 90% split-conformal intervals; DVC lockfile; five offline W&B experiment runs; serialized champion and model card |
| 16–23 · product | FastAPI inference and reporting routes; custom Next.js design system; Landing, Estimate, Explore, Model Lab, Explain, Fairness, and Methodology screens |
| 24–25 · QA | `pytest`: 5 passed; Ruff: passed; frontend typecheck, ESLint, and production build: passed; Playwright: 3 passed; `dvc status`: up to date |
| 26 · deployment | `render.yaml` and frontend environment contract are ready. Remote health, inference, and CORS checks await an actual deployment. |

## Verified model result

- Champion: Gradient Boosting Regressor, selected by training CV RMSE.
- Held-out test R²: 0.8498.
- Held-out test RMSE: ₹1.2507 lakh/year.
- Held-out test MAE: ₹0.9747 lakh/year.
- Nominal interval coverage: 90%; observed held-out coverage: 90.13%.

These numbers come from `artifacts/champion/metrics.json`. The generated dataset is synthetic and is not a live salary survey. Offline W&B runs are local and ignored by Git; set `COMPLENS_WANDB=1` and `WANDB_MODE=offline` during training to reproduce them. The pinned W&B version in `pyproject.toml` has been verified on this Windows workspace.
