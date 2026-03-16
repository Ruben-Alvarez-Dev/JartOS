"""
Tests Routes

Test history and results viewing.
"""

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from pathlib import Path
from typing import Optional

from TIER_10_USER_APPS.tests.store import TestStore

router = APIRouter()

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


def get_store():
    """Get test store instance."""
    return TestStore(db_path=str(DATA_DIR / "tests.db"))


@router.get("/tests", response_class=HTMLResponse)
async def tests_view(request: Request):
    """Render tests overview page."""
    templates = request.app.state.templates
    store = get_store()

    tests = store.list_tests(limit=50)
    results = store.list_results(limit=20)

    # Calculate average score
    avg_score = 0
    if results:
        avg_score = sum(r.score_percentage for r in results) / len(results)

    # Count passed tests
    passed = sum(1 for r in results if r.passed)

    # Convert results to dict for JSON serialization in template
    results_json = [r.to_dict() for r in results]

    return templates.TemplateResponse(
        "tests.html",
        {
            "request": request,
            "tests": tests,
            "results": results,
            "results_json": results_json,
            "stats": {
                "total_tests": len(tests),
                "total_results": len(results),
                "average_score": round(avg_score, 1),
                "passed": passed,
            },
        },
    )


@router.get("/tests/{test_id}", response_class=HTMLResponse)
async def test_detail_view(request: Request, test_id: str):
    """Render test detail page."""
    templates = request.app.state.templates
    store = get_store()

    test = store.get_test(test_id)
    if not test:
        return HTMLResponse(content="Test not found", status_code=404)

    sessions = store.list_sessions(test_id=test_id, limit=10)
    results = store.list_results(test_id=test_id, limit=10)

    return templates.TemplateResponse(
        "test_detail.html",
        {
            "request": request,
            "test": test,
            "sessions": sessions,
            "results": results,
        },
    )


@router.get("/tests/result/{session_id}", response_class=HTMLResponse)
async def result_detail_view(request: Request, session_id: str):
    """Render result detail page."""
    templates = request.app.state.templates
    store = get_store()

    result = store.get_result(session_id)
    if not result:
        return HTMLResponse(content="Result not found", status_code=404)

    session = store.get_session(session_id)
    test = store.get_test(result.test_id) if result.test_id else None

    return templates.TemplateResponse(
        "result_detail.html",
        {
            "request": request,
            "result": result,
            "session": session,
            "test": test,
        },
    )


# API Routes

@router.get("/api/tests")
async def list_tests(limit: int = Query(50)):
    """List all tests."""
    store = get_store()
    tests = store.list_tests(limit=limit)
    return {"tests": [t.to_dict() for t in tests]}


@router.get("/api/tests/{test_id}")
async def get_test(test_id: str):
    """Get a test by ID."""
    store = get_store()
    test = store.get_test(test_id)
    if not test:
        return {"error": "Test not found"}
    return test.to_dict()


@router.get("/api/tests/results")
async def list_results(test_id: Optional[str] = None, limit: int = Query(50)):
    """List test results."""
    store = get_store()
    results = store.list_results(test_id=test_id, limit=limit)
    return {"results": [r.to_dict() for r in results]}


@router.get("/api/tests/stats")
async def get_test_stats():
    """Get test statistics."""
    store = get_store()
    results = store.list_results(limit=100)

    if not results:
        return {
            "total_tests": store.get_test_count(),
            "total_sessions": store.get_session_count(),
            "average_score": 0,
            "pass_rate": 0,
        }

    avg_score = sum(r.score_percentage for r in results) / len(results)
    passed = sum(1 for r in results if r.passed)
    pass_rate = (passed / len(results)) * 100 if results else 0

    return {
        "total_tests": store.get_test_count(),
        "total_sessions": store.get_session_count(),
        "average_score": round(avg_score, 1),
        "pass_rate": round(pass_rate, 1),
    }
