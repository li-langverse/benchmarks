import Link from "next/link";
import type { ReactNode } from "react";
import { formatRelativePerf } from "@/lib/perf-relative";

export type RelativeBarItem = {
  key: string;
  label: ReactNode;
  relative: number;
  isReference?: boolean;
  highlight?: boolean;
  dimmed?: boolean;
  href?: string;
};

type RelativeBarListProps = {
  items: RelativeBarItem[];
  caption: ReactNode;
  ariaLabel: string;
  referenceNote?: string;
};

export function RelativeBarList({
  items,
  caption,
  ariaLabel,
  referenceNote = "SOTA = 1.0",
}: RelativeBarListProps) {
  if (items.length === 0) {
    return (
      <p className="mono" style={{ color: "var(--muted)", marginTop: "1rem" }}>
        No relative performance data — missing measured rows or SOTA reference.
      </p>
    );
  }

  const maxRelative = Math.max(...items.map((b) => b.relative), 1);

  return (
    <figure className="perf-relative-chart" style={{ marginTop: "1.25rem" }}>
      <figcaption
        className="mono"
        style={{ fontSize: "0.85rem", color: "var(--muted)", marginBottom: "0.75rem" }}
      >
        {caption}
        {referenceNote ? (
          <span style={{ display: "block", marginTop: "0.35rem" }}>{referenceNote}</span>
        ) : null}
      </figcaption>
      <ul
        className="perf-relative-bars"
        style={{ listStyle: "none", margin: 0, padding: 0, display: "grid", gap: "0.5rem" }}
        role="img"
        aria-label={ariaLabel}
      >
        {items.map((bar) => {
          const widthPct = Math.min(100, (bar.relative / maxRelative) * 100);
          const labelNode = bar.href ? (
            <Link href={bar.href} className="mono">
              {bar.label}
            </Link>
          ) : (
            bar.label
          );
          return (
            <li
              key={bar.key}
              style={{
                display: "grid",
                gridTemplateColumns: "minmax(7rem, 1.25fr) 1fr 4.5rem",
                alignItems: "center",
                gap: "0.75rem",
                opacity: bar.dimmed ? 0.65 : 1,
              }}
            >
              <span style={{ justifySelf: "start", fontSize: "0.9rem" }}>{labelNode}</span>
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
                  style={{
                    width: `${widthPct}%`,
                    height: "100%",
                    background: bar.isReference
                      ? "var(--accent)"
                      : bar.highlight
                        ? "var(--green)"
                        : "color-mix(in srgb, var(--muted) 70%, var(--text))",
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
