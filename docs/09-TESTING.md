# Estrategia de Testing

**Version:** 0.1.0
**Ultima actualizacion:** 2025-03-16

---

## Indice

1. [Vision General](#1-vision-general)
2. [Estructura de Tests](#2-estructura-de-tests)
3. [Convenciones de Testing](#3-convenciones-de-testing)
4. [Cobertura de Codigo](#4-cobertura-de-codigo)
5. [Comandos de pytest](#5-comandos-de-pytest)
6. [CI/CD Integration](#6-cicd-integration)
7. [Tests por Modulo](#7-tests-por-modulo)

---

## 1. Vision General

### 1.1 Piramide de Testing

```
                    +-----------+
                   /     E2E     \          # Pocos, lentos, caros
                  /---------------\
                 /   Integration   \        # Moderados
                /-------------------\
               /      Unit Tests     \      # Muchos, rapidos, baratos
              /-----------------------\
             /      Static Analysis     \   # Todo el codigo
            +---------------------------+
```

### 1.2 Tipos de Tests

| Tipo | Proporcion | Velocidad | Proposito |
|------|------------|-----------|-----------|
| Unit | 70% | Rapido (<1s) | Logica individual |
| Integration | 20% | Medio (<10s) | Interaccion entre modulos |
| E2E | 10% | Lento (<60s) | Flujos completos |

### 1.3 Cobertura Requerida

| Modulo | Cobertura Minima | Cobertura Objetivo |
|--------|------------------|-------------------|
| src/temario/ | 80% | 90% |
| src/flashcards/ | 80% | 90% |
| src/tests/ | 80% | 90% |
| src/ai/ | 70% | 85% |
| src/web/ | 70% | 85% |
| **Total** | **80%** | **90%** |

---

## 2. Estructura de Tests

### 2.1 Directorio de Tests

```
tests/
|
+-- __init__.py
+-- conftest.py                    # Fixtures globales
|
+-- temario/
|   +-- __init__.py
|   +-- conftest.py                # Fixtures de temario
|   +-- test_parser.py             # Tests de parser
|   +-- test_chunker.py            # Tests de chunker
|   +-- test_store.py              # Tests de store
|   +-- test_embedder.py           # Tests de embedder
|   +-- test_searcher.py           # Tests de searcher
|   +-- test_ingest.py             # Tests de ingestion
|   +-- test_cli.py                # Tests de CLI
|   +-- test_integration.py        # Tests de integracion
|
+-- flashcards/
|   +-- __init__.py
|   +-- conftest.py
|   +-- test_models.py
|   +-- test_store.py
|   +-- test_generator.py
|   +-- test_sm2.py                # SM-2 algorithm
|   +-- test_reviewer.py
|   +-- test_cli.py
|
+-- tests/
|   +-- __init__.py
|   +-- conftest.py
|   +-- test_models.py
|   +-- test_store.py
|   +-- test_generator.py
|   +-- test_solver.py
|   +-- test_analyzer.py
|   +-- test_cli.py
|
+-- ai/
|   +-- __init__.py
|   +-- conftest.py
|   +-- test_minimax_client.py
|   +-- test_analyzer.py
|   +-- test_predictor.py
|   +-- test_planner.py
|   +-- test_recommender.py
|   +-- test_cli.py
|
+-- web/
    +-- __init__.py
    +-- conftest.py
    +-- test_routes.py             # Tests de endpoints
    +-- test_api.py                # Tests de API
    +-- test_integration.py        # Tests de integracion web
```

### 2.2 conftest.py Global

```python
# tests/conftest.py
"""
Fixtures globales para todos los tests.
"""
import os
import pytest
import tempfile
import sqlite3
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir():
    """Directorio con datos de prueba."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_dir():
    """Directorio temporal para cada test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_db(temp_dir):
    """Base de datos temporal para tests."""
    db_path = temp_dir / "test.db"
    conn = sqlite3.connect(str(db_path))
    yield conn
    conn.close()


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Variables de entorno mockeadas."""
    monkeypatch.setenv("MISTRAL_API_KEY", "test_key_123")
    monkeypatch.setenv("MINIMAX_API_KEY", "test_key_456")
    monkeypatch.setenv("MINIMAX_GROUP_ID", "test_group_789")


@pytest.fixture
def sample_pdf_path(test_data_dir):
    """Ruta a PDF de prueba."""
    return test_data_dir / "sample.pdf"


@pytest.fixture
def sample_docx_path(test_data_dir):
    """Ruta a DOCX de prueba."""
    return test_data_dir / "sample.docx"
```

### 2.3 Fixtures por Modulo

```python
# tests/temario/conftest.py
"""
Fixtures especificas del modulo temario.
"""
import pytest
from src.temario.models import Document, Chunk
from src.temario.store import TemarioStore


@pytest.fixture
def sample_document():
    """Documento de prueba."""
    return Document(
        id=1,
        filename="test.pdf",
        filepath="/path/to/test.pdf",
        file_type="pdf",
        title="Test Document",
        tema=1,
        total_pages=10,
        total_chunks=20
    )


@pytest.fixture
def sample_chunk():
    """Chunk de prueba."""
    return Chunk(
        id=1,
        document_id=1,
        content="Este es un texto de prueba para testing.",
        token_count=10,
        chunk_index=0,
        page_number=1,
        tema=1
    )


@pytest.fixture
def sample_embedding():
    """Embedding de prueba (1024 dimensiones)."""
    import numpy as np
    return list(np.random.rand(1024).astype(float))


@pytest.fixture
def temario_store(temp_db):
    """Store de temario con DB temporal."""
    return TemarioStore(connection=temp_db)


@pytest.fixture
def populated_store(temario_store, sample_document, sample_chunk):
    """Store con datos de prueba."""
    temario_store.insert_document(sample_document)
    temario_store.insert_chunk(sample_chunk)
    return temario_store
```

---

## 3. Convenciones de Testing

### 3.1 Nombres de Tests

```python
# PATRON: test_<unidad>_<escenario>_<resultado_esperado>

# Ejemplos:
def test_chunker_divide_text_correctly():
    """Test que el chunker divide texto correctamente."""
    pass

def test_parser_raises_error_on_invalid_pdf():
    """Test que parser lanza error con PDF invalido."""
    pass

def test_sm2_increases_interval_on_good_rating():
    """Test que SM-2 incrementa intervalo con buena calificacion."""
    pass
```

### 3.2 Estructura AAA

```python
def test_searcher_returns_relevant_results(populated_store):
    """Test que searcher retorna resultados relevantes."""
    # ARRANGE
    query = "texto de prueba"
    expected_min_score = 0.5

    # ACT
    results = populated_store.search(query, limit=5)

    # ASSERT
    assert len(results) > 0
    assert all(r.score >= expected_min_score for r in results)
```

### 3.3 Uso de Marcadores

```python
import pytest

@pytest.mark.unit
def test_pure_function():
    """Test unitario puro, sin dependencias externas."""
    pass

@pytest.mark.integration
def test_database_interaction(temp_db):
    """Test de integracion con base de datos."""
    pass

@pytest.mark.slow
def test_api_call():
    """Test que llama a API externa (lento)."""
    pass

@pytest.mark.skip(reason="Esperando implementacion de feature")
def test_future_feature():
    """Test para feature no implementado."""
    pass
```

### 3.4 Parametrizacion

```python
@pytest.mark.parametrize("rating,expected_interval", [
    (0, 1),   # De nuevo -> 1 dia
    (1, 1),   # Dificil -> 1 dia
    (2, 3),   # Bien -> 3 dias
    (3, 6),   # Facil -> 6 dias
    (4, 10),  # Muy facil -> 10 dias
])
def test_sm2_interval_calculation(rating, expected_interval):
    """Test calculo de intervalo SM-2 para diferentes ratings."""
    from src.flashcards.scheduler import SM2Scheduler

    scheduler = SM2Scheduler()

    # Flashcard con valores iniciales
    card = Flashcard(ease_factor=2.5, interval=1, repetitions=0)

    new_interval = scheduler.calculate_interval(card, rating)

    assert new_interval == expected_interval
```

### 3.5 Mocking

```python
from unittest.mock import Mock, patch, MagicMock

@patch("src.temario.embedder.httpx.post")
def test_embedder_handles_api_error(mock_post):
    """Test que embedder maneja errores de API."""
    # Configurar mock
    mock_post.return_value = Mock(
        status_code=500,
        json=lambda: {"error": "Internal Server Error"}
    )

    embedder = Embedder(api_key="test_key")

    # Debe lanzar excepcion
    with pytest.raises(APIError):
        embedder.embed(["texto de prueba"])


@patch("src.ai.minimax_client.MiniMaxClient.generate")
def test_flashcard_generation_with_mock(mock_generate):
    """Test generacion de flashcards con LLM mockeado."""
    mock_generate.return_value = """
    PREGUNTA: Cual es el articulo 1?
    RESPUESTA: Espana se constituye en un Estado social...
    """

    generator = FlashcardGenerator()
    cards = generator.generate_from_chunk(sample_chunk)

    assert len(cards) == 1
    assert "articulo 1" in cards[0].front.lower()
```

---

## 4. Cobertura de Codigo

### 4.1 Configuracion de Cobertura

```toml
# pyproject.toml

[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/conftest.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
fail_under = 80
show_missing = true
skip_covered = true
```

### 4.2 Ejecutar con Cobertura

```bash
# Cobertura basica
pytest --cov=src

# Cobertura detallada
pytest --cov=src --cov-report=term-missing

# Reporte HTML
pytest --cov=src --cov-report=html
# Abrir htmlcov/index.html

# Reporte XML (para CI)
pytest --cov=src --cov-report=xml

# Cobertura minima (falla si < 80%)
pytest --cov=src --cov-fail-under=80
```

### 4.3 Interpretar Reporte

```
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
src/temario/__init__.py                 5      0   100%
src/temario/models.py                  25      2    92%   45-46
src/temario/store.py                   80     15    81%   23-25, 67-70
src/temario/parser.py                  60      8    87%   34, 89-92
src/temario/chunker.py                 45      5    89%   12, 56
src/temario/embedder.py                50     12    76%   23-30, 45-48
-----------------------------------------------------------------
TOTAL                                 265     42    84%
```

**Acciones:**
- `Miss`: Lineas no cubiertas
- `Cover`: Porcentaje de cobertura
- `Missing`: Numeros de linea sin cubrir

---

## 5. Comandos de pytest

### 5.1 Comandos Basicos

```bash
# Ejecutar todos los tests
pytest

# Modo verbose
pytest -v

# Mostrar output de prints
pytest -s

# Detener en primer fallo
pytest -x

# Ejecutar tests especificos
pytest tests/temario/

# Ejecutar un archivo
pytest tests/temario/test_parser.py

# Ejecutar un test especifico
pytest tests/temario/test_parser.py::test_parse_pdf
```

### 5.2 Filtrado

```bash
# Por palabra clave
pytest -k "parser"

# Por marcador
pytest -m unit
pytest -m "not slow"
pytest -m "integration or slow"

# Por modulo
pytest tests/temario/
```

### 5.3 Paralelismo

```bash
# Instalar plugin
pip install pytest-xdist

# Ejecutar en paralelo (auto)
pytest -n auto

# Especificar numero de workers
pytest -n 4
```

### 5.4 Reportes

```bash
# Reporte de fallos
pytest --tb=short

# Reporte detallado
pytest --tb=long

# Solo trazas de fallos
pytest --tb=line

# Sin trazas
pytest --tb=no

# Reporte JSON
pip install pytest-json-report
pytest --json-report
```

### 5.5 Debugging

```bash
# Entrar al debugger en fallos
pytest --pdb

# Debugger al inicio
pytest --trace

# Mostrar locals en fallos
pytest -l
```

### 5.6 Comando Maestro

```bash
# Ejecucion completa con todo
pytest \
    -v \
    --tb=short \
    --cov=src \
    --cov-report=term-missing \
    --cov-fail-under=80 \
    -n auto \
    --durations=10
```

---

## 6. CI/CD Integration

### 6.1 GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint with ruff
        run: |
          ruff check src/ tests/

      - name: Format check with black
        run: |
          black --check src/ tests/

      - name: Run tests
        run: |
          pytest \
            -v \
            --tb=short \
            --cov=src \
            --cov-report=xml \
            --cov-fail-under=80
        env:
          MISTRAL_API_KEY: ${{ secrets.MISTRAL_API_KEY }}
          MINIMAX_API_KEY: ${{ secrets.MINIMAX_API_KEY }}
          MINIMAX_GROUP_ID: ${{ secrets.MINIMAX_GROUP_ID }}

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

### 6.2 Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest -v --tb=short -x
        language: system
        pass_filenames: false
        always_run: true
```

```bash
# Instalar hooks
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

### 6.3 Makefile

```makefile
# Makefile
.PHONY: test lint format coverage clean

test:
	pytest -v --tb=short

test-all:
	pytest -v --tb=short --cov=src --cov-report=term-missing

test-unit:
	pytest -v -m unit

test-integration:
	pytest -v -m integration

test-parallel:
	pytest -v -n auto

lint:
	ruff check src/ tests/

format:
	black src/ tests/

format-check:
	black --check src/ tests/

coverage:
	pytest --cov=src --cov-report=html
	open htmlcov/index.html

check: lint format-check test-all
	@echo "All checks passed!"

clean:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
```

---

## 7. Tests por Modulo

### 7.1 Temario

```python
# tests/temario/test_parser.py
"""Tests del parser de documentos."""
import pytest
from src.temario.parser import Parser


class TestParser:
    """Tests de la clase Parser."""

    @pytest.fixture
    def parser(self):
        return Parser()

    def test_parse_pdf_extracts_text(self, parser, sample_pdf_path):
        """Test que el parser extrae texto de PDF."""
        result = parser.parse(sample_pdf_path)

        assert result is not None
        assert len(result.text) > 0
        assert result.page_count > 0

    def test_parse_docx_extracts_text(self, parser, sample_docx_path):
        """Test que el parser extrae texto de DOCX."""
        result = parser.parse(sample_docx_path)

        assert result is not None
        assert len(result.text) > 0

    def test_parse_invalid_file_raises_error(self, parser, temp_dir):
        """Test que parser lanza error con archivo invalido."""
        invalid_file = temp_dir / "invalid.xyz"
        invalid_file.write_text("not a valid file")

        with pytest.raises(ValueError, match="Invalid file type"):
            parser.parse(invalid_file)

    def test_parse_nonexistent_file_raises_error(self, parser):
        """Test que parser lanza error con archivo inexistente."""
        with pytest.raises(FileNotFoundError):
            parser.parse("/nonexistent/file.pdf")
```

```python
# tests/temario/test_chunker.py
"""Tests del chunker de texto."""
import pytest
from src.temario.chunker import Chunker


class TestChunker:
    """Tests de la clase Chunker."""

    @pytest.fixture
    def chunker(self):
        return Chunker(target_tokens=100, max_tokens=150, min_tokens=50)

    def test_chunk_empty_text_returns_empty(self, chunker):
        """Test chunking de texto vacio."""
        chunks = chunker.chunk("")
        assert chunks == []

    def test_chunk_short_text_returns_single_chunk(self, chunker):
        """Test chunking de texto corto."""
        text = "Este es un texto corto de prueba."
        chunks = chunker.chunk(text)

        assert len(chunks) == 1
        assert chunks[0].content == text

    def test_chunk_long_text_respects_max_tokens(self, chunker):
        """Test que chunks respetan max_tokens."""
        text = "Esta es una oracion. " * 100  # Texto largo
        chunks = chunker.chunk(text)

        for chunk in chunks:
            assert chunk.token_count <= chunker.max_tokens

    def test_chunk_preserves_sentence_boundaries(self, chunker):
        """Test que chunking preserva limites de oraciones."""
        text = "Primera oracion. Segunda oracion. Tercera oracion."
        chunks = chunker.chunk(text)

        # Ningun chunk debe cortar a mitad de oracion
        for chunk in chunks:
            assert chunk.content.rstrip().endswith(".") or \
                   chunk.content == chunks[-1].content

    @pytest.mark.parametrize("text_length,expected_chunks", [
        (50, 1),
        (200, 2),
        (500, 5),
        (1000, 10),
    ])
    def test_chunk_count_approximates_target(self, chunker, text_length, expected_chunks):
        """Test que numero de chunks es aproximado al esperado."""
        words = ["palabra"] * text_length
        text = " ".join(words)

        chunks = chunker.chunk(text)

        # Permitir +/- 30% de variacion
        assert abs(len(chunks) - expected_chunks) <= expected_chunks * 0.3
```

```python
# tests/temario/test_searcher.py
"""Tests del buscador semantico."""
import pytest
import numpy as np
from src.temario.searcher import Searcher
from src.temario.models import Chunk, SearchResult


class TestSearcher:
    """Tests de la clase Searcher."""

    @pytest.fixture
    def searcher(self):
        return Searcher()

    @pytest.fixture
    def sample_chunks(self):
        """Chunks de prueba con embeddings."""
        return [
            Chunk(
                id=1,
                document_id=1,
                content="La Constitucion es la norma suprema",
                embedding=list(np.random.rand(1024))
            ),
            Chunk(
                id=2,
                document_id=1,
                content="El Gobierno dirige la politica interior",
                embedding=list(np.random.rand(1024))
            ),
        ]

    def test_cosine_similarity_returns_value_between_0_and_1(self, searcher):
        """Test que similitud coseno esta entre 0 y 1."""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        vec3 = [0.0, 1.0, 0.0]

        sim_same = searcher.cosine_similarity(vec1, vec2)
        sim_ortho = searcher.cosine_similarity(vec1, vec3)

        assert sim_same == 1.0
        assert sim_ortho == 0.0

    def test_search_returns_sorted_results(self, searcher, sample_chunks):
        """Test que busqueda retorna resultados ordenados por score."""
        query_embedding = list(np.random.rand(1024))

        results = searcher.search(
            query_embedding=query_embedding,
            chunks=sample_chunks,
            limit=10
        )

        # Verificar orden descendente
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_search_respects_limit(self, searcher, sample_chunks):
        """Test que busqueda respeta el limite."""
        query_embedding = list(np.random.rand(1024))

        results = searcher.search(
            query_embedding=query_embedding,
            chunks=sample_chunks,
            limit=1
        )

        assert len(results) <= 1

    def test_search_respects_threshold(self, searcher, sample_chunks):
        """Test que busqueda filtra por umbral de similitud."""
        query_embedding = list(np.random.rand(1024))

        results = searcher.search(
            query_embedding=query_embedding,
            chunks=sample_chunks,
            threshold=0.9  # Umbral alto
        )

        # Con umbral alto, puede que no haya resultados
        for result in results:
            assert result.score >= 0.9
```

### 7.2 Flashcards

```python
# tests/flashcards/test_sm2.py
"""Tests del algoritmo SM-2."""
import pytest
from datetime import datetime, timedelta
from src.flashcards.scheduler import SM2Scheduler
from src.flashcards.models import Flashcard


class TestSM2Scheduler:
    """Tests del algoritmo SM-2."""

    @pytest.fixture
    def scheduler(self):
        return SM2Scheduler()

    @pytest.fixture
    def new_card(self):
        return Flashcard(
            id=1,
            deck_id=1,
            front="Pregunta",
            back="Respuesta",
            ease_factor=2.5,
            interval=0,
            repetitions=0
        )

    @pytest.mark.parametrize("rating,expected_interval,expected_repetitions", [
        (0, 1, 0),  # De nuevo -> intervalo 1, reinicia repeticiones
        (1, 1, 0),  # Dificil -> intervalo 1, reinicia
        (2, 3, 1),  # Bien -> intervalo 3
        (3, 6, 1),  # Facil -> intervalo 6
    ])
    def test_sm2_new_card_rating(
        self, scheduler, new_card, rating, expected_interval, expected_repetitions
    ):
        """Test calculo de SM-2 para cartas nuevas."""
        result = scheduler.review(new_card, rating)

        assert result.interval == expected_interval
        assert result.repetitions == expected_repetitions

    def test_sm2_ease_factor_increases_on_good_rating(self, scheduler, new_card):
        """Test que ease factor aumenta con buena calificacion."""
        original_ef = new_card.ease_factor

        result = scheduler.review(new_card, 3)  # Facil

        assert result.ease_factor > original_ef

    def test_sm2_ease_factor_decreases_on_bad_rating(self, scheduler):
        """Test que ease factor disminuye con mala calificacion."""
        card = Flashcard(
            id=1, deck_id=1, front="P", back="R",
            ease_factor=2.5, interval=6, repetitions=3
        )

        result = scheduler.review(card, 0)  # De nuevo

        assert result.ease_factor < card.ease_factor

    def test_sm2_ease_factor_never_below_minimum(self, scheduler):
        """Test que ease factor nunca baja del minimo (1.3)."""
        card = Flashcard(
            id=1, deck_id=1, front="P", back="R",
            ease_factor=1.5, interval=6, repetitions=3
        )

        # Multiples calificaciones malas
        for _ in range(5):
            card = scheduler.review(card, 0)

        assert card.ease_factor >= 1.3

    def test_sm2_interval_multiplies_by_ease_factor(self, scheduler):
        """Test que intervalo se multiplica por ease factor."""
        card = Flashcard(
            id=1, deck_id=1, front="P", back="R",
            ease_factor=2.5, interval=6, repetitions=3
        )

        result = scheduler.review(card, 3)  # Facil

        expected = int(6 * 2.5 * scheduler.easy_bonus)
        assert result.interval == expected

    def test_sm2_resets_on_bad_rating(self, scheduler):
        """Test que SM-2 reinicia con calificacion mala."""
        card = Flashcard(
            id=1, deck_id=1, front="P", back="R",
            ease_factor=2.5, interval=30, repetitions=5
        )

        result = scheduler.review(card, 0)  # De nuevo

        assert result.interval == 1
        assert result.repetitions == 0
```

### 7.3 Web

```python
# tests/web/test_routes.py
"""Tests de endpoints web."""
import pytest
from fastapi.testclient import TestClient
from src.web.app import app


@pytest.fixture
def client():
    """Cliente de test para FastAPI."""
    return TestClient(app)


class TestDashboardRoutes:
    """Tests de rutas del dashboard."""

    def test_get_dashboard_returns_200(self, client):
        """Test que dashboard retorna 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_get_dashboard_stats_returns_json(self, client):
        """Test que stats retorna JSON."""
        response = client.get("/api/dashboard/stats")

        assert response.status_code == 200
        data = response.json()
        assert "temario" in data
        assert "flashcards" in data


class TestTemarioRoutes:
    """Tests de rutas de temario."""

    def test_list_documents_returns_empty_list(self, client):
        """Test que lista documentos vacios inicialmente."""
        response = client.get("/api/temario/documents")

        assert response.status_code == 200
        data = response.json()
        assert "documents" in data
        assert isinstance(data["documents"], list)

    def test_search_without_query_returns_400(self, client):
        """Test que busqueda sin query retorna error."""
        response = client.post("/api/temario/search", json={})

        assert response.status_code == 422  # Validation error

    def test_search_with_query_returns_results(self, client):
        """Test que busqueda con query retorna resultados."""
        response = client.post(
            "/api/temario/search",
            json={"query": "constitucion"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "results" in data


class TestFlashcardRoutes:
    """Tests de rutas de flashcards."""

    def test_create_deck_returns_201(self, client):
        """Test que crear deck retorna 201."""
        response = client.post(
            "/api/flashcards/decks",
            json={"name": "Test Deck"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Deck"

    def test_list_decks_includes_created_deck(self, client):
        """Test que listar decks incluye el creado."""
        # Crear deck
        client.post("/api/flashcards/decks", json={"name": "Test"})

        # Listar
        response = client.get("/api/flashcards/decks")

        assert response.status_code == 200
        data = response.json()
        assert any(d["name"] == "Test" for d in data["decks"])
```

---

## 8. Mejores Practicas

### 8.1 Tests Deterministicos

```python
# MAL: Test no deterministico
def test_search_returns_results():
    results = search("query")  # Depende de datos en DB
    assert len(results) > 0

# BIEN: Test deterministico
def test_search_returns_results(populated_store):
    results = populated_store.search("query")
    assert len(results) == 3  # Sabemos cuantos hay
```

### 8.2 Isolation

```python
# MAL: Test que afecta a otros
def test_create_document(db):
    create_document("test.pdf")
    # No limpia

# BIEN: Test aislado
def test_create_document(temp_db):
    create_document("test.pdf", temp_db)
    # temp_db se limpia automaticamente
```

### 8.3 Readability

```python
# MAL: Test ilegible
def test_sm2():
    c = Flashcard(1, 1, "p", "r", 2.5, 0, 0)
    r = sm2(c, 3)
    assert r.i == 6

# BIEN: Test legible
def test_sm2_increases_interval_for_easy_card():
    """Test que SM-2 incrementa intervalo para carta facil."""
    card = Flashcard(
        id=1, deck_id=1, front="Question", back="Answer",
        ease_factor=2.5, interval=0, repetitions=0
    )

    result = scheduler.review(card, rating=3)  # Easy

    assert result.interval == 6  # 6 days for easy first review
```

---

**Fin del documento de Testing**
