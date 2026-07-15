from abc import ABC, abstractmethod

from pydantic import BaseModel


class RerankResult(BaseModel):
    index: int # Index of the original document in the requested list
    relevance_score: float # Scored typically from 0.0 to 1.0
    text: str # The original text chunk

class RerankerProvider(ABC):
    """
    Abstract interface for cross-encoder or reranking models (e.g. Cohere, Voyage).
    Used to re-score and re-order the initial fast retrieval (Top-K) from a Vector Store,
    providing much higher accuracy for the final context window.
    """

    @abstractmethod
    async def rerank(self, query: str, documents: list[str], top_n: int = 5) -> list[RerankResult]:
        """
        Takes a search query and a list of candidate documents, 
        evaluating them simultaneously (cross-attention) to return a sorted, scored subset.
        """
        pass
