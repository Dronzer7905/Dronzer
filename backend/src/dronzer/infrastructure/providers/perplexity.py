import json
from collections.abc import AsyncGenerator
from typing import Any

import httpx
import structlog

from dronzer.domain.sdk.provider import DiscoveredModel, IProvider, ProviderCapabilities

logger = structlog.get_logger("dronzer.providers.perplexity")


class PerplexityProvider(IProvider):
    """
    Perplexity AI API integration (OpenAI compatible).
    """

    def __init__(self, default_base_url: str = "https://api.perplexity.ai"):
        self.default_base_url = default_base_url
        self._capabilities = ProviderCapabilities(
            chat=True,
            vision=False,
            embeddings=False,
            images=False,
            streaming=True,
            json_mode=False,
            tool_calling=False,
        )

    @property
    def provider_name(self) -> str:
        return "perplexity"

    async def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    async def discover_models(
        self, api_key: str, base_url: str | None = None
    ) -> list[DiscoveredModel]:
        # Perplexity does not have a public /models endpoint at the time of writing.
        static_models = [
            ("llama-3-sonar-small-32k-chat", 32768),
            ("llama-3-sonar-small-32k-online", 32768),
            ("llama-3-sonar-large-32k-chat", 32768),
            ("llama-3-sonar-large-32k-online", 32768),
        ]

        return [
            DiscoveredModel(
                id=m[0], name=m[0], context_window=m[1], capabilities=self._capabilities
            )
            for m in static_models
        ]

    async def generate_chat(
        self, payload: dict[str, Any], api_key: str, base_url: str | None = None
    ) -> dict[str, Any]:
        url = f"{base_url or self.default_base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "accept": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            return response.json()

    async def generate_stream(
        self, payload: dict[str, Any], api_key: str, base_url: str | None = None
    ) -> AsyncGenerator[dict[str, Any]]:
        url = f"{base_url or self.default_base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "accept": "application/json",
        }
        payload["stream"] = True

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST", url, headers=headers, json=payload, timeout=60.0
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        yield json.loads(line[6:])

    async def check_health(self, api_key: str, base_url: str | None = None) -> bool:
        # A simple dummy prompt to test auth since there is no models endpoint
        try:
            payload = {
                "model": "llama-3-sonar-small-32k-chat",
                "max_tokens": 1,
                "messages": [{"role": "user", "content": "hi"}],
            }
            await self.generate_chat(payload, api_key, base_url)
            return True
        except Exception:
            return False
