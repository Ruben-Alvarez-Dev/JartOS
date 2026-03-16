"""
Tests for DocumentParser.
"""

import pytest
import tempfile
from pathlib import Path

from TIER_09_KNOWLEDGE.temario.parser import DocumentParser, ParsedDocument, ParsedPage


class TestDocumentParser:
    """Tests for DocumentParser class."""

    def test_parser_initialization(self):
        """Test parser initializes correctly."""
        parser = DocumentParser()
        assert parser.extract_tables is True
        assert parser.extract_images is False

    def test_parser_custom_config(self):
        """Test parser with custom configuration."""
        parser = DocumentParser(
            extract_tables=False,
            extract_images=True,
        )
        assert parser.extract_tables is False
        assert parser.extract_images is True

    def test_parse_nonexistent_file(self, parser):
        """Test parsing a non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            parser.parse("/nonexistent/file.pdf")

    def test_parse_unsupported_file(self, parser):
        """Test parsing unsupported file type raises error."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"test content")
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Unsupported file type"):
                parser.parse(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_extract_metadata_tema(self, parser):
        """Test tema extraction from text."""
        doc = ParsedDocument(
            filename="test.pdf",
            file_type="pdf",
            pages=[
                ParsedPage(page_number=1, text="TEMA 5: Procedimiento Administrativo"),
            ],
        )
        parser._extract_metadata(doc)
        assert doc.tema == 5

    def test_extract_metadata_titulo(self, parser):
        """Test title extraction from text."""
        doc = ParsedDocument(
            filename="test.pdf",
            file_type="pdf",
            pages=[
                ParsedPage(
                    page_number=1,
                    text="TITULO: El Procedimiento Administrativo Comun"
                ),
            ],
        )
        parser._extract_metadata(doc)
        assert "Procedimiento Administrativo" in doc.title

    def test_extract_metadata_no_tema(self, parser):
        """Test no tema extraction when not present."""
        doc = ParsedDocument(
            filename="test.pdf",
            file_type="pdf",
            pages=[
                ParsedPage(page_number=1, text="Introduccion al Derecho"),
            ],
        )
        parser._extract_metadata(doc)
        assert doc.tema is None

    def test_table_to_text(self, parser):
        """Test table to text conversion."""
        table = [
            ["Header 1", "Header 2", "Header 3"],
            ["Value 1", "Value 2", "Value 3"],
            ["Value 4", "Value 5", "Value 6"],
        ]
        text = parser._table_to_text(table)

        assert "Header 1" in text
        assert "Value 1" in text
        assert "Value 6" in text

    def test_table_to_text_empty(self, parser):
        """Test table to text with empty table."""
        text = parser._table_to_text([])
        assert text == ""

    def test_extract_text_by_page(self, parser):
        """Test extracting text by page."""
        # This would require an actual PDF file, so we test the method exists
        assert hasattr(parser, 'extract_text_by_page')


class TestParsedDocument:
    """Tests for ParsedDocument dataclass."""

    def test_parsed_document_creation(self):
        """Test creating a ParsedDocument."""
        doc = ParsedDocument(
            filename="test.pdf",
            file_type="pdf",
            total_pages=5,
            full_text="Sample text",
        )

        assert doc.filename == "test.pdf"
        assert doc.file_type == "pdf"
        assert doc.total_pages == 5
        assert doc.tema is None
        assert doc.title is None

    def test_parsed_document_with_metadata(self):
        """Test ParsedDocument with metadata."""
        doc = ParsedDocument(
            filename="test.pdf",
            file_type="pdf",
            tema=3,
            title="Tema 3: Contratos",
            metadata={"has_tema": True},
        )

        assert doc.tema == 3
        assert doc.title == "Tema 3: Contratos"
        assert doc.metadata["has_tema"] is True


class TestParsedPage:
    """Tests for ParsedPage dataclass."""

    def test_parsed_page_creation(self):
        """Test creating a ParsedPage."""
        page = ParsedPage(
            page_number=1,
            text="Sample page content",
        )

        assert page.page_number == 1
        assert page.text == "Sample page content"
        assert page.tables == []

    def test_parsed_page_with_tables(self):
        """Test ParsedPage with tables."""
        table = [["A", "B"], ["1", "2"]]
        page = ParsedPage(
            page_number=1,
            text="Content",
            tables=[table],
        )

        assert len(page.tables) == 1
        assert page.tables[0] == table
