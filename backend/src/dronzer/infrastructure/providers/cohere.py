import json
from collections.abc import AsyncGenerator
from typing import Any

import httpx
import structlog

from dronzer.domain.sdk.provider import DiscoveredModel, IProvider, ProviderCapabilities

logger = structlog.get_logger("dronzer.providers.cohere")


class CohereProvider(IProvider):
    """
    Cohere API integration. Uses Cohere's /v1/chat endpoint which is unique.
    """

    def __init__(self, default_base_url: str = "https://api.cohere.ai/v1"):
        self.default_base_url = default_base_url
        self._capabilities = ProviderCapabilities(
            chat=True,
            vision=False,
            embeddings=True,
            images=False,
            streaming=True,
            json_mode=True,
            tool_calling=True,
        )

    @property
    def provider_name(self) -> str:
        return "cohere"

    async def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    async def discover_models(
        self, api_key: str, base_url: str | None = None
    ) -> list[DiscoveredModel]:
        url = f"{base_url or self.default_base_url}/models"
        headers = {"Authorization": f"Bearer {api_key}", "accept": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            models = []
            for item in data.get("models", []):
                if "chat" in item.get("endpoints", []):
                    models.append(
                        DiscoveredModel(
                            id=item["name"],
                            name=item["name"],
                            context_window=item.get("context_length", 128000),
                            capabilities=self._capabilities,
                        )
                    )
            return models

    async def generate_chat(
        self, payload: dict[str, Any], api_key: str, base_url: str | None = None
    ) -> dict[str, Any]:
        # Pre-plugin must map OpenAI payload to Cohere payload.
        url = f"{base_url or self.default_base_url}/chat"
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
        url = f"{base_url or self.default_base_url}/chat"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "accept": "application/stream+json",
        }
        payload["stream"] = True

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST", url, headers=headers, json=payload, timeout=60.0
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        yield json.loads(line)

    async def check_health(self, api_key: str, base_url: str | None = None) -> bool:
        try:
            url = f"{base_url or self.default_base_url}/models"
            headers = {"Authorization": f"Bearer {api_key}"}
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False
