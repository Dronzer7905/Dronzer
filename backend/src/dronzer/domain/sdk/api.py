from typing import Any

import structlog

from dronzer.infrastructure.cache import DistributedCache


class ExtensionLogFacade:
    def __init__(self, extension_id: str):
        self._logger = structlog.get_logger(f"dronzer.ext.{extension_id}")

    def info(self, msg: str, **kwargs):
        self._logger.info(msg, **kwargs)

    def error(self, msg: str, **kwargs):
        self._logger.error(msg, **kwargs)

    def warn(self, msg: str, **kwargs):
        self._logger.warning(msg, **kwargs)

    def debug(self, msg: str, **kwargs):
        self._logger.debug(msg, **kwargs)


class ExtensionCacheFacade:
    def __init__(self, cache: DistributedCache, extension_id: str):
        self._cache = cache
        self._prefix = f"ext:{extension_id}:"

    async def get(self, key: str) -> Any | None:
        return await self._cache.get(f"{self._prefix}{key}")

    async def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> bool:
        return await self._cache.set(f"{self._prefix}{key}", value, ttl_seconds)


class DronzerExtensionAPI:
    """
    The facade providing controlled access to Dronzer core services.
    Passed to ExtensionContext.
    """

    def __init__(self, extension_id: str, cache: DistributedCache):
        self.logger = ExtensionLogFacade(extension_id)
        self.cache = ExtensionCacheFacade(cache, extension_id)

        # In a full implementation, this would also expose Database facades,
        # Metrics registries, and Event Bus publishers, properly isolated
        # by the extension_id to prevent naming collisions.
