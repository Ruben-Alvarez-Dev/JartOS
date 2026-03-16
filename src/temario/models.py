"""
Data models for the temario ingestion system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json


@dataclass
class Document:
    """Represents an ingested document."""

    id: Optional[int] = None
    filename: str = ""
    filepath: str = ""
    file_type: str = ""  # 'pdf' or 'docx'
    title: Optional[str] = None
    tema: Optional[int] = None
    total_pages: int = 0
    total_chunks: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "filename": self.filename,
            "filepath": self.filepath,
            "file_type": self.file_type,
            "title": self.title,
            "tema": self.tema,
            "total_pages": self.total_pages,
            "total_chunks": self.total_chunks,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Document":
        """Create from dictionary."""
        return cls(
            id=data.get("id"),
            filename=data.get("filename", ""),
            filepath=data.get("filepath", ""),
            file_type=data.get("file_type", ""),
            title=data.get("title"),
            tema=data.get("tema"),
            total_pages=data.get("total_pages", 0),
            total_chunks=data.get("total_chunks", 0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class Chunk:
    """Represents a text chunk from a document."""

    id: Optional[int] = None
    document_id: int = 0
    content: str = ""
    token_count: int = 0
    chunk_index: int = 0
    page_number: Optional[int] = None
    tema: Optional[int] = None
    apartado: Optional[str] = None
    titulo: Optional[str] = None
    embedding: Optional[list] = None
    created_at: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "document_id": self.document_id,
            "content": self.content,
            "token_count": self.token_count,
            "chunk_index": self.chunk_index,
            "page_number": self.page_number,
            "tema": self.tema,
            "apartado": self.apartado,
            "titulo": self.titulo,
            "embedding": self.embedding,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Chunk":
        """Create from dictionary."""
        return cls(
            id=data.get("id"),
            document_id=data.get("document_id", 0),
            content=data.get("content", ""),
            token_count=data.get("token_count", 0),
            chunk_index=data.get("chunk_index", 0),
            page_number=data.get("page_number"),
            tema=data.get("tema"),
            apartado=data.get("apartado"),
            titulo=data.get("titulo"),
            embedding=data.get("embedding"),
            created_at=data.get("created_at"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class SearchResult:
    """Represents a search result."""

    chunk: Chunk
    score: float
    search_type: str  # 'semantic' or 'hybrid'

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "chunk": self.chunk.to_dict(),
            "score": self.score,
            "search_type": self.search_type,
        }


@dataclass
class IngestionResult:
    """Result of an ingestion operation."""

    success: bool
    document: Optional[Document] = None
    chunks_created: int = 0
    embeddings_created: int = 0
    errors: list = field(default_factory=list)
    duration_seconds: float = 0.0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "document": self.document.to_dict() if self.document else None,
            "chunks_created": self.chunks_created,
            "embeddings_created": self.embeddings_created,
            "errors": self.errors,
            "duration_seconds": self.duration_seconds,
        }
