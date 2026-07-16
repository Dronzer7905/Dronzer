# System Architecture — Dronzer AI Gateway

**Document Status:** ✅ Approved
**Version:** 2.0
**Last Updated:** July 2026

---

## Overview

Dronzer is engineered as a **universal AI reverse proxy** sitting between client applications and all LLM providers. It is designed so that clients never communicate with an LLM provider directly — instead, every request passes through Dronzer's intelligent routing, security, and observability stack.

**Architecture Styles Applied:**
- Clean Architecture (Domain → Application → Infrastructure → Presentation)
- Hexagonal Architecture (Ports & Adapters)
- Event-Driven (cross-cutting concerns via internal event bus)
- Reverse Proxy pattern (transparent to OpenAI-compatible clients)

---

## Resolved Architectural Decisions (ADRs)

| Decision | Resolution |
|---|---|
| Multi-worker cache consistency | Accept 60-second eventual consistency. Recommend single worker for v1 deployments. |
| Health data granularity | Provider + Model + Key level (maximum granularity) |
| Audit log storage | Same PostgreSQL database with 90-day retention policy |
| Plugin distribution | `pip` packages (primary) + single-file drop-in to `/plugins/` (alternative) |
| Consumer key hashing | HMAC-SHA256 with master `SECRET_KEY` for fast O(1) validation |
| API versioning | URL path (`/api/v1/`) for management API; OpenAI-native path for gateway API |
| Health endpoint | Simple `/health` (200/503) + `/health/detailed` (admin auth required) |
| Default routing strategy | Priority-based routing |
| Database | PostgreSQL 15+ (production); SQLite removed in v2.0 |
| License | Apache 2.0 |

---

## Architecture Summary

| Attribute | Value |
|---|---|
| **Style** | Clean Architecture + Hexagonal + Event-Driven + Reverse Proxy |
| **Process Model** | Single process (Gateway + Management API unified) |
| **Subsystems** | 25 subsystems across 4 tiers |
| **Communication** | Direct calls (hot path), Event bus (cross-cutting), Shared Redis cache (reads) |
| **Resilience** | Health Engine → Circuit Breaker → Retry Engine (3-tier stack) |
| **Gateway Overhead** | ~5.4ms P99 latency added |
| **Memory per Worker** | ~138MB |
| **Scalability** | Vertical (Uvicorn workers) + Horizontal (instances behind LB, shared PostgreSQL) |

---

## The 4 Architectural Tiers

### Tier 1 — Interface Layer (Presentation)
- **OpenAI Compatibility Router:** Accepts `/v1/chat/completions`, `/v1/embeddings`, `/v1/models` requests.
- **Management API Router:** Provides CRUD operations for providers, models, API keys, routing policies (`/api/v1/`).
- **Auth Middleware:** Validates consumer gateway keys (HMAC-SHA256 lookup) and admin JWT sessions.
- **Rate Limiting Middleware:** Sliding-window rate limiting enforced via Redis.

### Tier 2 — Application Layer
- **Decision Intelligence Engine:** Evaluates policies, filters candidates, scores and ranks models, returns an immutable `ExecutionPlan`.
- **Failover Orchestrator:** Executes the `ExecutionPlan`, handles retries and provider switching transparently.
- **Plugin Orchestrator:** Manages plugin lifecycle (load, activate, deactivate) and invokes pre/post-process hooks.

### Tier 3 — Domain Layer
- **Provider Entity:** Represents an LLM provider with health state and configuration.
- **Model Entity:** Represents a specific model with capabilities (vision, function calling, JSON mode) and performance metadata.
- **API Key Entity:** Consumer-facing gateway key with quota, budget, and task-type restrictions.
- **Routing Rule Entity:** Ordered priority rules defining which providers/models to use under what conditions.

### Tier 4 — Infrastructure Layer
- **Database:** Async SQLAlchemy 2.0 with PostgreSQL. Alembic for migrations.
- **Redis Cache:** In-memory hot config cache + rate limit sliding windows + semantic response cache.
- **Provider Adapters:** HTTP clients for each LLM provider (OpenAI, Anthropic, Google, Groq, etc.) translating the internal request format to each provider's native API.
- **Event Bus:** In-process async event bus for `ConfigChangedEvent`, `PluginConfigChangedEvent`, `HealthUpdatedEvent`.

---

## Performance Profile

| Metric | Value |
|---|---|
| P50 Gateway Overhead | 2.1ms |
| P90 Gateway Overhead | 3.5ms |
| P99 Gateway Overhead | 6.2ms |
| Max RPS (single pod, proxy) | 4,200 RPS |
| Memory per Worker | ~138MB |
| Semantic Cache Hit TTFT | ~12ms (bypasses LLM entirely) |
