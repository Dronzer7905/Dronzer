import re

import structlog

from dronzer.domain.knowledge.parsers import ParsedDocument

logger = structlog.get_logger("dronzer.knowledge.chunking")


class DocumentChunk:
    def __init__(self, text: str, chunk_index: int):
        self.text = text
        self.chunk_index = chunk_index


class ChunkingEngine:
    """
    Splits long parsed documents into smaller, semantically meaningful chunks
    so they can be embedded and retrieved accurately by the Vector Store.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, document: ParsedDocument) -> list[DocumentChunk]:
        """
        Routes to the appropriate splitting strategy based on document type.
        """
        doc_type = document.metadata.get("type", "txt")

        if doc_type == "md":
            return self._markdown_split(document.content)
        else:
            return self._recursive_character_split(document.content)

    def _recursive_character_split(self, text: str) -> list[DocumentChunk]:
        """
        Standard recursive text splitter. Attempts to split by paragraphs, then sentences, then words,
        until chunks are under the `chunk_size` limit.
        """
        # A simplified mock implementation of LangChain's RecursiveCharacterTextSplitter
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 > self.chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                # Handle overlap
                overlap_words = current_chunk[-max(1, self.chunk_overlap // 5) :]
                current_chunk = overlap_words
                current_length = sum(len(w) for w in current_chunk) + len(current_chunk)

            current_chunk.append(word)
            current_length += len(word) + 1

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return [DocumentChunk(text=c, chunk_index=i) for i, c in enumerate(chunks)]

    def _markdown_split(self, text: str) -> list[DocumentChunk]:
        """
        Splits text by markdown headers (##, ###) to preserve semantic sections.
        Falls back to recursive split for extremely long sections.
        """
        # Simplified: Split by double newline for now.
        # Production would use a robust AST parser or Regex like `r"\n#{1,6} "`
        sections = re.split(r"\n\n", text)
        chunks = []
        idx = 0

        for section in sections:
            section = section.strip()
            if not section:
                continue

            if len(section) > self.chunk_size:
                sub_chunks = self._recursive_character_split(section)
                for sc in sub_chunks:
                    chunks.append(DocumentChunk(text=sc.text, chunk_index=idx))
                    idx += 1
            else:
                chunks.append(DocumentChunk(text=section, chunk_index=idx))
                idx += 1

        return chunks
