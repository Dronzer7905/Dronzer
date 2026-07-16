# Dronzer AI Gateway — Implementation Specification Roadmap

**Document Status:** ✅ Approved
**Version:** 1.0
**Last Updated:** July 2026

---

## Overview

This document describes the 20-phase implementation specification that guided the development of Dronzer v2.0. Each phase represents a discrete, independently testable increment of the system.

---

## Phase Breakdown

| Phase | Name | Description |
|---|---|---|
| 1 | **Repository Foundation** | Monorepo structure, pyproject.toml, Next.js scaffold, .gitignore, pre-commit hooks |
| 2 | **Core Framework** | FastAPI app factory, structured logging (structlog), settings management (pydantic-settings) |
| 3 | **Database Layer** | SQLAlchemy 2.0 async engine, Alembic migrations, Base models, session factory |
| 4 | **Dependency Injection** | Composition root (`dependencies.py`), factory functions, async lifespan management |
| 5 | **Configuration System** | Database-driven config loading, in-memory hot cache, event bus (`ConfigChangedEvent`) |
| 6 | **Plugin Framework** | Plugin loader, `ExtensionBase` interface, pre/post-process hooks, sandbox |
| 7 | **Provider SDK** | Abstract `ProviderAdapter` port, OpenAI and Anthropic adapter implementations |
| 8 | **OpenAI Compatibility API** | `/v1/chat/completions`, `/v1/embeddings`, `/v1/models` routes with Pydantic schemas |
| 9 | **Routing Engine** | Routing group resolution, rule execution, `ExecutionPlan` builder |
| 10 | **API Key Rotation** | Key pool management, health scoring, LRU/Priority/Weighted strategies |
| 11 | **Model Selection** | Capability filtering, composite scoring engine, audit trace generation |
| 12 | **Provider Failover** | Circuit breaker per provider, retry orchestrator, transparent error masking |
| 13 | **Health Engine** | Sliding-window health tracking (provider, model, key), status probes |
| 14 | **Dashboard Backend** | Admin CRUD APIs (`/api/v1/`): providers, models, keys, policies, organizations |
| 15 | **Dashboard Frontend** | Next.js Light Theme scaffold, sidebar layout, auth flow, API client setup |
| 16 | **Authentication** | Consumer key HMAC validation middleware, admin JWT session management |
| 17 | **RBAC** | Organization → Project → Key hierarchy, role definitions, permission checks |
| 18 | **Metrics & Observability** | Prometheus metrics at `/metrics`, Grafana dashboard provisioning, request trace logging |
| 19 | **Deployment** | Docker Compose (dev + prod), Kubernetes Helm chart, GitHub Actions CI/CD |
| 20 | **Production Hardening** | Load testing (wrk), security audit, rate limit tuning, memory profiling |

---

## Quality Gates (All Phases)

Every phase must satisfy:

- **Unit Test Coverage:** ≥90% for all new modules.
- **Static Analysis:** `ruff check .` must pass with zero warnings.
- **Type Checking:** `mypy .` must pass in strict mode.
- **Clean Architecture:** No cross-layer import violations (enforced by ruff import rules).
- **Migration Safety:** Every schema change must have a corresponding Alembic migration (append-only).

---

## Seed Scripts (Post-Phase 3)

After Phase 3 (Database Layer) is complete, the seed scripts become runnable:

```bash
# Required after running: alembic upgrade head
python scripts/seed_free_providers.py     # Phase 3+
python scripts/patch_model_metadata.py   # Phase 11+
```

These scripts must remain idempotent across all future schema changes.
