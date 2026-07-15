# Dronzer AI Gateway - Developer Guide

Welcome to the Dronzer Developer Guide! This document will walk you through how to integrate Dronzer into your existing applications, write custom plugins, and interact with the gateway programmatically.

## Quick Start

The fastest way to get started with Dronzer is to treat it exactly like the OpenAI API. We designed the gateway to be **100% compliant** with the OpenAI specification.

### 1. Connecting Your App
If you are using the official OpenAI Python or Node.js SDK, you simply need to change the `base_url` parameter to point to your Dronzer instance.

**Python Example:**
```python
from openai import OpenAI
client = OpenAI(
    api_key="your-dronzer-api-key",
    base_url="https://api.dronzer.ai/v1"
)
```

**Node.js Example:**
```javascript
const OpenAI = require("openai");
const client = new OpenAI({
    apiKey: "your-dronzer-api-key",
    baseURL: "https://api.dronzer.ai/v1"
});
```

### 2. Requesting Any Model
Because Dronzer handles the provider translation layer, you can request Anthropic, Google, or Groq models directly through the OpenAI SDK!

```python
response = client.chat.completions.create(
    model="claude-3-opus", # Dronzer translates this to Anthropic's API!
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Writing Custom Plugins
Dronzer supports a powerful middleware plugin system. Plugins can intercept requests before they hit the provider, or mutate responses before they return to the client.

To write a plugin, implement the `PluginInterface` in `backend/src/dronzer/domain/plugins/interface.py`.

```python
class MyCustomPlugin(PluginInterface):
    async def pre_process(self, request_data: dict) -> dict:
        # Mutate the request here
        return request_data

    async def post_process(self, response_data: dict) -> dict:
        # Mutate the response here
        return response_data
```
Place your plugin inside `backend/src/dronzer/application/plugins/` and it will be dynamically loaded at boot.
