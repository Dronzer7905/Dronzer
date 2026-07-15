import uuid

from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dronzer.infrastructure.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class KnowledgeSpace(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Top-level namespace for a RAG deployment. 
    Isolated by Organization and Project.
    """
    __tablename__ = "knowledge_spaces"

    name: Mapped[str] = mapped_column(String(255))
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    settings: Mapped[dict] = mapped_column(JSON, default=dict) # e.g. default embedding model, access policies

    # Relationships
    collections: Mapped[list["KnowledgeCollection"]] = relationship("KnowledgeCollection", back_populates="space", cascade="all, delete-orphan")

class KnowledgeCollection(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    A logical grouping of Documents (like a folder or a specific domain knowledge base).
    Maps 1:1 to an underlying Vector Database collection/index.
    """
    __tablename__ = "knowledge_collections"

    name: Mapped[str] = mapped_column(String(255))
    space_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("knowledge_spaces.id", ondelete="CASCADE"), index=True)

    embedding_model: Mapped[str] = mapped_column(String(100), default="text-embedding-3-small")
    vector_dimension: Mapped[int] = mapped_column(Integer, default=1536)

    metadata_schema: Mapped[dict] = mapped_column(JSON, default=dict)

    # Relationships
    space: Mapped["KnowledgeSpace"] = relationship("KnowledgeSpace", back_populates="collections")
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="collection", cascade="all, delete-orphan")

class Document(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Represents an ingested file (PDF, TXT, MD) prior to chunking.
    Tracks the ingestion pipeline status.
    """
    __tablename__ = "knowledge_documents"

    title: Mapped[str] = mapped_column(String(500))
    collection_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("knowledge_collections.id", ondelete="CASCADE"), index=True)

    file_type: Mapped[str] = mapped_column(String(50)) # e.g., 'pdf', 'markdown'
    file_size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    hash_checksum: Mapped[str] = mapped_column(String(255), index=True) # Used for duplicate detection

    status: Mapped[str] = mapped_column(String(50), default="PENDING") # PENDING, PROCESSING, COMPLETED, FAILED
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    document_metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    # Relationships
    collection: Mapped["KnowledgeCollection"] = relationship("KnowledgeCollection", back_populates="documents")
