"""
CLI commands for the flashcards system.

Commands:
    flashcards create-deck <name> [--description <desc>] [--tema <id>]
    flashcards create <deck> "<front>" "<back>"
    flashcards import <deck> <file.json>
    flashcards review <deck>
    flashcards list [--deck <name>]
    flashcards stats [<deck>]
    flashcards delete <card_id>
    flashcards preview <deck>
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .models import Deck, Flashcard
from .store import FlashcardStore
from .scheduler import SM2Scheduler
from .reviewer import Reviewer


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="flashcards",
        description="Flashcard system with SM-2 spaced repetition"
    )
    parser.add_argument(
        "--db",
        default="data/flashcards.db",
        help="Path to SQLite database (default: data/flashcards.db)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # create-deck
    create_deck = subparsers.add_parser("create-deck", help="Create a new deck")
    create_deck.add_argument("name", help="Deck name")
    create_deck.add_argument("--description", "-d", default="", help="Deck description")
    create_deck.add_argument("--tema", "-t", type=int, help="Associated tema ID")

    # create
    create = subparsers.add_parser("create", help="Create a flashcard")
    create.add_argument("deck", help="Deck name or ID")
    create.add_argument("front", help="Front of card (question)")
    create.add_argument("back", help="Back of card (answer)")

    # import
    import_cmd = subparsers.add_parser("import", help="Import flashcards from JSON")
    import_cmd.add_argument("deck", help="Deck name or ID")
    import_cmd.add_argument("file", help="JSON file with cards")

    # review
    review = subparsers.add_parser("review", help="Start a review session")
    review.add_argument("deck", help="Deck name or ID")
    review.add_argument("--no-new", action="store_true", help="Skip new cards")
    review.add_argument("--no-due", action="store_true", help="Skip due cards")

    # list
    list_cmd = subparsers.add_parser("list", help="List flashcards")
    list_cmd.add_argument("--deck", "-d", help="Filter by deck name or ID")
    list_cmd.add_argument("--limit", "-l", type=int, default=20, help="Max cards to show")

    # stats
    stats = subparsers.add_parser("stats", help="Show statistics")
    stats.add_argument("deck", nargs="?", help="Deck name or ID (optional)")

    # delete
    delete = subparsers.add_parser("delete", help="Delete a flashcard")
    delete.add_argument("card_id", type=int, help="Card ID to delete")

    # preview
    preview = subparsers.add_parser("preview", help="Preview review session")
    preview.add_argument("deck", help="Deck name or ID")

    # scheduler-preview
    sched_preview = subparsers.add_parser(
        "scheduler-preview",
        help="Preview SM-2 interval progression"
    )
    sched_preview.add_argument("rating", type=int, help="Rating to simulate (0-5)")
    sched_preview.add_argument(
        "--count", "-c", type=int, default=5, help="Number of reviews"
    )

    return parser


def resolve_deck(store: FlashcardStore, deck_ref: str) -> Optional[Deck]:
    """Resolve deck by name or ID."""
    # Try as ID first
    try:
        deck_id = int(deck_ref)
        return store.get_deck(deck_id)
    except ValueError:
        pass

    # Try as name
    return store.get_deck_by_name(deck_ref)


def cmd_create_deck(args, store: FlashcardStore) -> int:
    """Create a new deck."""
    # Check if deck exists
    existing = store.get_deck_by_name(args.name)
    if existing:
        print(f"Error: Deck '{args.name}' already exists (id={existing.id})")
        return 1

    deck = Deck(
        name=args.name,
        description=args.description,
        tema_id=args.tema,
    )
    created = store.create_deck(deck)
    print(f"Created deck: {created.name} (id={created.id})")
    return 0


def cmd_create(args, store: FlashcardStore) -> int:
    """Create a flashcard."""
    deck = resolve_deck(store, args.deck)
    if not deck:
        print(f"Error: Deck '{args.deck}' not found")
        return 1

    card = Flashcard(
        deck_id=deck.id,
        front=args.front,
        back=args.back,
    )
    created = store.create_flashcard(card)
    print(f"Created card {created.id} in deck '{deck.name}'")
    print(f"  Q: {created.front}")
    print(f"  A: {created.back}")
    return 0


def cmd_import(args, store: FlashcardStore) -> int:
    """Import flashcards from JSON file."""
    deck = resolve_deck(store, args.deck)
    if not deck:
        print(f"Error: Deck '{args.deck}' not found")
        return 1

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{args.file}' not found")
        return 1

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Support both array format and object with 'cards' key
        if isinstance(data, dict) and 'cards' in data:
            cards_data = data['cards']
        elif isinstance(data, list):
            cards_data = data
        else:
            print("Error: Invalid JSON format. Expected array or {cards: [...]}")
            return 1

        cards = []
        for item in cards_data:
            if 'front' not in item or 'back' not in item:
                print(f"Warning: Skipping invalid card: {item}")
                continue

            card = Flashcard(
                deck_id=deck.id,
                front=item['front'],
                back=item['back'],
                source_chunk_id=item.get('source_chunk_id'),
            )
            cards.append(card)

        if not cards:
            print("No valid cards found in file")
            return 1

        created = store.create_flashcards_batch(cards)
        print(f"Imported {len(created)} cards into deck '{deck.name}'")
        return 0

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_review(args, store: FlashcardStore) -> int:
    """Start an interactive review session."""
    deck = resolve_deck(store, args.deck)
    if not deck:
        print(f"Error: Deck '{args.deck}' not found")
        return 1

    scheduler = SM2Scheduler()
    reviewer = Reviewer(store, scheduler)

    # Preview first
    preview = reviewer.preview_review_cards(deck.id)
    print(f"\nDeck: {preview['deck_name']}")
    print(f"Cards due: {preview['due_count']}")
    print(f"New cards: {preview['new_count']}")
    print(f"Will review: {preview['total_to_review']} cards")

    if preview['total_to_review'] == 0:
        print("\nNo cards to review! Great job!")
        return 0

    print("\nStarting review session...")
    print("Press Ctrl+C at any time to stop.\n")

    try:
        session = reviewer.run_interactive_session(
            deck.id,
            include_new=not args.no_new,
            include_due=not args.no_due,
        )

        # Show summary
        print("\n" + "=" * 60)
        print("SESSION SUMMARY")
        print("=" * 60)
        print(f"Cards reviewed: {session.cards_reviewed}")
        print(f"Correct: {session.cards_correct}")
        print(f"Again: {session.cards_again}")
        print(f"Accuracy: {session.accuracy:.1f}%")
        print(f"Duration: {session.duration_seconds:.1f} seconds")
        print("=" * 60)

        return 0

    except KeyboardInterrupt:
        print("\n\nSession cancelled")
        return 0


def cmd_list(args, store: FlashcardStore) -> int:
    """List flashcards."""
    if args.deck:
        deck = resolve_deck(store, args.deck)
        if not deck:
            print(f"Error: Deck '{args.deck}' not found")
            return 1
        cards = store.get_flashcards_by_deck(deck.id, limit=args.limit)
        deck_name = deck.name
    else:
        # List all decks with card counts
        decks = store.list_decks(limit=100)
        if not decks:
            print("No decks found. Create one with 'flashcards create-deck <name>'")
            return 0

        print("DECKS:")
        print("-" * 60)
        for deck in decks:
            stats = store.get_deck_stats(deck.id)
            print(f"  {deck.id:3d}. {deck.name}")
            print(f"       Cards: {stats.total_cards} | Due: {stats.due_cards} | New: {stats.new_cards}")
            if deck.description:
                print(f"       {deck.description}")
        return 0

    if not cards:
        print(f"No cards in deck '{deck_name}'")
        return 0

    print(f"CARDS IN '{deck_name}':")
    print("-" * 60)
    for card in cards:
        status = "NEW" if card.is_new else f"due:{card.next_review}"
        print(f"  [{card.id}] {status}")
        print(f"      Q: {card.front[:50]}{'...' if len(card.front) > 50 else ''}")
        print(f"      A: {card.back[:50]}{'...' if len(card.back) > 50 else ''}")
        print(f"      ease: {card.ease_factor:.2f} | interval: {card.interval}d | reps: {card.repetitions}")
        print()

    return 0


def cmd_stats(args, store: FlashcardStore) -> int:
    """Show statistics."""
    if args.deck:
        deck = resolve_deck(store, args.deck)
        if not deck:
            print(f"Error: Deck '{args.deck}' not found")
            return 1

        stats = store.get_deck_stats(deck.id)
        print(f"\nSTATS FOR '{stats.deck_name}':")
        print("=" * 40)
        print(f"Total cards:    {stats.total_cards}")
        print(f"New cards:      {stats.new_cards}")
        print(f"Due today:      {stats.due_cards}")
        print(f"Learned:        {stats.learned_cards}")
        print(f"Total reviews:  {stats.total_reviews}")
        print(f"Avg ease:       {stats.average_ease_factor:.2f}")
        print("=" * 40)
    else:
        stats = store.get_all_stats()
        print("\nGLOBAL STATISTICS:")
        print("=" * 40)
        print(f"Total decks:      {stats['total_decks']}")
        print(f"Total cards:      {stats['total_cards']}")
        print(f"Total reviews:    {stats['total_reviews']}")
        print(f"Cards due today:  {stats['cards_due_today']}")
        print(f"Average ease:     {stats['average_ease_factor']:.2f}")
        print("=" * 40)

    return 0


def cmd_delete(args, store: FlashcardStore) -> int:
    """Delete a flashcard."""
    card = store.get_flashcard(args.card_id)
    if not card:
        print(f"Error: Card {args.card_id} not found")
        return 1

    # Confirm
    print(f"Delete card {args.card_id}?")
    print(f"  Q: {card.front}")
    print(f"  A: {card.back}")
    response = input("Confirm (y/N): ")

    if response.lower() != 'y':
        print("Cancelled")
        return 0

    deleted = store.delete_flashcard(args.card_id)
    if deleted:
        print(f"Deleted card {args.card_id}")
        return 0
    else:
        print("Failed to delete card")
        return 1


def cmd_preview(args, store: FlashcardStore) -> int:
    """Preview a review session."""
    deck = resolve_deck(store, args.deck)
    if not deck:
        print(f"Error: Deck '{args.deck}' not found")
        return 1

    scheduler = SM2Scheduler()
    reviewer = Reviewer(store, scheduler)

    preview = reviewer.preview_review_cards(deck.id)
    print(f"\nREVIEW PREVIEW FOR '{preview['deck_name']}':")
    print("=" * 40)
    print(f"Due cards available:  {preview['due_count']}")
    print(f"New cards available:  {preview['new_count']}")
    print("-" * 40)
    print(f"Due cards to review:  {preview['due_to_review']}")
    print(f"New cards to review:  {preview['new_to_review']}")
    print(f"Total to review:      {preview['total_to_review']}")
    print("=" * 40)

    return 0


def cmd_scheduler_preview(args, store: FlashcardStore) -> int:
    """Preview SM-2 interval progression."""
    if not 0 <= args.rating <= 5:
        print("Error: Rating must be 0-5")
        return 1

    scheduler = SM2Scheduler()
    intervals = scheduler.preview_intervals(args.rating, args.count)

    print(f"\nSM-2 INTERVAL PROGRESSION (rating={args.rating}):")
    print("=" * 40)
    for i, interval in enumerate(intervals, 1):
        print(f"  Review {i}: {interval} day(s)")
    print("=" * 40)

    return 0


def main(argv: Optional[list] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    # Initialize store
    store = FlashcardStore(db_path=args.db)

    # Dispatch command
    commands = {
        "create-deck": cmd_create_deck,
        "create": cmd_create,
        "import": cmd_import,
        "review": cmd_review,
        "list": cmd_list,
        "stats": cmd_stats,
        "delete": cmd_delete,
        "preview": cmd_preview,
        "scheduler-preview": cmd_scheduler_preview,
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args, store)
    else:
        print(f"Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
