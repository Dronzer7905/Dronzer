# Dronzer AI Gateway — API Key Rotation Engine

**Document Status:** ✅ Approved  
**Version:** 1.0  
**Approved Date:** July 8, 2026  

> Full document available in conversation artifacts. This is the permanent reference summary.

## Core Philosophy
- **Intelligent Allocation:** Keys are selected based on health, quota, and specific strategies (LRU, Priority, Weighted), not just random rotation.
- **Fail Gracefully:** Transient errors (429, 5xx) trigger transparent retries with a fallback key.

## Key Lifecycle & Health
- **States:** Active, Cooldown, Recovering (Half-Open), Expired, Disabled.
- **Health Score:** Driven by latency, 5xx rate, and 429 frequency. Drops below a threshold force a key into Cooldown.
- **Recovery:** Exponential backoff for cooldowns. Uses active probing (canary requests) to test recovery.

## Performance & Scalability
- **O(1) Selection:** Circular lists/deques in memory allow ultra-fast key checkout.
- **Eventual Consistency:** Quota and token usage sync asynchronously to Redis to avoid blocking proxy threads.

## Approved Open Decisions
- **Default Strategy:** Least Recently Used (LRU) for new providers to maximize bucket refill time.
- **Transparent Retries:** Max 3 retries before returning an error to the consumer to avoid massive latency.
- **Multi-Tenancy:** "Bring Your Own Key" (BYOK) is allowed; Key Pools are strictly isolated by `organization_id`.
