#!/usr/bin/env python3
"""Patch bench/pillar pages for pillar-drilldown-charts (run from repo root)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "dashboard-next"

BENCH = ROOT / "app/bench/[id]/page.tsx"
PILLAR = ROOT / "app/pillar/[id]/page.tsx"


def patch_bench() -> None:
    text = BENCH.read_text()
    if "BenchFacetComposition" in text:
        print("bench: already patched")
        return
    text = text.replace(
        "import { HonestyCallout } from \"@/components/bench/honesty-callout\";\n"
        "import { LangsTable } from \"@/components/bench/langs-table\";\n"
        "import { PerfRelativeBars } from \"@/components/bench/perf-relative-bars\";\n"
        "import { OsTable } from \"@/components/bench/os-table\";\n"
        "import { PerfNotClaimable } from \"@/components/bench/perf-not-claimable\";\n"
        "import { ValidityPanel } from \"@/components/bench/validity-panel\";\n",
        "import { BenchFacetComposition } from \"@/components/bench/bench-facet-composition\";\n",
    )
    text = text.replace(
        "        <HonestyCallout variant={row.variant} />\n"
        "        <PerfNotClaimable row={row} />\n"
        "        <ValidityPanel row={row} />\n\n"
        "        <dl",
        "        <dl",
        1,
    )
    block = (
        "        <h3 style={{ fontSize: \"1rem\", marginTop: \"1.5rem\", color: \"var(--text)\" }}>\n"
        "          Performance vs best competitor\n"
        "        </h3>\n"
        "        <PerfRelativeBars\n"
        "          series={series}\n"
        "          sotaLang={row.sota_lang}\n"
        "          lowerIsBetter={lowerIsBetter}\n"
        "          claimable={perfClaimable}\n"
        "        />\n\n"
        "        <h3 style={{ fontSize: \"1rem\", marginTop: \"1.5rem\", color: \"var(--text)\" }}>\n"
        "          Absolute measurements\n"
        "        </h3>\n"
        "        <LangsTable series={series} metric={row.metric} />\n"
        "        <OsTable row={row} series={series} />\n\n"
        "        {deltas"
    )
    repl = (
        "        <BenchFacetComposition\n"
        "          row={row}\n"
        "          series={series}\n"
        "          lowerIsBetter={lowerIsBetter}\n"
        "          perfClaimable={perfClaimable}\n"
        "        />\n\n"
        "        {deltas"
    )
    if block not in text:
        raise SystemExit("bench: expected PerfRelativeBars block not found")
    text = text.replace(block, repl, 1)
    text = text.replace(
        "          <dt>Validity</dt>\n"
        "          <dd>\n"
        "            {row.validity_status ? (\n"
        "              <ValidityBadge\n"
        "                status={row.validity_status}\n"
        "                source={row.validity_source}\n"
        "              />\n"
        "            ) : (\n"
        "              \"—\"\n"
        "            )}\n"
        "          </dd>\n",
        "",
        1,
    )
    text = text.replace(
        '          <Link href="/">← Overview</Link>\n        </p>',
        '          <Link href="/">← Overview</Link>\n'
        "          {row.pillar ? (\n"
        "            <>\n"
        '              {" · "}\n'
        "              <Link href={`/pillar/${row.pillar}/`}>Pillar {row.pillar}</Link>\n"
        "            </>\n"
        "          ) : null}\n"
        "        </p>",
        1,
    )
    BENCH.write_text(text)
    print("bench: patched")


def patch_pillar() -> None:
    if "PillarSummaryStrip" in PILLAR.read_text():
        print("pillar: already patched")
        return
    PILLAR.write_text("""import Link from "next/link";
import { notFound } from "next/navigation";
import { BenchmarkRelativeBars } from "@/components/charts/benchmark-relative-bars";
import { BenchRowList } from "@/components/drilldown/bench-row-list";
import { PillarSummaryStrip } from "@/components/pillar/pillar-summary-strip";
import { getPillar, PILLAR_IDS } from "@/lib/pillars";
import {
  benchmarkRelativeItems,
  bottomRelativeItems,
  measuredPerfRows,
  statusCountsForRows,
  topRelativeItems,
} from "@/lib/pillar-charts";
import { loadSummary } from "@/lib/summary";
import { isPerfClaimable, pillarPerfCounts } from "@/lib/validity";

type PageProps = {
  params: Promise<{ id: string }>;
};

const TOP_N = 12;
const BOTTOM_N = 6;

export function generateStaticParams() {
  return PILLAR_IDS.map((id) => ({ id }));
}

export default async function PillarPage({ params }: PageProps) {
  const { id } = await params;
  const pillar = getPillar(id);
  if (!pillar) notFound();

  const summary = loadSummary();
  const rows = summary.rows.filter((r) => r.pillar === id);
  const statusCounts = statusCountsForRows(rows);
  const perfCounts = pillarPerfCounts(summary.rows, id);
  const measured = measuredPerfRows(rows);
  const relativeItems = benchmarkRelativeItems(rows, isPerfClaimable);
  const topItems = topRelativeItems(relativeItems, TOP_N);
  const bottomItems = bottomRelativeItems(relativeItems, BOTTOM_N);

  return (
    <main>
      <section className="placeholder">
        <h2>{pillar.label}</h2>
        <p>{pillar.description}</p>
        <p className="mono" style={{ marginTop: "0.75rem", fontSize: "0.85rem", color: "var(--muted)" }}>
          Li is never SOTA — bars use <code>ratio_vs_sota</code> (1.0 = best competitor). Green
          perf requires validity pass.
        </p>

        <PillarSummaryStrip
          statusCounts={statusCounts}
          perfCounts={perfCounts}
          measuredCount={measured.length}
          totalRows={rows.length}
        />

        {relativeItems.length > 0 ? (
          <>
            <section aria-label="Top measured benches vs SOTA" style={{ marginTop: "1.5rem" }}>
              <h3 style={{ fontSize: "1rem", margin: 0, color: "var(--text)" }}>
                Measured performance (top {Math.min(TOP_N, relativeItems.length)} vs SOTA)
              </h3>
              <BenchmarkRelativeBars
                items={topItems}
                title={`${pillar.label} — highest Li relative speed`}
              />
            </section>

            {bottomItems.length > 0 &&
            bottomItems[0].benchmark !== topItems[0]?.benchmark ? (
              <section aria-label="Bottom measured benches vs SOTA" style={{ marginTop: "1.5rem" }}>
                <h3 style={{ fontSize: "1rem", margin: 0, color: "var(--text)" }}>
                  Furthest from best competitor (bottom {bottomItems.length})
                </h3>
                <BenchmarkRelativeBars
                  items={bottomItems}
                  title={`${pillar.label} — lowest Li relative speed`}
                />
              </section>
            ) : null}
          </>
        ) : (
          <p className="mono" style={{ marginTop: "1.25rem", color: "var(--muted)" }}>
            No measured <code>ratio_vs_sota</code> rows in this pillar yet — charts appear after
            harness CSV ingest.
          </p>
        )}

        <h3 style={{ fontSize: "1rem", marginTop: "1.75rem", color: "var(--text)" }}>
          All benchmarks
        </h3>
        <BenchRowList
          rows={rows}
          emptyMessage={`No rows tagged pillar="${id}" in summary.json.`}
        />

        <p style={{ marginTop: "1.25rem" }}>
          <Link href="/">← Overview</Link>
          {" · "}
          <Link href="/matrix/">Facet matrix</Link>
        </p>
      </section>
    </main>
  );
}
""")
    print("pillar: patched")


def main() -> None:
    patch_bench()
    patch_pillar()


if __name__ == "__main__":
    main()
