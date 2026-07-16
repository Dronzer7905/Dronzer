import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.application.orchestration.context import DecisionContext, ExecutionPlan, RequestContext
from dronzer.application.orchestration.key_rotation import APIKeyRotationEngine
from dronzer.application.orchestration.model import ModelSelectionEngine
from dronzer.application.orchestration.provider import ProviderSelectionEngine
from dronzer.application.orchestration.routing import RoutingEngine

logger = structlog.get_logger("dronzer.orchestration.decision")


class DecisionIntelligenceEngine:
    """
    The Central Brain.
    Orchestrates the selection of providers, models, and keys, and outputs
    a deterministic ExecutionPlan for the pipeline.
    """

    def __init__(
        self,
        provider_engine: ProviderSelectionEngine | None = None,
        model_engine: ModelSelectionEngine | None = None,
        key_engine: APIKeyRotationEngine | None = None,
        routing_engine: RoutingEngine | None = None,
    ):
        self.provider_engine = provider_engine or ProviderSelectionEngine()
        self.model_engine = model_engine or ModelSelectionEngine()
        self.key_engine = key_engine or APIKeyRotationEngine()
        self.routing_engine = routing_engine or RoutingEngine()

    async def generate_execution_plan(
        self, request_context: RequestContext, session: AsyncSession = None
    ) -> ExecutionPlan:
        """
        Runs the full decision lifecycle.
        Requires a database session to query providers, models, and API keys.
        """
        if session is None:
            raise ValueError(
                "DecisionIntelligenceEngine requires a database session. "
                "Pass the AsyncSession from the request pipeline."
            )

        logger.info("Decision Engine triggered", tenant_id=str(request_context.tenant_id))

        # 1. Initialize Context
        decision_context = DecisionContext(request_context=request_context)

        # Note: In a real flow, active_policy is fetched from the DB via tenant_id.
        # We assume active_policy is populated here by the Pipeline before calling this.

        # 2. Filter Valid Providers
        await self.provider_engine.filter_providers(decision_context, session)
        if not decision_context.valid_providers:
            raise Exception("No valid AI providers available for this request.")

        # 3. Filter Valid Models based on capabilities and context window
        valid_models = await self.model_engine.filter_models(decision_context, session)
        if not valid_models:
            raise Exception("No valid AI models satisfy the requested capabilities.")

        # 4. Rank Models via Routing Strategy
        ranked_models = self.routing_engine.execute_strategy(decision_context, valid_models)

        # 4.5 Task-Aware Overrides (Gateway Key Custom Priority)
        if request_context.model_priorities:
            priority_map = {
                str(m_id): idx for idx, m_id in enumerate(request_context.model_priorities)
            }

            def custom_sort(model):
                m_str = str(model.id)
                # If explicitly prioritized, put at the top in exact order
                if m_str in priority_map:
                    return (0, priority_map[m_str])
                # Otherwise, fallback to the end (global pool)
                return (1, 0)

            ranked_models.sort(key=custom_sort)

        # 5. Select API Keys and build the fallback chain
        primary_model = None
        primary_key = None
        fallback_chain = []

        for model in ranked_models:
            keys = await self.key_engine.get_all_keys(model.provider_id, session)
            if not keys:
                logger.warning(
                    "Skipping model due to lack of valid API keys", model_id=str(model.id)
                )
                continue

            for key in keys:
                if not primary_model:
                    primary_model = model
                    primary_key = key
                else:
                    fallback_chain.append(
                        {"provider_id": model.provider_id, "model_id": model.id, "key_id": key.id}
                    )

        if not primary_model or not primary_key:
            raise Exception("Failed to secure a valid API key for any ranked models.")

        # 6. Finalize Execution Plan
        plan = ExecutionPlan(
            primary_provider_id=primary_model.provider_id,
            primary_model_id=primary_model.id,
            primary_key_id=primary_key.id,
            fallback_chain=fallback_chain,
            is_streaming=request_context.payload.get("stream", False),
        )

        decision_context.log_decision(
            step="DecisionComplete",
            action="GeneratedPlan",
            reason="Successfully built primary and fallback chain",
            metadata={"primary_model": primary_model.name},
        )

        return plan
