/** CSS bar charts for multi-language benchmark comparison. */

export type LangPoint = {
  lang: string;
  value: number;
  unit: string;
  variant?: string;
  label?: string;
  passed?: boolean;
};

export type ChartSpec = {
  id: string;
  title: string;
  metric: string;
  unit: string;
  lower_is_better: boolean;
  reference_lang: string;
  series: LangPoint[];
  grouped?: boolean;
  repo: string;
  path: string;
  status: string;
  ratio_vs_reference?: number | null;
  pending?: boolean;
};

const LANG_COLORS: Record<string, string> = {
  li: "var(--lang-li)",
  cpp: "var(--lang-cpp)",
  rust: "var(--lang-rust)",
  julia: "var(--lang-julia)",
  nginx: "var(--lang-nginx)",
  apache: "var(--lang-apache)",
  lighttpd: "var(--lang-lighttpd)",
  node: "var(--lang-node)",
  bun: "var(--lang-bun)",
  harness: "var(--lang-harness)",
  go: "var(--lang-go)",
  python: "var(--lang-python)",
};

function barLangLabel(p: LangPoint): string {
  if (p.variant && p.lang === "li") return `${p.lang}/${p.variant}`;
  if (p.variant && p.variant !== "ci" && p.variant !== "release") {
    return `${p.lang}/${p.variant}`;
  }
  return p.lang;
}

function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
}

function formatValue(v: number, unit: string): string {
  if (unit === "pass") return v >= 1 ? "pass" : "fail";
  if (unit === "bool") return v >= 1 ? "OK" : "—";
  if (unit === "×") return `${v.toFixed(2)}×`;
  if (v >= 1000 || (v > 0 && v < 0.01)) return v.toExponential(2);
  return v.toFixed(4);
}

function groupSeries(series: LangPoint[]): { label: string; points: LangPoint[] }[] {
  const groups = new Map<string, LangPoint[]>();
  for (const p of series) {
    const key = p.label ?? p.lang;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key)!.push(p);
  }
  return [...groups.entries()].map(([label, points]) => ({ label, points }));
}

export function renderBarChart(chart: ChartSpec): string {
  if (chart.pending || chart.series.length === 0) {
    return `
      <article class="chart-card" data-status="${chart.status}">
        <header class="chart-header">
          <h3>${esc(chart.title)}</h3>
          <span class="badge unknown">pending</span>
        </header>
        <p class="chart-empty">No timing data yet — wire CI for ${esc(chart.repo)}.</p>
      </article>`;
  }

  const groups = chart.grouped
    ? groupSeries(chart.series)
    : [{ label: "", points: chart.series }];
  const allValues = chart.series.map((s) => s.value).filter((v) => v > 0);
  const maxVal = Math.max(...allValues, 1.0);

  const groupHtml = groups
    .map((g) => {
      const bars = g.points
        .map((p) => {
          const h = Math.max(4, (p.value / maxVal) * 100);
          const color = LANG_COLORS[p.lang] ?? "var(--muted)";
          const isRef = p.lang === chart.reference_lang;
          return `
            <div class="bar-col" title="${esc(p.lang)}: ${formatValue(p.value, p.unit)} vs ${esc(chart.reference_lang)}">
              
              
              <div class="bar-value">${formatValue(p.value, p.unit)}</div>
              <div class="bar-track">
                <div class="bar-fill${isRef ? " ref" : ""}" style="height:${h}%;background:${color}"></div>
              </div>
              <div class="bar-label">${esc(barLangLabel(p))}</div>
            </div>`;
        })
        .join("");
      return `
        <div class="bar-group">
          ${g.label ? `<div class="bar-group-title">${esc(g.label)}</div>` : ""}
          <div class="bar-row">${bars}</div>
        </div>`;
    })
    .join("");

  const ratio =
    chart.ratio_vs_reference != null
      ? `<span class="mono chart-ratio">${chart.ratio_vs_reference.toFixed(2)}× vs ${esc(chart.reference_lang)}</span>`
      : "";

  return `
    <article class="chart-card" data-status="${chart.status}" data-id="${esc(chart.id)}">
      <header class="chart-header">
        <h3>${esc(chart.title)}</h3>
        <span class="badge ${chart.status}">${chart.status}</span>
      </header>
      <p class="chart-meta">
        ${esc(chart.metric)} · ratio (${esc(chart.unit || "×")}) ·
        <a href="https://github.com/li-langverse/${esc(chart.repo)}/tree/main/${esc(chart.path)}" target="_blank" rel="noopener">${esc(chart.repo)}</a>
        ${ratio}
      </p>
      <div class="chart-bars">${groupHtml}</div>
    </article>`;
}

export function renderCategorySection(
  catKey: string,
  label: string,
  charts: ChartSpec[]
): string {
  if (!charts.length) return "";
  const cards = charts.map(renderBarChart).join("");
  return `
    <section class="chart-section" id="cat-${esc(catKey)}">
      <h2>${esc(label)}</h2>
      <div class="chart-grid">${cards}</div>
    </section>`;
}
