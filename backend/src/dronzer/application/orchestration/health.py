import uuid

from dronzer.application.orchestration.circuit_breaker import CircuitBreaker


class HealthEngine:
    """
    Manages the health status of Providers and Models.
    Coordinates Circuit Breakers per provider.
    """

    def __init__(self) -> None:
        # In a real distributed system, this state is synchronized via Redis.
        # For memory-layer hot path, we keep localized Circuit Breakers.
        self._provider_breakers: dict[uuid.UUID, CircuitBreaker] = {}

    def get_breaker(self, provider_id: uuid.UUID) -> CircuitBreaker:
        """Retrieves or initializes a circuit breaker for a provider."""
        if provider_id not in self._provider_breakers:
            self._provider_breakers[provider_id] = CircuitBreaker()
        return self._provider_breakers[provider_id]

    def is_provider_healthy(self, provider_id: uuid.UUID) -> bool:
        """Checks if a provider is healthy enough to receive traffic."""
        breaker = self.get_breaker(provider_id)
        return breaker.allow_request()

    def record_success(self, provider_id: uuid.UUID) -> None:
        """Records a successful request, healing the provider."""
        breaker = self.get_breaker(provider_id)
        breaker.record_success()

    def record_failure(self, provider_id: uuid.UUID) -> None:
        """Records a failure, potentially degrading the provider's health."""
        breaker = self.get_breaker(provider_id)
        breaker.record_failure()
