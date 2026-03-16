"""
Preparedness Predictor - Predicts exam readiness using LLM and historical data.
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Optional, List

from .models import PreparednessPrediction, LearningMetrics, Priority
from .store import AIStore
from .analyzer import WeakAreasAnalyzer

logger = logging.getLogger(__name__)


class MiniMaxClient:
    """Simple MiniMax API client for predictions."""

    def __init__(self, api_key: Optional[str] = None, model: str = "MiniMax-Text-01"):
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        self.model = model
        self.base_url = "https://api.minimax.chat/v1"

    def generate(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.3) -> str:
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
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature,
            }

            response = httpx.post(url, json=payload, headers=headers, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except Exception as e:
            logger.warning(f"MiniMax API error: {e}")
            return self._fallback_generate(prompt)

    def _fallback_generate(self, prompt: str) -> str:
        """Fallback when API unavailable."""
        # Return a simple JSON response based on prompt analysis
        if "preparedness" in prompt.lower() or "prediction" in prompt.lower():
            return json.dumps({
                "overall_score": 50,
                "confidence": 0.5,
                "level": "intermediate",
                "recommended_hours_per_week": 10,
                "estimated_days_to_ready": 30,
                "key_factors": ["Based on available metrics"],
                "suggestions": ["Continue regular study", "Focus on weak areas"],
            })
        return "{}"


class PreparednessPredictor:
    """
    Predicts exam preparedness using ML heuristics and LLM insights.

    Factors considered:
    - Flashcard retention (ease factor, review success rate)
    - Test performance (average scores, trends)
    - Study consistency (days active, streak)
    - Weak areas count and severity
    """

    # Scoring weights
    FLASHCARD_WEIGHT = 0.25
    TEST_WEIGHT = 0.35
    CONSISTENCY_WEIGHT = 0.20
    WEAK_AREAS_WEIGHT = 0.20

    def __init__(
        self,
        ai_store: AIStore,
        analyzer: WeakAreasAnalyzer,
        llm_client: Optional[MiniMaxClient] = None,
    ):
        """
        Initialize the predictor.

        Args:
            ai_store: AIStore instance
            analyzer: WeakAreasAnalyzer instance
            llm_client: Optional MiniMaxClient for LLM insights
        """
        self.ai_store = ai_store
        self.analyzer = analyzer
        self.llm = llm_client or MiniMaxClient()

    def predict(self, use_llm: bool = True) -> PreparednessPrediction:
        """
        Generate a preparedness prediction.

        Args:
            use_llm: Whether to use LLM for enhanced insights

        Returns:
            PreparednessPrediction object
        """
        # Compute fresh metrics
        metrics = self.analyzer.compute_learning_metrics()

        # Calculate base scores
        flashcard_score = self._calculate_flashcard_score(metrics)
        test_score = self._calculate_test_score(metrics)
        consistency_score = self._calculate_consistency_score(metrics)
        weak_areas_score = self._calculate_weak_areas_score(metrics)

        # Weighted combination
        overall_score = (
            flashcard_score * self.FLASHCARD_WEIGHT +
            test_score * self.TEST_WEIGHT +
            consistency_score * self.CONSISTENCY_WEIGHT +
            weak_areas_score * self.WEAK_AREAS_WEIGHT
        )

        # Determine level
        level = self._determine_level(overall_score)

        # Calculate confidence based on data availability
        confidence = self._calculate_confidence(metrics)

        # Get weak and strong areas
        weak_areas = self._get_weak_area_names()
        strong_areas = self._get_strong_area_names(metrics, test_score)

        # Estimate time to ready
        days_to_ready = self._estimate_days_to_ready(overall_score, metrics)

        # Build prediction
        prediction = PreparednessPrediction(
            overall_score=round(overall_score, 1),
            confidence=round(confidence, 2),
            level=level,
            weak_areas=weak_areas[:5],
            strong_areas=strong_areas[:3],
            recommended_hours_per_week=self._recommend_study_hours(overall_score, metrics),
            estimated_days_to_ready=days_to_ready,
            factors={
                "flashcard_score": round(flashcard_score, 1),
                "test_score": round(test_score, 1),
                "consistency_score": round(consistency_score, 1),
                "weak_areas_score": round(weak_areas_score, 1),
                "total_reviews": metrics.total_reviews,
                "total_tests": metrics.total_tests,
            },
        )

        # Optionally enhance with LLM
        if use_llm and self.llm.api_key:
            prediction = self._enhance_with_llm(prediction, metrics)

        # Save prediction
        self.ai_store.save_prediction(prediction)

        logger.info(f"Generated prediction: {prediction.overall_score}% ({prediction.level})")
        return prediction

    def _calculate_flashcard_score(self, metrics: LearningMetrics) -> float:
        """Calculate score based on flashcard performance."""
        if metrics.total_flashcards == 0:
            return 50.0  # Neutral if no data

        # Higher ease factor = better retention
        ease_score = min(100, (metrics.avg_ease_factor - 1.3) / 1.7 * 100)

        # Lower again rate = better
        again_score = max(0, 100 - metrics.again_rate * 2)

        # Learning progress
        if metrics.total_flashcards > 0:
            progress_score = (metrics.flashcards_learned / metrics.total_flashcards) * 100
        else:
            progress_score = 0

        return (ease_score * 0.4 + again_score * 0.3 + progress_score * 0.3)

    def _calculate_test_score(self, metrics: LearningMetrics) -> float:
        """Calculate score based on test performance."""
        if metrics.total_tests == 0:
            return 50.0  # Neutral if no tests

        # Average test score is primary indicator
        score = metrics.avg_test_score

        # Bonus for pass rate
        if metrics.total_tests > 0:
            pass_rate = metrics.tests_passed / metrics.total_tests
            score = score * 0.8 + pass_rate * 100 * 0.2

        return min(100, score)

    def _calculate_consistency_score(self, metrics: LearningMetrics) -> float:
        """Calculate score based on study consistency."""
        score = 0.0

        # Days active (max 30 days)
        if metrics.days_active > 0:
            score += min(50, metrics.days_active / 30 * 50)

        # Streak bonus
        if metrics.streak_days > 0:
            score += min(30, metrics.streak_days * 3)

        # Study time bonus (aim for 10+ hours)
        if metrics.study_time_hours > 0:
            score += min(20, metrics.study_time_hours / 10 * 20)

        return min(100, score)

    def _calculate_weak_areas_score(self, metrics: LearningMetrics) -> float:
        """Calculate score based on weak areas (fewer = better)."""
        # Start at 100, penalize for weak areas
        score = 100.0

        # Critical areas hurt more
        weak_areas = self.ai_store.get_weak_areas(limit=10)
        critical_count = len([a for a in weak_areas if a.priority == Priority.CRITICAL])
        high_count = len([a for a in weak_areas if a.priority == Priority.HIGH])

        score -= critical_count * 15
        score -= high_count * 8
        score -= max(0, len(weak_areas) - critical_count - high_count) * 3

        return max(0, score)

    def _determine_level(self, score: float) -> str:
        """Determine preparedness level from score."""
        if score >= 80:
            return "ready"
        elif score >= 60:
            return "advanced"
        elif score >= 40:
            return "intermediate"
        else:
            return "beginner"

    def _calculate_confidence(self, metrics: LearningMetrics) -> float:
        """Calculate confidence in prediction based on data availability."""
        confidence = 0.0

        # More data = higher confidence
        if metrics.total_reviews >= 50:
            confidence += 0.3
        elif metrics.total_reviews >= 20:
            confidence += 0.2
        elif metrics.total_reviews >= 5:
            confidence += 0.1

        if metrics.total_tests >= 5:
            confidence += 0.3
        elif metrics.total_tests >= 2:
            confidence += 0.2
        elif metrics.total_tests >= 1:
            confidence += 0.1

        if metrics.days_active >= 14:
            confidence += 0.2
        elif metrics.days_active >= 7:
            confidence += 0.1

        if metrics.study_time_hours >= 5:
            confidence += 0.2
        elif metrics.study_time_hours >= 2:
            confidence += 0.1

        return min(1.0, confidence)

    def _get_weak_area_names(self) -> List[str]:
        """Get list of weak area names."""
        areas = self.ai_store.get_weak_areas(limit=10)
        return [f"Tema {a.tema}" if a.tema else a.apartado for a in areas if a.priority in [Priority.CRITICAL, Priority.HIGH]]

    def _get_strong_area_names(self, metrics: LearningMetrics, test_score: float) -> List[str]:
        """Get list of strong area names."""
        # If test score is good, some areas must be strong
        if test_score >= 70:
            return ["General knowledge", "Test-taking skills"]
        elif test_score >= 60:
            return ["Basic concepts"]
        return []

    def _estimate_days_to_ready(self, score: float, metrics: LearningMetrics) -> Optional[int]:
        """Estimate days until ready for exam."""
        if score >= 80:
            return 0  # Already ready

        # Calculate improvement needed
        improvement_needed = 80 - score

        # Estimate based on study pace
        if metrics.study_time_hours > 0 and metrics.days_active > 0:
            hours_per_day = metrics.study_time_hours / metrics.days_active
            # Assume 5% improvement per study hour
            hours_needed = improvement_needed / 5
            days = int(hours_needed / max(hours_per_day, 0.5))
            return min(180, max(7, days))

        # Default estimate: 2 points per day of study
        return min(180, max(7, int(improvement_needed / 2)))

    def _recommend_study_hours(self, score: float, metrics: LearningMetrics) -> float:
        """Recommend weekly study hours."""
        if score >= 80:
            return 5.0  # Maintenance
        elif score >= 60:
            return 10.0
        elif score >= 40:
            return 15.0
        else:
            return 20.0

    def _enhance_with_llm(self, prediction: PreparednessPrediction, metrics: LearningMetrics) -> PreparednessPrediction:
        """Enhance prediction with LLM insights."""
        prompt = f"""Analyze the following learning data and provide insights for exam preparedness.

Metrics:
- Total flashcards: {metrics.total_flashcards}
- Flashcards learned: {metrics.flashcards_learned}
- Average ease factor: {metrics.avg_ease_factor}
- Total reviews: {metrics.total_reviews}
- Again rate: {metrics.again_rate}%
- Total tests: {metrics.total_tests}
- Tests passed: {metrics.tests_passed}
- Average test score: {metrics.avg_test_score}%
- Study hours: {metrics.study_time_hours}
- Days active: {metrics.days_active}
- Streak: {metrics.streak_days} days
- Weak areas count: {metrics.weak_areas_count}

Current calculated score: {prediction.overall_score}%
Level: {prediction.level}
Weak areas: {', '.join(prediction.weak_areas)}

Return JSON with:
{{
    "adjusted_score": <float 0-100>,
    "confidence": <float 0-1>,
    "key_insights": [<list of 2-3 key insights>],
    "study_suggestions": [<list of 2-3 actionable suggestions>],
    "motivation_message": <encouraging message based on progress>
}}
"""

        try:
            response = self.llm.generate(prompt, temperature=0.3)

            # Parse JSON from response
            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start >= 0 and json_end > json_start:
                data = json.loads(response[json_start:json_end])

                # Update prediction with LLM insights
                if "adjusted_score" in data:
                    # Weight LLM adjustment 30%, our calculation 70%
                    prediction.overall_score = round(
                        prediction.overall_score * 0.7 + data["adjusted_score"] * 0.3, 1
                    )
                    prediction.level = self._determine_level(prediction.overall_score)

                if "confidence" in data:
                    prediction.confidence = round(
                        prediction.confidence * 0.5 + data["confidence"] * 0.5, 2
                    )

                if "key_insights" in data:
                    prediction.factors["llm_insights"] = data["key_insights"]

                if "study_suggestions" in data:
                    prediction.factors["llm_suggestions"] = data["study_suggestions"]

                if "motivation_message" in data:
                    prediction.factors["motivation"] = data["motivation_message"]

        except Exception as e:
            logger.warning(f"LLM enhancement failed: {e}")

        return prediction

    def get_trend(self, days: int = 30) -> dict:
        """
        Get prediction trend over time.

        Args:
            days: Number of days to analyze

        Returns:
            Trend analysis dict
        """
        # Get recent predictions
        # For now, return basic trend based on test scores
        if self.analyzer.test_store:
            results = self.analyzer.test_store.list_results(limit=50)

            if len(results) >= 2:
                recent_scores = [r.score_percentage for r in results[:10]]
                older_scores = [r.score_percentage for r in results[10:20]] if len(results) >= 20 else []

                recent_avg = sum(recent_scores) / len(recent_scores)
                older_avg = sum(older_scores) / len(older_scores) if older_scores else recent_avg

                if recent_avg > older_avg + 5:
                    trend = "improving"
                elif recent_avg < older_avg - 5:
                    trend = "declining"
                else:
                    trend = "stable"

                return {
                    "trend": trend,
                    "recent_average": round(recent_avg, 1),
                    "older_average": round(older_avg, 1) if older_scores else None,
                    "improvement": round(recent_avg - older_avg, 1),
                }

        return {"trend": "insufficient_data"}
