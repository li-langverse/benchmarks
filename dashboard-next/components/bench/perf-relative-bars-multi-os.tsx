import type { LangPoint } from "@/lib/summary";
import { buildRelativePerfBars, formatRelativePerf } from "@/lib/perf-relative";

type PerfRelativeBarsMultiOsProps = {
  seriesByOs: Record<string, LangPoint[]>;
  sotaLangByOs: Record<string, string | null | undefined>;
  lowerIsBetter: boolean;
  claimable: boolean;
  pending?: boolean;
  osOrder?: string[];
};

type BarCell = {
  relative: number;
  isSota: boolean;
};

function keyFor(pt: { lang: string; variant?: string }) {
  return `${pt.lang}::${pt.variant ?? ""}`;
}

export function PerfRelativeBarsMultiOs({
  seriesByOs,
  sotaLangByOs,
  lowerIsBetter,
  claimable,
  pending = false,
  osOrder = ["linux", "macos", "windows"],
}: PerfRelativeBarsMultiOsProps) {
  if (pending) {
    return (
      <figure className="perf-relative-chart perf-relative-pending">
        <figcaption className="mono perf-relative-caption">
          Not measured — this catalog row has no wall-clock data in the current ingest.
          Bars below are placeholders only.
        </figcaption>
        <div className="perf-bar-fill-pending" role="img" aria-label="Performance not measured" />
      </figure>
    );
  }

  const oss = osOrder.filter((os) => (seriesByOs[os]?.length ?? 0) > 0);
  if (oss.length === 0) {
    return (
      <p className="mono" style={{ color: "var(--muted)", marginTop: "1rem" }}>
        No relative performance chart — missing competitor series.
      </p>
    );
  }

  const table = new Map<string, { lang: string; variant?: string; byOs: Record<string, BarCell> }>();
  let globalMax = 1;

  for (const os of oss) {
    const series = seriesByOs[os] ?? [];
    const sotaLang = sotaLangByOs[os];
    const bars = buildRelativePerfBars(series, sotaLang, lowerIsBetter);
    for (const b of bars) {
      globalMax = Math.max(globalMax, b.relative);
      const k = keyFor(b);
      const existing = table.get(k) ?? { lang: b.lang, variant: b.variant, byOs: {} };
      existing.byOs[os] = { relative: b.relative, isSota: b.isSota };
      table.set(k, existing);
    }
  }

  const rows = [...table.values()].sort((a, b) => {
    const aBest = Math.max(...Object.values(a.byOs).map((v) => v.relative), 0);
    const bBest = Math.max(...Object.values(b.byOs).map((v) => v.relative), 0);
    return bBest - aBest;
  });

  return (
    <figure className="perf-relative-chart" style={{ marginTop: "1.25rem" }}>
      <figcaption
        className="mono"
        style={{ fontSize: "0.85rem", color: "var(--muted)", marginBottom: "0.75rem" }}
      >
        Relative speed vs best competitor — SOTA = 1.0 per OS, higher is better.
        {!claimable ? (
          <span style={{ display: "block", marginTop: "0.35rem", color: "var(--yellow)" }}>
            Validity gate not passed — bars are informational only.
          </span>
        ) : null}
      </figcaption>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: `7rem repeat(${oss.length}, 1fr) 4.5rem`,
          gap: "0.5rem 0.75rem",
          alignItems: "center",
        }}
        role="img"
        aria-label="Relative performance by OS"
      >
        <div />
        {oss.map((os) => (
          <div key={os} className="mono" style={{ color: "var(--muted)", fontSize: "0.8rem" }}>
            {os}
          </div>
        ))}
        <div className="mono" style={{ color: "var(--muted)", fontSize: "0.8rem", textAlign: "right" }}>
          best
        </div>

        {rows.map((r) => {
          const label = r.variant ? `${r.lang} (${r.variant})` : r.lang;
          const best = Math.max(...Object.values(r.byOs).map((v) => v.relative), 0);
          return (
            <>
              <span
                key={`${label}-chip`}
                className={`lang-chip lang-${r.lang}`}
                style={{ justifySelf: "start", opacity: claimable ? 1 : 0.65 }}
              >
                {label}
              </span>
              {oss.map((os) => {
                const cell = r.byOs[os];
                const rel = cell?.relative;
                const widthPct = rel != null ? Math.min(100, (rel / globalMax) * 100) : 0;
                const isSota = cell?.isSota ?? false;
                return (
                  <div
                    key={`${label}-${os}`}
                    style={{
                      height: "1.25rem",
                      background: "color-mix(in srgb, var(--border) 60%, transparent)",
                      borderRadius: "4px",
                      overflow: "hidden",
                      opacity: claimable || isSota ? 1 : 0.65,
                    }}
                    title={rel != null ? `${os}: ${formatRelativePerf(rel)}` : `${os}: —`}
                  >
                    {rel != null ? (
                      <div
                        role="presentation"
                        className={
                          isSota
                            ? "perf-bar-fill-sota"
                            : r.lang === "li"
                              ? "perf-bar-fill-li"
                              : "perf-bar-fill-other"
                        }
                        style={{
                          width: `${widthPct}%`,
                          height: "100%",
                          borderRadius: "4px",
                          minWidth: rel > 0 ? "2px" : 0,
                        }}
                      />
                    ) : null}
                  </div>
                );
              })}
              <span key={`${label}-best`} className="mono" style={{ textAlign: "right" }}>
                {best > 0 ? formatRelativePerf(best) : "—"}
              </span>
            </>
          );
        })}
      </div>
    </figure>
  );
}
