from typing import Any


class DronzerException(Exception):
    """Base exception for all Dronzer AI Gateway errors."""

    def __init__(self, message: str, status_code: int = 500, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class RoutingException(DronzerException):
    """Raised when the Decision Engine fails to find a valid route."""
    def __init__(self, message: str = "No valid routes available.", details: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=503, details=details)


class AuthenticationException(DronzerException):
    """Raised for invalid or missing API tokens."""
    def __init__(self, message: str = "Authentication failed.", details: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=401, details=details)


class ConfigurationException(DronzerException):
    """Raised when tenant or gateway configuration is invalid."""
    def __init__(self, message: str = "Configuration error.", details: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=400, details=details)


class RateLimitException(DronzerException):
    """Raised when a tenant exceeds their allowed quota."""
    def __init__(self, message: str = "Rate limit exceeded.", retry_after: int = 60) -> None:
        details = {"retry_after": retry_after}
        super().__init__(message, status_code=429, details=details)
