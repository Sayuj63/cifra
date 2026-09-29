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

  useEffect(() => {
    Promise.all([
      request<Meta>("/model"),
      request<Metrics>("/model/metrics"),
      request<Profile>("/reports/data-profile"),
    ]).then(([meta, metrics, profile]) => setData({ meta, metrics, profile }))
      .catch((cause) => setError(String(cause.message)));
  }, []);

  return <>
    <div className="hero">
      <div className="hero-copy">
        <span className="hero-badge"><span className="status-dot" /> EVIDENCE-BASED SALARY INTELLIGENCE <span aria-hidden="true">↗</span></span>
        <h1>Salary estimates.<br /><span>With evidence.</span></h1>
        <p>CompLens benchmarks candidate compensation using five validated regression approaches and exposes the uncertainty and reasoning behind every estimate.</p>
        <div className="button-row"><Link className="button primary" href="/estimate">Estimate compensation <span aria-hidden="true">→</span></Link><Link className="button" href="/model-lab">Explore the model <span aria-hidden="true">↗</span></Link></div>
        <div className="hero-note"><span /> MODEL EXECUTION BY <strong>scikit-learn</strong> <span /></div>
      </div>
      <div className="hero-evidence">
        <div className="evidence-bar"><div><span className="evidence-mark">C<span>.</span></span><span>COMPLENS</span><span className="evidence-divider">/</span><span>production-model</span></div><span><i /> LIVE MODEL EVIDENCE</span></div>
        <div className="evidence-body"><div className="evidence-title"><span className="eyebrow">01 → 05&nbsp;&nbsp; FROM COMPARISON TO DEPLOYMENT</span><h2>One model. A visible proof trail.</h2><p>Every figure below is served from the trained model artifact.</p></div><div className="evidence-result"><span className="eyebrow">Selected regressor</span>{data ? <><h3>{data.meta.model_family}</h3><span className="status">CHAMPION · v{data.meta.model_version}</span></> : error ? <Notice kind="error">Model evidence unavailable. {error}</Notice> : <p>Loading validated model evidence…</p>}</div></div>
        {data && <div className="evidence-grid"><Metric label="5-fold CV RMSE" value={money(data.metrics.cross_validation.mean.rmse)} note="INR/year" /><Metric label="CV R²" value={number(data.metrics.cross_validation.mean.r2, 3)} /><Metric label="Test interval coverage" value={`${number(data.metrics.interval.test_coverage * 100, 1)}%`} note="90% nominal interval" /><Metric label="Dataset" value={data.profile.rows.toLocaleString()} note="synthetic candidates" /></div>}
        <div className="evidence-foot"><span>ISOLATED TEST · CALIBRATED INTERVAL · SERIALIZED PIPELINE</span><Link href="/model-lab">INSPECT RESULTS <span aria-hidden="true">→</span></Link></div>
      </div>
      <div className="hero-bottom"><span>+ &nbsp; Five required regression models</span><span>+ &nbsp; Held-out test evaluation</span><span>+ &nbsp; A range you can inspect</span><span>SCROLL TO EXPLORE ↓</span></div>
    </div>
    <Section label="01 / One workflow" title="An estimate you can inspect"><div className="feature-grid"><article><span className="eyebrow">01 / ESTIMATE</span><h3>One candidate, one measured range.</h3><p>Use the deployed sklearn pipeline to produce a point prediction and a calibrated prediction interval.</p><Link href="/estimate">Open estimator →</Link></article><article><span className="eyebrow">02 / UNDERSTAND</span><h3>See what changed the result.</h3><p>Inspect model attributions, global importance, and controlled city scenarios.</p><Link href="/explain">View explanations →</Link></article><article><span className="eyebrow">03 / VERIFY</span><h3>Follow the model evidence.</h3><p>Compare five required regressors on the same five training folds, then inspect the untouched test result.</p><Link href="/model-lab">Enter Model Lab →</Link></article></div></Section>
    <Section label="02 / Scope" title="Built as a reproducible research instrument"><p>CompLens uses a transparent synthetic dataset for an academic case study. Values are educational examples and are not live market salary benchmarks.</p></Section>
  </>;
}
