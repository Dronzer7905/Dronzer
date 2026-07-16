# Dronzer AI Gateway — Configuration System Architecture

**Document Status:** ✅ Approved
**Version:** 1.0
**Last Updated:** July 2026

---

## Overview

The Configuration System is the **control plane** of the Dronzer Gateway. It ensures that every behavioral setting — routing rules, provider keys, rate limits, plugin toggles — is applied instantly, without restarting the server, and with full audit history.

---

## Core Philosophy

| Principle | Description |
|---|---|
| **Dynamic & Restart-less** | Configuration changes propagate instantly via the internal event bus — no `kill -HUP` or pod restarts required. |
| **Cache-Driven Hot Path** | The gateway proxy hot path reads strictly from an in-memory O(1) cache. The database is never queried during request processing. |
| **Safe Execution** | All writes undergo strict schema validation (Pydantic) and referential integrity checks before being committed. |
| **Fail-Open Reads** | If PostgreSQL is unreachable, the gateway continues routing using the last known good cached configuration. |

---

## Configuration Hierarchy

Settings are applied in strict precedence order — higher levels override lower ones:

```
1. Emergency Override          ← Highest priority (operator kill-switch)
2. Runtime Override            ← Per-request HTTP header override (if enabled)
3. Project Override            ← Specific to a Project within an Organization
4. Organization Override       ← Applies to all Projects in an Organization
5. Provider Override           ← Specific to a provider (e.g., always use GPT-4o for Org A)
6. Global Settings             ← Platform-wide defaults
7. Environment Variables       ← Secrets and bootstrap config only (not routing logic)
8. Code Defaults               ← Lowest priority — hardcoded fallbacks
```

---

## Hot Reload Mechanism

The hot-reload flow ensures zero downtime when configuration changes:

```
Admin writes config change (via Dashboard or API)
        │
        ▼
Pydantic schema validation + DB referential integrity check
        │
        ▼
SQLAlchemy async write to PostgreSQL
        │
        ▼
Write-Through Cache update (local in-memory cache updated immediately)
        │
        ▼
ConfigChangedEvent emitted on internal event bus
        │
        ▼
All subscribed subsystems (Router, HealthEngine, PluginOrchestrator) reload affected config
```

A 60-second background task additionally verifies the local cache hash against the database to detect and correct any potential drift.

---

## Configuration Domains

| Domain | What It Controls |
|---|---|
| Provider Settings | Base URLs, authentication scheme, timeout values |
| Model Settings | Capability flags, context window, cost-per-token |
| Routing Rules | Priority order, strategy (priority/round-robin/weighted), fallback chains |
| API Key Settings | Budget limits, RPM quotas, task-type restrictions |
| Rate Limiting | Sliding-window sizes per key, per project, per organization |
| Plugin Settings | Enabled/disabled state, capability grants |
| Health Engine | Circuit breaker thresholds, cooldown durations |

---

## Approved Decisions

| Decision | Choice |
|---|---|
| Runtime header overrides | Permitted if `allow_consumer_routing_overrides = true` in Project config |
| Draft/publish workflow | Direct publishing for v1.0; draft → review → publish deferred to v2 |
| Multi-tenant scope | Organization settings act as **hard limits** for quotas and **defaults** for behaviors |
| Cache invalidation granularity | Targeted per-entity invalidation (not full flush) to minimize disruption |
