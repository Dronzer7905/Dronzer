import structlog

from sqlalchemy.ext.asyncio import AsyncSession

from dronzer.infrastructure.database.models.telemetry import RequestLog

logger = structlog.get_logger("dronzer.orchestration.postgres_metrics")


class PostgresMetricsTracker:
    """
    Production metrics tracker that writes real telemetry data
    to the RequestLog table in PostgreSQL.
    """

    def __init__(self):
        self._pending_latency: int = 0
        self._pending_provider_id: str | None = None
        self._pending_model_id: str | None = None

    async def record_latency(
        self,
        model_id: str,
        provider_id: str,
        latency_ms: int,
        session: AsyncSession = None,
    ) -> None:
        """
        Stores latency data in instance state to be flushed alongside usage data.
        """
        self._pending_latency = latency_ms
        self._pending_provider_id = provider_id
        self._pending_model_id = model_id
        logger.debug(
            "Latency recorded (pending flush)",
            model_id=model_id,
            provider_id=provider_id,
            latency_ms=latency_ms,
        )

    async def record_usage(
        self,
        key_id: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float,
        session: AsyncSession = None,
    ) -> None:
        """
        Creates a RequestLog row with real latency, token usage, and cost data.
        Flushes the pending latency accumulated from record_latency().
        """
        if not session:
            logger.warning("No DB session available — skipping metrics persistence")
            return

        try:
            log = RequestLog(
                latency_ms=self._pending_latency,
                status_code=200,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                cost=cost,
                decision_trace={
                    "provider_id": self._pending_provider_id,
                    "model_id": self._pending_model_id,
                    "api_key_id": key_id,
                },
            )
            session.add(log)
            await session.commit()

            logger.info(
                "Request metrics persisted",
                latency_ms=self._pending_latency,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                cost=cost,
            )
        except Exception as e:
            logger.error("Failed to persist request metrics", error=str(e))
            # Don't let metrics failures crash the request pipeline
            await session.rollback()
        finally:
            # Reset pending state
            self._pending_latency = 0
            self._pending_provider_id = None
            self._pending_model_id = None
