"""Meaningful reproducibility and leakage checks."""

import numpy as np
import pandas as pd
from sklearn.base import clone

from ml.data.generate import FEATURES, generate
from ml.data.validate import validate
from ml.models.definitions import make_model
from ml.models.train import split


def test_generation_is_deterministic_and_non_linear():
    one = generate(1000, 42)
    two = generate(1000, 42)
    pd.testing.assert_frame_equal(one, two)
    assert validate(one)["valid"]
    assert one.experience_years.isna().any()
    assert one.certifications.isna().any()
    assert (one.salary > 0).all()


def test_split_is_disjoint_and_preprocessing_is_fit_only_on_train():
    frame = generate(400, 42)
    train, calibration, test = split(frame)
    assert len(train) == 280 and len(calibration) == len(test) == 60
    assert not set(train.index) & set(test.index)
    x = train[FEATURES].copy()
    y = train.salary
    model = make_model("Linear Regression").fit(x, y)
    original = (
        model.named_steps["preprocess"]
        .named_transformers_["experience"]
        .named_steps["impute"]
        .statistics_[0]
    )
    changed_test = test[FEATURES].copy()
    changed_test["experience_years"] = 45
    model.predict(changed_test)
    later = (
        model.named_steps["preprocess"]
        .named_transformers_["experience"]
        .named_steps["impute"]
        .statistics_[0]
    )
    assert original == later == np.nanmedian(x.experience_years)
    unknown = changed_test.iloc[:1].copy()
    unknown["city"] = "Unseen city"
    assert np.isfinite(model.predict(unknown)[0])
    assert clone(model) is not model
