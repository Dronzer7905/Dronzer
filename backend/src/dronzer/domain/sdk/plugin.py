from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class PluginMetadata(BaseModel):
    name: str
    version: str
    description: str
    author: str
    dependencies: list[str] = []

class IPlugin(ABC):
    """
    Abstract Base Class for all Gateway Plugins.
    Plugins can register new providers, routing strategies, or intercept the pipeline.
    """

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        pass

    @abstractmethod
    async def on_startup(self) -> None:
        """Called when the plugin is loaded into the gateway."""
        pass

    @abstractmethod
    async def on_shutdown(self) -> None:
        """Called when the plugin is unloaded or gateway shuts down."""
        pass

    @abstractmethod
    def get_providers(self) -> list[Any]:
        """Returns a list of IProvider instances implemented by this plugin."""
        return []
