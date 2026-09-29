"""Generate the model card and college report from real artifact values."""

from ml.common import ARTIFACTS, ROOT, read_json


def build() -> None:
    champion = ARTIFACTS / "champion"
    reports = ARTIFACTS / "reports"
    meta = read_json(champion / "metadata.json")
    metrics = read_json(champion / "metrics.json")
    comparison = read_json(reports / "model_comparison.json")
    profile = read_json(reports / "data_profile.json")
    linearity = read_json(reports / "linearity.json")
    fairness = read_json(reports / "fairness.json")
    test = metrics["test"]
    rows = [
        f"| {item['model']} | {item['cv']['mean']['r2']:.3f} | "
        f"₹{item['cv']['mean']['rmse'] / 100000:.2f}L | "
        f"₹{item['cv']['mean']['mae'] / 100000:.2f}L |"
        for item in comparison["models"]
    ]
    card = f"""# CompLens Model Card

## Model identity

- Version: {meta["model_version"]}
- Champion: {meta["model_family"]}
- Dataset SHA-256: `{meta["dataset_sha256"]}`
- Training timestamp (UTC): {meta["trained_at"]}
- Task: annual salary regression in INR/year

## Intended use

Demonstrate reproducible salary estimation for an academic case study using synthetic Indian candidate profiles. The output is an educational benchmark, not a real compensation offer or market quote.

## Inputs and training data

Features: experience years, education level, job role, industry, city, and certification count. The deterministic generator creates {profile["rows"]:,} rows with nonlinear experience growth, role interactions, salary-dependent noise, and controlled missingness. It is not a real survey.

## Evaluation

One deterministic 70/15/15 train/calibration/test split, seed {meta["random_seed"]}. Model selection uses five shuffled training folds and lowest mean CV RMSE. The test partition is held out from selection.

| Model | CV R² | CV RMSE (INR/year) | CV MAE (INR/year) |
|---|---:|---:|---:|
{chr(10).join(rows)}

Champion held-out test: R² {test["r2"]:.3f}; MSE {test["mse"]:,.0f} INR²; RMSE ₹{test["rmse"] / 100000:.2f}L/year; MAE ₹{test["mae"] / 100000:.2f}L/year.

## Prediction uncertainty

The interval uses the finite-sample split-conformal absolute residual quantile on {meta["calibration_rows"]:,} separate calibration rows. Nominal coverage is {meta["nominal_coverage"]:.0%}; observed held-out test coverage is {metrics["interval"]["test_coverage"]:.1%}. Marginal coverage does not guarantee coverage for every individual or city subgroup.

## Explainability and fairness

Global importance is measured by permutation RMSE increase. Tree-based champions use Tree SHAP on transformed features, grouped back to six raw inputs. Other champions use exact six-feature Shapley values against a fixed reference profile. City ablation compares the same model family and folds with and without city. Geographic error and coverage are evaluated on the held-out test set with subgroup counts.

## Limitations and failure modes

- Synthetic salary relationships may not reflect real compensation markets.
- The input omits company size, seniority, negotiation, equity, and local market shifts.
- Missing values use fold-local median imputation; unusual incomplete profiles may be less reliable.
- Protected-class labels are absent, so demographic fairness cannot be established.
- Feature importance and city sensitivity are predictive associations, not causal effects.
- A 90% marginal interval can have lower coverage for an individual subgroup.

## Reproduction

Run `python -m ml.data.generate`, `python -m ml.evaluation.eda`, and `python -m ml.models.train --trials 3`, or `dvc repro`. Training produces the model, metadata, reports, plots, and calibration radius. No test labels enter hyperparameter selection.
"""
    (ROOT / "MODEL_CARD.md").write_text(card, encoding="utf-8")
    report = f"""# CompLens — Employee Salary Prediction Case Study

## Problem and data

Estimate annual salary in INR/year from six candidate attributes for a recruitment consultancy scenario. The project uses {profile["rows"]:,} deterministic synthetic profiles because the required attributes are not consistently available together in one public survey. SHA-256: `{profile["sha256"]}`. Missing experience: {profile["missing_pct"]["experience_years"]:.2f}%; missing certifications: {profile["missing_pct"]["certifications"]:.2f}%. The data is educational and is not a live salary benchmark.

## Method

The generator combines role, education, industry, city, certifications, a saturating experience function, role-by-experience interaction, and heteroscedastic noise. Data is split before any preprocessing: 70% training ({read_json(reports / "split.json")["train"]:,}), 15% calibration, 15% testing. Each sklearn pipeline imputes numeric values with training-fold medians, imputes categorical values with training-fold modes, one-hot encodes categories, and ignores unknown categories. Polynomial regression adds only an experience-squared term.

Five required algorithms are compared with 5-fold shuffled cross-validation on the training partition. Optuna searches tree-family hyperparameters using CV RMSE. Selection uses mean CV RMSE, then MAE and model name for ties. The held-out test is evaluated once after selection.

## Cross-validation results

| Model | CV R² | CV RMSE (INR/year) | CV MAE (INR/year) |
|---|---:|---:|---:|
{chr(10).join(rows)}

Selected champion: **{meta["model_family"]}**. Test R² {test["r2"]:.3f}, MSE {test["mse"]:,.0f} INR², RMSE ₹{test["rmse"] / 100000:.2f}L/year, MAE ₹{test["mae"] / 100000:.2f}L/year. Residual plots are stored in `artifacts/plots/`.

## Research questions

**Is salary growth with experience linear?** {linearity["conclusion"]} Linear CV RMSE is ₹{linearity["linear_cv_rmse"] / 100000:.2f}L versus polynomial ₹{linearity["polynomial_cv_rmse"] / 100000:.2f}L, an improvement of {linearity["rmse_improvement_pct"]:.1f}%. The generator itself contains a saturating experience term.

**Does city contribute predictive information?** With-city CV RMSE is ₹{fairness["ablation"]["with_city_cv_rmse"] / 100000:.2f}L versus without-city ₹{fairness["ablation"]["without_city_cv_rmse"] / 100000:.2f}L. Delta: ₹{fairness["ablation"]["delta_rmse"] / 100000:.2f}L. This is an ablation, not a causal claim.

**How uncertain is an estimate?** A separate calibration set sets a 90% split-conformal interval; test coverage is {metrics["interval"]["test_coverage"]:.1%}. The interval targets marginal coverage, not individual certainty.

**What attributes matter?** `artifacts/reports/importance.json` records permutation RMSE increases from held-out data; the Explain page visualizes the actual ranking. Importance is predictive, not causal.

**What fairness limits remain?** Test MAE, RMSE, mean residual, sample count, and interval coverage are reported for each city. No protected-class labels exist, so demographic fairness cannot be established.

## System and limitations

FastAPI loads the serialized pipeline and artifact metadata. Next.js calls the API and never computes salary in JavaScript. DVC records generate → EDA/train dependencies; optional W&B logging records metrics and the champion artifact when credentials are supplied. Synthetic data, omitted compensation drivers, and geographic subgroup variation limit real-world applicability. See `MODEL_CARD.md` for failure modes and retraining steps.
"""
    (ROOT / "REPORT.md").write_text(report, encoding="utf-8")
    strongest = read_json(reports / "importance.json")[0]
    presentation = f"""# CompLens presentation outline

1. **Problem.** A recruitment consultancy needs evidence-based annual salary estimates in INR. Open the landing page.
2. **Data.** Show Methodology: {profile["rows"]:,} deterministic synthetic candidates, six features, and controlled missingness. Explain that the figures are educational.
3. **Hypothesis.** Open Explore and show the salary-versus-experience scatter. The generator contains saturating experience growth.
4. **Linearity test.** Linear CV RMSE is ₹{linearity["linear_cv_rmse"] / 100000:.2f}L; polynomial is ₹{linearity["polynomial_cv_rmse"] / 100000:.2f}L, a {linearity["rmse_improvement_pct"]:.1f}% improvement. Show the two curves.
5. **Experiment.** Open Model Lab. Compare the five required algorithms on identical five training folds. Selection uses CV RMSE before test evaluation.
6. **Champion.** {meta["model_family"]} wins training CV. Held-out test R² is {test["r2"]:.3f}, RMSE ₹{test["rmse"] / 100000:.2f}L, and MAE ₹{test["mae"] / 100000:.2f}L. Show residual plots.
7. **Reproducibility.** Show `dvc dag`, `dvc.lock`, and the local JSON experiment reports. Open W&B only if a credentialed run was actually logged.
8. **Prediction.** Enter a candidate in Estimate. Point out that the browser calls FastAPI and the serialized sklearn pipeline.
9. **Uncertainty and explanation.** Show the 90% split-conformal prediction interval, observed test coverage {metrics["interval"]["test_coverage"]:.1%}, and the real local contributions. Top global permutation feature: {strongest["display_name"]}.
10. **City and limits.** Open Fairness. City ablation changes CV RMSE by ₹{fairness["ablation"]["delta_rmse"] / 100000:.2f}L. Discuss subgroup sample counts, interval coverage, synthetic-data limits, and why demographic fairness cannot be established.

Close with the measured answer to each research question rather than a generic model claim. The live product and `REPORT.md` are the evidence.
"""
    (ROOT / "PRESENTATION.md").write_text(presentation, encoding="utf-8")


if __name__ == "__main__":
    build()
