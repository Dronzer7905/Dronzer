import json
from collections.abc import AsyncGenerator
from typing import Any

import httpx
import structlog

from dronzer.domain.sdk.provider import DiscoveredModel, IProvider, ProviderCapabilities

logger = structlog.get_logger("dronzer.providers.gemini")


class GeminiProvider(IProvider):
    """
    Google Gemini (Vertex AI / Studio) API integration.
    """

    def __init__(
        self, default_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    ):
        self.default_base_url = default_base_url
        self._capabilities = ProviderCapabilities(
            chat=True,
            vision=True,
            embeddings=True,
            images=False,
            audio=True,
            streaming=True,
            json_mode=True,
            structured_outputs=True,
            tool_calling=True,
        )

    @property
    def provider_name(self) -> str:
        return "gemini"

    async def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    async def discover_models(
        self, api_key: str, base_url: str | None = None
    ) -> list[DiscoveredModel]:
        url = f"{base_url or self.default_base_url}/models?key={api_key}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            models = []
            for item in data.get("models", []):
                name = item["name"].replace("models/", "")
                models.append(
                    DiscoveredModel(
                        id=name,
                        name=item.get("displayName", name),
                        context_window=item.get("inputTokenLimit", 32768),
                        capabilities=self._capabilities,
                    )
                )
            return models

    async def generate_chat(
        self, payload: dict[str, Any], api_key: str, base_url: str | None = None
    ) -> dict[str, Any]:
        url = f"{base_url or self.default_base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            return response.json()

    async def generate_stream(
        self, payload: dict[str, Any], api_key: str, base_url: str | None = None
    ) -> AsyncGenerator[dict[str, Any]]:
        url = f"{base_url or self.default_base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
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
        try:
            url = f"{base_url or self.default_base_url}/models?key={api_key}"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False
