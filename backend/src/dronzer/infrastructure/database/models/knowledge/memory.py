import uuid

from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dronzer.infrastructure.database.base import Base, TimestampMixin, UUIDMixin


class MemorySession(Base, UUIDMixin, TimestampMixin):
    """
    Tracks an agent's long-term and short-term conversational context.
    """

    __tablename__ = "memory_sessions"

    session_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )

    summary: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # Periodically updated rolling summary

    # Relationships
    turns: Mapped[list["MemoryTurn"]] = relationship(
        "MemoryTurn", back_populates="session", cascade="all, delete-orphan"
    )


class MemoryTurn(Base, UUIDMixin, TimestampMixin):
    """
    An individual interaction (user prompt and agent response) within a session.
    """

    __tablename__ = "memory_turns"

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("memory_sessions.id", ondelete="CASCADE"), index=True
    )

    role: Mapped[str] = mapped_column(String(50))  # 'user', 'assistant', 'system'
    content: Mapped[str] = mapped_column(Text)
    token_count: Mapped[int] = mapped_column(Integer, default=0)

    turn_metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    # Relationships
    session: Mapped["MemorySession"] = relationship("MemorySession", back_populates="turns")
