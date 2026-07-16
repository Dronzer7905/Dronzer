# Dronzer Roadmap

This document outlines the planned development trajectory for the Dronzer AI Gateway following the v2.0.0 release.

> **Have a feature idea?** Open a [GitHub Discussion](https://github.com/dronzer7905/dronzer/discussions) — community input directly shapes this roadmap.

---

## ✅ Completed — v2.0.0 (July 2026)

- Task-Aware Decision Intelligence Engine
- 44+ free-tier provider integrations (Groq, Google AI Studio, Cerebras, Mistral, Cohere, OpenRouter, Fireworks, Together, Novita, Nebius)
- 3-Tier Failover Stack (HealthEngine → CircuitBreaker → RetryEngine)
- Clean Architecture FastAPI backend (Python 3.13+)
- Light Theme Next.js Admin Dashboard
- Prometheus metrics & Grafana dashboards
- Multi-Tenant RBAC (Organization → Project → Key)
- Encrypted API Key vault with intelligent LRU/Priority rotation
- Plugin system with sandboxed runtime
- Docker Compose and Kubernetes Helm Chart deployment

---

## 🚧 In Progress — v2.1 (Q3 2026)

### Advanced Load Balancing Strategies
Currently the engine uses Priority-based routing. v2.1 will introduce:
- **Round-Robin** — Distribute load evenly across healthy providers.
- **Latency-Based** — Route to the provider with the lowest measured P50 latency for the request's token volume.
- **Weighted** — Assign custom traffic percentages per provider (e.g., 70% Groq / 30% OpenRouter).

### Custom Provider UI (No Migrations Required)
Users will be able to define entirely custom API endpoints, authentication schemes, and models directly from the Admin Dashboard — without writing any code or running database migrations.

### Enhanced Seed Tooling
Automated provider health checking during seeding to skip providers that are temporarily unreachable, with a `--dry-run` flag for validation.

---

## 📅 Planned — v2.2 (Q4 2026)

### Cost Analytics Dashboard
Beautiful, interactive visualizations breaking down:
- Token usage and estimated USD spend per Provider, Model, Project, and API Key.
- Cost comparison: "What would this traffic cost at full OpenAI rate vs. current Dronzer routing?"
- Automatic budget alert thresholds with Slack/webhook notifications.

### Edge Deployment Proxies
Lightweight proxy nodes for deploying the Dronzer router to edge runtimes:
- **Cloudflare Workers** support for sub-10ms global routing.
- **Vercel Edge Functions** integration.

### Semantic Caching (Redis)
Cache semantically similar prompts to avoid redundant LLM calls. A Cosine Similarity check against cached embeddings will serve cached responses for queries with >95% semantic overlap, dramatically reducing costs.

---

## 🔮 Future Exploration (v3.x)

- **Dronzer CLI v2** — `dronzer run`, `dronzer prompt push`, `dronzer logs tail` for a first-class developer experience.
- **Native Agent Framework** — Built-in ReAct agent loop with tool registry and human-in-the-loop approval gates.
- **LLM-as-a-Judge Evaluator** — Automated quality scoring for A/B prompt experiments.
- **Rust-Based Hot Path** — A Rust reverse-proxy layer for ultra-low-latency passthrough on the gateway hot path.
