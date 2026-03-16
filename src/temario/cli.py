#!/usr/bin/env python3
"""
Temario CLI - Command-line interface for temario ingestion system.

Commands:
    ingest <file>     - Ingest a PDF/DOCX document
    ingest-dir <dir>  - Ingest all documents in a directory
    search <query>    - Search temario chunks
    ask <question>    - Ask a question (returns context for LLM)
    stats             - Show database statistics
    list              - List ingested documents
"""

import argparse
import logging
import os
import sys
from pathlib import Path

import yaml

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from temario.ingest import TemarioIngestor
from temario.store import TemarioStore
from temario.searcher import SemanticSearcher
from temario.embedder import MistralEmbedder


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def load_config(config_path: str = None) -> dict:
    """Load configuration."""
    if config_path is None:
        config_path = os.getenv(
            "TEMARIO_CONFIG",
            "configs/temario.yaml"
        )

    if Path(config_path).exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}


def cmd_ingest(args):
    """Ingest a document."""
    setup_logging(args.verbose)

    ingestor = TemarioIngestor(
        config_path=args.config,
        db_path=args.db,
    )

    def progress(stage, current, total):
        stages = ["parsing", "document", "chunking", "embedding", "complete"]
        if stage in stages:
            print(f"[{current}/{total}] {stage.capitalize()}...")

    result = ingestor.ingest(
        args.file,
        skip_embeddings=args.skip_embeddings,
        progress_callback=progress,
    )

    if result.success:
        print(f"\nSuccess!")
        print(f"  Document: {result.document.filename}")
        print(f"  Chunks created: {result.chunks_created}")
        print(f"  Embeddings: {result.embeddings_created}")
        print(f"  Duration: {result.duration_seconds:.2f}s")
    else:
        print(f"\nFailed: {', '.join(result.errors)}")
        sys.exit(1)


def cmd_ingest_dir(args):
    """Ingest all documents in a directory."""
    setup_logging(args.verbose)

    ingestor = TemarioIngestor(
        config_path=args.config,
        db_path=args.db,
    )

    def progress(filename, stage, current, total):
        print(f"[{current}/{total}] {filename}: {stage}")

    results = ingestor.ingest_directory(
        args.directory,
        skip_embeddings=args.skip_embeddings,
        progress_callback=progress,
    )

    successful = sum(1 for r in results if r.success)
    print(f"\nIngested {successful}/{len(results)} documents successfully")


def cmd_search(args):
    """Search temario chunks."""
    setup_logging(args.verbose)

    config = load_config(args.config)
    db_path = args.db or config.get("database", {}).get("path", "data/temario.db")

    store = TemarioStore(db_path=db_path)
    embedder = MistralEmbedder()
    searcher = SemanticSearcher(store=store, embedder=embedder)

    results = searcher.search(
        query=args.query,
        limit=args.limit,
        tema=args.tema,
        threshold=args.threshold,
    )

    if not results:
        print("No results found.")
        return

    print(f"\nFound {len(results)} results:\n")

    for i, result in enumerate(results, 1):
        chunk = result.chunk
        print(f"--- Result {i} (score: {result.score:.3f}) ---")
        print(f"Tema: {chunk.tema or 'N/A'} | Page: {chunk.page_number or 'N/A'}")
        print(f"Content: {chunk.content[:200]}...")
        print()


def cmd_ask(args):
    """Ask a question (returns context for LLM)."""
    setup_logging(args.verbose)

    config = load_config(args.config)
    db_path = args.db or config.get("database", {}).get("path", "data/temario.db")

    store = TemarioStore(db_path=db_path)
    embedder = MistralEmbedder()
    searcher = SemanticSearcher(store=store, embedder=embedder)

    _, context = searcher.ask(
        question=args.question,
        context_limit=args.context,
        tema=args.tema,
    )

    if not context:
        print("No relevant context found.")
        return

    print(f"\nQuestion: {args.question}")
    print(f"\nContext chunks ({len(context)}):\n")

    for i, result in enumerate(context, 1):
        chunk = result.chunk
        print(f"--- Context {i} (relevance: {result.score:.3f}) ---")
        print(f"Source: Tema {chunk.tema or 'N/A'}, Page {chunk.page_number or 'N/A'}")
        print(chunk.content)
        print()


def cmd_stats(args):
    """Show database statistics."""
    setup_logging(args.verbose)

    config = load_config(args.config)
    db_path = args.db or config.get("database", {}).get("path", "data/temario.db")

    store = TemarioStore(db_path=db_path)
    stats = store.get_stats()

    print("\nTemario Database Statistics:")
    print(f"  Documents: {stats['documents']}")
    print(f"  Chunks: {stats['chunks']}")
    print(f"  Embeddings: {stats['embeddings']}")
    print(f"  Total tokens: {stats['total_tokens']:,}")


def cmd_list(args):
    """List ingested documents."""
    setup_logging(args.verbose)

    config = load_config(args.config)
    db_path = args.db or config.get("database", {}).get("path", "data/temario.db")

    store = TemarioStore(db_path=db_path)
    documents = store.list_documents(limit=args.limit, offset=args.offset)

    if not documents:
        print("No documents found.")
        return

    print(f"\nDocuments ({len(documents)}):\n")
    for doc in documents:
        print(f"  [{doc.id}] {doc.filename}")
        print(f"      Type: {doc.file_type} | Tema: {doc.tema or 'N/A'}")
        print(f"      Pages: {doc.total_pages} | Chunks: {doc.total_chunks}")
        print(f"      Ingested: {doc.created_at}")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Temario Ingestion System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s ingest documento.pdf
    %(prog)s search "contratos administrativos"
    %(prog)s ask "¿Qué es un contrato menor?"
    %(prog)s stats
        """,
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "-c", "--config",
        default=None,
        help="Path to config file (default: configs/temario.yaml)",
    )
    parser.add_argument(
        "--db",
        default=None,
        help="Override database path",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest a document")
    ingest_parser.add_argument("file", help="Path to PDF or DOCX file")
    ingest_parser.add_argument(
        "--skip-embeddings",
        action="store_true",
        help="Skip embedding generation",
    )
    ingest_parser.set_defaults(func=cmd_ingest)

    # ingest-dir command
    ingest_dir_parser = subparsers.add_parser(
        "ingest-dir", help="Ingest all documents in a directory"
    )
    ingest_dir_parser.add_argument("directory", help="Path to directory")
    ingest_dir_parser.add_argument(
        "--skip-embeddings",
        action="store_true",
        help="Skip embedding generation",
    )
    ingest_dir_parser.set_defaults(func=cmd_ingest_dir)

    # search command
    search_parser = subparsers.add_parser("search", help="Search temario chunks")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("-l", "--limit", type=int, default=5, help="Max results")
    search_parser.add_argument("-t", "--tema", type=int, help="Filter by tema")
    search_parser.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="Minimum similarity threshold",
    )
    search_parser.set_defaults(func=cmd_search)

    # ask command
    ask_parser = subparsers.add_parser("ask", help="Ask a question")
    ask_parser.add_argument("question", help="Question to ask")
    ask_parser.add_argument("-c", "--context", type=int, default=5, help="Context chunks")
    ask_parser.add_argument("-t", "--tema", type=int, help="Filter by tema")
    ask_parser.set_defaults(func=cmd_ask)

    # stats command
    stats_parser = subparsers.add_parser("stats", help="Show database statistics")
    stats_parser.set_defaults(func=cmd_stats)

    # list command
    list_parser = subparsers.add_parser("list", help="List ingested documents")
    list_parser.add_argument("-l", "--limit", type=int, default=100)
    list_parser.add_argument("-o", "--offset", type=int, default=0)
    list_parser.set_defaults(func=cmd_list)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
