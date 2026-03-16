"""
Test Generator CLI Commands.

Commands:
  tests generate <tema> --count 10 --type multiple
  tests solve <test_id>
  tests analyze <session_id>
  tests list
  tests history
  tests show <test_id>
"""

import argparse
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.tests import (
    TestStore,
    TestGenerator,
    TestSolver,
    TestAnalyzer,
    TestConfig,
    QuestionType,
    TestMode,
)


def get_store() -> TestStore:
    """Get TestStore instance."""
    return TestStore(db_path="data/tests.db")


def get_generator() -> TestGenerator:
    """Get TestGenerator instance."""
    store = get_store()

    # Try to get temario components
    try:
        from src.temario import TemarioStore, MistralEmbedder, SemanticSearcher
        temario_store = TemarioStore(db_path="data/temario.db")
        embedder = MistralEmbedder()
        searcher = SemanticSearcher(temario_store, embedder)
    except ImportError:
        temario_store = None
        embedder = None
        searcher = None

    return TestGenerator(
        store=store,
        temario_store=temario_store,
        embedder=embedder,
        searcher=searcher,
    )


# ============ Commands ============

def cmd_generate(args):
    """Generate a new test."""
    generator = get_generator()

    # Parse question types
    q_types = []
    if args.type == "multiple":
        q_types.append(QuestionType.MULTIPLE_CHOICE)
    elif args.type == "truefalse":
        q_types.append(QuestionType.TRUE_FALSE)
    elif args.type == "mixed":
        q_types.extend([QuestionType.MULTIPLE_CHOICE, QuestionType.TRUE_FALSE])

    # Create config
    config = TestConfig(
        question_count=args.count,
        question_types=q_types,
        difficulty=args.difficulty,
    )

    print(f"\nGenerating test from Tema {args.tema}...")
    print(f"  Questions: {args.count}")
    print(f"  Type: {args.type}")
    print(f"  Difficulty: {args.difficulty}")

    try:
        # Generate test
        test = generator.generate_from_tema(
            tema=args.tema,
            config=config,
            title=args.title or f"Test - Tema {args.tema}",
        )

        print(f"\n✓ Test generated successfully!")
        print(f"  Test ID: {test.id}")
        print(f"  Title: {test.title}")
        print(f"  Questions: {test.question_count}")
        print(f"\nTo take the test, run:")
        print(f"  python -m src.tests.cli solve {test.id}")

    except Exception as e:
        print(f"\n✗ Error generating test: {e}")
        return 1

    return 0


def cmd_solve(args):
    """Take a test interactively."""
    store = get_store()
    test = store.get_test(args.test_id)

    if not test:
        print(f"✗ Test not found: {args.test_id}")
        return 1

    solver = TestSolver(store)

    # Set mode
    mode = TestMode.EXAM if args.exam else TestMode.PRACTICE

    # Start session
    session = solver.start_session(args.test_id, mode)

    # Run interactive test
    result = solver.run_interactive(test, session)

    if result:
        print(f"\nSession ID: {session.id}")
        print(f"To view detailed analysis, run:")
        print(f"  python -m src.tests.cli analyze {session.id}")

    return 0


def cmd_analyze(args):
    """Analyze a test session."""
    store = get_store()
    analyzer = TestAnalyzer(store)

    try:
        analysis = analyzer.analyze_session(args.session_id)

        print(f"\n{'='*60}")
        print(f"TEST ANALYSIS")
        print(f"{'='*60}")
        print(f"\nTest: {analysis['test_title']}")
        print(f"Date: {analysis['date']}")
        print(f"\nScore: {analysis['score']}%")
        print(f"Status: {'PASSED ✓' if analysis['passed'] else 'NOT PASSED ✗'}")
        print(f"\nResults:")
        print(f"  Correct: {analysis['correct']}/{analysis['total_questions']}")
        print(f"  Incorrect: {analysis['incorrect']}")
        print(f"  Unanswered: {analysis['unanswered']}")
        print(f"\nTime:")
        print(f"  Total: {analysis['time_spent_seconds']:.1f} seconds")
        print(f"  Avg per question: {analysis['avg_time_per_question']:.1f} seconds")

        if analysis['weak_areas']:
            print(f"\nWeak Areas:")
            for area in analysis['weak_areas']:
                print(f"  - {area}")

        if analysis['strong_areas']:
            print(f"\nStrong Areas:")
            for area in analysis['strong_areas']:
                print(f"  - {area}")

        if analysis['recommendations']:
            print(f"\nRecommendations:")
            for rec in analysis['recommendations']:
                print(f"  - {rec}")

    except Exception as e:
        print(f"✗ Error analyzing session: {e}")
        return 1

    return 0


def cmd_list(args):
    """List all tests."""
    store = get_store()
    tests = store.list_tests(limit=args.limit)

    if not tests:
        print("No tests found.")
        print("\nTo generate a test, run:")
        print("  python -m src.tests.cli generate <tema>")
        return 0

    print(f"\n{'='*60}")
    print(f"TESTS ({len(tests)})")
    print(f"{'='*60}\n")

    for test in tests:
        print(f"  [{test.id}] {test.title}")
        print(f"      Questions: {len(test.questions) if test.questions else '?'}")
        print(f"      Created: {test.created_at.strftime('%Y-%m-%d %H:%M')}")
        print()

    return 0


def cmd_history(args):
    """Show test history."""
    store = get_store()
    analyzer = TestAnalyzer(store)

    history = analyzer.get_test_history(test_id=args.test_id, limit=args.limit)

    if not history:
        print("No test history found.")
        print("\nTo take a test, run:")
        print("  python -m src.tests.cli solve <test_id>")
        return 0

    print(f"\n{'='*60}")
    print(f"TEST HISTORY ({len(history)} sessions)")
    print(f"{'='*60}\n")

    for item in history:
        status = "✓" if item['passed'] else "✗"
        print(f"  {status} [{item['session_id']}] {item['test_title']}")
        print(f"      Score: {item['score']}% | Correct: {item['correct']}/{item['total_questions']}")
        print(f"      Time: {item['time_spent_minutes']:.1f} min | Date: {item['date'][:10] if item['date'] else 'N/A'}")
        print()

    return 0


def cmd_show(args):
    """Show test details."""
    store = get_store()
    test = store.get_test(args.test_id)

    if not test:
        print(f"✗ Test not found: {args.test_id}")
        return 1

    print(f"\n{'='*60}")
    print(f"TEST: {test.title}")
    print(f"{'='*60}")
    print(f"\nID: {test.id}")
    print(f"Description: {test.description}")
    print(f"Questions: {test.question_count}")
    print(f"Created: {test.created_at.strftime('%Y-%m-%d %H:%M')}")
    print(f"\nConfig:")
    print(f"  Mode: {test.config.mode.value}")
    print(f"  Difficulty: {test.config.difficulty}")
    print(f"  Time limit: {test.config.time_limit_minutes or 'None'} minutes")

    if test.questions:
        print(f"\nQuestions:")
        for i, q in enumerate(test.questions, 1):
            print(f"  {i}. [{q.question_type.value}] {q.text[:80]}...")

    return 0


def cmd_progress(args):
    """Show progress statistics."""
    store = get_store()
    analyzer = TestAnalyzer(store)

    stats = analyzer.get_progress_stats(days=args.days)

    print(f"\n{'='*60}")
    print(f"PROGRESS REPORT (Last {stats['period_days']} days)")
    print(f"{'='*60}\n")

    print(f"Tests taken: {stats['tests_taken']}")
    print(f"Average score: {stats['average_score']}%")
    print(f"Score range: {stats.get('min_score', 0)}% - {stats.get('max_score', 100)}%")
    print(f"Pass rate: {stats['pass_rate']}%")
    print(f"Total time: {stats['total_time_hours']:.1f} hours")
    print(f"Trend: {stats['trend']}")

    # Show recommendations
    recommendations = analyzer.get_study_recommendations()
    if recommendations:
        print(f"\nRecommendations:")
        for rec in recommendations:
            priority_marker = "!" if rec['priority'] == 'high' else "·"
            print(f"  {priority_marker} {rec['message']}")
            if rec.get('action'):
                print(f"    → {rec['action']}")

    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Test Generator CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a new test")
    gen_parser.add_argument("tema", help="Tema number or name")
    gen_parser.add_argument("--count", type=int, default=10, help="Number of questions")
    gen_parser.add_argument("--type", choices=["multiple", "truefalse", "mixed"], default="multiple", help="Question type")
    gen_parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], default="medium", help="Question difficulty")
    gen_parser.add_argument("--title", help="Test title")

    # solve command
    solve_parser = subparsers.add_parser("solve", help="Take a test")
    solve_parser.add_argument("test_id", help="Test ID")
    solve_parser.add_argument("--exam", action="store_true", help="Exam mode (no feedback)")

    # analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a session")
    analyze_parser.add_argument("session_id", help="Session ID")

    # list command
    list_parser = subparsers.add_parser("list", help="List all tests")
    list_parser.add_argument("--limit", type=int, default=20, help="Max results")

    # history command
    history_parser = subparsers.add_parser("history", help="Show test history")
    history_parser.add_argument("--test-id", help="Filter by test ID")
    history_parser.add_argument("--limit", type=int, default=20, help="Max results")

    # show command
    show_parser = subparsers.add_parser("show", help="Show test details")
    show_parser.add_argument("test_id", help="Test ID")

    # progress command
    progress_parser = subparsers.add_parser("progress", help="Show progress statistics")
    progress_parser.add_argument("--days", type=int, default=30, help="Days to analyze")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Dispatch to command handler
    commands = {
        "generate": cmd_generate,
        "solve": cmd_solve,
        "analyze": cmd_analyze,
        "list": cmd_list,
        "history": cmd_history,
        "show": cmd_show,
        "progress": cmd_progress,
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
