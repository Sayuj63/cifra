"""Prediction contract and unavailable-artifact behavior."""

from fastapi.testclient import TestClient

from apps.api import main
from ml.evaluation.explainability import shap_module

CLIENT = TestClient(main.app)
VALID = {
    "experience_years": 7,
    "education_level": "Master's",
    "job_role": "ML Engineer",
    "industry": "FinTech",
    "city": "Mumbai",
    "certifications": 3,
}


def test_rejects_bad_candidate():
    assert CLIENT.post("/api/v1/predict", json={**VALID, "experience_years": -1}).status_code == 422
    assert CLIENT.post("/api/v1/predict", json={**VALID, "city": "Atlantis"}).status_code == 422
    assert CLIENT.post("/api/v1/predict", json={**VALID, "unknown": 1}).status_code == 422


def test_unavailable_model_is_explicit(monkeypatch, tmp_path):
    main.load_model.cache_clear()
    monkeypatch.setattr(main, "ARTIFACTS", tmp_path)
    response = CLIENT.post("/api/v1/predict", json=VALID)
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "MODEL_UNAVAILABLE"
    main.load_model.cache_clear()


def test_real_prediction_after_training():
    if not (main.ARTIFACTS / "champion" / "model.joblib").exists():
        return
    response = CLIENT.post("/api/v1/predict", json=VALID)
    assert response.status_code == 200
    data = response.json()
    assert (
        data["interval"]["lower_inr"]
        <= data["prediction"]["salary_inr"]
        <= data["interval"]["upper_inr"]
    )
    explanation = CLIENT.post("/api/v1/explain", json=VALID).json()
    assert (
        abs(
            explanation["baseline"]
            + sum(x["contribution"] for x in explanation["contributions"])
            - explanation["prediction"]
        )
        < 1e-6
    )
    if shap_module() is not None and main.model_metadata()["model_family"] in {
        "Decision Tree",
        "Random Forest",
        "Gradient Boosting",
    }:
        assert explanation["method"] == "Tree SHAP grouped by raw feature"

    curve_response = CLIENT.post("/api/v1/curve", json=VALID)
    assert curve_response.status_code == 200
    curve = curve_response.json()
    index = curve["experience_years"].index(VALID["experience_years"])
    assert round(curve["salary_inr"][index]) == data["prediction"]["salary_inr"]
