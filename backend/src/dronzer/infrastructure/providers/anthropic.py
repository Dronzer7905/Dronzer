import json
from collections.abc import AsyncGenerator
from typing import Any

import httpx
import structlog

from dronzer.domain.sdk.provider import DiscoveredModel, IProvider, ProviderCapabilities

logger = structlog.get_logger("dronzer.providers.anthropic")

class AnthropicProvider(IProvider):
    """
    Anthropic API (Claude) integration.
    """

    def __init__(self, default_base_url: str = "https://api.anthropic.com/v1"):
        self.default_base_url = default_base_url
        self._capabilities = ProviderCapabilities(
            chat=True,
            vision=True,
            embeddings=False, # Handled via Voyage typically, but skipping here
            images=False,
            audio=False,
            streaming=True,
            json_mode=True, # Note: Anthropic doesn't have a strict JSON mode flag, just tool calling
            structured_outputs=True, # Via tool calling
            tool_calling=True
        )

    @property
    def provider_name(self) -> str:
        return "anthropic"

    async def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    async def discover_models(self, api_key: str, base_url: str | None = None) -> list[DiscoveredModel]:
        # Anthropic doesn't have a dynamic models endpoint like OpenAI, so we return a static list
        # based on their known capability matrix.
        static_models = [
            ("claude-3-opus-20240229", 200000),
            ("claude-3-sonnet-20240229", 200000),
            ("claude-3-haiku-20240307", 200000),
            ("claude-3-5-sonnet-20240620", 200000),
        ]

        return [
            DiscoveredModel(id=m[0], name=m[0], context_window=m[1], capabilities=self._capabilities)
            for m in static_models
        ]

    async def generate_chat(self, payload: dict[str, Any], api_key: str, base_url: str | None = None) -> dict[str, Any]:
        url = f"{base_url or self.default_base_url}/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()

            # Map Anthropic's response to the standard OpenAI-like schema expected by the gateway
            data = response.json()
            return {
                "id": data.get("id"),
                "object": "chat.completion",
                "model": payload.get("model", "unknown"),
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": data.get("content", [{}])[0].get("text", "")
                    },
                    "finish_reason": "stop" if data.get("stop_reason") == "end_turn" else data.get("stop_reason")
                }],
                "usage": {
                    "prompt_tokens": data.get("usage", {}).get("input_tokens", 0),
                    "completion_tokens": data.get("usage", {}).get("output_tokens", 0),
                }
            }

    async def generate_stream(self, payload: dict[str, Any], api_key: str, base_url: str | None = None) -> AsyncGenerator[dict[str, Any]]:
        url = f"{base_url or self.default_base_url}/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload["stream"] = True

        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, headers=headers, json=payload, timeout=60.0) as response:
                response.raise_for_status()
                # Streaming mapping logic omitted for brevity in Phase 14 foundation
                async for line in response.aiter_lines():
                    yield json.loads(line)

    async def check_health(self, api_key: str, base_url: str | None = None) -> bool:
        # A simple dummy prompt to test auth
        try:
            payload = {"model": "claude-3-haiku-20240307", "max_tokens": 1, "messages": [{"role": "user", "content": "hello"}]}
            await self.generate_chat(payload, api_key, base_url)
            return True
        except Exception:
            return False
