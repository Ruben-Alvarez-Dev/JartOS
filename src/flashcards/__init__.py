"""
Flashcards module - SM-2 spaced repetition system.

This module provides a complete flashcard system with:
- SM-2 algorithm for spaced repetition scheduling
- SQLite storage for decks, cards, and review logs
- Interactive CLI for card management and review
- AI-powered card generation from temario content

Usage:
    from flashcards import FlashcardStore, SM2Scheduler, Reviewer

    # Initialize
    store = FlashcardStore()
    scheduler = SM2Scheduler()
    reviewer = Reviewer(store, scheduler)

    # Create a deck
    deck = store.create_deck(Deck(name="Tema 1"))

    # Add cards
    card = store.create_flashcard(Flashcard(
        deck_id=deck.id,
        front="What is X?",
        back="X is Y.",
    ))

    # Review cards
    session = reviewer.run_interactive_session(deck.id)
"""

from .models import (
    Deck,
    Flashcard,
    ReviewLog,
    ReviewRating,
    ReviewSession,
    DeckStats,
)
from .store import FlashcardStore
from .scheduler import SM2Scheduler
from .reviewer import Reviewer
from .generator import (
    FlashcardGenerator,
    GeneratedCard,
    generate_for_deck,
)
from .cli import main as cli_main

__all__ = [
    # Models
    "Deck",
    "Flashcard",
    "ReviewLog",
    "ReviewRating",
    "ReviewSession",
    "DeckStats",
    # Storage
    "FlashcardStore",
    # Scheduling
    "SM2Scheduler",
    # Review
    "Reviewer",
    # Generation
    "FlashcardGenerator",
    "GeneratedCard",
    "generate_for_deck",
    # CLI
    "cli_main",
]

__version__ = "1.0.0"
