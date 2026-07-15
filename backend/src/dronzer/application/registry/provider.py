
import structlog

from dronzer.domain.sdk.provider import IProvider

logger = structlog.get_logger("dronzer.registry.provider")

class ProviderRegistry:
    """
    Central repository of all loaded AI Provider implementations.
    Allows dynamic lookup of provider SDKs at runtime.
    """

    def __init__(self):
        self._providers: dict[str, IProvider] = {}

    def register(self, provider: IProvider) -> None:
        """Registers a provider SDK."""
        name = provider.provider_name.lower()
        if name in self._providers:
            logger.warning("Overwriting existing provider registration", provider=name)

        self._providers[name] = provider
        logger.info("Provider registered successfully", provider=name)

    def unregister(self, provider_name: str) -> None:
        """Removes a provider SDK from the registry."""
        name = provider_name.lower()
        if name in self._providers:
            del self._providers[name]
            logger.info("Provider unregistered", provider=name)

    def get(self, provider_name: str) -> IProvider | None:
        """Retrieves a provider SDK by name."""
        return self._providers.get(provider_name.lower())

    def get_all(self) -> list[IProvider]:
        """Returns all registered provider SDKs."""
        return list(self._providers.values())
