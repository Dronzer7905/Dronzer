from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any

from pydantic import BaseModel


class ProviderCapabilities(BaseModel):
    chat: bool = False
    vision: bool = False
    embeddings: bool = False
    images: bool = False
    audio: bool = False
    streaming: bool = False
    json_mode: bool = False
    structured_outputs: bool = False
    tool_calling: bool = False

class DiscoveredModel(BaseModel):
    id: str
    name: str
    context_window: int
    capabilities: ProviderCapabilities

class IProvider(ABC):
    """
    Abstract Base Class for all AI Providers.
    Every provider (built-in or plugin) must implement this interface.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """The canonical name of the provider (e.g., 'openai')."""
        pass

    @abstractmethod
    async def get_capabilities(self) -> ProviderCapabilities:
        """Returns the hardware/software capabilities of this provider SDK."""
        pass

    @abstractmethod
    async def discover_models(self, api_key: str, base_url: str | None = None) -> list[DiscoveredModel]:
        """Dynamically fetches available models from the provider's API."""
        pass

    @abstractmethod
    async def generate_chat(self, payload: dict[str, Any], api_key: str, base_url: str | None = None) -> dict[str, Any]:
        """Executes a standard chat completion request."""
        pass

    @abstractmethod
    async def generate_stream(self, payload: dict[str, Any], api_key: str, base_url: str | None = None) -> AsyncGenerator[dict[str, Any]]:
        """Executes a streaming chat completion request."""
        pass

    @abstractmethod
    async def check_health(self, api_key: str, base_url: str | None = None) -> bool:
        """Validates connectivity and authentication."""
        pass
