import "./style.css";
import { renderCategorySection, type ChartSpec } from "./charts";

type Hardware = {
  reference_lang: string;
  cpu_models: string[];
  cpu_model_primary: string;
  build_flags: string[];
  git_shas: string[];
  host_uname: string;
  host_platform: string;
  display_note: string;
};

type Summary = {
  generated_at: string;
  hardware?: Hardware;
  sources: Record<string, string>;
  tier_counts: Record<string, { green: number; yellow: number; red: number; unknown: number }>;
  categories: Record<string, { label: string; charts: ChartSpec[] }>;
  rows: Row[];
};

type Row = {
  benchmark: string;
  repo: string;
  tier: number;
  category?: string;
  metric: string;
  ratio_vs_cpp: number | null;
  reference_lang?: string;
  unit: string | null;
  variant?: string | null;
  status: string;
  ph_ids: string[];
  path: string;
  threshold_ratio_cpp: number;
};

const CATEGORY_NAV = ["micro", "physics", "http", "tooling", "correctness"];

async function loadSummary(): Promise<Summary> {
  const base = import.meta.env.BASE_URL.replace(/\/?$/, "/");
  const res = await fetch(`${base}latest/summary.json`);
  if (!res.ok) throw new Error(`Failed to load summary: ${res.status}`);
  return res.json();
}

function tierStrip(counts: Summary["tier_counts"]): string {
  const tiers = ["0", "1", "2", "3", "5"];
  return tiers
    .map((t) => {
      const c = counts[t] ?? { green: 0, yellow: 0, red: 0, unknown: 0 };
      return `
        <div class="tier-card">
          <h3>Tier ${t}</h3>
          <div class="counts">
            <span class="g">${c.green} ok</span>
            <span class="y">${c.yellow} warn</span>
            <span class="r">${c.red} fail</span>
            <span class="u">${c.unknown} ?</span>
          </div>
        </div>`;
    })
    .join("");
}

function badge(status: string): string {
  return `<span class="badge ${status}">${status}</span>`;
}

function fmtRatio(n: number | null, ref: string): string {
  if (n == null) return "—";
  return `${n.toFixed(3)}× vs ${ref}`;
}

function hardwareBanner(hw: Hardware | undefined): string {
  if (!hw) return "";
  const cpus =
    hw.cpu_models.length > 0 ? hw.cpu_models.join(", ") : hw.cpu_model_primary;
  const flags = hw.build_flags.length ? hw.build_flags.join(" · ") : "—";
  const shas = hw.git_shas.length ? hw.git_shas.join(", ") : "—";
  return `
    <section class="hardware-banner" aria-label="Measurement hardware">
      <h2>Hardware &amp; reference</h2>
      <p><strong>Reference:</strong> <code>${hw.reference_lang}</code> = 1.00× · all bars and table ratios are relative (no absolute wall times).</p>
      <ul>
        <li><strong>CPU:</strong> ${cpus}</li>
        <li><strong>Host:</strong> ${hw.host_uname || hw.host_platform}</li>
        <li><strong>Build flags:</strong> ${flags}</li>
        <li><strong>git sha(s):</strong> ${shas}</li>
      </ul>
      <p class="hw-note">${hw.display_note}</p>
    </section>`;
}

function renderTable(rows: Row[]): string {
  return rows
    .map((r) => {
      const ref = r.reference_lang ?? "cpp";
      return `
    <tr data-tier="${r.tier}" data-repo="${r.repo}" data-status="${r.status}" data-category="${r.category ?? ""}">
      <td><strong>${r.benchmark}</strong></td>
      <td>${r.category ?? "—"}</td>
      <td>${r.repo}</td>
      <td class="mono">${r.tier}</td>
      <td>${r.metric}</td>
      <td class="mono">${fmtRatio(r.ratio_vs_cpp, ref)}</td>
      <td>${badge(r.status)}</td>
      <td class="mono">${(r.ph_ids ?? []).join(", ")}</td>
      <td class="mono"><a href="https://github.com/li-langverse/${r.repo}/tree/main/${r.path}" target="_blank" rel="noopener">source</a></td>
    </tr>`;
    })
    .join("");
}

function applyFilters(root: HTMLElement) {
  const tier = (root.querySelector("#f-tier") as HTMLSelectElement).value;
  const repo = (root.querySelector("#f-repo") as HTMLSelectElement).value;
  const cat = (root.querySelector("#f-category") as HTMLSelectElement).value;
  const failing = (root.querySelector("#f-fail") as HTMLInputElement).checked;
  root.querySelectorAll("tbody tr").forEach((tr) => {
    const el = tr as HTMLTableRowElement;
    let show = true;
    if (tier && el.dataset.tier !== tier) show = false;
    if (repo && el.dataset.repo !== repo) show = false;
    if (cat && el.dataset.category !== cat) show = false;
    if (failing && el.dataset.status === "green") show = false;
    el.style.display = show ? "" : "none";
  });
}

function categoryNav(categories: Summary["categories"]): string {
  return CATEGORY_NAV.filter((k) => categories[k])
    .map(
      (k) =>
        `<a class="cat-pill" href="#cat-${k}">${categories[k].label}</a>`
    )
    .join("");
}

function legend(): string {
  const langs = [
    "li",
    "cpp",
    "rust",
    "julia",
    "nginx",
    "apache",
    "lighttpd",
    "node",
    "bun",
    "harness",
  ];
  return `
    <div class="lang-legend">
      <p class="legend-title">Bar height = ratio vs reference (<code>cpp</code> or catalog oracle); reference lang is always 1.00×</p>
      ${langs
        .map(
          (l) =>
            `<span class="legend-item"><span class="legend-swatch" data-lang="${l}"></span>${l}</span>`
        )
        .join("")}
    </div>`;
}

async function main() {
  const app = document.querySelector("#app")!;
  try {
    const data = await loadSummary();
    const reds = data.rows.filter((r) => r.status === "red");
    const alert =
      reds.length > 0
        ? `<div class="alert"><strong>${reds.length} regression(s):</strong> ${reds.map((r) => r.benchmark).join(", ")}</div>`
        : "";

    const chartSections = CATEGORY_NAV.map((k) => {
      const block = data.categories[k];
      if (!block) return "";
      return renderCategorySection(k, block.label, block.charts);
    }).join("");

    app.innerHTML = `
      <header>
        <h1>Li benchmarks</h1>
        <p>Updated ${new Date(data.generated_at).toLocaleString()} · relative to <strong>cpp</strong> (or catalog oracle) · <a href="https://github.com/li-langverse/benchmarks">repo</a></p>
      </header>
      <main>
        ${alert}
        ${hardwareBanner(data.hardware)}
        <section class="tier-strip">${tierStrip(data.tier_counts)}</section>
        <nav class="category-nav">${categoryNav(data.categories)}</nav>
        ${legend()}
        ${chartSections}
        <section class="table-section">
          <h2>All benchmarks</h2>
          <div class="filters">
            <label>Category <select id="f-category"><option value="">all</option><option>micro</option><option>physics</option><option>http</option><option>tooling</option><option>correctness</option></select></label>
            <label>Tier <select id="f-tier"><option value="">all</option><option>0</option><option>1</option><option>2</option><option>3</option><option>5</option></select></label>
            <label>Repo <select id="f-repo"><option value="">all</option><option>lic</option><option>lis</option><option>lip</option><option>lit</option></select></label>
            <label><input type="checkbox" id="f-fail" /> Failing / warn only</label>
          </div>
          <table>
            <thead>
              <tr>
                <th>Benchmark</th><th>Category</th><th>Repo</th><th>Tier</th><th>Metric</th>
                <th>Ratio</th><th>Status</th><th>PH</th><th>Path</th>
              </tr>
            </thead>
            <tbody>${renderTable(data.rows)}</tbody>
          </table>
        </section>
      </main>`;

    ["#f-tier", "#f-repo", "#f-category", "#f-fail"].forEach((sel) => {
      app.querySelector(sel)?.addEventListener("change", () => applyFilters(app));
    });
  } catch (e) {
    app.innerHTML = `<main><p class="alert">Could not load dashboard: ${(e as Error).message}</p></main>`;
  }
}

main();
