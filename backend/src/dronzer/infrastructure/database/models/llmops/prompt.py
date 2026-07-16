import uuid
from typing import Optional

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dronzer.infrastructure.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class PromptCollection(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Groups logically related Prompts together (e.g. "Customer Support Bots", "Code Generation").
    """

    __tablename__ = "prompt_collections"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)

    prompts: Mapped[list["Prompt"]] = relationship("Prompt", back_populates="collection")


class Prompt(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    The top-level container for a Prompt. This tracks the name and ownership,
    but the actual text templates are stored in PromptVersion (like Git branches/commits).
    """

    __tablename__ = "prompts"

    collection_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("prompt_collections.id"))
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id")
    )  # Assuming users exist

    name: Mapped[str] = mapped_column(String(255), index=True)  # e.g. "Llama-3-Python-Coder"
    description: Mapped[str | None] = mapped_column(Text)

    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)

    collection: Mapped[Optional["PromptCollection"]] = relationship(
        "PromptCollection", back_populates="prompts"
    )
    versions: Mapped[list["PromptVersion"]] = relationship(
        "PromptVersion", back_populates="prompt", order_by="desc(PromptVersion.created_at)"
    )


class PromptVersion(Base, UUIDMixin, TimestampMixin):
    """
    An immutable version of a Prompt.
    Contains the raw Jinja2 template and model parameters.
    """

    __tablename__ = "prompt_versions"

    prompt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("prompts.id", ondelete="CASCADE"))

    version_tag: Mapped[str] = mapped_column(String(50))  # e.g. "v1.0.0", "v1.0.1-draft"
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)

    template_text: Mapped[str] = mapped_column(Text)  # Raw string with {{ variables }}
    variables_schema: Mapped[dict] = mapped_column(JSON, default=dict)  # Enforces required inputs

    # Optional defaults for model execution
    default_model: Mapped[str | None] = mapped_column(String(100))
    temperature: Mapped[float] = mapped_column(Integer, default=0.7)

    commit_message: Mapped[str | None] = mapped_column(String(512))

    prompt: Mapped["Prompt"] = relationship("Prompt", back_populates="versions")
