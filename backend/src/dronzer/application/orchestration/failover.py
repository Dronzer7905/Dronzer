import uuid
from collections.abc import Awaitable, Callable
from typing import Any

import structlog

from dronzer.application.orchestration.context import ExecutionPlan
from dronzer.application.orchestration.health import HealthEngine

logger = structlog.get_logger("dronzer.orchestration.failover")


class FailoverEngine:
    """
    Handles automatic failover to fallback models/providers if the primary
    execution plan completely fails (after all retries are exhausted).
    """

    def __init__(self, health_engine: HealthEngine):
        self.health_engine = health_engine

    async def execute_with_failover(
        self,
        plan: ExecutionPlan,
        execute_func: Callable[[uuid.UUID, uuid.UUID, uuid.UUID], Awaitable[Any]],
    ) -> Any:
        """
        Iterates through the ExecutionPlan.
        First tries the primary config. If it fails fatally, it triggers the fallback chain.
        execute_func receives (provider_id, model_id, key_id).
        """

        # Primary Execution
        try:
            logger.info("Executing primary plan", provider=str(plan.primary_provider_id))
            return await execute_func(
                plan.primary_provider_id, plan.primary_model_id, plan.primary_key_id
            )
        except Exception as e:
            logger.warning("Primary execution failed fatally. Engaging failover.", error=str(e))
            self.health_engine.record_failure(plan.primary_provider_id)

        # Fallback Chain Execution
        for index, fallback in enumerate(plan.fallback_chain):
            provider_id = fallback.get("provider_id")
            model_id = fallback.get("model_id")
            key_id = fallback.get("key_id")

            if not provider_id or not model_id or not key_id:
                logger.error(
                    "Invalid fallback configuration missing required UUIDs", fallback=fallback
                )
                continue

            # Check if this fallback provider is even healthy before trying
            if not self.health_engine.is_provider_healthy(provider_id):
                logger.warning(
                    "Skipping fallback due to unhealthy provider circuit", provider=str(provider_id)
                )
                continue

            try:
                logger.info(f"Executing fallback chain {index + 1}", provider=str(provider_id))
                result = await execute_func(provider_id, model_id, key_id)
                self.health_engine.record_success(provider_id)
                return result
            except Exception as e:
                logger.warning(f"Fallback {index + 1} failed.", error=str(e))
                self.health_engine.record_failure(provider_id)

        # If we reach here, EVERYTHING failed.
        logger.error("All primary and fallback executions failed.")
        raise Exception("Fatal: Exhausted all execution and failover strategies.")
