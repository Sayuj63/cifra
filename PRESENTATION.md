# Cifra presentation outline

1. **Problem.** A recruitment consultancy needs evidence-based annual salary estimates in INR. Open the landing page.
2. **Data.** Show Methodology: 7,500 deterministic synthetic candidates, six features, and controlled missingness. Explain that the figures are educational.
3. **Hypothesis.** Open Explore and show the salary-versus-experience scatter. The generator contains saturating experience growth.
4. **Linearity test.** Linear CV RMSE is ₹1.52L; polynomial is ₹1.27L, a 16.9% improvement. Show the two curves.
5. **Experiment.** Open Model Lab. Compare the five required algorithms on identical five training folds. Selection uses CV RMSE before test evaluation.
6. **Champion.** Gradient Boosting wins training CV. Held-out test R² is 0.850, RMSE ₹1.25L, and MAE ₹0.97L. Show residual plots.
7. **Reproducibility.** Show `dvc dag`, `dvc.lock`, and the local JSON experiment reports. Open W&B only if a credentialed run was actually logged.
8. **Prediction.** Enter a candidate in Estimate. Point out that the browser calls FastAPI and the serialized sklearn pipeline.
9. **Uncertainty and explanation.** Show the 90% split-conformal prediction interval, observed test coverage 90.1%, and the real local contributions. Top global permutation feature: Experience.
10. **City and limits.** Open Fairness. City ablation changes CV RMSE by ₹0.04L. Discuss subgroup sample counts, interval coverage, synthetic-data limits, and why demographic fairness cannot be established.

Close with the measured answer to each research question rather than a generic model claim. The live product and `REPORT.md` are the evidence.
