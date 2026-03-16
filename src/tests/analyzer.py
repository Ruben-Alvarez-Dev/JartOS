"""
Test Analyzer - Analysis and insights from test results.

Provides statistics, weak area identification, and progress tracking.
"""

from datetime import datetime, timedelta
from typing import Optional
from collections import defaultdict

from .models import TestResult, TestSession
from .store import TestStore


class TestAnalyzer:
    """Analyzes test results and provides insights."""

    def __init__(self, store: TestStore):
        """
        Initialize test analyzer.

        Args:
            store: TestStore instance
        """
        self.store = store

    def analyze_session(self, session_id: str) -> dict:
        """
        Analyze a specific session in detail.

        Args:
            session_id: Session ID to analyze

        Returns:
            Detailed analysis dict
        """
        session = self.store.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")

        result = self.store.get_result(session_id)
        if not result:
            raise ValueError(f"Result not found for session: {session_id}")

        test = self.store.get_test(session.test_id)
        if not test:
            raise ValueError(f"Test not found: {session.test_id}")

        # Build detailed analysis
        question_analysis = []
        for question in test.questions:
            answer = session.answers.get(question.id)
            if answer:
                question_analysis.append({
                    "question_id": question.id,
                    "question_text": question.text[:100] + "..." if len(question.text) > 100 else question.text,
                    "is_correct": answer.is_correct,
                    "time_spent": answer.time_spent_seconds,
                    "difficulty": question.difficulty,
                })

        return {
            "session_id": session_id,
            "test_title": test.title,
            "score": result.score_percentage,
            "passed": result.passed,
            "total_questions": result.total_questions,
            "correct": result.correct_answers,
            "incorrect": result.incorrect_answers,
            "unanswered": result.unanswered,
            "time_spent_seconds": result.time_spent_seconds,
            "avg_time_per_question": result.time_spent_seconds / result.total_questions if result.total_questions > 0 else 0,
            "weak_areas": result.weak_areas,
            "strong_areas": result.strong_areas,
            "recommendations": result.recommendations,
            "questions": question_analysis,
            "date": session.completed_at.isoformat() if session.completed_at else None,
        }

    def get_weak_areas(self, limit: int = 5) -> list[dict]:
        """
        Get weak areas across all tests.

        Args:
            limit: Maximum number of weak areas to return

        Returns:
            List of weak areas with statistics
        """
        results = self.store.list_results(limit=100)

        # Aggregate by source/tema
        area_stats = defaultdict(lambda: {"correct": 0, "total": 0})

        for result in results:
            # Use weak_areas from results
            for area in result.weak_areas:
                area_stats[area]["total"] += 1

            # Also track strong areas for context
            for area in result.strong_areas:
                if area not in area_stats:
                    area_stats[area]["correct"] = 1
                    area_stats[area]["total"] = 1
                else:
                    area_stats[area]["correct"] += 1

        # Calculate percentages and sort
        weak_areas = []
        for area, stats in area_stats.items():
            pct = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            weak_areas.append({
                "area": area,
                "score_percentage": round(pct, 1),
                "times_tested": stats["total"],
                "needs_review": pct < 60,
            })

        # Sort by score (lowest first)
        weak_areas.sort(key=lambda x: x["score_percentage"])

        return weak_areas[:limit]

    def get_progress_stats(self, days: int = 30) -> dict:
        """
        Get progress statistics over time.

        Args:
            days: Number of days to analyze

        Returns:
            Progress statistics dict
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        results = self.store.list_results(limit=200)

        # Filter by date
        recent_results = [
            r for r in results
            if r.created_at >= cutoff_date
        ]

        if not recent_results:
            return {
                "period_days": days,
                "tests_taken": 0,
                "average_score": 0,
                "pass_rate": 0,
                "total_time_hours": 0,
                "trend": "no_data",
            }

        # Calculate statistics
        scores = [r.score_percentage for r in recent_results]
        passed_count = sum(1 for r in recent_results if r.passed)
        total_time = sum(r.time_spent_seconds for r in recent_results)

        # Calculate trend
        if len(recent_results) >= 2:
            first_half = recent_results[:len(recent_results)//2]
            second_half = recent_results[len(recent_results)//2:]

            first_avg = sum(r.score_percentage for r in first_half) / len(first_half)
            second_avg = sum(r.score_percentage for r in second_half) / len(second_half)

            if second_avg > first_avg + 5:
                trend = "improving"
            elif second_avg < first_avg - 5:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        return {
            "period_days": days,
            "tests_taken": len(recent_results),
            "average_score": round(sum(scores) / len(scores), 1),
            "min_score": round(min(scores), 1),
            "max_score": round(max(scores), 1),
            "pass_rate": round(passed_count / len(recent_results) * 100, 1),
            "total_time_hours": round(total_time / 3600, 2),
            "trend": trend,
        }

    def get_test_history(self, test_id: Optional[str] = None, limit: int = 10) -> list[dict]:
        """
        Get history of test attempts.

        Args:
            test_id: Filter by test ID (optional)
            limit: Maximum results to return

        Returns:
            List of test attempt summaries
        """
        results = self.store.list_results(test_id=test_id, limit=limit)

        history = []
        for result in results:
            test = self.store.get_test(result.test_id)
            session = self.store.get_session(result.session_id)

            history.append({
                "session_id": result.session_id,
                "test_id": result.test_id,
                "test_title": test.title if test else "Unknown",
                "score": result.score_percentage,
                "passed": result.passed,
                "total_questions": result.total_questions,
                "correct": result.correct_answers,
                "time_spent_minutes": round(result.time_spent_seconds / 60, 1),
                "date": session.completed_at.isoformat() if session and session.completed_at else None,
            })

        return history

    def get_study_recommendations(self) -> list[dict]:
        """
        Get personalized study recommendations based on test history.

        Returns:
            List of recommendations
        """
        recommendations = []

        # Get weak areas
        weak_areas = self.get_weak_areas()
        if weak_areas:
            priority_area = weak_areas[0]
            recommendations.append({
                "type": "weak_area",
                "priority": "high",
                "area": priority_area["area"],
                "message": f"Focus on '{priority_area['area']}' - current score: {priority_area['score_percentage']}%",
                "action": f"Generate a test focused on {priority_area['area']} for practice",
            })

        # Get progress stats
        stats = self.get_progress_stats(days=30)

        if stats["tests_taken"] == 0:
            recommendations.append({
                "type": "engagement",
                "priority": "medium",
                "message": "No tests taken in the last 30 days",
                "action": "Take a test to track your progress",
            })
        elif stats["trend"] == "declining":
            recommendations.append({
                "type": "trend",
                "priority": "high",
                "message": f"Scores are declining (avg: {stats['average_score']}%)",
                "action": "Review weak areas and consider restudying the material",
            })
        elif stats["trend"] == "improving":
            recommendations.append({
                "type": "encouragement",
                "priority": "low",
                "message": f"Great progress! Average score: {stats['average_score']}%",
                "action": "Keep up the good work!",
            })

        # Time-based recommendations
        if stats["total_time_hours"] < 1:
            recommendations.append({
                "type": "time",
                "priority": "medium",
                "message": f"Only {stats['total_time_hours']:.1f} hours of testing in the last 30 days",
                "action": "Aim for at least 2-3 hours per week of practice",
            })

        return recommendations

    def compare_sessions(self, session_id_1: str, session_id_2: str) -> dict:
        """
        Compare two test sessions.

        Args:
            session_id_1: First session ID
            session_id_2: Second session ID

        Returns:
            Comparison dict
        """
        result1 = self.store.get_result(session_id_1)
        result2 = self.store.get_result(session_id_2)

        if not result1 or not result2:
            raise ValueError("One or both sessions not found")

        return {
            "session_1": {
                "id": session_id_1,
                "score": result1.score_percentage,
                "correct": result1.correct_answers,
                "time": result1.time_spent_seconds,
            },
            "session_2": {
                "id": session_id_2,
                "score": result2.score_percentage,
                "correct": result2.correct_answers,
                "time": result2.time_spent_seconds,
            },
            "score_improvement": round(result2.score_percentage - result1.score_percentage, 1),
            "time_difference": round(result2.time_spent_seconds - result1.time_spent_seconds, 1),
            "improved": result2.score_percentage > result1.score_percentage,
        }
