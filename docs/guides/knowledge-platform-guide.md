# Dronzer AI Gateway - Knowledge Platform & RAG Guide

Welcome to the Dronzer Knowledge Platform. This system empowers the AI Gateway with infinite memory, semantic search, and Enterprise Retrieval-Augmented Generation (RAG).

## Core Concepts
- **Knowledge Spaces**: The top-level namespace bounded by an Enterprise Tenant (Organization & Project).
- **Collections**: Logical groupings of vectors mapping directly to indices in the underlying Vector Database (e.g., Qdrant, Milvus).
- **Ingestion Pipeline**: The asynchronous process of parsing raw files (PDF/MD), chunking them, and embedding them into Dense Vectors.

## Embedding and Vector Databases
Dronzer is provider-agnostic. 
- **Embeddings**: By default, it integrates with OpenAI (`text-embedding-3-small`), but abstractions are provided for Cohere, Voyage, and local models.
- **Vector Stores**: The standard implementation relies on Qdrant, but you can swap the `VectorStoreProvider` out for pgvector or Pinecone.

## Advanced Retrieval Strategies
1. **Semantic Search (Top-K)**: Uses Cosine Similarity to find chunks closely matching the query's mathematical embedding.
2. **Hybrid Search (BM25 + Dense)**: Combines keyword search with vector search for optimal recall.
3. **Cross-Encoder Reranking**: If enabled, Dronzer will fetch an initial large batch of documents (e.g., Top-20) and pass them through a Reranker (like Cohere Rerank) to perfectly score and sort the final Top-5 context injected into the prompt.

## Agent Memory
The Knowledge Platform also powers the Gateway's Long-Term memory. `MemorySession` instances automatically summarize older conversation turns and embed them into the Vector Database, allowing AI Agents to "remember" context from weeks or months ago.
