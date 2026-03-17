# 📚 INGESTA (INBOX/LAB) Y FLUJO DE DATOS (RAG)

## 1. Visión General

El sistema de conocimiento de JartOS sigue un **pipeline de destilación de 5 escalones** que transforma información cruda en **Golden RAG** (conocimiento verificado).

```
DATOS CRUDOS (PDFs, Videos, Audio, Web)
    │
    ▼
┌─────────────────────────────────────────┐
│  ESCALÓN 1: INGESTA                     │
│  - OCR (Tesseract/GPT-4 Vision)         │
│  - Transcripción (Whisper)              │
│  - Parsing estructurado                 │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  ESCALÓN 2: INBOX (Verdad Oficial)      │
│  - BOE, Currículos oficiales            │
│  - No sujetos a crítica                 │
│  - Análisis de consistencia estructural │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  ESCALÓN 3: LAB (Zona de Discusión)     │
│  - Apuntes propios                      │
│  - Fuentes dudosas                      │
│  - Requiere aprobación explícita        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  ESCALÓN 4: PROCESAMIENTO AGENTES       │
│  - Especialistas analizan               │
│  - Concilio valida (3/3 votos)          │
│  - Estructuración y enriquecimiento     │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  ESCALÓN 5: GOLDEN RAG                  │
│  - Conocimiento verificado final        │
│  - Alta inmutabilidad (no absoluta)     │
│  - Base para todas las consultas        │
└─────────────────────────────────────────┘
```

---

## 2. Esquema de Base de Datos (`temario.db`)

**Ubicación:** `TIER_06_STORAGE/data/temario.db`
**Motor:** SQLite

### Tabla `temario_documents`
```sql
CREATE TABLE temario_documents (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    source TEXT,          -- 'BOE', 'TODOFP', 'AUTOR_X', 'LAB'
    created_at TEXT,
    processed_at TEXT,
    status TEXT,          -- 'pending', 'validated', 'golden'
    metadata TEXT         -- JSON
);
```

### Tabla `temario_chunks`
```sql
CREATE TABLE temario_chunks (
    id TEXT PRIMARY KEY,
    document_id TEXT,
    chunk_index INTEGER,
    content TEXT NOT NULL,
    metadata TEXT,        -- JSON con tags, tema, etc.
    embedding TEXT,       -- Vector JSON (768 dimensiones)
    escalation_level INTEGER DEFAULT 1,
    verified BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (document_id) REFERENCES temario_documents(id)
);
```

### Índices
```sql
CREATE INDEX idx_chunks_document ON temario_chunks(document_id);
CREATE INDEX idx_chunks_verified ON temario_chunks(verified);
CREATE INDEX idx_docs_status ON temario_documents(status);
```

---

## 3. Directorios Físicos

```
/Volumes/NVME_4TB/jartos-data/
├── INBOX/                    # Escalón 2: Verdad Oficial
│   ├── BOE/                  # Boletines oficiales
│   ├── TODOFP/               # Currículos oficiales
│   └── AUTORES/              # Temarios de autores reconocidos
│
├── LAB/                      # Escalón 3: Discusión
│   ├── apuntes/              # Apuntes propios
│   ├── internet/             # Fuentes web
│   └── pendientes/           # A revisar
│
├── PROCESSED/                # Escalón 4: En proceso
│   ├── chunks/               # Fragmentos procesados
│   └── embeddings/           # Vectores generados
│
└── GOLDEN_RAG/               # Escalón 5: Conocimiento verificado
    ├── temario/              # Temario estructurado
    ├── normativas/           # Leyes y regulaciones
    └── flashcards/           # Tarjetas de estudio
```

---

## 4. Pipeline de Ingesta INBOX

### Flujo Automático
```
1. Usuario mueve PDF a /INBOX
2. watchdog_inbox.py detecta el archivo
3. DocumentParser extrae texto (OCR si es necesario)
4. TextChunker divide en fragmentos (~500 tokens)
5. MistralEmbedder genera vectores (768 dims)
6. TemarioStore guarda en SQLite
7. Estado = 'validated' (INBOX no requiere aprobación)
```

### Código de Referencia
```python
# TIER_05_INGEST/watchdog_inbox.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class INBOXHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(('.pdf', '.docx', '.txt')):
            process_document(event.src_path, source='INBOX')

# Procesamiento
def process_document(filepath, source):
    text = DocumentParser.parse(filepath)
    chunks = TextChunker.chunk(text, size=500)
    embeddings = MistralEmbedder.embed_batch(chunks)
    TemarioStore.insert(chunks, embeddings, source=source, auto_validate=(source=='INBOX'))
```

---

## 5. Pipeline de Ingesta LAB

### Flujo con Aprobación
```
1. Usuario mueve archivo a /LAB
2. watchdog_lab.py detecta el archivo
3. DocumentParser extrae texto
4. Agente Investigador genera resumen y propuesta
5. Notificación al usuario (Telegram/Web UI)
6. Usuario aprueba o rechaza
7. Si aprueba: se vectoriza e inserta
8. Si rechaza: se archiva en /LAB/rechazados/
```

### Endpoint de Aprobación
```http
POST /api/v1/lab/approve
Content-Type: application/json

{
  "document_id": "doc_123",
  "approved": true,
  "notes": "Confirmado con fuente secundaria"
}
```

---

## 6. Sistema RAG Híbrido

| Tipo | Backend | Contenido | Uso |
|------|---------|-----------|-----|
| **RAG Estático** | SQLite | BOE, currículos | Fuente de verdad inmutable |
| **RAG Dinámico** | Qdrant | Apuntes, notas | Búsqueda semántica |
| **RAG Vectorial** | Qdrant | Contenido procesado | Consultas de agentes |

### Configuración Qdrant
```yaml
# Colecciones
collections:
  - name: temario_golden
    vectors:
      size: 768
      distance: Cosine
    payload_schema:
      tema: keyword
      autor: keyword
      escalon: integer
      verified: bool
```

---

## 7. Contratos de Calidad (Quality Contracts)

| ID | Contrato | Prioridad | Descripción |
|----|----------|-----------|-------------|
| QC-001 | Alineación Curricular | CRÍTICA | Todo contenido debe citar RA y CE oficiales |
| QC-002 | Integridad Terminológica | ALTA | Usar terminología oficial del currículo |
| QC-003 | Formato Estructurado | MEDIA | Seguir plantillas Junta de Andalucía |
| QC-004 | Coherencia Temporal | MEDIA | Horas de actividades ≤ Total horas módulo |

---

## 8. Embeddings

### Modelo por Defecto
- **Modelo:** Mistral Embed (`mistral-embed`)
- **Dimensiones:** 768
- **Normalización:** Cosine similarity

### Alternativas
| Modelo | Dimensiones | Uso |
|--------|-------------|-----|
| `nomic-embed-text` | 768 | Local (Ollama) |
| `text-embedding-3-small` | 1536 | OpenAI |
| `voyage-2` | 1024 | Alternativa cloud |
