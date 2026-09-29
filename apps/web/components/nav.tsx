"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const links = [["/estimate", "Estimate"], ["/explore", "Explore"], ["/model-lab", "Model Lab"],
  ["/explain", "Explain"], ["/fairness", "Fairness"], ["/methodology", "Methodology"]];

export function Nav() {
  const path = usePathname();
  const [open, setOpen] = useState(false);
  return <header className="site-header"><div className="header-inner"><Link className="brand" href="/" onClick={() => setOpen(false)}><span className="brand-mark">C<span>.</span></span><span>CompLens</span></Link><button className="mobile-menu" type="button" aria-expanded={open} aria-controls="main-nav" onClick={() => setOpen(!open)}>Menu</button><nav id="main-nav" className={open ? "nav open" : "nav"} aria-label="Primary navigation">{links.map(([href, label]) => <Link key={href} className={path === href ? "active" : ""} href={href} onClick={() => setOpen(false)}>{label}</Link>)}</nav><span className="header-caption">Salary intelligence / India</span></div></header>;
}
