import uuid

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from dronzer.infrastructure.database.base import Base, TimestampMixin, UUIDMixin


class SystemSetting(Base, UUIDMixin, TimestampMixin):
    """Global configuration settings overrides."""

    __tablename__ = "system_settings"

    key: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    value: Mapped[dict] = mapped_column(JSON)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)


class PluginRegistry(Base, UUIDMixin, TimestampMixin):
    """Registered external Python plugins."""

    __tablename__ = "plugin_registry"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    version: Mapped[str] = mapped_column(String(50))
    module_path: Mapped[str] = mapped_column(String(500))
    is_enabled: Mapped[bool] = mapped_column(default=False)


class PluginConfiguration(Base, UUIDMixin, TimestampMixin):
    """Configuration for a specific plugin."""

    __tablename__ = "plugin_configurations"

    plugin_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("plugin_registry.id", ondelete="CASCADE")
    )
    config: Mapped[dict] = mapped_column(JSON, default=dict)


class BackgroundJob(Base, UUIDMixin, TimestampMixin):
    """Tracking for asynchronous background tasks."""

    __tablename__ = "background_jobs"

    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(
        String(50), index=True
    )  # pending, running, failed, completed
    error_message: Mapped[str | None] = mapped_column(String(2000), nullable=True)


class FeatureFlag(Base, UUIDMixin, TimestampMixin):
    """Dynamic toggles for platform features."""

    __tablename__ = "feature_flags"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    is_enabled: Mapped[bool] = mapped_column(default=False)


class Secret(Base, UUIDMixin, TimestampMixin):
    """Encrypted general-purpose secrets (e.g. for plugins)."""

    __tablename__ = "secrets"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    encrypted_value: Mapped[str] = mapped_column(String(2000))
