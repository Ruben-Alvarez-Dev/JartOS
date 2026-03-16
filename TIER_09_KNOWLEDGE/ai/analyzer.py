"""
Weak Areas Analyzer - Analyzes flashcard and test data to identify weak areas.
"""

import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Optional, Dict

from .models import WeakArea, LearningMetrics, Priority
from .store import AIStore

logger = logging.getLogger(__name__)


class WeakAreasAnalyzer:
    """
    Analyzes learning data to identify weak areas.

    Combines data from:
    - Flashcard ease factors (SM-2 algorithm)
    - Test scores by topic
    - Review history patterns
    """

    # Threshold for low ease factor (below 2.3 indicates struggling)
    LOW_EASE_THRESHOLD = 2.3
    # Threshold for test score weakness (below 60%)
    LOW_TEST_THRESHOLD = 60.0

    def __init__(
        self,
        ai_store: AIStore,
        flashcard_store=None,
        test_store=None,
        temario_store=None,
    ):
        """
        Initialize the analyzer.

        Args:
            ai_store: AIStore instance
            flashcard_store: Optional FlashcardStore for flashcard data
            test_store: Optional TestStore for test data
            temario_store: Optional TemarioStore for topic info
        """
        self.ai_store = ai_store
        self.flashcard_store = flashcard_store
        self.test_store = test_store
        self.temario_store = temario_store

    def analyze_all(self) -> List[WeakArea]:
        """
        Perform comprehensive weak area analysis.

        Returns:
            List of identified weak areas, sorted by severity
        """
        # Collect data from both sources
        flashcard_areas = self._analyze_flashcard_areas() if self.flashcard_store else {}
        test_areas = self._analyze_test_areas() if self.test_store else {}

        # Merge and compute combined scores
        weak_areas = self._merge_area_data(flashcard_areas, test_areas)

        # Prioritize
        weak_areas = self._prioritize_areas(weak_areas)

        # Save to store
        if weak_areas:
            self.ai_store.clear_weak_areas()
            self.ai_store.save_weak_areas_batch(weak_areas)

        logger.info(f"Identified {len(weak_areas)} weak areas")
        return weak_areas

    def _analyze_flashcard_areas(self) -> Dict[str, dict]:
        """
        Analyze flashcard data by topic.

        Returns:
            Dict mapping area key to statistics
        """
        areas = defaultdict(lambda: {
            "ease_factors": [],
            "card_count": 0,
            "again_count": 0,
            "tema": None,
            "apartado": None,
        })

        try:
            # Get all decks
            decks = self.flashcard_store.list_decks()

            for deck in decks:
                # Get cards for this deck
                cards = self.flashcard_store.get_flashcards_by_deck(deck.id)

                for card in cards:
                    # Determine area key
                    area_key = f"tema_{deck.tema_id}" if deck.tema_id else f"deck_{deck.id}"

                    # Collect ease factor
                    areas[area_key]["ease_factors"].append(card.ease_factor)
                    areas[area_key]["card_count"] += 1
                    areas[area_key]["tema"] = deck.tema_id
                    areas[area_key]["deck_name"] = deck.name

                    # Get review logs to count "again" ratings
                    if card.repetitions > 0:
                        reviews = self.flashcard_store.get_review_logs(card.id, limit=10)
                        again_ratings = sum(1 for r in reviews if r.rating == 0)
                        areas[area_key]["again_count"] += again_ratings

            # Calculate averages
            result = {}
            for key, data in areas.items():
                if data["ease_factors"]:
                    avg_ease = sum(data["ease_factors"]) / len(data["ease_factors"])
                    again_rate = data["again_count"] / max(len(data["ease_factors"]), 1) * 100

                    result[key] = {
                        "avg_ease_factor": avg_ease,
                        "card_count": data["card_count"],
                        "again_rate": again_rate,
                        "tema": data["tema"],
                        "deck_name": data.get("deck_name", key),
                    }

            return result

        except Exception as e:
            logger.error(f"Error analyzing flashcard areas: {e}")
            return {}

    def _analyze_test_areas(self) -> Dict[str, dict]:
        """
        Analyze test results by topic.

        Returns:
            Dict mapping area key to statistics
        """
        areas = defaultdict(lambda: {
            "scores": [],
            "test_count": 0,
        })

        try:
            # Get all test results
            results = self.test_store.list_results(limit=100)

            for result in results:
                # Use weak_areas and strong_areas to identify topics
                for area in result.weak_areas:
                    areas[area]["scores"].append(30)  # Approximate low score for weak area
                    areas[area]["test_count"] += 1

                for area in result.strong_areas:
                    areas[area]["scores"].append(80)  # Approximate high score for strong area
                    areas[area]["test_count"] += 1

                # Also track overall scores by test config temas
                test = self.test_store.get_test(result.test_id)
                if test and test.config.temas:
                    for tema in test.config.temas:
                        key = f"tema_{tema}"
                        areas[key]["scores"].append(result.score_percentage)
                        areas[key]["test_count"] += 1

            # Calculate averages
            result = {}
            for key, data in areas.items():
                if data["scores"]:
                    avg_score = sum(data["scores"]) / len(data["scores"])
                    result[key] = {
                        "avg_score": avg_score,
                        "test_count": data["test_count"],
                    }

            return result

        except Exception as e:
            logger.error(f"Error analyzing test areas: {e}")
            return {}

    def _merge_area_data(
        self,
        flashcard_areas: Dict[str, dict],
        test_areas: Dict[str, dict],
    ) -> List[WeakArea]:
        """
        Merge flashcard and test area data.

        Args:
            flashcard_areas: Data from flashcard analysis
            test_areas: Data from test analysis

        Returns:
            List of WeakArea objects
        """
        all_keys = set(flashcard_areas.keys()) | set(test_areas.keys())
        weak_areas = []

        for key in all_keys:
            fc_data = flashcard_areas.get(key, {})
            test_data = test_areas.get(key, {})

            # Calculate combined score (weighted average)
            # Normalize ease factor to 0-100 scale (2.5 = 50%, lower = worse)
            ease_score = 0
            if fc_data.get("avg_ease_factor"):
                # Ease factor ranges from 1.3 to 3.0+
                # Map 1.3 -> 0, 2.5 -> 50, 3.0 -> 75
                ease = fc_data["avg_ease_factor"]
                ease_score = max(0, min(100, (ease - 1.3) / 1.7 * 100))

            test_score = test_data.get("avg_score", 50)

            # Weight: 60% test, 40% flashcard (tests more reliable indicator)
            if fc_data and test_data:
                combined = test_score * 0.6 + ease_score * 0.4
                source = "combined"
            elif test_data:
                combined = test_score
                source = "tests"
            else:
                combined = ease_score
                source = "flashcards"

            # Only include if combined score is below threshold or ease is low
            if combined < 60 or fc_data.get("avg_ease_factor", 3.0) < self.LOW_EASE_THRESHOLD:
                # Extract tema and apartado from key
                tema = fc_data.get("tema") or self._extract_tema_from_key(key)

                weak_area = WeakArea(
                    tema=str(tema) if tema else key,
                    apartado=fc_data.get("deck_name", ""),
                    source=source,
                    flashcard_ease_avg=fc_data.get("avg_ease_factor", 2.5),
                    test_score_avg=test_data.get("avg_score", 0),
                    combined_score=round(combined, 1),
                    cards_affected=fc_data.get("card_count", 0),
                    tests_affected=test_data.get("test_count", 0),
                )
                weak_areas.append(weak_area)

        return weak_areas

    def _extract_tema_from_key(self, key: str) -> Optional[str]:
        """Extract tema number from key like 'tema_1' or 'deck_2'."""
        if key.startswith("tema_"):
            return key[5:]
        return None

    def _prioritize_areas(self, areas: List[WeakArea]) -> List[WeakArea]:
        """
        Assign priorities to weak areas.

        Args:
            areas: List of weak areas

        Returns:
            Sorted list with priorities assigned
        """
        for area in areas:
            if area.combined_score < 30:
                area.priority = Priority.CRITICAL
            elif area.combined_score < 45:
                area.priority = Priority.HIGH
            elif area.combined_score < 55:
                area.priority = Priority.MEDIUM
            else:
                area.priority = Priority.LOW

        # Sort by priority then by combined score
        priority_order = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3,
        }
        areas.sort(key=lambda a: (priority_order[a.priority], a.combined_score))

        return areas

    def compute_learning_metrics(self) -> LearningMetrics:
        """
        Compute comprehensive learning metrics.

        Returns:
            LearningMetrics object
        """
        metrics = LearningMetrics()

        try:
            # Flashcard metrics
            if self.flashcard_store:
                stats = self.flashcard_store.get_all_stats()
                metrics.total_flashcards = stats.get("total_cards", 0)
                metrics.flashcards_new = stats.get("total_cards", 0) - stats.get("total_reviews", 0)
                metrics.flashcards_learned = stats.get("total_reviews", 0)
                metrics.avg_ease_factor = stats.get("average_ease_factor", 2.5)
                metrics.total_reviews = stats.get("total_reviews", 0)

                # Calculate again rate from review logs
                if metrics.total_reviews > 0:
                    # Estimate based on low ease factor cards
                    decks = self.flashcard_store.list_decks()
                    again_count = 0
                    total_cards = 0
                    for deck in decks:
                        cards = self.flashcard_store.get_flashcards_by_deck(deck.id)
                        for card in cards:
                            total_cards += 1
                            if card.ease_factor < self.LOW_EASE_THRESHOLD:
                                again_count += 1
                    metrics.again_rate = (again_count / max(total_cards, 1)) * 100

            # Test metrics
            if self.test_store:
                results = self.test_store.list_results(limit=200)
                metrics.total_tests = len(results)
                metrics.tests_passed = sum(1 for r in results if r.passed)

                if results:
                    metrics.avg_test_score = sum(r.score_percentage for r in results) / len(results)

                # Count weak areas
                weak_areas = self.analyze_all()
                metrics.weak_areas_count = len([a for a in weak_areas if a.priority in [Priority.CRITICAL, Priority.HIGH]])

            # Save metrics
            self.ai_store.save_learning_metrics(metrics)

        except Exception as e:
            logger.error(f"Error computing learning metrics: {e}")

        return metrics

    def get_study_time_estimate(self) -> dict:
        """
        Estimate study time based on weak areas and metrics.

        Returns:
            Dict with time estimates
        """
        weak_areas = self.ai_store.get_weak_areas(limit=10)
        metrics = self.ai_store.get_learning_metrics()

        # Base: 2 hours per weak area per week
        critical_areas = len([a for a in weak_areas if a.priority == Priority.CRITICAL])
        high_areas = len([a for a in weak_areas if a.priority == Priority.HIGH])

        recommended_hours = (
            critical_areas * 3 +  # 3 hours per critical area
            high_areas * 2 +       # 2 hours per high area
            max(0, 5 - critical_areas - high_areas)  # Base 5 hours
        )

        return {
            "recommended_hours_per_week": min(recommended_hours, 25),
            "critical_areas": critical_areas,
            "high_areas": high_areas,
            "total_weak_areas": len(weak_areas),
        }
