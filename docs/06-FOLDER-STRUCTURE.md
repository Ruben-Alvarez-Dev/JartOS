# Estructura de Carpetas

**Version:** 0.1.0
**Ultima actualizacion:** 2025-03-16

---

## Indice

1. [Diagrama de Estructura](#1-diagrama-de-estructura)
2. [Descripcion de Carpetas](#2-descripcion-de-carpetas)
3. [Convenciones de Nomenclatura](#3-convenciones-de-nomenclatura)
4. [Archivos .gitignore](#4-archivos-gitignore)
5. [Archivos por Modulo](#5-archivos-por-modulo)

---

## 1. Diagrama de Estructura

```
JartOS/
|
+-- .github/
|   +-- workflows/
|       +-- ci.yml                    # GitHub Actions CI
|       +-- release.yml               # Release workflow
|
+-- .venv/                            # Virtual environment (NO commitear)
|
+-- backups/                          # Backups de base de datos
|   +-- temario_20250316.db.bak
|   +-- oposiciones_20250316.db.bak
|
+-- configs/                          # Archivos de configuracion
|   +-- config.yaml                   # Configuracion principal
|   +-- temario.yaml                  # Config de modulo temario
|   +-- flashcards.yaml               # Config de modulo flashcards
|   +-- tests.yaml                    # Config de modulo tests
|   +-- ai.yaml                       # Config de modulo AI
|
+-- data/                             # Bases de datos SQLite
|   +-- temario.db                    # Documentos y chunks
|   +-- oposiciones.db                # Flashcards, tests, analytics
|
+-- docs/                             # Documentacion
|   +-- 01-CONTEXT.md                 # Contexto del proyecto
|   +-- 02-ARCHITECTURE.md            # Arquitectura del sistema
|   +-- 03-MODULES/                   # Documentacion de modulos
|   |   +-- temario-ingestion.md
|   |   +-- flashcards-sm2.md
|   |   +-- test-generator.md
|   |   +-- dashboard-web.md
|   +-- 04-ROADMAP.md                 # Roadmap de implementacion
|   +-- 05-SOURCE-FILES.md            # Archivos fuente
|   +-- 06-FOLDER-STRUCTURE.md        # Este archivo
|   +-- 07-SETUP.md                   # Guia de instalacion
|   +-- 08-API-REFERENCE.md           # Referencia de API
|   +-- 09-TESTING.md                 # Estrategia de testing
|
+-- documents/                        # Documentos del usuario (NO commitear)
|   +-- temario/
|       +-- Tema1.pdf
|       +-- Tema2.docx
|
+-- logs/                             # Archivos de log
|   +-- oposiciones.log
|   +-- temario.log
|   +-- api.log
|
+-- scripts/                          # Scripts de utilidad
|   +-- run_web.py                    # Iniciar servidor web
|   +-- backup_db.py                  # Backup de bases de datos
|   +-- seed_data.py                  # Datos de prueba
|   +-- migrate.py                    # Migraciones de DB
|
+-- src/                              # Codigo fuente principal
|   +-- __init__.py
|   |
|   +-- core/                         # Modulo core
|   |   +-- __init__.py
|   |   +-- config.py                 # Carga de configuracion
|   |   +-- logger.py                 # Sistema de logging
|   |   +-- exceptions.py             # Excepciones custom
|   |   +-- db.py                     # Conexion a bases de datos
|   |
|   +-- temario/                      # Modulo de temario
|   |   +-- __init__.py
|   |   +-- models.py                 # Document, Chunk, SearchResult
|   |   +-- store.py                  # SQLite operations
|   |   +-- parser.py                 # PDF/DOCX parsing
|   |   +-- chunker.py                # Text chunking
|   |   +-- embedder.py               # Mistral embeddings
|   |   +-- searcher.py               # Semantic search
|   |   +-- ingest.py                 # Orquestacion de ingestion
|   |   +-- cli.py                    # CLI commands
|   |
|   +-- flashcards/                   # Modulo de flashcards
|   |   +-- __init__.py
|   |   +-- models.py                 # Deck, Flashcard, ReviewLog
|   |   +-- store.py                  # SQLite operations
|   |   +-- generator.py              # Generacion con IA
|   |   +-- scheduler.py              # SM-2 algorithm
|   |   +-- reviewer.py               # Review session manager
|   |   +-- cli.py                    # CLI commands
|   |
|   +-- tests/                        # Modulo de tests
|   |   +-- __init__.py
|   |   +-- models.py                 # Test, Question, TestSession
|   |   +-- store.py                  # SQLite operations
|   |   +-- generator.py              # Generacion de preguntas
|   |   +-- solver.py                 # Evaluacion de respuestas
|   |   +-- analyzer.py               # Analisis de resultados
|   |   +-- cli.py                    # CLI commands
|   |
|   +-- ai/                           # Modulo de AI analytics
|   |   +-- __init__.py
|   |   +-- models.py                 # WeakArea, StudyPlan, Recommendation
|   |   +-- store.py                  # SQLite operations
|   |   +-- minimax_client.py         # MiniMax API client
|   |   +-- analyzer.py               # Deteccion de areas debiles
|   |   +-- predictor.py              # Prediccion de preparacion
|   |   +-- planner.py                # Planes de estudio
|   |   +-- recommender.py            # Recomendaciones diarias
|   |   +-- cli.py                    # CLI commands
|   |
|   +-- web/                          # Modulo web dashboard
|       +-- __init__.py
|       +-- app.py                    # FastAPI application
|       +-- routes/
|       |   +-- __init__.py
|       |   +-- dashboard.py          # Dashboard endpoints
|       |   +-- temario.py            # Temario endpoints
|       |   +-- flashcards.py         # Flashcards endpoints
|       |   +-- tests.py              # Tests endpoints
|       +-- templates/                # Jinja2 templates
|       |   +-- base.html
|       |   +-- dashboard/
|       |   |   +-- index.html
|       |   +-- temario/
|       |   |   +-- list.html
|       |   |   +-- search.html
|       |   +-- flashcards/
|       |   |   +-- deck.html
|       |   |   +-- review.html
|       |   +-- tests/
|       |       +-- take.html
|       |       +-- results.html
|       +-- static/
|           +-- css/
|           |   +-- style.css
|           +-- js/
|               +-- app.js
|
+-- tests/                            # Tests
|   +-- __init__.py
|   +-- conftest.py                   # Pytest fixtures globales
|   |
|   +-- temario/
|   |   +-- __init__.py
|   |   +-- conftest.py               # Fixtures de temario
|   |   +-- test_parser.py
|   |   +-- test_chunker.py
|   |   +-- test_store.py
|   |   +-- test_embedder.py
|   |   +-- test_searcher.py
|   |   +-- test_integration.py
|   |
|   +-- flashcards/
|   |   +-- __init__.py
|   |   +-- test_flashcards.py
|   |   +-- test_sm2.py
|   |   +-- test_generator.py
|   |
|   +-- tests/
|   |   +-- __init__.py
|   |   +-- test_tests.py
|   |   +-- test_generator.py
|   |   +-- test_analyzer.py
|   |
|   +-- ai/
|   |   +-- __init__.py
|   |   +-- test_ai.py
|   |   +-- test_predictor.py
|   |   +-- test_planner.py
|   |
|   +-- web/
|       +-- __init__.py
|       +-- conftest.py
|       +-- test_web_app.py
|
+-- .env.example                      # Template de environment
+-- .env                              # Environment (NO commitear)
+-- .gitignore                        # Git ignore
+-- pyproject.toml                    # Configuracion del proyecto
+-- README.md                         # README principal
+-- LICENSE                           # Licencia
```

---

## 2. Descripcion de Carpetas

### 2.1 .github/

**Proposito:** Configuracion de GitHub Actions.

| Archivo | Descripcion |
|---------|-------------|
| `workflows/ci.yml` | CI pipeline: tests, lint, coverage |
| `workflows/release.yml` | Release automation |

### 2.2 backups/

**Proposito:** Backups de las bases de datos.

**Convencion:** `{dbname}_{YYYYMMDD}.db.bak`

```bash
# Crear backup manual
python scripts/backup_db.py

# Backups automaticos (configurar cron)
0 2 * * * cd ~/CLIs/JartOS && python scripts/backup_db.py
```

### 2.3 configs/

**Proposito:** Archivos de configuracion YAML.

| Archivo | Descripcion |
|---------|-------------|
| `config.yaml` | Configuracion principal |
| `temario.yaml` | Configuracion especifica de temario |
| `flashcards.yaml` | Configuracion especifica de flashcards |
| `tests.yaml` | Configuracion especifica de tests |
| `ai.yaml` | Configuracion especifica de AI |

### 2.4 data/

**Proposito:** Bases de datos SQLite.

| Archivo | Descripcion | Tamano estimado |
|---------|-------------|-----------------|
| `temario.db` | Documentos y chunks | 50-200 MB |
| `oposiciones.db` | Flashcards, tests, analytics | 10-50 MB |

**Nota:** NO commitear a Git (datos del usuario).

### 2.5 docs/

**Proposito:** Documentacion del proyecto.

| Prefijo | Tipo |
|---------|------|
| `01-` | Contexto |
| `02-` | Arquitectura |
| `03-` | Modulos |
| `04-` | Roadmap |
| `05-` | Fuente |
| `06-` | Estructura |
| `07-` | Setup |
| `08-` | API |
| `09-` | Testing |

### 2.6 documents/

**Proposito:** Documentos PDF/DOCX del usuario.

**Estructura:**
```
documents/
+-- temario/
    +-- Tema1.pdf
    +-- Tema2.pdf
    +-- Tema3.docx
```

**Nota:** NO commitear a Git (datos del usuario).

### 2.7 logs/

**Proposito:** Archivos de log.

| Archivo | Contenido |
|---------|-----------|
| `oposiciones.log` | Log general |
| `temario.log` | Log del modulo temario |
| `api.log` | Log de la API web |

**Rotacion:** Automatica al alcanzar 10 MB.

### 2.8 scripts/

**Proposito:** Scripts de utilidad.

| Script | Descripcion |
|--------|-------------|
| `run_web.py` | Iniciar servidor web |
| `backup_db.py` | Backup de bases de datos |
| `seed_data.py` | Crear datos de prueba |
| `migrate.py` | Migraciones de esquema |

### 2.9 src/

**Proposito:** Codigo fuente principal.

#### src/core/

**Modulos core del sistema:**

| Archivo | Descripcion |
|---------|-------------|
| `config.py` | Carga de configuracion YAML + env |
| `logger.py` | Sistema de logging |
| `exceptions.py` | Excepciones custom |
| `db.py` | Conexion a SQLite |

#### src/temario/

**Modulo de gestion de temario:**

| Archivo | Descripcion |
|---------|-------------|
| `models.py` | Data classes: Document, Chunk, SearchResult |
| `store.py` | Operaciones SQLite |
| `parser.py` | Parsing de PDF y DOCX |
| `chunker.py` | Division de texto en chunks |
| `embedder.py` | Generacion de embeddings (Mistral) |
| `searcher.py` | Busqueda semantica |
| `ingest.py` | Orquestacion de ingestion |
| `cli.py` | Comandos CLI |

#### src/flashcards/

**Modulo de flashcards con SM-2:**

| Archivo | Descripcion |
|---------|-------------|
| `models.py` | Data classes: Deck, Flashcard, ReviewLog |
| `store.py` | Operaciones SQLite |
| `generator.py` | Generacion con IA |
| `scheduler.py` | Algoritmo SM-2 |
| `reviewer.py` | Gestion de sesiones de repaso |
| `cli.py` | Comandos CLI |

#### src/tests/

**Modulo de generacion y evaluacion:**

| Archivo | Descripcion |
|---------|-------------|
| `models.py` | Data classes: Test, Question, TestSession |
| `store.py` | Operaciones SQLite |
| `generator.py` | Generacion de preguntas |
| `solver.py` | Evaluacion de respuestas |
| `analyzer.py` | Analisis de resultados |
| `cli.py` | Comandos CLI |

#### src/ai/

**Modulo de AI analytics:**

| Archivo | Descripcion |
|---------|-------------|
| `models.py` | Data classes: WeakArea, StudyPlan, Recommendation |
| `store.py` | Operaciones SQLite |
| `minimax_client.py` | Cliente de MiniMax API |
| `analyzer.py` | Deteccion de areas debiles |
| `predictor.py` | Prediccion de preparacion |
| `planner.py` | Generacion de planes |
| `recommender.py` | Recomendaciones diarias |
| `cli.py` | Comandos CLI |

#### src/web/

**Modulo web dashboard:**

| Directorio/Archivo | Descripcion |
|-------------------|-------------|
| `app.py` | Aplicacion FastAPI |
| `routes/` | Endpoints de la API |
| `templates/` | Templates Jinja2 |
| `static/` | CSS, JS, imagenes |

### 2.10 tests/

**Proposito:** Tests del proyecto.

**Estructura espeja src/**:
```
tests/
+-- temario/          # Tests de temario
+-- flashcards/       # Tests de flashcards
+-- tests/            # Tests de modulo tests
+-- ai/               # Tests de AI
+-- web/              # Tests de web
```

---

## 3. Convenciones de Nomenclatura

### 3.1 Archivos Python

| Tipo | Convencion | Ejemplo |
|------|------------|---------|
| Modulo | snake_case | `temario_store.py` |
| Test | test_{module}.py | `test_temario_store.py` |
| CLI | cli.py | `src/temario/cli.py` |
| Config | {module}.yaml | `configs/temario.yaml` |

### 3.2 Directorios

| Tipo | Convencion | Ejemplo |
|------|------------|---------|
| Modulo | snake_case | `src/temario/` |
| Test | Igual que modulo | `tests/temario/` |
| Config | plural | `configs/` |
| Data | plural | `data/` |

### 3.3 Archivos de Configuracion

| Archivo | Convencion |
|---------|------------|
| Principal | `config.yaml` |
| Por modulo | `{module}.yaml` |
| Environment | `.env` |
| Git ignore | `.gitignore` |
| README | `README.md` |

### 3.4 Base de Datos

| Archivo | Convencion |
|---------|------------|
| DB principal | `{dominio}.db` |
| Backup | `{dbname}_{YYYYMMDD}.db.bak` |

### 3.5 Logs

| Archivo | Convencion |
|---------|------------|
| Log general | `oposiciones.log` |
| Por modulo | `{module}.log` |

### 3.6 Documentacion

| Tipo | Prefijo | Ejemplo |
|------|---------|---------|
| Contexto | `01-` | `01-CONTEXT.md` |
| Arquitectura | `02-` | `02-ARCHITECTURE.md` |
| Modulos | `03-` | `03-MODULES/` |
| Roadmap | `04-` | `04-ROADMAP.md` |
| Fuente | `05-` | `05-SOURCE-FILES.md` |
| Estructura | `06-` | `06-FOLDER-STRUCTURE.md` |
| Setup | `07-` | `07-SETUP.md` |
| API | `08-` | `08-API-REFERENCE.md` |
| Testing | `09-` | `09-TESTING.md` |

---

## 4. Archivos .gitignore

### 4.1 .gitignore Principal

```gitignore
# =============================================================================
# OPOSICIONES-SYSTEM - Git Ignore
# =============================================================================

# -----------------------------------------------------------------------------
# Python
# -----------------------------------------------------------------------------
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# -----------------------------------------------------------------------------
# Virtual Environments
# -----------------------------------------------------------------------------
.venv/
venv/
ENV/
env/
.envrc

# -----------------------------------------------------------------------------
# IDE
# -----------------------------------------------------------------------------
.idea/
.vscode/
*.swp
*.swo
*~
.project
.pydevproject
.settings/

# -----------------------------------------------------------------------------
# Environment Variables
# -----------------------------------------------------------------------------
.env
.env.local
.env.*.local
*.env

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------
*.db
*.sqlite3
data/*.db
!data/.gitkeep

# -----------------------------------------------------------------------------
# Logs
# -----------------------------------------------------------------------------
logs/
*.log

# -----------------------------------------------------------------------------
# Backups
# -----------------------------------------------------------------------------
backups/
*.bak

# -----------------------------------------------------------------------------
# User Documents
# -----------------------------------------------------------------------------
documents/temario/*.pdf
documents/temario/*.docx
!documents/temario/.gitkeep

# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
.coverage
.coverage.*
htmlcov/
.pytest_cache/
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# -----------------------------------------------------------------------------
# Type Checking
# -----------------------------------------------------------------------------
.mypy_cache/
.dmypy.json
dmypy.json

# -----------------------------------------------------------------------------
# OS
# -----------------------------------------------------------------------------
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
desktop.ini

# -----------------------------------------------------------------------------
# Temporary Files
# -----------------------------------------------------------------------------
*.tmp
*.temp
*.bak
*~

# -----------------------------------------------------------------------------
# Build Artifacts
# -----------------------------------------------------------------------------
*.pyc
*.pyo
*.exe
*.dll
*.so
*.dylib
```

### 4.2 .gitkeep para carpetas vacias

Crear archivos `.gitkeep` en carpetas que deben existir pero estan vacias:

```bash
# Crear .gitkeep en carpetas vacias
touch data/.gitkeep
touch logs/.gitkeep
touch backups/.gitkeep
touch documents/temario/.gitkeep
```

---

## 5. Archivos por Modulo

### 5.1 Modulo Temario

```
src/temario/
+-- __init__.py           # Exports: Document, Chunk, SearchResult, ingest, search
+-- models.py             # @dataclass: Document, Chunk, SearchResult, IngestionResult
+-- store.py              # class TemarioStore: SQLite CRUD operations
+-- parser.py             # class Parser: PDF/DOCX text extraction
+-- chunker.py            # class Chunker: Token-based chunking
+-- embedder.py           # class Embedder: Mistral API integration
+-- searcher.py           # class Searcher: Semantic search
+-- ingest.py             # class Ingestor: Orchestration
+-- cli.py                # app = typer.Typer(): CLI commands
```

### 5.2 Modulo Flashcards

```
src/flashcards/
+-- __init__.py           # Exports: Deck, Flashcard, create_deck, review
+-- models.py             # @dataclass: Deck, Flashcard, ReviewLog
+-- store.py              # class FlashcardStore: SQLite CRUD
+-- generator.py          # class Generator: AI-powered generation
+-- scheduler.py          # class SM2Scheduler: SM-2 algorithm
+-- reviewer.py           # class Reviewer: Session management
+-- cli.py                # app = typer.Typer(): CLI commands
```

### 5.3 Modulo Tests

```
src/tests/
+-- __init__.py           # Exports: Test, Question, create_test, take_test
+-- models.py             # @dataclass: Test, Question, TestSession, TestResult
+-- store.py              # class TestStore: SQLite CRUD
+-- generator.py          # class TestGenerator: Question generation
+-- solver.py             # class Solver: Answer evaluation
+-- analyzer.py           # class Analyzer: Result analysis
+-- cli.py                # app = typer.Typer(): CLI commands
```

### 5.4 Modulo AI

```
src/ai/
+-- __init__.py           # Exports: analyze, predict, plan, recommend
+-- models.py             # @dataclass: WeakArea, StudyPlan, Recommendation
+-- store.py              # class AIStore: SQLite CRUD
+-- minimax_client.py     # class MiniMaxClient: API wrapper
+-- analyzer.py           # class WeakAreaAnalyzer: Detection
+-- predictor.py          # class Predictor: Readiness prediction
+-- planner.py            # class Planner: Weekly plans
+-- recommender.py        # class Recommender: Daily recommendations
+-- cli.py                # app = typer.Typer(): CLI commands
```

### 5.5 Modulo Web

```
src/web/
+-- __init__.py           # Exports: app
+-- app.py                # app = FastAPI(): Main application
+-- routes/
    +-- __init__.py       # Export all routers
    +-- dashboard.py      # router = APIRouter(): Dashboard endpoints
    +-- temario.py        # router = APIRouter(): Temario endpoints
    +-- flashcards.py     # router = APIRouter(): Flashcards endpoints
    +-- tests.py          # router = APIRouter(): Tests endpoints
+-- templates/
    +-- base.html         # Base template
    +-- dashboard/
        +-- index.html    # Dashboard home
    +-- temario/
        +-- list.html     # Document list
        +-- search.html   # Search interface
    +-- flashcards/
        +-- deck.html     # Deck view
        +-- review.html   # Review session
    +-- tests/
        +-- take.html     # Test taking
        +-- results.html  # Results view
+-- static/
    +-- css/
        +-- style.css     # Main styles
    +-- js/
        +-- app.js        # Main JavaScript
```

---

## 6. Creacion Rapida de Estructura

### Script de setup

```bash
#!/bin/bash
# =============================================================================
# create_structure.sh - Crea la estructura de carpetas
# =============================================================================

# Directorio base
BASE_DIR="JartOS"
mkdir -p "$BASE_DIR" && cd "$BASE_DIR"

# Estructura principal
mkdir -p .github/workflows
mkdir -p backups
mkdir -p configs
mkdir -p data
mkdir -p docs/03-MODULES
mkdir -p documents/temario
mkdir -p logs
mkdir -p scripts

# Estructura src
mkdir -p src/core
mkdir -p src/temario
mkdir -p src/flashcards
mkdir -p src/tests
mkdir -p src/ai
mkdir -p src/web/routes
mkdir -p src/web/templates/dashboard
mkdir -p src/web/templates/temario
mkdir -p src/web/templates/flashcards
mkdir -p src/web/templates/tests
mkdir -p src/web/static/css
mkdir -p src/web/static/js

# Estructura tests
mkdir -p tests/temario
mkdir -p tests/flashcards
mkdir -p tests/tests
mkdir -p tests/ai
mkdir -p tests/web

# Archivos __init__.py
touch src/__init__.py
touch src/core/__init__.py
touch src/temario/__init__.py
touch src/flashcards/__init__.py
touch src/tests/__init__.py
touch src/ai/__init__.py
touch src/web/__init__.py
touch src/web/routes/__init__.py
touch tests/__init__.py
touch tests/temario/__init__.py
touch tests/flashcards/__init__.py
touch tests/tests/__init__.py
touch tests/ai/__init__.py
touch tests/web/__init__.py

# .gitkeep files
touch data/.gitkeep
touch logs/.gitkeep
touch backups/.gitkeep
touch documents/temario/.gitkeep

# Archivos de configuracion
touch configs/config.yaml
touch configs/temario.yaml

# Archivos principales
touch .env.example
touch .gitignore
touch pyproject.toml
touch README.md
touch LICENSE

echo "Estructura creada en $BASE_DIR"
```

---

**Fin del documento de Estructura de Carpetas**
