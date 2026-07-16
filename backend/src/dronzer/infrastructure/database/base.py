import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base declarative class for all SQLAlchemy models."""

    pass


def utcnow() -> datetime:
    """Returns an aware UTC datetime."""
    return datetime.now(UTC)


class UUIDMixin:
    """Provides a UUID primary key."""

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


class TimestampMixin:
    """Provides created_at and updated_at columns."""

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class SoftDeleteMixin:
    """Provides soft-delete capabilities."""

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)

    def soft_delete(self) -> None:
        self.is_deleted = True
        self.deleted_at = utcnow()
