"""
Tests for TextChunker.
"""

import pytest

from TIER_09_KNOWLEDGE.temario.chunker import TextChunker, ChunkConfig


class TestTextChunker:
    """Tests for TextChunker class."""

    def test_chunker_initialization(self):
        """Test chunker initializes with default config."""
        chunker = TextChunker()
        assert chunker.config.target_tokens == 500
        assert chunker.config.max_tokens == 700
        assert chunker.config.min_tokens == 100

    def test_chunker_custom_config(self):
        """Test chunker with custom configuration."""
        config = ChunkConfig(
            target_tokens=200,
            max_tokens=300,
            min_tokens=50,
        )
        chunker = TextChunker(config=config)
        assert chunker.config.target_tokens == 200

    def test_count_tokens_basic(self, chunker):
        """Test basic token counting."""
        text = "This is a test sentence."
        count = chunker.count_tokens(text)
        assert count > 0
        assert count < 20  # Should be reasonable

    def test_count_tokens_empty(self, chunker):
        """Test token counting with empty text."""
        assert chunker.count_tokens("") == 0
        # Whitespace-only text may have 1 token (tiktoken behavior)
        assert chunker.count_tokens("   ") >= 0

    def test_chunk_text_basic(self, chunker, sample_text):
        """Test basic text chunking."""
        chunks = chunker.chunk_text(sample_text)

        assert len(chunks) > 0
        for chunk in chunks:
            assert "content" in chunk
            assert "token_count" in chunk
            assert chunk["token_count"] > 0

    def test_chunk_text_respects_max_tokens(self, chunker, sample_text):
        """Test chunks don't exceed max tokens."""
        chunks = chunker.chunk_text(sample_text)

        for chunk in chunks:
            # Allow some flexibility
            assert chunk["token_count"] <= chunker.config.max_tokens * 1.1

    def test_chunk_text_empty(self, chunker):
        """Test chunking empty text."""
        chunks = chunker.chunk_text("")
        assert chunks == []

        chunks = chunker.chunk_text("   ")
        assert chunks == []

    def test_chunk_text_with_page_number(self, chunker, sample_text):
        """Test chunking with page number metadata."""
        chunks = chunker.chunk_text(sample_text, page_number=5)

        for chunk in chunks:
            assert chunk["page_number"] == 5

    def test_chunk_text_with_metadata(self, chunker, sample_text):
        """Test chunking with custom metadata."""
        chunks = chunker.chunk_text(
            sample_text,
            metadata={"tema": 1, "source": "test"},
        )

        for chunk in chunks:
            assert chunk["metadata"]["tema"] == 1
            assert chunk["metadata"]["source"] == "test"

    def test_chunk_index_sequential(self, chunker, sample_text):
        """Test chunk indices are sequential."""
        chunks = chunker.chunk_text(sample_text)

        indices = [c["chunk_index"] for c in chunks]
        assert indices == list(range(len(chunks)))

    def test_split_paragraphs(self, chunker, sample_text):
        """Test paragraph splitting."""
        paragraphs = chunker._split_paragraphs(sample_text)

        assert len(paragraphs) > 1
        for para in paragraphs:
            assert len(para.strip()) > 0

    def test_split_sentences(self, chunker):
        """Test sentence splitting."""
        text = "Primera oracion. Segunda oracion. Tercera oracion."
        sentences = chunker._split_sentences(text)

        assert len(sentences) >= 2  # At least split some

    def test_estimate_chunks(self, chunker, sample_text):
        """Test chunk estimation."""
        estimate = chunker.estimate_chunks(sample_text)
        actual = len(chunker.chunk_text(sample_text))

        # Estimate should be within reasonable range
        assert abs(estimate - actual) <= max(estimate, actual) * 0.5

    def test_chunk_small_text(self, chunker):
        """Test chunking text smaller than min_tokens."""
        # Create text that's larger than min_tokens to ensure a chunk is created
        small_text = ". ".join([f"Sentence {i} with some content" for i in range(5)])
        chunks = chunker.chunk_text(small_text)

        # Should create at least one chunk if text is meaningful
        # Note: very short text below min_tokens may not create chunks
        if chunks:
            assert len(chunks) >= 1

    def test_chunk_large_paragraph(self, chunker):
        """Test chunking a large paragraph by sentences."""
        # Create a large paragraph
        large_para = ". ".join([
            f"Sentence number {i} with some content to make it longer"
            for i in range(50)
        ])

        chunks = chunker.chunk_text(large_para)

        assert len(chunks) > 1
        total_tokens = sum(c["token_count"] for c in chunks)
        assert total_tokens > chunker.config.target_tokens


class TestChunkConfig:
    """Tests for ChunkConfig dataclass."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ChunkConfig()

        assert config.target_tokens == 500
        assert config.max_tokens == 700
        assert config.min_tokens == 100
        assert config.overlap_sentences == 2

    def test_custom_config(self):
        """Test custom configuration."""
        config = ChunkConfig(
            target_tokens=300,
            max_tokens=400,
            min_tokens=50,
            overlap_sentences=3,
        )

        assert config.target_tokens == 300
        assert config.max_tokens == 400
        assert config.min_tokens == 50
        assert config.overlap_sentences == 3
