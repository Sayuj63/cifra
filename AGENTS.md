# AGENTS.md — Cifra Operating Rules

This file contains non-negotiable instructions for any coding agent working in this repository.

## 1. Mission

Build **Cifra**, a production-style Employee Salary Prediction ML project for a B.Tech CSE Semester V machine-learning case study.

The system must satisfy every academic requirement while demonstrating professional ML engineering.

The finished system must be reproducible from source code and must never rely on fake numbers or hardcoded model outputs.

---

# 2. Non-negotiable ML rules

1. Never hardcode ML metrics in the frontend.
2. Never calculate salary predictions in JavaScript.
3. Never preprocess the full dataset before train/calibration/test splitting.
4. Never fit imputers, scalers, encoders, or polynomial transforms on test data.
5. Never use the test set for model selection or hyperparameter tuning.
6. Never claim a model is "best" before actual evaluation.
7. Never fabricate Weights & Biases runs.
8. Never fabricate residual plots.
9. Never fabricate prediction intervals.
10. Never fabricate SHAP or feature-importance values.
11. Never silently drop missing rows.
12. Never leak target salary into feature engineering.
13. Always use deterministic random seeds where supported.
14. All candidate models must be evaluated under the same data split and CV strategy.
15. Every deployable model must be wrapped in a serializable sklearn pipeline.
16. Production metrics displayed by the web app must come from generated artifact files.
17. Every chart must display units.
18. Every salary output must clearly state INR/year or lakh/year.
19. Every analytical conclusion must be supported by actual computed evidence.
20. The champion model must be selected from the five algorithms required by the assignment.

---

# 3. Engineering rules

- Python 3.12 preferred.
- Type hints for production Python code.
- Use `pyproject.toml`.
- Use `ruff` for linting.
- Use `pytest` for ML/API tests.
- Use TypeScript in the frontend.
- Do not disable type checking to make builds pass.
- Do not introduce `any` without a documented reason.
- No giant files. Prefer cohesive modules.
- Separate notebook exploration from production training code.
- No secrets in git.
- `.env.example` must document required environment variables.
- Every generated model artifact must contain version metadata.
- API must validate all inputs.
- API errors must be explicit and structured.
- Frontend must handle loading, error, empty, and success states.
- Build must work from a clean clone.

---

# 4. UI anti-slop rules

Do not use generic AI-generated dashboard aesthetics.

STRICTLY FORBIDDEN:

- gradients
- glassmorphism
- purple/blue AI gradients
- giant hero gradient text
- floating decorative blobs
- excessive shadows
- arbitrary cards everywhere
- rounded-xl/2xl on every element
- icon beside every heading
- three KPI cards merely because dashboards use them
- fake analytics
- fake command palettes
- stock AI illustrations
- sparkles icon
- random decorative lines
- unnecessary sidebars
- rainbow charts
- huge empty hero layouts
- fake testimonials
- lorem ipsum
- meaningless "AI-powered" marketing copy

Orange is an accent, not a background color.

---

# 5. Design behavior

The application should feel like:

- a research instrument
- a premium B2B SaaS product
- a compensation-analysis tool
- a clean scientific interface

It should NOT feel like:

- an admin dashboard
- a hackathon prototype
- a Streamlit page
- a template marketplace UI
- a generic shadcn demo

Use Base UI primitives or equivalent unstyled accessible primitives where helpful.

---

# 6. Mandatory runtime architecture

Frontend:
Next.js + TypeScript

Backend:
FastAPI

ML:
scikit-learn

Data:
Pandas + NumPy

Experiment tracking:
Weights & Biases

Dataset/pipeline versioning:
DVC

Hyperparameter optimization:
Optuna

Explainability:
SHAP + permutation importance

Prediction intervals:
MAPIE or another valid conformal prediction implementation compatible with the chosen model.

Serialization:
joblib

The frontend must call the FastAPI service for inference.

---

# 7. Required application screens

At minimum:

1. Landing / Overview
2. Estimate
3. Explore
4. Model Lab
5. Explain
6. Fairness
7. Methodology

Do not add more pages until these are correct.

---

# 8. Required artifact sources

The frontend must load metrics/model metadata from generated files or API responses.

Expected production artifacts:

- `artifacts/champion/model.joblib`
- `artifacts/champion/metadata.json`
- `artifacts/champion/metrics.json`
- `artifacts/champion/feature_schema.json`
- `artifacts/reports/model_comparison.json`
- `artifacts/reports/fairness.json`
- `artifacts/reports/residual_summary.json`

---

# 9. Phase gate rule

Codex may not move to a later phase merely because files exist.

A phase is complete only when:

1. implementation exists
2. tests pass
3. required artifact/output exists
4. acceptance criteria in `TASKS.md` are satisfied
5. no known regression remains from earlier phases

If a phase fails, fix it before proceeding.

---

# 10. No fake demos

If training has not run yet, the UI must show a proper "model artifacts unavailable" state.

Never create placeholder metrics such as:

- R² = 0.94
- RMSE = ₹1.2L
- 90% confidence

unless generated by the actual pipeline.

---

# 11. Documentation discipline

When a major architectural decision is made, update the relevant spec instead of relying on hidden agent context.

Keep:
- `README.md`
- `MODEL_CARD.md`
- API docs
- data-generation rationale
- evaluation methodology

synchronized with implementation.

---

# 12. Definition of done

The project is complete only when a fresh user can:

1. clone the repository
2. install dependencies
3. generate or obtain the dataset
4. reproduce preprocessing
5. train all five required algorithms
6. reproduce cross-validation
7. reproduce model comparison
8. produce residual diagnostics
9. select the champion using the documented methodology
10. generate prediction intervals
11. start the FastAPI server
12. start the Next.js frontend
13. submit a candidate profile
14. receive a real model prediction
15. view explanation and uncertainty
16. inspect model comparison and methodology
17. run the test suite successfully
