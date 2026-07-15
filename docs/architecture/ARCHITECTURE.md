# System Architecture — Dronzer AI Gateway

**Document Status:** ✅ Approved  
**Version:** 2.0  
**Approved Date:** July 8, 2026  

> Full document available in conversation artifacts. This is the permanent reference summary.

## Resolved Architectural Decisions

| Decision | Resolution |
|---|---|
| Multi-worker cache consistency | Accept 60s eventual consistency. Recommend single worker for v1. |
| Health data granularity | Provider + Model + Key level (maximum granularity) |
| Audit storage | Same database with 90-day retention policy |
| Plugin distribution | pip packages (primary) + single-file drop-in (alternative) |
| Consumer key hashing | HMAC-SHA256 with master key for fast validation |
| API versioning | URL path for management API (/api/v1/), OpenAI-native for gateway API |
| Health endpoint | Simple /health (200/503) + /health/detailed (admin auth) |
| Default routing strategy | Priority-based |

## Architecture Summary

- **Style:** Clean Architecture + Hexagonal + Event-Driven + Reverse Proxy
- **Process Model:** Single process (Gateway + Management API + Dashboard)
- **25 Subsystems** across 4 tiers (Interface → Application → Domain → Infrastructure)
- **Communication:** Direct calls (hot path), Event bus (cross-cutting), Shared cache (reads)
- **Resilience:** Health Engine → Circuit Breaker → Retry Engine (3-tier stack)
- **Performance:** ~5.4ms gateway overhead, ~138MB memory per worker
- **Scalability:** Vertical (workers) + Horizontal (instances behind LB, shared PostgreSQL)
- **15 Design Decisions** documented as ADRs
