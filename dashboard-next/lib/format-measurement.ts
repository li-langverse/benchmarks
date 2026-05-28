/** Format harness mean ± sample stddev (value column in CSV is mean). */

export function formatMeanStd(
  value: number | null | undefined,
  stddev?: number | null,
  unit?: string | null,
  sampleRuns?: number | null,
): string {
  if (value == null || Number.isNaN(value)) return "—";
  const u = unit ? ` ${unit}` : "";
  const core =
    stddev != null && stddev > 0
      ? `${value} ± ${stddev}${u}`
      : `${value}${u}`;
  const n =
    sampleRuns != null && sampleRuns > 0 ? ` (n=${sampleRuns})` : "";
  return core + n;
}
