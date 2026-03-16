"""
AI Module - Advanced analytics and intelligent recommendations.

Phase 5 of oposiciones-system: Predictive analysis and smart study planning.
"""

from .models import (
    WeakArea,
    PreparednessPrediction,
    StudyPlan,
    DailyRecommendation,
    LearningMetrics,
)
from .analyzer import WeakAreasAnalyzer
from .predictor import PreparednessPredictor
from .planner import StudyPlanner
from .recommender import DailyRecommender
from .store import AIStore

__all__ = [
    # Models
    "WeakArea",
    "PreparednessPrediction",
    "StudyPlan",
    "DailyRecommendation",
    "LearningMetrics",
    # Components
    "WeakAreasAnalyzer",
    "PreparednessPredictor",
    "StudyPlanner",
    "DailyRecommender",
    "AIStore",
]
