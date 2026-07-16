# Dronzer Community Onboarding Guide

Welcome to the Dronzer Core Team! We are thrilled to have you contribute to the Universal AI Integration Platform. This guide gets you from zero to a fully working development environment.

---

## 1. Clone & Environment Setup

```bash
# Fork the repo on GitHub first, then clone your fork
git clone https://github.com/dronzer7905/dronzer.git
cd dronzer

# Set up the backend
cd backend
python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows
pip install -r requirements.txt

# Set up the frontend
cd ../frontend
npm install
```

---

## 2. Start Infrastructure with Docker

The easiest way to run PostgreSQL and Redis locally:

```bash
# From the repo root
docker-compose up -d
```

This starts Postgres 15 on port `5433` and Redis 7 on port `6379`.

---

## 3. Configure & Seed the Database

```bash
cd backend

# Copy environment template
cp .env.example .env
# Edit .env — set DATABASE_URL and generate SECRET_KEY / ENCRYPTION_KEY

# Apply schema migrations
alembic upgrade head

# Seed providers and models (required — the DB starts empty after cloning)
python scripts/seed_free_providers.py
python scripts/patch_model_metadata.py
```

---

## 4. Start the Development Servers

```bash
# Terminal 1 — Backend API Gateway
cd backend && fastapi run src/dronzer/main.py
# Available at: http://localhost:8000

# Terminal 2 — Frontend Dashboard
cd frontend && npm run dev
# Available at: http://localhost:3000
```

---

## 5. Running the Test Suite

All PRs require 100% of existing tests to pass:

```bash
cd backend
pytest tests/ -v
```

Before committing, always run the quality checks:

```bash
ruff check .      # Linting
ruff format .     # Formatting
mypy .            # Type checking
```

---

## 6. Submitting a Pull Request

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-awesome-feature
   ```

2. **Follow Clean Architecture import boundaries** — the `domain/` layer must have zero external library imports. See [REPOSITORY_STRUCTURE.md](../architecture/REPOSITORY_STRUCTURE.md) for the full rules.

3. **Write tests** — new features require unit tests; new provider adapters require integration tests.

4. **Push and open the PR** using the [Pull Request Template](../../.github/PULL_REQUEST_TEMPLATE.md).

A Core Maintainer will review within **48 hours** and leave feedback or approve for merge.

---

## 7. Community Channels

| Channel | Purpose |
|---|---|
| [GitHub Discussions](https://github.com/dronzer7905/dronzer/discussions) | Architecture questions, ideas, general chat |
| [GitHub Issues](https://github.com/dronzer7905/dronzer/issues) | Bug reports, concrete feature requests |
| [Pull Requests](https://github.com/dronzer7905/dronzer/pulls) | Code contributions |

We follow the [Code of Conduct](../../CODE_OF_CONDUCT.md) in all community spaces.
