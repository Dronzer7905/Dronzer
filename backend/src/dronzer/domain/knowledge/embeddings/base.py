from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """
    Abstract interface for converting text chunks into dense vector embeddings.
    """

    @abstractmethod
    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Generates embeddings for a batch of documents. 
        Usually optimized for retrieval (e.g. Voyage AI uses a specific prefix for documents).
        """
        pass

    @abstractmethod
    async def embed_query(self, text: str) -> list[float]:
        """
        Generates an embedding for a search query.
        Usually optimized for searching (e.g. Voyage AI uses a specific prefix for queries).
        """
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Returns the vector dimensionality for this model (e.g., 1536 for text-embedding-3-small)."""
        pass
