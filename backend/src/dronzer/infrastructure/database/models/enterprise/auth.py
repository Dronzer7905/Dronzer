import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dronzer.infrastructure.database.models.enterprise.tenant import Organization, Project

from sqlalchemy import JSON, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dronzer.infrastructure.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Enterprise Identity.
    Represents a human or service account accessing the Gateway dashboard/API.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)  # Null if SSO
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )

    # Identity Federation / SSO
    is_sso: Mapped[bool] = mapped_column(Boolean, default=False)
    sso_provider: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # e.g., 'entra', 'okta', 'google'
    sso_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="users")
    roles: Mapped[list["Role"]] = relationship("Role", secondary="user_roles")


class Role(Base, UUIDMixin, TimestampMixin):
    """
    ABAC/RBAC Role defining granular permissions across the Tenant.
    """

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(255))
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )

    # JSON array of granted policies (e.g., ["projects:read", "api_keys:write"])
    permissions: Mapped[list] = mapped_column(JSON, default=list)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="roles")


class UserRole(Base):
    """Join table for Users <-> Roles."""

    __tablename__ = "user_roles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )


class APIKey(Base, UUIDMixin, TimestampMixin):
    """
    Vaulted credentials used by client applications to consume the Gateway.
    """

    __tablename__ = "api_keys"

    key_hash: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )

    # Restrictions
    expires_at: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="api_keys")
