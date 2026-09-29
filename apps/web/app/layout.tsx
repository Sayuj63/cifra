import type { Metadata, Viewport } from "next";
import "@fontsource-variable/inter";
import "@fontsource-variable/space-grotesk";
import { Nav } from "@/components/nav";
import { siteDescription, siteName, siteTitle, siteUrl } from "@/lib/site";
import "./globals.css";
import "./arrow-theme.css";

const logo = "/cifra-logo.png";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: { default: siteTitle, template: `%s | ${siteName}` },
  description: siteDescription,
  applicationName: siteName,
  category: "education",
  keywords: ["Cifra", "salary estimator", "salary prediction", "machine learning", "India", "prediction interval", "model explainability"],
  alternates: { canonical: "/" },
  icons: {
    icon: [{ url: logo, type: "image/png", sizes: "any" }],
    shortcut: logo,
    apple: [{ url: logo, type: "image/png" }],
  },
  manifest: "/manifest.webmanifest",
  openGraph: {
    type: "website",
    url: siteUrl,
    siteName,
    title: siteTitle,
    description: siteDescription,
    images: [{ url: logo, width: 1254, height: 1254, alt: "Cifra orange C logo with a rising salary chart" }],
  },
  twitter: {
    card: "summary",
    title: siteTitle,
    description: siteDescription,
    images: [logo],
  },
};

export const viewport: Viewport = {
  themeColor: "#ffffff",
  colorScheme: "light",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><a className="skip-link" href="#main-content">Skip to content</a><Nav /><main id="main-content">{children}</main><footer className="site-footer"><span>Cifra / Synthetic compensation research</span><span>Estimates in INR/year · Educational use</span></footer></body></html>;
}
