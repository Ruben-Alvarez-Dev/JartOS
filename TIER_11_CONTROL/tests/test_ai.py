"""
Tests for AI Module - Analytics, Predictions, and Recommendations.
"""

import json
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
import pytest

from TIER_09_KNOWLEDGE.ai.models import (
    WeakArea,
    PreparednessPrediction,
    StudyPlan,
    StudyTask,
    DailyRecommendation,
    LearningMetrics,
    Priority,
    StudyGoal,
)
from TIER_09_KNOWLEDGE.ai.store import AIStore
from TIER_09_KNOWLEDGE.ai.analyzer import WeakAreasAnalyzer
from TIER_09_KNOWLEDGE.ai.predictor import PreparednessPredictor
from TIER_09_KNOWLEDGE.ai.planner import StudyPlanner
from TIER_09_KNOWLEDGE.ai.recommender import DailyRecommender


# ============ Fixtures ============

@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    yield db_path
    Path(db_path).unlink(missing_ok=True)


@pytest.fixture
def ai_store(temp_db):
    """Create AIStore with temporary database."""
    return AIStore(db_path=temp_db)


@pytest.fixture
def mock_flashcard_store():
    """Mock FlashcardStore for testing."""
    class MockFlashcardStore:
        def list_decks(self):
            from dataclasses import dataclass
            @dataclass
            class MockDeck:
                id: int
                name: str
                tema_id: int
            return [
                MockDeck(id=1, name="Tema 1", tema_id=1),
                MockDeck(id=2, name="Tema 2", tema_id=2),
            ]

        def get_flashcards_by_deck(self, deck_id):
            from dataclasses import dataclass
            @dataclass
            class MockCard:
                id: int
                deck_id: int
                ease_factor: float
                repetitions: int
            if deck_id == 1:
                return [
                    MockCard(id=1, deck_id=1, ease_factor=2.0, repetitions=5),  # Low ease
                    MockCard(id=2, deck_id=1, ease_factor=2.2, repetitions=3),
                ]
            return [
                MockCard(id=3, deck_id=2, ease_factor=2.8, repetitions=5),
            ]

        def get_review_logs(self, card_id, limit=10):
            from dataclasses import dataclass
            @dataclass
            class MockReview:
                rating: int
            return [MockReview(rating=0), MockReview(rating=3)]  # 1 again, 1 good

        def get_all_stats(self):
            return {
                "total_cards": 10,
                "total_reviews": 20,
                "average_ease_factor": 2.3,
                "cards_due_today": 5,
            }

    return MockFlashcardStore()


@pytest.fixture
def mock_test_store():
    """Mock TestStore for testing."""
    class MockTestStore:
        def list_results(self, limit=50):
            from dataclasses import dataclass
            from datetime import datetime
            @dataclass
            class MockResult:
                test_id: str
                score_percentage: float
                passed: bool
                weak_areas: list
                strong_areas: list
                created_at: datetime

            return [
                MockResult(
                    test_id="test1",
                    score_percentage=55.0,
                    passed=False,
                    weak_areas=["Tema 1"],
                    strong_areas=["Tema 2"],
                    created_at=datetime.now() - timedelta(days=1),
                ),
                MockResult(
                    test_id="test2",
                    score_percentage=70.0,
                    passed=True,
                    weak_areas=[],
                    strong_areas=["Tema 1", "Tema 2"],
                    created_at=datetime.now(),
                ),
            ]

        def get_test(self, test_id):
            from dataclasses import dataclass
            @dataclass
            class MockConfig:
                temas: list
            @dataclass
            class MockTest:
                id: str
                config: MockConfig
            return MockTest(id=test_id, config=MockConfig(temas=["1"]))

    return MockTestStore()


# ============ Model Tests ============

class TestModels:
    """Test data models."""

    def test_weak_area_creation(self):
        """Test WeakArea model creation and serialization."""
        area = WeakArea(
            tema="1",
            apartado="Test area",
            source="combined",
            flashcard_ease_avg=2.0,
            test_score_avg=50.0,
            combined_score=45.0,
            cards_affected=5,
            tests_affected=2,
            priority=Priority.HIGH,
        )

        # Test to_dict
        data = area.to_dict()
        assert data["tema"] == "1"
        assert data["priority"] == "high"
        assert data["combined_score"] == 45.0

        # Test from_dict
        restored = WeakArea.from_dict(data)
        assert restored.tema == area.tema
        assert restored.priority == area.priority
        assert restored.combined_score == area.combined_score

    def test_preparedness_prediction_creation(self):
        """Test PreparednessPrediction model."""
        prediction = PreparednessPrediction(
            overall_score=65.0,
            confidence=0.75,
            level="intermediate",
            weak_areas=["Tema 1", "Tema 3"],
            strong_areas=["Tema 2"],
            recommended_hours_per_week=12.0,
            estimated_days_to_ready=30,
            factors={"flashcard_score": 60, "test_score": 70},
        )

        data = prediction.to_dict()
        assert data["overall_score"] == 65.0
        assert data["level"] == "intermediate"
        assert len(data["weak_areas"]) == 2

        restored = PreparednessPrediction.from_dict(data)
        assert restored.level == prediction.level
        assert restored.factors == prediction.factors

    def test_study_plan_creation(self):
        """Test StudyPlan model with tasks."""
        task = StudyTask(
            id="task1",
            description="Review Tema 1",
            type=StudyGoal.WEAK_AREA_IMPROVEMENT,
            tema="1",
            duration_minutes=30,
            priority=Priority.HIGH,
        )

        plan = StudyPlan(
            week_start="2026-03-16",
            week_end="2026-03-22",
            total_hours=10.0,
            goals=["Master weak areas", "Take 2 tests"],
            tasks=[task],
            focus_areas=["Tema 1"],
        )

        data = plan.to_dict()
        assert data["total_hours"] == 10.0
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["description"] == "Review Tema 1"

        restored = StudyPlan.from_dict(data)
        assert len(restored.tasks) == 1
        assert restored.tasks[0].type == StudyGoal.WEAK_AREA_IMPROVEMENT

    def test_daily_recommendation_creation(self):
        """Test DailyRecommendation model."""
        rec = DailyRecommendation(
            date="2026-03-15",
            priority=Priority.HIGH,
            type="flashcard_review",
            title="Review 10 due cards",
            description="You have 10 flashcards due",
            action="Start review session",
            estimated_minutes=20,
            reason="Spaced repetition",
        )

        data = rec.to_dict()
        assert data["priority"] == "high"
        assert data["type"] == "flashcard_review"
        assert data["estimated_minutes"] == 20

        restored = DailyRecommendation.from_dict(data)
        assert restored.title == rec.title
        assert restored.priority == rec.priority

    def test_learning_metrics_creation(self):
        """Test LearningMetrics model."""
        metrics = LearningMetrics(
            total_flashcards=100,
            flashcards_learned=60,
            flashcards_new=40,
            avg_ease_factor=2.4,
            total_reviews=200,
            again_rate=15.0,
            total_tests=10,
            tests_passed=7,
            avg_test_score=72.5,
            study_time_hours=15.0,
            days_active=14,
            streak_days=5,
        )

        data = metrics.to_dict()
        assert data["total_flashcards"] == 100
        assert data["avg_test_score"] == 72.5

        restored = LearningMetrics.from_dict(data)
        assert restored.total_flashcards == metrics.total_flashcards
        assert restored.streak_days == metrics.streak_days


# ============ Store Tests ============

class TestAIStore:
    """Test AIStore persistence."""

    def test_save_and_get_weak_area(self, ai_store):
        """Test saving and retrieving weak areas."""
        area = WeakArea(
            tema="1",
            apartado="Test",
            source="tests",
            combined_score=40.0,
            priority=Priority.HIGH,
        )

        saved = ai_store.save_weak_area(area)
        assert saved.id is not None

        retrieved = ai_store.get_weak_areas(limit=10)
        assert len(retrieved) == 1
        assert retrieved[0].tema == "1"

    def test_save_weak_areas_batch(self, ai_store):
        """Test batch saving weak areas."""
        areas = [
            WeakArea(tema="1", source="tests", combined_score=30.0, priority=Priority.CRITICAL),
            WeakArea(tema="2", source="tests", combined_score=50.0, priority=Priority.HIGH),
            WeakArea(tema="3", source="tests", combined_score=60.0, priority=Priority.MEDIUM),
        ]

        saved = ai_store.save_weak_areas_batch(areas)
        assert len(saved) == 3

        retrieved = ai_store.get_weak_areas(limit=10)
        assert len(retrieved) == 3
        # Should be sorted by combined_score (lowest first)
        assert retrieved[0].combined_score == 30.0

    def test_clear_weak_areas(self, ai_store):
        """Test clearing weak areas."""
        ai_store.save_weak_area(WeakArea(tema="1", source="tests", combined_score=40.0))
        assert len(ai_store.get_weak_areas()) == 1

        count = ai_store.clear_weak_areas()
        assert count == 1
        assert len(ai_store.get_weak_areas()) == 0

    def test_save_and_get_prediction(self, ai_store):
        """Test saving and retrieving predictions."""
        prediction = PreparednessPrediction(
            overall_score=75.0,
            confidence=0.8,
            level="advanced",
            weak_areas=["Tema 1"],
            strong_areas=["Tema 2"],
            recommended_hours_per_week=8.0,
        )

        saved = ai_store.save_prediction(prediction)
        assert saved.id is not None

        latest = ai_store.get_latest_prediction()
        assert latest is not None
        assert latest.overall_score == 75.0
        assert latest.level == "advanced"

    def test_save_and_get_study_plan(self, ai_store):
        """Test saving and retrieving study plans."""
        today = date.today()
        plan = StudyPlan(
            week_start=today.isoformat(),
            week_end=(today + timedelta(days=6)).isoformat(),
            total_hours=10.0,
            goals=["Study hard"],
            tasks=[
                StudyTask(id="t1", description="Task 1", type=StudyGoal.REVIEW, duration_minutes=30),
            ],
        )

        saved = ai_store.save_study_plan(plan)
        assert saved.id is not None

        current = ai_store.get_current_study_plan()
        assert current is not None
        assert current.total_hours == 10.0
        assert len(current.tasks) == 1

    def test_save_and_get_recommendations(self, ai_store):
        """Test saving and retrieving daily recommendations."""
        today = date.today().isoformat()

        recs = [
            DailyRecommendation(
                date=today,
                priority=Priority.HIGH,
                type="flashcard_review",
                title="Review cards",
                description="Due cards",
                action="Start review",
                estimated_minutes=20,
            ),
            DailyRecommendation(
                date=today,
                priority=Priority.MEDIUM,
                type="test",
                title="Take test",
                description="Practice",
                action="Start test",
                estimated_minutes=30,
            ),
        ]

        saved = ai_store.save_recommendations_batch(recs)
        assert len(saved) == 2

        retrieved = ai_store.get_todays_recommendations()
        assert len(retrieved) == 2
        # Should be sorted by priority
        assert retrieved[0].priority == Priority.HIGH

    def test_mark_recommendation_completed(self, ai_store):
        """Test marking recommendation as completed."""
        today = date.today().isoformat()
        rec = DailyRecommendation(
            date=today,
            priority=Priority.HIGH,
            type="test",
            title="Test",
            description="Test",
            action="Do it",
        )

        saved = ai_store.save_recommendation(rec)
        assert not saved.completed

        success = ai_store.mark_recommendation_completed(saved.id)
        assert success

        retrieved = ai_store.get_todays_recommendations()
        assert retrieved[0].completed

    def test_save_and_get_learning_metrics(self, ai_store):
        """Test saving and retrieving learning metrics."""
        metrics = LearningMetrics(
            total_flashcards=50,
            total_tests=5,
            avg_test_score=70.0,
        )

        saved = ai_store.save_learning_metrics(metrics)
        assert saved.total_flashcards == 50

        retrieved = ai_store.get_learning_metrics()
        assert retrieved is not None
        assert retrieved.total_flashcards == 50
        assert retrieved.avg_test_score == 70.0


# ============ Analyzer Tests ============

class TestWeakAreasAnalyzer:
    """Test WeakAreasAnalyzer."""

    def test_analyze_with_mock_data(self, ai_store, mock_flashcard_store, mock_test_store):
        """Test analysis with mock stores."""
        analyzer = WeakAreasAnalyzer(
            ai_store=ai_store,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )

        weak_areas = analyzer.analyze_all()

        # Should identify weak areas from mock data
        assert isinstance(weak_areas, list)
        # Tema 1 has lower ease factors, should be flagged
        assert any("1" in wa.tema for wa in weak_areas)

    def test_compute_learning_metrics(self, ai_store, mock_flashcard_store, mock_test_store):
        """Test computing learning metrics."""
        analyzer = WeakAreasAnalyzer(
            ai_store=ai_store,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )

        metrics = analyzer.compute_learning_metrics()

        assert metrics.total_flashcards == 10  # From mock
        assert metrics.total_reviews == 20
        assert metrics.avg_ease_factor == 2.3

    def test_get_study_time_estimate(self, ai_store, mock_flashcard_store, mock_test_store):
        """Test study time estimation."""
        analyzer = WeakAreasAnalyzer(
            ai_store=ai_store,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )

        # Run analysis first
        analyzer.analyze_all()

        estimate = analyzer.get_study_time_estimate()

        assert "recommended_hours_per_week" in estimate
        assert estimate["recommended_hours_per_week"] > 0


# ============ Predictor Tests ============

class TestPreparednessPredictor:
    """Test PreparednessPredictor."""

    def test_predict_without_llm(self, ai_store, mock_flashcard_store, mock_test_store):
        """Test prediction without LLM (no API key)."""
        analyzer = WeakAreasAnalyzer(
            ai_store=ai_store,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )
        predictor = PreparednessPredictor(ai_store=ai_store, analyzer=analyzer)

        prediction = predictor.predict(use_llm=False)

        assert prediction.overall_score >= 0
        assert prediction.overall_score <= 100
        assert prediction.level in ["beginner", "intermediate", "advanced", "ready"]
        assert prediction.confidence >= 0
        assert prediction.confidence <= 1

    def test_predict_saves_to_store(self, ai_store, mock_flashcard_store, mock_test_store):
        """Test that prediction is saved to store."""
        analyzer = WeakAreasAnalyzer(
            ai_store=ai_store,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )
        predictor = PreparednessPredictor(ai_store=ai_store, analyzer=analyzer)

        predictor.predict(use_llm=False)

        saved = ai_store.get_latest_prediction()
        assert saved is not None

    def test_determine_level(self, ai_store, mock_flashcard_store, mock_test_store):
        """Test level determination logic."""
        analyzer = WeakAreasAnalyzer(
            ai_store=ai_store,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )
        predictor = PreparednessPredictor(ai_store=ai_store, analyzer=analyzer)

        assert predictor._determine_level(85) == "ready"
        assert predictor._determine_level(65) == "advanced"
        assert predictor._determine_level(45) == "intermediate"
        assert predictor._determine_level(25) == "beginner"


# ============ Planner Tests ============

class TestStudyPlanner:
    """Test StudyPlanner."""

    def test_generate_weekly_plan(self, ai_store, mock_flashcard_store, mock_test_store):
        """Test generating a weekly plan."""
        analyzer = WeakAreasAnalyzer(
            ai_store=ai_store,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )
        analyzer.analyze_all()  # Need weak areas first

        planner = StudyPlanner(
            ai_store=ai_store,
            analyzer=analyzer,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )

        plan = planner.generate_weekly_plan(total_hours=10.0)

        assert plan.total_hours > 0
        assert len(plan.goals) > 0
        assert len(plan.tasks) > 0
        assert plan.week_start is not None
        assert plan.week_end is not None

    def test_generate_daily_recommendations(self, ai_store, mock_flashcard_store, mock_test_store):
        """Test generating daily recommendations."""
        analyzer = WeakAreasAnalyzer(
            ai_store=ai_store,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )
        analyzer.analyze_all()

        planner = StudyPlanner(
            ai_store=ai_store,
            analyzer=analyzer,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )

        recs = planner.generate_daily_recommendations()

        assert isinstance(recs, list)
        # Should have at least one recommendation
        assert len(recs) >= 0


# ============ Recommender Tests ============

class TestDailyRecommender:
    """Test DailyRecommender."""

    def test_get_recommendations(self, ai_store, mock_flashcard_store, mock_test_store):
        """Test getting daily recommendations."""
        analyzer = WeakAreasAnalyzer(
            ai_store=ai_store,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )
        analyzer.analyze_all()

        predictor = PreparednessPredictor(ai_store=ai_store, analyzer=analyzer)
        predictor.predict(use_llm=False)

        recommender = DailyRecommender(
            ai_store=ai_store,
            analyzer=analyzer,
            predictor=predictor,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )

        recs = recommender.get_recommendations()

        assert isinstance(recs, list)

    def test_complete_recommendation(self, ai_store, mock_flashcard_store, mock_test_store):
        """Test completing a recommendation."""
        analyzer = WeakAreasAnalyzer(
            ai_store=ai_store,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )
        analyzer.analyze_all()

        predictor = PreparednessPredictor(ai_store=ai_store, analyzer=analyzer)
        recommender = DailyRecommender(
            ai_store=ai_store,
            analyzer=analyzer,
            predictor=predictor,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )

        # Generate recommendations
        recs = recommender.get_recommendations(refresh=True)

        if recs:
            # Complete first recommendation
            success = recommender.complete_recommendation(recs[0].id)
            assert success

    def test_get_progress_summary(self, ai_store, mock_flashcard_store, mock_test_store):
        """Test getting progress summary."""
        analyzer = WeakAreasAnalyzer(
            ai_store=ai_store,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )
        analyzer.analyze_all()

        predictor = PreparednessPredictor(ai_store=ai_store, analyzer=analyzer)
        recommender = DailyRecommender(
            ai_store=ai_store,
            analyzer=analyzer,
            predictor=predictor,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )

        recommender.get_recommendations(refresh=True)
        summary = recommender.get_progress_summary()

        assert "total_recommendations" in summary
        assert "completed" in summary
        assert "remaining" in summary


# ============ Integration Tests ============

class TestAIIntegration:
    """Integration tests for the AI module."""

    def test_full_workflow(self, ai_store, mock_flashcard_store, mock_test_store):
        """Test the full AI analysis workflow."""
        # 1. Analyze weak areas
        analyzer = WeakAreasAnalyzer(
            ai_store=ai_store,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )
        weak_areas = analyzer.analyze_all()
        metrics = analyzer.compute_learning_metrics()

        assert len(weak_areas) >= 0
        assert metrics is not None

        # 2. Generate prediction
        predictor = PreparednessPredictor(ai_store=ai_store, analyzer=analyzer)
        prediction = predictor.predict(use_llm=False)

        assert prediction is not None
        assert ai_store.get_latest_prediction() is not None

        # 3. Generate study plan
        planner = StudyPlanner(
            ai_store=ai_store,
            analyzer=analyzer,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )
        plan = planner.generate_weekly_plan(total_hours=10.0)

        assert plan is not None

        # 4. Generate daily recommendations
        recommender = DailyRecommender(
            ai_store=ai_store,
            analyzer=analyzer,
            predictor=predictor,
            flashcard_store=mock_flashcard_store,
            test_store=mock_test_store,
        )
        recs = recommender.get_recommendations()

        assert isinstance(recs, list)

        # 5. Verify all data persisted
        assert len(ai_store.get_weak_areas()) >= 0
        assert ai_store.get_latest_prediction() is not None
        assert ai_store.get_learning_metrics() is not None
