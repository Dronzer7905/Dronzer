# Dronzer Backend

This directory contains the core Dronzer AI Gateway — a Python FastAPI application built on Clean Architecture principles.

---

## Architecture

The backend is organized into four strictly isolated layers:

```
src/dronzer/
├── domain/           # Core business logic — ZERO external dependencies
│   ├── entities/     # Database-agnostic data models (Pydantic / dataclasses)
│   ├── ports/        # Abstract interfaces (Repository, Cache, Provider)
│   └── services/     # Pure domain logic (scoring, health checks)
├── application/      # Use cases — depends only on domain/
│   ├── orchestrator/ # Request routing, failover, retry orchestration
│   ├── plugins/      # Plugin loader and lifecycle management
│   └── services/     # Application-level services (key rotation, etc.)
├── infrastructure/   # Implements domain ports — DB, Redis, HTTP
│   ├── database/     # SQLAlchemy models, Alembic migrations, session factory
│   ├── providers/    # Adapter implementations (OpenAI, Anthropic, Groq, etc.)
│   └── cache/        # Redis client, semantic cache
└── presentation/     # FastAPI routers, middleware, request/response schemas
    ├── api/          # Route handlers (v1/chat/completions, admin CRUD)
    └── middleware/   # Auth, rate limiting, request ID injection
```

---

## Local Development Setup

### 1. Prerequisites

| Dependency | Minimum Version |
|---|---|
| Python | 3.13+ |
| PostgreSQL | 15+ |
| Redis | 7+ |

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your local database credentials:

```env
DATABASE_URL=postgresql+asyncpg://dronzer:your_password@localhost:5433/dronzer_prod
SECRET_KEY=<run: openssl rand -hex 32>
ENCRYPTION_KEY=<run: openssl rand -hex 32>
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

### 4. Apply Database Migrations

```bash
alembic upgrade head
```

This creates all tables, indexes, and constraints in your PostgreSQL database.

### 5. Seed Providers & Models

> ⚠️ **Models do NOT auto-populate on clone.** After migrations, you must manually run the seed scripts to populate the provider and model registry.

```bash
# Seeds 44+ free-tier providers and their models into the database.
# This creates provider/model RECORDS only — it does NOT insert any API keys.
# Safe to re-run — skips entries that already exist.
python scripts/seed_free_providers.py

# Enriches model metadata: task type affinities, capabilities, context windows
python scripts/patch_model_metadata.py
```

> **🔑 API keys are NOT seeded.** After running these scripts, you must open the Admin Dashboard and manually enter your own API key for each provider. The seed scripts only register the provider name, base URL, and model list. No routing will happen until you add at least one API key per provider.

After seeding, the following providers will be registered and awaiting your API keys:

| Provider | Where to Get a Free Key | Free Key Required |
|---|---|---|
| Groq | https://console.groq.com/keys | ✅ |
| Google AI Studio | https://aistudio.google.com/app/apikey | ✅ |
| Mistral | https://console.mistral.ai/ | ✅ |
| Cerebras | https://cloud.cerebras.ai/ | ✅ |
| OpenRouter | https://openrouter.ai/settings/keys | ✅ |
| Cloudflare Workers AI | https://dash.cloudflare.com/profile/api-tokens | ✅ |
| NVIDIA NIM | https://build.nvidia.com/ | ✅ |
| OpenAI | https://platform.openai.com/api-keys | ✅ (paid) |
| Anthropic | https://console.anthropic.com/ | ✅ (paid) |


### 6. Start the Dev Server

```bash
fastapi run src/dronzer/main.py
# API available at: http://localhost:8000
# OpenAPI docs at:  http://localhost:8000/docs
```

---

## Code Quality

All code must pass these checks before committing:

```bash
ruff check .           # Linting (enforces Clean Architecture import rules)
ruff format .          # Formatting
mypy .                 # Strict type checking
pytest tests/          # Full test suite
```

These are also enforced automatically in CI via GitHub Actions.

---

## Key Configuration

| Variable | Description | Required |
|---|---|---|
| `DATABASE_URL` | Async PostgreSQL connection string | ✅ |
| `SECRET_KEY` | JWT signing key (32 bytes hex) | ✅ |
| `ENCRYPTION_KEY` | Fernet key for API key encryption (32 bytes hex) | ✅ |
| `ENVIRONMENT` | `development` or `production` | ✅ |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, `ERROR` | Optional |
| `ENABLE_METRICS` | Expose Prometheus metrics at `/metrics` | Optional |

---

## Full Documentation

For complete documentation, see the [`docs/`](../docs/) directory:

- [Architecture Overview](../docs/architecture/ARCHITECTURE.md)
- [Database Architecture](../docs/architecture/DATABASE_ARCHITECTURE.md)
- [Configuration System](../docs/architecture/CONFIGURATION_SYSTEM.md)
- [Developer Guide](../docs/guides/developer-guide.md)
