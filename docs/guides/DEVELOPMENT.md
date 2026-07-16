# Development Guide

Welcome to the Dronzer development guide! This document gets you from a fresh clone to a fully running local development environment.

---

## Prerequisites

| Dependency | Minimum Version | Install |
|---|---|---|
| Python | 3.13+ | [python.org](https://python.org) |
| Node.js | 20+ | [nodejs.org](https://nodejs.org) |
| PostgreSQL | 15+ | `docker-compose up -d` (easiest) |
| Redis | 7+ | `docker-compose up -d` (easiest) |
| Git | Latest | System package manager |

---

## Quick Start (Docker)

The easiest way to get all infrastructure running locally:

```bash
# From the repo root — starts Postgres 15, Redis 7, and Adminer (DB GUI)
docker-compose up -d
```

This gives you:
- PostgreSQL on port `5433`
- Redis on port `6379`

---

## Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows

# Install all dependencies (including dev extras)
pip install -r requirements.txt
```

### Configure Environment

```bash
cp .env.example .env
# Edit .env — set DATABASE_URL, SECRET_KEY, ENCRYPTION_KEY
```

Generate secure keys with:
```bash
openssl rand -hex 32    # Use twice: once for SECRET_KEY, once for ENCRYPTION_KEY
```

### Apply Migrations & Seed Data

> ⚠️ The database is **empty after cloning**. You must run these steps before the gateway will have any models to route to.

```bash
# Step 1: Create the database schema
alembic upgrade head

# Step 2: Seed 44+ free-tier providers and models
python scripts/seed_free_providers.py

# Step 3: Enrich model metadata (capabilities, task affinities)
python scripts/patch_model_metadata.py
```

### Start the Backend

```bash
fastapi run src/dronzer/main.py
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Dashboard: http://localhost:3000
```

---

## Quality Gates

All of these must pass before submitting a pull request:

```bash
cd backend

# Linting (enforces Clean Architecture import boundaries)
ruff check .

# Auto-formatting
ruff format .

# Strict type checking
mypy .

# Full test suite
pytest tests/
```

Pre-commit hooks run `ruff check` and `ruff format` automatically on every commit.

---

## Useful Commands

| Command | Description |
|---|---|
| `alembic upgrade head` | Apply all pending migrations |
| `alembic downgrade -1` | Roll back the last migration |
| `alembic revision --autogenerate -m "description"` | Generate a new migration |
| `alembic history` | Show full migration history |
| `pytest tests/ -v` | Run tests with verbose output |
| `pytest tests/ -k "test_routing"` | Run only tests matching a pattern |
| `ruff check . --fix` | Auto-fix all fixable lint errors |
