import Link from "next/link";
import { PILLARS } from "@/lib/pillars";

type HeaderProps = {
  title?: string;
  subtitle?: string;
};

export function Header({
  title = "Li Benchmarks",
  subtitle = "Performance, security, and correctness across the Li ecosystem",
}: HeaderProps) {
  return (
    <header className="site-header">
      <div className="site-header-inner">
        <div>
          <h1>
            <Link href="/">{title}</Link>
          </h1>
          {subtitle ? <p>{subtitle}</p> : null}
        </div>
        <nav className="site-nav" aria-label="Site">
          <Link href="/">Overview</Link>
          <Link href="/#search">Search</Link>
          <Link href="/matrix/">Matrix</Link>
          <Link href="/gpu-matrix/">GPU matrix</Link>
          <Link href="/history/">History</Link>
        </nav>
        <nav className="pillar-nav" aria-label="Pillars">
          {PILLARS.map((p) => (
            <Link key={p.id} href={`/pillar/${p.id}/`}>
              {p.label}
            </Link>
          ))}
          <Link href="/proofs/">Proofs ≠ bench</Link>
        </nav>
      </div>
    </header>
  );
}
