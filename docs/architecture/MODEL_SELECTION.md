# Dronzer AI Gateway — Model Selection & Orchestration Engine

**Document Status:** ✅ Approved  
**Version:** 1.0  
**Approved Date:** July 8, 2026  

> Full document available in conversation artifacts. This is the permanent reference summary.

## Core Philosophy
- **Fungible Resources:** Models are abstracted into combinations of Capabilities, Health, Performance, and Cost.
- **Explainable Decisions:** The engine logs deterministic, auditable reasons for every model selection.
- **Strict Capabilities:** Matching enforces strict boolean/enum checks (e.g., Vision, JSON mode).

## Scoring & Selection
- **Scoring Equation:** Computes a composite score based on weighted factors: Latency, Cost, Health, and Quality.
- **Dynamic Groups:** Clients request logical groups (e.g., `model="fast-and-cheap"`) instead of hardcoded model names.
- **O(1) Resolution:** Group expansion and alias mapping happen entirely in-memory using hash maps.

## Lifecycle & Discovery
- **Auto-Discovery:** Background jobs scrape provider APIs to dynamically populate the registry.
- **Health Tracking:** Distinct from API Key health; tracking model-specific 5xx rates and TTFT (Time-to-First-Token).

## Approved Open Decisions
- **Capability Enforcement:** Fail Fast. Reject requests if a requested capability (e.g., Vision payload) isn't matched by the requested model; no silent upgrades.
- **Discovery Source of Truth:** Admin manual overrides always lock and win against API auto-discovery.
- **Benchmarking Standard:** Standardize on `tiktoken` equivalent logic internally to normalize Token-Per-Second metrics across providers.
