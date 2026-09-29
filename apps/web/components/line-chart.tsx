"use client";

import { money } from "@/lib/api";

export function LineChart({ x, series, xLabel, yLabel, marker }: { x: number[]; series: { label: string; values: number[]; color: string }[]; xLabel: string; yLabel: string; marker?: number }) {
  const width = 680, height = 330, left = 72, right = 20, top = 20, bottom = 45;
  const all = series.flatMap(s => s.values);
  const min = Math.floor(Math.min(...all) / 100_000) * 100_000;
  const max = Math.ceil(Math.max(...all) / 100_000) * 100_000;
  const px = (v: number) => left + (v - x[0]) / (x[x.length - 1] - x[0]) * (width - left - right);
  const py = (v: number) => top + (max - v) / (max - min || 1) * (height - top - bottom);
  return <div className="chart-frame"><svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label={`${yLabel} by ${xLabel}`}><line x1={left} x2={width - right} y1={height - bottom} y2={height - bottom} stroke="#D9D6CF" /><line x1={left} x2={left} y1={top} y2={height - bottom} stroke="#D9D6CF" />{[0,.25,.5,.75,1].map(t => { const value = min + (max - min) * t; const y = py(value); return <g key={t}><line x1={left} x2={width - right} y1={y} y2={y} stroke="#E8E6E1" /><text x={left - 10} y={y + 4} textAnchor="end" fontSize="11" fill="#676762">{money(value)}</text></g>; })}{[0,.25,.5,.75,1].map(t => { const value = x[0] + (x[x.length - 1] - x[0]) * t; return <text key={t} x={px(value)} y={height - 25} textAnchor="middle" fontSize="11" fill="#676762">{value.toFixed(0)}</text>; })}{series.map(s => <polyline key={s.label} fill="none" stroke={s.color} strokeWidth="2.4" points={s.values.map((v, i) => `${px(x[i])},${py(v)}`).join(" ")} />)}{marker !== undefined && series[0] && x.includes(marker) && <circle cx={px(marker)} cy={py(series[0].values[x.indexOf(marker)])} r="5" fill="#FF5A1F" stroke="#fff" strokeWidth="2" />}<text x={width / 2} y={height - 3} textAnchor="middle" fontSize="11" fill="#676762">{xLabel}</text></svg><div className="button-row chart-caption">{series.map(s => <span key={s.label}><span style={{ color: s.color }}>━━ </span>{s.label}</span>)}</div><div className="chart-caption">Vertical axis: {yLabel}</div></div>;
}
