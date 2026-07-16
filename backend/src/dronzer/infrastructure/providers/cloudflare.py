import json
from collections.abc import AsyncGenerator
from typing import Any

import httpx
import structlog

from dronzer.domain.sdk.provider import DiscoveredModel, IProvider, ProviderCapabilities

logger = structlog.get_logger("dronzer.providers.cloudflare")


class CloudflareProvider(IProvider):
    """
    Cloudflare Workers AI integration (OpenAI compatible).
    Note: Requires account ID in base URL: https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1
    """

    def __init__(
        self,
        default_base_url: str = "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1",
    ):
        self.default_base_url = default_base_url
        self._capabilities = ProviderCapabilities(
            chat=True,
            vision=True,
            embeddings=True,
            images=True,
            streaming=True,
            json_mode=False,
            tool_calling=False,
        )

    @property
    def provider_name(self) -> str:
        return "cloudflare-workers-ai"

    def _resolve_url(self, base_url: str | None, endpoint: str) -> str:
        url = base_url or self.default_base_url
        if "{account_id}" in url:
            # Note: For production use, the user must provide the base URL
            # containing their actual account ID in the UI/DB.
            logger.warning(
                "Cloudflare account_id in base URL was not resolved. Ensure the base URL is set in the database."
            )

        return f"{url.rstrip('/')}/{endpoint.lstrip('/')}"

    async def get_capabilities(self) -> ProviderCapabilities:
        return self._capabilities

    async def discover_models(
        self, api_key: str, base_url: str | None = None
    ) -> list[DiscoveredModel]:
        # Cloudflare's OpenAI compatible /models endpoint
        url = self._resolve_url(base_url, "models")
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            models = []
            for item in data.get("data", []):
                models.append(
                    DiscoveredModel(
                        id=item["id"],
                        name=item["id"],
                        context_window=8192,
                        capabilities=self._capabilities,
                    )
                )
            return models

    async def generate_chat(
        self, payload: dict[str, Any], api_key: str, base_url: str | None = None
    ) -> dict[str, Any]:
        url = self._resolve_url(base_url, "chat/completions")
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=120.0)
            response.raise_for_status()
            return response.json()

    async def generate_stream(
        self, payload: dict[str, Any], api_key: str, base_url: str | None = None
    ) -> AsyncGenerator[dict[str, Any]]:
        url = self._resolve_url(base_url, "chat/completions")
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload["stream"] = True

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST", url, headers=headers, json=payload, timeout=120.0
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        yield json.loads(line[6:])

    async def check_health(self, api_key: str, base_url: str | None = None) -> bool:
        try:
            url = self._resolve_url(base_url, "models")
            headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False
