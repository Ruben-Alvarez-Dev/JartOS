"""
TemarioStore - SQLite-based storage for temario chunks and embeddings.

Provides CRUD operations for documents and chunks with vector similarity search.
"""

import sqlite3
import json
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from .models import Document, Chunk, SearchResult

logger = logging.getLogger(__name__)


class TemarioStore:
    """SQLite-based storage for temario documents and chunks."""

    def __init__(self, db_path: str = "data/temario.db"):
        """
        Initialize the store.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Documents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS temario_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    filepath TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    title TEXT,
                    tema INTEGER,
                    total_pages INTEGER DEFAULT 0,
                    total_chunks INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    metadata TEXT DEFAULT '{}'
                )
            """)

            # Chunks table with embedding storage
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS temario_chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    token_count INTEGER DEFAULT 0,
                    chunk_index INTEGER NOT NULL,
                    page_number INTEGER,
                    tema INTEGER,
                    apartado TEXT,
                    titulo TEXT,
                    embedding TEXT,
                    created_at TEXT NOT NULL,
                    metadata TEXT DEFAULT '{}',
                    FOREIGN KEY (document_id) REFERENCES temario_documents(id) ON DELETE CASCADE
                )
            """)

            # Create indexes for efficient querying
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_chunks_document_id
                ON temario_chunks(document_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_chunks_tema
                ON temario_chunks(tema)
            """)

            conn.commit()
            logger.info(f"Database initialized at {self.db_path}")

    # ============ Document CRUD ============

    def create_document(self, document: Document) -> Document:
        """
        Create a new document record.

        Args:
            document: Document to create (without id)

        Returns:
            Created document with id
        """
        now = datetime.now().isoformat()
        document.created_at = now
        document.updated_at = now

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO temario_documents
                (filename, filepath, file_type, title, tema, total_pages,
                 total_chunks, created_at, updated_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                document.filename,
                document.filepath,
                document.file_type,
                document.title,
                document.tema,
                document.total_pages,
                document.total_chunks,
                document.created_at,
                document.updated_at,
                json.dumps(document.metadata),
            ))
            document.id = cursor.lastrowid
            conn.commit()

        logger.info(f"Created document: {document.filename} (id={document.id})")
        return document

    def get_document(self, doc_id: int) -> Optional[Document]:
        """
        Get a document by ID.

        Args:
            doc_id: Document ID

        Returns:
            Document or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM temario_documents WHERE id = ?", (doc_id,)
            )
            row = cursor.fetchone()
            if row:
                return Document.from_dict({
                    **dict(row),
                    "metadata": json.loads(row["metadata"]),
                })
        return None

    def get_document_by_filename(self, filename: str) -> Optional[Document]:
        """
        Get a document by filename.

        Args:
            filename: Document filename

        Returns:
            Document or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM temario_documents WHERE filename = ?", (filename,)
            )
            row = cursor.fetchone()
            if row:
                return Document.from_dict({
                    **dict(row),
                    "metadata": json.loads(row["metadata"]),
                })
        return None

    def list_documents(self, limit: int = 100, offset: int = 0) -> List[Document]:
        """
        List all documents.

        Args:
            limit: Maximum number of documents to return
            offset: Offset for pagination

        Returns:
            List of documents
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM temario_documents
                   ORDER BY created_at DESC LIMIT ? OFFSET ?""",
                (limit, offset),
            )
            rows = cursor.fetchall()
            return [
                Document.from_dict({
                    **dict(row),
                    "metadata": json.loads(row["metadata"]),
                })
                for row in rows
            ]

    def update_document(self, document: Document) -> Document:
        """
        Update a document.

        Args:
            document: Document to update (must have id)

        Returns:
            Updated document
        """
        document.updated_at = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE temario_documents
                SET filename=?, filepath=?, file_type=?, title=?, tema=?,
                    total_pages=?, total_chunks=?, updated_at=?, metadata=?
                WHERE id=?
            """, (
                document.filename,
                document.filepath,
                document.file_type,
                document.title,
                document.tema,
                document.total_pages,
                document.total_chunks,
                document.updated_at,
                json.dumps(document.metadata),
                document.id,
            ))
            conn.commit()

        logger.info(f"Updated document: {document.filename} (id={document.id})")
        return document

    def delete_document(self, doc_id: int) -> bool:
        """
        Delete a document and all its chunks.

        Args:
            doc_id: Document ID

        Returns:
            True if deleted, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Chunks are deleted by CASCADE
            cursor.execute("DELETE FROM temario_documents WHERE id = ?", (doc_id,))
            deleted = cursor.rowcount > 0
            conn.commit()

        if deleted:
            logger.info(f"Deleted document id={doc_id}")
        return deleted

    # ============ Chunk CRUD ============

    def create_chunk(self, chunk: Chunk) -> Chunk:
        """
        Create a new chunk record.

        Args:
            chunk: Chunk to create (without id)

        Returns:
            Created chunk with id
        """
        chunk.created_at = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO temario_chunks
                (document_id, content, token_count, chunk_index, page_number,
                 tema, apartado, titulo, embedding, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                chunk.document_id,
                chunk.content,
                chunk.token_count,
                chunk.chunk_index,
                chunk.page_number,
                chunk.tema,
                chunk.apartado,
                chunk.titulo,
                json.dumps(chunk.embedding) if chunk.embedding else None,
                chunk.created_at,
                json.dumps(chunk.metadata),
            ))
            chunk.id = cursor.lastrowid
            conn.commit()

        return chunk

    def create_chunks_batch(self, chunks: List[Chunk]) -> List[Chunk]:
        """
        Create multiple chunks in a single transaction.

        Args:
            chunks: List of chunks to create

        Returns:
            List of created chunks with ids
        """
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for chunk in chunks:
                chunk.created_at = now
                cursor.execute("""
                    INSERT INTO temario_chunks
                    (document_id, content, token_count, chunk_index, page_number,
                     tema, apartado, titulo, embedding, created_at, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    chunk.document_id,
                    chunk.content,
                    chunk.token_count,
                    chunk.chunk_index,
                    chunk.page_number,
                    chunk.tema,
                    chunk.apartado,
                    chunk.titulo,
                    json.dumps(chunk.embedding) if chunk.embedding else None,
                    chunk.created_at,
                    json.dumps(chunk.metadata),
                ))
                chunk.id = cursor.lastrowid
            conn.commit()

        logger.info(f"Created {len(chunks)} chunks in batch")
        return chunks

    def get_chunk(self, chunk_id: int) -> Optional[Chunk]:
        """
        Get a chunk by ID.

        Args:
            chunk_id: Chunk ID

        Returns:
            Chunk or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM temario_chunks WHERE id = ?", (chunk_id,)
            )
            row = cursor.fetchone()
            if row:
                return self._row_to_chunk(row)
        return None

    def get_chunks_by_document(self, doc_id: int) -> List[Chunk]:
        """
        Get all chunks for a document.

        Args:
            doc_id: Document ID

        Returns:
            List of chunks
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM temario_chunks
                   WHERE document_id = ? ORDER BY chunk_index""",
                (doc_id,),
            )
            rows = cursor.fetchall()
            return [self._row_to_chunk(row) for row in rows]

    def get_chunks_by_tema(self, tema: int) -> List[Chunk]:
        """
        Get all chunks for a tema.

        Args:
            tema: Tema number

        Returns:
            List of chunks
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM temario_chunks
                   WHERE tema = ? ORDER BY document_id, chunk_index""",
                (tema,),
            )
            rows = cursor.fetchall()
            return [self._row_to_chunk(row) for row in rows]

    def update_chunk_embedding(self, chunk_id: int, embedding: List[float]) -> bool:
        """
        Update a chunk's embedding.

        Args:
            chunk_id: Chunk ID
            embedding: Embedding vector

        Returns:
            True if updated, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE temario_chunks SET embedding = ? WHERE id = ?",
                (json.dumps(embedding), chunk_id),
            )
            updated = cursor.rowcount > 0
            conn.commit()

        return updated

    def update_chunks_embeddings_batch(
        self, chunk_ids: List[int], embeddings: List[List[float]]
    ) -> int:
        """
        Update embeddings for multiple chunks.

        Args:
            chunk_ids: List of chunk IDs
            embeddings: List of embedding vectors (same order as chunk_ids)

        Returns:
            Number of chunks updated
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            updated = 0
            for chunk_id, embedding in zip(chunk_ids, embeddings):
                cursor.execute(
                    "UPDATE temario_chunks SET embedding = ? WHERE id = ?",
                    (json.dumps(embedding), chunk_id),
                )
                updated += cursor.rowcount
            conn.commit()

        logger.info(f"Updated embeddings for {updated} chunks")
        return updated

    def delete_chunks_by_document(self, doc_id: int) -> int:
        """
        Delete all chunks for a document.

        Args:
            doc_id: Document ID

        Returns:
            Number of chunks deleted
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM temario_chunks WHERE document_id = ?", (doc_id,)
            )
            deleted = cursor.rowcount
            conn.commit()

        logger.info(f"Deleted {deleted} chunks for document id={doc_id}")
        return deleted

    # ============ Vector Search ============

    def get_all_embeddings(self) -> List[tuple]:
        """
        Get all chunk IDs and embeddings for similarity search.

        Returns:
            List of (chunk_id, embedding) tuples
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, embedding FROM temario_chunks WHERE embedding IS NOT NULL"
            )
            rows = cursor.fetchall()
            return [
                (row["id"], json.loads(row["embedding"]))
                for row in rows
            ]

    def get_chunks_by_ids(self, chunk_ids: List[int]) -> List[Chunk]:
        """
        Get multiple chunks by IDs.

        Args:
            chunk_ids: List of chunk IDs

        Returns:
            List of chunks
        """
        if not chunk_ids:
            return []

        placeholders = ",".join("?" * len(chunk_ids))
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT * FROM temario_chunks WHERE id IN ({placeholders})",
                chunk_ids,
            )
            rows = cursor.fetchall()
            return [self._row_to_chunk(row) for row in rows]

    # ============ Statistics ============

    def get_stats(self) -> dict:
        """
        Get database statistics.

        Returns:
            Dictionary with statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM temario_documents")
            doc_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM temario_chunks")
            chunk_count = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM temario_chunks WHERE embedding IS NOT NULL"
            )
            embedding_count = cursor.fetchone()[0]

            cursor.execute(
                "SELECT SUM(token_count) FROM temario_chunks"
            )
            total_tokens = cursor.fetchone()[0] or 0

            return {
                "documents": doc_count,
                "chunks": chunk_count,
                "embeddings": embedding_count,
                "total_tokens": total_tokens,
            }

    # ============ Helpers ============

    def _row_to_chunk(self, row: sqlite3.Row) -> Chunk:
        """Convert a database row to a Chunk object."""
        return Chunk.from_dict({
            **dict(row),
            "embedding": json.loads(row["embedding"]) if row["embedding"] else None,
            "metadata": json.loads(row["metadata"]),
        })
