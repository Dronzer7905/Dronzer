import uuid

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from dronzer.infrastructure.database.base import Base, TimestampMixin, UUIDMixin


class RoutingPolicy(Base, UUIDMixin, TimestampMixin):
    """Defines the hierarchical policy for routing (Global, Org, Project)."""

    __tablename__ = "routing_policies"

    level: Mapped[str] = mapped_column(String(50))  # global, organization, project
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=True
    )

    config: Mapped[dict] = mapped_column(JSON, default=dict)
    priority: Mapped[int] = mapped_column(Integer, default=0)


class RoutingRule(Base, UUIDMixin, TimestampMixin):
    """Specific rule for overriding routing behavior."""

    __tablename__ = "routing_rules"

    name: Mapped[str] = mapped_column(String(255))
    condition: Mapped[dict] = mapped_column(JSON, default=dict)  # e.g., {"model": "gpt-4"}
    action: Mapped[dict] = mapped_column(JSON, default=dict)  # e.g., {"route_to": "anthropic"}
    is_active: Mapped[bool] = mapped_column(default=True)


class RetryPolicy(Base, UUIDMixin, TimestampMixin):
    """Retry behavior for failed upstream requests."""

    __tablename__ = "retry_policies"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    backoff_multiplier: Mapped[float] = mapped_column(default=2.0)
    status_codes_to_retry: Mapped[list[int]] = mapped_column(
        JSON, default=lambda: [429, 500, 502, 503, 504]
    )


class CircuitBreaker(Base, UUIDMixin, TimestampMixin):
    """Circuit breaker configuration."""

    __tablename__ = "circuit_breakers"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    failure_threshold: Mapped[int] = mapped_column(Integer, default=5)
    recovery_timeout_seconds: Mapped[int] = mapped_column(Integer, default=60)
