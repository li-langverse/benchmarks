import Link from "next/link";
import { notFound } from "next/navigation";
import { BenchFacetComposition } from "@/components/bench/bench-facet-composition";
import { ValidityBadge } from "@/components/bench/validity-badge";
import { Badge } from "@/components/ui/badge";
import { getLangSeries } from "@/lib/bench-series";
import { deltasForBenchmark, loadHistoryIndex } from "@/lib/history";
import { githubTreeUrl } from "@/lib/github";
import { isPerfClaimable } from "@/lib/validity";
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
  const series = getLangSeries(summary, row);
  const sourceUrl = githubTreeUrl(row.repo, row.path);
  const phText = row.ph_ids.length > 0 ? row.ph_ids.join(", ") : "—";
  const deltas = deltasForBenchmark(loadHistoryIndex(), id);
  const lowerIsBetter =
    row.metric === "wall_time" ||
    row.metric === "latency" ||
    row.metric === "latency_p95";
  const perfClaimable = isPerfClaimable(row);

  return (
    <main>
      <section className="placeholder">
        <h2>
          {row.benchmark} <Badge status={row.status} />
          {row.validity_status ? (
            <ValidityBadge
              status={row.validity_status}
              source={row.validity_source}
            />
          ) : null}
        </h2>
        <p style={{ color: "var(--muted)", fontSize: "0.9rem" }}>
          Tier {row.tier} · {row.metric}
          {row.size_label ? ` · ${row.size_label}` : row.problem_size ? ` · ${row.problem_size}` : ""}
          {row.variant ? ` · variant ${row.variant}` : ""}
          {row.os ? ` · OS ${row.os}` : ""}
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
          <dt>Problem size</dt>
          <dd>
            {row.size_label ?? row.problem_size ?? "—"}
            {row.base_id ? (
              <span className="mono" style={{ color: "var(--muted)" }}>
                {" "}
                (family <code>{row.base_id}</code>)
              </span>
            ) : null}
          </dd>
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
          <dd>
            {row.package ? (
              <Link href={`/packages/${row.package}/`}>{row.package}</Link>
            ) : (
              "—"
            )}
          </dd>
          <dt>Li / catalog oracle</dt>
          <dd>
            {row.li_value ?? "—"} / {row.cpp_value ?? "—"}{" "}
            {row.unit ?? ""}
            {row.compare_oracle ? (
              <span className="mono"> ({row.compare_oracle})</span>
            ) : null}
          </dd>
          <dt>Ratio vs catalog oracle</dt>
          <dd>
            {row.ratio_vs_cpp != null ? `${row.ratio_vs_cpp.toFixed(4)}×` : "—"}
          </dd>
          <dt>Best competitor</dt>
          <dd>
            {row.sota_lang ?? "—"}
            {row.sota_value != null ? ` (${row.sota_value} ${row.unit ?? ""})` : ""}
          </dd>
          <dt>Li relative speed vs SOTA</dt>
          <dd>
            {row.ratio_vs_sota != null ? (
              <>
                {row.ratio_vs_sota.toFixed(3)}{" "}
                <span className="mono" style={{ color: "var(--muted)" }}>
                  (1.0 = <code>{row.sota_lang ?? "best competitor"}</code> speed)
                </span>
              </>
            ) : (
              "—"
            )}
          </dd>
          <dt>Threshold</dt>
          <dd>{row.threshold_ratio_cpp}×</dd>
          <dt>Source</dt>
          <dd>
            <a href={sourceUrl} target="_blank" rel="noopener noreferrer">
              {row.repo}/{row.path}
            </a>
          </dd>
        </dl>

        <p style={{ marginTop: "1rem" }}>
          <span className="mono" style={{ color: "var(--muted)" }}>
            PH ids:{" "}
          </span>
          {phText}
        </p>

        <BenchFacetComposition
          row={row}
          series={series}
          lowerIsBetter={lowerIsBetter}
          perfClaimable={perfClaimable}
        />

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
          {row.pillar ? (
            <>
              {" · "}
              <Link href={`/pillar/${row.pillar}/`}>Pillar {row.pillar}</Link>
            </>
          ) : null}
        </p>
      </section>
    </main>
  );
}
