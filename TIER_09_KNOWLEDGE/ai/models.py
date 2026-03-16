"""
Data models for AI analytics and recommendations.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class Priority(str, Enum):
    """Priority levels for recommendations."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class StudyGoal(str, Enum):
    """Study goal types."""
    WEAK_AREA_IMPROVEMENT = "weak_area_improvement"
    NEW_CONTENT = "new_content"
    REVIEW = "review"
    PRACTICE_TEST = "practice_test"


@dataclass
class WeakArea:
    """Represents an identified weak area."""
    id: Optional[int] = None
    tema: str = ""
    apartado: str = ""
    source: str = ""  # "flashcards", "tests", "combined"
    flashcard_ease_avg: float = 2.5
    test_score_avg: float = 0.0
    combined_score: float = 0.0  # Weighted combination
    cards_affected: int = 0
    tests_affected: int = 0
    priority: Priority = Priority.MEDIUM
    created_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tema": self.tema,
            "apartado": self.apartado,
            "source": self.source,
            "flashcard_ease_avg": self.flashcard_ease_avg,
            "test_score_avg": self.test_score_avg,
            "combined_score": self.combined_score,
            "cards_affected": self.cards_affected,
            "tests_affected": self.tests_affected,
            "priority": self.priority.value,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WeakArea":
        return cls(
            id=data.get("id"),
            tema=data.get("tema", ""),
            apartado=data.get("apartado", ""),
            source=data.get("source", ""),
            flashcard_ease_avg=data.get("flashcard_ease_avg", 2.5),
            test_score_avg=data.get("test_score_avg", 0.0),
            combined_score=data.get("combined_score", 0.0),
            cards_affected=data.get("cards_affected", 0),
            tests_affected=data.get("tests_affected", 0),
            priority=Priority(data.get("priority", "medium")),
            created_at=data.get("created_at"),
        )


@dataclass
class LearningMetrics:
    """Aggregated learning metrics."""
    total_flashcards: int = 0
    flashcards_learned: int = 0
    flashcards_new: int = 0
    avg_ease_factor: float = 2.5
    total_reviews: int = 0
    again_rate: float = 0.0  # Percentage of "again" ratings

    total_tests: int = 0
    tests_passed: int = 0
    avg_test_score: float = 0.0
    weak_areas_count: int = 0

    study_time_hours: float = 0.0
    days_active: int = 0
    streak_days: int = 0

    def to_dict(self) -> dict:
        return {
            "total_flashcards": self.total_flashcards,
            "flashcards_learned": self.flashcards_learned,
            "flashcards_new": self.flashcards_new,
            "avg_ease_factor": self.avg_ease_factor,
            "total_reviews": self.total_reviews,
            "again_rate": self.again_rate,
            "total_tests": self.total_tests,
            "tests_passed": self.tests_passed,
            "avg_test_score": self.avg_test_score,
            "weak_areas_count": self.weak_areas_count,
            "study_time_hours": self.study_time_hours,
            "days_active": self.days_active,
            "streak_days": self.streak_days,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LearningMetrics":
        return cls(
            total_flashcards=data.get("total_flashcards", 0),
            flashcards_learned=data.get("flashcards_learned", 0),
            flashcards_new=data.get("flashcards_new", 0),
            avg_ease_factor=data.get("avg_ease_factor", 2.5),
            total_reviews=data.get("total_reviews", 0),
            again_rate=data.get("again_rate", 0.0),
            total_tests=data.get("total_tests", 0),
            tests_passed=data.get("tests_passed", 0),
            avg_test_score=data.get("avg_test_score", 0.0),
            weak_areas_count=data.get("weak_areas_count", 0),
            study_time_hours=data.get("study_time_hours", 0.0),
            days_active=data.get("days_active", 0),
            streak_days=data.get("streak_days", 0),
        )


@dataclass
class PreparednessPrediction:
    """Predicted preparedness level."""
    id: Optional[int] = None
    overall_score: float = 0.0  # 0-100%
    confidence: float = 0.0  # Confidence in prediction
    level: str = "beginner"  # beginner, intermediate, advanced, ready
    weak_areas: List[str] = field(default_factory=list)
    strong_areas: List[str] = field(default_factory=list)
    recommended_hours_per_week: float = 10.0
    estimated_days_to_ready: Optional[int] = None
    factors: dict = field(default_factory=dict)  # What influenced prediction
    created_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "overall_score": self.overall_score,
            "confidence": self.confidence,
            "level": self.level,
            "weak_areas": self.weak_areas,
            "strong_areas": self.strong_areas,
            "recommended_hours_per_week": self.recommended_hours_per_week,
            "estimated_days_to_ready": self.estimated_days_to_ready,
            "factors": self.factors,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PreparednessPrediction":
        return cls(
            id=data.get("id"),
            overall_score=data.get("overall_score", 0.0),
            confidence=data.get("confidence", 0.0),
            level=data.get("level", "beginner"),
            weak_areas=data.get("weak_areas", []),
            strong_areas=data.get("strong_areas", []),
            recommended_hours_per_week=data.get("recommended_hours_per_week", 10.0),
            estimated_days_to_ready=data.get("estimated_days_to_ready"),
            factors=data.get("factors", {}),
            created_at=data.get("created_at"),
        )


@dataclass
class StudyTask:
    """A single study task."""
    id: str = ""
    description: str = ""
    type: StudyGoal = StudyGoal.REVIEW
    tema: Optional[str] = None
    duration_minutes: int = 30
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    completed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "type": self.type.value,
            "tema": self.tema,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority.value,
            "completed": self.completed,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StudyTask":
        return cls(
            id=data.get("id", ""),
            description=data.get("description", ""),
            type=StudyGoal(data.get("type", "review")),
            tema=data.get("tema"),
            duration_minutes=data.get("duration_minutes", 30),
            priority=Priority(data.get("priority", "medium")),
            completed=data.get("completed", False),
            completed_at=data.get("completed_at"),
        )


@dataclass
class StudyPlan:
    """Weekly study plan."""
    id: Optional[int] = None
    week_start: str = ""  # ISO date
    week_end: str = ""
    total_hours: float = 0.0
    goals: List[str] = field(default_factory=list)
    tasks: List[StudyTask] = field(default_factory=list)
    daily_breakdown: dict = field(default_factory=dict)  # day -> tasks
    focus_areas: List[str] = field(default_factory=list)
    generated_by: str = "ai"  # "ai" or "manual"
    created_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "week_start": self.week_start,
            "week_end": self.week_end,
            "total_hours": self.total_hours,
            "goals": self.goals,
            "tasks": [t.to_dict() for t in self.tasks],
            "daily_breakdown": {k: [t.to_dict() for t in v] for k, v in self.daily_breakdown.items()},
            "focus_areas": self.focus_areas,
            "generated_by": self.generated_by,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StudyPlan":
        tasks = [StudyTask.from_dict(t) for t in data.get("tasks", [])]
        daily_breakdown = {
            k: [StudyTask.from_dict(t) for t in v]
            for k, v in data.get("daily_breakdown", {}).items()
        }
        return cls(
            id=data.get("id"),
            week_start=data.get("week_start", ""),
            week_end=data.get("week_end", ""),
            total_hours=data.get("total_hours", 0.0),
            goals=data.get("goals", []),
            tasks=tasks,
            daily_breakdown=daily_breakdown,
            focus_areas=data.get("focus_areas", []),
            generated_by=data.get("generated_by", "ai"),
            created_at=data.get("created_at"),
        )


@dataclass
class DailyRecommendation:
    """Daily study recommendation."""
    id: Optional[int] = None
    date: str = ""  # ISO date
    priority: Priority = Priority.MEDIUM
    type: str = ""  # "flashcard_review", "test", "new_content", "weak_area"
    title: str = ""
    description: str = ""
    action: str = ""  # Specific action to take
    target_id: Optional[str] = None  # ID of deck, test, etc.
    estimated_minutes: int = 15
    reason: str = ""  # Why this recommendation
    completed: bool = False
    created_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date,
            "priority": self.priority.value,
            "type": self.type,
            "title": self.title,
            "description": self.description,
            "action": self.action,
            "target_id": self.target_id,
            "estimated_minutes": self.estimated_minutes,
            "reason": self.reason,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DailyRecommendation":
        return cls(
            id=data.get("id"),
            date=data.get("date", ""),
            priority=Priority(data.get("priority", "medium")),
            type=data.get("type", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            action=data.get("action", ""),
            target_id=data.get("target_id"),
            estimated_minutes=data.get("estimated_minutes", 15),
            reason=data.get("reason", ""),
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
        )
