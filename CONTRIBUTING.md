# Contributing to Dronzer

Thank you for considering contributing to the Dronzer AI Gateway! We welcome contributions of all kinds — bug fixes, new provider integrations, documentation improvements, and more.

---

## Prerequisites

Before contributing, ensure you have the following installed:

| Dependency | Minimum Version |
|---|---|
| Python | 3.13+ |
| Node.js | 20+ |
| PostgreSQL | 15+ |
| Redis | 7+ |
| Git | Latest |

---

## Setting Up the Development Environment

```bash
# 1. Fork and clone the repository
git clone https://github.com/dronzer7905/dronzer.git
cd dronzer

# 2. Set up the backend
cd backend
python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows
pip install -e ".[dev]"

# 3. Configure environment variables
cp .env.example .env
# Edit .env with your local DB credentials and secret keys

# 4. Apply database migrations
alembic upgrade head

# 5. Seed the database with free providers and models
python scripts/seed_free_providers.py
python scripts/patch_model_metadata.py

# 6. Set up the frontend
cd ../frontend
npm install
```

---

## How Can I Contribute?

### 🐛 Reporting Bugs

- Search [existing issues](https://github.com/dronzer7905/dronzer/issues) before opening a new one.
- Use the **Bug Report** issue template.
- Include: OS, Python version, Dronzer version, steps to reproduce, and any relevant logs or trace IDs.

### 💡 Suggesting Enhancements

- Open a [GitHub Discussion](https://github.com/dronzer7905/dronzer/discussions) to discuss your idea before implementing it.
- For concrete proposals, use the **Feature Request** issue template.

### 🔌 Adding a New Provider

To add a new LLM provider:
1. Implement the provider adapter in `backend/src/dronzer/infrastructure/providers/`.
2. Register it via the seed script or Admin Dashboard (no hardcoded provider names in business logic).
3. Add the provider to `SUPPORT_MATRICES.md`.
4. Write unit tests for the adapter.

---

## Pull Request Process

1. **Branch from `main`:**
   ```bash
   git checkout -b feature/my-awesome-feature
   ```

2. **Follow Clean Architecture boundaries:**
   - `domain/` layer has **zero** external dependencies.
   - `application/` depends only on `domain/`.
   - `infrastructure/` implements domain ports (SQLAlchemy, Redis, httpx).
   - `presentation/` (FastAPI routers) depends on `application/`.

3. **Enforce code style before committing:**
   ```bash
   # Run inside backend/ with venv activated
   ruff check .
   ruff format .
   mypy .
   ```

4. **Run the test suite:**
   ```bash
   pytest tests/
   ```

5. **Open the Pull Request** and fill out the PR template thoroughly. A core maintainer will review it within **48 hours**.

---

## Code Standards

- **No Magic Strings:** All string constants must be defined as enums or named constants.
- **Strict Type Hints:** All Python functions must have complete type annotations (enforced by `mypy --strict`).
- **Docstrings:** All public classes and methods must have docstrings.
- **Test Coverage:** New features must include unit tests. Integration tests are required for new provider adapters.

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).
