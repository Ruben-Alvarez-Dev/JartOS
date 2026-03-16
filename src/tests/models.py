"""
Test Generator Data Models

Defines dataclasses for tests, questions, sessions, and results.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class QuestionType(Enum):
    """Supported question types."""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    OPEN_ENDED = "open_ended"


class TestMode(Enum):
    """Test taking modes."""
    PRACTICE = "practice"  # Show feedback after each answer
    EXAM = "exam"  # No feedback until complete


@dataclass
class TestConfig:
    """Configuration for test generation."""
    question_count: int = 10
    question_types: list[QuestionType] = field(default_factory=lambda: [QuestionType.MULTIPLE_CHOICE])
    difficulty: str = "medium"  # easy, medium, hard
    temas: list[str] = field(default_factory=list)
    mode: TestMode = TestMode.PRACTICE
    time_limit_minutes: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "question_count": self.question_count,
            "question_types": [qt.value for qt in self.question_types],
            "difficulty": self.difficulty,
            "temas": self.temas,
            "mode": self.mode.value,
            "time_limit_minutes": self.time_limit_minutes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TestConfig":
        return cls(
            question_count=data.get("question_count", 10),
            question_types=[QuestionType(qt) for qt in data.get("question_types", ["multiple_choice"])],
            difficulty=data.get("difficulty", "medium"),
            temas=data.get("temas", []),
            mode=TestMode(data.get("mode", "practice")),
            time_limit_minutes=data.get("time_limit_minutes"),
        )


@dataclass
class Question:
    """A single question in a test."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    test_id: str = ""
    question_type: QuestionType = QuestionType.MULTIPLE_CHOICE
    text: str = ""
    options: list[str] = field(default_factory=list)  # For multiple choice
    correct_index: int = 0  # Index of correct answer
    explanation: str = ""
    difficulty: str = "medium"
    source_chunk_ids: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "test_id": self.test_id,
            "question_type": self.question_type.value,
            "text": self.text,
            "options": self.options,
            "correct_index": self.correct_index,
            "explanation": self.explanation,
            "difficulty": self.difficulty,
            "source_chunk_ids": self.source_chunk_ids,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Question":
        return cls(
            id=data.get("id", str(uuid.uuid4())[:8]),
            test_id=data.get("test_id", ""),
            question_type=QuestionType(data.get("question_type", "multiple_choice")),
            text=data.get("text", ""),
            options=data.get("options", []),
            correct_index=data.get("correct_index", 0),
            explanation=data.get("explanation", ""),
            difficulty=data.get("difficulty", "medium"),
            source_chunk_ids=data.get("source_chunk_ids", []),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
        )

    def check_answer(self, answer_index: int) -> bool:
        """Check if the given answer index is correct."""
        return answer_index == self.correct_index


@dataclass
class Test:
    """A test containing multiple questions."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    config: TestConfig = field(default_factory=TestConfig)
    questions: list[Question] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "config": self.config.to_dict(),
            "questions": [q.to_dict() for q in self.questions],
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Test":
        return cls(
            id=data.get("id", str(uuid.uuid4())[:8]),
            title=data.get("title", ""),
            description=data.get("description", ""),
            config=TestConfig.from_dict(data.get("config", {})),
            questions=[Question.from_dict(q) for q in data.get("questions", [])],
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
        )

    @property
    def question_count(self) -> int:
        return len(self.questions)


@dataclass
class SessionAnswer:
    """An answer submitted during a test session."""
    question_id: str
    answer_index: int
    is_correct: bool
    time_spent_seconds: float = 0.0
    answered_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "question_id": self.question_id,
            "answer_index": self.answer_index,
            "is_correct": self.is_correct,
            "time_spent_seconds": self.time_spent_seconds,
            "answered_at": self.answered_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SessionAnswer":
        return cls(
            question_id=data["question_id"],
            answer_index=data["answer_index"],
            is_correct=data["is_correct"],
            time_spent_seconds=data.get("time_spent_seconds", 0.0),
            answered_at=datetime.fromisoformat(data["answered_at"]) if "answered_at" in data else datetime.now(),
        )


@dataclass
class TestSession:
    """A test taking session."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    test_id: str = ""
    status: str = "in_progress"  # in_progress, completed, abandoned
    answers: dict[str, SessionAnswer] = field(default_factory=dict)  # question_id -> answer
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    current_question_index: int = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "test_id": self.test_id,
            "status": self.status,
            "answers": {qid: a.to_dict() for qid, a in self.answers.items()},
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "current_question_index": self.current_question_index,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TestSession":
        return cls(
            id=data.get("id", str(uuid.uuid4())[:8]),
            test_id=data.get("test_id", ""),
            status=data.get("status", "in_progress"),
            answers={qid: SessionAnswer.from_dict(a) for qid, a in data.get("answers", {}).items()},
            started_at=datetime.fromisoformat(data["started_at"]) if "started_at" in data else datetime.now(),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
            current_question_index=data.get("current_question_index", 0),
        )

    def record_answer(self, question_id: str, answer_index: int, is_correct: bool, time_spent: float = 0.0):
        """Record an answer for a question."""
        self.answers[question_id] = SessionAnswer(
            question_id=question_id,
            answer_index=answer_index,
            is_correct=is_correct,
            time_spent_seconds=time_spent,
        )

    def complete(self):
        """Mark session as completed."""
        self.status = "completed"
        self.completed_at = datetime.now()


@dataclass
class TestResult:
    """Analysis results from a completed test session."""
    session_id: str = ""
    test_id: str = ""
    total_questions: int = 0
    correct_answers: int = 0
    incorrect_answers: int = 0
    unanswered: int = 0
    score_percentage: float = 0.0
    time_spent_seconds: float = 0.0
    weak_areas: list[str] = field(default_factory=list)  # Topics needing review
    strong_areas: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "test_id": self.test_id,
            "total_questions": self.total_questions,
            "correct_answers": self.correct_answers,
            "incorrect_answers": self.incorrect_answers,
            "unanswered": self.unanswered,
            "score_percentage": self.score_percentage,
            "time_spent_seconds": self.time_spent_seconds,
            "weak_areas": self.weak_areas,
            "strong_areas": self.strong_areas,
            "recommendations": self.recommendations,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TestResult":
        return cls(
            session_id=data.get("session_id", ""),
            test_id=data.get("test_id", ""),
            total_questions=data.get("total_questions", 0),
            correct_answers=data.get("correct_answers", 0),
            incorrect_answers=data.get("incorrect_answers", 0),
            unanswered=data.get("unanswered", 0),
            score_percentage=data.get("score_percentage", 0.0),
            time_spent_seconds=data.get("time_spent_seconds", 0.0),
            weak_areas=data.get("weak_areas", []),
            strong_areas=data.get("strong_areas", []),
            recommendations=data.get("recommendations", []),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
        )

    @property
    def passed(self) -> bool:
        """Check if the test was passed (>=60%)."""
        return self.score_percentage >= 60.0
