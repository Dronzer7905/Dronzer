# Dronzer v2.0 Support Matrices

This document provides the definitive compatibility matrix for Dronzer v2.0, confirming enterprise readiness across infrastructure, LLM providers, and plugins.

---

## Supported Provider & Model Matrix

The following providers are pre-seeded by `seed_free_providers.py` (all free-tier unless noted):

| Provider | Key Models | Streaming | Function Calling | Vision | Status |
|---|---|:---:|:---:|:---:|:---:|
| **Groq** | llama-3.1-8b-instant, llama-3.3-70b-versatile, qwen3-32b, llama-4-scout, gpt-oss-120b, compound | ✅ | ✅ | ❌ | Stable |
| **Google AI Studio** | gemini-2.5-flash, gemini-2.5-flash-lite, gemini-3-flash, gemini-3.1-flash-lite | ✅ | ✅ | ✅ | Stable |
| **Cerebras** | llama-3.1-8b, llama-3.3-70b, llama-4-scout, llama-4-maverick, qwen3-32b | ✅ | ✅ | ❌ | Stable |
| **Mistral** | mistral-small-latest, mistral-medium-latest, pixtral-12b, devstral-small | ✅ | ✅ | ✅ (pixtral) | Stable |
| **Cohere** | command-a-03-2025, command-r7b-12-2024 | ✅ | ✅ | ❌ | Stable |
| **OpenRouter** | Multiple free-tier routing models | ✅ | ✅ | Varies | Stable |
| **Fireworks AI** | llama-4-scout, llama-4-maverick, deepseek-r2 | ✅ | ✅ | ❌ | Stable |
| **Together AI** | llama-3.3-70b-turbo, deepseek-v3, deepseek-r1 | ✅ | ✅ | ❌ | Stable |
| **Novita AI** | llama-3.1-8b, llama-3.1-70b, phi-4 | ✅ | ✅ | ❌ | Stable |
| **Nebius AI Studio** | llama-3.3-70b, deepseek-v3 | ✅ | ✅ | ❌ | Stable |
| **OpenAI** *(BYOK)* | gpt-4o, gpt-4-turbo, gpt-3.5-turbo | ✅ | ✅ | ✅ | Stable |
| **Anthropic** *(BYOK)* | claude-3-5-sonnet, claude-3-haiku | ✅ | ✅ | ✅ | Stable |
| **Local (Ollama)** | llama3, phi3, mistral (any installed model) | ✅ | ❌ | ❌ | Stable |

> **BYOK** = Bring Your Own Key — provider requires you to supply your own paid API key via the Admin Dashboard.
> **Free-tier providers** also require you to enter your own API key via the Dashboard — the seed script only creates the provider/model records, not the keys.
> Get free keys at: [Groq](https://console.groq.com/keys) · [Google AI Studio](https://aistudio.google.com/app/apikey) · [OpenRouter](https://openrouter.ai/settings/keys) · [Cerebras](https://cloud.cerebras.ai/) · [NVIDIA NIM](https://build.nvidia.com/)

---

## Supported Vector Database Matrix (Knowledge Platform)

| Vector DB | Cloud Hosted | Self Hosted | Hybrid Search | Role-Based Access |
|---|:---:|:---:|:---:|:---:|
| **Qdrant** | ✅ | ✅ | ✅ | ✅ |
| **Pinecone** | ✅ | ❌ | ✅ | ✅ |
| **Milvus** | ✅ | ✅ | ✅ | ✅ |
| **Weaviate** | ✅ | ✅ | ✅ | ✅ |
| **pgvector** | ✅ | ✅ | ❌ | ✅ |

---

## Supported Authentication Matrix

| Method | Tenant Isolation | MFA Supported | Status |
|---|:---:|:---:|:---:|
| **API Keys (Bearer `dz-sk-...`)** | ✅ | N/A | Stable |
| **OAuth2 / OIDC** | ✅ | ✅ | Stable |
| **SAML 2.0 (Enterprise SSO)** | ✅ | ✅ | Stable |
| **SCIM 2.0 (Directory Sync)** | ✅ | ✅ | Stable |

---

## Infrastructure Compatibility Matrix

| Component | Minimum Version | Recommended Version | Notes |
|---|---|---|---|
| **Python** | 3.10 | 3.13 | 3.13 required for latest performance improvements |
| **PostgreSQL** | 15.0 | 16.0 | 15+ required for Declarative Partitioning features |
| **Redis** | 6.2 | 7.2+ | 7+ recommended for Redis Streams (Pub/Sub) |
| **Node.js** | 20.0 | 22.0 | For building the frontend dashboard |
| **Kubernetes** | 1.25 | 1.29 | For Helm chart deployments |
| **Docker** | 24.0 | Latest | For Docker Compose deployments |
