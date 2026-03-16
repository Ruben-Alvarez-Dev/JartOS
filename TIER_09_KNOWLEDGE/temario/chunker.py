"""
TextChunker - Intelligent text chunking for temario documents.

Splits text into semantic chunks of approximately 500 tokens,
respecting sentence and paragraph boundaries.
"""

import re
import logging
from typing import List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Try to import tiktoken, fall back to word-based estimation
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    logger.warning("tiktoken not available, using word-based token estimation")


@dataclass
class ChunkConfig:
    """Configuration for text chunking."""

    target_tokens: int = 500
    max_tokens: int = 700
    min_tokens: int = 100
    overlap_sentences: int = 2
    encoding_name: str = "cl100k_base"


class TextChunker:
    """
    Intelligent text chunker for temario documents.

    Splits text into chunks of approximately target_tokens while
    respecting semantic boundaries (paragraphs, sentences).
    """

    # Sentence boundary pattern (handles Spanish punctuation)
    SENTENCE_PATTERN = re.compile(
        r'(?<=[.!?。।။])\s+(?=[A-ZÁÉÍÓÚÑÜa-záéíóúñü])|'
        r'(?<=\n)\s*(?=[A-ZÁÉÍÓÚÑÜa-záéíóúñü\d])'
    )

    # Paragraph boundary pattern
    PARAGRAPH_PATTERN = re.compile(r'\n\s*\n')

    def __init__(self, config: Optional[ChunkConfig] = None):
        """
        Initialize the chunker.

        Args:
            config: Chunking configuration
        """
        self.config = config or ChunkConfig()

        # Initialize tokenizer
        if TIKTOKEN_AVAILABLE:
            try:
                self.encoder = tiktoken.get_encoding(self.config.encoding_name)
            except Exception:
                self.encoder = None
        else:
            self.encoder = None

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in text.

        Uses tiktoken if available, otherwise estimates based on words.

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        if self.encoder:
            return len(self.encoder.encode(text))
        else:
            # Fallback: ~1.3 tokens per word for Spanish
            words = len(text.split())
            return int(words * 1.3)

    def chunk_text(
        self,
        text: str,
        page_number: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> List[dict]:
        """
        Chunk text into semantic segments.

        Args:
            text: Text to chunk
            page_number: Optional page number for metadata
            metadata: Optional additional metadata

        Returns:
            List of chunk dictionaries with content, token_count, and metadata
        """
        if not text or not text.strip():
            return []

        # First, split by paragraphs
        paragraphs = self._split_paragraphs(text)
        chunks = []
        current_chunk = []
        current_tokens = 0
        chunk_index = 0

        for para in paragraphs:
            para_tokens = self.count_tokens(para)

            # If single paragraph is too large, split by sentences
            if para_tokens > self.config.max_tokens:
                # Save current chunk first
                if current_chunk:
                    chunk = self._create_chunk(
                        current_chunk, chunk_index, page_number, metadata
                    )
                    chunks.append(chunk)
                    chunk_index += 1
                    current_chunk = []
                    current_tokens = 0

                # Split large paragraph by sentences
                sentence_chunks = self._chunk_large_paragraph(
                    para, page_number, metadata, chunk_index
                )
                chunks.extend(sentence_chunks)
                chunk_index += len(sentence_chunks)

            # If adding paragraph exceeds max, start new chunk
            elif current_tokens + para_tokens > self.config.max_tokens:
                # Check if current chunk is large enough
                if current_tokens >= self.config.min_tokens:
                    chunk = self._create_chunk(
                        current_chunk, chunk_index, page_number, metadata
                    )
                    chunks.append(chunk)
                    chunk_index += 1

                    # Start new chunk with overlap
                    overlap = self._get_overlap_sentences(current_chunk)
                    current_chunk = overlap + [para]
                    current_tokens = sum(self.count_tokens(p) for p in current_chunk)
                else:
                    # Current chunk too small, add anyway
                    current_chunk.append(para)
                    current_tokens += para_tokens

            else:
                # Add paragraph to current chunk
                current_chunk.append(para)
                current_tokens += para_tokens

                # Check if we've reached target
                if current_tokens >= self.config.target_tokens:
                    chunk = self._create_chunk(
                        current_chunk, chunk_index, page_number, metadata
                    )
                    chunks.append(chunk)
                    chunk_index += 1
                    current_chunk = []
                    current_tokens = 0

        # Don't forget the last chunk
        if current_chunk and current_tokens >= self.config.min_tokens:
            chunk = self._create_chunk(
                current_chunk, chunk_index, page_number, metadata
            )
            chunks.append(chunk)

        logger.debug(f"Created {len(chunks)} chunks from text")
        return chunks

    def _split_paragraphs(self, text: str) -> List[str]:
        """
        Split text into paragraphs.

        Args:
            text: Text to split

        Returns:
            List of paragraphs
        """
        # Split by double newlines
        paragraphs = self.PARAGRAPH_PATTERN.split(text)

        # Clean up and filter empty paragraphs
        return [p.strip() for p in paragraphs if p.strip()]

    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.

        Args:
            text: Text to split

        Returns:
            List of sentences
        """
        sentences = self.SENTENCE_PATTERN.split(text)
        return [s.strip() for s in sentences if s.strip()]

    def _chunk_large_paragraph(
        self,
        paragraph: str,
        page_number: Optional[int],
        metadata: Optional[dict],
        start_index: int,
    ) -> List[dict]:
        """
        Chunk a large paragraph by sentences.

        Args:
            paragraph: Paragraph text
            page_number: Page number
            metadata: Additional metadata
            start_index: Starting chunk index

        Returns:
            List of chunk dictionaries
        """
        sentences = self._split_sentences(paragraph)
        chunks = []
        current_sentences = []
        current_tokens = 0
        chunk_index = start_index

        for sentence in sentences:
            sentence_tokens = self.count_tokens(sentence)

            if current_tokens + sentence_tokens > self.config.max_tokens:
                if current_sentences:
                    chunk = self._create_chunk_from_sentences(
                        current_sentences, chunk_index, page_number, metadata
                    )
                    chunks.append(chunk)
                    chunk_index += 1

                    # Add overlap
                    overlap = current_sentences[-self.config.overlap_sentences:]
                    current_sentences = overlap + [sentence]
                    current_tokens = sum(self.count_tokens(s) for s in current_sentences)
            else:
                current_sentences.append(sentence)
                current_tokens += sentence_tokens

                if current_tokens >= self.config.target_tokens:
                    chunk = self._create_chunk_from_sentences(
                        current_sentences, chunk_index, page_number, metadata
                    )
                    chunks.append(chunk)
                    chunk_index += 1
                    current_sentences = []
                    current_tokens = 0

        if current_sentences and current_tokens >= self.config.min_tokens:
            chunk = self._create_chunk_from_sentences(
                current_sentences, chunk_index, page_number, metadata
            )
            chunks.append(chunk)

        return chunks

    def _get_overlap_sentences(self, paragraphs: List[str]) -> List[str]:
        """
        Get the last N sentences for overlap.

        Args:
            paragraphs: List of paragraphs

        Returns:
            List of sentences for overlap
        """
        if not paragraphs:
            return []

        # Get sentences from last paragraph
        last_para = paragraphs[-1]
        sentences = self._split_sentences(last_para)

        if len(sentences) <= self.config.overlap_sentences:
            return [last_para]

        # Return last N sentences as single paragraph
        overlap = sentences[-self.config.overlap_sentences:]
        return [" ".join(overlap)]

    def _create_chunk(
        self,
        paragraphs: List[str],
        chunk_index: int,
        page_number: Optional[int],
        metadata: Optional[dict],
    ) -> dict:
        """
        Create a chunk dictionary from paragraphs.

        Args:
            paragraphs: List of paragraphs
            chunk_index: Index of this chunk
            page_number: Page number
            metadata: Additional metadata

        Returns:
            Chunk dictionary
        """
        content = "\n\n".join(paragraphs)
        token_count = self.count_tokens(content)

        chunk = {
            "content": content,
            "token_count": token_count,
            "chunk_index": chunk_index,
            "page_number": page_number,
            "metadata": metadata or {},
        }

        return chunk

    def _create_chunk_from_sentences(
        self,
        sentences: List[str],
        chunk_index: int,
        page_number: Optional[int],
        metadata: Optional[dict],
    ) -> dict:
        """
        Create a chunk dictionary from sentences.

        Args:
            sentences: List of sentences
            chunk_index: Index of this chunk
            page_number: Page number
            metadata: Additional metadata

        Returns:
            Chunk dictionary
        """
        content = " ".join(sentences)
        token_count = self.count_tokens(content)

        chunk = {
            "content": content,
            "token_count": token_count,
            "chunk_index": chunk_index,
            "page_number": page_number,
            "metadata": metadata or {},
        }

        return chunk

    def estimate_chunks(self, text: str) -> int:
        """
        Estimate the number of chunks for a text.

        Args:
            text: Text to estimate

        Returns:
            Estimated number of chunks
        """
        total_tokens = self.count_tokens(text)
        return max(1, total_tokens // self.config.target_tokens)
