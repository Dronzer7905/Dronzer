# Dronzer AI Gateway 🚀

**Dronzer** is an enterprise-grade, open-source AI Orchestration Platform. It acts as the ultimate universal integration layer between your applications, internal knowledge, and the global ecosystem of Foundation Models (OpenAI, Anthropic, Gemini, Groq, OpenRouter, Mistral, Cerebras, and more).

![Status](https://img.shields.io/badge/Status-Production_Ready_v2.0-success)
![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Core Features

### 🧠 Task-Aware Decision Engine
Don't hardcode models in your apps. Simply ask Dronzer for a "Coding", "Reasoning", "Vision", or "General Chat" completion. The **Decision Intelligence Engine** analyzes your prompt and requirements (e.g. JSON mode, Tool Calling) and dynamically routes your request to the optimal model architecture globally.

### 🛡️ Ironclad Provider Failover
Never suffer from API downtime or rate limits again. Dronzer's robust `FailoverEngine` catches provider crashes (`429 Too Many Requests`, `500 Server Error`) and seamlessly re-routes the payload to the next healthy provider in your fallback stack within milliseconds. Your users will never know there was an outage.

### 🔑 Secure Gateway Keys
Manage access dynamically. Generate Task-Aware API Keys from the beautiful Next.js dashboard. You can bind keys to specific projects, enforce strict usage quotas, and restrict keys to specialized task types.

### 🔌 100% OpenAI Compatible
Zero vendor lock-in. Dronzer is fully compliant with the standard OpenAI API structure. You can instantly point **Cursor IDE**, **Continue.dev**, **LangChain**, or any standard OpenAI SDK directly at your local Dronzer instance by simply overriding the `base_url`.

---

## 🎨 Minimal Light Theme Dashboard
Dronzer ships with a highly polished, professional Light Theme Next.js dashboard to manage your providers, models, and API keys.

## 🚀 Getting Started

### 1. Backend Setup (FastAPI & PostgreSQL)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Or venv\\Scripts\\activate on Windows
pip install -r requirements.txt

# Seed the database with 45+ pre-configured Free Tier Models
python scripts/seed_free_providers.py
python scripts/patch_model_metadata.py

# Start the Gateway Server
fastapi run src/dronzer/main.py
```

### 2. Frontend Setup (Next.js)
```bash
cd frontend
npm install
npm run dev
```

### 3. Usage Example
Point any OpenAI SDK to your gateway!

```python
from openai import OpenAI

client = OpenAI(
  base_url="http://localhost:8000/v1",
  api_key="dz-sk-your_gateway_key"
)

# Dronzer will dynamically route this to the best model available!
response = client.chat.completions.create(
  model="auto",
  messages=[{"role": "user", "content": "Explain quantum computing."}]
)
print(response.choices[0].message.content)
```

## 🤝 Contributing
Pull requests are welcome! Feel free to add support for new Foundation Model providers or improve the Decision Engine's load balancing algorithms.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
