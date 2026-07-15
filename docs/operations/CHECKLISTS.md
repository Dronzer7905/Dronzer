# Dronzer Operational Checklists

## 1. Maintainer Release Checklist
- [ ] Verify GitHub Actions (`dronzer-ci.yml`) passes.
- [ ] Ensure `pyproject.toml` version is bumped and dependencies are pinned.
- [ ] Tag the commit (e.g. `v2.0.0`) and draft the GitHub Release.
- [ ] Build and Push Docker Images to Docker Hub (`dronzer/api`, `dronzer/gateway`).
- [ ] Publish the Helm Chart to the OCI registry.

## 2. Production Deployment Checklist
- [ ] Deploy Postgres 15+ in High Availability (HA) mode.
- [ ] Deploy Redis 7+ with Persistence enabled (for Rate Limiting and Caching).
- [ ] Run `alembic upgrade head` before scaling up the API Gateway pods.
- [ ] Configure `DRONZER_JWT_SECRET` via Kubernetes Secrets.
- [ ] Set `ENVIRONMENT=production`.

## 3. Backup Checklist
- [ ] Enable daily automated `pg_dump` of the Postgres Database.
- [ ] (Optional) Enable RDB snapshots for the Redis Cache to preserve Semantic Cache hits.

## 4. Disaster Recovery Checklist
- [ ] In the event of an LLM provider (e.g., OpenAI) global outage, verify that the `ABExperimentEngine` and `Router` automatically failover to fallback models (e.g., Anthropic or Local Llama3).
- [ ] To restore from backup: Spin up fresh Postgres instance -> apply `pg_dump` -> restart all Dronzer Gateway pods.
