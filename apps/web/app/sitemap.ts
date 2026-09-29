import type { MetadataRoute } from "next";
import { siteUrl } from "@/lib/site";

const routes = ["/", "/estimate", "/explore", "/model-lab", "/explain", "/fairness", "/methodology"];

export default function sitemap(): MetadataRoute.Sitemap {
  return routes.map((route) => ({ url: `${siteUrl}${route}`, changeFrequency: "monthly" }));
}
