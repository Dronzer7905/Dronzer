import uuid

from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from dronzer.infrastructure.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class AgentProfile(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Defines an autonomous AI Agent that can participate in workflows.
    Includes instructions, roles, and allowed tools.
    """

    __tablename__ = "agent_profiles"

    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255))  # e.g. "Senior Python Engineer", "Data Analyst"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )

    system_prompt: Mapped[str] = mapped_column(Text)

    # Model configuration (e.g. gpt-4-turbo, claude-3-opus)
    model_config: Mapped[dict] = mapped_column(JSON, default=dict)

    # List of Tool IDs this agent is permitted to execute (RBAC)
    allowed_tools: Mapped[list] = mapped_column(JSON, default=list)

    # ID of the Supervisor agent if this is a sub-agent
    supervisor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("agent_profiles.id", ondelete="SET NULL"), nullable=True
    )


class AgentState(Base, UUIDMixin, TimestampMixin):
    """
    Tracks the short-term working memory and active goals of a running Agent.
    """

    __tablename__ = "agent_states"

    agent_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("agent_profiles.id", ondelete="CASCADE"), index=True
    )
    execution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workflow_executions.id", ondelete="CASCADE"), index=True
    )

    current_goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    scratchpad: Mapped[list] = mapped_column(JSON, default=list)  # ReAct pattern reasoning steps
