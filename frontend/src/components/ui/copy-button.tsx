"use client";

import { useState, useCallback } from "react";
import { Check, Copy } from "lucide-react";
import { cn } from "@/lib/utils";

interface CopyButtonProps {
  value: string;
  className?: string;
  label?: string;
}

export function CopyButton({ value, className, label }: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback for non-secure contexts
      const textarea = document.createElement("textarea");
      textarea.value = value;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [value]);

  return (
    <button
      onClick={handleCopy}
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium",
        "bg-bg-elevated border border-border-primary",
        "hover:border-accent-primary hover:bg-accent-muted",
        "transition-all duration-200",
        "focus-visible:ring-2 focus-visible:ring-accent-primary",
        className
      )}
      title="Copy to clipboard"
    >
      {copied ? (
        <>
          <Check className="h-3.5 w-3.5 text-success" />
          {label ? <span className="text-success">Copied!</span> : null}
        </>
      ) : (
        <>
          <Copy className="h-3.5 w-3.5 text-text-secondary" />
          {label ? <span className="text-text-secondary">{label}</span> : null}
        </>
      )}
    </button>
  );
}
