"""
AI Store - SQLite persistence for AI analytics and recommendations.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from .models import (
    WeakArea,
    PreparednessPrediction,
    StudyPlan,
    StudyTask,
    DailyRecommendation,
    LearningMetrics,
    Priority,
    StudyGoal,
)


class AIStore:
    """SQLite-based storage for AI analytics."""

    def __init__(self, db_path: str = "data/ai.db"):
        """
        Initialize the AI store.

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

        # Weak areas table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weak_areas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tema TEXT NOT NULL,
                apartado TEXT,
                source TEXT NOT NULL,
                flashcard_ease_avg REAL DEFAULT 2.5,
                test_score_avg REAL DEFAULT 0,
                combined_score REAL DEFAULT 0,
                cards_affected INTEGER DEFAULT 0,
                tests_affected INTEGER DEFAULT 0,
                priority TEXT DEFAULT 'medium',
                created_at TEXT NOT NULL
            )
        """)

        # Predictions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                overall_score REAL NOT NULL,
                confidence REAL NOT NULL,
                level TEXT NOT NULL,
                weak_areas_json TEXT,
                strong_areas_json TEXT,
                recommended_hours_per_week REAL DEFAULT 10,
                estimated_days_to_ready INTEGER,
                factors_json TEXT,
                created_at TEXT NOT NULL
            )
        """)

        # Study plans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_start TEXT NOT NULL,
                week_end TEXT NOT NULL,
                total_hours REAL DEFAULT 0,
                goals_json TEXT,
                tasks_json TEXT,
                daily_breakdown_json TEXT,
                focus_areas_json TEXT,
                generated_by TEXT DEFAULT 'ai',
                created_at TEXT NOT NULL
            )
        """)

        # Daily recommendations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                priority TEXT DEFAULT 'medium',
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                action TEXT,
                target_id TEXT,
                estimated_minutes INTEGER DEFAULT 15,
                reason TEXT,
                completed INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)

        # Learning metrics table (single row, updated)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_metrics (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                metrics_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_weak_areas_tema ON weak_areas(tema)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_created ON predictions(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_plans_week ON study_plans(week_start)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_recommendations_date ON daily_recommendations(date)")

        conn.commit()
        conn.close()

    # ============ Weak Areas ============

    def save_weak_area(self, area: WeakArea) -> WeakArea:
        """Save a weak area."""
        now = datetime.now().isoformat()
        area.created_at = now

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO weak_areas
            (tema, apartado, source, flashcard_ease_avg, test_score_avg,
             combined_score, cards_affected, tests_affected, priority, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            area.tema,
            area.apartado,
            area.source,
            area.flashcard_ease_avg,
            area.test_score_avg,
            area.combined_score,
            area.cards_affected,
            area.tests_affected,
            area.priority.value,
            area.created_at,
        ))
        area.id = cursor.lastrowid
        conn.commit()
        conn.close()

        return area

    def save_weak_areas_batch(self, areas: List[WeakArea]) -> List[WeakArea]:
        """Save multiple weak areas."""
        now = datetime.now().isoformat()
        conn = self._get_connection()
        cursor = conn.cursor()

        for area in areas:
            area.created_at = now
            cursor.execute("""
                INSERT INTO weak_areas
                (tema, apartado, source, flashcard_ease_avg, test_score_avg,
                 combined_score, cards_affected, tests_affected, priority, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                area.tema,
                area.apartado,
                area.source,
                area.flashcard_ease_avg,
                area.test_score_avg,
                area.combined_score,
                area.cards_affected,
                area.tests_affected,
                area.priority.value,
                area.created_at,
            ))
            area.id = cursor.lastrowid

        conn.commit()
        conn.close()
        return areas

    def get_weak_areas(self, limit: int = 10) -> List[WeakArea]:
        """Get all weak areas, sorted by combined score."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM weak_areas
            ORDER BY combined_score ASC, created_at DESC
            LIMIT ?
        """, (limit,))

        areas = []
        for row in cursor.fetchall():
            areas.append(WeakArea(
                id=row["id"],
                tema=row["tema"],
                apartado=row["apartado"],
                source=row["source"],
                flashcard_ease_avg=row["flashcard_ease_avg"],
                test_score_avg=row["test_score_avg"],
                combined_score=row["combined_score"],
                cards_affected=row["cards_affected"],
                tests_affected=row["tests_affected"],
                priority=Priority(row["priority"]),
                created_at=row["created_at"],
            ))

        conn.close()
        return areas

    def clear_weak_areas(self) -> int:
        """Clear all weak areas (for refresh)."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM weak_areas")
        count = cursor.rowcount
        conn.commit()
        conn.close()
        return count

    # ============ Predictions ============

    def save_prediction(self, prediction: PreparednessPrediction) -> PreparednessPrediction:
        """Save a preparedness prediction."""
        now = datetime.now().isoformat()
        prediction.created_at = now

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO predictions
            (overall_score, confidence, level, weak_areas_json, strong_areas_json,
             recommended_hours_per_week, estimated_days_to_ready, factors_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prediction.overall_score,
            prediction.confidence,
            prediction.level,
            json.dumps(prediction.weak_areas),
            json.dumps(prediction.strong_areas),
            prediction.recommended_hours_per_week,
            prediction.estimated_days_to_ready,
            json.dumps(prediction.factors),
            prediction.created_at,
        ))
        prediction.id = cursor.lastrowid
        conn.commit()
        conn.close()

        return prediction

    def get_latest_prediction(self) -> Optional[PreparednessPrediction]:
        """Get the most recent prediction."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM predictions ORDER BY created_at DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return PreparednessPrediction(
            id=row["id"],
            overall_score=row["overall_score"],
            confidence=row["confidence"],
            level=row["level"],
            weak_areas=json.loads(row["weak_areas_json"]) if row["weak_areas_json"] else [],
            strong_areas=json.loads(row["strong_areas_json"]) if row["strong_areas_json"] else [],
            recommended_hours_per_week=row["recommended_hours_per_week"],
            estimated_days_to_ready=row["estimated_days_to_ready"],
            factors=json.loads(row["factors_json"]) if row["factors_json"] else {},
            created_at=row["created_at"],
        )

    # ============ Study Plans ============

    def save_study_plan(self, plan: StudyPlan) -> StudyPlan:
        """Save a study plan."""
        now = datetime.now().isoformat()
        plan.created_at = now

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO study_plans
            (week_start, week_end, total_hours, goals_json, tasks_json,
             daily_breakdown_json, focus_areas_json, generated_by, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            plan.week_start,
            plan.week_end,
            plan.total_hours,
            json.dumps(plan.goals),
            json.dumps([t.to_dict() for t in plan.tasks]),
            json.dumps({k: [t.to_dict() for t in v] for k, v in plan.daily_breakdown.items()}),
            json.dumps(plan.focus_areas),
            plan.generated_by,
            plan.created_at,
        ))
        plan.id = cursor.lastrowid
        conn.commit()
        conn.close()

        return plan

    def get_current_study_plan(self) -> Optional[StudyPlan]:
        """Get the study plan for the current week."""
        from datetime import date

        today = date.today().isoformat()
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM study_plans
            WHERE week_start <= ? AND week_end >= ?
            ORDER BY created_at DESC LIMIT 1
        """, (today, today))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        tasks = [StudyTask.from_dict(t) for t in json.loads(row["tasks_json"])]
        daily_breakdown = {
            k: [StudyTask.from_dict(t) for t in v]
            for k, v in json.loads(row["daily_breakdown_json"]).items()
        }

        return StudyPlan(
            id=row["id"],
            week_start=row["week_start"],
            week_end=row["week_end"],
            total_hours=row["total_hours"],
            goals=json.loads(row["goals_json"]),
            tasks=tasks,
            daily_breakdown=daily_breakdown,
            focus_areas=json.loads(row["focus_areas_json"]),
            generated_by=row["generated_by"],
            created_at=row["created_at"],
        )

    # ============ Daily Recommendations ============

    def save_recommendation(self, rec: DailyRecommendation) -> DailyRecommendation:
        """Save a daily recommendation."""
        now = datetime.now().isoformat()
        rec.created_at = now

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO daily_recommendations
            (date, priority, type, title, description, action, target_id,
             estimated_minutes, reason, completed, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rec.date,
            rec.priority.value,
            rec.type,
            rec.title,
            rec.description,
            rec.action,
            rec.target_id,
            rec.estimated_minutes,
            rec.reason,
            1 if rec.completed else 0,
            rec.created_at,
        ))
        rec.id = cursor.lastrowid
        conn.commit()
        conn.close()

        return rec

    def save_recommendations_batch(self, recs: List[DailyRecommendation]) -> List[DailyRecommendation]:
        """Save multiple recommendations."""
        now = datetime.now().isoformat()
        conn = self._get_connection()
        cursor = conn.cursor()

        for rec in recs:
            rec.created_at = now
            cursor.execute("""
                INSERT INTO daily_recommendations
                (date, priority, type, title, description, action, target_id,
                 estimated_minutes, reason, completed, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                rec.date,
                rec.priority.value,
                rec.type,
                rec.title,
                rec.description,
                rec.action,
                rec.target_id,
                rec.estimated_minutes,
                rec.reason,
                1 if rec.completed else 0,
                rec.created_at,
            ))
            rec.id = cursor.lastrowid

        conn.commit()
        conn.close()
        return recs

    def get_todays_recommendations(self) -> List[DailyRecommendation]:
        """Get recommendations for today."""
        from datetime import date
        today = date.today().isoformat()

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM daily_recommendations
            WHERE date = ?
            ORDER BY priority ASC, created_at ASC
        """, (today,))

        recs = []
        for row in cursor.fetchall():
            recs.append(DailyRecommendation(
                id=row["id"],
                date=row["date"],
                priority=Priority(row["priority"]),
                type=row["type"],
                title=row["title"],
                description=row["description"],
                action=row["action"],
                target_id=row["target_id"],
                estimated_minutes=row["estimated_minutes"],
                reason=row["reason"],
                completed=bool(row["completed"]),
                created_at=row["created_at"],
            ))

        conn.close()
        return recs

    def mark_recommendation_completed(self, rec_id: int) -> bool:
        """Mark a recommendation as completed."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE daily_recommendations
            SET completed = 1
            WHERE id = ?
        """, (rec_id,))

        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def clear_todays_recommendations(self) -> int:
        """Clear today's recommendations (for regeneration)."""
        from datetime import date
        today = date.today().isoformat()

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM daily_recommendations WHERE date = ?", (today,))
        count = cursor.rowcount
        conn.commit()
        conn.close()
        return count

    # ============ Learning Metrics ============

    def save_learning_metrics(self, metrics: LearningMetrics) -> LearningMetrics:
        """Save learning metrics (upsert)."""
        now = datetime.now().isoformat()
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO learning_metrics (id, metrics_json, updated_at)
            VALUES (1, ?, ?)
        """, (json.dumps(metrics.to_dict()), now))

        conn.commit()
        conn.close()
        return metrics

    def get_learning_metrics(self) -> Optional[LearningMetrics]:
        """Get current learning metrics."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM learning_metrics WHERE id = 1")
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return LearningMetrics.from_dict(json.loads(row["metrics_json"]))
