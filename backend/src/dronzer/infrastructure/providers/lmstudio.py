import json
from collections.abc import AsyncGenerator
from typing import Any

import httpx
import structlog

from dronzer.domain.sdk.provider import DiscoveredModel, IProvider, ProviderCapabilities

logger = structlog.get_logger("dronzer.providers.lmstudio")


class LMStudioProvider(IProvider):
    """
    LM Studio Local API integration (OpenAI compatible).
    """

    def __init__(self, default_base_url: str = "http://localhost:1234/v1"):
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
        return "lmstudio"

    async def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    async def discover_models(
        self, api_key: str, base_url: str | None = None
    ) -> list[DiscoveredModel]:
        url = f"{base_url or self.default_base_url}/models"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            models = []
            for item in data.get("data", []):
                models.append(
                    DiscoveredModel(
                        id=item["id"],
                        name=item["id"],
                        context_window=4096,  # LM Studio usually runs limited context GGUFs
                        capabilities=self._capabilities,
                    )
                )
            return models

    async def generate_chat(
        self, payload: dict[str, Any], api_key: str, base_url: str | None = None
    ) -> dict[str, Any]:
        url = f"{base_url or self.default_base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=300.0)
            response.raise_for_status()
            return response.json()

    async def generate_stream(
        self, payload: dict[str, Any], api_key: str, base_url: str | None = None
    ) -> AsyncGenerator[dict[str, Any]]:
        url = f"{base_url or self.default_base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload["stream"] = True

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST", url, headers=headers, json=payload, timeout=300.0
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        yield json.loads(line[6:])

    async def check_health(self, api_key: str, base_url: str | None = None) -> bool:
        try:
            url = f"{base_url or self.default_base_url}/models"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False
