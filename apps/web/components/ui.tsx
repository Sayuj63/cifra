"use client";

import { Tooltip } from "@base-ui/react/tooltip";
import type { ReactNode } from "react";

export function Eyebrow({ children }: { children: ReactNode }) { return <span className="eyebrow">{children}</span>; }
export function PageIntro({ kicker, title, children }: { kicker: string; title: string; children: ReactNode }) {
  return <header className="page-intro"><Eyebrow>{kicker}</Eyebrow><h1>{title}</h1><p>{children}</p></header>;
}
export function Notice({ children, kind = "note" }: { children: ReactNode; kind?: "note" | "error" }) {
  return <div className={`notice ${kind}`} role={kind === "error" ? "alert" : undefined}>{children}</div>;
}
export function Info({ text }: { text: string }) {
  return <Tooltip.Provider><Tooltip.Root><Tooltip.Trigger className="info-trigger" aria-label="More information">i</Tooltip.Trigger><Tooltip.Portal><Tooltip.Positioner sideOffset={8}><Tooltip.Popup className="tooltip">{text}</Tooltip.Popup></Tooltip.Positioner></Tooltip.Portal></Tooltip.Root></Tooltip.Provider>;
}
export function Section({ label, title, children }: { label: string; title: string; children: ReactNode }) {
  return <section className="section"><div className="section-heading"><Eyebrow>{label}</Eyebrow><h2>{title}</h2></div>{children}</section>;
}
export function Metric({ label, value, note }: { label: string; value: string; note?: string }) {
  return <div className="metric"><span className="eyebrow">{label}</span><strong>{value}</strong>{note && <small>{note}</small>}</div>;
}
