import uuid

from sqlalchemy import JSON, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from dronzer.infrastructure.database.base import Base, TimestampMixin, UUIDMixin


class AuditLog(Base, UUIDMixin, TimestampMixin):
    """Immutable audit trail for system and configuration changes."""

    __tablename__ = "audit_logs"

    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(255), index=True)
    resource_type: Mapped[str] = mapped_column(String(100))
    resource_id: Mapped[str] = mapped_column(String(255))
    changes: Mapped[dict] = mapped_column(JSON, default=dict)


class RequestLog(Base, UUIDMixin, TimestampMixin):
    """Detailed trace of an AI routing request."""

    __tablename__ = "request_logs"

    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True
    )
    provider_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("providers.id", ondelete="SET NULL"), nullable=True
    )
    model_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("models.id", ondelete="SET NULL"), nullable=True
    )

    latency_ms: Mapped[int] = mapped_column(Integer)
    status_code: Mapped[int] = mapped_column(Integer)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
    cost: Mapped[float] = mapped_column(Float, default=0.0)

    # Store the entire JSON trace of the decision engine
    decision_trace: Mapped[dict] = mapped_column(JSON, default=dict)


class ProviderHealth(Base, UUIDMixin, TimestampMixin):
    """Rolling health snapshot for a Provider."""

    __tablename__ = "provider_health"

    provider_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("providers.id", ondelete="CASCADE"), unique=True
    )
    error_count: Mapped[int] = mapped_column(Integer, default=0)
    success_rate: Mapped[float] = mapped_column(Float, default=100.0)
    is_circuit_open: Mapped[bool] = mapped_column(default=False)


class ModelHealth(Base, UUIDMixin, TimestampMixin):
    """Rolling health snapshot for a Model."""

    __tablename__ = "model_health"

    model_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("models.id", ondelete="CASCADE"), unique=True
    )
    avg_latency_ms: Mapped[int] = mapped_column(Integer, default=0)


class KeyHealth(Base, UUIDMixin, TimestampMixin):
    """Rolling health and quota usage for an API Key."""

    __tablename__ = "key_health"

    api_key_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("api_keys.id", ondelete="CASCADE"), unique=True
    )
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    rate_limit_hits: Mapped[int] = mapped_column(Integer, default=0)
    is_cooldown: Mapped[bool] = mapped_column(default=False)
