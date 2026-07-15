# Dronzer AI Gateway — Database Architecture Blueprint

**Document Status:** ✅ Approved  
**Version:** 1.0  
**Approved Date:** July 8, 2026  

> Full document available in conversation artifacts. This is the permanent reference summary.

## Database Philosophy
- **Control Plane:** The database entirely dictates the gateway's routing, health, and plugin logic.
- **Cache-Accelerated:** Reads are handled via in-memory/Redis cache; writes are for configuration and telemetry.

## Core Domains
1. Provider Management
2. Model Management
3. API Key Management
4. Routing System
5. Health & Circuit Breaker System
6. Plugin System
7. Security & Identity (Multi-tenant ready)
8. Observability (Logs, Metrics)
9. Background Services
10. Configuration System

## Structural Design
- **Entities & Aggregates:** Driven by DDD (Domain-Driven Design).
- **Soft Deletion:** Core entities use `deleted_at` to preserve referential integrity for logs.
- **Partitioning:** High-volume logs use time-based Declarative Partitioning.
- **Primary Keys:** UUIDv4 globally.

## Security & Reliability
- **Encryption:** Symmetric (Fernet) column-level encryption for API Keys.
- **History Tracking:** Config changes use `_history` tables via PostgreSQL triggers.
- **Consistency:** Strict Foreign Keys; no Deferred Constraints.
