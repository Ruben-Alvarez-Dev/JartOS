"""
SemanticSearcher - Semantic search over temario chunks.

Provides similarity search using cosine similarity and optional
hybrid search combining semantic and keyword matching.
"""

import math
import logging
from typing import List, Optional, Tuple
from dataclasses import dataclass

from .store import TemarioStore
from .models import Chunk, SearchResult
from .embedder import MistralEmbedder

logger = logging.getLogger(__name__)


@dataclass
class SearchConfig:
    """Configuration for search."""

    default_limit: int = 5
    similarity_threshold: float = 0.7
    semantic_weight: float = 0.8
    keyword_weight: float = 0.2


class SemanticSearcher:
    """
    Semantic search over temario chunks.

    Uses vector similarity (cosine) for semantic search.
    Supports optional hybrid search with keyword matching.
    """

    def __init__(
        self,
        store: TemarioStore,
        embedder: MistralEmbedder,
        config: Optional[SearchConfig] = None,
    ):
        """
        Initialize the searcher.

        Args:
            store: TemarioStore instance
            embedder: MistralEmbedder instance
            config: Search configuration
        """
        self.store = store
        self.embedder = embedder
        self.config = config or SearchConfig()

    def search(
        self,
        query: str,
        limit: Optional[int] = None,
        tema: Optional[int] = None,
        threshold: Optional[float] = None,
    ) -> List[SearchResult]:
        """
        Perform semantic search over temario chunks.

        Args:
            query: Search query
            limit: Maximum number of results (default from config)
            tema: Filter by tema number
            threshold: Minimum similarity score (default from config)

        Returns:
            List of SearchResult objects sorted by relevance
        """
        limit = limit or self.config.default_limit
        threshold = threshold or self.config.similarity_threshold

        # Get query embedding
        logger.debug(f"Searching for: {query}")
        query_embedding = self.embedder.embed(query)

        # Get all embeddings from store
        all_embeddings = self.store.get_all_embeddings()

        if not all_embeddings:
            logger.warning("No embeddings found in store")
            return []

        # Calculate similarities
        similarities: List[Tuple[int, float]] = []
        for chunk_id, embedding in all_embeddings:
            similarity = self._cosine_similarity(query_embedding, embedding)
            if similarity >= threshold:
                similarities.append((chunk_id, similarity))

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Take top results
        top_results = similarities[:limit * 2]  # Get extra for tema filtering

        # Get chunks
        chunk_ids = [cid for cid, _ in top_results]
        chunks = self.store.get_chunks_by_ids(chunk_ids)

        # Build results
        chunk_map = {c.id: c for c in chunks}
        results = []

        for chunk_id, score in top_results:
            chunk = chunk_map.get(chunk_id)
            if chunk is None:
                continue

            # Filter by tema if specified
            if tema is not None and chunk.tema != tema:
                continue

            results.append(SearchResult(
                chunk=chunk,
                score=score,
                search_type="semantic",
            ))

            if len(results) >= limit:
                break

        logger.info(f"Found {len(results)} results for query")
        return results

    def hybrid_search(
        self,
        query: str,
        limit: Optional[int] = None,
        tema: Optional[int] = None,
    ) -> List[SearchResult]:
        """
        Perform hybrid search combining semantic and keyword matching.

        Args:
            query: Search query
            limit: Maximum number of results
            tema: Filter by tema number

        Returns:
            List of SearchResult objects sorted by combined score
        """
        limit = limit or self.config.default_limit

        # Get semantic results
        semantic_results = self.search(
            query,
            limit=limit * 2,
            tema=tema,
            threshold=0.3,  # Lower threshold for hybrid
        )

        # Calculate keyword scores
        query_terms = set(query.lower().split())

        scored_results = []
        for result in semantic_results:
            # Semantic score
            semantic_score = result.score * self.config.semantic_weight

            # Keyword score (Jaccard similarity)
            content_terms = set(result.chunk.content.lower().split())
            if query_terms and content_terms:
                intersection = len(query_terms & content_terms)
                union = len(query_terms | content_terms)
                keyword_score = (intersection / union) * self.config.keyword_weight
            else:
                keyword_score = 0.0

            # Combined score
            combined_score = semantic_score + keyword_score

            scored_results.append(SearchResult(
                chunk=result.chunk,
                score=combined_score,
                search_type="hybrid",
            ))

        # Sort by combined score
        scored_results.sort(key=lambda x: x.score, reverse=True)

        return scored_results[:limit]

    def ask(
        self,
        question: str,
        context_limit: int = 5,
        tema: Optional[int] = None,
    ) -> Tuple[str, List[SearchResult]]:
        """
        Answer a question using RAG.

        Retrieves relevant chunks and uses them as context for answering.

        Args:
            question: Question to answer
            context_limit: Number of context chunks to use
            tema: Filter by tema number

        Returns:
            Tuple of (answer, context_chunks)
        """
        # Get relevant chunks
        results = self.search(
            question,
            limit=context_limit,
            tema=tema,
        )

        # Return context for LLM to generate answer
        # (The actual LLM call is handled by the CLI or API layer)
        return "", results

    def _cosine_similarity(
        self,
        vec1: List[float],
        vec2: List[float],
    ) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Cosine similarity score (0 to 1)
        """
        if len(vec1) != len(vec2):
            raise ValueError("Vectors must have same dimension")

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def find_similar_chunks(
        self,
        chunk_id: int,
        limit: int = 5,
    ) -> List[SearchResult]:
        """
        Find chunks similar to a given chunk.

        Args:
            chunk_id: ID of the reference chunk
            limit: Maximum number of results

        Returns:
            List of similar chunks with similarity scores
        """
        chunk = self.store.get_chunk(chunk_id)
        if not chunk or not chunk.embedding:
            logger.warning(f"Chunk {chunk_id} not found or has no embedding")
            return []

        # Get all embeddings
        all_embeddings = self.store.get_all_embeddings()

        # Calculate similarities
        similarities: List[Tuple[int, float]] = []
        for other_id, embedding in all_embeddings:
            if other_id == chunk_id:
                continue
            similarity = self._cosine_similarity(chunk.embedding, embedding)
            similarities.append((other_id, similarity))

        # Sort and get top results
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_ids = [cid for cid, _ in similarities[:limit]]

        # Get chunks
        chunks = self.store.get_chunks_by_ids(top_ids)
        chunk_map = {c.id: c for c in chunks}

        results = []
        for other_id, score in similarities[:limit]:
            if other_id in chunk_map:
                results.append(SearchResult(
                    chunk=chunk_map[other_id],
                    score=score,
                    search_type="similarity",
                ))

        return results
