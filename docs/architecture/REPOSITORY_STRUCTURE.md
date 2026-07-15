# Dronzer AI Gateway — Engineering Handbook: Repository Blueprint

**Document Status:** ✅ Approved  
**Version:** 1.0  
**Approved Date:** July 8, 2026  

> Full document available in conversation artifacts. This is the permanent reference summary.

## Structural Overview
- **Monorepo:** Backend (Python 3.13+) and Frontend (Next.js/React)
- **Backend Architecture:** Clean Architecture (Domain → Application → Infrastructure → Interface)
- **Frontend Architecture:** App Router, reusable components, API clients separated.

## Top-Level Directories
- `/backend` — Python FastAPI application
- `/frontend` — Next.js React Dashboard
- `/plugins` — Dynamic plugin mount point
- `/docs` — Architecture, API, and Developer guides
- `/docker`, `/k8s`, `/.github`, `/scripts`, `/assets`, `/examples`

## Python Package Rules
- **Domain Layer:** Zero external dependencies.
- **Application Layer:** Depends only on Domain.
- **Infrastructure Layer:** Implements Domain ports (SQLAlchemy, Redis, httpx).
- **Interface Layer:** FastAPI routers, middlewares. Depends on Application.
- **Composition Root:** `dependencies.py` wires Infrastructure into Application.

## Plugin System
- Discovered at runtime.
- Emits `PluginConfigChangedEvent` for dynamic reload without server restart.

## CI/CD & Maintenance
- Strict import rules enforced by Ruff.
- Migrations via Alembic (append-only).
- Comprehensive testing (Unit, Integration, E2E).
