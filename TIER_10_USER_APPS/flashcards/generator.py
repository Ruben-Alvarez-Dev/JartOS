"""
Generator - AI-powered flashcard generation from temario chunks.

Generates question-answer pairs from temario content.
"""

import json
import logging
from typing import List, Optional
from dataclasses import dataclass

from .models import Flashcard, Deck
from .store import FlashcardStore

logger = logging.getLogger(__name__)


@dataclass
class GeneratedCard:
    """A generated flashcard before saving."""
    front: str
    back: str
    source_chunk_id: Optional[int] = None
    confidence: float = 1.0


class FlashcardGenerator:
    """
    Generates flashcards from temario content.

    Strategies:
    - Definition extraction
    - Key concept Q&A
    - Fact-based questions
    """

    def __init__(
        self,
        store: FlashcardStore,
        temario_store=None,
        min_confidence: float = 0.7,
    ):
        """
        Initialize the generator.

        Args:
            store: FlashcardStore instance
            temario_store: Optional TemarioStore for chunk access
            min_confidence: Minimum confidence for auto-approval
        """
        self.store = store
        self.temario_store = temario_store
        self.min_confidence = min_confidence

    def generate_from_text(
        self,
        text: str,
        source_chunk_id: Optional[int] = None,
    ) -> List[GeneratedCard]:
        """
        Generate flashcards from a text chunk.

        Uses simple heuristics to extract Q&A pairs.

        Args:
            text: Text content to process
            source_chunk_id: Optional chunk ID reference

        Returns:
            List of generated cards
        """
        cards = []

        # Strategy 1: Definition extraction
        cards.extend(self._extract_definitions(text, source_chunk_id))

        # Strategy 2: Key concept questions
        cards.extend(self._extract_concepts(text, source_chunk_id))

        # Strategy 3: Fact-based questions
        cards.extend(self._extract_facts(text, source_chunk_id))

        return cards

    def _extract_definitions(
        self,
        text: str,
        source_chunk_id: Optional[int],
    ) -> List[GeneratedCard]:
        """Extract definition-based cards."""
        cards = []

        # Common definition patterns
        patterns = [
            (" se define como ", " se define como "),
            (": ", ": "),  # Colon patterns
            (" es ", " es "),
            (" significa ", " significa "),
        ]

        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line or len(line) < 20:
                continue

            # Look for definition patterns
            for sep_before, sep_after in patterns:
                if sep_before in line.lower():
                    parts = line.split(sep_after, 1)
                    if len(parts) == 2:
                        term = parts[0].strip()
                        definition = parts[1].strip()

                        if len(term) > 3 and len(definition) > 10:
                            # Create definition card
                            cards.append(GeneratedCard(
                                front=f"Definicion: {term}",
                                back=definition,
                                source_chunk_id=source_chunk_id,
                                confidence=0.8,
                            ))
                            break

        return cards

    def _extract_concepts(
        self,
        text: str,
        source_chunk_id: Optional[int],
    ) -> List[GeneratedCard]:
        """Extract concept-based cards."""
        cards = []

        # Look for enumerated items
        lines = text.split('\n')
        current_context = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Track context (previous non-item lines)
            if not (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                if len(line) > 20:
                    current_context = line[:100]

            # Extract items that look like key points
            if line[0].isdigit() and '.' in line[:3]:
                # Remove number prefix
                content = line.split('.', 1)[-1].strip()
                if len(content) > 10:
                    # Create what-is question
                    if current_context:
                        cards.append(GeneratedCard(
                            front=f"Que es: {content[:80]}",
                            back=current_context,
                            source_chunk_id=source_chunk_id,
                            confidence=0.6,
                        ))

        return cards

    def _extract_facts(
        self,
        text: str,
        source_chunk_id: Optional[int],
    ) -> List[GeneratedCard]:
        """Extract fact-based cards."""
        cards = []

        # Look for sentences with specific patterns
        fact_patterns = [
            "el plazo",
            "la fecha",
            "el numero",
            "el porcentaje",
            "el importe",
            "la cantidad",
            "el limite",
            "el requisito",
        ]

        sentences = text.replace('\n', ' ').split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence or len(sentence) < 20:
                continue

            lower = sentence.lower()
            for pattern in fact_patterns:
                if pattern in lower:
                    # Create fact-based question
                    question = f"Cual es {pattern} {' '.join(sentence.split()[3:8])}?"
                    cards.append(GeneratedCard(
                        front=question,
                        back=sentence,
                        source_chunk_id=source_chunk_id,
                        confidence=0.5,
                    ))
                    break

        return cards

    def generate_from_chunk(
        self,
        chunk_id: int,
    ) -> List[GeneratedCard]:
        """
        Generate flashcards from a temario chunk.

        Args:
            chunk_id: Chunk ID to process

        Returns:
            List of generated cards
        """
        if not self.temario_store:
            raise ValueError("TemarioStore not configured")

        chunk = self.temario_store.get_chunk(chunk_id)
        if not chunk:
            logger.warning(f"Chunk {chunk_id} not found")
            return []

        return self.generate_from_text(chunk.content, chunk_id)

    def generate_from_tema(
        self,
        tema: int,
        limit: int = 50,
    ) -> List[GeneratedCard]:
        """
        Generate flashcards from all chunks in a tema.

        Args:
            tema: Tema number
            limit: Maximum cards to generate

        Returns:
            List of generated cards
        """
        if not self.temario_store:
            raise ValueError("TemarioStore not configured")

        chunks = self.temario_store.get_chunks_by_tema(tema)
        all_cards = []

        for chunk in chunks[:limit]:
            cards = self.generate_from_text(chunk.content, chunk.id)
            all_cards.extend(cards)

            if len(all_cards) >= limit:
                break

        return all_cards[:limit]

    def save_generated_cards(
        self,
        deck_id: int,
        cards: List[GeneratedCard],
        auto_approve: bool = False,
    ) -> List[Flashcard]:
        """
        Save generated cards to the database.

        Args:
            deck_id: Deck ID to save to
            cards: Generated cards
            auto_approve: Auto-approve high-confidence cards

        Returns:
            List of saved Flashcard objects
        """
        saved = []

        for gen_card in cards:
            # Filter by confidence if auto-approve is off
            if not auto_approve and gen_card.confidence < self.min_confidence:
                logger.debug(f"Skipping low-confidence card: {gen_card.front[:50]}")
                continue

            card = Flashcard(
                deck_id=deck_id,
                front=gen_card.front,
                back=gen_card.back,
                source_chunk_id=gen_card.source_chunk_id,
            )

            try:
                saved_card = self.store.create_flashcard(card)
                saved.append(saved_card)
            except Exception as e:
                logger.error(f"Failed to save card: {e}")

        logger.info(f"Saved {len(saved)} cards to deck {deck_id}")
        return saved

    def export_for_review(
        self,
        cards: List[GeneratedCard],
        output_path: str,
    ) -> int:
        """
        Export generated cards to JSON for manual review.

        Args:
            cards: Generated cards
            output_path: Output file path

        Returns:
            Number of cards exported
        """
        data = {
            "generated_cards": [
                {
                    "front": card.front,
                    "back": card.back,
                    "source_chunk_id": card.source_chunk_id,
                    "confidence": card.confidence,
                }
                for card in cards
            ]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Exported {len(cards)} cards to {output_path}")
        return len(cards)


def generate_for_deck(
    deck_id: int,
    text: str,
    store: FlashcardStore,
    auto_approve: bool = False,
) -> List[Flashcard]:
    """
    Convenience function to generate and save cards for a deck.

    Args:
        deck_id: Deck ID
        text: Source text
        store: FlashcardStore instance
        auto_approve: Auto-approve high-confidence cards

    Returns:
        List of saved Flashcard objects
    """
    generator = FlashcardGenerator(store)
    generated = generator.generate_from_text(text)
    return generator.save_generated_cards(deck_id, generated, auto_approve)
