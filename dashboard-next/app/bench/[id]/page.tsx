import Link from "next/link";
import { notFound } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { deltasForBenchmark, loadHistoryIndex } from "@/lib/history";
import { findRow, loadSummary } from "@/lib/summary";

type PageProps = { params: Promise<{ id: string }> };

export function generateStaticParams() {
  return loadSummary().rows.map((row) => ({ id: row.benchmark }));
}

export default async function BenchPage({ params }: PageProps) {
  const { id } = await params;
  const summary = loadSummary();
  const row = findRow(summary, id);
  if (!row) notFound();
  const deltas = deltasForBenchmark(loadHistoryIndex(), id);

  return (
    <main>
      <section className="placeholder">
        <h2>
          {row.benchmark} <Badge status={row.status} />
        </h2>
        <p style={{ color: "var(--muted)", fontSize: "0.9rem" }}>
          Tier {row.tier} · {row.repo} · {row.metric}
        </p>
        <dl
          className="mono"
          style={{
            marginTop: "1rem",
            display: "grid",
            gridTemplateColumns: "auto 1fr",
            gap: "0.35rem 1rem",
          }}
        >
          <dt>Path</dt>
          <dd>{row.path}</dd>
          <dt>Category</dt>
          <dd>{row.category ?? "—"}</dd>
          <dt>Pillar</dt>
          <dd>
            {row.pillar ? (
              <Link href={`/pillar/${row.pillar}/`}>{row.pillar}</Link>
            ) : (
              "—"
            )}
          </dd>
          <dt>Package</dt>
          <dd>{row.package ?? "—"}</dd>
          <dt>Li / C++</dt>
          <dd>
            {row.li_value ?? "—"} / {row.cpp_value ?? "—"}{" "}
            {row.unit ?? ""}
          </dd>
          <dt>Ratio vs C++</dt>
          <dd>
            {row.ratio_vs_cpp != null ? `${row.ratio_vs_cpp.toFixed(4)}×` : "—"}
          </dd>
          <dt>PH ids</dt>
          <dd>{row.ph_ids.join(", ") || "—"}</dd>
        </dl>
        {deltas.length > 0 ? (
          <section style={{ marginTop: "1.5rem" }}>
            <h3 style={{ fontSize: "1rem", margin: 0 }}>Latest history deltas</h3>
            <ul style={{ paddingLeft: "1.25rem", margin: "0.75rem 0 0" }}>
              {deltas.map((d, i) => (
                <li key={`${d.field}-${i}`} className="mono">
                  <strong>{d.field}</strong>:{" "}
                  {d.from !== undefined ? String(d.from) : "—"}
                  {d.to !== undefined ? ` → ${d.to}` : ""}
                  {d.delta !== undefined ? ` (Δ ${d.delta})` : ""}
                  {d.improved !== undefined
                    ? ` · ${d.improved ? "improved" : "regressed"}`
                    : ""}
                </li>
              ))}
            </ul>
            <p style={{ marginTop: "0.75rem" }}>
              <Link href="/history/">All latest deltas →</Link>
            </p>
          </section>
        ) : null}
        <p style={{ marginTop: "1.25rem" }}>
          <Link href="/">← Overview</Link>
        </p>
      </section>
    </main>
  );
}
