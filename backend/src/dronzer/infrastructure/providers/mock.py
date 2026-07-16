import asyncio
import time
from collections.abc import AsyncGenerator
from typing import Any

import structlog

from dronzer.domain.sdk.provider import DiscoveredModel, IProvider, ProviderCapabilities

logger = structlog.get_logger("dronzer.providers.mock")


class MockProvider(IProvider):
    """
    Mock Provider for automated integration testing and local development.
    Does not require network access.
    """

    def __init__(self):
        self._capabilities = ProviderCapabilities(
            chat=True,
            vision=True,
            embeddings=True,
            images=True,
            streaming=True,
            json_mode=True,
            tool_calling=True,
        )

    @property
    def provider_name(self) -> str:
        return "mock"

    async def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    async def discover_models(
        self, api_key: str, base_url: str | None = None
    ) -> list[DiscoveredModel]:
        return [
            DiscoveredModel(
                id="mock-model-1",
                name="Mock Model 1",
                context_window=100000,
                capabilities=self._capabilities,
            )
        ]

    async def generate_chat(
        self, payload: dict[str, Any], api_key: str, base_url: str | None = None
    ) -> dict[str, Any]:
        # Simulate network latency
        await asyncio.sleep(0.1)

        # Test error injection
        if payload.get("model") == "trigger-error":
            raise Exception("Mock provider simulated error")

        return {
            "id": "mock_chat_123",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": payload.get("model", "mock-model-1"),
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "This is a mocked response for testing.",
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 5, "completion_tokens": 8, "total_tokens": 13},
        }

    async def generate_stream(
        self, payload: dict[str, Any], api_key: str, base_url: str | None = None
    ) -> AsyncGenerator[dict[str, Any]]:
        chunks = ["This ", "is ", "a ", "mocked ", "streamed ", "response."]
        for chunk in chunks:
            await asyncio.sleep(0.05)
            yield {
                "id": "mock_stream_123",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": payload.get("model", "mock-model-1"),
                "choices": [{"delta": {"content": chunk}, "finish_reason": None}],
            }
        # Final chunk
        yield {
            "id": "mock_stream_123",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": payload.get("model", "mock-model-1"),
            "choices": [{"delta": {}, "finish_reason": "stop"}],
        }

    async def check_health(self, api_key: str, base_url: str | None = None) -> bool:
        return True
