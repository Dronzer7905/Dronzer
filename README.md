# Dronzer AI Gateway 🚀

**Dronzer** is an enterprise-grade, open-source AI Orchestration Platform. It acts as the ultimate universal integration layer between your applications, internal knowledge, and the global ecosystem of Foundation Models — including OpenAI, Anthropic, Google AI Studio, Groq, OpenRouter, Mistral, Cerebras, and many more.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.13+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15+-black.svg)](https://nextjs.org/)
[![Status](https://img.shields.io/badge/Status-Production_Ready_v2.0-success)](https://github.com/dronzer7905/dronzer/releases)

---

## ✨ Core Features

### 🧠 Task-Aware Decision Engine
Don't hardcode models in your apps. Simply ask Dronzer for a `coding`, `reasoning`, `vision`, or `general` completion. The **Decision Intelligence Engine** analyzes your prompt and requirements (JSON mode, tool calling, vision payload) and dynamically routes to the optimal model globally.

### 🛡️ Ironclad Provider Failover
Never suffer from API downtime or rate limits again. Dronzer's `FailoverEngine` catches provider crashes (`429 Too Many Requests`, `500 Server Error`) and seamlessly re-routes to the next healthy provider in your fallback stack — within milliseconds. Your users will never know there was an outage.

### 🔑 Secure Gateway Keys
Generate Task-Aware API Keys from the Next.js dashboard. Bind keys to specific projects, enforce strict usage quotas, and restrict keys to specialized task types. All keys are encrypted at rest using Fernet symmetric encryption.

### 🔌 100% OpenAI-Compatible
Zero vendor lock-in. Dronzer is fully compliant with the OpenAI API specification. Point **Cursor IDE**, **Continue.dev**, **LangChain**, **LlamaIndex**, or any OpenAI SDK directly at your local Dronzer instance by simply overriding the `base_url`.

### 🎨 Minimal Light Theme Dashboard
A polished, professional Next.js dashboard to manage your providers, models, API keys, and routing policies — with live cost and usage analytics.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

| Dependency | Minimum Version | Notes |
|---|---|---|
| **Python** | 3.13+ | Backend runtime |
| **Node.js** | 20+ | Frontend dashboard |
| **PostgreSQL** | 15+ | Primary database |
| **Redis** | 7+ | Rate limiting & caching |

---

## 🚀 Getting Started

### Step 1 — Clone the Repository

```bash
git clone https://github.com/dronzer7905/dronzer.git
cd dronzer
```

### Step 2 — Backend Setup (FastAPI)

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Linux / macOS
# venv\Scripts\activate           # Windows

# Install all dependencies
pip install -r requirements.txt   # or: pip install -e ".[dev]" for dev extras
```

### Step 3 — Configure Environment Variables

```bash
# Copy the example env file and fill in your values
cp .env.example .env
```

Open `backend/.env` and set your database credentials and secret keys:

```env
DATABASE_URL=postgresql+asyncpg://dronzer:your_password@localhost:5433/dronzer_prod
SECRET_KEY=your_32_byte_secret_key_here
ENCRYPTION_KEY=your_32_byte_encryption_key_here
```

> **Tip:** Run `openssl rand -hex 32` to generate secure random keys.

### Step 4 — First-Time Database Setup

> ⚠️ **Important:** The database is empty after cloning. Models and providers do **NOT** auto-populate. You must run the following steps manually after the schema is created.

```bash
# 1. Apply all database migrations to create the schema
alembic upgrade head

# 2. Seed the database with 44+ pre-configured free-tier providers & models
#    This creates provider and model RECORDS only — not API keys
#    (Groq, Google AI Studio, Mistral, Cerebras, OpenRouter, Cloudflare, NVIDIA NIM, and more)
python scripts/seed_free_providers.py

# 3. Enrich model metadata (task types, capabilities, context windows)
python scripts/patch_model_metadata.py
```

> **What seeding does NOT do:** The seed scripts only create provider/model database records. They do **not** insert any API keys. You must add your own provider API keys in the next step.

### Step 5 — Initial Admin Setup & API Keys

Open the **Admin Dashboard** at `http://localhost:3000` (start the frontend first — see Step 6), then:

1. **Initial Setup:** On your first visit, you will be prompted to create your initial Super Admin account (email and password).
2. Go to **Providers** → click on any provider (e.g., Groq).
2. Click **"Add API Key"** and paste your key.
3. The key is **encrypted at rest** using Fernet symmetric encryption — it is never stored in plain text.

Free API keys for the seeded providers can be obtained here:

| Provider | Free API Key URL |
|---|---|
| Groq | https://console.groq.com/keys |
| Google AI Studio | https://aistudio.google.com/app/apikey |
| Mistral | https://console.mistral.ai/ |
| Cerebras | https://cloud.cerebras.ai/ |
| OpenRouter | https://openrouter.ai/settings/keys |
| Cloudflare Workers AI | https://dash.cloudflare.com/profile/api-tokens |
| NVIDIA NIM | https://build.nvidia.com/ |

> **No API key = no routing.** The gateway cannot forward requests to a provider until at least one API key is entered for that provider via the Dashboard.

### Step 6 — Start the Gateway Server

```bash
# From the backend directory (with venv activated)
fastapi run src/dronzer/main.py
# Gateway will be available at http://localhost:8000
```

### Step 7 — Frontend Setup (Next.js Dashboard)

```bash
cd ../frontend
npm install
npm run dev
# Dashboard available at http://localhost:3000
```

---

## 🧪 Quick Usage Example

Point any OpenAI-compatible SDK at your local gateway:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dz-sk-your_gateway_key"   # Generate this from the dashboard
)

# Dronzer routes this to the best available free model automatically
response = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "Explain quantum computing in simple terms."}]
)
print(response.choices[0].message.content)
```

```python
# Or request a specific task type — the engine picks the best model for the job
response = client.chat.completions.create(
    model="coding",   # Routes to a code-optimized model (e.g. Qwen3-32B or GPT-4o)
    messages=[{"role": "user", "content": "Write a Python async HTTP client."}]
)
```

---

## 🐳 Docker Compose (Quick Start)

The fastest way to run the full stack locally:

```bash
# From the repo root
docker-compose up -d

# Step 1: Apply schema and seed provider/model records (one-time setup)
docker exec -it dronzer-backend alembic upgrade head
docker exec -it dronzer-backend python scripts/seed_free_providers.py
docker exec -it dronzer-backend python scripts/patch_model_metadata.py
```

> **🔑 After seeding, open the Dashboard at `http://localhost:3000` and add your own API key for each provider.** The seed scripts only create provider/model records — no API keys are inserted automatically.


---

## 📁 Repository Structure

```
dronzer/
├── backend/                # Python FastAPI Gateway (Clean Architecture)
│   ├── src/dronzer/
│   │   ├── domain/         # Core business logic, no external deps
│   │   ├── application/    # Use cases, orchestration
│   │   ├── infrastructure/ # Database, Redis, HTTP clients
│   │   └── presentation/   # FastAPI routers, middleware
│   └── scripts/            # seed_free_providers.py, patch_model_metadata.py
├── frontend/               # Next.js Admin Dashboard (Light Theme)
├── docs/                   # Architecture, guides, reference docs
├── docker/                 # Dockerfiles
├── helm/                   # Kubernetes Helm charts
├── k8s/                    # Raw Kubernetes manifests
├── plugins/                # Drop-in gateway extension plugins
└── sdks/                   # Client SDKs
```

---

## 📖 Documentation

| Document | Description |
|---|---|
| [Architecture Overview](docs/architecture/ARCHITECTURE.md) | System design, subsystems, ADRs |
| [Developer Guide](docs/guides/developer-guide.md) | SDK integration, custom plugins |
| [Administrator Guide](docs/guides/administrator-guide.md) | Deployment, scaling, observability |
| [Enterprise Guide](docs/guides/enterprise-guide.md) | Multi-tenancy, SSO, compliance |
| [LLMOps Guide](docs/guides/llmops-guide.md) | Prompt registry, A/B testing, evaluation |
| [Breaking Changes](docs/guides/BREAKING_CHANGES.md) | v1.x → v2.0 migration notes |

---

## 🤝 Contributing

Pull requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on setting up the development environment, code style requirements, and submitting patches.

- **Bug Reports:** [Open an issue](https://github.com/dronzer7905/dronzer/issues/new?labels=bug&template=bug_report.md)
- **Feature Requests:** [Open a discussion](https://github.com/dronzer7905/dronzer/discussions)
- **Security Vulnerabilities:** [Report privately](https://github.com/dronzer7905/dronzer/security/advisories/new)

---

## 📄 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.
