import type { ValidityStatus } from "@/lib/summary";

const VALIDITY_CLASS: Record<ValidityStatus, string> = {
  pass: "validity-pass",
  fail: "validity-fail",
  unknown: "validity-unknown",
};

type ValidityBadgeProps = {
  status: ValidityStatus;
  source?: string;
};

export function ValidityBadge({ status, source }: ValidityBadgeProps) {
  const label =
    status === "pass"
      ? "validity pass"
      : status === "fail"
        ? "validity fail"
        : "validity unknown";
  return (
    <span
      className={`validity-badge ${VALIDITY_CLASS[status] ?? VALIDITY_CLASS.unknown}`}
      title={source ? `Source: ${source}` : undefined}
    >
      {label}
    </span>
  );
}
