# Dronzer AI Gateway — Administrator Guide

Welcome to the Dronzer Administrator Guide! This document covers operational management of the Dronzer Gateway, including deployment topologies, configuration, scaling, and observability.

---

## Deployment Options

Dronzer ships as a set of Docker containers. Two primary deployment topologies are supported:

### Option 1 — Docker Compose (Single Node)

Best for small to medium workloads, internal tools, and development teams.

```bash
# Clone the repository
git clone https://github.com/dronzer7905/dronzer.git
cd dronzer

# Start the full production stack
docker-compose -f docker-compose.prod.yml up -d
```

This brings up:
- PostgreSQL 15 (database)
- Redis 7 (rate limiting + caching)
- Python FastAPI Gateway (port `8000`)
- Next.js Admin Dashboard (port `3000`)
- Prometheus (port `9090`)
- Grafana (port `3001`)

> ⚠️ **First-Time Setup:** After the stack is running, seed the database:
> ```bash
> docker exec -it dronzer-backend alembic upgrade head
> docker exec -it dronzer-backend python scripts/seed_free_providers.py
> docker exec -it dronzer-backend python scripts/patch_model_metadata.py
> ```

### Option 2 — Kubernetes Helm Chart (High Availability)

Best for enterprise workloads requiring auto-scaling, zero-downtime deployments, and multi-region topology.

```bash
# Install using the bundled Helm chart
helm install my-dronzer ./helm/dronzer -f ./helm/dronzer/values.yaml

# Or from a custom values file for your environment
helm install my-dronzer ./helm/dronzer -f ./helm/dronzer/values.production.yaml
```

**Minimum Kubernetes version:** 1.25+ (recommended: 1.29+)

After Helm install, run the database migration Job:
```bash
kubectl create job --from=cronjob/dronzer-migrate dronzer-migrate-init
```

---

## Admin Dashboard

Navigate to `http://localhost:3000` (or your production dashboard URL).

From the dashboard you can:

| Feature | Description |
|---|---|
| **Manage API Keys** | Issue, revoke, and set budget/token quotas per consumer key |
| **Configure Providers** | Add new providers, input their API keys (encrypted at rest) |
| **Configure Models** | Enable/disable models, set capability flags, adjust scoring weights |
| **Routing Policies** | Define failover rules (e.g., "If Groq fails → route to Cerebras") |
| **Monitor Costs** | Live token usage and estimated USD spend per provider and model |
| **View Audit Logs** | Immutable log of all config changes, key rotations, and request traces |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | ✅ | Async PostgreSQL URL: `postgresql+asyncpg://user:pass@host:port/db` |
| `SECRET_KEY` | ✅ | JWT signing key (run `openssl rand -hex 32`) |
| `ENCRYPTION_KEY` | ✅ | Fernet encryption key for stored provider API keys |
| `ENVIRONMENT` | ✅ | `development` or `production` |
| `LOG_LEVEL` | Optional | `DEBUG`, `INFO`, `WARNING`, `ERROR` (default: `INFO`) |
| `ENABLE_METRICS` | Optional | Set `true` to expose Prometheus metrics at `/metrics` |
| `REDIS_URL` | Optional | Redis URL (default: `redis://localhost:6379`) — required for rate limiting |

---

## System Observability

### Prometheus Metrics
Dronzer exports detailed Prometheus metrics at `http://localhost:8000/metrics`:

| Metric | Description |
|---|---|
| `dronzer_requests_total` | Total requests by provider, model, status |
| `dronzer_request_latency_seconds` | Latency histograms (gateway overhead) |
| `dronzer_provider_health_score` | Real-time health score per provider |
| `dronzer_api_key_quota_used` | Quota consumption per consumer key |
| `dronzer_failover_total` | Total failover events by provider |

### Grafana Dashboard
If deployed with `docker-compose.prod.yml`, Grafana is preconfigured at `http://localhost:3001`:
- Live request throughput and error rates
- P50/P90/P99 latency percentiles per provider
- Provider health heatmap
- Token cost analytics over time

### Health Endpoints

| Endpoint | Auth | Description |
|---|---|---|
| `GET /health` | None | Returns `200 OK` or `503 Service Unavailable` |
| `GET /health/detailed` | Admin JWT | Full subsystem health report (DB, Redis, providers) |

---

## Scaling

### Vertical Scaling (Single Node)
Increase Uvicorn worker count in the Dockerfile or Docker Compose:
```yaml
command: uvicorn src.dronzer.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Horizontal Scaling (Multi-Node)
Deploy multiple Gateway instances behind a load balancer. All instances share:
- The same PostgreSQL database
- The same Redis instance (for rate limiting consistency)

Note: Cache consistency is eventually consistent (60-second sync window) across workers.
