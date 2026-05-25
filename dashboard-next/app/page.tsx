import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { PILLARS } from "@/lib/pillars";
import { loadSummary } from "@/lib/summary";

const TIER_ORDER = ["0", "1", "2", "3", "5"];

export default function HomePage() {
  const summary = loadSummary();

  return (
    <main>
      <section className="placeholder" style={{ marginBottom: "1.5rem" }}>
        <h2>Overview</h2>
        <p>
          Next.js dashboard scaffold (WP1). Data from{" "}
          <span className="mono">data/latest/summary.json</span> at build time.
        </p>
        <p className="mono" style={{ marginTop: "0.75rem" }}>
          Generated: {summary.generated_at}
        </p>
      </section>

      <section className="tier-strip" aria-label="Tier status counts">
        {TIER_ORDER.map((tier) => {
          const c = summary.tier_counts[tier] ?? {
            green: 0,
            yellow: 0,
            red: 0,
            unknown: 0,
          };
          return (
            <div key={tier} className="tier-card">
              <h3>Tier {tier}</h3>
              <div className="counts">
                <span className="g">{c.green} ok</span>
                <span className="y">{c.yellow} warn</span>
                <span className="r">{c.red} fail</span>
                <span className="u">{c.unknown} ?</span>
              </div>
            </div>
          );
        })}
      </section>

      <section>
        <h2 style={{ fontSize: "1.15rem", marginBottom: "1rem" }}>Pillars</h2>
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {PILLARS.map((p) => (
            <li
              key={p.id}
              style={{
                marginBottom: "0.75rem",
                padding: "0.75rem 1rem",
                background: "var(--surface)",
                border: "1px solid var(--border)",
                borderRadius: 8,
              }}
            >
              <Link href={`/pillar/${p.id}/`}>
                <strong>{p.label}</strong>
              </Link>
              <p style={{ margin: "0.35rem 0 0", color: "var(--muted)", fontSize: "0.9rem" }}>
                {p.description}
              </p>
            </li>
          ))}
        </ul>
      </section>

      <section style={{ marginTop: "2rem" }}>
        <h2 style={{ fontSize: "1.15rem", marginBottom: "0.75rem" }}>Sample benchmarks</h2>
        <p style={{ color: "var(--muted)", fontSize: "0.9rem" }}>
          First five catalog rows (full table in a later WP):
        </p>
        <ul style={{ paddingLeft: "1.25rem" }}>
          {summary.rows.slice(0, 5).map((row) => (
            <li key={row.benchmark} style={{ marginBottom: "0.35rem" }}>
              <Link href={`/bench/${row.benchmark}/`}>{row.benchmark}</Link>{" "}
              <Badge status={row.status} />
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
