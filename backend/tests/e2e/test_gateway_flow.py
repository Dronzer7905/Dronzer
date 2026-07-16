import os
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from dronzer.presentation.api.server import create_app

# Ensure the Gateway is running on localhost:8000 before executing E2E tests
GATEWAY_URL = os.getenv("DRONZER_GATEWAY_URL", "http://localhost:8000/v1")
API_KEY = os.getenv("DRONZER_E2E_API_KEY", "test-key-123")

app = create_app()


@pytest.mark.asyncio
@patch("dronzer.presentation.api.middleware.auth.async_session_factory")
async def test_openai_chat_completion_compatibility(mock_factory):
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

    # Mock DB session for middleware
    mock_session = AsyncMock()
    mock_factory.return_value.__aenter__.return_value = mock_session
    mock_result = MagicMock()
    mock_db_key = MagicMock()
    mock_db_key.id = "mock-id"
    mock_db_key.organization_id = "org-id"
    mock_db_key.project_id = "proj-id"
    mock_db_key.task_type = "general"
    mock_db_key.model_priorities = []
    mock_db_key.provider_priorities = []
    mock_result.scalars().first.return_value = mock_db_key
    mock_session.execute.return_value = mock_result

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # We need to mock the pipeline otherwise it will try to call real OpenAI
        class MockPipeline:
            async def execute(self, request, *args, **kwargs):
                import time

                from dronzer.domain.entities.chat import (
                    ChatChoice,
                    ChatCompletionResponse,
                    ChatMessage,
                    ChatUsage,
                )

                return ChatCompletionResponse(
                    id="test-id",
                    created=int(time.time()),
                    model="gpt-4o",
                    choices=[
                        ChatChoice(
                            index=0,
                            finish_reason="stop",
                            message=ChatMessage(role="assistant", content="hello world"),
                        )
                    ],
                    usage=ChatUsage(prompt_tokens=10, completion_tokens=10, total_tokens=20),
                )

        app.state.pipeline = MockPipeline()
        response = await client.post(
            "/v1/chat/completions", json=payload, headers=headers, timeout=30.0
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
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health/liveness", timeout=5.0)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
