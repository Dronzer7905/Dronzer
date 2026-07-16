import structlog

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.application.orchestration.capability import CapabilityEngine
from dronzer.application.orchestration.context import DecisionContext
from dronzer.infrastructure.database.models.ai import Model

logger = structlog.get_logger("dronzer.orchestration.model")


class ModelSelectionEngine:
    """
    Discovers, filters, and matches models based on capabilities, context window, and aliases.
    Queries the database directly via a per-request session.
    """

    async def filter_models(self, context: DecisionContext, session: AsyncSession) -> list[Model]:
        """
        Filters models belonging to valid providers that satisfy
        the requested capabilities and context window.
        """
        logger.info("Filtering valid models")

        result = await session.execute(
            select(Model).where(
                Model.is_active == True,
                Model.is_deleted == False,
            )
        )
        all_models = list(result.scalars().all())
        valid_models = []

        requested = context.request_context.requested_model
        for model in all_models:
            logger.info(f"Checking model {model.name} with requested {requested}")
            # 1. Must belong to a valid provider
            if model.provider_id not in context.valid_providers:
                logger.info(f"Model {model.name} failed provider check")
                continue

            # 2. Must satisfy context window
            if context.request_context.estimated_prompt_tokens > model.context_window:
                logger.info(f"Model {model.name} failed context window check")
                continue

            # 3. Must satisfy capabilities (e.g. vision, json_mode)
            if not CapabilityEngine.matches(
                context.request_context.requested_capabilities, model.capabilities
            ):
                logger.warning(
                    f"Model {model.name} failed capability check. Req: {context.request_context.requested_capabilities}, Prov: {model.capabilities}"
                )
                continue

            logger.info(f"Model {model.name} passed capability check.")

            # 4. Name matching or Alias resolution
            if requested:
                # If the user requests "auto", bypass the strict name check
                # to allow semantic routing and cross-model failovers based on capabilities.
                if requested.lower() == "auto":
                    logger.info(
                        f"Auto alias detected. Bypassing strict name check for {model.name}"
                    )
                else:
                    # Match if the requested model name is contained in (or equals) the DB model name
                    if requested.lower() not in model.name.lower():
                        logger.info(f"Model {model.name} failed name check")
                        continue

            valid_models.append(model)

        context.valid_models = [m.id for m in valid_models]

        context.log_decision(
            step="ModelSelection",
            action="FilterModels",
            reason="Matched capabilities, context window, and valid providers",
            metadata={"count": len(valid_models)},
        )

        return valid_models
