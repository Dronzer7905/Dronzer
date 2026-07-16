from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger("dronzer.knowledge.parsers")


class ParsedDocument:
    def __init__(self, content: str, metadata: dict[str, Any]):
        self.content = content
        self.metadata = metadata


class BaseParser(ABC):
    """Abstract interface for extracting text from files."""

    @abstractmethod
    async def parse(self, file_path: Path) -> ParsedDocument:
        pass


class TextParser(BaseParser):
    """Simple parser for raw TXT files."""

    async def parse(self, file_path: Path) -> ParsedDocument:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        return ParsedDocument(content=content, metadata={"source": str(file_path), "type": "txt"})


class MarkdownParser(BaseParser):
    """Parser for MD files. Retains markdown syntax for smart chunking later."""

    async def parse(self, file_path: Path) -> ParsedDocument:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        return ParsedDocument(content=content, metadata={"source": str(file_path), "type": "md"})


class PDFParser(BaseParser):
    """
    Parser for PDF files.
    In a real implementation, this would use `PyMuPDF` (fitz) or `pypdf` to extract text and tables.
    """

    async def parse(self, file_path: Path) -> ParsedDocument:
        logger.info(f"Parsing PDF: {file_path}")
        # Simulated extraction
        content = "Extracted text from PDF simulation."
        return ParsedDocument(
            content=content, metadata={"source": str(file_path), "type": "pdf", "pages": 1}
        )


class ParserFactory:
    """Returns the correct parser based on file extension."""

    @staticmethod
    def get_parser(file_path: Path) -> BaseParser:
        ext = file_path.suffix.lower()
        if ext == ".md":
            return MarkdownParser()
        elif ext == ".pdf":
            return PDFParser()
        elif ext in [".txt", ".csv", ".json"]:
            return TextParser()
        else:
            raise ValueError(f"Unsupported file type for ingestion: {ext}")
