import type { ReactNode } from "react";

export type BenchStatus = "green" | "yellow" | "red" | "unknown" | string;

const STATUS_CLASS: Record<string, string> = {
  green: "badge-green",
  yellow: "badge-yellow",
  red: "badge-red",
  unknown: "badge-unknown",
};

/** Non-color status cue (UX-A01). */
const STATUS_ICON: Record<string, string> = {
  green: "✓",
  yellow: "~",
  red: "✗",
  unknown: "?",
};

type BadgeProps = {
  status: BenchStatus;
  children?: ReactNode;
  className?: string;
};

export function Badge({ status, children, className = "" }: BadgeProps) {
  const key = status in STATUS_CLASS ? status : "unknown";
  const icon = STATUS_ICON[key] ?? "?";
  const label = children ?? status;
  return (
    <span className={`badge ${STATUS_CLASS[key]} ${className}`.trim()}>
      <span className="badge-icon" aria-hidden="true">
        {icon}
      </span>{" "}
      {label}
    </span>
  );
}

export { Badge as StatusBadge };
