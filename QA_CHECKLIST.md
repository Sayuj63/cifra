# Final QA Checklist

## ML correctness

- [ ] Raw dataset generation is deterministic.
- [ ] Data split happens before fitting preprocessing.
- [ ] Calibration and test sets are isolated.
- [ ] Missing values are handled inside pipelines.
- [ ] Categorical encoding handles unknown categories.
- [ ] All five required algorithms are implemented.
- [ ] Polynomial regression is genuinely different from linear regression.
- [ ] Cross-validation uses training data only.
- [ ] Hyperparameter tuning does not inspect test labels.
- [ ] Champion is selected programmatically.
- [ ] Test metrics are generated from held-out data.
- [ ] Residual plots use actual predictions.
- [ ] Prediction intervals use a valid calibration approach.
- [ ] No feature importance is fabricated.
- [ ] City ablation is implemented fairly.
- [ ] Subgroup metrics show sample size.

## Required assignment metrics

- [ ] R²
- [ ] MSE
- [ ] RMSE
- [ ] MAE
- [ ] Residual Plot
- [ ] k-fold CV

## Academic conclusions

- [ ] strongest attributes discussed
- [ ] best-performing required model justified
- [ ] experience linearity analyzed empirically
- [ ] city predictive contribution analyzed
- [ ] fairness concerns discussed
- [ ] limitations documented
- [ ] real-world applicability discussed

## API

- [ ] `/health`
- [ ] `/model`
- [ ] `/model/metrics`
- [ ] `/features`
- [ ] `/predict`
- [ ] invalid inputs rejected
- [ ] unavailable model returns 503
- [ ] schema tests pass

## Frontend

- [ ] no hardcoded ML metrics
- [ ] no client-side salary formula
- [ ] loading states
- [ ] error states
- [ ] empty states
- [ ] success states
- [ ] mobile tested
- [ ] tablet tested
- [ ] desktop tested
- [ ] keyboard focus visible
- [ ] readable contrast
- [ ] chart axes labeled
- [ ] salary units clear

## Design anti-slop

- [ ] no gradients
- [ ] no glassmorphism
- [ ] no excessive rounded cards
- [ ] no purple AI aesthetic
- [ ] no random icons
- [ ] no fake analytics
- [ ] no decorative blobs
- [ ] orange used semantically
- [ ] typography hierarchy consistent
- [ ] spacing follows token scale

## Reproducibility

- [ ] fresh clone documented
- [ ] dataset generation command documented
- [ ] training command documented
- [ ] artifact paths documented
- [ ] backend startup documented
- [ ] frontend startup documented
- [ ] tests documented
- [ ] environment variables documented

## Security / robustness

- [ ] no secrets committed
- [ ] CORS configured
- [ ] API validates inputs
- [ ] frontend escapes user-controlled text
- [ ] no arbitrary file reads
- [ ] artifact loading uses controlled paths
- [ ] debug mode disabled in production

## Presentation

- [ ] app starts cleanly
- [ ] demo profile prepared
- [ ] W&B project accessible if used
- [ ] plots pre-generated
- [ ] no broken charts
- [ ] no console errors
- [ ] no visible stack traces
- [ ] Methodology page matches implementation
