import json
import logging
from typing import Any

from redis.asyncio import Redis

logger = logging.getLogger("dronzer.infrastructure.cache")


class DistributedCache:
    """
    Enterprise caching layer supporting Redis distributed caching with TTLs,
    cache warming, and invalidation strategies.
    """

    def __init__(self, redis_client: Redis, prefix: str = "dronzer:cache:"):
        self.redis = redis_client
        self.prefix = prefix

    def _key(self, key: str) -> str:
        return f"{self.prefix}{key}"

    async def get(self, key: str) -> Any | None:
        """Retrieves a value from the cache."""
        try:
            val = await self.redis.get(self._key(key))
            if val:
                return json.loads(val)
            return None
        except Exception as e:
            logger.warning(f"Cache GET failed for {key}: {e}")
            return None

    async def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> bool:
        """Sets a value in the cache with a Time-To-Live (TTL)."""
        try:
            serialized = json.dumps(value)
            await self.redis.setex(self._key(key), ttl_seconds, serialized)
            return True
        except Exception as e:
            logger.warning(f"Cache SET failed for {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Invalidates a specific cache key."""
        try:
            await self.redis.delete(self._key(key))
            return True
        except Exception as e:
            logger.warning(f"Cache DELETE failed for {key}: {e}")
            return False

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidates multiple cache keys matching a glob pattern."""
        try:
            keys = await self.redis.keys(self._key(pattern))
            if keys:
                await self.redis.delete(*keys)
            return len(keys)
        except Exception as e:
            logger.warning(f"Cache invalidate pattern failed for {pattern}: {e}")
            return 0

    async def warm(self, data_map: dict[str, Any], ttl_seconds: int = 86400):
        """Pre-warms the cache with multiple key-value pairs (e.g. at boot time)."""
        pipeline = self.redis.pipeline()
        for k, v in data_map.items():
            pipeline.setex(self._key(k), ttl_seconds, json.dumps(v))
        await pipeline.execute()
        logger.info(f"Cache warmed with {len(data_map)} items.")
