import type { ReactNode } from "react";

export type BenchStatus = "green" | "yellow" | "red" | "unknown" | string;

const STATUS_CLASS: Record<string, string> = {
  green: "badge-green",
  yellow: "badge-yellow",
  red: "badge-red",
  unknown: "badge-unknown",
};

type BadgeProps = {
  status: BenchStatus;
  children?: ReactNode;
  className?: string;
};

export function Badge({ status, children, className = "" }: BadgeProps) {
  const key = status in STATUS_CLASS ? status : "unknown";
  return (
    <span className={`badge ${STATUS_CLASS[key]} ${className}`.trim()}>
      {children ?? status}
    </span>
  );
}

export { Badge as StatusBadge };
