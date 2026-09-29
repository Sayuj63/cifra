"use client";

import { useEffect, useState } from "react";
import { SalaryCurve } from "@/app/explain/salary-curve";
import { Notice, PageIntro, Section } from "@/components/ui";
import { money, request, type Candidate, type Explanation } from "@/lib/api";

type Importance = { feature: string; display_name: string; rmse_increase_inr: number; std: number }[];
type Counterfactual = { results: { value: string; salary_inr: number }[] };
const example: Candidate = { experience_years: 8, education_level: "Master's", job_role: "ML Engineer",
  industry: "FinTech", city: "Mumbai", certifications: 3 };

export default function Explain() {
  const [importance, setImportance] = useState<Importance | null>(null);
  const [local, setLocal] = useState<Explanation | null>(null);
  const [cities, setCities] = useState<Counterfactual | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      request<Importance>("/reports/importance"),
      request<Explanation>("/explain", example),
      request<Counterfactual>("/counterfactual", { candidate: example, vary: "city" }),
    ]).then(([global, explanation, counterfactual]) => {
      setImportance(global); setLocal(explanation); setCities(counterfactual);
    }).catch(e => setError(e.message));
  }, []);

  return <>
    <PageIntro kicker="04 / Explainability" title="Understand the estimate">
      Global importance measures predictive dependence. Local contributions explain one example candidate. Neither establishes causality.
    </PageIntro>
    {error ? <Notice kind="error">{error}</Notice> : !importance ? <Notice>Loading explanation reports...</Notice> : <>
      <Section label="Global" title="Which inputs carry predictive information?">
        <p>Permutation importance is the increase in held-out RMSE when one raw feature is shuffled. Larger values mean the fitted model relied more on that feature.</p>
        <div className="bars">{importance.map(item => {
          const max = Math.max(...importance.map(x => Math.max(0, x.rmse_increase_inr)));
          return <div className="bar-row" key={item.feature}><span>{item.display_name}</span><div className="bar-track"><div className="bar-fill" style={{ width: `${Math.max(0, item.rmse_increase_inr) / max * 100}%` }} /></div><strong className="mono">{money(item.rmse_increase_inr)}</strong></div>;
        })}</div>
        <p className="small-note top-space">Unit: change in RMSE (INR/year). A negative value means shuffling happened to improve this evaluation sample.</p>
      </Section>
      <Section label="Response" title="Explore a salary growth curve"><SalaryCurve /></Section>
      <Section label="Local" title="Why this example estimate?">
        <div className="wide-right"><div><p>The six contributions are computed by the deployed explanation method and sum to the model prediction.</p><p className="small-note">Method: {local?.method ?? "Calculating..."}</p><p className="small-note">Example: 8 years · Master&apos;s · ML Engineer · FinTech · Mumbai · 3 certifications.</p></div><div className="panel">{local ? <><div className="explanation-row"><span>Model baseline</span><strong>{money(local.baseline)}</strong></div>{local.contributions.map(item => <div className="explanation-row" key={item.feature}><span>{item.display_name}</span><strong className={item.contribution >= 0 ? "positive" : "negative"}>{item.contribution >= 0 ? "+" : "−"}{money(Math.abs(item.contribution))}</strong></div>)}<div className="explanation-row"><strong>Final estimate</strong><strong>{money(local.prediction)}</strong></div></> : <p>Calculating explanation...</p>}</div></div>
      </Section>
      <Section label="Sensitivity" title="Change only the city">
        <p>The example candidate stays fixed while the model receives each city in turn. These predictions describe model response, not a causal relocation benefit.</p>
        {cities ? <div className="data-table-wrap"><table className="data-table"><thead><tr><th>City</th><th>Predicted annual salary</th></tr></thead><tbody>{cities.results.map(row => <tr key={row.value}><td>{row.value}</td><td>{money(row.salary_inr)}</td></tr>)}</tbody></table></div> : <Notice>Calculating city scenarios...</Notice>}
      </Section>
    </>}
  </>;
}
