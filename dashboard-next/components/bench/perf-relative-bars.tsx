import type { LangPoint } from "@/lib/summary";
import {
  buildRelativePerfBars,
  formatRelativePerf,
} from "@/lib/perf-relative";

type PerfRelativeBarsProps = {
  series: LangPoint[];
  sotaLang?: string | null;
  lowerIsBetter: boolean;
  claimable: boolean;
  /** Catalog row with no wall-clock ingest yet (UX-B06). */
  pending?: boolean;
};

export function PerfRelativeBars({
  series,
  sotaLang,
  lowerIsBetter,
  claimable,
  pending = false,
}: PerfRelativeBarsProps) {
  if (pending) {
    return (
      <figure className="perf-relative-chart perf-relative-pending">
        <figcaption className="mono perf-relative-caption">
          Not measured — this catalog row has no wall-clock data in the current ingest.
          Bars below are placeholders only.
        </figcaption>
        <div
          className="perf-bar-fill-pending"
          role="img"
          aria-label="Performance not measured"
        />
      </figure>
    );
  }

  const bars = buildRelativePerfBars(series, sotaLang, lowerIsBetter);

  if (bars.length === 0) {
    return (
      <p className="mono" style={{ color: "var(--muted)", marginTop: "1rem" }}>
        No relative performance chart — missing competitor series or SOTA lang.
      </p>
    );
  }

  const maxRelative = Math.max(...bars.map((b) => b.relative), 1);

  return (
    <figure className="perf-relative-chart" style={{ marginTop: "1.25rem" }}>
      <figcaption
        className="mono"
        style={{ fontSize: "0.85rem", color: "var(--muted)", marginBottom: "0.75rem" }}
      >
        Relative speed vs best competitor ({sotaLang}) — SOTA = 1.0, higher is
        better. Absolute {series[0]?.unit ? `${series[0].unit} ` : ""}values are
        in the table below.
        {!claimable ? (
          <span style={{ display: "block", marginTop: "0.35rem", color: "var(--yellow)" }}>
            Validity gate not passed — bars are informational only.
          </span>
        ) : null}
      </figcaption>
      <ul
        className="perf-relative-bars"
        style={{ listStyle: "none", margin: 0, padding: 0, display: "grid", gap: "0.5rem" }}
        role="img"
        aria-label={`Relative performance vs ${sotaLang ?? "best competitor"}`}
      >
        {bars.map((bar) => {
          const widthPct = Math.min(100, (bar.relative / maxRelative) * 100);
          const label = bar.variant ? `${bar.lang} (${bar.variant})` : bar.lang;
          return (
            <li
              key={`${bar.lang}-${bar.variant ?? ""}`}
              style={{
                display: "grid",
                gridTemplateColumns: "7rem 1fr 4.5rem",
                alignItems: "center",
                gap: "0.75rem",
                opacity: claimable || bar.isSota ? 1 : 0.65,
              }}
            >
              <span className={`lang-chip lang-${bar.lang}`} style={{ justifySelf: "start" }}>
                {label}
                {bar.isSota ? (
                  <span className="mono" style={{ color: "var(--muted)", marginLeft: "0.25rem" }}>
                    SOTA
                  </span>
                ) : null}
              </span>
              <div
                style={{
                  height: "1.25rem",
                  background: "color-mix(in srgb, var(--border) 60%, transparent)",
                  borderRadius: "4px",
                  overflow: "hidden",
                }}
              >
                <div
                  role="presentation"
                  className={
                    bar.isSota
                      ? "perf-bar-fill-sota"
                      : bar.lang === "li"
                        ? "perf-bar-fill-li"
                        : "perf-bar-fill-other"
                  }
                  style={{
                    width: `${widthPct}%`,
                    height: "100%",
                    borderRadius: "4px",
                    minWidth: bar.relative > 0 ? "2px" : 0,
                  }}
                />
              </div>
              <span className="mono" style={{ textAlign: "right" }}>
                {formatRelativePerf(bar.relative)}
              </span>
            </li>
          );
        })}
      </ul>
    </figure>
  );
}
