import type { LangPoint, Summary, SummaryRow } from "@/lib/summary";

/** Lang series from row.langs, or chart series in summary.categories. */
function chartIdsForRow(row: SummaryRow): string[] {
  const ids = [row.benchmark];
  if (row.os && row.os !== "unknown") {
    ids.unshift(`${row.benchmark}@${row.os}`);
  }
  return ids;
}

export function getLangSeries(summary: Summary, row: SummaryRow): LangPoint[] {
  if (row.langs && row.langs.length > 0) return row.langs;
  for (const block of Object.values(summary.categories)) {
    for (const cid of chartIdsForRow(row)) {
      const chart = block.charts.find((c) => c.id === cid);
      if (chart?.series?.length) return chart.series;
    }
  }
  return [];
}
