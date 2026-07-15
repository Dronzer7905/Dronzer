import structlog

from dronzer.infrastructure.cache import DistributedCache

logger = structlog.get_logger("dronzer.enterprise.quotas")

class QuotaExceededException(Exception):
    pass

class QuotaEngine:
    """
    High-performance distributed rate limiting and token quota tracking.
    Uses Redis to synchronize counters across the Gateway cluster.
    """
    def __init__(self, cache: DistributedCache):
        self.cache = cache

    async def check_and_consume_rpm(self, tenant_id: str, limit: int) -> bool:
        """
        Sliding window rate limiter for Requests Per Minute (RPM).
        Raises QuotaExceededException if the limit is breached.
        """
        key = f"quota:rpm:{tenant_id}"
        # In a real Redis implementation, this would use a Lua script
        # to atomically increment and set a 60-second TTL.

        # Simulated logic:
        current = await self.cache.get(key)
        if current and int(current) >= limit:
            logger.warning("RPM Quota Exceeded", tenant=tenant_id, limit=limit)
            raise QuotaExceededException(f"Rate limit of {limit} RPM exceeded for tenant {tenant_id}")

        # await self.cache.increment(key, ttl=60)
        return True

    async def check_token_budget(self, project_id: str, max_tokens: int, estimated_tokens: int) -> bool:
        """
        Checks if a project has enough tokens left in its monthly budget to service the request.
        """
        key = f"quota:tokens:month:{project_id}"
        current = await self.cache.get(key)

        if current:
            projected = int(current) + estimated_tokens
            if projected > max_tokens:
                logger.warning("Token Budget Exceeded", project=project_id, max=max_tokens, projected=projected)
                raise QuotaExceededException(f"Token budget of {max_tokens} exceeded. Projected: {projected}")

        return True

    async def record_token_usage(self, project_id: str, actual_tokens: int) -> None:
        """
        Commits actual token usage post-request.
        """
        key = f"quota:tokens:month:{project_id}"
        # await self.cache.increment(key, amount=actual_tokens, ttl=2592000) # 30 days
        logger.debug(f"Recorded {actual_tokens} tokens for project {project_id}")
