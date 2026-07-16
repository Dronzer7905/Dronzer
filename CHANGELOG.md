# Changelog

All notable changes to the Dronzer AI Gateway are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] — 2026-07-15

### Added

- **Decision Intelligence Engine:** Built `DecisionIntelligenceEngine` to analyze tasks (`coding`, `reasoning`, `vision`, `general`) and dynamically route requests to the optimal model architecture. Routing decisions generate a full auditable JSON trace.
- **Resilient Failover Stack:** Introduced a 3-tier resilience stack — `HealthEngine` → `CircuitBreaker` → `RetryEngine`. Transparently masks provider `429` and `5xx` errors from consumers.
- **Provider Registry (44+ Models):** Integrated 44+ free and premium models across the following providers:
  - **Groq** — Llama 3.1/3.3, Qwen3-32B, Llama-4-Scout, GPT-OSS-120B/20B, Compound
  - **Google AI Studio** — Gemini 2.5 Flash, Gemini 2.5 Flash Lite, Gemini 3 Flash, Gemini 3.1 Flash Lite
  - **Cerebras** — Llama 3.1 8B/70B, Llama 4 Scout/Maverick, Qwen 3-32B
  - **Mistral** — Mistral Small/Medium, Pixtral 12B, Devstral Small
  - **Cohere** — Command A, Command R7B
  - **OpenRouter** — Multiple free-tier models
  - **Fireworks AI** — Llama 4 Scout/Maverick, DeepSeek R2
  - **Together AI** — Llama 3.3 Turbo, DeepSeek V3/R1
  - **Novita AI** — Llama 3.1 8B/70B, Phi-4
  - **Nebius AI Studio** — Llama 3.3 70B, DeepSeek V3
- **Seed Scripts:** Added `seed_free_providers.py` and `patch_model_metadata.py` for repeatable, idempotent database population (safe to re-run on existing data).
- **Admin Dashboard:** Built a minimal, polished **Light Theme** Next.js dashboard for API Key generation, budget management, and provider health monitoring.
- **OpenAI API Compliance:** Fully compatible with the standard OpenAI API at `/v1/chat/completions` for instant drop-in replacement in any app or IDE.
- **Plugin System:** Dynamic plugin loader at runtime. Plugins receive sandboxed facades for logging and cache access; high-risk capabilities require explicit administrator approval.
- **API Key Rotation Engine:** Intelligent key selection via LRU, Priority, and Weighted strategies with health-based scoring (latency, 5xx rate, 429 frequency).
- **Multi-Tenant RBAC:** Organization → Project → Key hierarchy with strict isolation. No key can access data across organizations.
- **Prometheus Metrics:** Exposed at `/metrics` for integration with Grafana dashboards.

### Changed

- Refactored the entire FastAPI backend to a **Clean Architecture** pattern (Domain → Application → Infrastructure → Presentation).
- Replaced raw DB calls with an async SQLAlchemy 2.0 session factory.
- Overhauled frontend aesthetic from v1 dark theme to a refined **Light Theme** design system.
- API versioning formalized under `/v1/` prefix for the gateway API; management API under `/api/v1/`.

### Removed

- Deprecated v1 local SQLite database support in favor of a robust async **PostgreSQL 15+** architecture.
- Removed global environment variable loading for provider API keys (`OPENAI_API_KEY`, etc.) — keys are now managed per-Organization in the encrypted database.

---

## [1.0.0] — 2026-01-10

### Added

- Initial release of the Dronzer AI Gateway.
- Basic OpenAI proxy with SQLite storage.
- Single-provider API key management.
- Rudimentary failover to a secondary provider on hard errors.
