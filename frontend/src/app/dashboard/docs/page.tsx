"use client";

import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  BookOpen, ChevronDown, ChevronRight, ArrowRight,
  LayoutDashboard, Building2, FolderKanban, ShieldCheck,
  Key, Cloud, Brain, Puzzle, MessageSquare, Activity,
  Zap, Code2, Search, Star, AlertTriangle, Info,
  ExternalLink, Copy, CheckCheck,
} from "lucide-react";
import { FREE_PROVIDERS, TOTAL_MODEL_COUNT, TOTAL_PROVIDER_COUNT, PROVIDER_COLORS } from "@/lib/data/free-providers";
import { cn } from "@/lib/utils";

// ─── Types ────────────────────────────────────────────────────────────────────

interface PageGuide {
  icon: React.ElementType;
  title: string;
  path: string;
  tagline: string;
  steps: string[];
  tips?: string[];
}

// ─── Data ─────────────────────────────────────────────────────────────────────

const PAGE_GUIDES: PageGuide[] = [
  {
    icon: LayoutDashboard,
    title: "Dashboard",
    path: "/dashboard",
    tagline: "Real-time system health at a glance.",
    steps: [
      "View live metrics: active requests, token usage, cache hit rate, and circuit breaker status.",
      "Check the system liveness indicator (green dot = gateway is up).",
      "Review uptime, loaded providers count, and plugin count from the Diagnostics card.",
      "Use the charts to spot traffic spikes or error patterns over time.",
    ],
    tips: [
      "If you see circuit_breakers_open > 0, a provider is temporarily down — check AI Providers to see which.",
      "Cache hit rate above 70% means your prompts are being served from cache — great for cost savings.",
    ],
  },
  {
    icon: Building2,
    title: "Organizations",
    path: "/dashboard/organizations",
    tagline: "Top-level tenants that own projects and keys.",
    steps: [
      "Create an organization with a name and optional billing email.",
      "Each organization can have multiple projects.",
      "Organizations isolate usage, keys, and routing rules.",
    ],
    tips: [
      "Start here — you need an org before you can create projects or gateway keys.",
      "For personal use, one org is enough.",
    ],
  },
  {
    icon: FolderKanban,
    title: "Projects",
    path: "/dashboard/projects",
    tagline: "Logical groupings for workloads within an organization.",
    steps: [
      "Create a project under an existing organization.",
      "Choose an environment: production, staging, or development.",
      "Assign gateway keys to specific projects to scope their access.",
    ],
    tips: [
      "Use separate projects for your prod app vs. your dev sandbox to keep rate limits and logs separate.",
    ],
  },
  {
    icon: ShieldCheck,
    title: "Gateway Keys",
    path: "/dashboard/gateway-keys",
    tagline: "The API keys YOUR users/apps use to talk to Dronzer.",
    steps: [
      "Create a gateway key linked to an organization and optionally a project.",
      "Optionally set task_type (e.g., 'chat', 'code') to steer routing.",
      "Set model_priorities or provider_priorities to control which providers get traffic.",
      "Copy the key_value immediately — it's only shown once.",
      "Use this key as the Bearer token in your OpenAI-compatible API calls to the gateway.",
    ],
    tips: [
      "Gateway keys are what your application uses. Provider Credentials are what the gateway uses internally.",
      "Set provider_priorities to ['groq', 'google-ai-studio'] to prefer fast/free providers.",
    ],
  },
  {
    icon: Key,
    title: "Provider Credentials",
    path: "/dashboard/api-keys",
    tagline: "The actual API keys the gateway uses to call upstream LLMs.",
    steps: [
      "After importing providers, come here to add your API keys.",
      "Select the provider (e.g., Groq), select a project, and paste your key.",
      "Add a label to identify the key (e.g., 'groq-production').",
      "The gateway will automatically rotate between healthy keys and skip failing ones.",
    ],
    tips: [
      "You can add multiple keys per provider — the gateway load-balances across them.",
      "A key marked is_failing means the last request to that key got an auth error — replace it.",
    ],
  },
  {
    icon: Cloud,
    title: "AI Providers",
    path: "/dashboard/providers",
    tagline: "The LLM providers the gateway routes to.",
    steps: [
      "Click 'Import from CSV' to auto-seed all 7 verified free providers.",
      "Or manually add a custom provider with a name, priority, and weight.",
      "Toggle providers on/off to include/exclude them from routing.",
      "Priority = lower number = tried first. Weight = higher number = more traffic share.",
    ],
    tips: [
      "Set Groq at priority 1 (fastest) and Google AI Studio at priority 2 (largest context) for a strong free-tier stack.",
      "Disabling a provider removes it from routing without deleting it.",
    ],
  },
  {
    icon: Brain,
    title: "Models",
    path: "/dashboard/models",
    tagline: "Individual model configs registered under providers.",
    steps: [
      "Models are auto-created when you import providers via the CSV flow.",
      "To add a single model manually: click 'Add Model', select a provider, enter the model ID exactly as it appears in the provider's API, and set the context window.",
      "Toggle models on/off to control which are available for routing.",
      "Click the edit pencil icon on any model's context window to update it.",
    ],
    tips: [
      "The model ID must match exactly what the provider API expects (e.g., 'llama-3.3-70b-versatile' for Groq, not 'Llama 3.3 70B').",
      "Context window limits are used by the gateway to reject oversized requests before they hit the provider.",
    ],
  },
  {
    icon: Puzzle,
    title: "Plugins",
    path: "/dashboard/plugins",
    tagline: "Extend the gateway with custom logic.",
    steps: [
      "Browse loaded plugins in the plugin registry.",
      "Click 'Reload Plugins' after dropping a new plugin into the plugins directory.",
      "Plugins can intercept requests, add custom headers, implement caching strategies, etc.",
    ],
  },
  {
    icon: MessageSquare,
    title: "Playground",
    path: "/dashboard/playground",
    tagline: "Test your gateway interactively before integrating.",
    steps: [
      "Select a gateway key to authenticate as.",
      "Choose a model from the dropdown (any model registered in your gateway).",
      "Type a message and send — the gateway routes it through the configured provider chain.",
      "Try streaming by toggling the stream switch.",
      "Check the response metadata to see which provider was actually used.",
    ],
    tips: [
      "Use the Playground to verify your provider + model setup before wiring up your application.",
      "If you get a 401, make sure the selected gateway key is active.",
    ],
  },
];

const QUICK_START_STEPS = [
  {
    number: "01",
    title: "Create an Organization",
    desc: "Go to Organizations and create one. This is the top-level tenant that owns everything.",
    href: "/dashboard/organizations",
    icon: Building2,
  },
  {
    number: "02",
    title: "Import Free LLM Providers",
    desc: `Go to AI Providers → click \"Import from CSV\" → select all 7 providers → Import. This registers ${TOTAL_MODEL_COUNT} models automatically.`,
    href: "/dashboard/providers",
    icon: Cloud,
  },
  {
    number: "03",
    title: "Add Your API Keys",
    desc: "Go to Provider Credentials and paste your actual API keys (Groq key, Google AI Studio key, etc.).",
    href: "/dashboard/api-keys",
    icon: Key,
  },
  {
    number: "04",
    title: "Create a Gateway Key",
    desc: "Go to Gateway Keys → create a key linked to your org. Copy the key_value — this is your single API key for all LLMs.",
    href: "/dashboard/gateway-keys",
    icon: ShieldCheck,
  },
  {
    number: "05",
    title: "Make Your First API Call",
    desc: "Use the Playground to test, or call the gateway directly with your app using the OpenAI SDK.",
    href: "/dashboard/playground",
    icon: Zap,
  },
];

// ─── Components ───────────────────────────────────────────────────────────────

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <button
      onClick={handleCopy}
      className="absolute right-2 top-2 p-1.5 rounded text-text-tertiary hover:text-text-primary hover:bg-bg-elevated transition-colors"
    >
      {copied ? <CheckCheck className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
    </button>
  );
}

function CodeBlock({ code, language = "bash" }: { code: string; language?: string }) {
  return (
    <div className="relative rounded-xl border border-border-primary bg-bg-primary overflow-x-auto mt-3">
      <div className="flex items-center gap-2 px-4 py-2 border-b border-border-primary bg-bg-elevated">
        <Code2 className="w-3.5 h-3.5 text-text-tertiary" />
        <span className="text-xs text-text-tertiary font-mono">{language}</span>
      </div>
      <pre className="p-4 text-xs font-mono text-text-secondary leading-relaxed overflow-x-auto">
        <code>{code}</code>
      </pre>
      <CopyButton text={code} />
    </div>
  );
}

function AccordionItem({ guide }: { guide: PageGuide }) {
  const [open, setOpen] = useState(false);
  const Icon = guide.icon;

  return (
    <div className={cn("rounded-xl border transition-all", open ? "border-accent-primary/30 bg-accent-muted/20" : "border-border-primary bg-bg-elevated")}>
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-4 p-4 text-left"
      >
        <div className={cn("w-10 h-10 rounded-xl flex items-center justify-center shrink-0 border transition-colors", open ? "bg-accent-primary/20 border-accent-primary/30 text-accent-primary" : "bg-bg-primary border-border-primary text-text-secondary")}>
          <Icon className="w-5 h-5" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-text-primary">{guide.title}</span>
            <Link
              href={guide.path}
              onClick={(e) => e.stopPropagation()}
              className="text-xs text-accent-primary hover:underline flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity"
            >
              Go <ExternalLink className="w-3 h-3" />
            </Link>
          </div>
          <p className="text-sm text-text-tertiary">{guide.tagline}</p>
        </div>
        {open ? <ChevronDown className="w-4 h-4 text-text-tertiary shrink-0" /> : <ChevronRight className="w-4 h-4 text-text-tertiary shrink-0" />}
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4 space-y-4 border-t border-border-primary pt-4">
              <div>
                <h4 className="text-xs font-bold text-text-tertiary uppercase tracking-wider mb-2">How to use</h4>
                <ol className="space-y-2">
                  {guide.steps.map((step, i) => (
                    <li key={i} className="flex gap-3 text-sm">
                      <span className="w-5 h-5 rounded-full bg-accent-primary/10 border border-accent-primary/20 text-accent-primary text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                        {i + 1}
                      </span>
                      <span className="text-text-secondary leading-relaxed">{step}</span>
                    </li>
                  ))}
                </ol>
              </div>

              {guide.tips && guide.tips.length > 0 && (
                <div>
                  <h4 className="text-xs font-bold text-text-tertiary uppercase tracking-wider mb-2">💡 Pro Tips</h4>
                  <div className="space-y-2">
                    {guide.tips.map((tip, i) => (
                      <div key={i} className="flex gap-2 p-3 rounded-lg border border-accent-primary/10 bg-accent-muted/20 text-xs text-text-secondary leading-relaxed">
                        <Star className="w-3.5 h-3.5 text-accent-primary shrink-0 mt-0.5" />
                        {tip}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <Link
                href={guide.path}
                className="inline-flex items-center gap-2 text-sm text-accent-primary hover:underline"
              >
                Open {guide.title} <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

// ─── Free Provider Table ──────────────────────────────────────────────────────

function FreeProviderTable() {
  const [search, setSearch] = useState("");

  const filtered = FREE_PROVIDERS.flatMap((p) =>
    p.models
      .filter(
        (m) =>
          m.modelId.toLowerCase().includes(search.toLowerCase()) ||
          p.provider.toLowerCase().includes(search.toLowerCase())
      )
      .map((m) => ({ ...m, provider: p.provider, color: p.color }))
  );

  const formatCw = (n: number) => {
    if (n >= 1000000) return `${Math.floor(n / 1000)}K`;
    if (n >= 1000) return `${Math.floor(n / 1000)}K`;
    return n.toString();
  };

  return (
    <div className="space-y-3">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" />
        <input
          type="text"
          placeholder="Search model ID or provider..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="input-field w-full pl-9 h-10"
        />
      </div>

      <div className="rounded-xl border border-border-primary overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-bg-elevated border-b border-border-primary text-text-secondary">
              <tr>
                <th className="px-4 py-3 font-semibold">Provider</th>
                <th className="px-4 py-3 font-semibold">Model ID</th>
                <th className="px-4 py-3 font-semibold">Context</th>
                <th className="px-4 py-3 font-semibold">Rate Limit</th>
                <th className="px-4 py-3 font-semibold">Daily Cap</th>
                <th className="px-4 py-3 font-semibold">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-primary">
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-text-tertiary">
                    No models match &quot;{search}&quot;
                  </td>
                </tr>
              ) : (
                filtered.map((m) => {
                  const colors = PROVIDER_COLORS[m.color];
                  return (
                    <tr key={`${m.provider}-${m.modelId}`} className="hover:bg-bg-elevated/50 transition-colors">
                      <td className="px-4 py-2.5">
                        <span className={cn("px-2 py-0.5 rounded text-[10px] font-bold border", colors.bg, colors.text, colors.border)}>
                          {m.provider.split(" ")[0]}
                        </span>
                      </td>
                      <td className="px-4 py-2.5 font-mono text-text-primary">{m.modelId}</td>
                      <td className="px-4 py-2.5 font-mono text-text-secondary">{formatCw(m.contextWindow)}</td>
                      <td className="px-4 py-2.5 text-text-tertiary max-w-[180px] truncate" title={m.rateLimitNote}>{m.rateLimitNote}</td>
                      <td className="px-4 py-2.5 text-text-tertiary">{m.dailyCap}</td>
                      <td className="px-4 py-2.5">
                        {m.isPreview ? (
                          <span className="px-1.5 py-0.5 rounded bg-yellow-500/10 text-yellow-400 border border-yellow-500/20 text-[10px] font-medium">PREVIEW</span>
                        ) : (
                          <span className="px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-medium">GA</span>
                        )}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
        <div className="px-4 py-2 bg-bg-elevated border-t border-border-primary flex items-center justify-between">
          <p className="text-xs text-text-tertiary">
            {filtered.length} of {TOTAL_MODEL_COUNT} models · Verified July 2026
          </p>
          <a
            href="https://openrouter.ai/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-accent-primary hover:underline flex items-center gap-1"
          >
            Check current limits <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function DocsPage() {
  const [activeSection, setActiveSection] = useState<string>("quickstart");

  const sections = [
    { id: "quickstart", label: "Quick Start", icon: Zap },
    { id: "pages", label: "Page Guide", icon: BookOpen },
    { id: "max-results", label: "Getting Max Results", icon: Star },
    { id: "api", label: "API Usage", icon: Code2 },
    { id: "free-models", label: "Free Model Reference", icon: Activity },
  ];

  return (
    <div className="max-w-7xl mx-auto pb-16">
      {/* Hero Header */}
      <motion.div
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative rounded-2xl border border-border-primary overflow-hidden mb-8 p-8"
        style={{ background: "linear-gradient(135deg, var(--accent-muted) 0%, var(--bg-elevated) 50%, var(--bg-primary) 100%)" }}
      >
        <div className="absolute -top-16 -right-16 w-64 h-64 rounded-full bg-accent-primary/10 blur-3xl pointer-events-none" />
        <div className="absolute -bottom-12 -left-12 w-48 h-48 rounded-full bg-purple-500/5 blur-3xl pointer-events-none" />

        <div className="relative flex items-start gap-5">
          <div className="w-14 h-14 rounded-2xl gradient-accent flex items-center justify-center shadow-lg shadow-accent-primary/20 shrink-0">
            <BookOpen className="w-7 h-7 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl font-bold text-text-primary">Dronzer Documentation</h1>
              <span className="px-2 py-0.5 rounded border border-accent-primary/30 bg-accent-muted text-accent-primary text-xs font-medium">v1.0</span>
            </div>
            <p className="text-text-secondary max-w-2xl leading-relaxed">
              Dronzer is an <strong className="text-text-primary">enterprise AI Gateway</strong> — a single, unified API endpoint that routes LLM requests to multiple providers with automatic failover, load balancing, caching, rate limit management, and observability.
              Use one key, get access to every free and paid LLM.
            </p>
            <div className="flex flex-wrap gap-3 mt-4">
              {[
                { label: `${TOTAL_PROVIDER_COUNT} Free Providers`, color: "text-emerald-400" },
                { label: `${TOTAL_MODEL_COUNT} Models`, color: "text-blue-400" },
                { label: "OpenAI-Compatible API", color: "text-purple-400" },
                { label: "Auto Failover", color: "text-orange-400" },
              ].map((badge) => (
                <span key={badge.label} className={cn("text-xs font-medium px-2 py-1 rounded-full bg-bg-elevated border border-border-primary", badge.color)}>
                  ✓ {badge.label}
                </span>
              ))}
            </div>
          </div>
        </div>
      </motion.div>

      <div className="flex gap-8">
        {/* Sidebar nav */}
        <div className="w-52 shrink-0">
          <div className="sticky top-6 space-y-1">
            <p className="text-xs font-bold text-text-tertiary uppercase tracking-wider px-3 mb-3">Contents</p>
            {sections.map((s) => {
              const Icon = s.icon;
              return (
                <button
                  key={s.id}
                  onClick={() => setActiveSection(s.id)}
                  className={cn(
                    "w-full flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm font-medium transition-all text-left",
                    activeSection === s.id
                      ? "bg-accent-muted text-accent-primary"
                      : "text-text-secondary hover:bg-bg-elevated hover:text-text-primary"
                  )}
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  {s.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Main content */}
        <div className="flex-1 min-w-0 space-y-8">

          {/* QUICK START */}
          {activeSection === "quickstart" && (
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-text-primary">Quick Start</h2>
                <p className="text-text-secondary mt-1">Get from zero to routing real LLM requests in under 5 minutes.</p>
              </div>

              <div className="space-y-4">
                {QUICK_START_STEPS.map((step, i) => {
                  const Icon = step.icon;
                  return (
                    <motion.div
                      key={step.number}
                      initial={{ opacity: 0, x: -12 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.08 }}
                      className="flex gap-4 p-5 rounded-xl border border-border-primary bg-bg-elevated hover:border-accent-primary/30 transition-all group"
                    >
                      <div className="flex flex-col items-center gap-2 shrink-0">
                        <div className="w-10 h-10 rounded-xl gradient-accent flex items-center justify-center shadow-sm">
                          <Icon className="w-5 h-5 text-white" />
                        </div>
                        {i < QUICK_START_STEPS.length - 1 && (
                          <div className="w-0.5 flex-1 bg-border-primary min-h-[24px]" />
                        )}
                      </div>
                      <div className="flex-1 pb-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs font-bold text-text-tertiary">STEP {step.number}</span>
                        </div>
                        <h3 className="font-semibold text-text-primary mb-1">{step.title}</h3>
                        <p className="text-sm text-text-secondary leading-relaxed">{step.desc}</p>
                        <Link
                          href={step.href}
                          className="inline-flex items-center gap-1 mt-2 text-xs text-accent-primary hover:underline"
                        >
                          Go there <ArrowRight className="w-3 h-3" />
                        </Link>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>
          )}

          {/* PAGE GUIDE */}
          {activeSection === "pages" && (
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-text-primary">Page-by-Page Guide</h2>
                <p className="text-text-secondary mt-1">Click any page to expand detailed instructions and pro tips.</p>
              </div>

              <div className="space-y-3">
                {PAGE_GUIDES.map((guide) => (
                  <AccordionItem key={guide.path} guide={guide} />
                ))}
              </div>
            </motion.div>
          )}

          {/* GETTING MAX RESULTS */}
          {activeSection === "max-results" && (
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-text-primary">Getting Max Results</h2>
                <p className="text-text-secondary mt-1">Strategies to maximize reliability, speed, and free-tier usage.</p>
              </div>

              <div className="space-y-4">
                {[
                  {
                    title: "Stack providers by priority + weight",
                    icon: Star,
                    color: "text-yellow-400",
                    content: (
                      <div className="space-y-2 text-sm text-text-secondary">
                        <p>Set <span className="font-mono text-accent-primary">priority</span> (1 = try first) and <span className="font-mono text-accent-primary">weight</span> (higher = more traffic share) on each provider. Recommended stack for free tier:</p>
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-3">
                          {[
                            { priority: 1, name: "Groq", reason: "Fastest (LPU), ~14K req/day" },
                            { priority: 2, name: "Google AI Studio", reason: "1M context, generous limits" },
                            { priority: 3, name: "OpenRouter", reason: "Auto-routes to any free model" },
                          ].map((p) => (
                            <div key={p.name} className="p-3 rounded-lg border border-border-primary bg-bg-elevated">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="text-xs bg-accent-primary/20 text-accent-primary px-1.5 py-0.5 rounded font-bold">P{p.priority}</span>
                                <span className="font-medium text-text-primary text-sm">{p.name}</span>
                              </div>
                              <p className="text-xs text-text-tertiary">{p.reason}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    ),
                  },
                  {
                    title: "Use context window limits to prevent rate limit hits",
                    icon: AlertTriangle,
                    color: "text-orange-400",
                    content: (
                      <p className="text-sm text-text-secondary">
                        Set each model&apos;s context window to the actual limit (e.g., 131072 for Groq models). The gateway rejects oversized requests before sending them — saving your rate limit quota for real traffic. For Cloudflare Workers AI, keep it at 8192 to stay within neuron budget.
                      </p>
                    ),
                  },
                  {
                    title: "Use task-type routing for specialized models",
                    icon: Zap,
                    color: "text-blue-400",
                    content: (
                      <div className="text-sm text-text-secondary space-y-2">
                        <p>When creating a Gateway Key, set <span className="font-mono text-accent-primary">task_type</span> to route to specialized models:</p>
                        <ul className="space-y-1 ml-4 list-disc text-xs">
                          <li><span className="font-mono text-accent-primary">code</span> → routes to Codestral, Qwen Coder, or Devstral</li>
                          <li><span className="font-mono text-accent-primary">reasoning</span> → routes to DeepSeek R1, Qwen3-32b</li>
                          <li><span className="font-mono text-accent-primary">chat</span> → routes to general models like Llama 70B</li>
                          <li><span className="font-mono text-accent-primary">embedding</span> → routes to text-embedding-004</li>
                        </ul>
                      </div>
                    ),
                  },
                  {
                    title: "Avoid PREVIEW models in production",
                    icon: AlertTriangle,
                    color: "text-red-400",
                    content: (
                      <div className="text-sm text-text-secondary space-y-2">
                        <p>Models marked <span className="px-1.5 py-0.5 rounded bg-yellow-500/10 text-yellow-400 border border-yellow-500/20 text-xs font-medium">PREVIEW</span> can be removed by providers at any time with no notice. Examples:</p>
                        <ul className="space-y-1 ml-4 list-disc text-xs">
                          <li>Groq: <span className="font-mono">llama-4-scout-17b</span>, <span className="font-mono">qwen/qwen3-32b</span></li>
                          <li>Cerebras: <span className="font-mono">gemma-4-31b</span>, <span className="font-mono">zai-glm-4.7</span></li>
                          <li>OpenRouter: <span className="font-mono">nvidia/nemotron-3-ultra:free</span></li>
                        </ul>
                        <p>Toggle these OFF in the Models page for production gateway keys, and use them only in your dev/staging projects.</p>
                      </div>
                    ),
                  },
                  {
                    title: "Multiple API keys per provider for higher throughput",
                    icon: Key,
                    color: "text-emerald-400",
                    content: (
                      <p className="text-sm text-text-secondary">
                        You can add multiple API keys for the same provider in Provider Credentials. Dronzer load-balances across them automatically. For example, add 3 Groq keys from 3 different free accounts → effectively triple your rate limit.
                      </p>
                    ),
                  },
                ].map((item) => {
                  const Icon = item.icon;
                  return (
                    <div key={item.title} className="rounded-xl border border-border-primary bg-bg-elevated p-5 space-y-3">
                      <div className="flex items-center gap-2">
                        <Icon className={cn("w-4 h-4", item.color)} />
                        <h3 className="font-semibold text-text-primary">{item.title}</h3>
                      </div>
                      {item.content}
                    </div>
                  );
                })}
              </div>
            </motion.div>
          )}

          {/* API USAGE */}
          {activeSection === "api" && (
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-text-primary">API Usage</h2>
                <p className="text-text-secondary mt-1">Dronzer is 100% OpenAI SDK-compatible. Drop it in as a replacement.</p>
              </div>

              <div className="space-y-5">
                <div className="p-4 rounded-xl border border-accent-primary/20 bg-accent-muted flex gap-3">
                  <Info className="w-4 h-4 text-accent-primary shrink-0 mt-0.5" />
                  <div className="text-sm text-text-secondary">
                    <strong className="text-text-primary">Base URL:</strong>{" "}
                    <span className="font-mono text-accent-primary">http://localhost:8000/v1</span>
                    {" "}(or your deployed gateway URL). Use your <strong className="text-text-primary">Gateway Key</strong> as the Bearer token.
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold text-text-primary mb-1">Python (OpenAI SDK)</h3>
                  <CodeBlock language="python" code={`from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="your-gateway-key-here",  # from Gateway Keys page
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",   # any registered model
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)`} />
                </div>

                <div>
                  <h3 className="font-semibold text-text-primary mb-1">JavaScript / TypeScript</h3>
                  <CodeBlock language="typescript" code={`import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:8000/v1",
  apiKey: "your-gateway-key-here",
});

const response = await client.chat.completions.create({
  model: "gemini-2.5-flash",
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(response.choices[0].message.content);`} />
                </div>

                <div>
                  <h3 className="font-semibold text-text-primary mb-1">cURL</h3>
                  <CodeBlock language="bash" code={`curl http://localhost:8000/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer your-gateway-key-here" \\
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'`} />
                </div>

                <div>
                  <h3 className="font-semibold text-text-primary mb-1">Streaming</h3>
                  <CodeBlock language="python" code={`stream = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Write a poem"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")`} />
                </div>

                <div>
                  <h3 className="font-semibold text-text-primary mb-1">List available models</h3>
                  <CodeBlock language="bash" code={`curl http://localhost:8000/v1/models \\
  -H "Authorization: Bearer your-gateway-key-here"`} />
                </div>
              </div>
            </motion.div>
          )}

          {/* FREE MODEL REFERENCE */}
          {activeSection === "free-models" && (
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-text-primary">Free Model Reference</h2>
                <p className="text-text-secondary mt-1">
                  All {TOTAL_MODEL_COUNT} free models across {TOTAL_PROVIDER_COUNT} providers, verified July 2026. Searchable.
                </p>
              </div>

              <div className="p-3 rounded-lg border border-yellow-500/20 bg-yellow-500/5 flex gap-2">
                <AlertTriangle className="w-4 h-4 text-yellow-400 shrink-0 mt-0.5" />
                <p className="text-xs text-yellow-300/90">
                  Rate limits and availability change frequently. Always verify against official provider docs before depending on them in production.
                </p>
              </div>

              <FreeProviderTable />

              {/* Provider summary cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {FREE_PROVIDERS.map((p) => {
                  const colors = PROVIDER_COLORS[p.color];
                  const stableCount = p.models.filter((m) => !m.isPreview).length;
                  return (
                    <div key={p.slug} className={cn("rounded-xl border p-4 space-y-2", colors.border, colors.bg)}>
                      <div className="flex items-center gap-2">
                        <span className={cn("text-sm font-bold", colors.text)}>{p.provider}</span>
                      </div>
                      <p className="text-xs text-text-tertiary leading-relaxed">{p.description}</p>
                      <div className="flex gap-3 text-xs">
                        <span className="text-text-secondary"><strong className="text-text-primary">{stableCount}</strong> stable</span>
                        {p.models.length - stableCount > 0 && (
                          <span className="text-yellow-400"><strong>{p.models.length - stableCount}</strong> preview</span>
                        )}
                      </div>
                      <a
                        href={`https://${p.baseUrl.split("/")[2]}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={cn("inline-flex items-center gap-1 text-xs hover:underline", colors.text)}
                      >
                        Provider docs <ExternalLink className="w-3 h-3" />
                      </a>
                    </div>
                  );
                })}
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
