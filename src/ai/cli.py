"""
AI Module CLI - Commands for AI-powered study recommendations.
"""

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer(name="ai", help="AI-powered study recommendations and predictions")
console = Console()


def get_stores():
    """Get store instances."""
    from ..flashcards.store import FlashcardStore
    from ..tests.store import TestStore
    from ..temario.store import TemarioStore
    from .store import AIStore

    data_dir = Path("data")

    flashcard_store = FlashcardStore(str(data_dir / "flashcards.db"))
    test_store = TestStore(str(data_dir / "tests.db"))
    temario_store = TemarioStore(str(data_dir / "temario.db"))
    ai_store = AIStore(str(data_dir / "ai.db"))

    return flashcard_store, test_store, temario_store, ai_store


def get_analyzer(ai_store, flashcard_store, test_store, temario_store):
    """Get analyzer instance."""
    from .analyzer import WeakAreasAnalyzer
    return WeakAreasAnalyzer(ai_store, flashcard_store, test_store, temario_store)


def get_predictor(ai_store, analyzer):
    """Get predictor instance."""
    from .predictor import PreparednessPredictor
    return PreparednessPredictor(ai_store, analyzer)


def get_recommender(ai_store, analyzer, predictor, flashcard_store, test_store):
    """Get recommender instance."""
    from .recommender import DailyRecommender
    return DailyRecommender(ai_store, analyzer, predictor, flashcard_store, test_store)


def get_planner(ai_store, analyzer, flashcard_store, test_store):
    """Get planner instance."""
    from .planner import StudyPlanner
    return StudyPlanner(ai_store, analyzer, flashcard_store, test_store)


@app.command()
def analyze():
    """Analyze weak areas from flashcard and test data."""

    flashcard_store, test_store, temario_store, ai_store = get_stores()
    analyzer = get_analyzer(ai_store, flashcard_store, test_store, temario_store)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing learning data...", total=None)
        weak_areas = analyzer.analyze_all()
        metrics = analyzer.compute_learning_metrics()

    if not weak_areas:
        console.print("[yellow]No weak areas identified. Great job![/yellow]")
        return

    # Display weak areas table
    table = Table(title="Weak Areas Analysis")
    table.add_column("Priority", style="bold")
    table.add_column("Tema/Area")
    table.add_column("Score", justify="right")
    table.add_column("Source")
    table.add_column("Cards", justify="right")
    table.add_column("Tests", justify="right")

    priority_colors = {
        "critical": "red",
        "high": "yellow",
        "medium": "blue",
        "low": "green",
    }

    for area in weak_areas:
        color = priority_colors.get(area.priority.value, "white")
        table.add_row(
            f"[{color}]{area.priority.value.upper()}[/{color}]",
            f"Tema {area.tema}" if area.tema else area.apartado,
            f"{area.combined_score}%",
            area.source,
            str(area.cards_affected),
            str(area.tests_affected),
        )

    console.print(table)

    # Display metrics summary
    console.print()
    metrics_panel = Panel(
        f"[bold]Learning Metrics[/bold]\n\n"
        f"Total Flashcards: {metrics.total_flashcards}\n"
        f"Flashcards Learned: {metrics.flashcards_learned}\n"
        f"Average Ease Factor: {metrics.avg_ease_factor:.2f}\n"
        f"Total Reviews: {metrics.total_reviews}\n\n"
        f"Total Tests: {metrics.total_tests}\n"
        f"Tests Passed: {metrics.tests_passed}\n"
        f"Average Test Score: {metrics.avg_test_score:.1f}%\n\n"
        f"Study Hours: {metrics.study_time_hours:.1f}h\n"
        f"Days Active: {metrics.days_active}",
        title="Summary",
        border_style="blue",
    )
    console.print(metrics_panel)


@app.command()
def predict(
    use_llm: bool = typer.Option(True, "--llm/--no-llm", help="Use LLM for enhanced insights"),
):
    """Predict exam preparedness level."""

    flashcard_store, test_store, temario_store, ai_store = get_stores()
    analyzer = get_analyzer(ai_store, flashcard_store, test_store, temario_store)
    predictor = get_predictor(ai_store, analyzer)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Calculating preparedness prediction...", total=None)
        prediction = predictor.predict(use_llm=use_llm)

    # Determine color based on level
    level_colors = {
        "ready": "green",
        "advanced": "blue",
        "intermediate": "yellow",
        "beginner": "red",
    }
    color = level_colors.get(prediction.level, "white")

    # Display prediction
    console.print()
    console.print(Panel(
        f"[bold {color}]{prediction.level.upper()}[/bold {color}]\n\n"
        f"Overall Score: [bold]{prediction.overall_score}%[/bold]\n"
        f"Confidence: {prediction.confidence * 100:.0f}%\n\n"
        f"Recommended Study: {prediction.recommended_hours_per_week}h/week\n"
        f"Est. Days to Ready: {prediction.estimated_days_to_ready or 'N/A'}",
        title="Preparedness Prediction",
        border_style=color,
    ))

    # Display weak and strong areas
    if prediction.weak_areas:
        console.print(f"\n[red]Weak Areas:[/red] {', '.join(prediction.weak_areas)}")

    if prediction.strong_areas:
        console.print(f"[green]Strong Areas:[/green] {', '.join(prediction.strong_areas)}")

    # Display LLM insights if available
    if prediction.factors.get("llm_insights"):
        console.print("\n[yellow]Key Insights:[/yellow]")
        for insight in prediction.factors["llm_insights"]:
            console.print(f"  - {insight}")

    if prediction.factors.get("motivation"):
        console.print(f"\n[italic]{prediction.factors['motivation']}[/italic]")


@app.command()
def plan(
    hours: Optional[float] = typer.Option(None, "--hours", "-h", help="Target study hours per week"),
    start: Optional[str] = typer.Option(None, "--start", "-s", help="Start date (YYYY-MM-DD)"),
):
    """Generate a weekly study plan."""

    flashcard_store, test_store, temario_store, ai_store = get_stores()
    analyzer = get_analyzer(ai_store, flashcard_store, test_store, temario_store)
    planner = get_planner(ai_store, analyzer, flashcard_store, test_store)

    # Parse start date if provided
    start_date = None
    if start:
        try:
            start_date = date.fromisoformat(start)
        except ValueError:
            console.print("[red]Invalid date format. Use YYYY-MM-DD[/red]")
            raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generating study plan...", total=None)
        study_plan = planner.generate_weekly_plan(
            start_date=start_date,
            total_hours=hours,
        )

    # Display plan summary
    console.print()
    console.print(Panel(
        f"[bold]Week: {study_plan.week_start} to {study_plan.week_end}[/bold]\n\n"
        f"Total Hours: {study_plan.total_hours}h\n"
        f"Total Tasks: {len(study_plan.tasks)}\n"
        f"Focus Areas: {', '.join(study_plan.focus_areas) if study_plan.focus_areas else 'General'}",
        title="Weekly Study Plan",
        border_style="green",
    ))

    # Display goals
    if study_plan.goals:
        console.print("\n[bold]Goals:[/bold]")
        for i, goal in enumerate(study_plan.goals, 1):
            console.print(f"  {i}. {goal}")

    # Display daily breakdown
    console.print("\n[bold]Daily Schedule:[/bold]")
    table = Table()
    table.add_column("Day", style="bold")
    table.add_column("Tasks")
    table.add_column("Time", justify="right")

    day_order = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for day in day_order:
        tasks = study_plan.daily_breakdown.get(day, [])
        if tasks:
            task_list = "\n".join([f"- {t.description}" for t in tasks])
            total_time = sum(t.duration_minutes for t in tasks)
            table.add_row(day.capitalize(), task_list, f"{total_time}min")
        else:
            table.add_row(day.capitalize(), "[dim]Rest day[/dim]", "-")

    console.print(table)


@app.command()
def today(
    refresh: bool = typer.Option(False, "--refresh", "-r", help="Regenerate recommendations"),
):
    """Get today's study recommendations."""

    flashcard_store, test_store, temario_store, ai_store = get_stores()
    analyzer = get_analyzer(ai_store, flashcard_store, test_store, temario_store)
    predictor = get_predictor(ai_store, analyzer)
    recommender = get_recommender(ai_store, analyzer, predictor, flashcard_store, test_store)

    recommendations = recommender.get_recommendations(refresh=refresh)

    if not recommendations:
        console.print("[yellow]No recommendations for today. Take a break![/yellow]")
        return

    console.print(f"\n[bold]Today's Study Recommendations ({date.today()})[/bold]\n")

    priority_colors = {
        "critical": "red",
        "high": "yellow",
        "medium": "blue",
        "low": "green",
    }

    for i, rec in enumerate(recommendations, 1):
        color = priority_colors.get(rec.priority.value, "white")
        status = "[green]Done[/green]" if rec.completed else "[dim]Pending[/dim]"

        console.print(Panel(
            f"[bold]{rec.title}[/bold]\n\n"
            f"{rec.description}\n\n"
            f"[italic]{rec.action}[/italic]\n\n"
            f"Time: {rec.estimated_minutes}min | Reason: {rec.reason}",
            title=f"[{color}]#{i} - {rec.priority.value.upper()}[/{color}]",
            subtitle=status,
            border_style=color,
        ))


@app.command()
def complete(
    recommendation_id: int = typer.Argument(..., help="Recommendation ID to mark complete"),
):
    """Mark a recommendation as completed."""

    flashcard_store, test_store, temario_store, ai_store = get_stores()
    analyzer = get_analyzer(ai_store, flashcard_store, test_store, temario_store)
    predictor = get_predictor(ai_store, analyzer)
    recommender = get_recommender(ai_store, analyzer, predictor, flashcard_store, test_store)

    if recommender.complete_recommendation(recommendation_id):
        console.print(f"[green]Recommendation #{recommendation_id} marked as completed![/green]")
    else:
        console.print(f"[red]Failed to mark recommendation as completed.[/red]")
        raise typer.Exit(1)


@app.command()
def status():
    """Show overall AI analytics status."""

    flashcard_store, test_store, temario_store, ai_store = get_stores()

    # Get latest data
    prediction = ai_store.get_latest_prediction()
    metrics = ai_store.get_learning_metrics()
    weak_areas = ai_store.get_weak_areas(limit=5)

    console.print("\n[bold]AI Analytics Status[/bold]\n")

    # Prediction status
    if prediction:
        level_colors = {"ready": "green", "advanced": "blue", "intermediate": "yellow", "beginner": "red"}
        color = level_colors.get(prediction.level, "white")
        console.print(f"Preparedness: [bold {color}]{prediction.overall_score}% ({prediction.level})[/bold {color}]")
        console.print(f"  Last prediction: {prediction.created_at}")
    else:
        console.print("Preparedness: [dim]No prediction yet. Run 'predict' command.[/dim]")

    # Weak areas count
    critical = len([a for a in weak_areas if a.priority.value == "critical"])
    high = len([a for a in weak_areas if a.priority.value == "high"])
    console.print(f"\nWeak Areas: {len(weak_areas)} ({critical} critical, {high} high)")

    # Metrics summary
    if metrics:
        console.print(f"\n[bold]Learning Stats:[/bold]")
        console.print(f"  Flashcards: {metrics.total_flashcards} ({metrics.flashcards_learned} learned)")
        console.print(f"  Tests: {metrics.total_tests} ({metrics.tests_passed} passed)")
        console.print(f"  Study Time: {metrics.study_time_hours:.1f}h")
        console.print(f"  Streak: {metrics.streak_days} days")

    # Current plan
    planner = get_planner(ai_store, None, None, None)
    plan = planner.get_current_plan()

    if plan:
        console.print(f"\n[bold]Current Plan:[/bold]")
        console.print(f"  Week: {plan.week_start} to {plan.week_end}")
        console.print(f"  Total Hours: {plan.total_hours}h")
        completed = sum(1 for t in plan.tasks if t.completed)
        console.print(f"  Progress: {completed}/{len(plan.tasks)} tasks completed")
    else:
        console.print(f"\n[dim]No active study plan. Run 'plan' command to generate one.[/dim]")


@app.command()
def export(
    output: str = typer.Option("ai_report.json", "--output", "-o", help="Output file path"),
):
    """Export AI analytics to JSON."""

    flashcard_store, test_store, temario_store, ai_store = get_stores()
    analyzer = get_analyzer(ai_store, flashcard_store, test_store, temario_store)
    predictor = get_predictor(ai_store, analyzer)

    # Run full analysis
    weak_areas = analyzer.analyze_all()
    metrics = analyzer.compute_learning_metrics()
    prediction = predictor.predict(use_llm=True)

    report = {
        "generated_at": date.today().isoformat(),
        "prediction": prediction.to_dict(),
        "metrics": metrics.to_dict() if metrics else None,
        "weak_areas": [a.to_dict() for a in weak_areas],
    }

    with open(output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    console.print(f"[green]Report exported to {output}[/green]")


if __name__ == "__main__":
    app()
