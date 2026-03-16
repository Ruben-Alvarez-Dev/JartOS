"""
Data models for the flashcards system with SM-2 spaced repetition.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class ReviewRating(int, Enum):
    """SM-2 quality rating (0-5)."""
    AGAIN = 0      # Complete failure
    HARD = 1       # Incorrect, but recognized
    HARD2 = 2      # Incorrect, but easy to recall
    GOOD = 3       # Correct with difficulty
    EASY = 4       # Correct after hesitation
    VERY_EASY = 5  # Perfect response


@dataclass
class Deck:
    """Represents a flashcard deck."""

    id: Optional[int] = None
    name: str = ""
    description: str = ""
    tema_id: Optional[int] = None
    card_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tema_id": self.tema_id,
            "card_count": self.card_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Deck":
        """Create from dictionary."""
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            description=data.get("description", ""),
            tema_id=data.get("tema_id"),
            card_count=data.get("card_count", 0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


@dataclass
class Flashcard:
    """Represents a flashcard with SM-2 scheduling fields."""

    id: Optional[int] = None
    deck_id: int = 0
    front: str = ""
    back: str = ""
    # SM-2 fields
    ease_factor: float = 2.5  # Default ease factor (1.3 - 3.0+)
    interval: int = 0         # Days until next review (0 = new)
    repetitions: int = 0      # Number of successful reviews
    next_review: Optional[str] = None  # ISO date string
    # Metadata
    source_chunk_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "deck_id": self.deck_id,
            "front": self.front,
            "back": self.back,
            "ease_factor": self.ease_factor,
            "interval": self.interval,
            "repetitions": self.repetitions,
            "next_review": self.next_review,
            "source_chunk_id": self.source_chunk_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Flashcard":
        """Create from dictionary."""
        return cls(
            id=data.get("id"),
            deck_id=data.get("deck_id", 0),
            front=data.get("front", ""),
            back=data.get("back", ""),
            ease_factor=data.get("ease_factor", 2.5),
            interval=data.get("interval", 0),
            repetitions=data.get("repetitions", 0),
            next_review=data.get("next_review"),
            source_chunk_id=data.get("source_chunk_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    @property
    def is_new(self) -> bool:
        """Check if card is new (never reviewed)."""
        return self.repetitions == 0

    @property
    def is_due(self) -> bool:
        """Check if card is due for review."""
        if not self.next_review:
            return True  # New cards are always due
        due_date = date.fromisoformat(self.next_review)
        return due_date <= date.today()


@dataclass
class ReviewLog:
    """Represents a flashcard review record."""

    id: Optional[int] = None
    flashcard_id: int = 0
    rating: int = 0  # 0-5 (ReviewRating)
    interval_before: int = 0
    interval_after: int = 0
    ease_factor_before: float = 2.5
    ease_factor_after: float = 2.5
    reviewed_at: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "flashcard_id": self.flashcard_id,
            "rating": self.rating,
            "interval_before": self.interval_before,
            "interval_after": self.interval_after,
            "ease_factor_before": self.ease_factor_before,
            "ease_factor_after": self.ease_factor_after,
            "reviewed_at": self.reviewed_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ReviewLog":
        """Create from dictionary."""
        return cls(
            id=data.get("id"),
            flashcard_id=data.get("flashcard_id", 0),
            rating=data.get("rating", 0),
            interval_before=data.get("interval_before", 0),
            interval_after=data.get("interval_after", 0),
            ease_factor_before=data.get("ease_factor_before", 2.5),
            ease_factor_after=data.get("ease_factor_after", 2.5),
            reviewed_at=data.get("reviewed_at"),
        )


@dataclass
class ReviewSession:
    """Represents a review session result."""

    deck_id: int
    deck_name: str
    cards_reviewed: int = 0
    cards_correct: int = 0
    cards_again: int = 0
    duration_seconds: float = 0.0
    review_logs: List[ReviewLog] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage."""
        if self.cards_reviewed == 0:
            return 0.0
        return (self.cards_correct / self.cards_reviewed) * 100

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "deck_id": self.deck_id,
            "deck_name": self.deck_name,
            "cards_reviewed": self.cards_reviewed,
            "cards_correct": self.cards_correct,
            "cards_again": self.cards_again,
            "accuracy": self.accuracy,
            "duration_seconds": self.duration_seconds,
            "review_logs": [log.to_dict() for log in self.review_logs],
        }


@dataclass
class DeckStats:
    """Statistics for a deck."""

    deck_id: int
    deck_name: str
    total_cards: int = 0
    new_cards: int = 0
    due_cards: int = 0
    learned_cards: int = 0
    average_ease_factor: float = 2.5
    total_reviews: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "deck_id": self.deck_id,
            "deck_name": self.deck_name,
            "total_cards": self.total_cards,
            "new_cards": self.new_cards,
            "due_cards": self.due_cards,
            "learned_cards": self.learned_cards,
            "average_ease_factor": self.average_ease_factor,
            "total_reviews": self.total_reviews,
        }
