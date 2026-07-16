# Dronzer AI Gateway — Decision Intelligence Engine

**Document Status:** ✅ Approved
**Version:** 1.0
**Last Updated:** July 2026

---

## Overview

The Decision Intelligence Engine (DIE) is the **central authority** of the Dronzer Gateway. Every routing decision — which provider, which model, which API key, with what timeout and retry strategy — flows through this single component. No other subsystem makes independent routing decisions.

---

## Core Philosophy

| Principle | Description |
|---|---|
| **Centralized Authority** | Every decision (routing, timeouts, retries, API key selection) is made exclusively here. No subsystem acts unilaterally. |
| **Deterministic Outcomes** | Given identical request context, tenant state, and health state, the engine always produces mathematically identical output. |
| **Explainability** | All routing decisions emit an auditable JSON trace documenting exactly why each candidate was accepted or rejected. |
| **Immutability** | The output `ExecutionPlan` is a frozen dataclass — it cannot be mutated after creation. |

---

## Decision Pipeline (7 Steps)

```
Incoming Request
       │
       ▼
1. Build Request Context
   └─ Parse: task_type, required_capabilities, consumer_key_id, org/project scope

       │
       ▼
2. Evaluate Hierarchical Policies
   └─ Resolve: Emergency → Runtime Header → Project → Org → Global
   └─ Output: Effective routing strategy, budget limits, allowed providers

       │
       ▼
3. Filter Candidates (Hard Constraints)
   └─ Remove: inactive models, capability mismatches, out-of-budget providers
   └─ Remove: models on cooldown or circuit-broken

       │
       ▼
4. Calculate Composite Scores
   └─ Score each surviving candidate:
      score = (w_health × health) + (w_latency × 1/latency) + (w_cost × 1/cost) + (w_quality × quality)

       │
       ▼
5. Rank & Select Winner
   └─ Highest composite score wins
   └─ Ties broken by model priority (admin-configured)

       │
       ▼
6. Attach Execution Strategy
   └─ Bind: retry count, per-attempt timeout, ordered fallback candidates

       │
       ▼
7. Return Immutable ExecutionPlan
   └─ Frozen dataclass consumed by the Failover Orchestrator
```

---

## ExecutionPlan Structure

```python
@dataclass(frozen=True)
class ExecutionPlan:
    primary: ProviderModelKeyTriple
    fallbacks: tuple[ProviderModelKeyTriple, ...]
    max_retries: int
    timeout_seconds: float
    strategy: RoutingStrategy
    audit_trace: AuditTrace          # Full JSON log of why each candidate was selected/rejected
```

---

## Performance Characteristics

| Optimization | Description |
|---|---|
| **Pre-Filtering** | Hard constraint elimination runs before expensive scoring math to minimize CPU cycles. |
| **Memoization** | Identical request contexts (same task type + same tenant policy snapshot) return cached `ExecutionPlan` instantly. |
| **O(1) Lookups** | All provider, model, and key registry lookups use hash maps — no linear scans. |
| **Plugin Hooks** | Extensions can filter candidates, alter scores, or mutate the final plan before it is frozen. |

---

## Audit Trace Example

Every plan includes a full trace for observability and debugging:

```json
{
  "request_id": "req_abc123",
  "task_type": "coding",
  "candidates_evaluated": 12,
  "candidates_rejected": [
    {"model": "gpt-4o", "reason": "BUDGET_EXCEEDED", "detail": "Provider OpenAI over org limit"},
    {"model": "gemini-2.5-flash", "reason": "CAPABILITY_MISMATCH", "detail": "vision=true required but model vision=false"}
  ],
  "winner": {
    "provider": "groq",
    "model": "qwen/qwen3-32b",
    "api_key_id": "key_xyz789",
    "composite_score": 0.874
  }
}
```
