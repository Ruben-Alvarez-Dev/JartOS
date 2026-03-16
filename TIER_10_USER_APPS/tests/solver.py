"""
Test Solver - Interactive test taking functionality.

Supports practice mode (feedback after each answer) and exam mode (no feedback until complete).
"""

import time
from datetime import datetime
from typing import Optional, Callable

from .models import (
    Test,
    Question,
    TestSession,
    SessionAnswer,
    TestMode,
    TestResult,
)


class TestSolver:
    """Manages interactive test sessions."""

    def __init__(self, store):
        """
        Initialize test solver.

        Args:
            store: TestStore instance
        """
        self.store = store
        self.active_session: Optional[TestSession] = None

    def start_session(self, test_id: str, mode: Optional[TestMode] = None) -> TestSession:
        """
        Start a new test session.

        Args:
            test_id: ID of the test to take
            mode: Session mode (defaults to test's configured mode)

        Returns:
            New TestSession
        """
        test = self.store.get_test(test_id)
        if not test:
            raise ValueError(f"Test not found: {test_id}")

        # Create session
        session = TestSession(
            test_id=test_id,
            status="in_progress",
        )

        # Set mode
        if mode:
            test.config.mode = mode

        # Save session
        self.store.save_session(session)
        self.active_session = session

        return session

    def resume_session(self, session_id: str) -> TestSession:
        """
        Resume an existing session.

        Args:
            session_id: ID of the session to resume

        Returns:
            TestSession
        """
        session = self.store.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")

        if session.status != "in_progress":
            raise ValueError(f"Session is not in progress: {session.status}")

        self.active_session = session
        return session

    def get_current_question(self, test: Test, session: TestSession) -> Optional[Question]:
        """
        Get the current question for a session.

        Args:
            test: The test being taken
            session: The active session

        Returns:
            Current Question or None if complete
        """
        if session.current_question_index >= len(test.questions):
            return None

        return test.questions[session.current_question_index]

    def submit_answer(
        self,
        test: Test,
        session: TestSession,
        answer_index: int,
        time_spent_seconds: float = 0.0,
    ) -> dict:
        """
        Submit an answer for the current question.

        Args:
            test: The test being taken
            session: The active session
            answer_index: Index of the selected answer
            time_spent_seconds: Time taken to answer

        Returns:
            Dict with feedback (if practice mode)
        """
        current_question = self.get_current_question(test, session)
        if not current_question:
            raise ValueError("No more questions")

        # Check answer
        is_correct = current_question.check_answer(answer_index)

        # Record answer
        session.record_answer(
            question_id=current_question.id,
            answer_index=answer_index,
            is_correct=is_correct,
            time_spent=time_spent_seconds,
        )

        # Advance to next question
        session.current_question_index += 1

        # Save session
        self.store.save_session(session)

        # Build response
        result = {
            "question_id": current_question.id,
            "is_correct": is_correct,
            "correct_index": current_question.correct_index,
            "explanation": current_question.explanation,
            "question_number": session.current_question_index,
            "total_questions": len(test.questions),
            "is_complete": session.current_question_index >= len(test.questions),
        }

        # Show feedback in practice mode
        if test.config.mode == TestMode.PRACTICE:
            result["show_feedback"] = True
        else:
            result["show_feedback"] = False
            # Don't show explanation in exam mode
            del result["explanation"]
            del result["correct_index"]

        return result

    def complete_session(self, test: Test, session: TestSession) -> TestResult:
        """
        Complete a session and generate results.

        Args:
            test: The test being taken
            session: The session to complete

        Returns:
            TestResult with analysis
        """
        # Mark any unanswered questions
        for question in test.questions:
            if question.id not in session.answers:
                session.record_answer(
                    question_id=question.id,
                    answer_index=-1,
                    is_correct=False,
                    time_spent=0.0,
                )

        # Complete session
        session.complete()
        self.store.save_session(session)

        # Calculate results
        result = self._calculate_result(test, session)

        # Save result
        self.store.save_result(result)

        self.active_session = None

        return result

    def _calculate_result(self, test: Test, session: TestSession) -> TestResult:
        """Calculate test results from session."""
        correct = sum(1 for a in session.answers.values() if a.is_correct)
        total = len(test.questions)
        unanswered = sum(1 for a in session.answers.values() if a.answer_index == -1)

        score = (correct / total * 100) if total > 0 else 0

        # Calculate time spent
        total_time = sum(a.time_spent_seconds for a in session.answers.values())

        # Identify weak and strong areas
        weak_areas = []
        strong_areas = []

        # Group questions by tema/source
        tema_results = {}
        for question in test.questions:
            answer = session.answers.get(question.id)
            if answer:
                # Get tema from source chunks (simplified)
                source = question.source_chunk_ids[0] if question.source_chunk_ids else "unknown"
                if source not in tema_results:
                    tema_results[source] = {"correct": 0, "total": 0}
                tema_results[source]["total"] += 1
                if answer.is_correct:
                    tema_results[source]["correct"] += 1

        # Categorize areas
        for source, stats in tema_results.items():
            pct = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            if pct < 60:
                weak_areas.append(source)
            elif pct >= 80:
                strong_areas.append(source)

        # Generate recommendations
        recommendations = []
        if score < 60:
            recommendations.append("Consider reviewing the material before retaking the test.")
        if weak_areas:
            recommendations.append(f"Focus on studying: {', '.join(weak_areas[:3])}")
        if score >= 80:
            recommendations.append("Great job! Ready for more challenging material.")

        return TestResult(
            session_id=session.id,
            test_id=test.id,
            total_questions=total,
            correct_answers=correct,
            incorrect_answers=total - correct - unanswered,
            unanswered=unanswered,
            score_percentage=round(score, 1),
            time_spent_seconds=total_time,
            weak_areas=weak_areas,
            strong_areas=strong_areas,
            recommendations=recommendations,
        )

    def run_interactive(
        self,
        test: Test,
        session: TestSession,
        input_fn: Optional[Callable] = None,
        output_fn: Optional[Callable] = None,
    ) -> TestResult:
        """
        Run an interactive test session.

        Args:
            test: The test to take
            session: The session to run
            input_fn: Function to get user input (default: builtins.input)
            output_fn: Function to display output (default: print)

        Returns:
            TestResult after completion
        """
        input_fn = input_fn or input
        output_fn = output_fn or print

        output_fn(f"\n{'='*60}")
        output_fn(f"Test: {test.title}")
        output_fn(f"Questions: {len(test.questions)}")
        output_fn(f"Mode: {test.config.mode.value}")
        output_fn(f"{'='*60}\n")

        while True:
            question = self.get_current_question(test, session)
            if not question:
                break

            # Display question
            output_fn(f"\nQuestion {session.current_question_index + 1}/{len(test.questions)}")
            output_fn(f"{'-'*40}")
            output_fn(question.text)

            # Display options
            for i, option in enumerate(question.options):
                output_fn(f"  {i + 1}. {option}")

            # Get answer
            start_time = time.time()
            while True:
                try:
                    answer = input_fn("\nYour answer (1-4, or 'q' to quit): ").strip()
                    if answer.lower() == "q":
                        output_fn("\nSession abandoned.")
                        session.status = "abandoned"
                        self.store.save_session(session)
                        return None

                    answer_index = int(answer) - 1
                    if 0 <= answer_index < len(question.options):
                        break
                    output_fn("Invalid option. Please enter 1-4.")
                except ValueError:
                    output_fn("Invalid input. Please enter a number.")

            time_spent = time.time() - start_time

            # Submit answer
            result = self.submit_answer(test, session, answer_index, time_spent)

            # Show feedback in practice mode
            if result.get("show_feedback"):
                if result["is_correct"]:
                    output_fn("\n✓ Correct!")
                else:
                    output_fn(f"\n✗ Incorrect. The correct answer was: {result['correct_index'] + 1}")
                if result.get("explanation"):
                    output_fn(f"\nExplanation: {result['explanation']}")

            if result["is_complete"]:
                break

        # Complete and show results
        test_result = self.complete_session(test, session)

        output_fn(f"\n{'='*60}")
        output_fn("TEST COMPLETE")
        output_fn(f"{'='*60}")
        output_fn(f"Score: {test_result.score_percentage}%")
        output_fn(f"Correct: {test_result.correct_answers}/{test_result.total_questions}")
        output_fn(f"Time: {test_result.time_spent_seconds:.1f} seconds")

        if test_result.passed:
            output_fn("\n✓ PASSED")
        else:
            output_fn("\n✗ NOT PASSED (need 60%)")

        if test_result.weak_areas:
            output_fn(f"\nAreas to review: {', '.join(test_result.weak_areas)}")

        if test_result.recommendations:
            output_fn("\nRecommendations:")
            for rec in test_result.recommendations:
                output_fn(f"  - {rec}")

        return test_result

    def abandon_session(self, session: TestSession):
        """Mark a session as abandoned."""
        session.status = "abandoned"
        self.store.save_session(session)
        if self.active_session and self.active_session.id == session.id:
            self.active_session = None
