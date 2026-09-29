# API Specification

Base:
`/api/v1`

All responses JSON.

---

# 1. Health

## GET `/health`

Response:

```json
{
  "status": "ok",
  "model_loaded": true,
  "model_version": "..."
}
```

Health returns HTTP 503 with `DEPLOYMENT_INCOMPLETE` and the missing artifact paths until the model, reports, and Explore plot are all present. Render uses this endpoint as its deployment readiness check.

---

# 2. Model metadata

## GET `/model`

Returns:

- model family
- version
- training timestamp
- dataset version
- feature names
- target
- nominal interval coverage

---

# 3. Model metrics

## GET `/model/metrics`

Returns real champion metrics:

```json
{
  "test": {
    "r2": 0.0,
    "mse": 0.0,
    "rmse": 0.0,
    "mae": 0.0
  },
  "cross_validation": {
    "r2_mean": 0.0,
    "r2_std": 0.0,
    "rmse_mean": 0.0,
    "rmse_std": 0.0,
    "mae_mean": 0.0,
    "mae_std": 0.0
  }
}
```

Values must be loaded from generated artifacts.

---

# 4. Feature schema

## GET `/features`

Returns valid:

- education values
- roles
- industries
- cities
- numeric ranges

Frontend inputs should be driven by this contract.

---

# 5. Prediction

## POST `/predict`

Request:

```json
{
  "experience_years": 7.0,
  "education_level": "Master's",
  "job_role": "ML Engineer",
  "industry": "FinTech",
  "city": "Mumbai",
  "certifications": 3
}
```

Response:

```json
{
  "prediction": {
    "salary_inr": 0,
    "salary_lakh": 0.0
  },
  "interval": {
    "lower_inr": 0,
    "upper_inr": 0,
    "coverage": 0.9
  },
  "model": {
    "family": "...",
    "version": "..."
  }
}
```

Do not invent a confidence percentage.

---

# 6. Explanation

## POST `/explain`

Same candidate payload.

Response:

```json
{
  "baseline": 0,
  "prediction": 0,
  "contributions": [
    {
      "feature": "experience_years",
      "display_name": "Experience",
      "contribution": 0
    }
  ],
  "method": "shap"
}
```

Only expose this endpoint if explanation is technically correct.

---

# 7. Counterfactual

## POST `/counterfactual`

Request:

```json
{
  "candidate": {
    "experience_years": 7,
    "education_level": "Master's",
    "job_role": "ML Engineer",
    "industry": "FinTech",
    "city": "Mumbai",
    "certifications": 3
  },
  "vary": "city"
}
```

Return predictions for allowed alternative values.

---

# 8. Reports

## POST `/curve`

Takes the validated candidate payload and returns model predictions for experience from 0 to 35 years in 0.5-year steps, with the other attributes fixed. The frontend may highlight points from this response but must not calculate salary values.

---

## GET `/reports/model-comparison`

Returns generated model comparison data.

## GET `/reports/fairness`

Returns generated subgroup diagnostics.

## GET `/reports/residuals`

Returns residual summary and references to plot assets/data.

---

# 9. Validation

Return HTTP 422 for invalid candidate inputs.

Examples:

- negative experience
- unsupported education value
- certifications below 0
- impossible category

Return HTTP 503 when model artifacts are missing.

Never fall back to a hardcoded prediction.

---

# 10. CORS

Restrict production CORS to known frontend origins.

Development may allow localhost origins explicitly.

---

# 11. Versioning

All endpoints under:

`/api/v1`

Do not silently break schemas.
