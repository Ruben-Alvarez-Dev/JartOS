# Archivos Fuente y Configuracion

**Version:** 0.1.0
**Ultima actualizacion:** 2026-03-16

---

## Indice

1. [Vision General](#1-vision-general)
2. [Archivos de OPENCLAW-city](#2-archivos-de-openclaw-city)
3. [Referencias de JartOS](#3-referencias-de-jartos)
4. [Adaptaciones de OPENCLAW-system](#4-adaptaciones-de-openclaw-system)
5. [API Keys Necesarias](#5-api-keys-necesarias)
6. [Archivos de Configuracion](#6-archivos-de-configuracion)
7. [Comandos de Setup](#7-comandos-de-setup)

---

## 1. Vision General

### Mapa de Fuentes

```
+============================================================================+
|                         FUENTES DEL PROYECTO                                |
+============================================================================+
|                                                                            |
|  OPENCLAW-city                         JartOS                              |
|  (Copiar directamente)                (Referenciar patrones)               |
|  +-- MiniMax integration              +-- CLI structure                    |
|  +-- Logging system                   +-- YAML configs                     |
|  +-- Config patterns                  +-- Script patterns                  |
|                                                                            |
+----------------------------------+-----------------------------------------+
                                   |
                                   v
+============================================================================+
|                         OPOSICIONES-SYSTEM                                  |
|                                                                            |
|  +-- src/temario/          (Nuevo + referencias)                           |
|  +-- src/flashcards/       (Nuevo)                                         |
|  +-- src/tests/            (Nuevo)                                         |
|  +-- src/ai/               (Nuevo + referencias)                           |
|  +-- src/web/              (Nuevo)                                         |
|  +-- configs/              (Adaptado de JartOS)                            |
|  +-- integrations/         (De OPENCLAW-city)                              |
|                                                                            |
+============================================================================+
                                   ^
                                   |
+----------------------------------+-----------------------------------------+
|                                                                            |
|  OPENCLAW-system                       NUEVO                              |
|  (Adaptar y simplificar)               (Implementar desde cero)            |
|  +-- Memory Store (adaptar)            +-- SM-2 Algorithm                  |
|  +-- RAG Store (usar)                  +-- Test Generator                  |
|  +-- Dashboard CLI (simplificar)       +-- AI Analytics                    |
|  +-- Security patterns (aplicar)       +-- Web Dashboard                   |
|                                                                            |
+============================================================================+
```

---

## 2. Archivos de OPENCLAW-city

### 2.1 Archivos a Copiar Directamente

| Archivo Origen | Destino | Descripcion | Modificacion |
|---------------|---------|-------------|--------------|
| `orchestrator/mcp_orchestrator.py` | `integrations/minimax_client.py` | Cliente MiniMax API | Simplificar, quitar MCP |
| `integrations/zadarma_client.py` | NO COPIAR | Solo referencia | - |
| `orchestrator/a2a_logger.py` | `src/core/logger.py` | Sistema de logging | Adaptar formato |
| `configs/*.yaml` | `configs/` | Templates de config | Adaptar estructura |

### 2.2 MiniMax Integration

**Origen:** `orchestrator/mcp_orchestrator.py`

```python
# COPIAR Y ADAPTAR:
# - Clase MiniMaxClient
# - Manejo de errores de API
# - Retry logic con backoff
# - Rate limiting

# NO COPIAR:
# - MCP protocol code
# - Agent orchestration
# - Voice-related code
```

**Archivo destino:** `src/ai/minimax_client.py`

```python
"""
MiniMax API Client para generacion de texto.
Adaptado de OPENCLAW-city/orchestrator/mcp_orchestrator.py
"""
import os
import time
import httpx
from typing import Optional

class MiniMaxClient:
    """Cliente para MiniMax API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        group_id: Optional[str] = None,
        model: str = "MiniMax-Text-01",
        base_url: str = "https://api.minimax.chat/v1"
    ):
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        self.group_id = group_id or os.getenv("MINIMAX_GROUP_ID")
        self.model = model
        self.base_url = base_url
        self.client = httpx.Client(timeout=60.0)

    def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 2048
    ) -> str:
        """Genera texto con MiniMax."""
        # TODO: Implementar con retry logic
        pass
```

### 2.3 Logging System

**Origen:** `orchestrator/a2a_logger.py`

```python
# COPIAR Y ADAPTAR:
# - Estructura de logger
# - Formato de logs
# - Rotacion de archivos

# NO COPIAR:
# - A2A-specific logging
# - Voice agent logs
```

**Archivo destino:** `src/core/logger.py`

### 2.4 Config Patterns

**Origen:** `configs/` directory

```yaml
# COPIAR estructura de:
# - database config pattern
# - api keys pattern (usando env vars)
# - logging config pattern

# NO COPIAR:
# - LiveKit config
# - SIP config
# - Zadarma config
```

---

## 3. Referencias de JartOS

### 3.1 Estructura de CLI

**Referenciar:** Patrones de CLI con typer

```python
# PATRON DE JartOS (referencia, no copiar):
# scripts/productivity/cli.py

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

@app.command()
def command_name(
    param: str = typer.Argument(..., help="Descripcion"),
    option: bool = typer.Option(False, "--flag", "-f")
):
    """Descripcion del comando."""
    # Implementacion
    pass

if __name__ == "__main__":
    app()
```

### 3.2 YAML Config Pattern

**Referenciar:** Estructura de archivos YAML

```yaml
# PATRON DE JartOS (referencia):
# configs/app.yaml

app:
  name: "JartOS"
  version: "1.0.0"

database:
  path: "data/app.db"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/app.log"
```

### 3.3 Script Patterns

**Referenciar:** Estructura de scripts

```python
# PATRON DE JartOS (referencia):
# scripts/utils/helpers.py

from pathlib import Path
from typing import Optional
import yaml

def load_config(config_path: Optional[Path] = None) -> dict:
    """Carga configuracion desde YAML."""
    if config_path is None:
        config_path = Path("configs/config.yaml")

    with open(config_path) as f:
        return yaml.safe_load(f)
```

---

## 4. Adaptaciones de OPENCLAW-system

### 4.1 Memory Store

**Origen:** `memory_store/` directory

| Componente | Accion | Adaptacion |
|------------|--------|------------|
| `memory_store.py` | Adaptar | Simplificar para temario |
| `models.py` | Usar | Data classes para Document, Chunk |
| `sqlite_handler.py` | Usar | Sin cambios mayores |

**Archivo destino:** `src/temario/store.py`

```python
"""
Temario Store - Adaptado de OPENCLAW-system/memory_store/
"""
import sqlite3
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

# ADAPTAR:
# - Schema para documents y chunks
# - Embeddings como BLOB
# - Metadatos adicionales (tema, pagina)

# SIMPLIFICAR:
# - Quitar sistema de agent memory
# - Quitar conversation history
# - Enfocar en temario storage
```

### 4.2 RAG Store

**Origen:** `rag_store/` directory

| Componente | Accion | Adaptacion |
|------------|--------|------------|
| `embedder.py` | Usar | Cambiar a Mistral |
| `searcher.py` | Usar | Sin cambios mayores |
| `chunker.py` | Adaptar | Ajustar tamaños |

**Archivo destino:** `src/temario/embedder.py`, `src/temario/searcher.py`

```python
"""
Embeddings - Adaptado de OPENCLAW-system/rag_store/
"""
# USAR DIRECTAMENTE:
# - Cosine similarity
# - Vector search logic
# - Chunking strategies

# CAMBIAR:
# - OpenAI embeddings -> Mistral embeddings
# - Dimensiones: 1536 -> 1024
```

### 4.3 Dashboard CLI

**Origen:** `dashboard/` directory

| Componente | Accion | Adaptacion |
|------------|--------|------------|
| `cli.py` | Simplificar | Solo comandos de temario |
| `commands/` | Seleccionar | Solo los necesarios |

**Archivo destino:** `src/temario/cli.py`

```python
"""
CLI - Simplificado de OPENCLAW-system/dashboard/
"""
# SIMPLIFICAR:
# - Quitar comandos de agent
# - Quitar comandos de memory
# - Mantener solo: ingest, search, list, delete

# MANTENER:
# - Rich formatting
# - Typer structure
# - Progress bars
```

### 4.4 Security Patterns

**Origen:** `security/` directory

| Componente | Accion | Adaptacion |
|------------|--------|------------|
| `input_validation.py` | Usar | Sin cambios |
| `sanitization.py` | Usar | Sin cambios |

**Principios a aplicar:**

```python
# PATRONES DE SEGURIDAD (aplicar):

# 1. Input validation
def validate_file_path(path: str) -> Path:
    """Valida que el path es seguro."""
    p = Path(path).resolve()
    if not p.exists():
        raise ValueError(f"File not found: {path}")
    if p.suffix.lower() not in [".pdf", ".docx"]:
        raise ValueError(f"Invalid file type: {p.suffix}")
    return p

# 2. API key sanitization
def sanitize_for_logging(text: str) -> str:
    """Remueve API keys del texto antes de loggear."""
    import re
    # Remueve patrones de API keys
    return re.sub(r'[A-Za-z0-9]{32,}', '[REDACTED]', text)

# 3. SQL injection prevention (usar parametrized queries)
def get_chunk(cursor: sqlite3.Cursor, chunk_id: int) -> Optional[dict]:
    """Obtiene chunk de forma segura."""
    cursor.execute(
        "SELECT * FROM chunks WHERE id = ?",
        (chunk_id,)  # Parametrizado, no string concatenation
    )
    return cursor.fetchone()
```

---

## 5. API Keys Necesarias

### 5.1 Formato de .env

**Archivo:** `.env` (NO commitear)

```bash
# =============================================================================
# OPOSICIONES-SYSTEM - Environment Variables
# =============================================================================
# COPIAR este archivo como .env y llenar los valores
# NUNCA commitear este archivo con valores reales
# =============================================================================

# -----------------------------------------------------------------------------
# MISTRAL AI - Embeddings
# -----------------------------------------------------------------------------
# Obtener en: https://console.mistral.ai/
# Plan: Free tier disponible (rate limits aplican)
MISTRAL_API_KEY=your_mistral_api_key_here

# -----------------------------------------------------------------------------
# MINIMAX - Generacion de texto
# -----------------------------------------------------------------------------
# Obtener en: https://www.minimaxi.com/
# Requiere: API Key + Group ID
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_GROUP_ID=your_minimax_group_id_here

# -----------------------------------------------------------------------------
# TELEGRAM BOT (Opcional - Fase 3+)
# -----------------------------------------------------------------------------
# Obtener en: @BotFather en Telegram
# Crear bot con /newbot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# -----------------------------------------------------------------------------
# OPTIONAL - Local LLM fallback
# -----------------------------------------------------------------------------
# Si usas Ollama local como fallback
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# -----------------------------------------------------------------------------
# APP CONFIG
# -----------------------------------------------------------------------------
# Entorno: development | production
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 5.2 .env.example (Commitear)

**Archivo:** `.env.example`

```bash
# =============================================================================
# OPOSICIONES-SYSTEM - Environment Variables Template
# =============================================================================
# COPIAR como .env y llenar los valores

# MISTRAL AI - Embeddings
MISTRAL_API_KEY=

# MINIMAX - Generacion de texto
MINIMAX_API_KEY=
MINIMAX_GROUP_ID=

# TELEGRAM BOT (Opcional)
TELEGRAM_BOT_TOKEN=

# OPTIONAL - Local LLM fallback
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# APP CONFIG
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 5.3 Obtener API Keys

| Proveedor | URL | Plan | Uso |
|-----------|-----|------|-----|
| **Mistral** | https://console.mistral.ai/ | Free tier disponible | Embeddings |
| **MiniMax** | https://www.minimaxi.com/ | Pay per use | Generacion texto |
| **Telegram** | @BotFather en Telegram | Gratuito | Bot (opcional) |

### 5.4 Costos Estimados

| Servicio | Modelo | Costo | Uso mensual estimado | Costo mensual |
|----------|--------|-------|----------------------|---------------|
| Mistral | mistral-embed | $0.0001/1K tokens | 500K tokens | ~$0.05 |
| MiniMax | MiniMax-Text-01 | $0.001/1K tokens | 1M tokens | ~$1.00 |
| **Total** | | | | **~$1-5/mes** |

---

## 6. Archivos de Configuracion

### 6.1 config.yaml Principal

**Archivo:** `configs/config.yaml`

```yaml
# =============================================================================
# OPOSICIONES-SYSTEM - Configuracion Principal
# =============================================================================
# Version: 0.1.0
# Ultima actualizacion: 2026-03-16
# =============================================================================

# -----------------------------------------------------------------------------
# Aplicacion
# -----------------------------------------------------------------------------
app:
  name: "Oposiciones System"
  version: "0.1.0"
  environment: "${ENVIRONMENT:development}"

# -----------------------------------------------------------------------------
# Base de Datos
# -----------------------------------------------------------------------------
database:
  temario:
    path: "data/temario.db"
    backup_dir: "backups/"

  oposiciones:
    path: "data/oposiciones.db"
    backup_dir: "backups/"

# -----------------------------------------------------------------------------
# Embeddings (Mistral)
# -----------------------------------------------------------------------------
embeddings:
  provider: "mistral"
  model: "mistral-embed"
  dimensions: 1024
  batch_size: 50
  api_key_env: "MISTRAL_API_KEY"

# -----------------------------------------------------------------------------
# LLM (MiniMax)
# -----------------------------------------------------------------------------
llm:
  provider: "minimax"
  model: "MiniMax-Text-01"
  api_key_env: "MINIMAX_API_KEY"
  group_id_env: "MINIMAX_GROUP_ID"
  temperature: 0.1
  max_tokens: 2048
  base_url: "https://api.minimax.chat/v1"

# -----------------------------------------------------------------------------
# Chunking
# -----------------------------------------------------------------------------
chunking:
  target_tokens: 500
  max_tokens: 700
  min_tokens: 100
  overlap_sentences: 2
  encoding: "cl100k_base"

# -----------------------------------------------------------------------------
# Busqueda
# -----------------------------------------------------------------------------
search:
  default_limit: 5
  similarity_threshold: 0.7
  weights:
    semantic: 0.8
    keyword: 0.2

# -----------------------------------------------------------------------------
# Flashcards (SM-2)
# -----------------------------------------------------------------------------
flashcards:
  sm2:
    default_ease_factor: 2.5
    min_ease_factor: 1.3
    interval_modifier: 1.0
    easy_bonus: 1.3
    new_cards_per_day: 20
    max_reviews_per_day: 100

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
tests:
  default_questions: 10
  max_questions: 50
  time_limit_minutes: 30
  question_types:
    - "multiple_choice"
    - "true_false"
    - "open_ended"

# -----------------------------------------------------------------------------
# AI Analytics
# -----------------------------------------------------------------------------
analytics:
  weak_area_threshold: 0.6
  prediction_confidence_threshold: 0.7
  recommendation_limit: 5

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging:
  level: "${LOG_LEVEL:INFO}"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/oposiciones.log"
  max_size_mb: 10
  backup_count: 5

# -----------------------------------------------------------------------------
# Web Dashboard
# -----------------------------------------------------------------------------
web:
  host: "127.0.0.1"
  port: 8000
  debug: true
  secret_key_env: "WEB_SECRET_KEY"
  templates_dir: "src/web/templates"
  static_dir: "src/web/static"
```

### 6.2 temario.yaml (Modulo)

**Archivo:** `configs/temario.yaml`

```yaml
# =============================================================================
# Modulo Temario - Configuracion
# =============================================================================

database:
  path: "data/temario.db"

embeddings:
  provider: "mistral"
  model: "mistral-embed"
  dimensions: 1024
  batch_size: 50
  api_key_env: "MISTRAL_API_KEY"

llm:
  provider: "minimax"
  model: "MiniMax-Text-01"
  api_key_env: "MINIMAX_API_KEY"
  group_id_env: "MINIMAX_GROUP_ID"
  temperature: 0.1
  max_tokens: 2048

chunking:
  target_tokens: 500
  max_tokens: 700
  min_tokens: 100
  overlap_sentences: 2
  encoding: "cl100k_base"

parser:
  pdf:
    extract_images: false
    extract_tables: true
  docx:
    extract_styles: true
  metadata_patterns:
    tema: "(?i)tema\\s*(\\d+)"
    titulo: "(?i)t[ií]tulo[:\\s]+(.+)"
    apartado: "(?i)apartado\\s*(\\d+)"

search:
  default_limit: 5
  similarity_threshold: 0.7
  weights:
    semantic: 0.8
    keyword: 0.2

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/temario.log"
```

### 6.3 pyproject.toml

**Archivo:** `pyproject.toml`

```toml
[project]
name = "oposiciones-system"
version = "0.1.0"
description = "Sistema integral de preparacion de oposiciones"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your@email.com"}
]

dependencies = [
    # Core
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "pydantic>=2.5.0",

    # CLI
    "typer>=0.9.0",
    "rich>=13.0.0",

    # Documents
    "pymupdf>=1.23.0",      # PDF parsing
    "python-docx>=1.1.0",   # DOCX parsing
    "tiktoken>=0.5.0",      # Token counting

    # AI/ML
    "httpx>=0.25.0",        # API calls
    "numpy>=1.24.0",        # Vector ops

    # Web (FastAPI)
    "fastapi>=0.109.0",
    "uvicorn>=0.25.0",
    "jinja2>=3.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
    "black>=23.0.0",
    "mypy>=1.7.0",
]

[project.scripts]
temario = "src.temario.cli:app"
flashcards = "src.flashcards.cli:app"
tests = "src.tests.cli:app"
ai = "src.ai.cli:app"

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["."]
include = ["src*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4"]

[tool.black]
line-length = 100
target-version = ["py310"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
```

---

## 7. Comandos de Setup

### 7.1 Clonar y Configurar

```bash
# =============================================================================
# SETUP INICIAL - Oposiciones System
# =============================================================================

# 1. Crear directorio del proyecto
mkdir -p ~/Projects/oposiciones-system
cd ~/Projects/oposiciones-system

# 2. Inicializar git
git init
git branch -M main

# 3. Crear estructura de carpetas
mkdir -p src/{temario,flashcards,tests,ai,web/routes,core}
mkdir -p tests/{temario,flashcards,tests,ai,web}
mkdir -p configs
mkdir -p data
mkdir -p logs
mkdir -p backups
mkdir -p documents
mkdir -p scripts

# 4. Crear archivos __init__.py
touch src/__init__.py
touch src/temario/__init__.py
touch src/flashcards/__init__.py
touch src/tests/__init__.py
touch src/ai/__init__.py
touch src/web/__init__.py
touch src/web/routes/__init__.py
touch src/core/__init__.py

# 5. Crear archivos vacios de config
touch configs/config.yaml
touch configs/temario.yaml

# 6. Crear .gitignore
cat > .gitignore << 'EOF'
# Python
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
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Environment
.env
*.env.local

# Database
*.db
*.sqlite3
data/*.db

# Logs
logs/
*.log

# Backups
backups/

# Documents (user data)
documents/*.pdf
documents/*.docx

# Coverage
.coverage
htmlcov/
.pytest_cache/

# MyPy
.mypy_cache/

# OS
.DS_Store
Thumbs.db
EOF

# 7. Crear .env desde template
cp .env.example .env
# EDITAR .env con las API keys reales

# 8. Crear virtual environment
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 9. Instalar dependencias
pip install --upgrade pip
pip install -e ".[dev]"

# 10. Verificar instalacion
python -c "import src; print('OK')"
```

### 7.2 Verificar Setup

```bash
# =============================================================================
# VERIFICACION - Oposiciones System
# =============================================================================

# Verificar Python version (>=3.10)
python --version

# Verificar virtual environment activo
which python  # Debe apuntar a .venv

# Verificar dependencias instaladas
pip list | grep -E "(typer|rich|fastapi|pydantic)"

# Verificar estructura
ls -la src/
ls -la configs/

# Verificar configuracion
cat configs/config.yaml

# Verificar .env (NO mostrar contenido!)
test -f .env && echo ".env exists" || echo ".env missing!"

# Ejecutar tests (deben pasar aunque esten vacios)
pytest -v

# Ejecutar linter
ruff check src/

# Ejecutar formatter
black --check src/
```

### 7.3 Comandos de Desarrollo

```bash
# =============================================================================
# COMANDOS DE DESARROLLO
# =============================================================================

# Activar entorno
source .venv/bin/activate

# Ejecutar tests con cobertura
pytest --cov=src --cov-report=term-missing

# Formatear codigo
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/

# Ejecutar CLI de temario
python -m src.temario.cli --help

# Ejecutar web server
python scripts/run_web.py

# Ejecutar todo (check)
pytest && ruff check src/ && black --check src/
```

---

**Fin del documento de Archivos Fuente**
