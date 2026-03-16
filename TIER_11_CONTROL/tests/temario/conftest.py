"""
Shared fixtures for temario tests.
"""

import pytest
import tempfile
import os
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from TIER_09_KNOWLEDGE.temario.store import TemarioStore
from TIER_09_KNOWLEDGE.temario.chunker import TextChunker, ChunkConfig
from TIER_09_KNOWLEDGE.temario.parser import DocumentParser
from TIER_09_KNOWLEDGE.temario.models import Document, Chunk


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    yield db_path

    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def store(temp_db):
    """Create a TemarioStore instance with temp database."""
    return TemarioStore(db_path=temp_db)


@pytest.fixture
def sample_document():
    """Create a sample document for testing."""
    return Document(
        filename="test_tema1.pdf",
        filepath="/path/to/test_tema1.pdf",
        file_type="pdf",
        title="Tema 1: Introduccion al Derecho Administrativo",
        tema=1,
        total_pages=10,
        metadata={"has_tema": True, "has_title": True},
    )


@pytest.fixture
def sample_chunks(sample_document):
    """Create sample chunks for testing."""
    return [
        Chunk(
            document_id=1,
            content="El Derecho Administrativo es la rama del Derecho Publico que regula la organizacion y actividad de la Administracion Publica.",
            token_count=25,
            chunk_index=0,
            page_number=1,
            tema=1,
        ),
        Chunk(
            document_id=1,
            content="Los principios generales del Derecho Administrativo incluyen: legalidad, jerarquia, publicidad e impugnabilidad.",
            token_count=20,
            chunk_index=1,
            page_number=2,
            tema=1,
        ),
        Chunk(
            document_id=1,
            content="Las fuentes del Derecho Administrativo son: la Constitucion, las leyes, los reglamentos y la jurisprudencia.",
            token_count=22,
            chunk_index=2,
            page_number=3,
            tema=1,
        ),
    ]


@pytest.fixture
def sample_text():
    """Sample text for chunking tests."""
    return """
    Tema 1: Introduccion al Derecho Administrativo

    El Derecho Administrativo es una rama fundamental del Derecho Publico que se encarga
    de regular la organizacion, funcionamiento y atribuciones de la Administracion Publica.
    Esta disciplina juridica ha evolucionado significativamente desde sus origenes hasta
    convertirse en un pilar esencial del Estado de Derecho.

    Los principios fundamentales que rigen el Derecho Administrativo son de suma importancia.
    El principio de legalidad establece que la Administracion solo puede actuar cuando una
    norma juridica lo autorice. El principio de jerarquia normativa organiza las fuentes
    del derecho en un orden de prelacion. El principio de publicidad exige que los actos
    administrativos sean conocidos por los ciudadanos.

    Las fuentes del Derecho Administrativo comprenden diversos ordenamientos juridicos.
    En primer lugar, la Constitucion Politica establece el marco fundamental. Las leyes
    organicas y ordinarias desarrollan los preceptos constitucionales. Los reglamentos
    complementan y desarrollan las normas legales. La jurisprudencia interpreta y aplica
    estas normas en casos concretos.

    La potestad reglamentaria es una de las funciones mas importantes de la Administracion.
    Permite dictar normas de caracter general y abstracto que regulan situaciones especificas.
    Los reglamentos pueden ser ejecutivos, independientes o de necesidad.
    """


@pytest.fixture
def chunker():
    """Create a TextChunker with default config."""
    return TextChunker(config=ChunkConfig(
        target_tokens=100,
        max_tokens=150,
        min_tokens=30,
        overlap_sentences=1,
    ))


@pytest.fixture
def parser():
    """Create a DocumentParser instance."""
    return DocumentParser(
        extract_tables=True,
        extract_images=False,
    )
