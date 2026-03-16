"""
Dashboard Routes

Main dashboard view with statistics and overview.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pathlib import Path

from temario.store import TemarioStore
from flashcards.store import FlashcardStore
from tests.store import TestStore

router = APIRouter()

# Database paths
DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


def get_stores():
    """Get store instances."""
    return {
        "temario": TemarioStore(db_path=str(DATA_DIR / "temario.db")),
        "flashcards": FlashcardStore(db_path=str(DATA_DIR / "flashcards.db")),
        "tests": TestStore(db_path=str(DATA_DIR / "tests.db")),
    }


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_view(request: Request):
    """Render main dashboard page."""
    templates = request.app.state.templates
    stores = get_stores()

    # Get statistics
    temario_stats = stores["temario"].get_stats()
    flashcard_stats = stores["flashcards"].get_all_stats()
    test_count = stores["tests"].get_test_count()
    session_count = stores["tests"].get_session_count()

    # Get recent tests
    recent_tests = stores["tests"].list_tests(limit=5)
    recent_results = stores["tests"].list_results(limit=5)

    # Get decks overview
    decks = stores["flashcards"].list_decks(limit=10)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "temario_stats": temario_stats,
            "flashcard_stats": flashcard_stats,
            "test_count": test_count,
            "session_count": session_count,
            "recent_tests": recent_tests,
            "recent_results": recent_results,
            "decks": decks,
        },
    )


@router.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics as JSON."""
    stores = get_stores()

    return {
        "temario": stores["temario"].get_stats(),
        "flashcards": stores["flashcards"].get_all_stats(),
        "tests": {
            "total_tests": stores["tests"].get_test_count(),
            "total_sessions": stores["tests"].get_session_count(),
        },
    }
