# Dronzer v2.0 Migration Guide

Welcome to Dronzer v2.0! This guide helps you transition your codebase, prompts, and infrastructure from the v1.x architecture to the new Universal AI Integration Platform.

## 1. Migrating Prompts to the Prompt Registry
In v1.x, you likely hardcoded prompts in your application code or stored them in a simple database.
In v2.0, **Prompts are treated as Code**.

**Action Required:**
1. Extract your prompts into `.jinja` files.
2. Use the new Dronzer CLI to push them to the registry:
   ```bash
   dronzer prompts push support-bot.jinja -m "Initial migration"
   ```
3. Update your application code to call the prompt by its ID via the SDK, rather than passing raw text strings.

## 2. Migrating to the Official SDKs
If you previously used raw `requests` or `httpx` to call the Dronzer API, we strongly recommend migrating to the official v2.0 SDKs.

**Python:**
```python
# Old v1.x
import httpx
res = httpx.post("https://api.dronzer.io/chat", json={"messages": [...]})

# New v2.0
from dronzer_client import DronzerClient
client = DronzerClient(api_key="...")
res = await client.execute_prompt(prompt_id="my-prompt", variables={"key": "val"})
```

## 3. Migrating Database Schemas
v2.0 introduces a strictly enforced multi-tenant RBAC schema. If you are self-hosting, you MUST run the Alembic migrations before starting the Gateway.
```bash
alembic upgrade head
```
*Note: SQLite is no longer supported for production. You must migrate to Postgres 15+.*
