import time
from enum import Enum


class CircuitState(Enum):
    CLOSED = "CLOSED"     # Normal operation, requests pass
    OPEN = "OPEN"         # Failing, requests blocked
    HALF_OPEN = "HALF_OPEN" # Testing recovery, partial requests pass

class CircuitBreaker:
    """
    Protects downstream systems from cascading failures by tracking
    errors and temporarily stopping traffic to failing providers.
    """

    def __init__(self, failure_threshold: int = 5, recovery_timeout_ms: int = 60000):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_ms = recovery_timeout_ms

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0

    def record_success(self) -> None:
        """Called upon successful LLM response."""
        if self.state == CircuitState.HALF_OPEN:
            # We successfully recovered!
            self.state = CircuitState.CLOSED
            self.failure_count = 0

        elif self.state == CircuitState.CLOSED:
            # Standard reset of error counts
            self.failure_count = 0

    def record_failure(self) -> None:
        """Called upon provider error (e.g. 500, timeout)."""
        self.failure_count += 1
        self.last_failure_time = time.time() * 1000

        if self.state == CircuitState.HALF_OPEN:
            # Recovery failed, snap back to OPEN
            self.state = CircuitState.OPEN

        elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
            # Threshold breached, open the circuit
            self.state = CircuitState.OPEN

    def allow_request(self) -> bool:
        """Checks if the request should be allowed through the circuit breaker."""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            now = time.time() * 1000
            # If the timeout has expired, move to HALF_OPEN to test a request
            if (now - self.last_failure_time) > self.recovery_timeout_ms:
                self.state = CircuitState.HALF_OPEN
                return True
            return False

        if self.state == CircuitState.HALF_OPEN:
            # In half-open, we allow one request through to test.
            # If it fails, record_failure will trip back to OPEN.
            # (In a highly concurrent system, this might let a few through, which is acceptable).
            return True

        return False
