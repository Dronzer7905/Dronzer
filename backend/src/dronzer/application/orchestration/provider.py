
import structlog

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.application.orchestration.context import DecisionContext
from dronzer.infrastructure.database.models.ai import Provider

logger = structlog.get_logger("dronzer.orchestration.provider")


class ProviderSelectionEngine:
    """
    Discovers and filters valid AI Providers based on routing rules and health.
    Queries the database directly via a per-request session.
    """

    async def filter_providers(self, context: DecisionContext, session: AsyncSession) -> list[Provider]:
        """
        Retrieves all active providers and filters out unhealthy ones 
        or those excluded by the tenant's RoutingPolicy.
        """
        logger.info("Filtering valid providers")

        result = await session.execute(
            select(Provider).where(
                Provider.is_active == True,
                Provider.is_deleted == False,
            )
        )
        active_providers = list(result.scalars().all())

        # Policy enforcement: If policy restricts to specific providers
        allowed_providers_config = context.active_policy.get("allowed_providers")

        if allowed_providers_config:
            active_providers = [
                p for p in active_providers
                if p.name in allowed_providers_config
            ]
            context.log_decision(
                step="ProviderSelection",
                action="FilterByPolicy",
                reason="Tenant policy restricted providers",
                metadata={"allowed": allowed_providers_config}
            )

        # Return remaining valid providers (CircuitBreaker checks happen later)
        context.valid_providers = [p.id for p in active_providers]
        return active_providers
