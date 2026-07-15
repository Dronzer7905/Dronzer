import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dronzer.infrastructure.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class Organization(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Top-level tenant structure."""
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    projects: Mapped[list["Project"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    users: Mapped[list["User"]] = relationship(back_populates="organization")


class Project(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Sub-tenant workspace within an organization."""
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), index=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)

    organization: Mapped["Organization"] = relationship(back_populates="projects")


class User(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Platform user."""
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    organization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True)

    organization: Mapped["Organization"] = relationship(back_populates="users")


class Role(Base, UUIDMixin, TimestampMixin):
    """RBAC Role definitions."""
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)


class Permission(Base, UUIDMixin, TimestampMixin):
    """RBAC Permission rules."""
    __tablename__ = "permissions"

    resource: Mapped[str] = mapped_column(String(100))
    action: Mapped[str] = mapped_column(String(100))
