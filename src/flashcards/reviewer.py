"""
Reviewer - Flashcard review session logic.

Manages review sessions with SM-2 scheduling.
"""

import time
import logging
from typing import List, Optional, Callable
from datetime import date

from .models import Flashcard, ReviewLog, ReviewSession, ReviewRating
from .scheduler import SM2Scheduler
from .store import FlashcardStore

logger = logging.getLogger(__name__)


class Reviewer:
    """
    Manages flashcard review sessions.

    Features:
    - Fetches due and new cards
    - Presents cards for review
    - Applies SM-2 scheduling
    - Records review logs
    """

    def __init__(
        self,
        store: FlashcardStore,
        scheduler: Optional[SM2Scheduler] = None,
        new_cards_per_session: int = 20,
        max_due_cards_per_session: int = 50,
    ):
        """
        Initialize the reviewer.

        Args:
            store: FlashcardStore instance
            scheduler: SM2Scheduler instance (default: new instance)
            new_cards_per_session: Maximum new cards to introduce per session
            max_due_cards_per_session: Maximum due cards to review per session
        """
        self.store = store
        self.scheduler = scheduler or SM2Scheduler()
        self.new_cards_per_session = new_cards_per_session
        self.max_due_cards_per_session = max_due_cards_per_session

    def start_session(
        self,
        deck_id: int,
        include_new: bool = True,
        include_due: bool = True,
    ) -> List[Flashcard]:
        """
        Start a review session and get cards to review.

        Args:
            deck_id: Deck ID to review
            include_new: Include new cards
            include_due: Include due cards

        Returns:
            List of cards to review
        """
        cards = []

        # Get due cards first (priority)
        if include_due:
            due_cards = self.store.get_due_cards(
                deck_id,
                limit=self.max_due_cards_per_session
            )
            cards.extend(due_cards)
            logger.info(f"Loaded {len(due_cards)} due cards")

        # Add new cards if quota allows
        if include_new and len(cards) < self.new_cards_per_session:
            remaining = self.new_cards_per_session - len(cards)
            new_cards = self.store.get_new_cards(deck_id, limit=remaining)
            cards.extend(new_cards)
            logger.info(f"Loaded {len(new_cards)} new cards")

        return cards

    def review_card(
        self,
        card: Flashcard,
        rating: int,
    ) -> tuple[Flashcard, ReviewLog]:
        """
        Review a single card with the given rating.

        Args:
            card: Flashcard to review
            rating: Quality rating (0-5)

        Returns:
            Tuple of (updated_card, review_log)
        """
        # Store before values
        interval_before = card.interval
        ease_factor_before = card.ease_factor

        # Calculate new schedule
        new_interval, new_ease, new_reps, next_review = self.scheduler.schedule(
            card, rating
        )

        # Update card
        card.interval = new_interval
        card.ease_factor = new_ease
        card.repetitions = new_reps
        card.next_review = next_review

        # Save updated card
        updated_card = self.store.update_flashcard(card)

        # Create review log
        log = ReviewLog(
            flashcard_id=card.id,
            rating=rating,
            interval_before=interval_before,
            interval_after=new_interval,
            ease_factor_before=ease_factor_before,
            ease_factor_after=new_ease,
        )
        saved_log = self.store.create_review_log(log)

        logger.debug(
            f"Reviewed card {card.id}: rating={rating}, "
            f"interval={interval_before}->{new_interval}"
        )

        return updated_card, saved_log

    def run_session(
        self,
        deck_id: int,
        rating_callback: Callable[[Flashcard], int],
        include_new: bool = True,
        include_due: bool = True,
    ) -> ReviewSession:
        """
        Run a complete review session.

        Args:
            deck_id: Deck ID to review
            rating_callback: Function that takes a card and returns a rating (0-5)
            include_new: Include new cards
            include_due: Include due cards

        Returns:
            ReviewSession with results
        """
        # Get deck info
        deck = self.store.get_deck(deck_id)
        if not deck:
            raise ValueError(f"Deck {deck_id} not found")

        session = ReviewSession(
            deck_id=deck_id,
            deck_name=deck.name,
        )

        # Get cards to review
        cards = self.start_session(deck_id, include_new, include_due)
        if not cards:
            logger.info("No cards to review")
            return session

        start_time = time.time()

        # Review each card
        for card in cards:
            try:
                rating = rating_callback(card)

                # Validate rating
                if not 0 <= rating <= 5:
                    logger.warning(f"Invalid rating {rating}, defaulting to 3")
                    rating = 3

                # Process review
                updated_card, log = self.review_card(card, rating)

                # Update session stats
                session.cards_reviewed += 1
                session.review_logs.append(log)

                if rating >= 3:
                    session.cards_correct += 1
                else:
                    session.cards_again += 1

            except Exception as e:
                logger.error(f"Error reviewing card {card.id}: {e}")
                continue

        session.duration_seconds = time.time() - start_time

        logger.info(
            f"Session complete: {session.cards_reviewed} cards, "
            f"{session.accuracy:.1f}% accuracy, "
            f"{session.duration_seconds:.1f}s"
        )

        return session

    def run_interactive_session(
        self,
        deck_id: int,
        show_answer_callback: Optional[Callable[[Flashcard], None]] = None,
    ) -> ReviewSession:
        """
        Run an interactive CLI review session.

        Args:
            deck_id: Deck ID to review
            show_answer_callback: Optional callback to show answer

        Returns:
            ReviewSession with results
        """
        def interactive_rating(card: Flashcard) -> int:
            """Get rating from user input."""
            print(f"\n{'='*60}")
            print(f"Q: {card.front}")
            print(f"{'='*60}")

            input("Press Enter to show answer...")

            print(f"\nA: {card.back}")
            print(f"\n{'-'*60}")

            if show_answer_callback:
                show_answer_callback(card)

            while True:
                try:
                    response = input(
                        "\nRate your recall:\n"
                        "  0 = Again (complete failure)\n"
                        "  1 = Hard (incorrect, recognized)\n"
                        "  2 = Hard (incorrect, easy recall)\n"
                        "  3 = Good (correct with difficulty)\n"
                        "  4 = Easy (correct after hesitation)\n"
                        "  5 = Very Easy (perfect)\n"
                        "\nYour rating (0-5): "
                    )
                    rating = int(response.strip())
                    if 0 <= rating <= 5:
                        return rating
                    print("Please enter a number between 0 and 5")
                except ValueError:
                    print("Invalid input, please enter a number")
                except KeyboardInterrupt:
                    print("\n\nSession interrupted")
                    return -1  # Signal to stop

            return 3  # Default to Good

        def rating_with_stop(card: Flashcard) -> int:
            """Wrapper to allow early termination."""
            rating = interactive_rating(card)
            if rating == -1:
                raise StopIteration("User cancelled")
            return rating

        try:
            return self.run_session(deck_id, rating_with_stop)
        except StopIteration:
            logger.info("Session stopped by user")
            # Return partial session
            return ReviewSession(
                deck_id=deck_id,
                deck_name=self.store.get_deck(deck_id).name if deck_id else "Unknown",
                cards_reviewed=0,
            )

    def preview_review_cards(self, deck_id: int) -> dict:
        """
        Preview cards that would be reviewed without starting a session.

        Args:
            deck_id: Deck ID

        Returns:
            Dict with due_count, new_count, total_to_review
        """
        deck = self.store.get_deck(deck_id)
        if not deck:
            return {"error": f"Deck {deck_id} not found"}

        stats = self.store.get_deck_stats(deck_id)

        due_to_review = min(stats.due_cards, self.max_due_cards_per_session)
        new_to_review = min(
            stats.new_cards,
            self.new_cards_per_session - due_to_review
        )

        return {
            "deck_name": stats.deck_name,
            "due_count": stats.due_cards,
            "new_count": stats.new_cards,
            "due_to_review": due_to_review,
            "new_to_review": max(0, new_to_review),
            "total_to_review": due_to_review + max(0, new_to_review),
        }
