from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class ExtensionManifest(BaseModel):
    """
    Metadata describing the extension. Defines capabilities and versioning.
    """

    id: str = Field(..., description="Unique identifier for the extension, e.g. 'com.acme.logging'")
    name: str = Field(..., description="Human readable name")
    version: str = Field(..., description="Semantic version string")
    author: str = Field(..., description="Author or organization name")
    description: str = Field("", description="Brief description of functionality")
    dronzer_version: str = Field(..., description="Required Dronzer API version, e.g. '^1.0.0'")

    # Sandboxing Capabilities
    allow_network: bool = Field(
        False, description="Whether this extension is allowed to make outbound network requests"
    )
    allow_filesystem: bool = Field(
        False, description="Whether this extension is allowed to read/write to the filesystem"
    )
    allow_database: bool = Field(
        False, description="Whether this extension can access the Dronzer database via the SDK"
    )

    dependencies: list[str] = Field(
        default_factory=list, description="IDs of other extensions required"
    )


class ExtensionContext:
    """
    The context object passed to an extension upon activation.
    Provides isolated access to the Dronzer SDK API.
    """

    def __init__(self, api_facade: Any):
        self.api = api_facade
        self.state: dict[str, Any] = {}


class ExtensionBase(ABC):
    """
    The base class all Dronzer extensions must inherit from.
    """

    def __init__(self, manifest: ExtensionManifest):
        self.manifest = manifest

    @abstractmethod
    async def on_activate(self, context: ExtensionContext) -> None:
        """
        Called when the extension is loaded and enabled.
        Use this to register hooks, providers, or routes.
        """
        pass

    @abstractmethod
    async def on_deactivate(self) -> None:
        """
        Called when the extension is disabled or the gateway is shutting down.
        Use this to clean up resources.
        """
        pass
