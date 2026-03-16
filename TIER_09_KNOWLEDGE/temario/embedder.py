"""
MistralEmbedder - Generate embeddings using Mistral API.

Provides batch embedding generation with rate limiting and error handling.
"""

import os
import time
import logging
from typing import List, Optional
import httpx

logger = logging.getLogger(__name__)


class MistralEmbedder:
    """
    Generate embeddings using Mistral's API.

    Uses mistral-embed model with 1024 dimensions.
    """

    API_URL = "https://api.mistral.ai/v1/embeddings"
    MODEL = "mistral-embed"
    DIMENSIONS = 1024

    def __init__(
        self,
        api_key: Optional[str] = None,
        batch_size: int = 50,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initialize the embedder.

        Args:
            api_key: Mistral API key (defaults to MISTRAL_API_KEY env var)
            batch_size: Number of texts to embed per API call
            max_retries: Maximum number of retries on failure
            retry_delay: Base delay between retries (exponential backoff)
        """
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Mistral API key required. Set MISTRAL_API_KEY environment "
                "variable or pass api_key parameter."
            )

        self.batch_size = batch_size
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def embed(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector (1024 dimensions)

        Raises:
            RuntimeError: If embedding fails after retries
        """
        embeddings = self.embed_batch([text])
        return embeddings[0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Processes in batches to respect API limits.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors

        Raises:
            RuntimeError: If embedding fails after retries
        """
        if not texts:
            return []

        all_embeddings = []

        # Process in batches
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            logger.debug(f"Embedding batch {i // self.batch_size + 1} "
                        f"({len(batch)} texts)")

            batch_embeddings = self._embed_batch_with_retry(batch)
            all_embeddings.extend(batch_embeddings)

            # Rate limiting - small delay between batches
            if i + self.batch_size < len(texts):
                time.sleep(0.1)

        logger.info(f"Generated {len(all_embeddings)} embeddings")
        return all_embeddings

    def _embed_batch_with_retry(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a batch with retry logic.

        Args:
            texts: Texts to embed

        Returns:
            List of embeddings

        Raises:
            RuntimeError: If all retries fail
        """
        last_error = None

        for attempt in range(self.max_retries):
            try:
                return self._call_api(texts)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    logger.warning(
                        f"Embedding failed (attempt {attempt + 1}): {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)

        raise RuntimeError(
            f"Failed to embed batch after {self.max_retries} attempts: {last_error}"
        )

    def _call_api(self, texts: List[str]) -> List[List[float]]:
        """
        Make the actual API call to Mistral.

        Args:
            texts: Texts to embed

        Returns:
            List of embeddings

        Raises:
            httpx.HTTPStatusError: On HTTP errors
            ValueError: On API errors
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.MODEL,
            "input": texts,
        }

        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                self.API_URL,
                headers=headers,
                json=payload,
            )

            if response.status_code != 200:
                error_detail = response.text
                raise httpx.HTTPStatusError(
                    f"API error {response.status_code}: {error_detail}",
                    request=response.request,
                    response=response,
                )

            data = response.json()

        # Extract embeddings from response
        if "data" not in data:
            raise ValueError(f"Unexpected API response: {data}")

        # Sort by index to maintain order
        embeddings_data = sorted(data["data"], key=lambda x: x["index"])
        embeddings = [item["embedding"] for item in embeddings_data]

        return embeddings

    @property
    def dimensions(self) -> int:
        """Return embedding dimensions."""
        return self.DIMENSIONS

    @property
    def model_name(self) -> str:
        """Return model name."""
        return self.MODEL
