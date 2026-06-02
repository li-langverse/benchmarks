import type { ValidityStatus } from "@/lib/summary";

const VALIDITY_CLASS: Record<ValidityStatus, string> = {
  pass: "validity-pass",
  fail: "validity-fail",
  unknown: "validity-unknown",
  skip: "validity-skip",
};

type ValidityBadgeProps = {
  status: ValidityStatus | string;
  source?: string;
};

export function ValidityBadge({ status, source }: ValidityBadgeProps) {
  const label =
    status === "pass"
      ? "validity pass"
      : status === "fail"
        ? "validity fail"
        : status === "skip"
          ? "platform skip"
          : "validity unknown";
  const key =
    status === "pass" || status === "fail" || status === "unknown" || status === "skip"
      ? status
      : "unknown";
  return (
    <span
      className={`validity-badge ${VALIDITY_CLASS[key] ?? VALIDITY_CLASS.unknown}`}
      title={source ? `Source: ${source}` : undefined}
    >
      {label}
    </span>
  );
}
