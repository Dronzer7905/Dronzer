# Dronzer AI Gateway — Developer Guide

Welcome to the Dronzer Developer Guide! This document walks you through integrating Dronzer into your applications, writing custom plugins, and interacting with the gateway programmatically.

---

## Quick Start — Connect Your Application

Dronzer is **100% compatible with the OpenAI API specification**. If you are using any OpenAI-compatible SDK, you only need to change the `base_url` (and optionally the `api_key`) to point at your Dronzer instance.

### Self-Hosted (Local Development)

```python
from openai import OpenAI

client = OpenAI(
    api_key="dz-sk-your_gateway_key",       # Generate from the Dronzer Dashboard
    base_url="http://localhost:8000/v1"      # Your local Dronzer instance
)
```

### Self-Hosted (Production)

```python
from openai import OpenAI

client = OpenAI(
    api_key="dz-sk-your_gateway_key",
    base_url="https://your-dronzer-domain.com/v1"    # Your deployed instance
)
```

```javascript
// Node.js
const OpenAI = require("openai");
const client = new OpenAI({
    apiKey: "dz-sk-your_gateway_key",
    baseURL: "http://localhost:8000/v1"    // or your production URL
});
```

---

## Requesting Models

### Auto-Routing (Recommended)
Let Dronzer's Decision Intelligence Engine choose the best available model:

```python
# Auto mode — routes to the globally best model for the task
response = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "Explain quantum computing."}]
)
```

### Task-Based Routing
Request a model optimized for a specific task category:

```python
# Coding task — routes to a code-optimized model (Qwen3-32B, DeepSeek V3, etc.)
response = client.chat.completions.create(
    model="coding",
    messages=[{"role": "user", "content": "Write a Python async HTTP client."}]
)

# Reasoning task — routes to a high-capability reasoning model (DeepSeek R1, etc.)
response = client.chat.completions.create(
    model="reasoning",
    messages=[{"role": "user", "content": "Solve this math problem step by step..."}]
)

# Vision task — routes to a vision-capable model (Gemini 2.5 Flash, Pixtral, etc.)
response = client.chat.completions.create(
    model="vision",
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "What's in this image?"},
        {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
    ]}]
)
```

### Direct Model Routing
Request a specific model — Dronzer translates to the appropriate provider API:

```python
# Request Claude — Dronzer routes to Anthropic's API automatically
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Request Gemini — Dronzer routes to Google AI Studio
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## Streaming Responses

Streaming works exactly as with the standard OpenAI SDK:

```python
stream = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "Write a poem about AI."}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

---

## Writing Custom Plugins

Dronzer supports a middleware plugin system. Plugins can intercept requests before they reach the provider or mutate responses before they are returned to the client.

To write a plugin, implement the `PluginInterface`:

```python
# backend/src/dronzer/domain/plugins/interface.py
from dronzer.domain.plugins.interface import PluginInterface

class MyCustomPlugin(PluginInterface):
    async def pre_process(self, request_data: dict) -> dict:
        # Modify the request before it reaches the LLM provider
        request_data["messages"].insert(0, {
            "role": "system",
            "content": "Always respond concisely."
        })
        return request_data

    async def post_process(self, response_data: dict) -> dict:
        # Modify the response before it reaches the consumer
        return response_data
```

Place your plugin file inside `backend/src/dronzer/application/plugins/` and it will be **automatically discovered and loaded at startup**.

Alternatively, drop a plugin into the `/plugins/` directory at the repo root for a zero-code-change deployment.

---

## Cursor IDE / Continue.dev Integration

To use Dronzer as the AI backend for your IDE extensions:

**Cursor IDE:**
1. Go to Settings → Models → Add Custom Model.
2. Set Base URL: `http://localhost:8000/v1`
3. Set API Key: `dz-sk-your_gateway_key`
4. Set Model Name: `coding` (or `auto`)

**Continue.dev (`~/.continue/config.json`):**
```json
{
  "models": [{
    "title": "Dronzer Gateway",
    "provider": "openai",
    "model": "auto",
    "apiBase": "http://localhost:8000/v1",
    "apiKey": "dz-sk-your_gateway_key"
  }]
}
```

---

## API Reference

The full OpenAPI specification is available at:
```
http://localhost:8000/docs       # Interactive Swagger UI
http://localhost:8000/openapi.json   # Raw OpenAPI schema
```
