# Dronzer v2.0 Breaking Changes

The v2.0 release includes several breaking architectural and API changes necessary to support Enterprise Multi-Tenancy and the new PromptOps engine.

## 💥 1. Dropped SQLite Support
**Change:** SQLite is no longer supported as a backend database.
**Reason:** The new Distributed DAG Workflow Engine and ABExperimentEngine require Postgres-specific features (JSONB, SKIP LOCKED) to function correctly at scale.
**Fix:** Migrate to PostgreSQL 15+.

## 💥 2. API Route Reorganization
**Change:** The `/chat` and `/completions` endpoints have been moved under the `/v1/` prefix.
- Old: `POST /chat/completions`
- New: `POST /v1/chat/completions`
**Reason:** Formalizing the API versioning for SDK generation.
**Fix:** Update any raw HTTP clients to append `/v1`. If you use the new SDKs, this is handled automatically.

## 💥 3. Provider Configuration
**Change:** Provider API keys (e.g., `OPENAI_API_KEY`) are no longer loaded from the global environment variables of the Dronzer server.
**Reason:** To support Multi-Tenancy, provider keys are now securely managed per-Organization in the Database (encrypted via KMS).
**Fix:** Use the Admin API or the Dronzer Web Dashboard to input your provider keys into your Organization's settings.

## 💥 4. Strict Rate Limiting
**Change:** The Gateway now enforces a strict Sliding Window Rate Limit (default 1000 req/min per API Key).
**Reason:** Protect the infrastructure from volumetric attacks.
**Fix:** Ensure your client applications handle `429 Too Many Requests` status codes and implement exponential backoff (The official v2.0 SDKs do this automatically).
