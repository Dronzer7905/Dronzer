import json
from typing import Any

import redis.asyncio as redis
import structlog

from dronzer.core.config import settings
from dronzer.domain.ports import ICache

logger = structlog.get_logger("dronzer.cache.redis")


class RedisCache(ICache):
    """
    Distributed cache implementation using Redis.
    Required for multi-worker hot reloads and health sync.
    """
    def __init__(self) -> None:
        self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        logger.info("Redis cache initialized.")

    async def get(self, key: str) -> Any:
        try:
            val = await self.client.get(key)
            if val:
                return json.loads(val)
            return None
        except Exception as e:
            logger.error("Redis GET failed", key=key, exc_info=e)
            return None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        try:
            serialized = json.dumps(value)
            await self.client.set(key, serialized, ex=ttl)
        except Exception as e:
            logger.error("Redis SET failed", key=key, exc_info=e)

    async def delete(self, key: str) -> None:
        try:
            await self.client.delete(key)
        except Exception as e:
            logger.error("Redis DELETE failed", key=key, exc_info=e)
