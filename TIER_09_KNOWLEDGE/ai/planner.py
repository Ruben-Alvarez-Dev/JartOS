"""
Study Planner - Generates weekly study plans based on weak areas and goals.
"""

import json
import logging
import os
from datetime import datetime, timedelta, date
from typing import List, Optional
from uuid import uuid4

from .models import StudyPlan, StudyTask, DailyRecommendation, Priority, StudyGoal
from .store import AIStore
from .analyzer import WeakAreasAnalyzer

logger = logging.getLogger(__name__)


class StudyPlanner:
    """
    Generates personalized study plans.

    Considers:
    - Weak areas (priority focus)
    - Available study time
    - Learning goals
    - Past performance
    """

    # Days of the week
    DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    # Default time slots per day (in minutes)
    DEFAULT_DAILY_MINUTES = {
        "monday": 90,
        "tuesday": 90,
        "wednesday": 90,
        "thursday": 90,
        "friday": 60,
        "saturday": 120,
        "sunday": 60,
    }

    def __init__(
        self,
        ai_store: AIStore,
        analyzer: WeakAreasAnalyzer,
        flashcard_store=None,
        test_store=None,
    ):
        """
        Initialize the planner.

        Args:
            ai_store: AIStore instance
            analyzer: WeakAreasAnalyzer instance
            flashcard_store: Optional FlashcardStore
            test_store: Optional TestStore
        """
        self.ai_store = ai_store
        self.analyzer = analyzer
        self.flashcard_store = flashcard_store
        self.test_store = test_store

    def generate_weekly_plan(
        self,
        start_date: Optional[date] = None,
        total_hours: Optional[float] = None,
        focus_areas: Optional[List[str]] = None,
    ) -> StudyPlan:
        """
        Generate a weekly study plan.

        Args:
            start_date: Start date (defaults to next Monday)
            total_hours: Target study hours (auto-calculated if None)
            focus_areas: Specific areas to focus on

        Returns:
            StudyPlan object
        """
        # Determine week boundaries
        if start_date is None:
            today = date.today()
            # Find next Monday
            days_until_monday = (7 - today.weekday()) % 7
            if days_until_monday == 0:
                days_until_monday = 7  # If today is Monday, start next week
            start_date = today + timedelta(days=days_until_monday)

        week_end = start_date + timedelta(days=6)

        # Get weak areas for planning
        weak_areas = self.ai_store.get_weak_areas(limit=10)

        # Calculate target hours
        if total_hours is None:
            time_estimate = self.analyzer.get_study_time_estimate()
            total_hours = time_estimate["recommended_hours_per_week"]

        # Generate goals
        goals = self._generate_goals(weak_areas, focus_areas)

        # Generate tasks
        tasks = self._generate_tasks(weak_areas, focus_areas, total_hours)

        # Distribute tasks across days
        daily_breakdown = self._distribute_tasks(tasks, start_date)

        # Calculate actual total hours
        total_minutes = sum(
            sum(t.duration_minutes for t in day_tasks)
            for day_tasks in daily_breakdown.values()
        )
        actual_hours = total_minutes / 60

        # Create plan
        plan = StudyPlan(
            week_start=start_date.isoformat(),
            week_end=week_end.isoformat(),
            total_hours=round(actual_hours, 1),
            goals=goals,
            tasks=tasks,
            daily_breakdown=daily_breakdown,
            focus_areas=focus_areas or [a.tema for a in weak_areas[:3]],
            generated_by="ai",
        )

        # Save plan
        self.ai_store.save_study_plan(plan)

        logger.info(f"Generated weekly plan: {plan.total_hours}h, {len(tasks)} tasks")
        return plan

    def _generate_goals(self, weak_areas: list, focus_areas: Optional[List[str]]) -> List[str]:
        """Generate study goals for the week."""
        goals = []

        # Weak area goals
        critical_areas = [a for a in weak_areas if a.priority == Priority.CRITICAL]
        if critical_areas:
            goals.append(f"Master {len(critical_areas)} critical weak area(s)")

        # Review goals
        high_areas = [a for a in weak_areas if a.priority == Priority.HIGH]
        if high_areas:
            goals.append(f"Improve {len(high_areas)} high-priority area(s)")

        # New content goal
        goals.append("Review and practice daily")

        # Test goal
        goals.append("Complete at least 2 practice tests")

        return goals[:5]

    def _generate_tasks(
        self,
        weak_areas: list,
        focus_areas: Optional[List[str]],
        total_hours: float,
    ) -> List[StudyTask]:
        """Generate study tasks."""
        tasks = []
        total_minutes = int(total_hours * 60)
        allocated_minutes = 0

        # Priority 1: Critical weak area flashcard review
        for area in weak_areas:
            if area.priority == Priority.CRITICAL and allocated_minutes < total_minutes * 0.5:
                task = StudyTask(
                    id=str(uuid4())[:8],
                    description=f"Review flashcards: Tema {area.tema}",
                    type=StudyGoal.WEAK_AREA_IMPROVEMENT,
                    tema=area.tema,
                    duration_minutes=30,
                    priority=Priority.CRITICAL,
                )
                tasks.append(task)
                allocated_minutes += task.duration_minutes

        # Priority 2: Practice tests on weak areas
        for area in weak_areas[:3]:
            if allocated_minutes < total_minutes * 0.7:
                task = StudyTask(
                    id=str(uuid4())[:8],
                    description=f"Practice test: Tema {area.tema}",
                    type=StudyGoal.PRACTICE_TEST,
                    tema=area.tema,
                    duration_minutes=20,
                    priority=area.priority,
                )
                tasks.append(task)
                allocated_minutes += task.duration_minutes

        # Priority 3: General flashcard review
        if self.flashcard_store:
            stats = self.flashcard_store.get_all_stats()
            due_cards = stats.get("cards_due_today", 0)

            if due_cards > 0 and allocated_minutes < total_minutes * 0.8:
                duration = min(30, due_cards * 2)  # ~2 min per card
                task = StudyTask(
                    id=str(uuid4())[:8],
                    description=f"Review {due_cards} due flashcards",
                    type=StudyGoal.REVIEW,
                    duration_minutes=duration,
                    priority=Priority.HIGH,
                )
                tasks.append(task)
                allocated_minutes += duration

        # Priority 4: New content
        remaining_time = total_minutes - allocated_minutes
        if remaining_time > 30:
            task = StudyTask(
                id=str(uuid4())[:8],
                description="Study new temario content",
                type=StudyGoal.NEW_CONTENT,
                duration_minutes=min(45, remaining_time),
                priority=Priority.MEDIUM,
            )
            tasks.append(task)

        return tasks

    def _distribute_tasks(self, tasks: List[StudyTask], start_date: date) -> dict:
        """Distribute tasks across the week."""
        daily_breakdown = {day: [] for day in self.DAYS}

        # Sort tasks by priority
        priority_order = {Priority.CRITICAL: 0, Priority.HIGH: 1, Priority.MEDIUM: 2, Priority.LOW: 3}
        sorted_tasks = sorted(tasks, key=lambda t: priority_order[t.priority])

        # Calculate available time per day
        daily_minutes = self.DEFAULT_DAILY_MINUTES.copy()

        # Distribute tasks
        task_idx = 0
        for day in self.DAYS:
            day_minutes = 0
            max_minutes = daily_minutes[day]

            while task_idx < len(sorted_tasks) and day_minutes < max_minutes:
                task = sorted_tasks[task_idx]
                if day_minutes + task.duration_minutes <= max_minutes * 1.2:  # Allow 20% overflow
                    daily_breakdown[day].append(task)
                    day_minutes += task.duration_minutes
                    task_idx += 1
                else:
                    break

        return daily_breakdown

    def get_current_plan(self) -> Optional[StudyPlan]:
        """Get the current week's study plan."""
        return self.ai_store.get_current_study_plan()

    def generate_daily_recommendations(self, target_date: Optional[date] = None) -> List[DailyRecommendation]:
        """
        Generate recommendations for a specific day.

        Args:
            target_date: Target date (defaults to today)

        Returns:
            List of DailyRecommendation objects
        """
        if target_date is None:
            target_date = date.today()

        # Clear existing recommendations for this date
        # Note: We need to clear by date, not just today
        self.ai_store.clear_todays_recommendations()

        recommendations = []
        day_name = self.DAYS[target_date.weekday()]

        # Get current plan
        plan = self.get_current_plan()

        if plan and day_name in plan.daily_breakdown:
            # Use tasks from plan
            for task in plan.daily_breakdown[day_name]:
                rec = DailyRecommendation(
                    date=target_date.isoformat(),
                    priority=task.priority,
                    type=task.type.value,
                    title=task.description,
                    description=f"Study task: {task.description}",
                    action=f"Complete: {task.description}",
                    target_id=task.tema,
                    estimated_minutes=task.duration_minutes,
                    reason="Part of weekly study plan",
                )
                recommendations.append(rec)

        # Add flashcard review if due
        if self.flashcard_store:
            stats = self.flashcard_store.get_all_stats()
            due = stats.get("cards_due_today", 0)

            if due > 0:
                rec = DailyRecommendation(
                    date=target_date.isoformat(),
                    priority=Priority.HIGH,
                    type="flashcard_review",
                    title=f"Review {due} due flashcards",
                    description=f"You have {due} flashcards due for review",
                    action="Start flashcard review session",
                    estimated_minutes=min(30, due * 2),
                    reason="Spaced repetition review due",
                )
                recommendations.append(rec)

        # Add weak area focus if critical
        weak_areas = self.ai_store.get_weak_areas(limit=3)
        for area in weak_areas:
            if area.priority == Priority.CRITICAL:
                rec = DailyRecommendation(
                    date=target_date.isoformat(),
                    priority=Priority.CRITICAL,
                    type="weak_area",
                    title=f"Focus on Tema {area.tema}",
                    description=f"Critical weak area (score: {area.combined_score}%)",
                    action=f"Study Tema {area.tema} material and take practice test",
                    target_id=str(area.tema),
                    estimated_minutes=30,
                    reason=f"Low score: {area.combined_score}%",
                )
                recommendations.append(rec)
                break  # Only one critical area per day

        # Sort by priority
        priority_order = {Priority.CRITICAL: 0, Priority.HIGH: 1, Priority.MEDIUM: 2, Priority.LOW: 3}
        recommendations.sort(key=lambda r: priority_order[r.priority])

        # Save recommendations
        if recommendations:
            self.ai_store.save_recommendations_batch(recommendations)

        logger.info(f"Generated {len(recommendations)} recommendations for {target_date}")
        return recommendations

    def mark_task_completed(self, task_id: str) -> bool:
        """Mark a task as completed in the current plan."""
        plan = self.get_current_plan()
        if not plan:
            return False

        for task in plan.tasks:
            if task.id == task_id:
                task.completed = True
                task.completed_at = datetime.now().isoformat()
                # Update plan in store
                self.ai_store.save_study_plan(plan)
                return True

        return False
