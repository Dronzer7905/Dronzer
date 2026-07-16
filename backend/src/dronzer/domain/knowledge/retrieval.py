import structlog

from dronzer.domain.knowledge.embeddings.base import EmbeddingProvider
from dronzer.domain.knowledge.reranking import RerankerProvider
from dronzer.domain.knowledge.vector_stores.base import SearchResult, VectorStoreProvider

logger = structlog.get_logger("dronzer.knowledge.retrieval")


class RetrievalEngine:
    """
    Executes advanced search strategies across the Vector Database.
    Supports Top-K dense search and Cross-Encoder Reranking.
    """

    def __init__(
        self,
        vector_store: VectorStoreProvider,
        embedding_provider: EmbeddingProvider,
        reranker: RerankerProvider | None = None,
    ):
        self.vector_store = vector_store
        self.embedding = embedding_provider
        self.reranker = reranker

    async def retrieve(
        self, query: str, collection_name: str, top_k: int = 5, rerank: bool = True
    ) -> list[SearchResult]:
        """
        Retrieves the most semantically relevant chunks for a given query.
        If a reranker is provided, it fetches more chunks initially (e.g. 20)
        and uses cross-attention to score and return the top_k.
        """
        logger.info("Executing Retrieval", query=query[:50], collection=collection_name)

        # 1. Embed the query
        query_vector = await self.embedding.embed_query(query)

        # 2. Determine initial fetch size
        fetch_size = top_k * 4 if (rerank and self.reranker) else top_k

        # 3. Dense Semantic Search (Top-K)
        initial_results = await self.vector_store.search(
            collection_name=collection_name, query_vector=query_vector, top_k=fetch_size
        )

        if not initial_results:
            return []

        # 4. Return early if reranking is disabled or not available
        if not rerank or not self.reranker:
            return initial_results[:top_k]

        # 5. Rerank (Cross-Encoder)
        documents = [res.payload.get("text", "") for res in initial_results]
        reranked_scores = await self.reranker.rerank(query=query, documents=documents, top_n=top_k)

        # 6. Reconstruct the final SearchResult list based on the reranked order
        final_results = []
        for r_res in reranked_scores:
            orig_result = initial_results[r_res.index]
            orig_result.score = r_res.relevance_score  # Update score to the cross-encoder score
            final_results.append(orig_result)

        logger.debug("Retrieval complete", returned=len(final_results))
        return final_results
