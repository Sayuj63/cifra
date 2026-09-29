"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const links = [["/estimate", "Estimate"], ["/explore", "Explore"], ["/model-lab", "Model Lab"],
  ["/explain", "Explain"], ["/fairness", "Fairness"], ["/methodology", "Methodology"]];

export function Nav() {
  const path = usePathname();
  const [open, setOpen] = useState(false);
  return <header className="site-header"><div className="header-inner"><Link className="brand" href="/" onClick={() => setOpen(false)}><span className="brand-mark" aria-hidden="true">C<span>.</span></span><span>COMPLENS</span></Link><nav id="main-nav" className={open ? "nav open" : "nav"} aria-label="Primary navigation">{links.map(([href, label]) => <Link key={href} className={path === href ? "active" : ""} href={href} onClick={() => setOpen(false)}>{label}</Link>)}</nav><Link className="header-cta" href="/estimate" onClick={() => setOpen(false)}>Estimate salary <span aria-hidden="true">→</span></Link><button className="mobile-menu" type="button" aria-label="Menu" aria-expanded={open} aria-controls="main-nav" onClick={() => setOpen(!open)}><span /><span /></button></div></header>;
}
