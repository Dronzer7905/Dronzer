import os

import httpx
import pytest

# Ensure the Gateway is running on localhost:8000 before executing E2E tests
GATEWAY_URL = os.getenv("DRONZER_GATEWAY_URL", "http://localhost:8000/v1")
API_KEY = os.getenv("DRONZER_E2E_API_KEY", "test-key-123")


@pytest.mark.asyncio
async def test_openai_chat_completion_compatibility():
    """
    Validates that the Gateway perfectly mocks the OpenAI /chat/completions endpoint
    and successfully routes a standard request.
    """
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a helpful test bot."},
            {"role": "user", "content": "Say 'hello world' and nothing else."},
        ],
        "temperature": 0.0,
        "max_tokens": 10,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GATEWAY_URL}/chat/completions", json=payload, headers=headers, timeout=30.0
        )

    assert response.status_code == 200, (
        f"Expected 200 OK, got {response.status_code}: {response.text}"
    )

    data = response.json()
    assert "id" in data, "Response missing 'id' field"
    assert data["object"] == "chat.completion", "Incorrect object type"
    assert len(data["choices"]) > 0, "No choices returned"

    message = data["choices"][0]["message"]
    assert message["role"] == "assistant", "Incorrect role"
    assert "hello world" in message["content"].lower(), f"Unexpected content: {message['content']}"

    assert "usage" in data, "Usage metadata missing"
    assert data["usage"]["total_tokens"] > 0, "Tokens not tracked"


@pytest.mark.asyncio
async def test_gateway_health():
    """Validates the health endpoint is active and reports Operational."""
    async with httpx.AsyncClient() as client:
        # Assuming health is mounted at root /health
        response = await client.get(f"{GATEWAY_URL.replace('/v1', '')}/health", timeout=5.0)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
