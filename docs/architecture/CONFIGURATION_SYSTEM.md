# Dronzer AI Gateway — Configuration System Architecture

**Document Status:** ✅ Approved  
**Version:** 1.0  
**Approved Date:** July 8, 2026  

> Full document available in conversation artifacts. This is the permanent reference summary.

## Core Philosophy
- **Dynamic & Restart-less:** Changes to configuration apply instantly via an event bus.
- **Cache-Driven:** The proxy hot path reads strictly from an O(1) in-memory cache, never from the DB.
- **Safe Execution:** Strict schema validation and referential integrity checks on write.

## Configuration Hierarchy
Precedence order:
1. Emergency Override
2. Runtime Override (Header-based)
3. Project Override
4. Organization Override
5. Provider Override
6. Global Settings
7. Environment Variables (Secrets & Bootstrap only)
8. Code Defaults

## Hot Reload & Reliability
- **Write-Through Caching:** DB writes instantly update local cache and broadcast a targeted `ConfigChangedEvent`.
- **Periodic Sync:** A 60s background task verifies cache hash against DB to prevent drift.
- **Fail-Open Reads:** If the DB is unreachable, the gateway continues routing using the last known good cached configuration.

## Approved Open Decisions
- **Runtime Overrides:** Permitted via HTTP headers if `allow_consumer_routing_overrides` is enabled.
- **Draft/Publish Workflow:** Direct publishing for v1.0. Draft workflows deferred to v2.
- **Multi-Tenant Strictness:** Org settings act as Hard Limits for quotas and Defaults for behaviors.
