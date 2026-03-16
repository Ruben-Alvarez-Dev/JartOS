# Modulo: Temario Ingestion

**Version:** 0.1.0
**Ultima actualizacion:** 2026-03-16

---

## Indice

1. [Descripcion](#1-descripcion)
2. [User Stories](#2-user-stories)
3. [Requirements (RFC 2119)](#3-requirements-rfc-2119)
4. [API Spec](#4-api-spec)
5. [CLI Spec](#5-cli-spec)
6. [Data Models](#6-data-models)
7. [Diagramas de Flujo](#7-diagramas-de-flujo)
8. [Configuracion](#8-configuracion)

---

## 1. Descripcion

El modulo de **Temario Ingestion** permite procesar documentos PDF y DOCX del temario de oposiciones, extraer su contenido, dividirlo en chunks semanticos, generar embeddings vectoriales y almacenar todo en una base de datos SQLite para busqueda semantica.

### Funcionalidades Principales

- Ingestion de documentos PDF y DOCX
- Extraccion de texto con preservacion de estructura
- Chunking inteligente por tokens (~500 tokens por chunk)
- Generacion de embeddings con Mistral API (1024 dimensiones)
- Busqueda semantica por similitud coseno
- Busqueda hibrida (semantica + keyword)
- QA sobre el temario con IA

### Componentes

```
src/temario/
+-- __init__.py      # Exporta componentes principales
+-- models.py        # Data models (Document, Chunk, SearchResult)
+-- store.py         # SQLite database operations
+-- parser.py        # PDF/DOCX parsing
+-- chunker.py       # Text chunking
+-- embedder.py      # Mistral API embeddings
+-- searcher.py      # Semantic search
+-- ingest.py        # Orquestacion de ingestion
+-- cli.py           # CLI commands
```

---

## 2. User Stories

### US-TM-001: Ingerir documento PDF

**Como** opositor
**Quiero** ingresar un documento PDF del temario
**Para** tenerlo disponible para busqueda y estudio

**Criterios de Aceptacion:**
- GIVEN un archivo PDF valido
- WHEN ejecuto el comando de ingestion
- THEN el sistema extrae el texto
- AND crea chunks semanticos
- AND genera embeddings
- AND almacena en la base de datos
- AND muestra resumen de lo procesado

---

### US-TM-002: Ingerir documento DOCX

**Como** opositor
**Quiero** ingresar un documento Word del temario
**Para** tenerlo disponible para busqueda y estudio

**Criterios de Aceptacion:**
- GIVEN un archivo DOCX valido
- WHEN ejecuto el comando de ingestion
- THEN el sistema extrae el texto
- AND preserva estilos (titulos, listas)
- AND crea chunks semanticos
- AND genera embeddings
- AND almacena en la base de datos

---

### US-TM-003: Buscar en el temario

**Como** opositor
**Quiero** buscar informacion en el temario por pregunta natural
**Para** encontrar respuestas rapidamente

**Criterios de Aceptacion:**
- GIVEN una consulta en lenguaje natural
- WHEN ejecuto la busqueda
- THEN el sistema genera embedding de la query
- AND busca por similitud coseno
- AND retorna los chunks mas relevantes
- AND muestra el score de similitud
- AND muestra metadata (tema, pagina)

---

### US-TM-004: Preguntar al temario

**Como** opositor
**Quiero** hacer preguntas sobre el temario y obtener respuestas
**Para** aclarar dudas sin leer todo el documento

**Criterios de Aceptacion:**
- GIVEN una pregunta en lenguaje natural
- WHEN ejecuto el comando de QA
- THEN el sistema busca contexto relevante
- AND envia contexto + pregunta a LLM
- AND genera respuesta con referencias
- AND muestra las fuentes utilizadas

---

### US-TM-005: Ver documentos ingresados

**Como** opositor
**Quiero** ver la lista de documentos ingresados
**Para** saber que temario tengo disponible

**Criterios de Aceptacion:**
- GIVEN documentos previamente ingresados
- WHEN solicito la lista
- THEN el sistema muestra todos los documentos
- AND muestra cantidad de chunks por documento
- AND muestra fecha de ingestion
- AND permite filtrar por tema

---

## 3. Requirements (RFC 2119)

### Requerimientos Funcionales

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| FR-TM-001 | El sistema MUST soportar ingestion de archivos PDF | Alta |
| FR-TM-002 | El sistema MUST soportar ingestion de archivos DOCX | Alta |
| FR-TM-003 | El sistema SHALL dividir el texto en chunks de ~500 tokens | Alta |
| FR-TM-004 | El sistema SHALL generar embeddings de 1024 dimensiones | Alta |
| FR-TM-005 | El sistema SHALL almacenar chunks con sus embeddings | Alta |
| FR-TM-006 | El sistema MUST permitir busqueda semantica | Alta |
| FR-TM-007 | El sistema SHOULD permitir busqueda hibrida | Media |
| FR-TM-008 | El sistema SHALL calcular similitud coseno | Alta |
| FR-TM-009 | El sistema SHALL extraer metadata (tema, pagina, titulo) | Media |
| FR-TM-010 | El sistema MAY detectar idioma automaticamente | Baja |
| FR-TM-011 | El sistema MUST manejar errores de API gracefully | Alta |
| FR-TM-012 | El sistema SHALL mostrar progreso durante ingestion | Media |

### Requerimientos No Funcionales

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| NFR-TM-001 | La ingestion SHALL completar en <60s por documento de 50 paginas | Alta |
| NFR-TM-002 | La busqueda SHALL retornar resultados en <2s | Alta |
| NFR-TM-003 | El sistema SHALL manejar documentos hasta 500 paginas | Media |
| NFR-TM-004 | Los embeddings SHALL almacenarse eficientemente (BLOB) | Alta |
| NFR-TM-005 | El sistema SHALL cachear embeddings para evitar recomputacion | Media |
| NFR-TM-006 | El sistema SHOULD soportar actualizacion de documentos | Baja |

---

## 4. API Spec

### Endpoints REST

#### POST /api/temario/ingest

Ingresa un nuevo documento al sistema.

**Request:**
```http
POST /api/temario/ingest HTTP/1.1
Content-Type: multipart/form-data

file: [PDF/DOCX file]
tema: 1  # Optional: numero de tema
title: "Tema 1 - La Constitucion"  # Optional: titulo personalizado
```

**Response (201 Created):**
```json
{
  "success": true,
  "document": {
    "id": 1,
    "filename": "Tema1.pdf",
    "file_type": "pdf",
    "title": "Tema 1 - La Constitucion",
    "tema": 1,
    "total_pages": 45,
    "total_chunks": 87,
    "created_at": "2026-03-16T10:30:00"
  },
  "chunks_created": 87,
  "embeddings_created": 87,
  "duration_seconds": 12.5
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "INVALID_FILE_TYPE",
  "message": "Solo se soportan archivos PDF y DOCX"
}
```

---

#### GET /api/temario/documents

Lista todos los documentos ingresados.

**Request:**
```http
GET /api/temario/documents?tema=1 HTTP/1.1
```

**Query Parameters:**
| Parametro | Tipo | Requerido | Descripcion |
|-----------|------|-----------|-------------|
| tema | int | No | Filtrar por numero de tema |
| limit | int | No | Maximo de resultados (default: 50) |
| offset | int | No | Offset para paginacion |

**Response (200 OK):**
```json
{
  "total": 10,
  "documents": [
    {
      "id": 1,
      "filename": "Tema1.pdf",
      "title": "Tema 1 - La Constitucion",
      "tema": 1,
      "total_pages": 45,
      "total_chunks": 87,
      "created_at": "2026-03-16T10:30:00"
    }
  ]
}
```

---

#### GET /api/temario/documents/{id}

Obtiene detalles de un documento especifico.

**Response (200 OK):**
```json
{
  "id": 1,
  "filename": "Tema1.pdf",
  "filepath": "/documents/temario/Tema1.pdf",
  "file_type": "pdf",
  "title": "Tema 1 - La Constitucion",
  "tema": 1,
  "total_pages": 45,
  "total_chunks": 87,
  "created_at": "2026-03-16T10:30:00",
  "metadata": {
    "author": "Centro de Estudios",
    "created": "2025-01-15"
  }
}
```

---

#### POST /api/temario/search

Busca en el temario por similitud semantica.

**Request:**
```http
POST /api/temario/search HTTP/1.1
Content-Type: application/json

{
  "query": "Que es la constitucion espanola?",
  "tema": 1,
  "limit": 5,
  "threshold": 0.7
}
```

**Response (200 OK):**
```json
{
  "query": "Que es la constitucion espanola?",
  "search_type": "semantic",
  "total_results": 5,
  "results": [
    {
      "chunk": {
        "id": 42,
        "document_id": 1,
        "content": "La Constitucion Espanola de 1978 es la norma suprema...",
        "token_count": 487,
        "tema": 1,
        "page_number": 5
      },
      "score": 0.89,
      "search_type": "semantic"
    }
  ]
}
```

---

#### POST /api/temario/qa

Pregunta al temario con generacion de respuesta.

**Request:**
```http
POST /api/temario/qa HTTP/1.1
Content-Type: application/json

{
  "question": "Cuales son los principios constitucionales fundamentales?",
  "tema": 1,
  "context_limit": 3
}
```

**Response (200 OK):**
```json
{
  "question": "Cuales son los principios constitucionales fundamentales?",
  "answer": "Los principios constitucionales fundamentales en Espana son...",
  "sources": [
    {
      "chunk_id": 42,
      "document": "Tema1.pdf",
      "page": 5,
      "relevance": 0.89
    }
  ],
  "confidence": 0.85,
  "generated_at": "2026-03-16T10:35:00"
}
```

---

#### DELETE /api/temario/documents/{id}

Elimina un documento y todos sus chunks.

**Response (200 OK):**
```json
{
  "success": true,
  "deleted_chunks": 87,
  "message": "Documento eliminado correctamente"
}
```

---

## 5. CLI Spec

### Comandos

#### temario ingest

Ingresa un documento al sistema.

```bash
python -m src.temario.cli ingest <filepath> [OPTIONS]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|-----------|-----------|-------------|
| filepath | Si | Ruta al archivo PDF o DOCX |

**Opciones:**
| Opcion | Default | Descripcion |
|--------|---------|-------------|
| --tema, -t | None | Numero de tema |
| --title | None | Titulo personalizado |
| --no-embed | False | Saltar generacion de embeddings |
| --verbose, -v | False | Mostrar progreso detallado |

**Ejemplo:**
```bash
# Ingerir PDF basico
python -m src.temario.cli ingest documents/Tema1.pdf

# Ingerir con metadata
python -m src.temario.cli ingest documents/Tema1.pdf --tema 1 --title "Constitucion"

# Modo verbose
python -m src.temario.cli ingest documents/Tema1.pdf -v
```

**Output:**
```
Ingresando documento: Tema1.pdf
+-- Extrayendo texto... OK (45 paginas)
+-- Creando chunks... OK (87 chunks)
+-- Generando embeddings... OK (batch 1/2)
+-- Generando embeddings... OK (batch 2/2)
+-- Guardando en DB... OK

Resumen:
  Documento ID: 1
  Paginas: 45
  Chunks: 87
  Tiempo: 12.5s
```

---

#### temario search

Busca en el temario.

```bash
python -m src.temario.cli search <query> [OPTIONS]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|-----------|-----------|-------------|
| query | Si | Consulta de busqueda |

**Opciones:**
| Opcion | Default | Descripcion |
|--------|---------|-------------|
| --tema, -t | None | Filtrar por tema |
| --limit, -l | 5 | Maximo de resultados |
| --json | False | Output en formato JSON |

**Ejemplo:**
```bash
python -m src.temario.cli search "constitucion espanola" --limit 3
```

**Output:**
```
Buscando: "constitucion espanola"
Encontrados: 3 resultados

[1] Score: 0.89 | Tema 1, Pag 5
    La Constitucion Espanola de 1978 es la norma suprema del ordenamiento
    juridico espanol...

[2] Score: 0.85 | Tema 1, Pag 12
    Los principios constitucionales fundamentales establecen...

[3] Score: 0.82 | Tema 1, Pag 8
    La Constitucion establece los derechos y libertades...
```

---

#### temario ask

Pregunta al temario (QA con IA).

```bash
python -m src.temario.cli ask <question> [OPTIONS]
```

**Opciones:**
| Opcion | Default | Descripcion |
|--------|---------|-------------|
| --tema, -t | None | Filtrar por tema |
| --context, -c | 3 | Numero de chunks de contexto |

**Ejemplo:**
```bash
python -m src.temario.cli ask "Cuales son los derechos fundamentales?"
```

---

#### temario list

Lista documentos ingresados.

```bash
python -m src.temario.cli list [OPTIONS]
```

**Opciones:**
| Opcion | Default | Descripcion |
|--------|---------|-------------|
| --tema, -t | None | Filtrar por tema |

---

#### temario delete

Elimina un documento.

```bash
python -m src.temario.cli delete <document_id>
```

---

## 6. Data Models

### Document

```python
@dataclass
class Document:
    id: Optional[int] = None
    filename: str = ""
    filepath: str = ""
    file_type: str = ""  # 'pdf' or 'docx'
    title: Optional[str] = None
    tema: Optional[int] = None
    total_pages: int = 0
    total_chunks: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: dict = field(default_factory=dict)
```

### Chunk

```python
@dataclass
class Chunk:
    id: Optional[int] = None
    document_id: int = 0
    content: str = ""
    token_count: int = 0
    chunk_index: int = 0
    page_number: Optional[int] = None
    tema: Optional[int] = None
    apartado: Optional[str] = None
    titulo: Optional[str] = None
    embedding: Optional[list] = None  # 1024 floats
    created_at: Optional[str] = None
    metadata: dict = field(default_factory=dict)
```

### SearchResult

```python
@dataclass
class SearchResult:
    chunk: Chunk
    score: float  # 0.0 - 1.0
    search_type: str  # 'semantic' or 'hybrid'
```

### IngestionResult

```python
@dataclass
class IngestionResult:
    success: bool
    document: Optional[Document] = None
    chunks_created: int = 0
    embeddings_created: int = 0
    errors: list = field(default_factory=list)
    duration_seconds: float = 0.0
```

---

## 7. Diagramas de Flujo

### Flujo de Ingestion

```
+-------------+     +-------------+     +-------------+
|   Usuario   |---->|  CLI/API    |---->|  ingest.py  |
|  (input)    |     |  (handler)  |     | (orquest)   |
+-------------+     +-------------+     +-------------+
                                               |
                       +-----------------------+-----------------------+
                       |                       |                       |
                       v                       v                       v
              +-------------+         +-------------+         +-------------+
              |  parser.py  |         | chunker.py  |         | embedder.py |
              | (PDF/DOCX)  |         | (tokens)    |         | (Mistral)   |
              +-------------+         +-------------+         +-------------+
                       |                       |                       |
                       v                       v                       v
                    [texto]               [chunks]              [embeddings]
                       |                       |                       |
                       +-----------------------+-----------------------+
                                               |
                                               v
                                      +-------------+
                                      |  store.py   |
                                      |  (SQLite)   |
                                      +-------------+
```

### Flujo de Busqueda

```
+-------------+     +-------------+     +-------------+
|   Query     |---->|  embedder   |---->|  searcher   |
|   (text)    |     | (Mistral)   |     |  (cosine)   |
+-------------+     +-------------+     +-------------+
                                               |
                                               v
                                        +-------------+
                                        |    DB       |
                                        |  (chunks)   |
                                        +-------------+
                                               |
                                               v
                                        +-------------+
                                        |  Results    |
                                        | (ranked)    |
                                        +-------------+
```

---

## 8. Configuracion

### configs/temario.yaml

```yaml
# Database settings
database:
  path: "data/temario.db"

# Embedding settings
embeddings:
  provider: "mistral"
  model: "mistral-embed"
  dimensions: 1024
  batch_size: 50
  api_key_env: "MISTRAL_API_KEY"

# LLM settings for QA
llm:
  provider: "minimax"
  model: "MiniMax-Text-01"
  api_key_env: "MINIMAX_API_KEY"
  group_id_env: "MINIMAX_GROUP_ID"
  temperature: 0.1
  max_tokens: 2048

# Chunking settings
chunking:
  target_tokens: 500
  max_tokens: 700
  min_tokens: 100
  overlap_sentences: 2
  encoding: "cl100k_base"  # Tiktoken encoding

# Parser settings
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

# Search settings
search:
  default_limit: 5
  similarity_threshold: 0.7
  weights:
    semantic: 0.8
    keyword: 0.2

# Logging
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/temario.log"
```

---

**Fin del documento del Modulo Temario Ingestion**
