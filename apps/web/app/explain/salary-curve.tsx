"use client";

import { useEffect, useState } from "react";
import { LineChart } from "@/components/line-chart";
import { Notice } from "@/components/ui";
import { money, request, type Candidate, type Schema } from "@/lib/api";

type Curve = { experience_years: number[]; salary_inr: number[]; unit: string };
type LockedProfile = Omit<Candidate, "experience_years">;

const initial: LockedProfile = {
  education_level: "Master's",
  job_role: "ML Engineer",
  industry: "FinTech",
  city: "Mumbai",
  certifications: 3,
};
const labels: Record<string, string> = {
  education_level: "Education",
  job_role: "Job role",
  industry: "Industry",
  city: "City",
};

export function SalaryCurve() {
  const [schema, setSchema] = useState<Schema | null>(null);
  const [profile, setProfile] = useState<LockedProfile>(initial);
  const [selectedYears, setSelectedYears] = useState(8);
  const [result, setResult] = useState<{ key: string; curve: Curve } | null>(null);
  const [failure, setFailure] = useState<{ key: string; message: string } | null>(null);
  const [schemaError, setSchemaError] = useState("");
  const profileKey = JSON.stringify(profile);
  const curve = result?.key === profileKey ? result.curve : null;
  const error = schemaError || (failure?.key === profileKey ? failure.message : "");

  useEffect(() => {
    request<Schema>("/features").then(setSchema).catch(e => setSchemaError(e.message));
  }, []);

  useEffect(() => {
    let active = true;
    request<Curve>("/curve", { ...profile, experience_years: 0 })
      .then(value => { if (active) { setResult({ key: profileKey, curve: value }); setFailure(null); } })
      .catch(e => { if (active) setFailure({ key: profileKey, message: e.message }); });
    return () => { active = false; };
  }, [profile, profileKey]);

  const selected = curve?.experience_years.indexOf(selectedYears) ?? -1;
  return <div className="wide-right">
    <div className="panel">
      <p className="small-note">Hold profile attributes fixed while experience moves across the chart.</p>
      {(["education_level", "job_role", "industry", "city"] as const).map(key =>
        <div className="field" key={key}>
          <label htmlFor={`curve-${key}`}>{labels[key]}</label>
          <select id={`curve-${key}`} value={profile[key]} disabled={!schema}
            onChange={event => setProfile({ ...profile, [key]: event.target.value })}>
            {schema?.categorical[key].map(value => <option key={value}>{value}</option>)}
          </select>
        </div>
      )}
      <div className="field">
        <label htmlFor="curve-certifications">Certifications</label>
        <input id="curve-certifications" type="number" min="0" max="15"
          value={profile.certifications}
          onChange={event => setProfile({ ...profile, certifications: Number(event.target.value) })} />
      </div>
      <div className="field">
        <label htmlFor="curve-years">Highlight experience <span className="field-value">{selectedYears} years</span></label>
        <input id="curve-years" type="range" min="0" max="35" step="0.5"
          value={selectedYears} onChange={event => setSelectedYears(Number(event.target.value))} />
      </div>
    </div>
    <div aria-live="polite">
      {error && <Notice kind="error">{error}</Notice>}
      {curve ? <>
        <LineChart x={curve.experience_years} xLabel="Experience (years)"
          yLabel="Annual salary (INR/year)" marker={selectedYears}
          series={[{ label: "Production model", values: curve.salary_inr, color: "#FF5A1F" }]} />
        <p className="top-space"><strong>{selectedYears} years: {selected >= 0 ? money(curve.salary_inr[selected]) : "—"}</strong></p>
        <p className="small-note">Each point is a model estimate for the fixed profile. The curve does not prove a causal salary path.</p>
      </> : !error && <Notice>Loading salary curve...</Notice>}
    </div>
  </div>;
}
