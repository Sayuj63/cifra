import type { Metadata } from "next";
import "@fontsource-variable/inter";
import "@fontsource-variable/space-grotesk";
import { Nav } from "@/components/nav";
import "./globals.css";
import "./arrow-theme.css";

export const metadata: Metadata = { title: "CompLens — Evidence-based salary intelligence",
  description: "Estimate compensation, understand why, and quantify uncertainty." };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><a className="skip-link" href="#main-content">Skip to content</a><Nav /><main id="main-content">{children}</main><footer className="site-footer"><span>CompLens / Synthetic compensation research</span><span>Estimates in INR/year · Educational use</span></footer></body></html>;
}
