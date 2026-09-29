# Viva Defense Guide

## Why synthetic data?

The required feature combination is not consistently available in one public salary dataset. Synthetic generation gives reproducibility and lets the project deliberately include nonlinear experience effects, missingness, city variation, and noise. It is transparently documented and is not claimed to represent real salary markets.

## Why not preprocess before splitting?

Doing so would let information from the test set influence imputers/scalers/encoders, creating data leakage and overly optimistic evaluation.

## Why k-fold CV?

A single split can produce unstable estimates. Five-fold CV evaluates performance across multiple partitions and provides both mean performance and variability.

## Why RMSE and MAE?

MAE measures average absolute error in interpretable salary units. RMSE penalizes large errors more strongly.

## Why R² too?

R² describes the fraction of target variance explained relative to a constant baseline, but it does not communicate error magnitude in rupees, so it is not used alone.

## Why polynomial regression?

The case study specifically asks whether salary growth with experience is linear. Adding polynomial experience terms allows a direct comparison against the linear baseline.

## What does a residual plot tell you?

Residual structure can reveal:
- nonlinear patterns
- heteroscedasticity
- outliers
- systematic under/overprediction

Random residual scatter around zero is generally desirable.

## Why keep a test set separate?

Model selection and tuning can indirectly overfit validation/CV information. A final untouched test set provides a less biased estimate of final generalization.

## What is the calibration set for?

The calibration set is used to determine conformal prediction interval widths without reusing test labels.

## Is the prediction interval a confidence score?

No. A regression prediction interval gives a range intended to contain a future target value at a chosen marginal coverage rate. It is not a classification probability or confidence percentage.

## Does feature importance prove causality?

No. Importance shows model reliance/predictive contribution, not causal effect.

## Does city significance imply bias?

No. Predictive contribution or counterfactual sensitivity to city does not by itself establish unfair discrimination. It indicates that the model changes when city changes and motivates deeper investigation.

## Can you claim demographic fairness?

No. The dataset lacks protected demographic labels. The project can report subgroup diagnostics by city but cannot establish fairness across gender, caste, religion, race, disability, etc.

## Why FastAPI + Next.js instead of Streamlit?

The goal is to separate inference from presentation. The ML model lives behind a typed API, and the frontend is a real client application. This resembles production architecture more closely.
