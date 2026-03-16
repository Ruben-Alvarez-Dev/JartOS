#!/usr/bin/env python3
"""
Quick test script to verify the temario ingestion system is working.

Run with: python3 scripts/temario_demo.py
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from temario.store import TemarioStore
from temario.parser import DocumentParser
from temario.chunker import TextChunker, ChunkConfig
from temario.models import Document, Chunk


def test_store():
    """Test basic store operations."""
    print("\n=== Testing TemarioStore ===")

    store = TemarioStore(db_path="data/temario/test.db")

    # Create document
    doc = Document(
        filename="test_tema1.pdf",
        filepath="/documents/test_tema1.pdf",
        file_type="pdf",
        title="Tema 1: Introduccion al Derecho Administrativo",
        tema=1,
        total_pages=10,
    )
    doc = store.create_document(doc)
    print(f"Created document: {doc.filename} (id={doc.id})")

    # Create chunks
    chunks = [
        Chunk(
            document_id=doc.id,
            content="El Derecho Administrativo es la rama del Derecho Publico que regula la Administracion Publica.",
            token_count=25,
            chunk_index=i,
            page_number=i+1,
            tema=1,
        )
        for i in range(5)
    ]
    chunks = store.create_chunks_batch(chunks)
    print(f"Created {len(chunks)} chunks")

    # Get stats
    stats = store.get_stats()
    print(f"Stats: {stats}")

    return True


def test_chunker():
    """Test text chunking."""
    print("\n=== Testing TextChunker ===")

    config = ChunkConfig(
        target_tokens=100,
        max_tokens=150,
        min_tokens=30,
    )
    chunker = TextChunker(config=config)

    sample_text = """
    El Derecho Administrativo es una rama fundamental del Derecho Publico.
    Se encarga de regular la organizacion y funcionamiento de la Administracion Publica.
    Los principios fundamentales incluyen: legalidad, jerarquia, publicidad e impugnabilidad.
    Las fuentes del Derecho Administrativo son: la Constitucion, las leyes, los reglamentos.
    La potestad reglamentaria permite a la Administracion dictar normas generales.
    """

    chunks = chunker.chunk_text(sample_text, page_number=1)
    print(f"Created {len(chunks)} chunks from sample text")

    for i, chunk in enumerate(chunks[:2]):
        print(f"\nChunk {i+1}:")
        print(f"  Tokens: {chunk['token_count']}")
        print(f"  Content: {chunk['content'][:100]}...")

    return True


def test_parser():
    """Test document parser."""
    print("\n=== Testing DocumentParser ===")

    parser = DocumentParser()

    # Test metadata extraction
    from temario.parser import ParsedDocument, ParsedPage

    doc = ParsedDocument(
        filename="test.pdf",
        file_type="pdf",
        pages=[
            ParsedPage(page_number=1, text="TEMA 5: Procedimiento Administrativo"),
        ],
    )
    parser._extract_metadata(doc)
    print(f"Extracted tema: {doc.tema}")
    print(f"Metadata: {doc.metadata}")

    return True


def main():
    """Run all tests."""
    print("=== Temario Ingestion System - Quick Test ===")

    results = []

    try:
        results.append(("Store", test_store()))
    except Exception as e:
        print(f"Store test failed: {e}")
        results.append(("Store", False))

    try:
        results.append(("Chunker", test_chunker()))
    except Exception as e:
        print(f"Chunker test failed: {e}")
        results.append(("Chunker", False))

    try:
        results.append(("Parser", test_parser()))
    except Exception as e:
        print(f"Parser test failed: {e}")
        results.append(("Parser", False))

    print("\n=== Results ===")
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status}")

    all_passed = all(r[1] for r in results)
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
