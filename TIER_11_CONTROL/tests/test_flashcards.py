"""
Tests for the flashcards system.

Run with: pytest tests/test_flashcards.py -v
"""

import pytest
import tempfile
import os
from datetime import date, timedelta
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from TIER_10_USER_APPS.flashcards.models import Deck, Flashcard, ReviewLog, ReviewRating, DeckStats
from TIER_10_USER_APPS.flashcards.store import FlashcardStore
from TIER_10_USER_APPS.flashcards.scheduler import SM2Scheduler
from TIER_10_USER_APPS.flashcards.reviewer import Reviewer


# ============ Fixtures ============

@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    yield db_path
    os.unlink(db_path)


@pytest.fixture
def store(temp_db):
    """Create a FlashcardStore with temporary database."""
    return FlashcardStore(db_path=temp_db)


@pytest.fixture
def scheduler():
    """Create an SM2Scheduler instance."""
    return SM2Scheduler()


@pytest.fixture
def reviewer(store, scheduler):
    """Create a Reviewer instance."""
    return Reviewer(store, scheduler)


# ============ Model Tests ============

class TestDeck:
    """Tests for Deck model."""

    def test_deck_creation(self):
        """Test basic deck creation."""
        deck = Deck(name="Test Deck", description="Test description")
        assert deck.name == "Test Deck"
        assert deck.description == "Test description"
        assert deck.card_count == 0
        assert deck.id is None

    def test_deck_to_dict(self):
        """Test deck serialization."""
        deck = Deck(id=1, name="Test", card_count=5)
        data = deck.to_dict()
        assert data["id"] == 1
        assert data["name"] == "Test"
        assert data["card_count"] == 5

    def test_deck_from_dict(self):
        """Test deck deserialization."""
        data = {"id": 1, "name": "Test", "card_count": 5}
        deck = Deck.from_dict(data)
        assert deck.id == 1
        assert deck.name == "Test"
        assert deck.card_count == 5


class TestFlashcard:
    """Tests for Flashcard model."""

    def test_flashcard_creation(self):
        """Test basic flashcard creation."""
        card = Flashcard(deck_id=1, front="Q?", back="A.")
        assert card.deck_id == 1
        assert card.front == "Q?"
        assert card.back == "A."
        assert card.ease_factor == 2.5
        assert card.interval == 0
        assert card.repetitions == 0

    def test_is_new(self):
        """Test is_new property."""
        new_card = Flashcard(deck_id=1, front="Q", back="A", repetitions=0)
        assert new_card.is_new is True

        reviewed_card = Flashcard(deck_id=1, front="Q", back="A", repetitions=1)
        assert reviewed_card.is_new is False

    def test_is_due(self):
        """Test is_due property."""
        # New card is always due
        new_card = Flashcard(deck_id=1, front="Q", back="A", next_review=None)
        assert new_card.is_due is True

        # Past due date
        past = (date.today() - timedelta(days=1)).isoformat()
        past_card = Flashcard(deck_id=1, front="Q", back="A", next_review=past)
        assert past_card.is_due is True

        # Future due date
        future = (date.today() + timedelta(days=10)).isoformat()
        future_card = Flashcard(deck_id=1, front="Q", back="A", next_review=future)
        assert future_card.is_due is False


# ============ Store Tests ============

class TestFlashcardStore:
    """Tests for FlashcardStore."""

    def test_init_database(self, temp_db):
        """Test database initialization."""
        store = FlashcardStore(db_path=temp_db)
        assert Path(temp_db).exists()

    def test_create_deck(self, store):
        """Test deck creation."""
        deck = Deck(name="Test Deck", description="Test")
        created = store.create_deck(deck)

        assert created.id is not None
        assert created.name == "Test Deck"
        assert created.created_at is not None

    def test_get_deck(self, store):
        """Test getting a deck by ID."""
        deck = Deck(name="Test")
        created = store.create_deck(deck)

        retrieved = store.get_deck(created.id)
        assert retrieved is not None
        assert retrieved.name == "Test"

    def test_get_deck_by_name(self, store):
        """Test getting a deck by name."""
        deck = Deck(name="Unique Name")
        created = store.create_deck(deck)

        retrieved = store.get_deck_by_name("Unique Name")
        assert retrieved is not None
        assert retrieved.id == created.id

    def test_list_decks(self, store):
        """Test listing decks."""
        for i in range(3):
            store.create_deck(Deck(name=f"Deck {i}"))

        decks = store.list_decks()
        assert len(decks) == 3

    def test_delete_deck(self, store):
        """Test deleting a deck."""
        deck = store.create_deck(Deck(name="To Delete"))
        deleted = store.delete_deck(deck.id)
        assert deleted is True

        retrieved = store.get_deck(deck.id)
        assert retrieved is None

    def test_create_flashcard(self, store):
        """Test flashcard creation."""
        deck = store.create_deck(Deck(name="Test"))
        card = Flashcard(deck_id=deck.id, front="Q?", back="A.")
        created = store.create_flashcard(card)

        assert created.id is not None
        assert created.deck_id == deck.id

    def test_create_flashcards_batch(self, store):
        """Test batch card creation."""
        deck = store.create_deck(Deck(name="Test"))
        cards = [
            Flashcard(deck_id=deck.id, front=f"Q{i}?", back=f"A{i}.")
            for i in range(5)
        ]
        created = store.create_flashcards_batch(cards)

        assert len(created) == 5
        assert all(c.id is not None for c in created)

    def test_get_due_cards(self, store):
        """Test getting due cards."""
        deck = store.create_deck(Deck(name="Test"))

        # Create due card
        past = (date.today() - timedelta(days=1)).isoformat()
        due_card = Flashcard(
            deck_id=deck.id, front="Due", back="A",
            next_review=past
        )
        store.create_flashcard(due_card)

        # Create future card
        future = (date.today() + timedelta(days=10)).isoformat()
        future_card = Flashcard(
            deck_id=deck.id, front="Future", back="A",
            next_review=future
        )
        store.create_flashcard(future_card)

        due = store.get_due_cards(deck.id)
        assert len(due) == 1
        assert due[0].front == "Due"

    def test_deck_stats(self, store):
        """Test getting deck statistics."""
        deck = store.create_deck(Deck(name="Test"))

        # Create various cards
        store.create_flashcard(Flashcard(deck_id=deck.id, front="New", back="A"))
        past = (date.today() - timedelta(days=1)).isoformat()
        store.create_flashcard(Flashcard(
            deck_id=deck.id, front="Due", back="A",
            next_review=past, repetitions=1
        ))

        stats = store.get_deck_stats(deck.id)
        assert stats.total_cards == 2
        assert stats.new_cards == 1
        assert stats.due_cards == 2  # Both new and past-due


# ============ Scheduler Tests ============

class TestSM2Scheduler:
    """Tests for SM-2 scheduler."""

    def test_initial_schedule(self, scheduler):
        """Test scheduling a new card."""
        card = Flashcard(deck_id=1, front="Q", back="A")

        # First review with rating 3 (Good)
        interval, ease, reps, next_review = scheduler.schedule(card, 3)

        assert interval == 1
        assert reps == 1
        assert ease >= 1.3

    def test_second_review(self, scheduler):
        """Test second successful review."""
        card = Flashcard(
            deck_id=1, front="Q", back="A",
            interval=1, repetitions=1, ease_factor=2.5
        )

        # Second review with rating 3 (Good)
        interval, ease, reps, next_review = scheduler.schedule(card, 3)

        assert interval == 6
        assert reps == 2

    def test_third_review(self, scheduler):
        """Test third successful review (multiplying by ease factor)."""
        card = Flashcard(
            deck_id=1, front="Q", back="A",
            interval=6, repetitions=2, ease_factor=2.5
        )

        interval, ease, reps, next_review = scheduler.schedule(card, 3)

        # 6 * 2.5 = 15
        assert interval == 15
        assert reps == 3

    def test_failed_review(self, scheduler):
        """Test failed review resets repetitions."""
        card = Flashcard(
            deck_id=1, front="Q", back="A",
            interval=10, repetitions=3, ease_factor=2.5
        )

        # Failed review with rating 0 (Again)
        interval, ease, reps, next_review = scheduler.schedule(card, 0)

        assert interval == 1
        assert reps == 0

    def test_ease_factor_update(self, scheduler):
        """Test ease factor adjustment."""
        card = Flashcard(
            deck_id=1, front="Q", back="A",
            interval=1, repetitions=1, ease_factor=2.5
        )

        # Easy response should increase ease factor
        _, ease_easy, _, _ = scheduler.schedule(card, 5)
        assert ease_easy > 2.5

        # Hard response should decrease ease factor
        _, ease_hard, _, _ = scheduler.schedule(card, 3)
        assert ease_hard < ease_easy

    def test_min_ease_factor(self, scheduler):
        """Test that ease factor doesn't go below minimum."""
        card = Flashcard(
            deck_id=1, front="Q", back="A",
            interval=1, repetitions=1, ease_factor=1.35
        )

        # Multiple failures shouldn't go below 1.3
        _, ease, _, _ = scheduler.schedule(card, 0)
        assert ease >= 1.3

    def test_preview_intervals(self, scheduler):
        """Test interval preview."""
        # Preview with Good rating
        intervals = scheduler.preview_intervals(3, count=5)
        assert intervals[0] == 1  # First review
        assert intervals[1] == 6  # Second review
        assert intervals[2] > 6   # Third review (6 * ease)

    def test_invalid_rating(self, scheduler):
        """Test that invalid ratings raise error."""
        card = Flashcard(deck_id=1, front="Q", back="A")

        with pytest.raises(ValueError):
            scheduler.schedule(card, 6)

        with pytest.raises(ValueError):
            scheduler.schedule(card, -1)


# ============ Reviewer Tests ============

class TestReviewer:
    """Tests for Reviewer."""

    def test_start_session(self, store, scheduler, reviewer):
        """Test starting a review session."""
        deck = store.create_deck(Deck(name="Test"))

        # Create some cards
        for i in range(5):
            store.create_flashcard(Flashcard(
                deck_id=deck.id, front=f"Q{i}", back=f"A{i}"
            ))

        cards = reviewer.start_session(deck.id)
        assert len(cards) > 0

    def test_review_card(self, store, scheduler, reviewer):
        """Test reviewing a single card."""
        deck = store.create_deck(Deck(name="Test"))
        card = store.create_flashcard(Flashcard(
            deck_id=deck.id, front="Q", back="A"
        ))

        updated_card, log = reviewer.review_card(card, rating=3)

        assert updated_card.interval == 1
        assert updated_card.repetitions == 1
        assert log.rating == 3

    def test_preview_review_cards(self, store, scheduler, reviewer):
        """Test previewing review cards."""
        deck = store.create_deck(Deck(name="Test"))

        # Create new card
        store.create_flashcard(Flashcard(deck_id=deck.id, front="Q", back="A"))

        preview = reviewer.preview_review_cards(deck.id)
        assert preview["new_count"] == 1
        assert preview["total_to_review"] >= 1

    def test_run_session(self, store, scheduler, reviewer):
        """Test running a complete session."""
        deck = store.create_deck(Deck(name="Test"))

        # Create cards
        for i in range(3):
            store.create_flashcard(Flashcard(
                deck_id=deck.id, front=f"Q{i}", back=f"A{i}"
            ))

        # Mock rating callback
        ratings = [3, 4, 5]  # Good, Easy, Very Easy
        rating_iter = iter(ratings)

        def rating_callback(card):
            return next(rating_iter)

        session = reviewer.run_session(deck.id, rating_callback)

        assert session.cards_reviewed == 3
        assert session.cards_correct == 3
        assert session.accuracy == 100.0


# ============ Integration Tests ============

class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_full_workflow(self, store):
        """Test complete flashcard workflow."""
        scheduler = SM2Scheduler()
        reviewer = Reviewer(store, scheduler)

        # 1. Create deck
        deck = store.create_deck(Deck(
            name="Tema 1 - Derecho Constitucional",
            description="Fundamentos constitucionales"
        ))
        assert deck.id is not None

        # 2. Add cards
        cards = store.create_flashcards_batch([
            Flashcard(deck_id=deck.id, front="Que es la Constitucion?", back="La norma suprema..."),
            Flashcard(deck_id=deck.id, front="Que es el Estado de Derecho?", back="Aquel en que..."),
            Flashcard(deck_id=deck.id, front="Cuales son los poderes del Estado?", back="Legislativo, Ejecutivo y Judicial"),
        ])
        assert len(cards) == 3

        # 3. Preview review cards
        preview = reviewer.preview_review_cards(deck.id)
        assert preview["total_to_review"] >= 3  # All new cards should be included

        # 4. Review a single card manually
        first_card = cards[0]
        updated_card, log = reviewer.review_card(first_card, rating=3)
        assert updated_card.interval == 1
        assert updated_card.repetitions == 1
        assert log.rating == 3

        # 5. Check stats
        stats = store.get_deck_stats(deck.id)
        assert stats.total_cards == 3
        assert stats.total_reviews == 1  # Only one card reviewed manually


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
