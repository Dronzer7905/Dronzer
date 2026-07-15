import time
from typing import Any

import structlog

from dronzer.domain.ports import ICache

logger = structlog.get_logger("dronzer.cache.memory")


class MemoryCache(ICache):
    """
    In-memory L1 cache. Used as a fallback or for extremely hot paths
    like Configuration reads to avoid Redis network hops.
    """
    def __init__(self) -> None:
        # Map of key -> (value, expires_at_timestamp)
        self._store: dict[str, tuple[Any, float | None]] = {}
        logger.info("Memory L1 cache initialized.")

    async def get(self, key: str) -> Any:
        if key not in self._store:
            return None

        value, expires_at = self._store[key]
        if expires_at is not None and time.time() > expires_at:
            del self._store[key]
            return None

        return value

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        expires_at = time.time() + ttl if ttl else None
        self._store[key] = (value, expires_at)

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)
