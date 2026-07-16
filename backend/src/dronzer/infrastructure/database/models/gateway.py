import uuid

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from dronzer.infrastructure.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class GatewayKey(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Dronzer Gateway API Keys (dz-sk-...).
    Used by external clients to authenticate against the gateway.
    The raw key is shown only once at creation; we store the hashed version.
    """

    __tablename__ = "gateway_keys"

    hashed_key: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    label: Mapped[str] = mapped_column(String(255))
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("projects.id", ondelete="SET NULL"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    # Task-Aware Routing Overrides
    task_type: Mapped[str] = mapped_column(String(100), default="chat")
    model_priorities: Mapped[list[str]] = mapped_column(JSON, default=list)
    provider_priorities: Mapped[list[str]] = mapped_column(JSON, default=list)
