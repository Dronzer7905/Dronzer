"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion } from "framer-motion";
import * as Dialog from "@radix-ui/react-dialog";
import {
  Brain, Filter, Edit2, X, Loader2,
  AlertTriangle, MessageSquare, Code2, Eye, Zap, Search,
  Info,
} from "lucide-react";

import { useModels, useUpdateModel } from "@/lib/hooks/use-models";
import { useProviders } from "@/lib/hooks/use-providers";
import { EmptyState } from "@/components/ui/empty-state";
import { SkeletonTable } from "@/components/ui/skeleton";
import { AddModelModal } from "@/components/models/add-model-modal";
import type { ModelConfigResponse } from "@/lib/api/types";
import { cn } from "@/lib/utils";

const cwSchema = z.object({
  context_window: z.number().min(1).max(2000000)
});
type CwForm = z.infer<typeof cwSchema>;

// ─── Capability pills derived from capabilities JSON ─────────────────────────

interface Cap {
  label: string;
  icon: React.ElementType;
  colorClass: string;
}

function getCapPills(caps: Record<string, unknown> = {}): Cap[] {
  const pills: Cap[] = [];
  if (caps.chat)       pills.push({ label: "Chat",      icon: MessageSquare, colorClass: "text-accent-primary bg-accent-muted border-accent-primary/20" });
  if (caps.code)       pills.push({ label: "Code",      icon: Code2,         colorClass: "text-blue-400 bg-blue-500/10 border-blue-500/20" });
  if (caps.vision)     pills.push({ label: "Vision",    icon: Eye,           colorClass: "text-purple-400 bg-purple-500/10 border-purple-500/20" });
  if (caps.reasoning)  pills.push({ label: "Reasoning", icon: Brain,         colorClass: "text-orange-400 bg-orange-500/10 border-orange-500/20" });
  if (caps.embedding)  pills.push({ label: "Embedding", icon: Search,        colorClass: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20" });
  if (caps.agentic)    pills.push({ label: "Agentic",   icon: Zap,           colorClass: "text-yellow-400 bg-yellow-500/10 border-yellow-500/20" });
  return pills;
}

// ─── Tooltip component (simple hover) ────────────────────────────────────────

function Tooltip({ children, tip }: { children: React.ReactNode; tip: string }) {
  return (
    <span className="relative group inline-flex items-center">
      {children}
      <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-max max-w-xs px-2 py-1.5 rounded-lg bg-bg-primary border border-border-primary text-xs text-text-secondary shadow-lg opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50 whitespace-normal text-center">
        {tip}
      </span>
    </span>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function ModelsPage() {
  const [providerFilter, setProviderFilter] = useState<string>("");
  const { data: models, isLoading } = useModels(providerFilter || undefined);
  const { data: providers } = useProviders();
  const updateModel = useUpdateModel();

  const [modelToEdit, setModelToEdit] = useState<ModelConfigResponse | null>(null);

  const { register, handleSubmit, reset, formState: { errors } } = useForm<CwForm>({
    resolver: zodResolver(cwSchema)
  });

  const openEditModal = (model: ModelConfigResponse) => {
    setModelToEdit(model);
    reset({ context_window: model.context_window });
  };

  const handleUpdateCw = async (data: CwForm) => {
    if (!modelToEdit) return;
    try {
      await updateModel.mutateAsync({
        modelId: modelToEdit.id,
        params: { context_window: data.context_window }
      });
      setModelToEdit(null);
    } catch (e) {
      // handled by tanstack query
    }
  };

  const handleToggle = (model: ModelConfigResponse) => {
    updateModel.mutate({
      modelId: model.id,
      params: { is_enabled: !model.is_enabled }
    });
  };

  const getProviderName = (id: string) =>
    providers?.find(p => p.id === id)?.name || id;

  const formatCw = (num: number) => {
    if (num >= 1_000_000) return `${(num / 1_000_000).toFixed(1)}M`;
    if (num >= 1000) return `${Math.floor(num / 1000)}K`;
    return num.toString();
  };

  // Count preview models
  const previewCount = models?.filter(m => m.capabilities?.is_preview).length ?? 0;

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row gap-4 sm:items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-text-primary tracking-tight">Models</h2>
          <p className="text-sm text-text-secondary mt-1">
            Configure AI models, availability, and routing limits.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" />
            <select
              value={providerFilter}
              onChange={(e) => setProviderFilter(e.target.value)}
              className="input-field pl-9 h-10 w-full sm:w-56 appearance-none bg-[url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20width%3D%2224%22%20height%3D%2224%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cpath%20d%3D%22M7%2010l5%205%205-5z%22%20fill%3D%22%236b7280%22%2F%3E%3C%2Fsvg%3E')] bg-[length:24px_24px] bg-[right_8px_center] bg-no-repeat"
            >
              <option value="">All Providers</option>
              {providers?.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
          <AddModelModal />
        </div>
      </div>

      {/* Preview model advisory banner */}
      {!isLoading && previewCount > 0 && (
        <div className="flex items-start gap-3 p-3 rounded-xl border border-yellow-500/20 bg-yellow-500/5">
          <AlertTriangle className="w-4 h-4 text-yellow-400 shrink-0 mt-0.5" />
          <p className="text-xs text-yellow-300/90">
            <span className="font-semibold text-yellow-400">{previewCount} preview model{previewCount > 1 ? "s" : ""}</span> detected.
            Preview models can be removed by the provider at any time with no notice.
            Disable them for production gateway keys and use stable (GA) models instead.
          </p>
        </div>
      )}

      {/* Table */}
      {isLoading ? (
        <div className="glass-card overflow-hidden">
          <SkeletonTable rows={8} />
        </div>
      ) : !models || models.length === 0 ? (
        <EmptyState
          icon={Brain}
          title="No models found"
          description={providerFilter ? "No models configured for this provider." : "No models configured yet."}
        />
      ) : (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card overflow-hidden"
        >
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-bg-elevated border-b border-border-primary text-text-secondary">
                <tr>
                  <th className="px-5 py-3 font-medium">Model ID</th>
                  <th className="px-5 py-3 font-medium">Provider</th>
                  <th className="px-5 py-3 font-medium">Context</th>
                  <th className="px-5 py-3 font-medium">Capabilities</th>
                  <th className="px-5 py-3 font-medium">Rate Limit</th>
                  <th className="px-5 py-3 font-medium">Daily Cap</th>
                  <th className="px-5 py-3 font-medium text-right">Enabled</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-primary">
                {models.map((model) => {
                  const caps = model.capabilities ?? {};
                  const isPreview = !!caps.is_preview;
                  const pills = getCapPills(caps);

                  return (
                    <tr
                      key={model.id}
                      className={cn(
                        "transition-colors group",
                        model.is_enabled ? "hover:bg-bg-card-hover" : "opacity-60 bg-bg-primary"
                      )}
                    >
                      {/* Model ID */}
                      <td className="px-5 py-3">
                        <div className="flex items-center gap-2">
                          <span className="font-mono font-medium text-accent-primary text-xs">
                            {model.name}
                          </span>
                          {isPreview && (
                            <Tooltip tip={caps.notes as string || "Preview — may be removed without notice"}>
                              <span className="px-1.5 py-0.5 rounded text-[10px] font-bold border bg-yellow-500/10 text-yellow-400 border-yellow-500/20 cursor-help">
                                PREVIEW
                              </span>
                            </Tooltip>
                          )}
                          {caps.notes && !isPreview && (
                            <Tooltip tip={caps.notes as string}>
                              <Info className="w-3.5 h-3.5 text-text-tertiary cursor-help hover:text-text-secondary transition-colors" />
                            </Tooltip>
                          )}
                        </div>
                      </td>

                      {/* Provider */}
                      <td className="px-5 py-3">
                        <span className="inline-flex items-center px-2 py-0.5 rounded bg-bg-elevated border border-border-primary text-xs font-medium text-text-secondary">
                          {getProviderName(model.provider_id)}
                        </span>
                      </td>

                      {/* Context Window */}
                      <td className="px-5 py-3">
                        <div className="flex items-center gap-1.5">
                          <span className="font-mono text-text-secondary text-xs">
                            {formatCw(model.context_window)}
                          </span>
                          <button
                            onClick={() => openEditModal(model)}
                            className="p-1 text-text-tertiary hover:text-accent-primary rounded transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100 focus:outline-none"
                            title="Edit Context Window"
                          >
                            <Edit2 className="w-3 h-3" />
                          </button>
                        </div>
                      </td>

                      {/* Capability pills */}
                      <td className="px-5 py-3">
                        <div className="flex flex-wrap gap-1">
                          {pills.length > 0 ? pills.map((p) => {
                            const PillIcon = p.icon;
                            return (
                              <span
                                key={p.label}
                                className={cn(
                                  "inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-medium border",
                                  p.colorClass
                                )}
                              >
                                <PillIcon className="w-2.5 h-2.5" />
                                {p.label}
                              </span>
                            );
                          }) : (
                            <span className="text-xs text-text-tertiary">—</span>
                          )}
                        </div>
                      </td>

                      {/* Rate limit */}
                      <td className="px-5 py-3">
                        <span className="text-xs text-text-secondary font-mono whitespace-nowrap">
                          {(caps.rate_limit as string) || "—"}
                        </span>
                      </td>

                      {/* Daily cap */}
                      <td className="px-5 py-3">
                        <span className="text-xs text-text-tertiary whitespace-nowrap">
                          {(caps.daily_cap as string) || "—"}
                        </span>
                      </td>

                      {/* Toggle */}
                      <td className="px-5 py-3 text-right">
                        <button
                          role="switch"
                          aria-checked={model.is_enabled}
                          onClick={() => handleToggle(model)}
                          className={cn(
                            "relative inline-flex h-5 w-9 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary",
                            model.is_enabled ? "bg-success" : "bg-bg-elevated"
                          )}
                        >
                          <span className="sr-only">Toggle model</span>
                          <span className={cn(
                            "pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out",
                            model.is_enabled ? "translate-x-4" : "translate-x-0"
                          )} />
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Table footer */}
          <div className="px-5 py-2.5 border-t border-border-primary bg-bg-elevated flex items-center gap-4">
            <span className="text-xs text-text-tertiary">
              {models.length} model{models.length !== 1 ? "s" : ""}
              {previewCount > 0 && (
                <span className="ml-2 text-yellow-400">{previewCount} preview</span>
              )}
            </span>
            <span className="text-xs text-text-tertiary ml-auto">
              Hover a model ID for notes &bull; Click ✎ to edit context window
            </span>
          </div>
        </motion.div>
      )}

      {/* Edit Context Window Modal */}
      <Dialog.Root open={!!modelToEdit} onOpenChange={(open) => !open && setModelToEdit(null)}>
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 bg-bg-overlay backdrop-blur-sm z-50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
          <Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-sm glass-card p-6 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
            <div className="flex items-center justify-between mb-6">
              <Dialog.Title className="text-lg font-semibold text-text-primary">Update Context Window</Dialog.Title>
              <Dialog.Close asChild>
                <button className="p-1 rounded-lg hover:bg-bg-elevated text-text-tertiary hover:text-text-primary transition-colors">
                  <X className="w-4 h-4" />
                </button>
              </Dialog.Close>
            </div>

            <p className="text-sm text-text-secondary mb-4">
              Setting limit for <span className="font-mono text-accent-primary">{modelToEdit?.name}</span>
            </p>

            <form onSubmit={handleSubmit(handleUpdateCw)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">Max Tokens</label>
                <input
                  {...register("context_window", { valueAsNumber: true })}
                  type="number"
                  autoFocus
                  className="input-field w-full h-10 font-mono"
                  disabled={updateModel.isPending}
                />
                {errors.context_window && (
                  <p className="mt-1.5 text-xs text-error">{errors.context_window.message}</p>
                )}
              </div>

              <div className="pt-2 flex justify-end gap-3">
                <Dialog.Close asChild>
                  <button type="button" className="px-4 py-2 rounded-lg text-sm font-medium bg-bg-elevated border border-border-primary text-text-secondary hover:text-text-primary">
                    Cancel
                  </button>
                </Dialog.Close>
                <button
                  type="submit"
                  disabled={updateModel.isPending}
                  className="px-4 py-2 rounded-lg text-sm font-medium text-white gradient-accent hover:opacity-90 flex items-center gap-2 disabled:opacity-70"
                >
                  {updateModel.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                  Save Changes
                </button>
              </div>
            </form>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>
    </div>
  );
}
