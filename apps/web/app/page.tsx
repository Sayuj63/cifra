"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Metric, Notice, Section } from "@/components/ui";
import { money, number, request } from "@/lib/api";

type Meta = { model_family: string; model_version: string; dataset_version: string };
type Metrics = { cross_validation: { mean: { rmse: number; r2: number } }; interval: { test_coverage: number } };
type Profile = { rows: number };

export default function Home() {
  const [data, setData] = useState<{ meta: Meta; metrics: Metrics; profile: Profile } | null>(null);
  const [error, setError] = useState("");
  useEffect(() => { Promise.all([request<Meta>("/model"), request<Metrics>("/model/metrics"), request<Profile>("/reports/data-profile")])
    .then(([meta, metrics, profile]) => setData({ meta, metrics, profile })).catch(e => setError(String(e.message))); }, []);
  return <><div className="hero"><div><span className="eyebrow">Evidence-based salary intelligence</span><h1>Salary estimates,<br />with evidence<span style={{ color: "var(--orange)" }}>.</span></h1><p>CompLens benchmarks candidate compensation using five validated regression approaches and exposes the uncertainty and reasoning behind every estimate.</p><div className="button-row"><Link className="button primary" href="/estimate">Estimate compensation →</Link><Link className="button" href="/model-lab">Explore the model</Link></div></div><aside className="hero-evidence"><span className="eyebrow">Production model</span>{data ? <><h3>{data.meta.model_family} <span className="small-note">v{data.meta.model_version}</span></h3><div className="evidence-grid"><Metric label="5-fold CV RMSE" value={money(data.metrics.cross_validation.mean.rmse)} note="INR/year" /><Metric label="CV R²" value={number(data.metrics.cross_validation.mean.r2, 3)} /><Metric label="Test interval coverage" value={`${number(data.metrics.interval.test_coverage * 100, 1)}%`} note="90% nominal interval" /><Metric label="Dataset" value={data.profile.rows.toLocaleString()} note="synthetic candidates" /></div></> : error ? <Notice kind="error">Model artifacts unavailable. Run the training pipeline to populate this evidence panel. {error}</Notice> : <p className="muted">Loading validated model evidence…</p>}</aside></div><Section label="One workflow" title="An estimate you can inspect"><div className="feature-grid"><article><span className="eyebrow">01 / Estimate</span><h3>One candidate, one measured range.</h3><p>Use the deployed sklearn pipeline to produce a point prediction and a calibrated prediction interval.</p><Link href="/estimate">Open estimator →</Link></article><article><span className="eyebrow">02 / Understand</span><h3>See what changed the result.</h3><p>Inspect model attributions, global importance, and controlled city scenarios.</p><Link href="/explain">View explanations →</Link></article><article><span className="eyebrow">03 / Verify</span><h3>Follow the model evidence.</h3><p>Compare five required regressors on the same five training folds, then inspect the untouched test result.</p><Link href="/model-lab">Enter Model Lab →</Link></article></div></Section><Section label="Scope" title="Built as a reproducible research instrument"><p>CompLens uses a transparent synthetic dataset for an academic case study. Values are educational examples and are not live market salary benchmarks.</p></Section></>;
}
