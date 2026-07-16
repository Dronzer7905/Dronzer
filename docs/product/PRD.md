# Product Requirements Document — Dronzer AI Gateway

**Document Status:** ✅ Approved
**Version:** 1.0
**Approved Date:** July 8, 2026

---

## Approved Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Project Name | **Dronzer** | Unique, memorable brand identity |
| Language | **Python 3.13+** | I/O-bound workload ideal for async Python; large AI contributor ecosystem |
| Database | **PostgreSQL 15+** | Production-grade; JSONB, SKIP LOCKED, Declarative Partitioning support |
| Frontend | **Next.js (App Router)** | Most mature React framework; component-driven, production-ready |
| License | **Apache 2.0** | Patent protection for enterprise adopters; industry-preferred for infrastructure |
| Initial Providers | **Groq, Google AI Studio, Cerebras, Mistral, Cohere, OpenRouter, Fireworks AI, Together AI, Novita AI, Nebius AI Studio, OpenAI, Anthropic** | 44+ free-tier models seeded out of the box |
| Telemetry | **None** | Trust-first open-source strategy — no data leaves the self-hosted instance |
| Model Seeding | **Manual (seed scripts)** | Database starts empty on clone; run `seed_free_providers.py` to populate |

---

## Key Product Requirements

- Enterprise-grade, open-source, self-hosted AI Gateway
- "NGINX for AI" — transparent proxy with unified OpenAI-compatible API (`/v1/chat/completions`)
- Fully database-driven — zero code changes required after deployment
- Admin Dashboard for all operational management
- Unlimited providers, models, and API keys — all managed dynamically via UI or API
- Automatic 3-tier failover: HealthEngine → CircuitBreaker → RetryEngine
- Intelligent routing: priority, round-robin, weighted, least-latency, task-aware
- Per-model and per-provider real-time health tracking
- Plugin architecture for zero-modification extensibility
- Streaming, embeddings, vision, function calling, and JSON mode support
- Licensed under **Apache 2.0** — no enterprise paywall, no feature gating
