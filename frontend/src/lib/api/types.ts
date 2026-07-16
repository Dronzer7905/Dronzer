// ============================================================
// Dronzer AI Gateway — API Type Definitions
// All interfaces match the actual backend schemas exactly.
// ============================================================

// ── Auth ─────────────────────────────────────────────────────

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface RefreshRequest {
  refresh_token: string;
}

export interface SetupRequest {
  email: string;
  password: string;
}

export interface SetupStatusResponse {
  is_setup: boolean;
}

/** Decoded JWT payload from the backend */
export interface TokenPayload {
  sub: string;   // user email
  role: string;  // e.g. "SUPER_ADMIN"
  exp: number;   // unix timestamp
  type: "access" | "refresh";
}

// ── Organizations ────────────────────────────────────────────

export interface OrganizationCreate {
  name: string;
  billing_email?: string;
}

export interface OrganizationResponse {
  id: string;
  name: string;
  billing_email?: string;
  created_at: string;
  is_active: boolean;
}

// ── Projects ─────────────────────────────────────────────────

export interface ProjectCreate {
  name: string;
  org_id: string;
  environment?: "production" | "staging" | "development";
}

export interface ProjectResponse {
  id: string;
  name: string;
  org_id: string;
  environment: string;
  created_at: string;
}

// ── Providers ────────────────────────────────────────────────

export interface ProviderCreate {
  name: string;
  priority?: number;
  weight?: number;
  models?: string[];
}

export interface ProviderConfigResponse {
  id: string;
  name: string;
  is_enabled: boolean;
  priority: number;
  weight: number;
  models: string[];
}

export interface ProviderToggleResponse {
  status: string;
  provider_id: string;
}

// ── Models ───────────────────────────────────────────────────

export interface ModelCapabilities {
  // Capability flags (from CSV analysis)
  chat?: boolean;
  code?: boolean;
  vision?: boolean;
  reasoning?: boolean;
  embedding?: boolean;
  agentic?: boolean;
  json_mode?: boolean;
  // CSV metadata fields
  is_preview?: boolean;
  rate_limit?: string;
  daily_cap?: string;
  notes?: string;
  verified_against?: string;
  // Allow any additional fields
  [key: string]: boolean | string | undefined;
}

export interface ModelConfigResponse {
  id: string;
  provider_id: string;
  name: string;
  is_enabled: boolean;
  context_window: number;
  capabilities: ModelCapabilities;
}

export interface ModelCreate {
  name: string;
  provider_id: string;
  context_window?: number;
}

export interface ModelUpdateParams {
  is_enabled?: boolean;
  context_window?: number;
}

// ── API Keys ─────────────────────────────────────────────────

export interface APIKeyCreate {
  provider_id: string;
  project_id: string;
  key_value: string;
  label?: string;
}

export interface APIKeyResponse {
  id: string;
  provider_id: string;
  project_id: string;
  label: string;
  is_active: boolean;
  is_failing: boolean;
}

// ── Gateway Keys ───────────────────────────────────────────────

export interface GatewayKeyCreate {
  label: string;
  organization_id: string;
  project_id?: string;
  task_type?: string;
  model_priorities?: string[];
  provider_priorities?: string[];
}

export interface GatewayKeyResponse {
  id: string;
  key_value?: string;
  label: string;
  organization_id: string;
  project_id?: string;
  task_type: string;
  model_priorities: string[];
  provider_priorities: string[];
  is_active: boolean;
  created_at: string;
}

// ── Plugins ──────────────────────────────────────────────────

export interface PluginResponse {
  name: string;
  version: string;
  author: string;
  description: string;
}

export interface PluginReloadResponse {
  status: string;
  message: string;
}

// ── Health ───────────────────────────────────────────────────

export interface HealthMetrics {
  active_requests: number;
  circuit_breakers_open: number;
  circuit_breakers_half_open: number;
  token_usage_total: number;
  cache_hit_rate: number;
  timeseries?: unknown[];
}

export interface HealthDiagnostics {
  database: string;
  redis: string;
  providers_loaded: number;
  plugins_loaded: number;
  uptime_seconds: number;
}

export interface LivenessResponse {
  status: string;
}

export interface ReadinessResponse {
  status: string;
}

// ── Chat (OpenAI-compatible) ─────────────────────────────────

export interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface ChatCompletionRequest {
  model: string;
  messages: ChatMessage[];
  temperature?: number;
  max_tokens?: number;
  stream?: boolean;
  top_p?: number;
  frequency_penalty?: number;
  presence_penalty?: number;
}

export interface ChatChoice {
  index: number;
  message: ChatMessage;
  finish_reason: string | null;
}

export interface ChatUsage {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

export interface ChatCompletionResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: ChatChoice[];
  usage?: ChatUsage;
}

/** Streaming chunk delta */
export interface ChatCompletionChunk {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: {
    index: number;
    delta: { role?: string; content?: string };
    finish_reason: string | null;
  }[];
}

// ── Gateway Models ───────────────────────────────────────────

export interface ModelCard {
  id: string;
  object: string;
  created: number;
  owned_by: string;
}

export interface ModelListResponse {
  object: string;
  data: ModelCard[];
}

// ── Errors ───────────────────────────────────────────────────

export interface ApiErrorDetail {
  message: string;
  type: string;
  param?: string;
  code?: string;
}

export interface ApiError {
  error: ApiErrorDetail;
}

// Also support the simpler { detail: "..." } format used by some endpoints
export interface SimpleError {
  detail: string;
}
