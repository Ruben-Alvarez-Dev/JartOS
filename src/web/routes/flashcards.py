"""
Flashcards Routes

Flashcard management and review interface.
"""

from fastapi import APIRouter, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from typing import Optional
from datetime import date

from flashcards.store import FlashcardStore
from flashcards.models import Deck, Flashcard

router = APIRouter()

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


def get_store():
    """Get flashcard store instance."""
    return FlashcardStore(db_path=str(DATA_DIR / "flashcards.db"))


@router.get("/flashcards", response_class=HTMLResponse)
async def flashcards_view(request: Request):
    """Render flashcards overview page."""
    templates = request.app.state.templates
    store = get_store()

    decks = store.list_decks(limit=100)
    stats = store.get_all_stats()

    # Get stats for each deck
    deck_stats = []
    for deck in decks:
        stats_obj = store.get_deck_stats(deck.id)
        if stats_obj:
            deck_stats.append(stats_obj.to_dict())

    return templates.TemplateResponse(
        "flashcards.html",
        {
            "request": request,
            "decks": decks,
            "stats": stats,
            "deck_stats": deck_stats,
        },
    )


@router.get("/flashcards/deck/{deck_id}", response_class=HTMLResponse)
async def deck_view(request: Request, deck_id: int):
    """Render deck detail page."""
    templates = request.app.state.templates
    store = get_store()

    deck = store.get_deck(deck_id)
    if not deck:
        return RedirectResponse(url="/flashcards", status_code=303)

    cards = store.get_flashcards_by_deck(deck_id, limit=200)
    stats = store.get_deck_stats(deck_id)

    # Get due and new cards count
    due_cards = store.get_due_cards(deck_id, limit=100)
    new_cards = store.get_new_cards(deck_id, limit=100)

    return templates.TemplateResponse(
        "deck.html",
        {
            "request": request,
            "deck": deck,
            "cards": cards,
            "stats": stats,
            "due_count": len(due_cards),
            "new_count": len(new_cards),
        },
    )


@router.get("/flashcards/review/{deck_id}", response_class=HTMLResponse)
async def review_view(request: Request, deck_id: int, mode: str = Query("due")):
    """Render review session page."""
    templates = request.app.state.templates
    store = get_store()

    deck = store.get_deck(deck_id)
    if not deck:
        return RedirectResponse(url="/flashcards", status_code=303)

    # Get cards to review
    if mode == "new":
        cards = store.get_new_cards(deck_id, limit=20)
    else:
        cards = store.get_due_cards(deck_id, limit=20)

    return templates.TemplateResponse(
        "review.html",
        {
            "request": request,
            "deck": deck,
            "cards": cards,
            "mode": mode,
        },
    )


@router.post("/flashcards/review/submit")
async def submit_review(
    card_id: int = Form(...),
    rating: int = Form(...),
):
    """Submit a flashcard review."""
    from flashcards.scheduler import SM2Scheduler

    store = get_store()
    scheduler = SM2Scheduler()

    card = store.get_flashcard(card_id)
    if not card:
        return {"success": False, "error": "Card not found"}

    # Calculate new scheduling
    old_interval = card.interval
    old_ease = card.ease_factor

    scheduler.schedule(card, rating)

    # Update card
    store.update_flashcard(card)

    # Log review
    from flashcards.models import ReviewLog
    log = ReviewLog(
        flashcard_id=card_id,
        rating=rating,
        interval_before=old_interval,
        interval_after=card.interval,
        ease_factor_before=old_ease,
        ease_factor_after=card.ease_factor,
    )
    store.create_review_log(log)

    return {"success": True}


# API Routes

@router.get("/api/flashcards/decks")
async def list_decks():
    """List all decks."""
    store = get_store()
    decks = store.list_decks()
    return {"decks": [d.to_dict() for d in decks]}


@router.post("/api/flashcards/decks")
async def create_deck(
    name: str = Form(...),
    description: str = Form(""),
):
    """Create a new deck."""
    store = get_store()
    deck = Deck(name=name, description=description)
    created = store.create_deck(deck)
    return {"success": True, "deck": created.to_dict()}


@router.get("/api/flashcards/deck/{deck_id}/cards")
async def list_cards(deck_id: int, limit: int = Query(50)):
    """List cards in a deck."""
    store = get_store()
    cards = store.get_flashcards_by_deck(deck_id, limit=limit)
    return {"cards": [c.to_dict() for c in cards]}


@router.post("/api/flashcards/cards")
async def create_card(
    deck_id: int = Form(...),
    front: str = Form(...),
    back: str = Form(...),
):
    """Create a new flashcard."""
    store = get_store()
    card = Flashcard(deck_id=deck_id, front=front, back=back)
    created = store.create_flashcard(card)
    return {"success": True, "card": created.to_dict()}


@router.delete("/api/flashcards/cards/{card_id}")
async def delete_card(card_id: int):
    """Delete a flashcard."""
    store = get_store()
    deleted = store.delete_flashcard(card_id)
    return {"success": deleted}
