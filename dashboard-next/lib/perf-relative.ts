import type { LangPoint } from "@/lib/summary";

/** Relative speed vs best competitor — SOTA = 1.0, higher is better. */
export function relativePerfVsSota(
  value: number,
  sotaValue: number,
  lowerIsBetter: boolean,
): number | null {
  if (value <= 0 || sotaValue <= 0) return null;
  return lowerIsBetter ? sotaValue / value : value / sotaValue;
}

export type RelativePerfBar = {
  lang: string;
  variant?: string;
  relative: number;
  isSota: boolean;
};

export function buildRelativePerfBars(
  series: LangPoint[],
  sotaLang: string | null | undefined,
  lowerIsBetter: boolean,
): RelativePerfBar[] {
  if (!sotaLang || series.length === 0) return [];
  const sotaPoint = series.find((p) => p.lang === sotaLang);
  const sotaValue = sotaPoint?.value;
  if (sotaValue == null || sotaValue <= 0) return [];

  const bars: RelativePerfBar[] = [];
  for (const pt of series) {
    const relative =
      pt.relative_perf ??
      relativePerfVsSota(pt.value, sotaValue, lowerIsBetter);
    if (relative == null) continue;
    bars.push({
      lang: pt.lang,
      variant: pt.variant,
      relative: pt.lang === sotaLang ? 1 : relative,
      isSota: pt.lang === sotaLang,
    });
  }

  return bars.sort((a, b) => b.relative - a.relative);
}

export function formatRelativePerf(value: number): string {
  return value.toFixed(3);
}
