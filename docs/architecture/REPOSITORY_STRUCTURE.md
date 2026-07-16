# Dronzer AI Gateway — Repository Structure

**Document Status:** ✅ Approved
**Version:** 1.0
**Last Updated:** July 2026

---

## Overview

Dronzer is organized as a **monorepo** containing both the Python backend and the Next.js frontend, along with infrastructure configurations, documentation, and tooling.

---

## Top-Level Directory Layout

```
dronzer/
├── backend/                    # Python 3.13+ FastAPI application
│   ├── src/dronzer/            # Application source (Clean Architecture)
│   │   ├── domain/             # ZERO external deps — entities, ports, pure services
│   │   ├── application/        # Use cases — depends only on domain/
│   │   ├── infrastructure/     # DB, Redis, HTTP clients — implements domain ports
│   │   └── presentation/       # FastAPI routers, middleware, Pydantic schemas
│   ├── scripts/                # Seed scripts (seed_free_providers.py, patch_model_metadata.py)
│   ├── tests/                  # Unit, integration, and E2E test suites
│   ├── alembic/                # Database migration files (append-only)
│   ├── alembic.ini             # Alembic config
│   ├── pyproject.toml          # Project metadata, dependencies, tool config (ruff, mypy)
│   ├── .env.example            # Environment variable template
│   └── Dockerfile              # Production container image
│
├── frontend/                   # Next.js 15 Admin Dashboard
│   ├── src/app/                # App Router pages (dashboard/, login/)
│   ├── src/components/         # UI primitives, layout, feature components
│   ├── src/lib/                # API clients, utilities
│   └── package.json
│
├── docs/                       # All project documentation
│   ├── architecture/           # System design, ADRs, data models
│   ├── guides/                 # Developer, admin, enterprise, LLMOps guides
│   ├── operations/             # Deployment checklists
│   ├── product/                # PRD, product decisions
│   └── reference/             # Benchmarks, support matrices
│
├── docker/                     # Dockerfiles and build context
├── docker-compose.yml          # Local development stack
├── docker-compose.prod.yml     # Production stack (with Prometheus + Grafana)
├── helm/                       # Kubernetes Helm chart for Dronzer
├── k8s/                        # Raw Kubernetes manifests
├── plugins/                    # Drop-in extension plugins mount point
├── sdks/                       # Official client SDKs
├── scripts/                    # Repo-level utility scripts
├── examples/                   # Integration examples (LangChain, OpenAI SDK, etc.)
├── assets/                     # Static assets (logos, screenshots)
└── .github/                    # CI/CD workflows, issue templates, PR template
```

---

## Python Package Layer Rules

These rules are enforced by `ruff` import checking and validated in CI:

| Layer | Rule |
|---|---|
| `domain/` | **Zero** external library imports. Only standard library and other domain modules. |
| `application/` | May import from `domain/` only. No infrastructure or framework imports. |
| `infrastructure/` | Implements domain ports. May import SQLAlchemy, Redis, httpx, etc. |
| `presentation/` | FastAPI routers and middleware. Imports from `application/` and `infrastructure/` (for DI). |
| `core/` | Shared config, logging setup, DI container. |

Violations of these boundaries fail the CI build.

---

## Dependency Injection

All infrastructure implementations are wired into the application layer via **`backend/src/dronzer/core/dependencies.py`** — the Composition Root. This is the only file where `infrastructure` is imported into `application` context.

---

## Plugin System

Plugins are discovered at runtime from the `/plugins/` directory:

- Each plugin is a Python package (or single `entrypoint.py` file) that subclasses `ExtensionBase`.
- Plugins are loaded on gateway startup and emit `PluginConfigChangedEvent` for dynamic reload without server restart.
- High-risk capabilities (`allow_network`, `allow_filesystem`) must be explicitly granted by an admin via the Dashboard.

---

## CI/CD

| Check | Tool | When |
|---|---|---|
| Linting | Ruff | Every commit (pre-commit hook + GitHub Actions) |
| Type checking | Mypy (strict) | Every PR |
| Tests | Pytest | Every PR |
| Import rules | Ruff import checker | Every PR |
| DB migrations | Alembic check | Every PR (ensures migrations are not missing) |
| Container build | Docker | Every merge to `main` |
