"""
Ingestion pipeline for temario documents.

Orchestrates the full pipeline: parse -> chunk -> embed -> store.
"""

import os
import time
import logging
from pathlib import Path
from typing import Optional, List, Callable
from datetime import datetime

import yaml

from .store import TemarioStore
from .parser import DocumentParser, ParsedDocument
from .chunker import TextChunker, ChunkConfig
from .embedder import MistralEmbedder
from .searcher import SemanticSearcher
from .models import Document, Chunk, IngestionResult

logger = logging.getLogger(__name__)


class TemarioIngestor:
    """
    Full ingestion pipeline for temario documents.

    Handles: parse -> chunk -> embed -> store
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        db_path: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Initialize the ingestor.

        Args:
            config_path: Path to config.yaml
            db_path: Override database path
            api_key: Override Mistral API key
        """
        # Load configuration
        self.config = self._load_config(config_path)

        # Override paths if provided
        if db_path:
            self.config["database"]["path"] = db_path

        # Initialize components
        self.store = TemarioStore(
            db_path=self.config["database"]["path"]
        )

        self.parser = DocumentParser(
            extract_tables=self.config.get("parser", {}).get("pdf", {}).get("extract_tables", True),
            extract_images=self.config.get("parser", {}).get("pdf", {}).get("extract_images", False),
        )

        chunk_config = ChunkConfig(
            target_tokens=self.config.get("chunking", {}).get("target_tokens", 500),
            max_tokens=self.config.get("chunking", {}).get("max_tokens", 700),
            min_tokens=self.config.get("chunking", {}).get("min_tokens", 100),
            overlap_sentences=self.config.get("chunking", {}).get("overlap_sentences", 2),
        )
        self.chunker = TextChunker(config=chunk_config)

        self.embedder = MistralEmbedder(
            api_key=api_key or os.getenv(
                self.config.get("embeddings", {}).get("api_key_env", "MISTRAL_API_KEY")
            ),
            batch_size=self.config.get("embeddings", {}).get("batch_size", 50),
        )

        self.searcher = SemanticSearcher(
            store=self.store,
            embedder=self.embedder,
        )

        # Setup logging
        self._setup_logging()

    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration from YAML file."""
        default_config = {
            "database": {"path": "data/temario.db"},
            "embeddings": {
                "provider": "mistral",
                "model": "mistral-embed",
                "dimensions": 1024,
                "batch_size": 50,
                "api_key_env": "MISTRAL_API_KEY",
            },
            "chunking": {
                "target_tokens": 500,
                "max_tokens": 700,
                "min_tokens": 100,
                "overlap_sentences": 2,
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "paths": {
                "documents": "documents/temario",
                "cache": "cache/temario",
                "logs": "logs",
            },
        }

        if config_path and Path(config_path).exists():
            with open(config_path, "r") as f:
                user_config = yaml.safe_load(f)
                # Merge configs
                self._deep_merge(default_config, user_config)

        return default_config

    def _deep_merge(self, base: dict, override: dict) -> None:
        """Deep merge override into base dict."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        log_config = self.config.get("logging", {})
        level = getattr(logging, log_config.get("level", "INFO"))
        log_format = log_config.get(
            "format",
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Configure root logger for this module
        logging.basicConfig(level=level, format=log_format)

    def ingest(
        self,
        filepath: str,
        skip_embeddings: bool = False,
        progress_callback: Optional[Callable[[str, int, int], None]] = None,
    ) -> IngestionResult:
        """
        Ingest a document into the temario system.

        Full pipeline: parse -> chunk -> embed -> store

        Args:
            filepath: Path to document (PDF or DOCX)
            skip_embeddings: Skip embedding generation (for testing)
            progress_callback: Callback for progress updates (stage, current, total)

        Returns:
            IngestionResult with document and stats
        """
        start_time = time.time()
        errors = []

        try:
            # Check if document already exists
            filename = Path(filepath).name
            existing = self.store.get_document_by_filename(filename)
            if existing:
                logger.info(f"Document already exists: {filename} (id={existing.id})")
                # Delete existing to re-ingest
                self.store.delete_document(existing.id)

            # Step 1: Parse document
            if progress_callback:
                progress_callback("parsing", 0, 4)

            logger.info(f"Parsing document: {filepath}")
            parsed = self.parser.parse(filepath)

            # Step 2: Create document record
            if progress_callback:
                progress_callback("document", 1, 4)

            document = Document(
                filename=filename,
                filepath=filepath,
                file_type=parsed.file_type,
                title=parsed.title,
                tema=parsed.tema,
                total_pages=parsed.total_pages,
                metadata=parsed.metadata,
            )
            document = self.store.create_document(document)

            # Step 3: Chunk text
            if progress_callback:
                progress_callback("chunking", 2, 4)

            logger.info("Chunking text...")
            chunks = self._create_chunks(document, parsed)

            # Store chunks
            chunks = self.store.create_chunks_batch(chunks)
            document.total_chunks = len(chunks)
            self.store.update_document(document)

            logger.info(f"Created {len(chunks)} chunks")

            # Step 4: Generate embeddings
            embeddings_created = 0
            if not skip_embeddings:
                if progress_callback:
                    progress_callback("embedding", 3, 4)

                logger.info("Generating embeddings...")
                embeddings_created = self._generate_embeddings(chunks)

            # Update progress
            if progress_callback:
                progress_callback("complete", 4, 4)

            duration = time.time() - start_time

            return IngestionResult(
                success=True,
                document=document,
                chunks_created=len(chunks),
                embeddings_created=embeddings_created,
                errors=errors,
                duration_seconds=duration,
            )

        except Exception as e:
            logger.error(f"Ingestion failed: {e}")
            errors.append(str(e))

            return IngestionResult(
                success=False,
                errors=errors,
                duration_seconds=time.time() - start_time,
            )

    def _create_chunks(
        self,
        document: Document,
        parsed: ParsedDocument,
    ) -> List[Chunk]:
        """
        Create chunks from parsed document.

        Args:
            document: Document record
            parsed: Parsed document

        Returns:
            List of Chunk objects (without embeddings)
        """
        chunks = []

        # Get text segments from parser
        segments = self.parser.get_text_for_chunking(parsed)

        chunk_index = 0
        for segment in segments:
            text = segment.get("text", "")
            if not text.strip():
                continue

            # Chunk the segment
            raw_chunks = self.chunker.chunk_text(
                text,
                page_number=segment.get("page_number"),
                metadata=segment.get("metadata", {}),
            )

            for raw in raw_chunks:
                chunk = Chunk(
                    document_id=document.id,
                    content=raw["content"],
                    token_count=raw["token_count"],
                    chunk_index=chunk_index,
                    page_number=raw.get("page_number"),
                    tema=document.tema,
                    titulo=document.title,
                    metadata=raw.get("metadata", {}),
                )

                # Extract apartado if present in content
                if segment.get("is_table"):
                    chunk.metadata["is_table"] = True

                chunks.append(chunk)
                chunk_index += 1

        return chunks

    def _generate_embeddings(self, chunks: List[Chunk]) -> int:
        """
        Generate embeddings for chunks.

        Args:
            chunks: List of chunks (must have ids)

        Returns:
            Number of embeddings created
        """
        if not chunks:
            return 0

        # Get texts
        texts = [chunk.content for chunk in chunks]
        chunk_ids = [chunk.id for chunk in chunks]

        # Generate embeddings in batches
        embeddings = self.embedder.embed_batch(texts)

        # Store embeddings
        updated = self.store.update_chunks_embeddings_batch(chunk_ids, embeddings)

        return updated

    def ingest_directory(
        self,
        directory: str,
        skip_embeddings: bool = False,
        progress_callback: Optional[Callable[[str, str, int, int], None]] = None,
    ) -> List[IngestionResult]:
        """
        Ingest all documents in a directory.

        Args:
            directory: Path to directory
            skip_embeddings: Skip embedding generation
            progress_callback: Callback (filename, stage, current, total)

        Returns:
            List of IngestionResults
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        # Find all PDF and DOCX files
        files = list(dir_path.glob("*.pdf")) + list(dir_path.glob("*.docx"))
        total = len(files)

        logger.info(f"Found {total} documents to ingest")

        results = []
        for i, filepath in enumerate(files):
            if progress_callback:
                progress_callback(filepath.name, "starting", i, total)

            result = self.ingest(
                str(filepath),
                skip_embeddings=skip_embeddings,
            )
            results.append(result)

            if progress_callback:
                status = "success" if result.success else "failed"
                progress_callback(filepath.name, status, i + 1, total)

        successful = sum(1 for r in results if r.success)
        logger.info(f"Ingested {successful}/{total} documents successfully")

        return results

    def get_stats(self) -> dict:
        """Get ingestion statistics."""
        return self.store.get_stats()
