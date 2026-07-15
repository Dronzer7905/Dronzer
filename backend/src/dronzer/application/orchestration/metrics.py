import structlog

from dronzer.domain.ports import IEventBus

logger = structlog.get_logger("dronzer.orchestration.metrics")


class MetricsTracker:
    """
    Aggregates telemetry during a request lifecycle and flushes to the EventBus.
    """
    def __init__(self, event_bus: IEventBus):
        self.event_bus = event_bus

    async def record_latency(self, model_id: str, provider_id: str, latency_ms: int) -> None:
        """Records Time-To-First-Token or total request latency."""
        await self.event_bus.publish("metric.latency", {
            "model_id": model_id,
            "provider_id": provider_id,
            "latency_ms": latency_ms
        })
        logger.debug("Latency recorded", model_id=model_id, latency_ms=latency_ms)

    async def record_usage(self, key_id: str, prompt_tokens: int, completion_tokens: int, cost: float) -> None:
        """Records token usage and cost for billing and quota limits."""
        await self.event_bus.publish("metric.usage", {
            "api_key_id": key_id,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "cost": cost
        })
        logger.debug("Usage recorded", key_id=key_id, total_tokens=prompt_tokens + completion_tokens, cost=cost)

    async def record_error(self, provider_id: str, status_code: int) -> None:
        """Records upstream HTTP errors to trigger circuit breakers."""
        await self.event_bus.publish("metric.error", {
            "provider_id": provider_id,
            "status_code": status_code
        })
        logger.warning("Upstream error recorded", provider_id=provider_id, status_code=status_code)
