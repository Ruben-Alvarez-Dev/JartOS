"""
SM-2 Spaced Repetition Scheduler.

Implements the SuperMemo 2 algorithm for flashcard scheduling.
"""

from datetime import date, timedelta
from typing import Tuple
import logging

from .models import Flashcard, ReviewRating

logger = logging.getLogger(__name__)


class SM2Scheduler:
    """
    SM-2 Algorithm Implementation.

    Based on: https://www.supermemo.com/en/archives1990-2015/english/ol/sm2

    The algorithm calculates:
    - interval: Days until next review
    - ease_factor: Difficulty adjustment (1.3 - 3.0+)
    - repetitions: Consecutive successful reviews
    """

    # SM-2 parameters
    MIN_EASE_FACTOR = 1.3
    DEFAULT_EASE_FACTOR = 2.5

    def __init__(
        self,
        easy_bonus: float = 1.3,
        interval_modifier: float = 1.0,
        new_cards_per_day: int = 20,
    ):
        """
        Initialize the scheduler.

        Args:
            easy_bonus: Multiplier for easy responses
            interval_modifier: Global interval multiplier
            new_cards_per_day: Maximum new cards to introduce per day
        """
        self.easy_bonus = easy_bonus
        self.interval_modifier = interval_modifier
        self.new_cards_per_day = new_cards_per_day

    def schedule(
        self,
        card: Flashcard,
        rating: int
    ) -> Tuple[int, float, int, str]:
        """
        Calculate next review based on SM-2 algorithm.

        Args:
            card: Flashcard to schedule
            rating: Quality rating (0-5)

        Returns:
            Tuple of (new_interval, new_ease_factor, new_repetitions, next_review_date)
        """
        # Validate rating
        if not 0 <= rating <= 5:
            raise ValueError(f"Rating must be 0-5, got {rating}")

        # Get current values
        ease_factor = card.ease_factor
        repetitions = card.repetitions
        interval = card.interval

        if rating >= 3:
            # Correct response
            new_repetitions, new_interval = self._calculate_success(
                repetitions, interval, ease_factor, rating
            )
            # Update ease factor
            new_ease_factor = self._calculate_ease_factor(ease_factor, rating)
        else:
            # Incorrect response - reset
            new_repetitions = 0
            new_interval = 1  # Review again tomorrow
            new_ease_factor = ease_factor  # Keep ease factor unchanged

            # Optionally decrease ease factor for failures
            if rating == 0:  # Complete failure
                new_ease_factor = max(
                    self.MIN_EASE_FACTOR,
                    ease_factor - 0.2
                )

        # Apply interval modifier
        new_interval = max(1, round(new_interval * self.interval_modifier))

        # Calculate next review date
        next_review = (date.today() + timedelta(days=new_interval)).isoformat()

        logger.debug(
            f"SM-2: rating={rating}, interval={interval}->{new_interval}, "
            f"ease={ease_factor:.2f}->{new_ease_factor:.2f}, "
            f"reps={repetitions}->{new_repetitions}"
        )

        return new_interval, new_ease_factor, new_repetitions, next_review

    def _calculate_success(
        self,
        repetitions: int,
        interval: int,
        ease_factor: float,
        rating: int
    ) -> Tuple[int, int]:
        """
        Calculate new repetition count and interval for successful review.

        Returns:
            Tuple of (new_repetitions, new_interval)
        """
        new_repetitions = repetitions + 1

        if new_repetitions == 1:
            # First successful review
            new_interval = 1
        elif new_repetitions == 2:
            # Second successful review
            new_interval = 6
        else:
            # Subsequent reviews - multiply by ease factor
            new_interval = round(interval * ease_factor)

        # Apply easy bonus for very easy responses
        if rating == 5:
            new_interval = round(new_interval * self.easy_bonus)

        return new_repetitions, new_interval

    def _calculate_ease_factor(
        self,
        current_ease: float,
        rating: int
    ) -> float:
        """
        Calculate new ease factor based on response quality.

        Formula: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))

        Args:
            current_ease: Current ease factor
            rating: Quality rating (0-5)

        Returns:
            New ease factor (clamped to minimum 1.3)
        """
        # SM-2 formula
        delta = 0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02)
        new_ease = current_ease + delta

        # Clamp to minimum
        return max(self.MIN_EASE_FACTOR, new_ease)

    def get_due_cards_count(self, cards: list) -> int:
        """
        Count cards due for review today.

        Args:
            cards: List of Flashcard objects

        Returns:
            Number of due cards
        """
        today = date.today()
        count = 0
        for card in cards:
            if card.is_due:
                count += 1
        return count

    def get_new_cards_count(self, cards: list) -> int:
        """
        Count new (unreviewed) cards.

        Args:
            cards: List of Flashcard objects

        Returns:
            Number of new cards
        """
        return sum(1 for card in cards if card.is_new)

    def preview_intervals(self, rating: int, count: int = 5) -> list:
        """
        Preview interval progression for a given rating.

        Args:
            rating: Quality rating to simulate
            count: Number of reviews to simulate

        Returns:
            List of intervals in days
        """
        # Create a mock card
        card = Flashcard(
            ease_factor=self.DEFAULT_EASE_FACTOR,
            interval=0,
            repetitions=0
        )

        intervals = []
        for _ in range(count):
            interval, ease, reps, _ = self.schedule(card, rating)
            intervals.append(interval)
            card.interval = interval
            card.ease_factor = ease
            card.repetitions = reps

        return intervals
