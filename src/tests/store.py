"""
Test Store - SQLite persistence for tests, sessions, and results.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import (
    Test,
    TestSession,
    TestResult,
    Question,
    TestConfig,
    QuestionType,
    TestMode,
)


class TestStore:
    """SQLite-based storage for tests, sessions, and results."""

    def __init__(self, db_path: str = "data/tests.db"):
        """
        Initialize the test store.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initialize database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Tests table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                config_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        # Questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id TEXT PRIMARY KEY,
                test_id TEXT NOT NULL,
                question_type TEXT NOT NULL,
                text TEXT NOT NULL,
                options_json TEXT,
                correct_index INTEGER NOT NULL,
                explanation TEXT,
                difficulty TEXT,
                source_chunk_ids_json TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (test_id) REFERENCES tests(id)
            )
        """)

        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                test_id TEXT NOT NULL,
                status TEXT NOT NULL,
                answers_json TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                current_question_index INTEGER NOT NULL,
                FOREIGN KEY (test_id) REFERENCES tests(id)
            )
        """)

        # Results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL UNIQUE,
                test_id TEXT NOT NULL,
                total_questions INTEGER NOT NULL,
                correct_answers INTEGER NOT NULL,
                incorrect_answers INTEGER NOT NULL,
                unanswered INTEGER NOT NULL,
                score_percentage REAL NOT NULL,
                time_spent_seconds REAL NOT NULL,
                weak_areas_json TEXT,
                strong_areas_json TEXT,
                recommendations_json TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id),
                FOREIGN KEY (test_id) REFERENCES tests(id)
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_test_id ON questions(test_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_test_id ON sessions(test_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_results_test_id ON results(test_id)")

        conn.commit()
        conn.close()

    # ============ Test Operations ============

    def save_test(self, test: Test) -> bool:
        """Save a test and its questions."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Save test
            cursor.execute("""
                INSERT OR REPLACE INTO tests (id, title, description, config_json, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                test.id,
                test.title,
                test.description,
                json.dumps(test.config.to_dict()),
                test.created_at.isoformat(),
            ))

            # Save questions
            for question in test.questions:
                cursor.execute("""
                    INSERT OR REPLACE INTO questions
                    (id, test_id, question_type, text, options_json, correct_index,
                     explanation, difficulty, source_chunk_ids_json, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    question.id,
                    question.test_id,
                    question.question_type.value,
                    question.text,
                    json.dumps(question.options),
                    question.correct_index,
                    question.explanation,
                    question.difficulty,
                    json.dumps(question.source_chunk_ids),
                    question.created_at.isoformat(),
                ))

            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving test: {e}")
            return False
        finally:
            conn.close()

    def get_test(self, test_id: str) -> Optional[Test]:
        """Get a test by ID with its questions."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Get test
            cursor.execute("SELECT * FROM tests WHERE id = ?", (test_id,))
            row = cursor.fetchone()

            if not row:
                return None

            # Get questions
            cursor.execute("SELECT * FROM questions WHERE test_id = ? ORDER BY created_at", (test_id,))
            question_rows = cursor.fetchall()

            questions = []
            for qrow in question_rows:
                questions.append(Question(
                    id=qrow["id"],
                    test_id=qrow["test_id"],
                    question_type=QuestionType(qrow["question_type"]),
                    text=qrow["text"],
                    options=json.loads(qrow["options_json"]) if qrow["options_json"] else [],
                    correct_index=qrow["correct_index"],
                    explanation=qrow["explanation"] or "",
                    difficulty=qrow["difficulty"] or "medium",
                    source_chunk_ids=json.loads(qrow["source_chunk_ids_json"]) if qrow["source_chunk_ids_json"] else [],
                    created_at=datetime.fromisoformat(qrow["created_at"]),
                ))

            return Test(
                id=row["id"],
                title=row["title"],
                description=row["description"] or "",
                config=TestConfig.from_dict(json.loads(row["config_json"])),
                questions=questions,
                created_at=datetime.fromisoformat(row["created_at"]),
            )
        finally:
            conn.close()

    def list_tests(self, limit: int = 50, offset: int = 0) -> list[Test]:
        """List all tests."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * FROM tests ORDER BY created_at DESC LIMIT ? OFFSET ?
            """, (limit, offset))

            tests = []
            for row in cursor.fetchall():
                tests.append(Test(
                    id=row["id"],
                    title=row["title"],
                    description=row["description"] or "",
                    config=TestConfig.from_dict(json.loads(row["config_json"])),
                    questions=[],  # Don't load questions for list view
                    created_at=datetime.fromisoformat(row["created_at"]),
                ))

            return tests
        finally:
            conn.close()

    def delete_test(self, test_id: str) -> bool:
        """Delete a test and its questions."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM questions WHERE test_id = ?", (test_id,))
            cursor.execute("DELETE FROM tests WHERE id = ?", (test_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting test: {e}")
            return False
        finally:
            conn.close()

    # ============ Session Operations ============

    def save_session(self, session: TestSession) -> bool:
        """Save a test session."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO sessions
                (id, test_id, status, answers_json, started_at, completed_at, current_question_index)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session.id,
                session.test_id,
                session.status,
                json.dumps({qid: a.to_dict() for qid, a in session.answers.items()}),
                session.started_at.isoformat(),
                session.completed_at.isoformat() if session.completed_at else None,
                session.current_question_index,
            ))

            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
        finally:
            conn.close()

    def get_session(self, session_id: str) -> Optional[TestSession]:
        """Get a session by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
            row = cursor.fetchone()

            if not row:
                return None

            from .models import SessionAnswer

            answers_data = json.loads(row["answers_json"])
            answers = {
                qid: SessionAnswer.from_dict(a)
                for qid, a in answers_data.items()
            }

            return TestSession(
                id=row["id"],
                test_id=row["test_id"],
                status=row["status"],
                answers=answers,
                started_at=datetime.fromisoformat(row["started_at"]),
                completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
                current_question_index=row["current_question_index"],
            )
        finally:
            conn.close()

    def list_sessions(self, test_id: Optional[str] = None, limit: int = 50) -> list[TestSession]:
        """List sessions, optionally filtered by test."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            if test_id:
                cursor.execute("""
                    SELECT * FROM sessions WHERE test_id = ? ORDER BY started_at DESC LIMIT ?
                """, (test_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM sessions ORDER BY started_at DESC LIMIT ?
                """, (limit,))

            sessions = []
            for row in cursor.fetchall():
                from .models import SessionAnswer
                answers_data = json.loads(row["answers_json"])
                answers = {
                    qid: SessionAnswer.from_dict(a)
                    for qid, a in answers_data.items()
                }

                sessions.append(TestSession(
                    id=row["id"],
                    test_id=row["test_id"],
                    status=row["status"],
                    answers=answers,
                    started_at=datetime.fromisoformat(row["started_at"]),
                    completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
                    current_question_index=row["current_question_index"],
                ))

            return sessions
        finally:
            conn.close()

    # ============ Result Operations ============

    def save_result(self, result: TestResult) -> bool:
        """Save a test result."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO results
                (session_id, test_id, total_questions, correct_answers, incorrect_answers,
                 unanswered, score_percentage, time_spent_seconds, weak_areas_json,
                 strong_areas_json, recommendations_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result.session_id,
                result.test_id,
                result.total_questions,
                result.correct_answers,
                result.incorrect_answers,
                result.unanswered,
                result.score_percentage,
                result.time_spent_seconds,
                json.dumps(result.weak_areas),
                json.dumps(result.strong_areas),
                json.dumps(result.recommendations),
                result.created_at.isoformat(),
            ))

            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving result: {e}")
            return False
        finally:
            conn.close()

    def get_result(self, session_id: str) -> Optional[TestResult]:
        """Get a result by session ID."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM results WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()

            if not row:
                return None

            return TestResult(
                session_id=row["session_id"],
                test_id=row["test_id"],
                total_questions=row["total_questions"],
                correct_answers=row["correct_answers"],
                incorrect_answers=row["incorrect_answers"],
                unanswered=row["unanswered"],
                score_percentage=row["score_percentage"],
                time_spent_seconds=row["time_spent_seconds"],
                weak_areas=json.loads(row["weak_areas_json"]) if row["weak_areas_json"] else [],
                strong_areas=json.loads(row["strong_areas_json"]) if row["strong_areas_json"] else [],
                recommendations=json.loads(row["recommendations_json"]) if row["recommendations_json"] else [],
                created_at=datetime.fromisoformat(row["created_at"]),
            )
        finally:
            conn.close()

    def list_results(self, test_id: Optional[str] = None, limit: int = 50) -> list[TestResult]:
        """List results, optionally filtered by test."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            if test_id:
                cursor.execute("""
                    SELECT * FROM results WHERE test_id = ? ORDER BY created_at DESC LIMIT ?
                """, (test_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM results ORDER BY created_at DESC LIMIT ?
                """, (limit,))

            results = []
            for row in cursor.fetchall():
                results.append(TestResult(
                    session_id=row["session_id"],
                    test_id=row["test_id"],
                    total_questions=row["total_questions"],
                    correct_answers=row["correct_answers"],
                    incorrect_answers=row["incorrect_answers"],
                    unanswered=row["unanswered"],
                    score_percentage=row["score_percentage"],
                    time_spent_seconds=row["time_spent_seconds"],
                    weak_areas=json.loads(row["weak_areas_json"]) if row["weak_areas_json"] else [],
                    strong_areas=json.loads(row["strong_areas_json"]) if row["strong_areas_json"] else [],
                    recommendations=json.loads(row["recommendations_json"]) if row["recommendations_json"] else [],
                    created_at=datetime.fromisoformat(row["created_at"]),
                ))

            return results
        finally:
            conn.close()

    # ============ Statistics ============

    def get_test_count(self) -> int:
        """Get total number of tests."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tests")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_session_count(self) -> int:
        """Get total number of sessions."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sessions")
        count = cursor.fetchone()[0]
        conn.close()
        return count
