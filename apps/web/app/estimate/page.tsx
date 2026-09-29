"use client";

import { useEffect, useState, type FormEvent } from "react";
import { Info, Notice, PageIntro, Section } from "@/components/ui";
import { money, request, type Candidate, type Explanation, type Prediction, type Schema } from "@/lib/api";

const starter: Candidate = { experience_years: 7, education_level: "Master's", job_role: "ML Engineer",
  industry: "FinTech", city: "Mumbai", certifications: 3 };
const labels: Record<string, string> = { education_level: "Education", job_role: "Job role", industry: "Industry", city: "City" };

export default function Estimate() {
  const [schema, setSchema] = useState<Schema | null>(null);
  const [candidate, setCandidate] = useState<Candidate>(starter);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [explanation, setExplanation] = useState<Explanation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => { request<Schema>("/features").then(setSchema).catch(e => setError(e.message)); }, []);
  async function submit(event: FormEvent) {
    event.preventDefault(); setLoading(true); setError(""); setExplanation(null);
    try { const result = await request<Prediction>("/predict", candidate); setPrediction(result);
      request<Explanation>("/explain", candidate).then(setExplanation).catch(() => setExplanation(null)); }
    catch (e) { setPrediction(null); setError(e instanceof Error ? e.message : String(e)); }
    finally { setLoading(false); }
  }
  return <><PageIntro kicker="01 / Salary estimator" title="Estimate compensation">Enter a candidate profile. The API runs the serialized production pipeline and returns an annual INR estimate with an interval calibrated on held-out data.</PageIntro><Section label="Candidate profile" title="A profile, measured"><div className="wide-right"><form onSubmit={submit} className="panel"><div className="field"><label htmlFor="experience">Experience <span className="field-value">{candidate.experience_years} years</span></label><input id="experience" type="range" min="0" max="35" step="0.5" value={candidate.experience_years} onChange={e => setCandidate({ ...candidate, experience_years: Number(e.target.value) })} /></div>{(["education_level", "job_role", "industry", "city"] as const).map(key => <div className="field" key={key}><label htmlFor={key}>{labels[key]}</label><select id={key} value={candidate[key]} onChange={e => setCandidate({ ...candidate, [key]: e.target.value })} disabled={!schema}>{schema?.categorical[key].map(value => <option key={value}>{value}</option>)}</select></div>)}<div className="field"><label htmlFor="certifications">Relevant certifications</label><input id="certifications" type="number" min={schema?.numeric.certifications.min ?? 0} max={schema?.numeric.certifications.max ?? 15} value={candidate.certifications} onChange={e => setCandidate({ ...candidate, certifications: Number(e.target.value) })} /></div><button className="button primary" type="submit" disabled={!schema || loading}>{loading ? "Calculating…" : "Estimate salary →"}</button></form><div aria-live="polite">{error && <Notice kind="error">{error}</Notice>}{prediction ? <div className="panel"><span className="eyebrow">Estimated annual compensation · INR/year</span><div className="result-salary">{money(prediction.prediction.salary_inr)}</div><p>Likely range: <strong>{money(prediction.interval.lower_inr)} – {money(prediction.interval.upper_inr)}</strong></p><div className="range-track" aria-hidden="true" /><div className="range-labels"><span>{money(prediction.interval.lower_inr)}</span><span>{money(prediction.prediction.salary_inr)}</span><span>{money(prediction.interval.upper_inr)}</span></div><p className="small-note top-space">{prediction.interval.coverage * 100}% prediction interval <Info text="Calibrated on held-out absolute prediction errors; targets marginal coverage across similar future observations." /> · {prediction.model.family} v{prediction.model.version}</p>{explanation && <><h3 className="top-space">Why this estimate?</h3><p className="small-note">Model baseline {money(explanation.baseline)} ? {explanation.method}. Contributions sum to the prediction.</p><div className="explanation-list">{explanation.contributions.map(item => <div className="explanation-row" key={item.feature}><span>{item.display_name}</span><strong className={item.contribution >= 0 ? "positive" : "negative"}>{item.contribution >= 0 ? "+" : "−"}{money(Math.abs(item.contribution))}</strong></div>)}</div></>}<p className="small-note top-space">Synthetic educational data. This is model evidence, not a live market quote.</p></div> : !error && <div className="panel"><span className="eyebrow">Prediction canvas</span><h2 className="top-space">An estimate with context.</h2><p>Submit the profile to see the model prediction, calibrated range, and feature contributions. No salary formula runs in the browser.</p></div>}</div></div></Section></>;
}
