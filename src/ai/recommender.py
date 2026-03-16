"""
Daily Recommender - Generates personalized daily study recommendations.
"""

import json
import logging
import os
from datetime import date, datetime, timedelta
from typing import List, Optional

from .models import DailyRecommendation, PreparednessPrediction, Priority
from .store import AIStore
from .analyzer import WeakAreasAnalyzer
from .predictor import PreparednessPredictor

logger = logging.getLogger(__name__)


class MiniMaxClient:
    """Simple MiniMax API client for recommendations."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        self.base_url = "https://api.minimax.chat/v1"

    def generate(self, prompt: str, max_tokens: int = 500, temperature: float = 0.5) -> str:
        """Generate text using MiniMax API."""
        if not self.api_key:
            return self._fallback_generate(prompt)

        try:
            import httpx

            url = f"{self.base_url}/text/chatcompletion_v2"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": "MiniMax-Text-01",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature,
            }

            response = httpx.post(url, json=payload, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except Exception as e:
            logger.warning(f"MiniMax API error: {e}")
            return self._fallback_generate(prompt)

    def _fallback_generate(self, prompt: str) -> str:
        """Fallback when API unavailable."""
        return json.dumps({
            "recommendations": [
                {
                    "title": "Review weak areas",
                    "description": "Focus on topics with low scores",
                    "priority": "high",
                    "action": "Study flashcards",
                    "minutes": 20,
                }
            ],
            "motivation": "Keep up the good work!",
        })


class DailyRecommender:
    """
    Generates personalized daily study recommendations.

    Uses:
    - Current weak areas
    - Due flashcards
    - Recent test performance
    - LLM for personalized tips
    """

    def __init__(
        self,
        ai_store: AIStore,
        analyzer: WeakAreasAnalyzer,
        predictor: PreparednessPredictor,
        flashcard_store=None,
        test_store=None,
        llm_client: Optional[MiniMaxClient] = None,
    ):
        """
        Initialize the recommender.

        Args:
            ai_store: AIStore instance
            analyzer: WeakAreasAnalyzer instance
            predictor: PreparednessPredictor instance
            flashcard_store: Optional FlashcardStore
            test_store: Optional TestStore
            llm_client: Optional MiniMaxClient
        """
        self.ai_store = ai_store
        self.analyzer = analyzer
        self.predictor = predictor
        self.flashcard_store = flashcard_store
        self.test_store = test_store
        self.llm = llm_client or MiniMaxClient()

    def get_recommendations(self, refresh: bool = False) -> List[DailyRecommendation]:
        """
        Get today's recommendations.

        Args:
            refresh: Force regeneration of recommendations

        Returns:
            List of DailyRecommendation objects
        """
        today = date.today().isoformat()

        # Check existing recommendations
        existing = self.ai_store.get_todays_recommendations()

        if existing and not refresh:
            return existing

        # Generate new recommendations
        return self._generate_recommendations()

    def _generate_recommendations(self) -> List[DailyRecommendation]:
        """Generate fresh recommendations for today."""
        today = date.today().isoformat()

        # Clear old recommendations
        self.ai_store.clear_todays_recommendations()

        recommendations = []

        # 1. Flashcard review (if due)
        if self.flashcard_store:
            rec = self._get_flashcard_recommendation(today)
            if rec:
                recommendations.append(rec)

        # 2. Weak area focus
        rec = self._get_weak_area_recommendation(today)
        if rec:
            recommendations.append(rec)

        # 3. Practice test (if haven't tested recently)
        rec = self._get_test_recommendation(today)
        if rec:
            recommendations.append(rec)

        # 4. New content (if caught up)
        rec = self._get_new_content_recommendation(today)
        if rec:
            recommendations.append(rec)

        # 5. LLM-enhanced tip
        if self.llm.api_key:
            rec = self._get_llm_tip(today)
            if rec:
                recommendations.append(rec)

        # Sort by priority
        priority_order = {Priority.CRITICAL: 0, Priority.HIGH: 1, Priority.MEDIUM: 2, Priority.LOW: 3}
        recommendations.sort(key=lambda r: priority_order[r.priority])

        # Save
        if recommendations:
            self.ai_store.save_recommendations_batch(recommendations)

        logger.info(f"Generated {len(recommendations)} recommendations")
        return recommendations

    def _get_flashcard_recommendation(self, today: str) -> Optional[DailyRecommendation]:
        """Get flashcard review recommendation."""
        if not self.flashcard_store:
            return None

        stats = self.flashcard_store.get_all_stats()
        due = stats.get("cards_due_today", 0)

        if due == 0:
            return None

        # Determine priority based on due count
        if due >= 20:
            priority = Priority.CRITICAL
        elif due >= 10:
            priority = Priority.HIGH
        else:
            priority = Priority.MEDIUM

        return DailyRecommendation(
            date=today,
            priority=priority,
            type="flashcard_review",
            title=f"Review {due} due flashcards",
            description=f"You have {due} flashcards due for spaced repetition review",
            action="Start flashcard review session",
            estimated_minutes=min(30, due * 2),
            reason="Spaced repetition optimizes long-term retention",
        )

    def _get_weak_area_recommendation(self, today: str) -> Optional[DailyRecommendation]:
        """Get weak area focus recommendation."""
        weak_areas = self.ai_store.get_weak_areas(limit=5)

        if not weak_areas:
            return None

        # Focus on most critical area
        area = weak_areas[0]

        if area.priority not in [Priority.CRITICAL, Priority.HIGH]:
            return None

        return DailyRecommendation(
            date=today,
            priority=area.priority,
            type="weak_area",
            title=f"Focus: Tema {area.tema}",
            description=f"Your weakest area (score: {area.combined_score}%)",
            action=f"Review Tema {area.tema} content and take a practice test",
            target_id=str(area.tema),
            estimated_minutes=25,
            reason=f"Current score: {area.combined_score}%",
        )

    def _get_test_recommendation(self, today: str) -> Optional[DailyRecommendation]:
        """Get practice test recommendation."""
        if not self.test_store:
            return None

        # Check if tested recently
        results = self.test_store.list_results(limit=5)

        if results:
            latest = results[0]
            if latest.created_at:
                days_since_test = (datetime.now() - latest.created_at).days

                if days_since_test < 2:
                    return None  # Tested recently

        # Get weak area to test
        weak_areas = self.ai_store.get_weak_areas(limit=1)
        tema = weak_areas[0].tema if weak_areas else None

        title = "Take a practice test"
        if tema:
            title = f"Take a practice test on Tema {tema}"

        return DailyRecommendation(
            date=today,
            priority=Priority.MEDIUM,
            type="test",
            title=title,
            description="Regular testing improves retention and identifies gaps",
            action="Generate and complete a practice test",
            target_id=str(tema) if tema else None,
            estimated_minutes=20,
            reason="Testing is key to measuring progress",
        )

    def _get_new_content_recommendation(self, today: str) -> Optional[DailyRecommendation]:
        """Get new content study recommendation."""
        # Check if caught up on reviews
        if self.flashcard_store:
            stats = self.flashcard_store.get_all_stats()
            due = stats.get("cards_due_today", 0)

            if due > 15:
                return None  # Too many reviews pending

        # Get prediction to see overall level
        prediction = self.ai_store.get_latest_prediction()

        if prediction and prediction.level == "beginner":
            # Need more foundational study
            return DailyRecommendation(
                date=today,
                priority=Priority.LOW,
                type="new_content",
                title="Study new temario content",
                description="Build your knowledge base with new material",
                action="Read and take notes on a new topic",
                estimated_minutes=20,
                reason="Foundation building phase",
            )

        return None

    def _get_llm_tip(self, today: str) -> Optional[DailyRecommendation]:
        """Get personalized tip from LLM."""
        prediction = self.ai_store.get_latest_prediction()
        metrics = self.ai_store.get_learning_metrics()
        weak_areas = self.ai_store.get_weak_areas(limit=3)

        prompt = f"""Generate a personalized study tip for a student preparing for exams.

Current status:
- Preparedness level: {prediction.level if prediction else 'unknown'}
- Overall score: {prediction.overall_score if prediction else 0}%
- Weak areas: {', '.join([f'Tema {a.tema}' for a in weak_areas])}
- Tests taken: {metrics.total_tests if metrics else 0}
- Flashcards reviewed: {metrics.total_reviews if metrics else 0}
- Study streak: {metrics.streak_days if metrics else 0} days

Return JSON:
{{
    "tip_title": "<short title>",
    "tip_description": "<detailed personalized tip>",
    "motivation": "<encouraging message>",
    "minutes": <recommended minutes for this activity>
}}
"""

        try:
            response = self.llm.generate(prompt, temperature=0.6)

            # Parse JSON
            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start >= 0 and json_end > json_start:
                data = json.loads(response[json_start:json_end])

                return DailyRecommendation(
                    date=today,
                    priority=Priority.LOW,
                    type="ai_tip",
                    title=data.get("tip_title", "Daily tip"),
                    description=data.get("tip_description", ""),
                    action=data.get("motivation", "Keep studying!"),
                    estimated_minutes=data.get("minutes", 15),
                    reason="Personalized AI recommendation",
                )

        except Exception as e:
            logger.warning(f"LLM tip generation failed: {e}")

        return None

    def complete_recommendation(self, rec_id: int) -> bool:
        """Mark a recommendation as completed."""
        return self.ai_store.mark_recommendation_completed(rec_id)

    def get_progress_summary(self) -> dict:
        """Get today's progress summary."""
        recommendations = self.ai_store.get_todays_recommendations()

        total = len(recommendations)
        completed = sum(1 for r in recommendations if r.completed)
        total_minutes = sum(r.estimated_minutes for r in recommendations)
        completed_minutes = sum(r.estimated_minutes for r in recommendations if r.completed)

        return {
            "total_recommendations": total,
            "completed": completed,
            "remaining": total - completed,
            "total_minutes": total_minutes,
            "completed_minutes": completed_minutes,
            "progress_percentage": round(completed / total * 100, 1) if total > 0 else 0,
        }
