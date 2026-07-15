"use client";

import { useState } from "react";
import * as Dialog from "@radix-ui/react-dialog";
import { AlertTriangle, X } from "lucide-react";
import { cn } from "@/lib/utils";

interface ConfirmationModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description: string;
  confirmLabel?: string;
  cancelLabel?: string;
  variant?: "danger" | "warning" | "default";
  onConfirm: () => void | Promise<void>;
  loading?: boolean;
}

export function ConfirmationModal({
  open,
  onOpenChange,
  title,
  description,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  variant = "danger",
  onConfirm,
  loading = false,
}: ConfirmationModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleConfirm = async () => {
    setIsSubmitting(true);
    try {
      await onConfirm();
      onOpenChange(false);
    } finally {
      setIsSubmitting(false);
    }
  };

  const isLoading = loading || isSubmitting;

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-bg-overlay backdrop-blur-sm z-50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
        <Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-md glass-card p-6 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
          <div className="flex items-start gap-4">
            <div
              className={cn(
                "p-2.5 rounded-xl shrink-0",
                variant === "danger" && "bg-error-muted",
                variant === "warning" && "bg-warning-muted",
                variant === "default" && "bg-accent-muted"
              )}
            >
              <AlertTriangle
                className={cn(
                  "h-5 w-5",
                  variant === "danger" && "text-error",
                  variant === "warning" && "text-warning",
                  variant === "default" && "text-accent-primary"
                )}
              />
            </div>
            <div className="flex-1">
              <Dialog.Title className="text-base font-semibold text-text-primary">
                {title}
              </Dialog.Title>
              <Dialog.Description className="mt-1.5 text-sm text-text-tertiary leading-relaxed">
                {description}
              </Dialog.Description>
            </div>
            <Dialog.Close asChild>
              <button className="p-1 rounded-lg hover:bg-bg-elevated transition-colors text-text-tertiary hover:text-text-primary">
                <X className="h-4 w-4" />
              </button>
            </Dialog.Close>
          </div>

          <div className="flex justify-end gap-3 mt-6">
            <Dialog.Close asChild>
              <button
                className="px-4 py-2 rounded-lg text-sm font-medium bg-bg-elevated border border-border-primary text-text-secondary hover:text-text-primary hover:border-border-secondary transition-all"
                disabled={isLoading}
              >
                {cancelLabel}
              </button>
            </Dialog.Close>
            <button
              onClick={handleConfirm}
              disabled={isLoading}
              className={cn(
                "px-4 py-2 rounded-lg text-sm font-medium text-white transition-all",
                "disabled:opacity-50 disabled:cursor-not-allowed",
                variant === "danger" && "bg-error hover:bg-red-600",
                variant === "warning" && "bg-warning hover:bg-amber-600 text-black",
                variant === "default" && "gradient-accent hover:opacity-90"
              )}
            >
              {isLoading ? (
                <span className="inline-flex items-center gap-2">
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Processing...
                </span>
              ) : (
                confirmLabel
              )}
            </button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
