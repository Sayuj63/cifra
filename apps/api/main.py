"""CompLens inference and artifact-backed reporting API."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from ml.common import ARTIFACTS, read_json
from ml.data.generate import CITY, EDUCATION, INDUSTRY, ROLE
from ml.evaluation.explainability import local_explanation


class Candidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    experience_years: float = Field(ge=0, le=45)
    education_level: Literal[tuple(EDUCATION)]
    job_role: Literal[tuple(ROLE)]
    industry: Literal[tuple(INDUSTRY)]
    city: Literal[tuple(CITY)]
    certifications: int = Field(ge=0, le=15)


class CounterfactualRequest(BaseModel):
    candidate: Candidate
    vary: Literal["city", "education_level", "industry", "job_role"] = "city"


@lru_cache(maxsize=1)
def load_model():
    path = ARTIFACTS / "champion" / "model.joblib"
    if not path.is_file():
        raise HTTPException(
            503, detail={"code": "MODEL_UNAVAILABLE", "message": "Train the model first."}
        )
    # Only load locally generated trusted artifacts; joblib is unsafe for untrusted files.
    return joblib.load(path)


def artifact(path: Path):
    if not path.is_file():
        raise HTTPException(503, detail={"code": "ARTIFACT_UNAVAILABLE", "message": path.name})
    return read_json(path)


app = FastAPI(title="CompLens API", version="1.0.0")
origins = [
    value.strip()
    for value in os.getenv("COMPLENS_CORS_ORIGINS", "http://localhost:3000").split(",")
    if value.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/api/v1/health")
def health():
    available = (ARTIFACTS / "champion" / "model.joblib").is_file()
    metadata = read_json(ARTIFACTS / "champion" / "metadata.json") if available else {}
    return {
        "status": "ok",
        "model_loaded": available,
        "model_version": metadata.get("model_version"),
    }


@app.get("/api/v1/model")
def model_metadata():
    return artifact(ARTIFACTS / "champion" / "metadata.json")


@app.get("/api/v1/model/metrics")
def model_metrics():
    return artifact(ARTIFACTS / "champion" / "metrics.json")


@app.get("/api/v1/features")
def features():
    return artifact(ARTIFACTS / "champion" / "feature_schema.json")


@app.post("/api/v1/predict")
def predict(candidate: Candidate):
    model = load_model()
    salary = float(model.predict(pd.DataFrame([candidate.model_dump()]))[0])
    metadata = model_metadata()
    radius = metadata["interval_radius_inr"]
    return {
        "prediction": {"salary_inr": round(salary), "salary_lakh": round(salary / 100_000, 2)},
        "interval": {
            "lower_inr": round(max(0, salary - radius)),
            "upper_inr": round(salary + radius),
            "coverage": metadata["nominal_coverage"],
        },
        "model": {"family": metadata["model_family"], "version": metadata["model_version"]},
    }


@app.post("/api/v1/explain")
def explain(candidate: Candidate):
    metadata = model_metadata()
    return local_explanation(load_model(), candidate.model_dump(), metadata["reference_profile"])


@app.post("/api/v1/counterfactual")
def counterfactual(request: CounterfactualRequest):
    options = {"city": CITY, "education_level": EDUCATION, "industry": INDUSTRY, "job_role": ROLE}[
        request.vary
    ]
    rows = [{**request.candidate.model_dump(), request.vary: value} for value in options]
    predictions = load_model().predict(pd.DataFrame(rows))
    return {
        "vary": request.vary,
        "unit": "INR/year",
        "results": [
            {"value": value, "salary_inr": round(float(prediction))}
            for value, prediction in zip(options, predictions, strict=True)
        ],
        "interpretation": "Model sensitivity, not a causal or fairness conclusion.",
    }


@app.post("/api/v1/curve")
def salary_curve(candidate: Candidate):
    years = np.arange(0, 35.5, 0.5)
    profile = candidate.model_dump()
    rows = [{**profile, "experience_years": float(year)} for year in years]
    values = load_model().predict(pd.DataFrame(rows))
    return {
        "experience_years": years.tolist(),
        "salary_inr": [float(value) for value in values],
        "unit": "INR/year",
        "profile": profile,
        "interpretation": "Model response at fixed other attributes; not a causal growth forecast.",
    }


REPORTS = {
    "model-comparison": "model_comparison.json",
    "fairness": "fairness.json",
    "residuals": "residual_summary.json",
    "eda": "eda.json",
    "growth-curve": "growth_curve.json",
    "linearity": "linearity.json",
    "importance": "importance.json",
    "data-profile": "data_profile.json",
    "split": "split.json",
    "tuning": "tuning.json",
}


@app.get("/api/v1/reports/{report_name}")
def report(report_name: str):
    if report_name not in REPORTS:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "Unknown report"})
    return artifact(ARTIFACTS / "reports" / REPORTS[report_name])


PLOTS = {
    "salary_distribution",
    "salary_vs_experience",
    "salary_by_education_level",
    "salary_by_job_role",
    "salary_by_industry",
    "salary_by_city",
    "certifications",
    "residual_vs_predicted",
    "residual_vs_experience",
    "residual_histogram",
}


@app.get("/api/v1/plots/{name}")
def plot(name: str):
    if name not in PLOTS:
        raise HTTPException(404, detail="Unknown plot")
    path = ARTIFACTS / "plots" / f"{name}.png"
    if not path.is_file():
        raise HTTPException(503, detail="Plot unavailable")
    return FileResponse(path, media_type="image/png")
