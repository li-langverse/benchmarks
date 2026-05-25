import type { LangPoint, Summary, SummaryRow } from "@/lib/summary";

/** Lang series from row.langs, or chart series in summary.categories. */
export function getLangSeries(summary: Summary, row: SummaryRow): LangPoint[] {
  if (row.langs && row.langs.length > 0) return row.langs;
  for (const block of Object.values(summary.categories)) {
    const chart = block.charts.find((c) => c.id === row.benchmark);
    if (chart?.series?.length) return chart.series;
  }
  return [];
}
