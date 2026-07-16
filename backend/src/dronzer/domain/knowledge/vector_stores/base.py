from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class VectorRecord(BaseModel):
    """A chunk of text converted into a dense vector with associated metadata."""

    id: str
    vector: list[float]
    payload: dict[str, Any]
    sparse_vector: dict[int, float] | None = None  # Support for Hybrid Search (BM25)


class SearchResult(BaseModel):
    id: str
    score: float
    payload: dict[str, Any]


class VectorStoreProvider(ABC):
    """
    Abstract interface for interacting with underlying Vector Databases (Qdrant, Pinecone, pgvector).
    Allows Dronzer to remain provider-agnostic.
    """

    @abstractmethod
    async def create_collection(self, collection_name: str, dimension: int) -> bool:
        """Initializes a new namespace in the vector store."""
        pass

    @abstractmethod
    async def upsert(self, collection_name: str, records: list[VectorRecord]) -> bool:
        """Inserts or updates vectors in bulk."""
        pass

    @abstractmethod
    async def search(
        self,
        collection_name: str,
        query_vector: list[float],
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        """Performs Dense Semantic Search (Cosine Similarity / Dot Product)."""
        pass

    @abstractmethod
    async def delete(self, collection_name: str, record_ids: list[str]) -> bool:
        """Removes vectors by ID. Used during document purging or chunk rotation."""
        pass
