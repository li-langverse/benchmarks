import "./style.css";

type Summary = {
  generated_at: string;
  source_csv: string;
  tier_counts: Record<string, { green: number; yellow: number; red: number; unknown: number }>;
  rows: Row[];
};

type Row = {
  benchmark: string;
  repo: string;
  tier: number;
  metric: string;
  li_value: number | null;
  cpp_value: number | null;
  ratio_vs_cpp: number | null;
  unit: string | null;
  variant?: string | null;
  status: string;
  ph_ids: string[];
  path: string;
  threshold_ratio_cpp: number;
};

async function loadSummary(): Promise<Summary> {
  const res = await fetch("/latest/summary.json");
  if (!res.ok) throw new Error(`Failed to load summary: ${res.status}`);
  return res.json();
}

function tierStrip(counts: Summary["tier_counts"]): string {
  const tiers = ["0", "1", "2", "5"];
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

function fmt(n: number | null, unit: string | null): string {
  if (n == null) return "—";
  return `${n.toFixed(4)}${unit ? " " + unit : ""}`;
}

function renderTable(rows: Row[]): string {
  return rows
    .map(
      (r) => `
    <tr data-tier="${r.tier}" data-repo="${r.repo}" data-status="${r.status}" data-variant="${r.variant ?? ""}">
      <td><strong>${r.benchmark}</strong></td>
      <td>${r.repo}</td>
      <td class="mono">${r.tier}</td>
      <td>${r.metric}</td>
      <td class="mono">${fmt(r.li_value, r.unit)}</td>
      <td class="mono">${fmt(r.cpp_value, r.unit)}</td>
      <td class="mono">${r.ratio_vs_cpp != null ? r.ratio_vs_cpp.toFixed(3) + "×" : "—"}</td>
      <td>${badge(r.status)}</td>
      <td class="mono">${(r.ph_ids ?? []).join(", ")}</td>
      <td class="mono"><a href="https://github.com/li-langverse/${r.repo}/tree/main/${r.path}" target="_blank" rel="noopener">source</a></td>
    </tr>`
    )
    .join("");
}

function applyFilters(root: HTMLElement) {
  const tier = (root.querySelector("#f-tier") as HTMLSelectElement).value;
  const repo = (root.querySelector("#f-repo") as HTMLSelectElement).value;
  const failing = (root.querySelector("#f-fail") as HTMLInputElement).checked;
  root.querySelectorAll("tbody tr").forEach((tr) => {
    const el = tr as HTMLTableRowElement;
    let show = true;
    if (tier && el.dataset.tier !== tier) show = false;
    if (repo && el.dataset.repo !== repo) show = false;
    if (failing && el.dataset.status === "green") show = false;
    el.style.display = show ? "" : "none";
  });
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

    app.innerHTML = `
      <header>
        <h1>Li benchmarks</h1>
        <p>Updated ${new Date(data.generated_at).toLocaleString()} · <a href="https://github.com/li-langverse/benchmarks">repo</a></p>
      </header>
      <main>
        ${alert}
        <section class="tier-strip">${tierStrip(data.tier_counts)}</section>
        <section class="filters">
          <label>Tier <select id="f-tier"><option value="">all</option><option>0</option><option>1</option><option>2</option><option>5</option></select></label>
          <label>Repo <select id="f-repo"><option value="">all</option><option>lic</option><option>lis</option></select></label>
          <label><input type="checkbox" id="f-fail" /> Failing / warn only</label>
        </section>
        <table>
          <thead>
            <tr>
              <th>Benchmark</th><th>Repo</th><th>Tier</th><th>Metric</th>
              <th>Li</th><th>Ref (cpp)</th><th>Ratio</th><th>Status</th><th>PH</th><th>Path</th>
            </tr>
          </thead>
          <tbody>${renderTable(data.rows)}</tbody>
        </table>
      </main>`;

    ["#f-tier", "#f-repo", "#f-fail"].forEach((sel) => {
      app.querySelector(sel)?.addEventListener("change", () => applyFilters(app));
    });
  } catch (e) {
    app.innerHTML = `<main><p class="alert">Could not load dashboard: ${(e as Error).message}</p></main>`;
  }
}

main();
