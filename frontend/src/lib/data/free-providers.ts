// ============================================================
// Dronzer AI Gateway — Free LLM Providers Data
// Generated from: Free_LLM_Providers_Verified_Jul2026.csv
// Verified: July 2026
// ============================================================

export interface FreeModelEntry {
  modelId: string;
  contextWindow: number;
  rateLimitNote: string;
  dailyCap: string;
  notes: string;
  isPreview: boolean;
  verifiedAgainst: string;
}

export interface FreeProviderData {
  provider: string;
  /** Slug used as the provider name when creating via API */
  slug: string;
  /** Base URL for the provider's API (informational) */
  baseUrl: string;
  /** Short description of the provider */
  description: string;
  /** Color class for UI (tailwind) */
  color: string;
  models: FreeModelEntry[];
}

// ---------------------------------------------------------------------------
// Provider Data — sourced directly from the CSV
// ---------------------------------------------------------------------------

export const FREE_PROVIDERS: FreeProviderData[] = [
  {
    provider: "Groq",
    slug: "groq",
    baseUrl: "https://api.groq.com/openai/v1",
    description: "LPU-based inference. Fastest small/large models on free tier. No credits system.",
    color: "orange",
    models: [
      {
        modelId: "llama-3.1-8b-instant",
        contextWindow: 131072,
        rateLimitNote: "~30 RPM / ~6000 TPM (default free tier)",
        dailyCap: "~14400 requests/day",
        notes: "Fastest small model on LPU hardware; genuinely free (not trial) - no credits system",
        isPreview: false,
        verifiedAgainst: "console.groq.com/docs/models (Jul 2026)",
      },
      {
        modelId: "llama-3.3-70b-versatile",
        contextWindow: 131072,
        rateLimitNote: "~30 RPM / ~6000 TPM (default)",
        dailyCap: "~1000 requests/day",
        notes: "Best general-purpose free model on Groq",
        isPreview: false,
        verifiedAgainst: "console.groq.com/docs/models (Jul 2026)",
      },
      {
        modelId: "openai/gpt-oss-120b",
        contextWindow: 131072,
        rateLimitNote: "~30 RPM / ~6000 TPM (default)",
        dailyCap: "~1000 requests/day",
        notes: "OpenAI's open-weight flagship; built-in browser search + code execution",
        isPreview: false,
        verifiedAgainst: "console.groq.com/docs/models (Jul 2026)",
      },
      {
        modelId: "openai/gpt-oss-20b",
        contextWindow: 131072,
        rateLimitNote: "~30 RPM / ~6000 TPM (default)",
        dailyCap: "~1000 requests/day",
        notes: "Smaller/faster GPT-OSS variant (~1000 tok/sec)",
        isPreview: false,
        verifiedAgainst: "console.groq.com/docs/models (Jul 2026)",
      },
      {
        modelId: "groq/compound",
        contextWindow: 131072,
        rateLimitNote: "200 RPM / 200K TPM",
        dailyCap: "N/A",
        notes: "Agentic system with built-in web search + code execution tools",
        isPreview: false,
        verifiedAgainst: "console.groq.com/docs/models (Jul 2026)",
      },
      {
        modelId: "groq/compound-mini",
        contextWindow: 131072,
        rateLimitNote: "200 RPM / 200K TPM",
        dailyCap: "N/A",
        notes: "Lighter agentic system variant",
        isPreview: false,
        verifiedAgainst: "console.groq.com/docs/models (Jul 2026)",
      },
      {
        modelId: "meta-llama/llama-4-scout-17b-16e-instruct",
        contextWindow: 131072,
        rateLimitNote: "Preview tier - lower/variable RPM",
        dailyCap: "N/A",
        notes: "PREVIEW - evaluation only; can be pulled with no notice",
        isPreview: true,
        verifiedAgainst: "console.groq.com/docs/models (Jul 2026)",
      },
      {
        modelId: "qwen/qwen3-32b",
        contextWindow: 131072,
        rateLimitNote: "Preview tier - lower/variable RPM",
        dailyCap: "N/A",
        notes: "PREVIEW - reasoning model; evaluation only",
        isPreview: true,
        verifiedAgainst: "console.groq.com/docs/models (Jul 2026)",
      },
    ],
  },

  {
    provider: "Google AI Studio",
    slug: "google-ai-studio",
    baseUrl: "https://generativelanguage.googleapis.com/v1beta/openai",
    description: "Gemini family models. Best all-round free models with 1M token context.",
    color: "blue",
    models: [
      {
        modelId: "gemini-2.5-flash",
        contextWindow: 1000000,
        rateLimitNote: "~10-15 RPM",
        dailyCap: "~250-1500 RPD (model-dependent)",
        notes: "Best all-round free model available today; multimodal",
        isPreview: false,
        verifiedAgainst: "ai.google.dev/gemini-api/docs/pricing (Jul 2026)",
      },
      {
        modelId: "gemini-2.5-flash-lite",
        contextWindow: 1000000,
        rateLimitNote: "~15 RPM",
        dailyCap: "~1000-1500 RPD",
        notes: "Lightweight/cheapest-quota variant",
        isPreview: false,
        verifiedAgainst: "ai.google.dev/gemini-api/docs/pricing (Jul 2026)",
      },
      {
        modelId: "gemini-3-flash",
        contextWindow: 1000000,
        rateLimitNote: "~10 RPM",
        dailyCap: "Lower RPD than 2.5 (newer model)",
        notes: "Latest flagship-speed model; check current GA status before depending on it",
        isPreview: false,
        verifiedAgainst: "ai.google.dev/gemini-api/docs/pricing (Jul 2026)",
      },
      {
        modelId: "gemini-3.1-flash-lite",
        contextWindow: 1000000,
        rateLimitNote: "~15 RPM",
        dailyCap: "Higher RPD (most generous)",
        notes: "GA since May 2026",
        isPreview: false,
        verifiedAgainst: "ai.google.dev/gemini-api/docs/pricing (Jul 2026)",
      },
      {
        modelId: "text-embedding-004",
        contextWindow: 8000,
        rateLimitNote: "Free on free tier",
        dailyCap: "N/A",
        notes: "Embeddings model - useful for RAG pipelines",
        isPreview: false,
        verifiedAgainst: "ai.google.dev/gemini-api/docs/pricing (Jul 2026)",
      },
    ],
  },

  {
    provider: "Mistral",
    slug: "mistral",
    baseUrl: "https://api.mistral.ai/v1",
    description: "Free Experiment mode. Phone verification required. Low RPS but no monthly cap.",
    color: "purple",
    models: [
      {
        modelId: "mistral-small-latest",
        contextWindow: 32000,
        rateLimitNote: "Free Experiment mode - low RPS (~1-2 RPS)",
        dailyCap: "Rate-limited (no fixed monthly cap)",
        notes: "Free MODE — console defaults every new key to Free mode. Phone verification required.",
        isPreview: false,
        verifiedAgainst: "docs.mistral.ai (Jul 2026)",
      },
      {
        modelId: "mistral-medium-latest",
        contextWindow: 32000,
        rateLimitNote: "Free Experiment mode - same low RPS",
        dailyCap: "Rate-limited",
        notes: "Runs on same $0 Free mode as Small",
        isPreview: false,
        verifiedAgainst: "docs.mistral.ai (Jul 2026)",
      },
      {
        modelId: "codestral-latest",
        contextWindow: 32000,
        rateLimitNote: "Free Experiment mode - same low RPS",
        dailyCap: "Rate-limited",
        notes: "Coding-specialist model still included under Free mode",
        isPreview: false,
        verifiedAgainst: "docs.mistral.ai (Jul 2026)",
      },
      {
        modelId: "devstral-small-latest",
        contextWindow: 32000,
        rateLimitNote: "Free Experiment mode - same low RPS",
        dailyCap: "Rate-limited",
        notes: "Lightweight open coding-agent model",
        isPreview: false,
        verifiedAgainst: "docs.mistral.ai (Jul 2026)",
      },
      {
        modelId: "labs-leanstral-2603",
        contextWindow: 32000,
        rateLimitNote: "Explicitly $0 / Free (no Experiment-mode gating)",
        dailyCap: "Kept open for a limited period",
        notes: "Lean 4 formal-proof coding agent - niche, not general chat",
        isPreview: false,
        verifiedAgainst: "mistral.ai/pricing/api (Jul 2026)",
      },
    ],
  },

  {
    provider: "Cerebras",
    slug: "cerebras",
    baseUrl: "https://api.cerebras.ai/v1",
    description: "Ultra-fast wafer-scale inference. 1M tokens/day free. Small but growing model catalog.",
    color: "green",
    models: [
      {
        modelId: "gpt-oss-120b",
        contextWindow: 8192,
        rateLimitNote: "~30 RPM",
        dailyCap: "1,000,000 tokens/day",
        notes: "Only PRODUCTION model on Cerebras' public free endpoint right now",
        isPreview: false,
        verifiedAgainst: "inference-docs.cerebras.ai/models/overview (Jul 2026)",
      },
      {
        modelId: "gemma-4-31b",
        contextWindow: 8192,
        rateLimitNote: "~30 RPM",
        dailyCap: "1,000,000 tokens/day",
        notes: "PREVIEW model - eval only - can vanish with no notice",
        isPreview: true,
        verifiedAgainst: "inference-docs.cerebras.ai/models/overview (Jul 2026)",
      },
      {
        modelId: "zai-glm-4.7",
        contextWindow: 8192,
        rateLimitNote: "~30 RPM",
        dailyCap: "1,000,000 tokens/day",
        notes: "PREVIEW model",
        isPreview: true,
        verifiedAgainst: "inference-docs.cerebras.ai/models/overview (Jul 2026)",
      },
    ],
  },

  {
    provider: "Cloudflare Workers AI",
    slug: "cloudflare-workers-ai",
    baseUrl: "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1",
    description: "Edge inference via Cloudflare Workers. 10K neurons/day shared across all models (~15-25 calls/day).",
    color: "yellow",
    models: [
      {
        modelId: "@cf/meta/llama-3.1-8b-instruct",
        contextWindow: 8192,
        rateLimitNote: "Shared 10K neuron/day pool",
        dailyCap: "10,000 neurons/day (shared across ALL models)",
        notes: "Neurons are shared across every model you call in a day - not per-model",
        isPreview: false,
        verifiedAgainst: "developers.cloudflare.com/workers-ai (Jul 2026)",
      },
      {
        modelId: "@cf/meta/llama-3.2-3b-instruct",
        contextWindow: 8192,
        rateLimitNote: "Shared 10K neuron/day pool",
        dailyCap: "Shared pool",
        notes: "Cheaper-per-call than the 8B model",
        isPreview: false,
        verifiedAgainst: "developers.cloudflare.com/workers-ai (Jul 2026)",
      },
      {
        modelId: "@cf/mistral/mistral-7b-instruct-v0.2",
        contextWindow: 8192,
        rateLimitNote: "Shared 10K neuron/day pool",
        dailyCap: "Shared pool",
        notes: "Small efficient model",
        isPreview: false,
        verifiedAgainst: "developers.cloudflare.com/workers-ai (Jul 2026)",
      },
      {
        modelId: "@cf/qwen/qwen2.5-7b-instruct",
        contextWindow: 8192,
        rateLimitNote: "Shared 10K neuron/day pool",
        dailyCap: "Shared pool",
        notes: "Small Alibaba model",
        isPreview: false,
        verifiedAgainst: "developers.cloudflare.com/workers-ai (Jul 2026)",
      },
      {
        modelId: "@cf/google/gemma-3-12b-it",
        contextWindow: 8192,
        rateLimitNote: "Shared 10K neuron/day pool",
        dailyCap: "Shared pool",
        notes: "Google open model",
        isPreview: false,
        verifiedAgainst: "developers.cloudflare.com/workers-ai (Jul 2026)",
      },
      {
        modelId: "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b",
        contextWindow: 8192,
        rateLimitNote: "Shared 10K neuron/day pool",
        dailyCap: "Shared pool",
        notes: "Reasoning-distilled model",
        isPreview: false,
        verifiedAgainst: "developers.cloudflare.com/workers-ai (Jul 2026)",
      },
    ],
  },

  {
    provider: "OpenRouter",
    slug: "openrouter",
    baseUrl: "https://openrouter.ai/api/v1",
    description: "Model aggregator. 20 RPM free; 50/day without funding, 1000/day after $10 one-time top-up.",
    color: "pink",
    models: [
      {
        modelId: "qwen/qwen3-coder:free",
        contextWindow: 262144,
        rateLimitNote: "20 RPM",
        dailyCap: "50/day (unfunded) or 1000/day (after $10 top-up)",
        notes: "Strongest free coding model on OpenRouter right now",
        isPreview: false,
        verifiedAgainst: "openrouter.ai/docs (Jul 2026)",
      },
      {
        modelId: "deepseek/deepseek-r1:free",
        contextWindow: 1000000,
        rateLimitNote: "20 RPM",
        dailyCap: "50/day or 1000/day",
        notes: "Reasoning model",
        isPreview: false,
        verifiedAgainst: "openrouter.ai (Jul 2026)",
      },
      {
        modelId: "deepseek/deepseek-chat-v3.1:free",
        contextWindow: 1000000,
        rateLimitNote: "20 RPM",
        dailyCap: "50/day or 1000/day",
        notes: "General flagship-class chat",
        isPreview: false,
        verifiedAgainst: "openrouter.ai (Jul 2026)",
      },
      {
        modelId: "meta-llama/llama-3.3-70b-instruct:free",
        contextWindow: 8192,
        rateLimitNote: "20 RPM",
        dailyCap: "50/day or 1000/day",
        notes: "Solid general-purpose free model",
        isPreview: false,
        verifiedAgainst: "openrouter.ai (Jul 2026)",
      },
      {
        modelId: "meta-llama/llama-4-maverick:free",
        contextWindow: 128000,
        rateLimitNote: "20 RPM",
        dailyCap: "50/day or 1000/day",
        notes: "Meta's 400B MoE flagship (17B active) - multimodal",
        isPreview: false,
        verifiedAgainst: "openrouter.ai (Jul 2026)",
      },
      {
        modelId: "openai/gpt-oss-120b:free",
        contextWindow: 131072,
        rateLimitNote: "20 RPM",
        dailyCap: "50/day or 1000/day",
        notes: "OpenAI open-weight model",
        isPreview: false,
        verifiedAgainst: "openrouter.ai (Jul 2026)",
      },
      {
        modelId: "openai/gpt-oss-20b:free",
        contextWindow: 131072,
        rateLimitNote: "20 RPM",
        dailyCap: "50/day or 1000/day",
        notes: "Smaller GPT-OSS variant",
        isPreview: false,
        verifiedAgainst: "openrouter.ai (Jul 2026)",
      },
      {
        modelId: "z-ai/glm-4.5-air:free",
        contextWindow: 128000,
        rateLimitNote: "20 RPM",
        dailyCap: "50/day or 1000/day",
        notes: "Zhipu GLM lightweight variant",
        isPreview: false,
        verifiedAgainst: "openrouter.ai (Jul 2026)",
      },
      {
        modelId: "nvidia/nemotron-3-ultra:free",
        contextWindow: 1000000,
        rateLimitNote: "20 RPM",
        dailyCap: "50/day or 1000/day",
        notes: "1M-context agent tasks while promo lasts - NVIDIA has pulled free Nemotron models before",
        isPreview: true,
        verifiedAgainst: "openrouter.ai (Jul 2026)",
      },
      {
        modelId: "openrouter/free",
        contextWindow: 131072,
        rateLimitNote: "20 RPM",
        dailyCap: "50/day or 1000/day",
        notes: "Auto-router — picks a working free model for you so your code keeps running",
        isPreview: false,
        verifiedAgainst: "openrouter.ai/docs/guides/routing/model-variants/free",
      },
    ],
  },

  {
    provider: "NVIDIA NIM",
    slug: "nvidia-nim",
    baseUrl: "https://integrate.api.nvidia.com/v1",
    description: "NVIDIA-hosted inference. ~40 RPM account-level. No fixed daily cap on base catalog.",
    color: "teal",
    models: [
      {
        modelId: "meta/llama-3.3-70b-instruct",
        contextWindow: 8192,
        rateLimitNote: "~40 RPM (account-level)",
        dailyCap: "No fixed daily cap published",
        notes: "CAVEAT: verify current behavior on your account — some report depleting credit pools",
        isPreview: false,
        verifiedAgainst: "build.nvidia.com (Jul 2026)",
      },
      {
        modelId: "deepseek-ai/deepseek-r1",
        contextWindow: 128000,
        rateLimitNote: "~40 RPM",
        dailyCap: "No fixed daily cap published",
        notes: "Reasoning model; larger models may be more rate-limited in practice",
        isPreview: false,
        verifiedAgainst: "build.nvidia.com (Jul 2026)",
      },
      {
        modelId: "qwen/qwen3-coder-480b-a35b-instruct",
        contextWindow: 262144,
        rateLimitNote: "~40 RPM",
        dailyCap: "No fixed daily cap published",
        notes: "Agentic coding model",
        isPreview: false,
        verifiedAgainst: "build.nvidia.com (Jul 2026)",
      },
      {
        modelId: "google/gemma-3-27b-it",
        contextWindow: 8192,
        rateLimitNote: "~40 RPM",
        dailyCap: "No fixed daily cap published",
        notes: "Google open model on NVIDIA infra",
        isPreview: false,
        verifiedAgainst: "build.nvidia.com (Jul 2026)",
      },
      {
        modelId: "nvidia/nemotron-mini-4b-instruct",
        contextWindow: 4096,
        rateLimitNote: "~40 RPM",
        dailyCap: "No fixed daily cap published",
        notes: "NVIDIA's own small model - most reliably free-tier per multiple trackers",
        isPreview: false,
        verifiedAgainst: "build.nvidia.com (Jul 2026)",
      },
      {
        modelId: "mistralai/mistral-large-3",
        contextWindow: 32000,
        rateLimitNote: "~40 RPM",
        dailyCap: "No fixed daily cap published",
        notes: "Mistral's flagship hosted free via NVIDIA - different access path than Mistral's own throttled Free mode",
        isPreview: false,
        verifiedAgainst: "build.nvidia.com (Jul 2026)",
      },
    ],
  },
];

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Get a provider entry by slug */
export const getProviderBySlug = (slug: string): FreeProviderData | undefined =>
  FREE_PROVIDERS.find((p) => p.slug === slug);

/** Total model count across all providers */
export const TOTAL_MODEL_COUNT = FREE_PROVIDERS.reduce((acc, p) => acc + p.models.length, 0);

/** Total provider count */
export const TOTAL_PROVIDER_COUNT = FREE_PROVIDERS.length;

/** Color map for provider badges */
export const PROVIDER_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  orange:  { bg: "bg-orange-500/10",  text: "text-orange-400",  border: "border-orange-500/20" },
  blue:    { bg: "bg-blue-500/10",    text: "text-blue-400",    border: "border-blue-500/20" },
  purple:  { bg: "bg-purple-500/10",  text: "text-purple-400",  border: "border-purple-500/20" },
  green:   { bg: "bg-emerald-500/10", text: "text-emerald-400", border: "border-emerald-500/20" },
  yellow:  { bg: "bg-yellow-500/10",  text: "text-yellow-400",  border: "border-yellow-500/20" },
  pink:    { bg: "bg-pink-500/10",    text: "text-pink-400",    border: "border-pink-500/20" },
  teal:    { bg: "bg-teal-500/10",    text: "text-teal-400",    border: "border-teal-500/20" },
};
