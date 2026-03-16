"""
Test Generator - AI-powered test generation from temario chunks.

Uses RAG pattern: retrieve relevant chunks → generate questions via LLM.
"""

import os
import time
from typing import Optional
import json

from .models import (
    Test,
    Question,
    TestConfig,
    QuestionType,
    TestMode,
)


class MiniMaxClient:
    """Client for MiniMax API (LLM for question generation)."""

    def __init__(self, api_key: Optional[str] = None, model: str = "MiniMax-Text-01"):
        """
        Initialize MiniMax client.

        Args:
            api_key: MiniMax API key (defaults to MINIMAX_API_KEY env var)
            model: Model to use for generation
        """
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        self.model = model
        self.base_url = "https://api.minimax.chat/v1"
        self.group_id = os.getenv("MINIMAX_GROUP_ID", "")

    def generate(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate text using MiniMax API.

        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text
        """
        if not self.api_key:
            # Fallback: use a simple template-based generation for testing
            return self._fallback_generate(prompt)

        try:
            import httpx

            url = f"{self.base_url}/text/chatcompletion_v2"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
            }

            response = httpx.post(url, json=payload, headers=headers, timeout=60.0)
            response.raise_for_status()

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"MiniMax API error: {e}")
            return self._fallback_generate(prompt)

    def _fallback_generate(self, prompt: str) -> str:
        """Fallback generation when API is not available."""
        # Extract topic from prompt and create a simple question
        return json.dumps({
            "question": "Based on the provided content, what is the main concept?",
            "options": [
                "Option A: The primary concept discussed",
                "Option B: A secondary concept",
                "Option C: An unrelated concept",
                "Option D: None of the above"
            ],
            "correct_index": 0,
            "explanation": "The primary concept is the main topic discussed in the provided content."
        })


class TestGenerator:
    """Generates tests from temario content using LLM."""

    def __init__(
        self,
        store,
        temario_store,
        embedder=None,
        searcher=None,
        llm_client: Optional[MiniMaxClient] = None,
    ):
        """
        Initialize test generator.

        Args:
            store: TestStore instance
            temario_store: TemarioStore instance
            embedder: MistralEmbedder instance
            searcher: SemanticSearcher instance
            llm_client: MiniMaxClient for question generation
        """
        self.store = store
        self.temario_store = temario_store
        self.embedder = embedder
        self.searcher = searcher
        self.llm = llm_client or MiniMaxClient()

    def generate_from_tema(
        self,
        tema: str,
        config: Optional[TestConfig] = None,
        title: Optional[str] = None,
    ) -> Test:
        """
        Generate a test from a specific tema.

        Args:
            tema: Tema number or name
            config: Test configuration
            title: Test title

        Returns:
            Generated Test with questions
        """
        config = config or TestConfig()
        config.temas = [tema]

        # Get chunks from tema
        chunks = self._get_chunks_from_tema(tema, config.question_count * 2)

        # Generate questions from chunks
        questions = self._generate_questions_from_chunks(chunks, config)

        # Create test
        test = Test(
            title=title or f"Test - Tema {tema}",
            description=f"Auto-generated test from Tema {tema}",
            config=config,
            questions=questions,
        )

        # Set test_id on questions
        for q in questions:
            q.test_id = test.id

        # Save test
        self.store.save_test(test)

        return test

    def generate_from_chunks(
        self,
        chunk_ids: list[str],
        config: Optional[TestConfig] = None,
        title: Optional[str] = None,
    ) -> Test:
        """
        Generate a test from specific chunks.

        Args:
            chunk_ids: List of chunk IDs
            config: Test configuration
            title: Test title

        Returns:
            Generated Test
        """
        config = config or TestConfig()

        # Get chunks
        chunks = []
        for chunk_id in chunk_ids:
            chunk = self.temario_store.get_chunk(chunk_id)
            if chunk:
                chunks.append(chunk)

        # Generate questions
        questions = self._generate_questions_from_chunks(chunks, config)

        # Create test
        test = Test(
            title=title or "Custom Test",
            description="Test from selected content",
            config=config,
            questions=questions,
        )

        for q in questions:
            q.test_id = test.id

        self.store.save_test(test)

        return test

    def generate_from_query(
        self,
        query: str,
        config: Optional[TestConfig] = None,
        title: Optional[str] = None,
    ) -> Test:
        """
        Generate a test from a semantic search query.

        Args:
            query: Search query for relevant content
            config: Test configuration
            title: Test title

        Returns:
            Generated Test
        """
        config = config or TestConfig()

        # Search for relevant chunks
        chunks = self._search_chunks(query, config.question_count * 2)

        # Generate questions
        questions = self._generate_questions_from_chunks(chunks, config)

        # Create test
        test = Test(
            title=title or f"Test: {query}",
            description=f"Auto-generated test for: {query}",
            config=config,
            questions=questions,
        )

        for q in questions:
            q.test_id = test.id

        self.store.save_test(test)

        return test

    def _get_chunks_from_tema(self, tema: str, count: int) -> list:
        """Get chunks from a specific tema."""
        # Try to get chunks from temario store
        try:
            all_chunks = self.temario_store.list_chunks()
            tema_chunks = [
                c for c in all_chunks
                if str(c.tema) == str(tema) or tema.lower() in str(c.tema).lower()
            ]
            return tema_chunks[:count]
        except Exception:
            return []

    def _search_chunks(self, query: str, count: int) -> list:
        """Search for relevant chunks using semantic search."""
        if self.searcher:
            try:
                results = self.searcher.search(query, top_k=count)
                return [r["chunk"] for r in results]
            except Exception:
                pass

        # Fallback: return empty (no semantic search available)
        return []

    def _generate_questions_from_chunks(
        self,
        chunks: list,
        config: TestConfig,
    ) -> list[Question]:
        """Generate questions from a list of chunks."""
        questions = []
        question_types = config.question_types or [QuestionType.MULTIPLE_CHOICE]

        for i in range(config.question_count):
            if not chunks:
                break

            # Select chunk (cycle through if needed)
            chunk = chunks[i % len(chunks)]

            # Select question type (cycle through types)
            q_type = question_types[i % len(question_types)]

            # Generate question
            question = self._generate_single_question(chunk, q_type, config.difficulty)
            if question:
                questions.append(question)

            # Small delay to avoid rate limits
            time.sleep(0.1)

        return questions

    def _generate_single_question(
        self,
        chunk,
        question_type: QuestionType,
        difficulty: str,
    ) -> Optional[Question]:
        """Generate a single question from a chunk using LLM."""
        # Build prompt
        prompt = self._build_question_prompt(chunk, question_type, difficulty)

        # Generate
        try:
            response = self.llm.generate(prompt, temperature=0.7)
            return self._parse_llm_response(response, chunk, question_type, difficulty)
        except Exception as e:
            print(f"Error generating question: {e}")
            return None

    def _build_question_prompt(self, chunk, question_type: QuestionType, difficulty: str) -> str:
        """Build prompt for LLM question generation."""
        content = chunk.content[:1000] if len(chunk.content) > 1000 else chunk.content

        if question_type == QuestionType.MULTIPLE_CHOICE:
            return f"""Generate a multiple-choice question based on the following content.

Content:
{content}

Requirements:
- Difficulty: {difficulty}
- Create a clear, unambiguous question
- Provide exactly 4 options (A, B, C, D)
- Only one correct answer
- Include an explanation

Return as JSON:
{{
    "question": "The question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_index": 0,
    "explanation": "Why this is correct"
}}"""

        elif question_type == QuestionType.TRUE_FALSE:
            return f"""Generate a true/false question based on the following content.

Content:
{content}

Requirements:
- Difficulty: {difficulty}
- Create a clear statement that is definitively true or false
- Include an explanation

Return as JSON:
{{
    "question": "The statement",
    "options": ["True", "False"],
    "correct_index": 0,
    "explanation": "Why this is true/false"
}}"""

        else:  # OPEN_ENDED
            return f"""Generate an open-ended question based on the following content.

Content:
{content}

Requirements:
- Difficulty: {difficulty}
- Create a question that requires a short written answer
- Include expected key points in the explanation

Return as JSON:
{{
    "question": "The question text",
    "options": [],
    "correct_index": 0,
    "explanation": "Key points the answer should include"
}}"""

    def _parse_llm_response(
        self,
        response: str,
        chunk,
        question_type: QuestionType,
        difficulty: str,
    ) -> Optional[Question]:
        """Parse LLM response into a Question object."""
        try:
            # Try to extract JSON from response
            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)

                return Question(
                    question_type=question_type,
                    text=data.get("question", ""),
                    options=data.get("options", []),
                    correct_index=data.get("correct_index", 0),
                    explanation=data.get("explanation", ""),
                    difficulty=difficulty,
                    source_chunk_ids=[chunk.id] if hasattr(chunk, "id") else [],
                )

        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")

        # Fallback: create a basic question
        return Question(
            question_type=question_type,
            text=f"Question about: {chunk.titulo if hasattr(chunk, 'titulo') else 'content'}",
            options=["Option A", "Option B", "Option C", "Option D"],
            correct_index=0,
            explanation="Generated question",
            difficulty=difficulty,
            source_chunk_ids=[chunk.id] if hasattr(chunk, "id") else [],
        )
