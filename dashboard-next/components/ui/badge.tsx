import type { ReactNode } from "react";

export type BenchStatus = "green" | "yellow" | "red" | "unknown" | string;

const STATUS_CLASS: Record<string, string> = {
  green: "badge-green",
  yellow: "badge-yellow",
  red: "badge-red",
  unknown: "badge-unknown",
  skip: "badge-skip",
};

/** Non-color status cue (UX-A01). */
const STATUS_ICON: Record<string, string> = {
  green: "✓",
  yellow: "~",
  red: "✗",
  unknown: "?",
  skip: "—",
};

type BadgeProps = {
  status: BenchStatus;
  children?: ReactNode;
  className?: string;
  title?: string;
};

export function Badge({ status, children, className = "", title }: BadgeProps) {
  const key = status in STATUS_CLASS ? status : "unknown";
  const icon = STATUS_ICON[key] ?? "?";
  const label = children ?? status;
  return (
    <span
      className={`badge ${STATUS_CLASS[key]} ${className}`.trim()}
      title={title}
    >
      <span className="badge-icon" aria-hidden="true">
        {icon}
      </span>{" "}
      {label}
    </span>
  );
}

export { Badge as StatusBadge };
