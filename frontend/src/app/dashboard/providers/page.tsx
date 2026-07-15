"use client";

import { motion } from "framer-motion";
import {
  Cloud, Sparkles, Globe, BrainCircuit, Activity,
  Zap, Server, Network, AlertTriangle, Info,
} from "lucide-react";
import { useProviders, useToggleProvider } from "@/lib/hooks/use-providers";
import { EmptyState } from "@/components/ui/empty-state";
import { SkeletonCard } from "@/components/ui/skeleton";
import { AddProviderModal } from "@/components/providers/add-provider-modal";
import { cn } from "@/lib/utils";

// ─── Static CSV-derived provider metadata ────────────────────────────────────

const PROVIDER_META: Record<string, {
  icon: React.ElementType;
  description: string;
  rateTier: string;
  rateTierColor: string;
  badge?: string;
  badgeColor?: string;
  caveat?: string;
}> = {
  groq: {
    icon: Zap,
    description: "LPU-powered inference — fastest free-tier latency available. Genuinely free, no credits system.",
    rateTier: "30–200 RPM",
    rateTierColor: "text-emerald-400",
    badge: "Fastest",
    badgeColor: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
  },
  "google-ai-studio": {
    icon: Globe,
    description: "Gemini family with 1M token context windows. Best all-round free multimodal models available.",
    rateTier: "10–15 RPM",
    rateTierColor: "text-blue-400",
    badge: "1M Context",
    badgeColor: "bg-blue-500/10 text-blue-400 border-blue-500/20",
  },
  mistral: {
    icon: Sparkles,
    description: "Free Experiment mode — phone verification required. Includes code specialists (Codestral, Devstral).",
    rateTier: "~1-2 RPS",
    rateTierColor: "text-orange-400",
    caveat: "Phone verification required to activate free mode.",
  },
  cerebras: {
    icon: BrainCircuit,
    description: "Fast free endpoint with 1M tokens/day limit. Only 1 production model; 2 are preview-only.",
    rateTier: "~30 RPM",
    rateTierColor: "text-purple-400",
    badge: "1M tok/day",
    badgeColor: "bg-purple-500/10 text-purple-400 border-purple-500/20",
  },
  "cloudflare-workers-ai": {
    icon: Server,
    description: "Edge-deployed models. Uses a shared 10K neuron/day pool across ALL models — very limited for production.",
    rateTier: "10K neurons/day",
    rateTierColor: "text-yellow-400",
    badge: "Shared Pool",
    badgeColor: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
    caveat: "~15–25 total calls/day shared across all Cloudflare models.",
  },
  openrouter: {
    icon: Network,
    description: "Routes to many free models. Auto-router keeps calls working even if a specific model ID is retired.",
    rateTier: "20 RPM",
    rateTierColor: "text-accent-primary",
    badge: "Auto-Router",
    badgeColor: "bg-accent-primary/10 text-accent-primary border-accent-primary/20",
  },
  "nvidia-nim": {
    icon: Activity,
    description: "NVIDIA-hosted open-weight models. Account-level 40 RPM. No fixed daily cap (verify current behavior).",
    rateTier: "~40 RPM",
    rateTierColor: "text-green-400",
    caveat: "Some trackers report a depleting credit pool — verify on your own account.",
  },
};

// ─── Component ────────────────────────────────────────────────────────────────

export default function ProvidersPage() {
  const { data: providers, isLoading } = useProviders();
  const toggleProvider = useToggleProvider();

  const handleToggle = (providerId: string, currentState: boolean) => {
    toggleProvider.mutate({ providerId, enable: !currentState });
  };

  const hasProviders = providers && providers.length > 0;

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-text-primary tracking-tight">AI Providers</h2>
          <p className="text-sm text-text-secondary mt-1">
            Manage your LLM provider connections and failover priority.
          </p>
        </div>
        <AddProviderModal />
      </div>

      {/* Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      ) : !hasProviders ? (
        <EmptyState
          icon={Cloud}
          title="No providers configured"
          description="Add a provider using the button above."
        />
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {providers.map((provider, i) => {
            const key = provider.name.toLowerCase().replace(/ /g, '-');
            const meta = PROVIDER_META[key];
            const Icon = meta?.icon ?? Cloud;

            return (
              <motion.div
                key={provider.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className={cn(
                  "glass-card p-5 flex flex-col gap-4 transition-all",
                  provider.is_enabled
                    ? "hover:glass-card-hover border-border-secondary/50"
                    : "opacity-70 grayscale-[20%]"
                )}
              >
                {/* Header row */}
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className={cn(
                      "w-11 h-11 rounded-xl flex items-center justify-center border shrink-0",
                      provider.is_enabled
                        ? "bg-accent-muted border-accent-primary/20 text-accent-primary"
                        : "bg-bg-elevated border-border-primary text-text-tertiary"
                    )}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-text-primary leading-tight">{provider.name}</h3>
                      {meta && (
                        <span className={cn("text-xs font-mono font-medium mt-0.5", meta.rateTierColor)}>
                          {meta.rateTier}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Enabled toggle */}
                  <button
                    role="switch"
                    aria-checked={provider.is_enabled}
                    onClick={() => handleToggle(provider.id, provider.is_enabled)}
                    className={cn(
                      "relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary",
                      provider.is_enabled ? "bg-success" : "bg-bg-elevated"
                    )}
                  >
                    <span className="sr-only">Toggle provider</span>
                    <span className={cn(
                      "pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out",
                      provider.is_enabled ? "translate-x-5" : "translate-x-0"
                    )} />
                  </button>
                </div>

                {/* Description */}
                {meta?.description && (
                  <p className="text-xs text-text-secondary leading-relaxed -mt-1">
                    {meta.description}
                  </p>
                )}

                {/* Caveat warning */}
                {meta?.caveat && (
                  <div className="flex items-start gap-2 px-3 py-2 rounded-lg border border-yellow-500/20 bg-yellow-500/5">
                    <AlertTriangle className="w-3.5 h-3.5 text-yellow-400 shrink-0 mt-0.5" />
                    <p className="text-[11px] text-yellow-300/90 leading-relaxed">{meta.caveat}</p>
                  </div>
                )}

                {/* Footer row: priority / weight / badge */}
                <div className="flex items-center gap-2 flex-wrap pt-1 border-t border-border-primary">
                  <span className="text-xs px-2 py-0.5 rounded border border-border-primary bg-bg-elevated text-text-tertiary">
                    Priority {provider.priority}
                  </span>
                  <span className="text-xs text-text-tertiary">Wt: {provider.weight}</span>
                  {meta?.badge && (
                    <span className={cn("ml-auto text-xs font-semibold px-2 py-0.5 rounded border", meta.badgeColor)}>
                      {meta.badge}
                    </span>
                  )}
                </div>

                {/* Models */}
                {provider.models && provider.models.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold text-text-tertiary uppercase tracking-wider mb-2">
                      Models ({provider.models.length})
                    </p>
                    <div className="flex flex-wrap gap-1.5 max-h-28 overflow-y-auto">
                      {provider.models.map((model) => (
                        <span
                          key={model}
                          className="inline-flex px-2 py-0.5 bg-bg-elevated border border-border-primary rounded text-[11px] font-mono text-text-secondary"
                        >
                          {model}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            );
          })}
        </motion.div>
      )}
    </div>
  );
}
