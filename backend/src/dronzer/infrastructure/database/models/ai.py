import uuid

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dronzer.infrastructure.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class Provider(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """AI Providers (e.g., OpenAI, Anthropic)."""

    __tablename__ = "providers"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    base_url: Mapped[str] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(default=True)

    models: Mapped[list["Model"]] = relationship(back_populates="provider")
    api_keys: Mapped[list["APIKey"]] = relationship(back_populates="provider")


class ProviderGroup(Base, UUIDMixin, TimestampMixin):
    """Logical grouping of providers for routing."""

    __tablename__ = "provider_groups"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)


class Model(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Specific AI Models (e.g., gpt-4, claude-3)."""

    __tablename__ = "models"

    name: Mapped[str] = mapped_column(String(255), index=True)
    provider_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("providers.id", ondelete="CASCADE"))
    context_window: Mapped[int] = mapped_column(Integer, default=4096)
    capabilities: Mapped[dict] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(default=True)

    provider: Mapped["Provider"] = relationship(back_populates="models")


class ModelGroup(Base, UUIDMixin, TimestampMixin):
    """Grouping for capability-based routing (e.g., 'gpt-4-class')."""

    __tablename__ = "model_groups"

    name: Mapped[str] = mapped_column(String(255), unique=True)


class APIKeyPool(Base, UUIDMixin, TimestampMixin):
    """Pool of API keys for rotation."""

    __tablename__ = "api_key_pools"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True
    )


class APIKey(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """API Keys for providers. Encrypted at rest."""

    __tablename__ = "api_keys"

    provider_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("providers.id", ondelete="CASCADE"))
    pool_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("api_key_pools.id", ondelete="SET NULL"), nullable=True
    )

    # Store encrypted string, use EncryptionManager to encrypt/decrypt
    encrypted_key: Mapped[str] = mapped_column(String(1000))

    is_active: Mapped[bool] = mapped_column(default=True)
    weight: Mapped[int] = mapped_column(Integer, default=100)

    provider: Mapped["Provider"] = relationship(back_populates="api_keys")
