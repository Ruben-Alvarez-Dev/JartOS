"""
Temario Routes

Temario search and document browsing.
"""

from fastapi import APIRouter, Request, Query, Form
from fastapi.responses import HTMLResponse
from pathlib import Path
from typing import Optional

from TIER_09_KNOWLEDGE.temario.store import TemarioStore
from TIER_09_KNOWLEDGE.temario.searcher import SemanticSearcher as Searcher

router = APIRouter()

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


def get_store():
    """Get temario store instance."""
    return TemarioStore(db_path=str(DATA_DIR / "temario.db"))


@router.get("/temario", response_class=HTMLResponse)
async def temario_view(request: Request):
    """Render temario overview page."""
    templates = request.app.state.templates
    store = get_store()

    documents = store.list_documents(limit=100)
    stats = store.get_stats()

    return templates.TemplateResponse(
        "temario.html",
        {
            "request": request,
            "documents": documents,
            "stats": stats,
        },
    )


@router.get("/temario/search", response_class=HTMLResponse)
async def search_view(
    request: Request,
    q: str = Query(""),
    tema: Optional[int] = Query(None),
):
    """Render search results page."""
    templates = request.app.state.templates
    store = get_store()

    results = []
    search_performed = False

    if q:
        search_performed = True
        try:
            searcher = Searcher(store=store)
            search_results = searcher.search(q, limit=20)
            results = [r.to_dict() for r in search_results]
        except Exception as e:
            results = []
            print(f"Search error: {e}")

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "query": q,
            "results": results,
            "search_performed": search_performed,
        },
    )


@router.get("/temario/document/{doc_id}", response_class=HTMLResponse)
async def document_view(request: Request, doc_id: int):
    """Render document detail page."""
    templates = request.app.state.templates
    store = get_store()

    document = store.get_document(doc_id)
    if not document:
        return HTMLResponse(content="Document not found", status_code=404)

    chunks = store.get_chunks_by_document(doc_id)

    return templates.TemplateResponse(
        "document.html",
        {
            "request": request,
            "document": document,
            "chunks": chunks,
        },
    )


@router.get("/temario/tema/{tema_num}", response_class=HTMLResponse)
async def tema_view(request: Request, tema_num: int):
    """Render tema view page."""
    templates = request.app.state.templates
    store = get_store()

    chunks = store.get_chunks_by_tema(tema_num)

    return templates.TemplateResponse(
        "tema.html",
        {
            "request": request,
            "tema_num": tema_num,
            "chunks": chunks,
            "chunk_count": len(chunks),
        },
    )


# API Routes

@router.get("/api/temario/documents")
async def list_documents(limit: int = Query(100)):
    """List all documents."""
    store = get_store()
    documents = store.list_documents(limit=limit)
    return {"documents": [d.to_dict() for d in documents]}


@router.get("/api/temario/stats")
async def get_temario_stats():
    """Get temario statistics."""
    store = get_store()
    return store.get_stats()


@router.get("/api/temario/search")
async def search_temario(
    q: str = Query(..., min_length=1),
    limit: int = Query(20),
):
    """Search temario content."""
    store = get_store()

    try:
        searcher = Searcher(store=store)
        results = searcher.search(q, limit=limit)
        return {"results": [r.to_dict() for r in results]}
    except Exception as e:
        return {"error": str(e), "results": []}


@router.get("/api/temario/chunks/{chunk_id}")
async def get_chunk(chunk_id: int):
    """Get a chunk by ID."""
    store = get_store()
    chunk = store.get_chunk(chunk_id)
    if not chunk:
        return {"error": "Chunk not found"}
    return chunk.to_dict()
