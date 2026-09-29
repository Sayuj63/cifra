export const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function request<T>(path: string, body?: unknown): Promise<T> {
  const response = await fetch(`${API}${path}`, {
    method: body === undefined ? "GET" : "POST",
    headers: body === undefined ? undefined : { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
    cache: "no-store",
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error?.detail?.message || error?.detail || `API error ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const money = (value: number) => `₹${(value / 100_000).toFixed(2)}L`;
export const shortMoney = (value: number) => `₹${(value / 100_000).toFixed(1)}L`;
export const number = (value: number, decimals = 2) => value.toFixed(decimals);

export type Candidate = {
  experience_years: number;
  education_level: string;
  job_role: string;
  industry: string;
  city: string;
  certifications: number;
};
export type Schema = {
  numeric: Record<string, { min: number; max: number }>;
  categorical: Record<string, string[]>;
};
export type Prediction = {
  prediction: { salary_inr: number; salary_lakh: number };
  interval: { lower_inr: number; upper_inr: number; coverage: number };
  model: { family: string; version: string };
};
export type Explanation = {
  baseline: number;
  prediction: number;
  method: string;
  contributions: { feature: string; display_name: string; contribution: number }[];
};
