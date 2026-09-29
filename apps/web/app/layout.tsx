import type { Metadata } from "next";
import { Nav } from "@/components/nav";
import "./globals.css";

export const metadata: Metadata = { title: "CompLens — Evidence-based salary intelligence",
  description: "Estimate compensation, understand why, and quantify uncertainty." };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><Nav /><main>{children}</main><footer className="site-footer"><span>CompLens / Synthetic compensation research</span><span>Estimates in INR/year · Educational use</span></footer></body></html>;
}
