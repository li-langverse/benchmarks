import Link from "next/link";
import type { LangPoint, SummaryRow } from "@/lib/summary";
import { HonestyCallout } from "@/components/bench/honesty-callout";
import { LangsTable } from "@/components/bench/langs-table";
import { PerfRelativeBars } from "@/components/bench/perf-relative-bars";
import { OsTable } from "@/components/bench/os-table";
import { PerfNotClaimable } from "@/components/bench/perf-not-claimable";
import { ValidityPanel } from "@/components/bench/validity-panel";
import { MemoryFacet } from "@/components/bench/memory-facet";
import { SecurityFacet } from "@/components/bench/security-facet";
import { FacetMatrixSnippet } from "@/components/bench/facet-matrix-snippet";

const FACET_ANCHORS = [
  { id: "validity", label: "① Validity" },
  { id: "perf", label: "② Perf" },
  { id: "os", label: "③ OS" },
  { id: "memory", label: "④ Memory" },
  { id: "security", label: "⑤ Security" },
] as const;

type BenchFacetCompositionProps = {
  row: SummaryRow;
  series: LangPoint[];
  lowerIsBetter: boolean;
  perfClaimable: boolean;
};

export function BenchFacetComposition({
  row,
  series,
  lowerIsBetter,
  perfClaimable,
}: BenchFacetCompositionProps) {
  return (
    <>
      <nav
        className="facet-rail mono"
        aria-label="Facet panels"
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "0.5rem 1rem",
          marginTop: "1rem",
          padding: "0.5rem 0",
          borderBottom: "1px solid var(--border)",
          fontSize: "0.85rem",
        }}
      >
        {FACET_ANCHORS.map(({ id, label }) => (
          <a key={id} href={`#facet-${id}`} style={{ color: "var(--accent)" }}>
            {label}
          </a>
        ))}
        <Link href="/matrix/" style={{ marginLeft: "auto", color: "var(--muted)" }}>
          Full matrix →
        </Link>
      </nav>

      <p className="mono tier-context" style={{ marginTop: "0.75rem", fontSize: "0.85rem", color: "var(--muted)" }}>
        Tier {row.tier}
        {row.category ? ` · ${row.category}` : ""}
        {row.pillar ? (
          <>
            {" "}
            · pillar <Link href={`/pillar/${row.pillar}/`}>{row.pillar}</Link>
          </>
        ) : null}
      </p>

      <HonestyCallout variant={row.variant} />
      <PerfNotClaimable row={row} />

      <section id="facet-validity" style={{ scrollMarginTop: "4rem" }}>
        <ValidityPanel row={row} />
      </section>

      <section id="facet-perf" className="facet-panel" aria-label="Performance facet" style={{ scrollMarginTop: "4rem" }}>
        <h3 style={{ fontSize: "1rem", margin: "1.5rem 0 0.5rem", color: "var(--text)" }}>
          ② Performance vs best competitor
        </h3>
        <PerfRelativeBars
          series={series}
          sotaLang={row.sota_lang}
          lowerIsBetter={lowerIsBetter}
          claimable={perfClaimable}
        />
        <FacetMatrixSnippet row={row} />
        <h4 style={{ fontSize: "0.95rem", margin: "1.25rem 0 0.5rem", color: "var(--text)" }}>
          Absolute measurements
        </h4>
        <LangsTable series={series} metric={row.metric} />
      </section>

      <section id="facet-os" style={{ scrollMarginTop: "4rem" }}>
        <h3 style={{ fontSize: "1rem", margin: "1.5rem 0 0.5rem", color: "var(--text)" }}>
          ③ OS / hosts
        </h3>
        <OsTable row={row} series={series} />
      </section>

      <section id="facet-memory" style={{ scrollMarginTop: "4rem" }}>
        <MemoryFacet row={row} />
      </section>

      <section id="facet-security" style={{ scrollMarginTop: "4rem" }}>
        <SecurityFacet row={row} />
      </section>
    </>
  );
}
