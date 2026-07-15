import random
import uuid

import structlog

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.infrastructure.database.models.ai import APIKey

logger = structlog.get_logger("dronzer.orchestration.key_rotation")


class APIKeyRotationEngine:
    """
    Selects the optimal API Key for a given provider, handling
    round-robin, weights, and health validation.
    Queries the database directly via a per-request session.
    """

    async def select_key(self, provider_id: uuid.UUID, session: AsyncSession) -> APIKey | None:
        """
        Pulls all active keys for the provider and selects one using weighted random choice.
        This provides load balancing across multiple keys.
        """
        result = await session.execute(
            select(APIKey).where(
                APIKey.provider_id == provider_id,
                APIKey.is_active == True,
                APIKey.is_deleted == False,
            )
        )
        valid_keys = list(result.scalars().all())

        if not valid_keys:
            logger.error("No active API keys found for provider", provider_id=str(provider_id))
            return None

        # Weighted random selection
        total_weight = sum(k.weight for k in valid_keys)
        if total_weight == 0:
            return random.choice(valid_keys)

        rand = random.uniform(0, total_weight)
        cumulative = 0.0

        for key in valid_keys:
            cumulative += key.weight
            if rand < cumulative:
                return key

        return valid_keys[-1]

    async def get_all_keys(self, provider_id: uuid.UUID, session: AsyncSession) -> list[APIKey]:
        """
        Retrieves all active API keys for a provider.
        Randomizes them to distribute load, then sorts by weight (highest priority first).
        """
        result = await session.execute(
            select(APIKey).where(
                APIKey.provider_id == provider_id,
                APIKey.is_active == True,
                APIKey.is_deleted == False,
            )
        )
        valid_keys = list(result.scalars().all())

        if not valid_keys:
            logger.error("No active API keys found for provider", provider_id=str(provider_id))
            return []

        # Shuffle first so equal weights are randomized
        random.shuffle(valid_keys)
        # Sort by weight descending (Python's sort is stable, so ties remain randomized)
        valid_keys.sort(key=lambda k: k.weight, reverse=True)
        return valid_keys
