"""
Tests for the Test Generator module.

Tests cover:
- Models: Test, Question, TestSession, TestResult
- Store: CRUD operations
- Generator: Question generation
- Solver: Interactive sessions
- Analyzer: Results analysis
"""

import pytest
import tempfile
import os
from datetime import datetime
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from TIER_10_USER_APPS.tests.models import (
    Question,
    QuestionType,
    Test,
    TestConfig,
    TestMode,
    TestSession,
    SessionAnswer,
    TestResult,
)
from TIER_10_USER_APPS.tests.store import TestStore
from TIER_10_USER_APPS.tests.generator import TestGenerator, MiniMaxClient
from TIER_10_USER_APPS.tests.solver import TestSolver
from TIER_10_USER_APPS.tests.analyzer import TestAnalyzer


# ============ Model Tests ============

class TestModels:
    """Tests for data models."""

    def test_question_creation(self):
        """Test creating a question."""
        q = Question(
            question_type=QuestionType.MULTIPLE_CHOICE,
            text="What is 2 + 2?",
            options=["3", "4", "5", "6"],
            correct_index=1,
            explanation="Basic arithmetic",
        )

        assert q.question_type == QuestionType.MULTIPLE_CHOICE
        assert q.text == "What is 2 + 2?"
        assert len(q.options) == 4
        assert q.correct_index == 1
        assert q.id  # Auto-generated ID

    def test_question_check_answer(self):
        """Test answer checking."""
        q = Question(
            text="Question",
            options=["A", "B", "C", "D"],
            correct_index=2,
        )

        assert q.check_answer(2) is True
        assert q.check_answer(0) is False

    def test_question_serialization(self):
        """Test question to_dict and from_dict."""
        q = Question(
            id="q123",
            test_id="t456",
            question_type=QuestionType.TRUE_FALSE,
            text="Is Python interpreted?",
            options=["True", "False"],
            correct_index=0,
            explanation="Python is interpreted.",
            difficulty="easy",
            source_chunk_ids=["chunk1", "chunk2"],
        )

        # To dict
        data = q.to_dict()
        assert data["id"] == "q123"
        assert data["question_type"] == "true_false"
        assert data["correct_index"] == 0

        # From dict
        q2 = Question.from_dict(data)
        assert q2.id == q.id
        assert q2.question_type == q.question_type
        assert q2.text == q.text

    def test_test_config(self):
        """Test TestConfig."""
        config = TestConfig(
            question_count=20,
            question_types=[QuestionType.MULTIPLE_CHOICE, QuestionType.TRUE_FALSE],
            difficulty="hard",
            temas=["Tema 1", "Tema 2"],
            mode=TestMode.EXAM,
            time_limit_minutes=60,
        )

        data = config.to_dict()
        assert data["question_count"] == 20
        assert data["difficulty"] == "hard"
        assert data["mode"] == "exam"

        config2 = TestConfig.from_dict(data)
        assert config2.question_count == 20
        assert config2.mode == TestMode.EXAM

    def test_test_creation(self):
        """Test Test creation."""
        questions = [
            Question(text=f"Q{i}", options=["A", "B"], correct_index=0)
            for i in range(3)
        ]

        test = Test(
            id="test1",
            title="Sample Test",
            description="A sample test",
            config=TestConfig(question_count=3),
            questions=questions,
        )

        assert test.id == "test1"
        assert test.title == "Sample Test"
        assert test.question_count == 3

    def test_test_serialization(self):
        """Test Test serialization."""
        test = Test(
            id="test1",
            title="Test",
            config=TestConfig(question_count=5),
            questions=[Question(text="Q1", options=["A", "B"], correct_index=0)],
        )

        data = test.to_dict()
        assert data["id"] == "test1"
        assert len(data["questions"]) == 1

        test2 = Test.from_dict(data)
        assert test2.id == test.id
        assert len(test2.questions) == 1

    def test_session_answer(self):
        """Test SessionAnswer."""
        answer = SessionAnswer(
            question_id="q1",
            answer_index=1,
            is_correct=True,
            time_spent_seconds=5.5,
        )

        data = answer.to_dict()
        assert data["question_id"] == "q1"
        assert data["is_correct"] is True

        answer2 = SessionAnswer.from_dict(data)
        assert answer2.question_id == "q1"

    def test_test_session(self):
        """Test TestSession."""
        session = TestSession(
            id="sess1",
            test_id="test1",
        )

        session.record_answer("q1", 0, True, 3.0)
        session.record_answer("q2", 1, False, 5.0)

        assert len(session.answers) == 2
        assert session.answers["q1"].is_correct is True

        data = session.to_dict()
        session2 = TestSession.from_dict(data)
        assert len(session2.answers) == 2

    def test_test_result(self):
        """Test TestResult."""
        result = TestResult(
            session_id="sess1",
            test_id="test1",
            total_questions=10,
            correct_answers=7,
            incorrect_answers=2,
            unanswered=1,
            score_percentage=70.0,
            time_spent_seconds=300.0,
            weak_areas=["Topic A"],
            strong_areas=["Topic B"],
        )

        assert result.passed is True  # >= 60%
        assert result.incorrect_answers == 2

        data = result.to_dict()
        result2 = TestResult.from_dict(data)
        assert result2.score_percentage == 70.0


# ============ Store Tests ============

class TestStoreClass:
    """Tests for TestStore."""

    @pytest.fixture
    def store(self, tmp_path):
        """Create a temporary store for testing."""
        db_path = tmp_path / "test_tests.db"
        from TIER_10_USER_APPS.tests.store import TestStore as TS
        return TS(db_path=str(db_path))

    @pytest.fixture
    def sample_test(self):
        """Create a sample test."""
        return Test(
            id="test1",
            title="Sample Test",
            description="A test",
            config=TestConfig(question_count=2),
            questions=[
                Question(
                    id="q1",
                    test_id="test1",
                    text="Question 1",
                    options=["A", "B", "C", "D"],
                    correct_index=0,
                ),
                Question(
                    id="q2",
                    test_id="test1",
                    text="Question 2",
                    options=["A", "B", "C", "D"],
                    correct_index=2,
                ),
            ],
        )

    def test_save_and_get_test(self, store, sample_test):
        """Test saving and retrieving a test."""
        # Save
        assert store.save_test(sample_test) is True

        # Get
        retrieved = store.get_test("test1")
        assert retrieved is not None
        assert retrieved.id == "test1"
        assert retrieved.title == "Sample Test"
        assert len(retrieved.questions) == 2

    def test_list_tests(self, store, sample_test):
        """Test listing tests."""
        store.save_test(sample_test)

        tests = store.list_tests()
        assert len(tests) >= 1
        assert any(t.id == "test1" for t in tests)

    def test_delete_test(self, store, sample_test):
        """Test deleting a test."""
        store.save_test(sample_test)
        assert store.delete_test("test1") is True
        assert store.get_test("test1") is None

    def test_save_and_get_session(self, store, sample_test):
        """Test saving and retrieving a session."""
        store.save_test(sample_test)

        session = TestSession(id="sess1", test_id="test1")
        session.record_answer("q1", 0, True, 3.0)

        assert store.save_session(session) is True

        retrieved = store.get_session("sess1")
        assert retrieved is not None
        assert retrieved.test_id == "test1"
        assert len(retrieved.answers) == 1

    def test_save_and_get_result(self, store, sample_test):
        """Test saving and retrieving results."""
        store.save_test(sample_test)

        result = TestResult(
            session_id="sess1",
            test_id="test1",
            total_questions=2,
            correct_answers=1,
            incorrect_answers=1,
            unanswered=0,
            score_percentage=50.0,
            time_spent_seconds=60.0,
        )

        assert store.save_result(result) is True

        retrieved = store.get_result("sess1")
        assert retrieved is not None
        assert retrieved.score_percentage == 50.0

    def test_test_count(self, store, sample_test):
        """Test test count."""
        initial = store.get_test_count()
        store.save_test(sample_test)
        assert store.get_test_count() == initial + 1


# ============ Generator Tests ============

class TestGeneratorClass:
    """Tests for TestGenerator."""

    @pytest.fixture
    def mock_store(self, tmp_path):
        """Create a mock store."""
        from TIER_10_USER_APPS.tests.store import TestStore as TS
        return TS(db_path=str(tmp_path / "gen_tests.db"))

    @pytest.fixture
    def mock_temario_store(self):
        """Create a mock temario store."""
        class MockChunk:
            def __init__(self, id, content, tema, titulo):
                self.id = id
                self.content = content
                self.tema = tema
                self.titulo = titulo

        class MockTemarioStore:
            def list_chunks(self):
                return [
                    MockChunk("c1", "Content for tema 1", "1", "Intro"),
                    MockChunk("c2", "More content for tema 1", "1", "Details"),
                    MockChunk("c3", "Content for tema 2", "2", "Intro"),
                ]

            def get_chunk(self, chunk_id):
                for c in self.list_chunks():
                    if c.id == chunk_id:
                        return c
                return None

        return MockTemarioStore()

    def test_generator_initialization(self, mock_store, mock_temario_store):
        """Test generator initialization."""
        gen = TestGenerator(
            store=mock_store,
            temario_store=mock_temario_store,
        )
        assert gen.store is not None

    def test_generate_from_tema(self, mock_store, mock_temario_store):
        """Test generating test from tema."""
        gen = TestGenerator(
            store=mock_store,
            temario_store=mock_temario_store,
        )

        config = TestConfig(question_count=2)
        test = gen.generate_from_tema("1", config)

        assert test is not None
        assert test.id
        assert len(test.questions) == 2
        assert test.questions[0].test_id == test.id

    def test_generate_from_chunks(self, mock_store, mock_temario_store):
        """Test generating test from specific chunks."""
        gen = TestGenerator(
            store=mock_store,
            temario_store=mock_temario_store,
        )

        test = gen.generate_from_chunks(
            chunk_ids=["c1", "c2"],
            config=TestConfig(question_count=2),
        )

        assert test is not None
        assert len(test.questions) == 2

    def test_minimax_client_fallback(self):
        """Test MiniMax client fallback generation."""
        client = MiniMaxClient(api_key=None)  # No API key
        response = client.generate("Test prompt")

        # Should return JSON
        assert response
        assert "question" in response or "{" in response


# ============ Solver Tests ============

class TestSolverClass:
    """Tests for TestSolver."""

    @pytest.fixture
    def setup(self, tmp_path):
        """Set up store with a test."""
        from TIER_10_USER_APPS.tests.store import TestStore as TS
        store = TS(db_path=str(tmp_path / "solver_tests.db"))

        test = Test(
            id="test1",
            title="Solver Test",
            config=TestConfig(mode=TestMode.PRACTICE),
            questions=[
                Question(id="q1", test_id="test1", text="Q1", options=["A", "B"], correct_index=0),
                Question(id="q2", test_id="test1", text="Q2", options=["A", "B"], correct_index=1),
                Question(id="q3", test_id="test1", text="Q3", options=["A", "B"], correct_index=0),
            ],
        )
        store.save_test(test)

        return store, test

    def test_start_session(self, setup):
        """Test starting a session."""
        store, test = setup
        solver = TestSolver(store)

        session = solver.start_session("test1")
        assert session is not None
        assert session.test_id == "test1"
        assert session.status == "in_progress"

    def test_get_current_question(self, setup):
        """Test getting current question."""
        store, test = setup
        solver = TestSolver(store)
        session = solver.start_session("test1")

        q = solver.get_current_question(test, session)
        assert q is not None
        assert q.id == "q1"

    def test_submit_answer(self, setup):
        """Test submitting an answer."""
        store, test = setup
        solver = TestSolver(store)
        session = solver.start_session("test1")

        result = solver.submit_answer(test, session, 0, 5.0)

        assert result["is_correct"] is True
        assert result["show_feedback"] is True  # Practice mode
        assert session.current_question_index == 1

    def test_complete_session(self, setup):
        """Test completing a session."""
        store, test = setup
        solver = TestSolver(store)
        session = solver.start_session("test1")

        # Answer all questions (Q1 correct=0, Q2 correct=1, Q3 correct=0)
        # Submit 0 for Q1 -> correct
        solver.submit_answer(test, session, 0, 5.0)
        # Submit 1 for Q2 -> correct (Q2 correct_index is 1)
        solver.submit_answer(test, session, 1, 5.0)
        # Submit 0 for Q3 -> correct (Q3 correct_index is 0)
        solver.submit_answer(test, session, 0, 5.0)

        result = solver.complete_session(test, session)

        assert result is not None
        assert result.total_questions == 3
        assert result.correct_answers == 3  # All answers are correct
        assert result.score_percentage == 100.0
        assert session.status == "completed"

    def test_exam_mode_no_feedback(self, setup):
        """Test exam mode doesn't show feedback."""
        store, test = setup
        test.config.mode = TestMode.EXAM
        solver = TestSolver(store)
        session = solver.start_session("test1")

        result = solver.submit_answer(test, session, 0, 5.0)

        assert result["show_feedback"] is False
        assert "explanation" not in result


# ============ Analyzer Tests ============

class TestAnalyzerClass:
    """Tests for TestAnalyzer."""

    @pytest.fixture
    def setup(self, tmp_path):
        """Set up store with test and results."""
        from TIER_10_USER_APPS.tests.store import TestStore as TS
        store = TS(db_path=str(tmp_path / "analyzer_tests.db"))

        test = Test(
            id="test1",
            title="Analysis Test",
            config=TestConfig(),
            questions=[
                Question(id="q1", test_id="test1", text="Q1", options=["A", "B"], correct_index=0),
                Question(id="q2", test_id="test1", text="Q2", options=["A", "B"], correct_index=0),
            ],
        )
        store.save_test(test)

        return store, test

    def test_analyze_session(self, setup):
        """Test analyzing a session."""
        store, test = setup
        solver = TestSolver(store)
        analyzer = TestAnalyzer(store)

        session = solver.start_session("test1")
        solver.submit_answer(test, session, 0, 5.0)
        solver.submit_answer(test, session, 1, 5.0)  # Wrong
        result = solver.complete_session(test, session)

        analysis = analyzer.analyze_session(session.id)

        assert analysis["score"] == 50.0
        assert analysis["correct"] == 1
        assert analysis["total_questions"] == 2

    def test_get_progress_stats(self, setup):
        """Test getting progress statistics."""
        store, test = setup
        solver = TestSolver(store)
        analyzer = TestAnalyzer(store)

        # Create a session with results
        session = solver.start_session("test1")
        solver.submit_answer(test, session, 0, 5.0)
        solver.submit_answer(test, session, 0, 5.0)
        solver.complete_session(test, session)

        stats = analyzer.get_progress_stats(days=30)

        assert stats["tests_taken"] >= 1
        assert stats["average_score"] >= 0
        assert stats["trend"] in ["improving", "declining", "stable", "no_data", "insufficient_data"]

    def test_get_test_history(self, setup):
        """Test getting test history."""
        store, test = setup
        solver = TestSolver(store)
        analyzer = TestAnalyzer(store)

        # Create multiple sessions
        for _ in range(3):
            session = solver.start_session("test1")
            solver.submit_answer(test, session, 0, 5.0)
            solver.submit_answer(test, session, 0, 5.0)
            solver.complete_session(test, session)

        history = analyzer.get_test_history()

        assert len(history) >= 3

    def test_get_study_recommendations(self, setup):
        """Test getting study recommendations."""
        store, test = setup
        analyzer = TestAnalyzer(store)

        recommendations = analyzer.get_study_recommendations()

        assert isinstance(recommendations, list)


# ============ Integration Tests ============

class TestIntegrationClass:
    """Integration tests for full workflow."""

    @pytest.fixture
    def full_setup(self, tmp_path):
        """Full setup with all components."""
        from TIER_10_USER_APPS.tests.store import TestStore as TS
        db_path = tmp_path / "integration.db"
        store = TS(db_path=str(db_path))

        # Mock temario
        class MockChunk:
            def __init__(self, id, content, tema):
                self.id = id
                self.content = content
                self.tema = tema
                self.titulo = f"Title {id}"

        class MockTemarioStore:
            def list_chunks(self):
                return [MockChunk(f"c{i}", f"Content {i}", "1") for i in range(10)]
            def get_chunk(self, chunk_id):
                return MockChunk(chunk_id, "Test content", "1")

        generator = TestGenerator(
            store=store,
            temario_store=MockTemarioStore(),
        )
        solver = TestSolver(store)
        analyzer = TestAnalyzer(store)

        return store, generator, solver, analyzer

    def test_full_workflow(self, full_setup):
        """Test complete workflow: generate → solve → analyze."""
        store, generator, solver, analyzer = full_setup

        # Generate test
        config = TestConfig(question_count=3)
        test = generator.generate_from_tema("1", config)
        assert test is not None
        assert len(test.questions) == 3

        # Solve test
        session = solver.start_session(test.id)

        for _ in range(len(test.questions)):
            q = solver.get_current_question(test, session)
            if q:
                solver.submit_answer(test, session, 0, 3.0)

        result = solver.complete_session(test, session)
        assert result is not None
        assert result.total_questions == 3

        # Analyze
        analysis = analyzer.analyze_session(session.id)
        assert analysis["session_id"] == session.id

        # Check history
        history = analyzer.get_test_history()
        assert len(history) >= 1


# ============ Run Tests ============

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
