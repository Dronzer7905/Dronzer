# Dronzer AI Gateway — API Key Rotation Engine

**Document Status:** ✅ Approved
**Version:** 1.0
**Last Updated:** July 2026

---

## Overview

The API Key Rotation Engine manages the pool of **provider API keys** (e.g., OpenAI keys, Groq keys) stored in the encrypted database. Its job is to intelligently select which key to use for each request, track key health, and seamlessly rotate away from unhealthy or rate-limited keys — all without exposing errors to the consumer.

This is separate from **consumer gateway keys** (the `dz-sk-...` keys that your applications use to authenticate with Dronzer).

---

## Core Philosophy

| Principle | Description |
|---|---|
| **Intelligent Allocation** | Keys are selected based on health, quota, and strategy — not random rotation. |
| **Transparent Recovery** | Transient errors (429, 5xx) trigger silent retries with a fallback key before returning an error to the consumer. |
| **Strict Tenant Isolation** | Key pools are isolated by `organization_id`. A key belonging to Org A can never be used for a request from Org B. |
| **BYOK Support** | "Bring Your Own Key" — Organizations can supply their own provider API keys which are encrypted and stored in their isolated key pool. |

---

## Key Lifecycle

```
New Key Added (via Dashboard / Admin API)
       │
       ▼
   [ACTIVE]  ←─────────────────────────────────────────────────┐
       │                                                         │
  429 or 5xx errors accumulate                                   │
       │                                                         │
       ▼                                                         │
  [COOLDOWN]  ← Exponential backoff timer starts                │
       │                                                         │
  Backoff expires → canary request sent                         │
       │                                                         │
  ┌────┴────┐                                                    │
  │ Success │ → [RECOVERING (Half-Open)] → monitors for 5 min   │
  │ Fail    │ → back to [COOLDOWN] with doubled backoff          │
  └─────────┘                                                    │
       │                                                         │
  Sustained success in RECOVERING                               │
       └──────────────────────────────────────────────────────→─┘

  [EXPIRED]   ← Key fails all recovery attempts (permanent failure)
  [DISABLED]  ← Manually disabled by an admin
```

---

## Selection Strategies

| Strategy | Description | Best For |
|---|---|---|
| **LRU (Least Recently Used)** | Default. Rotates through keys in order to maximize each provider's rate-limit bucket refill time. | General use, free-tier keys |
| **Priority** | Always uses the highest-priority healthy key first. | Premium keys with higher limits |
| **Weighted** | Distributes requests proportionally based on configured weights (e.g., 70/30 split). | Balancing two different-tier keys |

---

## Health Scoring

Each key has a real-time health score (0.0 – 1.0) computed from a 1-minute sliding window:

```
health_score = (1 - 5xx_rate) × 0.5
             + (1 - 429_rate) × 0.3
             + (1 - normalized_latency) × 0.2
```

A key with `health_score < 0.4` is automatically moved to **Cooldown** state.

---

## Performance

| Metric | Value |
|---|---|
| Key selection latency | O(1) via circular deque / sorted list in memory |
| Quota sync latency | Async — usage synced to Redis every 100ms to avoid blocking proxy threads |
| Max retries before consumer error | 3 attempts (configurable per routing rule) |

---

## Approved Decisions

| Decision | Choice |
|---|---|
| Default strategy for new providers | **LRU** — maximizes bucket refill time |
| Max retries before consumer error | **3** — balances recovery with acceptable latency |
| Quota/token tracking | Asynchronous Redis sync — eventual consistency acceptable for billing accuracy |
| Key pool isolation | Strictly by `organization_id` — no cross-tenant key sharing |
