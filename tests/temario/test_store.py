"""
Tests for TemarioStore.
"""

import pytest
import json

from temario.models import Document, Chunk
from temario.store import TemarioStore


class TestTemarioStore:
    """Tests for TemarioStore class."""

    def test_store_initialization(self, temp_db):
        """Test store initializes with database."""
        store = TemarioStore(db_path=temp_db)
        assert store.db_path.exists()

    def test_create_tables(self, store):
        """Test database tables are created."""
        import sqlite3

        with sqlite3.connect(store.db_path) as conn:
            cursor = conn.cursor()

            # Check documents table
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='temario_documents'"
            )
            assert cursor.fetchone() is not None

            # Check chunks table
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='temario_chunks'"
            )
            assert cursor.fetchone() is not None


class TestDocumentCRUD:
    """Tests for Document CRUD operations."""

    def test_create_document(self, store, sample_document):
        """Test creating a document."""
        created = store.create_document(sample_document)

        assert created.id is not None
        assert created.filename == sample_document.filename
        assert created.created_at is not None

    def test_get_document(self, store, sample_document):
        """Test retrieving a document."""
        created = store.create_document(sample_document)
        retrieved = store.get_document(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.filename == created.filename

    def test_get_document_not_found(self, store):
        """Test retrieving non-existent document."""
        result = store.get_document(9999)
        assert result is None

    def test_get_document_by_filename(self, store, sample_document):
        """Test retrieving document by filename."""
        created = store.create_document(sample_document)
        retrieved = store.get_document_by_filename(sample_document.filename)

        assert retrieved is not None
        assert retrieved.id == created.id

    def test_list_documents(self, store, sample_document):
        """Test listing documents."""
        store.create_document(sample_document)

        docs = store.list_documents()
        assert len(docs) >= 1

    def test_list_documents_pagination(self, store):
        """Test document list pagination."""
        for i in range(5):
            doc = Document(
                filename=f"doc_{i}.pdf",
                filepath=f"/path/doc_{i}.pdf",
                file_type="pdf",
            )
            store.create_document(doc)

        page1 = store.list_documents(limit=2, offset=0)
        page2 = store.list_documents(limit=2, offset=2)

        assert len(page1) == 2
        assert len(page2) >= 2
        assert page1[0].id != page2[0].id

    def test_update_document(self, store, sample_document):
        """Test updating a document."""
        created = store.create_document(sample_document)
        original_updated_at = created.updated_at
        created.title = "Updated Title"
        created.total_pages = 20

        updated = store.update_document(created)

        assert updated.title == "Updated Title"
        assert updated.total_pages == 20
        # updated_at should be updated (may be same if very fast)
        assert updated.updated_at >= original_updated_at

    def test_delete_document(self, store, sample_document):
        """Test deleting a document."""
        created = store.create_document(sample_document)
        deleted = store.delete_document(created.id)

        assert deleted is True
        assert store.get_document(created.id) is None

    def test_delete_document_not_found(self, store):
        """Test deleting non-existent document."""
        deleted = store.delete_document(9999)
        assert deleted is False


class TestChunkCRUD:
    """Tests for Chunk CRUD operations."""

    def test_create_chunk(self, store, sample_document):
        """Test creating a chunk."""
        doc = store.create_document(sample_document)

        chunk = Chunk(
            document_id=doc.id,
            content="Test content",
            token_count=10,
            chunk_index=0,
        )
        created = store.create_chunk(chunk)

        assert created.id is not None
        assert created.content == "Test content"

    def test_create_chunks_batch(self, store, sample_document, sample_chunks):
        """Test creating multiple chunks in batch."""
        doc = store.create_document(sample_document)

        for chunk in sample_chunks:
            chunk.document_id = doc.id

        created = store.create_chunks_batch(sample_chunks)

        assert len(created) == len(sample_chunks)
        for chunk in created:
            assert chunk.id is not None

    def test_get_chunk(self, store, sample_document, sample_chunks):
        """Test retrieving a chunk."""
        doc = store.create_document(sample_document)
        for chunk in sample_chunks:
            chunk.document_id = doc.id

        created = store.create_chunks_batch(sample_chunks)
        retrieved = store.get_chunk(created[0].id)

        assert retrieved is not None
        assert retrieved.content == created[0].content

    def test_get_chunks_by_document(self, store, sample_document, sample_chunks):
        """Test retrieving chunks by document."""
        doc = store.create_document(sample_document)
        for chunk in sample_chunks:
            chunk.document_id = doc.id

        store.create_chunks_batch(sample_chunks)
        retrieved = store.get_chunks_by_document(doc.id)

        assert len(retrieved) == len(sample_chunks)

    def test_get_chunks_by_tema(self, store, sample_document, sample_chunks):
        """Test retrieving chunks by tema."""
        doc = store.create_document(sample_document)
        for chunk in sample_chunks:
            chunk.document_id = doc.id
            chunk.tema = 1

        store.create_chunks_batch(sample_chunks)
        retrieved = store.get_chunks_by_tema(1)

        assert len(retrieved) == len(sample_chunks)

    def test_update_chunk_embedding(self, store, sample_document):
        """Test updating chunk embedding."""
        doc = store.create_document(sample_document)
        chunk = Chunk(
            document_id=doc.id,
            content="Test",
            token_count=5,
            chunk_index=0,
        )
        created = store.create_chunk(chunk)

        embedding = [0.1] * 1024
        updated = store.update_chunk_embedding(created.id, embedding)

        assert updated is True

        retrieved = store.get_chunk(created.id)
        assert retrieved.embedding is not None
        assert len(retrieved.embedding) == 1024

    def test_update_chunks_embeddings_batch(self, store, sample_document, sample_chunks):
        """Test batch embedding update."""
        doc = store.create_document(sample_document)
        for chunk in sample_chunks:
            chunk.document_id = doc.id

        created = store.create_chunks_batch(sample_chunks)

        chunk_ids = [c.id for c in created]
        embeddings = [[0.1] * 1024 for _ in chunk_ids]

        updated = store.update_chunks_embeddings_batch(chunk_ids, embeddings)
        assert updated == len(chunk_ids)

    def test_delete_chunks_by_document(self, store, sample_document, sample_chunks):
        """Test deleting chunks by document."""
        doc = store.create_document(sample_document)
        for chunk in sample_chunks:
            chunk.document_id = doc.id

        store.create_chunks_batch(sample_chunks)

        deleted = store.delete_chunks_by_document(doc.id)
        assert deleted == len(sample_chunks)

        remaining = store.get_chunks_by_document(doc.id)
        assert len(remaining) == 0


class TestStoreStats:
    """Tests for store statistics."""

    def test_get_stats_empty(self, store):
        """Test stats with empty database."""
        stats = store.get_stats()

        assert stats["documents"] == 0
        assert stats["chunks"] == 0
        assert stats["embeddings"] == 0

    def test_get_stats_with_data(self, store, sample_document, sample_chunks):
        """Test stats with data."""
        doc = store.create_document(sample_document)
        for chunk in sample_chunks:
            chunk.document_id = doc.id

        store.create_chunks_batch(sample_chunks)

        stats = store.get_stats()

        assert stats["documents"] == 1
        assert stats["chunks"] == len(sample_chunks)
        assert stats["total_tokens"] > 0


class TestEmbeddingStorage:
    """Tests for embedding storage and retrieval."""

    def test_store_and_retrieve_embedding(self, store, sample_document):
        """Test storing and retrieving embeddings."""
        doc = store.create_document(sample_document)
        chunk = Chunk(
            document_id=doc.id,
            content="Test content for embedding",
            token_count=20,
            chunk_index=0,
            embedding=[0.5] * 1024,
        )
        created = store.create_chunk(chunk)

        retrieved = store.get_chunk(created.id)
        assert retrieved.embedding is not None
        assert len(retrieved.embedding) == 1024
        assert all(e == 0.5 for e in retrieved.embedding)

    def test_get_all_embeddings(self, store, sample_document, sample_chunks):
        """Test retrieving all embeddings."""
        doc = store.create_document(sample_document)

        for i, chunk in enumerate(sample_chunks):
            chunk.document_id = doc.id
            chunk.embedding = [0.1 * i] * 1024

        store.create_chunks_batch(sample_chunks)

        all_embeddings = store.get_all_embeddings()

        assert len(all_embeddings) == len(sample_chunks)
        for chunk_id, embedding in all_embeddings:
            assert len(embedding) == 1024
