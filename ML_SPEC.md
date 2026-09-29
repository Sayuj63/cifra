# ML Specification

## 1. Feature groups

Numerical:
- experience_years
- certifications

Categorical:
- education_level
- job_role
- industry
- city

Target:
- salary

---

# 2. Preprocessing

Use sklearn `ColumnTransformer`.

Numerical pipeline:

1. `SimpleImputer(strategy="median")`
2. scaling only where useful/required

Categorical pipeline:

1. `SimpleImputer(strategy="most_frequent")`
2. `OneHotEncoder(handle_unknown="ignore")`

Do not ordinal-encode nominal fields.

---

# 3. Linear Regression

Use standard linear regression with preprocessing.

Experience enters with degree 1.

Purpose:
baseline and linearity comparison.

---

# 4. Polynomial Regression

Polynomial expansion must be restricted carefully.

Do NOT blindly polynomial-expand all one-hot features.

Preferred approach:

- create polynomial terms for `experience_years`
- degree 2 baseline
- optionally compare degree 2 and 3 using cross-validation

The categorical features remain normally encoded.

Purpose:
test whether nonlinear experience terms materially improve fit.

---

# 5. Decision Tree Regressor

Tune:

- max_depth
- min_samples_split
- min_samples_leaf
- max_features if applicable

Avoid unconstrained overfit trees as the final tuned candidate.

---

# 6. Random Forest Regressor

Tune:

- n_estimators
- max_depth
- min_samples_split
- min_samples_leaf
- max_features

Use deterministic random state.

---

# 7. Gradient Boosting Regressor

Tune:

- n_estimators
- learning_rate
- max_depth
- min_samples_split
- min_samples_leaf
- subsample

Use deterministic random state where available.

---

# 8. Cross-validation

Default:

`KFold(n_splits=5, shuffle=True, random_state=42)`

For each model record:

- fold R²
- fold MSE
- fold RMSE
- fold MAE

Aggregate:

- mean
- standard deviation

---

# 9. Model selection

Primary ranking metric:

mean cross-validated RMSE.

Secondary diagnostics:

- MAE
- R²
- fold variance
- train-vs-CV gap
- residual behavior

The test set must not be part of selection.

---

# 10. Test evaluation

After model selection, evaluate champion on held-out test data once.

Compute:

- R²
- MSE
- RMSE
- MAE

Store exact values.

---

# 11. Residual diagnostics

Required plots:

1. residual vs predicted
2. residual histogram
3. residual vs experience

Optional:
4. Q-Q plot

Required summary statistics:

- residual mean
- residual std
- residual median
- 5th / 95th percentiles

Interpret:

- curvature
- heteroscedasticity
- outliers
- systematic bias

---

# 12. Linearity study

This is a core academic requirement.

Compare Linear Regression and Polynomial Regression.

Produce:

- salary vs experience scatter
- fitted linear curve
- fitted polynomial curve
- CV RMSE comparison
- residual-vs-experience comparison

Do not conclude nonlinearity solely from visual intuition.

Use measured performance and residual structure.

---

# 13. Hyperparameter optimization

Use Optuna.

Objective:

minimize mean 5-fold CV RMSE.

Do not optimize on the test set.

Save:

- study name
- number of trials
- best parameters
- best CV score
- optimization history artifact

W&B integration is encouraged.

---

# 14. Experiment tracking

For every meaningful training run log:

- model family
- dataset version
- seed
- feature list
- row counts
- split metadata
- hyperparameters
- CV metrics
- train metrics
- training duration
- residual plots
- prediction-vs-actual table
- artifact version

Use Weights & Biases when credentials are available.

If W&B credentials are absent, training must still work locally and save equivalent JSON artifacts.

---

# 15. Explainability

Global:
- permutation importance for champion

Local:
- SHAP if compatible and stable with the chosen pipeline/model

If SHAP cannot be applied correctly to the wrapped model, do not fake it. Implement a correct transformed-feature path or omit local SHAP until valid.

Never interpret feature importance as causal effect.

---

# 16. Experience response

Generate a partial response curve by holding a representative candidate profile fixed while sweeping experience from 0 to 30 years.

This becomes the "Salary Growth Curve" in the product.

---

# 17. City ablation

Train the same champion model family under two feature sets:

A:
all features

B:
all features except city

Compare 5-fold CV RMSE and MAE.

Report delta.

This measures predictive contribution, not causality.

---

# 18. Fairness / subgroup diagnostics

For each city on the held-out test set calculate:

- sample count
- MAE
- RMSE
- mean residual
- prediction interval coverage

Do not create a fake fairness score.

Document that protected-group fairness cannot be established without protected-class labels.

---

# 19. Prediction intervals

Preferred:
MAPIE / conformal regression.

Use calibration data that was not used for fitting the final model.

Default target coverage:
90%.

Expose:

- point estimate
- lower bound
- upper bound
- requested/nominal coverage

Do not call a regression prediction interval "confidence score."

---

# 20. Champion artifact

Save:

`artifacts/champion/model.joblib`

Metadata:

```json
{
  "model_family": "...",
  "model_version": "...",
  "dataset_version": "...",
  "trained_at": "...",
  "features": [],
  "target": "salary",
  "random_seed": 42
}
```

Also save:
- metrics
- feature schema
- conformal/calibration object if separate
