"""
FlashcardStore - SQLite-based storage for flashcards with SM-2 scheduling.

Provides CRUD operations for decks, flashcards, and review logs.
"""

import sqlite3
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime, date

from .models import Deck, Flashcard, ReviewLog, DeckStats

logger = logging.getLogger(__name__)


class FlashcardStore:
    """SQLite-based storage for flashcards and decks."""

    def __init__(self, db_path: str = "data/flashcards.db"):
        """
        Initialize the store.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Decks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flashcard_decks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT DEFAULT '',
                    tema_id INTEGER,
                    card_count INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

            # Flashcards table with SM-2 fields
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flashcards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    deck_id INTEGER NOT NULL,
                    front TEXT NOT NULL,
                    back TEXT NOT NULL,
                    ease_factor REAL DEFAULT 2.5,
                    interval INTEGER DEFAULT 0,
                    repetitions INTEGER DEFAULT 0,
                    next_review TEXT,
                    source_chunk_id INTEGER,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (deck_id) REFERENCES flashcard_decks(id) ON DELETE CASCADE
                )
            """)

            # Review logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flashcard_reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flashcard_id INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    interval_before INTEGER DEFAULT 0,
                    interval_after INTEGER DEFAULT 0,
                    ease_factor_before REAL DEFAULT 2.5,
                    ease_factor_after REAL DEFAULT 2.5,
                    reviewed_at TEXT NOT NULL,
                    FOREIGN KEY (flashcard_id) REFERENCES flashcards(id) ON DELETE CASCADE
                )
            """)

            # Create indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_flashcards_deck_id
                ON flashcards(deck_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_flashcards_next_review
                ON flashcards(next_review)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_reviews_flashcard_id
                ON flashcard_reviews(flashcard_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_reviews_reviewed_at
                ON flashcard_reviews(reviewed_at)
            """)

            conn.commit()
            logger.info(f"Flashcard database initialized at {self.db_path}")

    # ============ Deck CRUD ============

    def create_deck(self, deck: Deck) -> Deck:
        """Create a new deck."""
        now = datetime.now().isoformat()
        deck.created_at = now
        deck.updated_at = now

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO flashcard_decks
                (name, description, tema_id, card_count, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                deck.name,
                deck.description,
                deck.tema_id,
                deck.card_count,
                deck.created_at,
                deck.updated_at,
            ))
            deck.id = cursor.lastrowid
            conn.commit()

        logger.info(f"Created deck: {deck.name} (id={deck.id})")
        return deck

    def get_deck(self, deck_id: int) -> Optional[Deck]:
        """Get a deck by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM flashcard_decks WHERE id = ?", (deck_id,)
            )
            row = cursor.fetchone()
            if row:
                return Deck.from_dict(dict(row))
        return None

    def get_deck_by_name(self, name: str) -> Optional[Deck]:
        """Get a deck by name."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM flashcard_decks WHERE name = ?", (name,)
            )
            row = cursor.fetchone()
            if row:
                return Deck.from_dict(dict(row))
        return None

    def list_decks(self, limit: int = 100, offset: int = 0) -> List[Deck]:
        """List all decks."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM flashcard_decks
                   ORDER BY created_at DESC LIMIT ? OFFSET ?""",
                (limit, offset),
            )
            rows = cursor.fetchall()
            return [Deck.from_dict(dict(row)) for row in rows]

    def update_deck(self, deck: Deck) -> Deck:
        """Update a deck."""
        deck.updated_at = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE flashcard_decks
                SET name=?, description=?, tema_id=?, card_count=?, updated_at=?
                WHERE id=?
            """, (
                deck.name,
                deck.description,
                deck.tema_id,
                deck.card_count,
                deck.updated_at,
                deck.id,
            ))
            conn.commit()

        logger.info(f"Updated deck: {deck.name} (id={deck.id})")
        return deck

    def delete_deck(self, deck_id: int) -> bool:
        """Delete a deck and all its flashcards."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM flashcard_decks WHERE id = ?", (deck_id,))
            deleted = cursor.rowcount > 0
            conn.commit()

        if deleted:
            logger.info(f"Deleted deck id={deck_id}")
        return deleted

    # ============ Flashcard CRUD ============

    def create_flashcard(self, card: Flashcard) -> Flashcard:
        """Create a new flashcard."""
        now = datetime.now().isoformat()
        card.created_at = now
        card.updated_at = now

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO flashcards
                (deck_id, front, back, ease_factor, interval, repetitions,
                 next_review, source_chunk_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                card.deck_id,
                card.front,
                card.back,
                card.ease_factor,
                card.interval,
                card.repetitions,
                card.next_review,
                card.source_chunk_id,
                card.created_at,
                card.updated_at,
            ))
            card.id = cursor.lastrowid

            # Update deck card count
            cursor.execute("""
                UPDATE flashcard_decks
                SET card_count = card_count + 1, updated_at = ?
                WHERE id = ?
            """, (now, card.deck_id))

            conn.commit()

        logger.info(f"Created flashcard id={card.id} in deck={card.deck_id}")
        return card

    def create_flashcards_batch(self, cards: List[Flashcard]) -> List[Flashcard]:
        """Create multiple flashcards in a single transaction."""
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for card in cards:
                card.created_at = now
                card.updated_at = now
                cursor.execute("""
                    INSERT INTO flashcards
                    (deck_id, front, back, ease_factor, interval, repetitions,
                     next_review, source_chunk_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    card.deck_id,
                    card.front,
                    card.back,
                    card.ease_factor,
                    card.interval,
                    card.repetitions,
                    card.next_review,
                    card.source_chunk_id,
                    card.created_at,
                    card.updated_at,
                ))
                card.id = cursor.lastrowid

            # Update deck card counts
            if cards:
                deck_id = cards[0].deck_id
                cursor.execute("""
                    UPDATE flashcard_decks
                    SET card_count = card_count + ?, updated_at = ?
                    WHERE id = ?
                """, (len(cards), now, deck_id))

            conn.commit()

        logger.info(f"Created {len(cards)} flashcards in batch")
        return cards

    def get_flashcard(self, card_id: int) -> Optional[Flashcard]:
        """Get a flashcard by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM flashcards WHERE id = ?", (card_id,)
            )
            row = cursor.fetchone()
            if row:
                return Flashcard.from_dict(dict(row))
        return None

    def get_flashcards_by_deck(
        self,
        deck_id: int,
        limit: int = 100,
        offset: int = 0
    ) -> List[Flashcard]:
        """Get all flashcards in a deck."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM flashcards
                   WHERE deck_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?""",
                (deck_id, limit, offset),
            )
            rows = cursor.fetchall()
            return [Flashcard.from_dict(dict(row)) for row in rows]

    def get_due_cards(self, deck_id: int, limit: int = 20) -> List[Flashcard]:
        """Get cards due for review in a deck."""
        today = date.today().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM flashcards
                   WHERE deck_id = ? AND (next_review IS NULL OR next_review <= ?)
                   ORDER BY next_review ASC NULLS FIRST, created_at ASC
                   LIMIT ?""",
                (deck_id, today, limit),
            )
            rows = cursor.fetchall()
            return [Flashcard.from_dict(dict(row)) for row in rows]

    def get_new_cards(self, deck_id: int, limit: int = 20) -> List[Flashcard]:
        """Get new (unreviewed) cards in a deck."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM flashcards
                   WHERE deck_id = ? AND repetitions = 0
                   ORDER BY created_at ASC LIMIT ?""",
                (deck_id, limit),
            )
            rows = cursor.fetchall()
            return [Flashcard.from_dict(dict(row)) for row in rows]

    def update_flashcard(self, card: Flashcard) -> Flashcard:
        """Update a flashcard."""
        card.updated_at = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE flashcards
                SET deck_id=?, front=?, back=?, ease_factor=?, interval=?,
                    repetitions=?, next_review=?, source_chunk_id=?, updated_at=?
                WHERE id=?
            """, (
                card.deck_id,
                card.front,
                card.back,
                card.ease_factor,
                card.interval,
                card.repetitions,
                card.next_review,
                card.source_chunk_id,
                card.updated_at,
                card.id,
            ))
            conn.commit()

        return card

    def delete_flashcard(self, card_id: int) -> bool:
        """Delete a flashcard."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Get deck_id before deleting
            cursor.execute("SELECT deck_id FROM flashcards WHERE id = ?", (card_id,))
            row = cursor.fetchone()
            if not row:
                return False
            deck_id = row[0]

            cursor.execute("DELETE FROM flashcards WHERE id = ?", (card_id,))
            deleted = cursor.rowcount > 0

            if deleted:
                # Update deck card count
                cursor.execute("""
                    UPDATE flashcard_decks
                    SET card_count = card_count - 1, updated_at = ?
                    WHERE id = ?
                """, (datetime.now().isoformat(), deck_id))

            conn.commit()

        if deleted:
            logger.info(f"Deleted flashcard id={card_id}")
        return deleted

    # ============ Review Log CRUD ============

    def create_review_log(self, log: ReviewLog) -> ReviewLog:
        """Create a review log entry."""
        log.reviewed_at = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO flashcard_reviews
                (flashcard_id, rating, interval_before, interval_after,
                 ease_factor_before, ease_factor_after, reviewed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                log.flashcard_id,
                log.rating,
                log.interval_before,
                log.interval_after,
                log.ease_factor_before,
                log.ease_factor_after,
                log.reviewed_at,
            ))
            log.id = cursor.lastrowid
            conn.commit()

        return log

    def get_review_logs(
        self,
        flashcard_id: int,
        limit: int = 100
    ) -> List[ReviewLog]:
        """Get review logs for a flashcard."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM flashcard_reviews
                   WHERE flashcard_id = ? ORDER BY reviewed_at DESC LIMIT ?""",
                (flashcard_id, limit),
            )
            rows = cursor.fetchall()
            return [ReviewLog.from_dict(dict(row)) for row in rows]

    def get_review_count(self, deck_id: Optional[int] = None) -> int:
        """Get total review count, optionally filtered by deck."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if deck_id:
                cursor.execute("""
                    SELECT COUNT(*) FROM flashcard_reviews r
                    JOIN flashcards f ON r.flashcard_id = f.id
                    WHERE f.deck_id = ?
                """, (deck_id,))
            else:
                cursor.execute("SELECT COUNT(*) FROM flashcard_reviews")
            return cursor.fetchone()[0]

    # ============ Statistics ============

    def get_deck_stats(self, deck_id: int) -> Optional[DeckStats]:
        """Get statistics for a deck."""
        deck = self.get_deck(deck_id)
        if not deck:
            return None

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Get card counts
            today = date.today().isoformat()
            cursor.execute("""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN repetitions = 0 THEN 1 ELSE 0 END) as new,
                    SUM(CASE WHEN next_review IS NULL OR next_review <= ? THEN 1 ELSE 0 END) as due,
                    AVG(ease_factor) as avg_ease
                FROM flashcards WHERE deck_id = ?
            """, (today, deck_id))
            row = cursor.fetchone()

            total_reviews = self.get_review_count(deck_id)

            return DeckStats(
                deck_id=deck_id,
                deck_name=deck.name,
                total_cards=row["total"] or 0,
                new_cards=row["new"] or 0,
                due_cards=row["due"] or 0,
                learned_cards=(row["total"] or 0) - (row["new"] or 0),
                average_ease_factor=round(row["avg_ease"] or 2.5, 2),
                total_reviews=total_reviews,
            )

    def get_all_stats(self) -> dict:
        """Get global statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM flashcard_decks")
            deck_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM flashcards")
            card_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM flashcard_reviews")
            review_count = cursor.fetchone()[0]

            cursor.execute("SELECT AVG(ease_factor) FROM flashcards")
            avg_ease = cursor.fetchone()[0] or 2.5

            today = date.today().isoformat()
            cursor.execute("""
                SELECT COUNT(*) FROM flashcards
                WHERE next_review IS NULL OR next_review <= ?
            """, (today,))
            due_count = cursor.fetchone()[0]

            return {
                "total_decks": deck_count,
                "total_cards": card_count,
                "total_reviews": review_count,
                "cards_due_today": due_count,
                "average_ease_factor": round(avg_ease, 2),
            }
