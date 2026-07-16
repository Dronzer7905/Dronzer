import enum
import uuid

from sqlalchemy import JSON, Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dronzer.infrastructure.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class ExecutionStatus(enum.StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"  # For Human-in-the-Loop
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class WorkflowTemplate(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Defines the structural DAG (Nodes and Edges) of a workflow.
    Usually exported/imported as JSON.
    """

    __tablename__ = "workflow_templates"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1)

    # Organization/Tenant isolation
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )

    # The raw DAG JSON structure (nodes, edges, parameters)
    definition: Mapped[dict] = mapped_column(JSON, default=dict)

    is_published: Mapped[bool] = mapped_column(Boolean, default=False)

    executions: Mapped[list["WorkflowExecution"]] = relationship(
        "WorkflowExecution", back_populates="template", cascade="all, delete-orphan"
    )


class WorkflowExecution(Base, UUIDMixin, TimestampMixin):
    """
    A single running instance of a WorkflowTemplate.
    """

    __tablename__ = "workflow_executions"

    template_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workflow_templates.id", ondelete="CASCADE"), index=True
    )

    status: Mapped[ExecutionStatus] = mapped_column(
        Enum(ExecutionStatus), default=ExecutionStatus.PENDING
    )

    input_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    output_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # State tracking for resumption after a PAUSE (HITL)
    current_node_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    execution_state: Mapped[dict] = mapped_column(JSON, default=dict)

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    template: Mapped["WorkflowTemplate"] = relationship(
        "WorkflowTemplate", back_populates="executions"
    )
