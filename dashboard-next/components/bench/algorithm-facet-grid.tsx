/**
 * Algorithm × Facet matrix — types only (WP2 implementation).
 * IA: docs/dashboard/diagram-layout.md
 */

import type { LangPoint, SummaryRow, ValidityStatus } from "@/lib/summary";

/** Fixed column order for overview matrix and detail panel sequence. */
export const FACET_ORDER = [
  "validity",
  "perf",
  "os",
  "memory",
  "security",
] as const;

export type FacetId = (typeof FACET_ORDER)[number];

export type FacetCellTone = "green" | "yellow" | "red" | "unknown" | "neutral";

/** One matrix cell — render layer maps to badges / mono / stub. */
export type FacetCell = {
  facet: FacetId;
  label: string;
  detail?: string;
  tone: FacetCellTone;
  claimable: boolean;
  href?: string;
};

export type AlgorithmFacetRow = {
  benchmark: string;
  tier: number;
  cells: Record<FacetId, FacetCell>;
};

export type AlgorithmFacetGridProps = {
  rows: AlgorithmFacetRow[];
  /** Virtualize when row count exceeds this (default 80). */
  virtualizeAbove?: number;
  onRowSelect?: (benchmark: string) => void;
};

/** Build facet cells from a summary row (ingest-shaped). */
export function facetCellsFromSummaryRow(row: SummaryRow): Record<FacetId, FacetCell> {
  const claimable = row.validity_status === "pass";
  const perfLabel =
    row.ratio_vs_sota != null && row.sota_lang
      ? `${row.ratio_vs_sota.toFixed(3)} vs ${row.sota_lang} (rel.)`
      : row.ratio_vs_cpp != null
        ? `${row.ratio_vs_cpp} vs ${row.compare_oracle ?? "oracle"}`
        : "—";

  return {
    validity: {
      facet: "validity",
      label: row.validity_status ?? "unknown",
      detail: row.validity_source,
      tone:
        row.validity_status === "pass"
          ? "green"
          : row.validity_status === "fail"
            ? "red"
            : "unknown",
      claimable,
    },
    perf: {
      facet: "perf",
      label: perfLabel,
      detail: claimable ? row.status : "not claimable",
      tone: claimable ? (row.status as FacetCellTone) : "unknown",
      claimable,
    },
    os: {
      facet: "os",
      label: row.os ?? "unknown",
      detail: langOsSummary(row.langs),
      tone: "neutral",
      claimable: true,
    },
    memory: {
      facet: "memory",
      label: "—",
      detail: "peak_rss ingest planned",
      tone: "neutral",
      claimable: false,
    },
    security: {
      facet: "security",
      label: row.category === "security" ? row.status : "gates",
      detail: row.category === "security" ? row.metric : undefined,
      tone: row.category === "security" ? (row.status as FacetCellTone) : "neutral",
      claimable: true,
      href: row.category === "security" ? undefined : "/matrix#security",
    },
  };
}

function langOsSummary(langs: LangPoint[] | undefined): string | undefined {
  if (!langs?.length) return undefined;
  const osSet = new Set(langs.map((p) => p.os ?? "unknown"));
  return osSet.size > 1 ? [...osSet].join(", ") : undefined;
}

/** Placeholder export — implement virtualized table in WP2. */
export function AlgorithmFacetGrid(_props: AlgorithmFacetGridProps): null {
  return null;
}
