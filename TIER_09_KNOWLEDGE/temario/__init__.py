"""
Temario Ingestion System

A system for ingesting, chunking, embedding, and searching PDF/DOCX documents
for oposiciones exam preparation.
"""

__version__ = "0.1.0"
__author__ = "Gentleman Programming"

from .store import TemarioStore
from .parser import DocumentParser
from .chunker import TextChunker
from .embedder import MistralEmbedder
from .searcher import SemanticSearcher

__all__ = [
    "TemarioStore",
    "DocumentParser",
    "TextChunker",
    "MistralEmbedder",
    "SemanticSearcher",
]
