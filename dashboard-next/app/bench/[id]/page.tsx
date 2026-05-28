import Link from "next/link";
import { notFound } from "next/navigation";
import { HonestyCallout } from "@/components/bench/honesty-callout";
import { LangsTable } from "@/components/bench/langs-table";
import { PerfRelativeBars } from "@/components/bench/perf-relative-bars";
import { OsTable } from "@/components/bench/os-table";
import { PerfNotClaimable } from "@/components/bench/perf-not-claimable";
import { NumericValidityPanel } from "@/components/bench/numeric-validity-panel";
import { ValidityPanel } from "@/components/bench/validity-panel";
import { ValidityBadge } from "@/components/bench/validity-badge";
import { Badge } from "@/components/ui/badge";
import { getLangSeries } from "@/lib/bench-series";
import { deltasForBenchmark, loadHistoryIndex } from "@/lib/history";
import { githubTreeUrl } from "@/lib/github";
import { isPerfClaimable } from "@/lib/validity";
import { formatMeanStd } from "@/lib/format-measurement";
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
        <h2 className="bench-page-title">
          <span title={row.benchmark}>{row.benchmark}</span>{" "}
          <Badge status={row.status} />
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

        <HonestyCallout variant={row.variant} />
        <PerfNotClaimable row={row} />
        <ValidityPanel row={row} />
        <NumericValidityPanel row={row} />

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
          <dt>Li / catalog oracle (mean ± σ)</dt>
          <dd>
            {formatMeanStd(
              row.li_value,
              row.li_stddev,
              row.unit,
              row.li_sample_runs,
            )}{" "}
            /{" "}
            {formatMeanStd(
              row.cpp_value,
              row.cpp_stddev,
              row.unit,
              row.cpp_sample_runs,
            )}
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
          <dt>Validity</dt>
          <dd>
            {row.validity_status ? (
              <ValidityBadge
                status={row.validity_status}
                source={row.validity_source}
              />
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

        <h3 className="bench-panel-heading">Performance vs best competitor</h3>
        {row.compare_oracle ? (
          <p className="mono bench-compare-oracle">
            Compare oracle: <code>{row.compare_oracle}</code>
          </p>
        ) : null}
        <PerfRelativeBars
          series={series}
          sotaLang={row.sota_lang}
          lowerIsBetter={lowerIsBetter}
          claimable={perfClaimable}
          pending={row.pending}
        />

        <h3 style={{ fontSize: "1rem", marginTop: "1.5rem", color: "var(--text)" }}>
          Absolute measurements
        </h3>
        <LangsTable series={series} metric={row.metric} />
        <OsTable row={row} series={series} />

        {deltas.length > 0 || row.numeric_validity?.ulps != null ? (
          <section className="bench-history-section" aria-labelledby="bench-history-heading">
            <h3 id="bench-history-heading" className="bench-panel-heading">
              Latest history deltas
            </h3>
            {row.numeric_validity?.ulps != null ? (
              <p className="mono bench-history-ulp">
                Current analytical deviation: <strong>{row.numeric_validity.ulps}</strong>{" "}
                ULP{row.numeric_validity.ulps === 1 ? "" : "s"}
                {row.numeric_validity.within_1ulp === true
                  ? " (within 1 ULP — oracle agreement)"
                  : row.numeric_validity.within_1ulp === false
                    ? " (over 1 ULP — investigate codegen / fast-math)"
                    : null}
              </p>
            ) : null}
            {deltas.length > 0 ? (
              <ul className="bench-history-list mono">
                {deltas.map((d, i) => (
                  <li key={`${d.field}-${i}`}>
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
            ) : (
              <p className="mono bench-history-empty">No snapshot deltas for this benchmark.</p>
            )}
            <p className="bench-history-link">
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
