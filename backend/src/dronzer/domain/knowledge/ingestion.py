from pathlib import Path
from typing import Any

import structlog

from dronzer.domain.enterprise.governance import PIIRedactor
from dronzer.domain.knowledge.chunking import ChunkingEngine
from dronzer.domain.knowledge.embeddings.base import EmbeddingProvider
from dronzer.domain.knowledge.parsers import ParserFactory
from dronzer.domain.knowledge.vector_stores.base import VectorRecord, VectorStoreProvider

logger = structlog.get_logger("dronzer.knowledge.ingestion")

class DocumentIngestionPipeline:
    """
    Orchestrates the conversion of a raw file into dense searchable vectors.
    1. Parse raw text
    2. Split into chunks
    3. Mask sensitive PII
    4. Generate embeddings
    5. Upsert to Vector Database
    
    This should be executed asynchronously by a Celery or Redis worker.
    """

    def __init__(self,
                 vector_store: VectorStoreProvider,
                 embedding_provider: EmbeddingProvider,
                 db_session: Any = None):
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider
        self.db = db_session
        self.chunker = ChunkingEngine()
        self.redactor = PIIRedactor(mode="redact")

    async def process_document(self, file_path: Path, collection_name: str, tenant_config: dict = None):
        logger.info("Starting ingestion pipeline", file=str(file_path), collection=collection_name)

        try:
            # 1. Parse
            parser = ParserFactory.get_parser(file_path)
            parsed_doc = await parser.parse(file_path)
            logger.debug("Parsed document", length=len(parsed_doc.content))

            # 2. Chunk
            chunks = self.chunker.split(parsed_doc)
            logger.debug("Document chunked", count=len(chunks))

            vectors = []

            # 3 & 4. Mask and Embed in batches
            batch_texts = []
            for chunk in chunks:
                safe_text = self.redactor.process_payload(chunk.text, tenant_config or {})
                batch_texts.append(safe_text)

            embeddings = await self.embedding_provider.embed_documents(batch_texts)

            # 5. Prepare Vector Records
            for idx, chunk in enumerate(chunks):
                record_id = f"doc_{file_path.stem}_chunk_{idx}"
                vectors.append(
                    VectorRecord(
                        id=record_id,
                        vector=embeddings[idx],
                        payload={
                            "text": batch_texts[idx],
                            "source": str(file_path),
                            "chunk_index": idx
                        }
                    )
                )

            # 6. Upsert to DB
            await self.vector_store.upsert(collection_name, vectors)
            logger.info("Ingestion complete", inserted=len(vectors), collection=collection_name)

            # Update Document status in Relational DB to COMPLETED...
            return True

        except Exception as e:
            logger.exception("Ingestion pipeline failed", file=str(file_path), error=str(e))
            # Update Document status in Relational DB to FAILED...
            return False
