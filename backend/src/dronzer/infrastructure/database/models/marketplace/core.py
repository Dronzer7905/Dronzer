import enum
import uuid

from sqlalchemy import JSON, Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dronzer.infrastructure.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class PackageType(str, enum.Enum):
    PLUGIN = "PLUGIN"
    PROVIDER = "PROVIDER"
    WORKFLOW = "WORKFLOW"
    PROMPT = "PROMPT"
    AGENT_TEMPLATE = "AGENT_TEMPLATE"
    DASHBOARD_WIDGET = "DASHBOARD_WIDGET"
    CONNECTOR = "CONNECTOR"

class Publisher(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Represents an Organization or Individual Developer that publishes packages to the Dronzer Marketplace.
    """
    __tablename__ = "publishers"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    namespace: Mapped[str] = mapped_column(String(100), unique=True, index=True) # e.g. "@google", "@community"

    website: Mapped[str | None] = mapped_column(String(255))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    packages: Mapped[list["Package"]] = relationship("Package", back_populates="publisher")

class Package(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Represents an AI Marketplace extension/plugin.
    """
    __tablename__ = "packages"

    publisher_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("publishers.id"))

    name: Mapped[str] = mapped_column(String(255), index=True) # "github-connector"
    package_type: Mapped[PackageType] = mapped_column(Enum(PackageType))

    description: Mapped[str] = mapped_column(Text)
    icon_url: Mapped[str | None] = mapped_column(String(255))

    # Discovery and Ranking
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    downloads: Mapped[int] = mapped_column(Integer, default=0)
    rating: Mapped[float] = mapped_column(Integer, default=0.0)

    # Monetization (Architecture only)
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    price_cents: Mapped[int] = mapped_column(Integer, default=0)

    publisher: Mapped["Publisher"] = relationship("Publisher", back_populates="packages")
    versions: Mapped[list["PackageVersion"]] = relationship("PackageVersion", back_populates="package")

class PackageVersion(Base, UUIDMixin, TimestampMixin):
    """
    Represents a specific Semantic Version of a Package.
    """
    __tablename__ = "package_versions"

    package_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("packages.id", ondelete="CASCADE"))

    version: Mapped[str] = mapped_column(String(50)) # e.g. "1.2.4"
    is_prerelease: Mapped[bool] = mapped_column(Boolean, default=False)

    # Security and Storage
    s3_url: Mapped[str] = mapped_column(String(512))
    sha256_hash: Mapped[str] = mapped_column(String(64))

    # Dependency Graph & Permissions
    dependencies: Mapped[dict] = mapped_column(JSON, default=dict) # {"@core/runtime": ">=1.0.0"}
    required_capabilities: Mapped[list[str]] = mapped_column(JSON, default=list) # ["network", "filesystem"]

    package: Mapped["Package"] = relationship("Package", back_populates="versions")
