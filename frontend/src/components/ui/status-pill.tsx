"use client";

import { cn } from "@/lib/utils";

type StatusVariant = "healthy" | "active" | "degraded" | "warning" | "unhealthy" | "failing" | "inactive" | "error";

const variantStyles: Record<StatusVariant, { dot: string; bg: string; text: string }> = {
  healthy:  { dot: "bg-success",        bg: "bg-success-muted",  text: "text-success" },
  active:   { dot: "bg-success",        bg: "bg-success-muted",  text: "text-success" },
  degraded: { dot: "bg-warning",        bg: "bg-warning-muted",  text: "text-warning" },
  warning:  { dot: "bg-warning",        bg: "bg-warning-muted",  text: "text-warning" },
  unhealthy:{ dot: "bg-error",          bg: "bg-error-muted",    text: "text-error" },
  failing:  { dot: "bg-error",          bg: "bg-error-muted",    text: "text-error" },
  inactive: { dot: "bg-text-muted",     bg: "bg-bg-elevated",    text: "text-text-tertiary" },
  error:    { dot: "bg-error",          bg: "bg-error-muted",    text: "text-error" },
};

interface StatusPillProps {
  status: StatusVariant | string;
  label?: string;
  className?: string;
}

export function StatusPill({ status, label, className }: StatusPillProps) {
  const variant = variantStyles[status as StatusVariant] ?? variantStyles.inactive;
  const displayLabel = label ?? status;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium capitalize",
        variant.bg,
        variant.text,
        className
      )}
    >
      <span className={cn("status-dot", variant.dot)} />
      {displayLabel}
    </span>
  );
}
