"""
Integration tests for the temario ingestion system.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from TIER_09_KNOWLEDGE.temario.store import TemarioStore
from TIER_09_KNOWLEDGE.temario.parser import DocumentParser
from TIER_09_KNOWLEDGE.temario.chunker import TextChunker, ChunkConfig
from TIER_09_KNOWLEDGE.temario.embedder import MistralEmbedder
from TIER_09_KNOWLEDGE.temario.searcher import SemanticSearcher
from TIER_09_KNOWLEDGE.temario.ingest import TemarioIngestor
from TIER_09_KNOWLEDGE.temario.models import Document, Chunk


class TestEmbedderMocked:
    """Tests for embedder with mocked API."""

    @pytest.fixture
    def mock_embedder(self):
        """Create embedder with mocked API key."""
        with patch.dict(os.environ, {"MISTRAL_API_KEY": "test-key"}):
            return MistralEmbedder(api_key="test-key", batch_size=10)

    def test_embedder_initialization(self, mock_embedder):
        """Test embedder initializes."""
        assert mock_embedder.api_key == "test-key"
        assert mock_embedder.batch_size == 10

    def test_dimensions_property(self, mock_embedder):
        """Test dimensions property."""
        assert mock_embedder.dimensions == 1024

    def test_model_name_property(self, mock_embedder):
        """Test model name property."""
        assert mock_embedder.model_name == "mistral-embed"

    @patch('httpx.Client.post')
    def test_embed_single(self, mock_post, mock_embedder):
        """Test embedding single text."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"index": 0, "embedding": [0.1] * 1024}]
        }
        mock_post.return_value.__enter__.return_value.post = Mock(return_value=mock_response)
        mock_post.return_value.__enter__.return_value = mock_response

        # Use direct API call mock
        with patch.object(mock_embedder, '_call_api') as mock_call:
            mock_call.return_value = [[0.1] * 1024]
            result = mock_embedder.embed("test text")
            assert len(result) == 1024


class TestSearcherMocked:
    """Tests for searcher with mocked dependencies."""

    @pytest.fixture
    def mock_store(self):
        """Create mock store."""
        store = Mock(spec=TemarioStore)
        store.get_all_embeddings.return_value = [
            (1, [0.1] * 1024),
            (2, [0.2] * 1024),
            (3, [0.3] * 1024),
        ]
        store.get_chunks_by_ids.return_value = [
            Chunk(id=1, document_id=1, content="Content 1", token_count=10, chunk_index=0, tema=1),
            Chunk(id=2, document_id=1, content="Content 2", token_count=10, chunk_index=1, tema=1),
            Chunk(id=3, document_id=1, content="Content 3", token_count=10, chunk_index=2, tema=2),
        ]
        return store

    @pytest.fixture
    def mock_embedder(self):
        """Create mock embedder."""
        embedder = Mock(spec=MistralEmbedder)
        embedder.embed.return_value = [0.15] * 1024  # Similar to chunk 1
        return embedder

    def test_searcher_initialization(self, mock_store, mock_embedder):
        """Test searcher initializes."""
        searcher = SemanticSearcher(store=mock_store, embedder=mock_embedder)
        assert searcher.store == mock_store
        assert searcher.embedder == mock_embedder

    def test_search_basic(self, mock_store, mock_embedder):
        """Test basic search."""
        searcher = SemanticSearcher(store=mock_store, embedder=mock_embedder)

        results = searcher.search("test query", limit=3)

        assert len(results) <= 3
        mock_embedder.embed.assert_called_once_with("test query")
        mock_store.get_all_embeddings.assert_called_once()

    def test_search_with_tema_filter(self, mock_store, mock_embedder):
        """Test search with tema filter."""
        searcher = SemanticSearcher(store=mock_store, embedder=mock_embedder)

        results = searcher.search("test query", tema=1)

        for result in results:
            if result.chunk.tema is not None:
                assert result.chunk.tema == 1


class TestIngestionPipeline:
    """Tests for the full ingestion pipeline."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def ingestor(self, temp_dir):
        """Create ingestor with temp database."""
        db_path = os.path.join(temp_dir, "test.db")

        with patch.dict(os.environ, {"MISTRAL_API_KEY": "test-key"}):
            ingestor = TemarioIngestor(
                db_path=db_path,
                api_key="test-key",
            )
            return ingestor

    def test_ingestor_initialization(self, ingestor):
        """Test ingestor initializes correctly."""
        assert ingestor.store is not None
        assert ingestor.parser is not None
        assert ingestor.chunker is not None
        assert ingestor.embedder is not None

    def test_get_stats(self, ingestor):
        """Test getting statistics."""
        stats = ingestor.get_stats()

        assert "documents" in stats
        assert "chunks" in stats
        assert "embeddings" in stats

    def test_ingest_nonexistent_file(self, ingestor):
        """Test ingesting non-existent file fails gracefully."""
        result = ingestor.ingest("/nonexistent/file.pdf", skip_embeddings=True)

        assert result.success is False
        assert len(result.errors) > 0


class TestEndToEnd:
    """End-to-end tests with real components (mocked API)."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            yield f.name
        os.unlink(f.name)

    def test_full_workflow(self, temp_db):
        """Test full workflow: create, store, search."""
        # 1. Create store
        store = TemarioStore(db_path=temp_db)

        # 2. Create document
        doc = Document(
            filename="test.pdf",
            filepath="/test/test.pdf",
            file_type="pdf",
            tema=1,
            title="Tema 1: Test",
        )
        doc = store.create_document(doc)

        # 3. Create chunks
        chunks = [
            Chunk(
                document_id=doc.id,
                content="El Derecho Administrativo regula la Administracion Publica.",
                token_count=20,
                chunk_index=i,
                tema=1,
            )
            for i in range(3)
        ]
        chunks = store.create_chunks_batch(chunks)

        # 4. Update document
        doc.total_chunks = len(chunks)
        store.update_document(doc)

        # 5. Verify
        retrieved_doc = store.get_document(doc.id)
        assert retrieved_doc.total_chunks == 3

        retrieved_chunks = store.get_chunks_by_document(doc.id)
        assert len(retrieved_chunks) == 3

        # 6. Stats
        stats = store.get_stats()
        assert stats["documents"] == 1
        assert stats["chunks"] == 3


class TestConfigLoading:
    """Tests for configuration loading."""

    def test_default_config(self):
        """Test default configuration is loaded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")

            with patch.dict(os.environ, {"MISTRAL_API_KEY": "test-key"}):
                ingestor = TemarioIngestor(db_path=db_path)

                assert "database" in ingestor.config
                assert "chunking" in ingestor.config
                assert ingestor.config["chunking"]["target_tokens"] == 500

    def test_custom_config(self):
        """Test custom configuration loading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "config.yaml")
            db_path = os.path.join(tmpdir, "test.db")

            # Write custom config
            with open(config_path, "w") as f:
                f.write("""
chunking:
  target_tokens: 300
  max_tokens: 400
database:
  path: custom.db
""")

            with patch.dict(os.environ, {"MISTRAL_API_KEY": "test-key"}):
                ingestor = TemarioIngestor(
                    config_path=config_path,
                    db_path=db_path,
                )

                assert ingestor.config["chunking"]["target_tokens"] == 300
                assert ingestor.config["chunking"]["max_tokens"] == 400
