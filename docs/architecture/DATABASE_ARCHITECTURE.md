# Dronzer AI Gateway — Database Architecture

**Document Status:** ✅ Approved
**Version:** 1.0
**Last Updated:** July 2026

---

## Overview

The PostgreSQL database is the **single source of truth** for all Dronzer configuration, routing logic, and telemetry. The gateway reads primarily from a Redis-backed in-memory cache to avoid database round-trips on the hot path, while all writes go through the database first and then propagate to the cache via the event bus.

---

## Database Philosophy

| Principle | Description |
|---|---|
| **Control Plane Authority** | The database entirely dictates routing, health thresholds, and plugin logic. No routing rules exist in code. |
| **Cache-Accelerated Reads** | All hot-path reads are served from the in-memory/Redis cache. The DB is only read during startup and cache miss recovery. |
| **Immutable Audit Trail** | Every configuration change is written to append-only `_history` tables via PostgreSQL triggers. |
| **Soft Deletion** | Core entities use a `deleted_at` timestamp to preserve referential integrity for logs and audit records. |

---

## Technology Stack

| Component | Choice | Reason |
|---|---|---|
| Database | PostgreSQL 15+ | JSONB, SKIP LOCKED, Declarative Partitioning, robust async driver support |
| ORM | SQLAlchemy 2.0 (async) | Native async with `asyncpg` driver, type-safe queries |
| Migrations | Alembic | Append-only migration history, CI-enforced |
| Primary Keys | UUIDv4 globally | Avoids sequential ID enumeration attacks, multi-node safe |
| Encryption | Fernet (symmetric) | Column-level encryption for all stored provider API keys |

---

## Core Data Domains

The schema is organized into 10 logical domains:

| # | Domain | Key Tables |
|---|---|---|
| 1 | **Provider Management** | `providers`, `provider_configs` |
| 2 | **Model Management** | `models`, `model_capabilities`, `model_metadata` |
| 3 | **API Key Management** | `consumer_keys`, `key_quotas`, `key_usage` |
| 4 | **Routing System** | `routing_rules`, `routing_policies`, `routing_groups` |
| 5 | **Health & Circuit Breaker** | `provider_health`, `model_health`, `circuit_breaker_states` |
| 6 | **Plugin System** | `plugins`, `plugin_configs`, `plugin_capabilities` |
| 7 | **Security & Identity** | `organizations`, `projects`, `users`, `roles`, `permissions` |
| 8 | **Observability** | `request_logs` (partitioned), `metrics_snapshots` |
| 9 | **Background Services** | `job_queue`, `job_executions` |
| 10 | **Configuration** | `global_config`, `config_history` |

---

## Structural Design Patterns

### Soft Deletion
All core entities include:
```sql
deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL
```
Queries filter `WHERE deleted_at IS NULL`. Hard deletes are never performed on entities referenced by logs.

### Time-Based Partitioning
The `request_logs` table uses PostgreSQL Declarative Partitioning by month:
```sql
PARTITION BY RANGE (created_at)
```
Old partitions are dropped automatically by a background job respecting the 90-day retention policy.

### Audit History Tables
Configuration-critical tables (`routing_rules`, `global_config`, `plugin_configs`) have companion `_history` tables populated by `AFTER UPDATE OR DELETE` triggers:
```
config_history (id, table_name, row_id, old_value, new_value, changed_by, changed_at)
```

### Referential Integrity
- All foreign keys are **strict** (no deferred constraints).
- `ON DELETE RESTRICT` is used on entities that would leave orphaned logs.
- `ON DELETE CASCADE` only for child configuration records (e.g., `key_quotas` cascade when a `consumer_key` is deleted).

---

## First-Time Setup

After cloning the repository, run these commands in order:

```bash
# Step 1: Create all tables and indexes
alembic upgrade head

# Step 2: Seed providers and models (database starts empty after clone)
python scripts/seed_free_providers.py
python scripts/patch_model_metadata.py
```

To verify the schema was applied successfully:
```bash
alembic current        # Should show: head
alembic history        # Shows full migration log
```
