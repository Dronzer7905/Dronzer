import os
import time
import uuid
from typing import Any

import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from dronzer.application.orchestration.capability import CapabilityEngine
from dronzer.application.orchestration.context import RequestContext
from dronzer.application.orchestration.cost import CostEngine
from dronzer.application.orchestration.decision import DecisionIntelligenceEngine
from dronzer.application.orchestration.failover import FailoverEngine
from dronzer.application.orchestration.plugin import IPluginHook
from dronzer.application.orchestration.retry import RetryEngine
from dronzer.infrastructure.providers.factory import ProviderFactory
from dronzer.infrastructure.database.models.ai import APIKey, Provider
from dronzer.infrastructure.security.encryption import crypto

logger = structlog.get_logger("dronzer.orchestration.pipeline")

class RequestPipeline:
    """
    The main entrypoint for the AI Orchestration Engine.
    Coordinates plugins, decision intelligence, retries, failovers, and telemetry.
    """

    def __init__(
        self,
        decision_engine,
        failover_engine,
        metrics,
        plugins: list[IPluginHook] = None
    ):
        self.decision_engine = decision_engine
        self.failover_engine = failover_engine
        self.metrics = metrics
        self.plugins = plugins or []

    async def _resolve_provider_name(self, provider_id: uuid.UUID, session: AsyncSession) -> str:
        """
        Resolves a provider UUID to its string name for ProviderFactory lookup.
        """
        result = await session.execute(select(Provider).where(Provider.id == provider_id))
        provider = result.scalars().first()
        if provider:
            return provider.name
        # Fallback: treat UUID as string name (backwards compat with mock engine)
        return str(provider_id)

    async def _execute_upstream_call(
        self,
        provider_id: uuid.UUID,
        model_id: uuid.UUID,
        key_id: uuid.UUID,
        payload: dict[str, Any],
        is_streaming: bool,
        session: AsyncSession = None,
    ) -> Any:
        """
        Instantiates the SDK via ProviderFactory and makes the live call.
        """
        # Resolve provider UUID → name and base_url for the factory
        base_url = None
        if session:
            result = await session.execute(select(Provider).where(Provider.id == provider_id))
            db_prov = result.scalars().first()
            if db_prov:
                provider_name = db_prov.name
                base_url = db_prov.base_url
            else:
                provider_name = str(provider_id)
        else:
            provider_name = str(provider_id)

        provider = ProviderFactory.get_provider(provider_name)
        
        # 1. Fetch API Key from database
        api_key_str = None
        if session:
            key_result = await session.execute(select(APIKey).where(APIKey.id == key_id))
            db_key = key_result.scalars().first()
            if db_key:
                try:
                    api_key_str = crypto.decrypt(db_key.encrypted_key)
                except Exception as e:
                    logger.error("Failed to decrypt provider API key", provider=provider_name, error=str(e))
                    raise ValueError(f"Failed to decrypt API key for {provider_name}. Check your SECRET_KEY.")

        # 2. Fallback to the environment variables
        if not api_key_str:
            env_key_name = f"{provider_name.upper()}_API_KEY"
            api_key_str = os.getenv(env_key_name)
        
        if not api_key_str:
            raise ValueError(
                f"Missing API Key for {provider_name}. "
                f"Please add it in the dashboard or set {provider_name.upper()}_API_KEY in your .env file."
            )

        # Resolve model UUID → name for the upstream payload
        if session:
            from dronzer.infrastructure.database.models.ai import Model
            model_result = await session.execute(select(Model).where(Model.id == model_id))
            db_model = model_result.scalars().first()
            if db_model:
                payload["model"] = db_model.name
            else:
                payload["model"] = str(model_id)
        else:
            payload["model"] = str(model_id)

        if is_streaming:
            return provider.generate_stream(payload, api_key_str, base_url=base_url)
        else:
            return await provider.generate_chat(payload, api_key_str, base_url=base_url)

    async def process_request(self, tenant_id: uuid.UUID, payload: dict[str, Any], session: AsyncSession = None, request_state: dict[str, Any] = None) -> dict[str, Any]:
        """
        Executes the complete request lifecycle.
        """
        start_time = time.time() * 1000

        state = request_state or {}

        # 1. Build Context
        task_type = state.get("task_type", "chat")
        capabilities = CapabilityEngine.detect_capabilities(payload)
        
        # Inject capabilities based on the GatewayKey's task type
        if task_type == "coding" and "code" not in capabilities:
            capabilities.append("code")
        elif task_type == "reasoning" and "reasoning" not in capabilities:
            capabilities.append("reasoning")
        elif task_type == "vision" and "vision" not in capabilities:
            capabilities.append("vision")
            
        context = RequestContext(
            tenant_id=tenant_id,
            project_id=state.get("project_id"),
            user_id=state.get("user_id"),
            payload=payload,
            headers={},
            requested_model=payload.get("model"),
            requested_capabilities=capabilities,
            gateway_key_id=state.get("gateway_key_id"),
            task_type=task_type,
            model_priorities=state.get("model_priorities", []),
            provider_priorities=state.get("provider_priorities", [])
        )

        # 2. Pre-Routing Plugins
        for plugin in self.plugins:
            context = await plugin.before_routing(context)

        # 3. Decision Intelligence (Routing, Selection)
        plan = await self.decision_engine.generate_execution_plan(context, session)

        # 4. Executor wrapping (Includes Retry logic)
        async def execute_target(provider_id: uuid.UUID, model_id: uuid.UUID, key_id: uuid.UUID) -> dict[str, Any]:
            # This is wrapped in the RetryEngine
            return await RetryEngine.execute_with_retry(
                self._execute_upstream_call,
                max_attempts=plan.max_retries,
                base_delay_ms=1000,
                provider_id=provider_id,
                model_id=model_id,
                key_id=key_id,
                payload=payload,
                is_streaming=plan.is_streaming,
                session=session
            )

        # 5. Execute with Failover protections
        try:
            response = await self.failover_engine.execute_with_failover(plan, execute_target)
        except Exception as e:
            # 6a. Fatal Failure Plugins
            for plugin in self.plugins:
                await plugin.after_failure(e, None)
            raise e

        # 6b. Post-Response Plugins
        for plugin in self.plugins:
            response = await plugin.after_response(response, None)

        # 7. Telemetry & Metrics
        end_time = time.time() * 1000
        latency = int(end_time - start_time)

        if plan.is_streaming:
            return response

        usage = response.get("usage", {})
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)

        estimated_cost = CostEngine.estimate_cost(prompt_tokens, completion_tokens, {})

        await self.metrics.record_latency(
            str(plan.primary_model_id), str(plan.primary_provider_id), latency, session
        )
        await self.metrics.record_usage(
            str(plan.primary_key_id), prompt_tokens, completion_tokens, estimated_cost, session
        )

        return response
