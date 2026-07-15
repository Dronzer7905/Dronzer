# Dronzer v2.0 Support Matrices

This document provides the definitive Compatibility Matrix for Dronzer v2.0, confirming Enterprise Readiness across infrastructure, LLM providers, and plugins.

## Supported Provider & Model Matrix

| Provider | Supported Models | Streaming | Function Calling | Vision | Status |
|---|---|:---:|:---:|:---:|:---:|
| **OpenAI** | `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo` | ✅ | ✅ | ✅ | Stable |
| **Anthropic** | `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, `claude-3-haiku-20240307` | ✅ | ✅ | ✅ | Stable |
| **Google** | `gemini-1.5-pro`, `gemini-1.5-flash` | ✅ | ✅ | ✅ | Stable |
| **Mistral** | `mistral-large-latest`, `mistral-small-latest` | ✅ | ✅ | ❌ | Stable |
| **Cohere** | `command-r-plus`, `command-r` | ✅ | ✅ | ❌ | Stable |
| **Groq** | `llama3-70b-8192`, `mixtral-8x7b-32768` | ✅ | ❌ | ❌ | Stable |
| **Local (Ollama)** | `llama3`, `phi3`, `mistral` | ✅ | ❌ | ❌ | Stable |

## Supported Vector Database Matrix (Knowledge Platform)

| Vector DB | Cloud Hosted | Self Hosted | Hybrid Search | Role-Based Access |
|---|:---:|:---:|:---:|:---:|
| **Pinecone** | ✅ | ❌ | ✅ | ✅ |
| **Qdrant** | ✅ | ✅ | ✅ | ✅ |
| **Milvus** | ✅ | ✅ | ✅ | ✅ |
| **Weaviate** | ✅ | ✅ | ✅ | ✅ |
| **pgvector** | ✅ | ✅ | ❌ | ✅ |

## Supported Authentication Matrix

| Method | Tenant Isolation | MFA Supported | Status |
|---|:---:|:---:|:---:|
| **API Keys (Bearer)** | ✅ | N/A | Stable |
| **OAuth2 / OIDC** | ✅ | ✅ | Stable |
| **SAML (Enterprise)** | ✅ | ✅ | Stable |

## Infrastructure Compatibility Matrix

| Component | Minimum Version | Recommended Version |
|---|---|---|
| **Python** | 3.10 | 3.13 |
| **PostgreSQL** | 15.0 | 16.0 |
| **Redis** | 6.2 | 7.0+ |
| **Kubernetes** | 1.25 | 1.29 |
