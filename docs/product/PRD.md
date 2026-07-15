# Product Requirements Document — Dronzer AI Gateway

**Document Status:** ✅ Approved  
**Version:** 1.0  
**Approved Date:** July 8, 2026  

> This document was approved and is the single source of truth for all product decisions.  
> See the full document in the conversation artifacts for the complete 25-section PRD.

## Approved Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Project Name | **Dronzer** | User-selected |
| Language | **Python** | User-selected. I/O-bound workload suitable for async Python. Large contributor pool for AI projects. |
| Database | **PostgreSQL (primary) + SQLite (alternative)** | Most reliable relational database. SQLite for onboarding ease. |
| Dashboard | **React SPA (embedded)** | Most mature frontend ecosystem, largest contributor pool. |
| License | **Apache 2.0** | Patent protection, enterprise-preferred. |
| Initial Providers | **OpenAI, Anthropic, Google AI, Mistral, Cohere, Groq, AWS Bedrock, Azure OpenAI, OpenRouter, Ollama** | Covers production-critical surface. More via dashboard. |
| Telemetry | **None** | Trust-first open-source strategy. |

## Key Product Requirements Summary

- Enterprise-grade, open-source, self-hosted AI Gateway
- "NGINX for AI" — transparent proxy with unified OpenAI-compatible API
- Fully database-driven — zero code changes after deployment
- Dashboard for all administrative operations
- Unlimited providers, models, API keys — all managed dynamically
- Automatic failover at provider, model, and key levels
- Intelligent routing (priority, round-robin, weighted, least-latency)
- Health engine with real-time tracking
- Circuit breaker per provider
- Plugin architecture for extensibility
- Streaming, embeddings, vision, image generation support
- Apache 2.0 licensed, no enterprise paywall
