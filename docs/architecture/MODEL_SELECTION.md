# Dronzer AI Gateway — Model Selection & Orchestration Engine

**Document Status:** ✅ Approved
**Version:** 2.0
**Last Updated:** July 2026

---

## Overview

The Model Selection Engine is the component responsible for choosing the single best `(provider, model, api_key)` triple for any given request. It operates entirely in-memory using pre-loaded, cached registries — the PostgreSQL database is never queried on the hot path.

---

## Core Philosophy

- **Fungible Resources:** Models are not identified by vendor name. They are abstracted into a combination of **Capabilities**, **Health Score**, **Performance Metrics**, and **Cost**.
- **Explainable Decisions:** Every model selection generates a deterministic, auditable JSON trace that records exactly why each candidate was accepted or rejected.
- **Strict Capability Enforcement:** Capability matching is boolean/enum — not fuzzy. A request requiring `vision=true` will never be silently routed to a text-only model.

---

## How Models Are Populated

> ⚠️ **Models do NOT auto-populate when the repository is cloned.** The database starts empty.

To populate the model registry, run the seed scripts after applying Alembic migrations:

```bash
alembic upgrade head
python scripts/seed_free_providers.py      # Seeds 44+ providers & models
python scripts/patch_model_metadata.py    # Enriches capabilities & task affinities
```

These scripts are **idempotent** — safe to re-run on an existing database (existing entries are skipped).

---

## Scoring & Selection Pipeline

The engine processes each request through a deterministic 7-step pipeline:

1. **Build Request Context** — Parse task type, required capabilities, consumer key constraints.
2. **Evaluate Hierarchical Policies** — Apply overrides from Emergency → Runtime Header → Project → Organization → Global settings.
3. **Filter Candidates (Hard Constraints)** — Remove providers/models that fail strict boolean checks:
   - Model must be `active` (not in Cooldown or Disabled state).
   - Model capabilities must satisfy all required flags (vision, function calling, JSON mode, streaming).
   - Model must be within the API key's allowed provider/task list.
4. **Calculate Composite Score** — For each surviving candidate, compute a normalized weighted score:
   ```
   score = w_health * health_score
         + w_latency * (1 / normalized_p50_latency)
         + w_cost * (1 / normalized_cost_per_token)
         + w_quality * quality_index
   ```
   Weights are configurable per routing rule.
5. **Rank & Select Winner** — The candidate with the highest composite score is selected.
6. **Attach Execution Strategy** — Bind retry count, timeout values, and fallback candidates.
7. **Return Immutable `ExecutionPlan`** — A frozen dataclass passed to the Failover Orchestrator.

---

## Dynamic Model Groups

Clients can request logical **Model Groups** instead of hardcoded model names:

| Group | Routes To |
|---|---|
| `auto` | Best available model for general tasks |
| `coding` | Code-optimized models (e.g., Qwen3-32B, DeepSeek V3) |
| `reasoning` | High-capability reasoning models (e.g., DeepSeek R1, Llama 4 Maverick) |
| `vision` | Vision-capable models (e.g., Gemini 2.5 Flash, Pixtral) |
| `fast-and-cheap` | Low-latency, low-cost models (e.g., Llama 3.1 8B Instant) |

Group expansion is O(1) — resolved entirely from in-memory hash maps.

---

## Lifecycle & Discovery

- **Database-Driven:** Models are loaded from PostgreSQL at startup and cached in memory.
- **Manual Seeding:** The primary population mechanism is the `seed_free_providers.py` script.
- **Admin Overrides Win:** Admin-created or admin-disabled models always take precedence over any automated discovery.
- **Health Tracking:** Separate from provider-level health. Tracks per-model 5xx rates and TTFT (Time-to-First-Token) using a 1-minute sliding window.

---

## Approved Decisions

| Decision | Choice |
|---|---|
| Capability mismatch | **Fail Fast** — reject request immediately, no silent upgrades |
| Admin manual lock | Always wins against any automated discovery or default |
| Token normalization | Use `tiktoken`-equivalent logic for cross-provider TPS normalization |
| Cache invalidation | `ModelUpdatedEvent` triggers instant hot-cache refresh |
