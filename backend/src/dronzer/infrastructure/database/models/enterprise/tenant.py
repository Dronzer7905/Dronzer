import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dronzer.infrastructure.database.models.enterprise.auth import APIKey, Role, User

from sqlalchemy import JSON, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dronzer.infrastructure.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class Organization(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Top-level Enterprise Tenant.
    Represents a company or business unit managing multiple Projects.
    """

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(100), index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # Hierarchical support (Sub-Organizations)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id"), nullable=True
    )

    # Billing & Settings
    stripe_customer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    settings: Mapped[dict] = mapped_column(JSON, default=dict)

    # Relationships
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="organization", cascade="all, delete-orphan"
    )
    users: Mapped[list["User"]] = relationship("User", back_populates="organization")
    roles: Mapped[list["Role"]] = relationship("Role", back_populates="organization")


class Project(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Sub-tenant environment.
    Represents an isolated environment (e.g. 'Prod-App-A', 'Dev-App-B') within an Organization.
    """

    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(100))
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )

    # Quotas and Budgeting
    monthly_budget_usd: Mapped[float | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="projects")
    api_keys: Mapped[list["APIKey"]] = relationship("APIKey", back_populates="project")
