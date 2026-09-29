# Data Specification

## 1. Dataset strategy

Use a deterministic synthetic dataset because the assignment explicitly requires a combination of features that is not consistently available in one public salary dataset.

Synthetic data must be transparent and reproducible.

Default row count:

`7500`

Default seed:

`42`

Target currency:

Indian Rupees per year.

---

# 2. Columns

## `experience_years`

Type:
float

Expected range:
0.0 to 35.0

Distribution:
mixture biased toward early/mid-career candidates.

Recommended generation:
- majority 0–12 years
- fewer 12–20
- small senior tail 20–35

Introduce approximately 2% missing values after target generation.

---

## `education_level`

Categorical:

- High School
- Bachelor's
- Master's
- PhD

Recommended probabilities:

- High School: 0.08
- Bachelor's: 0.52
- Master's: 0.34
- PhD: 0.06

---

## `job_role`

Recommended categories:

- Software Engineer
- Data Analyst
- Data Scientist
- ML Engineer
- Product Manager
- DevOps Engineer
- Cybersecurity Engineer
- Business Analyst

Use role-specific base salary and experience interaction values.

---

## `industry`

Recommended:

- Technology
- FinTech
- Healthcare
- E-commerce
- Consulting
- Manufacturing
- Telecom

---

## `city`

Recommended:

- Bengaluru
- Mumbai
- Delhi NCR
- Hyderabad
- Pune
- Chennai
- Kolkata
- Ahmedabad

City effect should exist but remain smaller than role/experience effects.

---

## `certifications`

Integer 0–8 for most cases.

Recommended distribution:
Poisson-like with clipping.

Introduce approximately 4% missing values after target generation.

---

## `salary`

Annual INR.

Do not make target perfectly deterministic.

---

# 3. Salary-generation model

The salary generator must deliberately include nonlinear and interaction effects.

Conceptual structure:

```text
salary =
    role_base
  + education_effect
  + industry_effect
  + city_effect
  + certification_effect
  + nonlinear_experience_effect
  + role_experience_interaction
  + stochastic_noise
```

Suggested nonlinear experience function:

```text
experience_effect =
max_experience_gain * (1 - exp(-experience / tau))
```

This produces rapid early growth and diminishing marginal gains.

Do not generate salary as a simple linear function of experience.

---

# 4. Recommended effect magnitudes

These are generation parameters, not final model results.

They may be adjusted, but keep them realistic relative to each other.

Example role bases:

- Data Analyst: 500000
- Business Analyst: 550000
- Software Engineer: 650000
- DevOps Engineer: 700000
- Cybersecurity Engineer: 720000
- Data Scientist: 750000
- ML Engineer: 800000
- Product Manager: 850000

Example education increments:

- High School: -50000
- Bachelor's: 0
- Master's: +120000
- PhD: +180000

Example city adjustments:

- Bengaluru: +100000
- Mumbai: +90000
- Delhi NCR: +70000
- Hyderabad: +50000
- Pune: +40000
- Chennai: +25000
- Kolkata: 0
- Ahmedabad: -15000

These should be modest enough that city is not the dominant predictor.

---

# 5. Experience behavior

Target behavior:

- 0–5 years: high marginal salary growth
- 5–12 years: continued but slower growth
- 12–20 years: diminishing growth
- 20+ years: relative flattening

Add role-dependent experience interaction so technical/leadership roles do not all grow identically.

---

# 6. Noise

Use heteroscedastic noise.

Candidates with higher expected salaries may have greater absolute salary variance.

Example:

```text
noise_std = 40000 + 0.05 * expected_salary
```

Then draw Gaussian noise.

Add a small fraction of heavier deviations to mimic noisy survey data.

---

# 7. Missingness

After salary has been generated from clean feature values:

- experience missing: approximately 2%
- certifications missing: approximately 4%

Optionally:
- small categorical missingness: <=1%

Never make missingness so severe that it dominates the project.

---

# 8. Validation

Reject or flag:

- experience < 0
- experience > 45
- certifications < 0
- certifications > 15
- salary <= 0
- unknown category labels
- impossible null target
- exact duplicate rows beyond a defined threshold

Generate a data-quality report.

---

# 9. Required generated outputs

- `data/raw/salary_survey.csv`
- `artifacts/reports/data_profile.json`
- `artifacts/reports/missingness.json`

Optional:
- parquet copy for fast loading

---

# 10. Dataset provenance text

The app/report should explain:

> This dataset is synthetically generated to combine all attributes required by the case study in a controlled and reproducible form. The generator models nonlinear salary growth, role and industry differences, geographic adjustments, interaction effects, missing values, and observational noise. Synthetic values are educational and must not be interpreted as real market salary benchmarks.
