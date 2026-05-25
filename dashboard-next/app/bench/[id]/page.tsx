import Link from "next/link";
import { notFound } from "next/navigation";
import { HonestyCallout } from "@/components/bench/honesty-callout";
import { LangsTable } from "@/components/bench/langs-table";
import { Badge } from "@/components/ui/badge";
import { getLangSeries } from "@/lib/bench-series";
import { githubTreeUrl } from "@/lib/github";
import { findRow, loadSummary } from "@/lib/summary";

type PageProps = {
  params: Promise<{ id: string }>;
};

export function generateStaticParams() {
  const summary = loadSummary();
  return summary.rows.map((row) => ({ id: row.benchmark }));
}

export default async function BenchPage({ params }: PageProps) {
  const { id } = await params;
  const summary = loadSummary();
  const row = findRow(summary, id);
  if (!row) notFound();

  const series = getLangSeries(summary, row);
  const sourceUrl = githubTreeUrl(row.repo, row.path);
  const phText = row.ph_ids.length > 0 ? row.ph_ids.join(", ") : "—";

  return (
    <main>
      <section className="placeholder">
        <h2>
          {row.benchmark} <Badge status={row.status} />
        </h2>
        <p style={{ color: "var(--muted)", fontSize: "0.9rem" }}>
          Tier {row.tier} · {row.metric}
          {row.variant ? ` · variant ${row.variant}` : ""}
        </p>

        <HonestyCallout variant={row.variant} />

        <dl
          className="mono"
          style={{
            marginTop: "1rem",
            display: "grid",
            gridTemplateColumns: "auto 1fr",
            gap: "0.35rem 1rem",
          }}
        >
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
          <dt>Li / C++</dt>
          <dd>
            {row.li_value ?? "—"} / {row.cpp_value ?? "—"}{" "}
            {row.unit ? row.unit : ""}
          </dd>
          <dt>Ratio vs C++</dt>
          <dd>
            {row.ratio_vs_cpp != null ? `${row.ratio_vs_cpp.toFixed(4)}×` : "—"}
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

        <h3 style={{ fontSize: "1rem", marginTop: "1.5rem", color: "var(--text)" }}>
          Language series
        </h3>
        <LangsTable series={series} metric={row.metric} />

        <p style={{ marginTop: "1.25rem" }}>
          <Link href="/">← Overview</Link>
        </p>
      </section>
    </main>
  );
}
