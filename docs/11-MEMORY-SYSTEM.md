# Sistema de Memoria

**Ultima actualizacion:** 2026-03-16
**Version:** 1.0.0
**Origen:** OPENCLAW-system + OPENCLAW-city

---

## Indice

1. [Vision General](#vision-general)
2. [Los 4 Tipos de Memoria](#los-4-tipos-de-memoria)
3. [Motor de Conocimiento 5 Capas](#motor-de-conocimiento-5-capas)
4. [Integracion con RAG Store](#integracion-con-rag-store)
5. [Implementacion Tecnica](#implementacion-tecnica)
6. [APIs y Uso](#apis-y-uso)

---

## Vision General

El sistema de memoria combina dos componentes heredados:

1. **Sistema de 4 Tipos de Memoria** (OPENCLAW-system) - Organizacion jerarquica
2. **RAG Store + Memory Store** (OPENCLAW-city) - Implementacion tecnica

### Diagrama de Componentes

```
+============================================================================+
|                    SISTEMA DE MEMORIA INTEGRADO                             |
+============================================================================+
                                       |
           +---------------------------+---------------------------+
           |                           |                           |
           v                           v                           v
+----------------------+    +----------------------+    +----------------------+
|   RAG STORE          |    |   MEMORY STORE       |    |   SECURITY PIPELINE  |
|                      |    |                      |    |                      |
| /opt/openclaw-memory/|    | /opt/openclaw-memory/|    | /opt/openclaw-memory/|
| rag_store.py         |    | memory_store.py      |    | security_pipeline.py |
|                      |    |                      |    |                      |
| - Embeddings 1024d   |    | - 4 tipos memoria    |    | - Validacion inputs  |
| - Busqueda semantica |    | - Persistencia       |    | - Sanitizacion       |
| - Chunks de texto    |    | - Contexto agentes   |    | - Auditoria          |
+----------------------+    +----------------------+    +----------------------+
           |                           |                           |
           +---------------------------+---------------------------+
                                       |
                                       v
+============================================================================+
|                         BASES DE DATOS                                      |
|  +---------------------------+  +-----------------------------+             |
|  |   temario.db              |  |   oposiciones.db            |             |
|  |   - documents             |  |   - memory_agent            |             |
|  |   - chunks                |  |   - memory_unit             |             |
|  |   - embeddings            |  |   - memory_domain           |             |
|  |                           |  |   - memory_global           |             |
|  +---------------------------+  +-----------------------------+             |
+============================================================================+
```

---

## Los 4 Tipos de Memoria

### Jerarquia de Memoria

```
+============================================================================+
|                         MEMORIA GLOBAL                                      |
|              (Conocimiento transversal del sistema)                         |
|  +------------------------------------------------------------------------+ |
|  | - Configuracion del sistema                                            | |
|  | - Normativas de oposiciones                                           | |
|  | - Estructura general del temario                                      | |
|  | - Patrones de estudio validados                                       | |
|  | - Conocimiento compartido por todos los agentes                       | |
|  +------------------------------------------------------------------------+ |
|  Scope: Todo el sistema                                                    |
|  Persistencia: Permanente                                                  |
|  Acceso: Todos los agentes (lectura)                                       |
+============================================================================+
            |                                  |
            | Hereda de                        | Hereda de
            v                                  v
+===========================+    +===========================+
|     MEMORIA DOMINIO       |    |     MEMORIA DOMINIO       |
|      (Temario)            |    |      (Tests)              |
|  +--------------------+   |    |  +--------------------+   |
|  | - Tema 1 completo  |   |    |  | - Tests del Tema 1 |   |
|  | - Tema 2 completo  |   |    |  | - Tests del Tema 2 |   |
|  | - Conceptos clave  |   |    |  | - Estadisticas     |   |
|  | - Relaciones       |   |    |  | - Patrones error   |   |
|  +--------------------+   |    |  +--------------------+   |
|  Scope: Un dominio         |    |  Scope: Un dominio        |
|  Ejemplo: "Derecho Const"  |    |  Ejemplo: "Tests general" |
+===========================+    +===========================+
            |                                  |
            | Hereda de                        | Hereda de
            v                                  v
+===========================+    +===========================+
|     MEMORIA UNIDAD        |    |     MEMORIA UNIDAD        |
|   (Equipo Flashcards)     |    |    (Equipo Analytics)     |
|  +--------------------+   |    |  +--------------------+   |
|  | - Deck "Tema 1"    |   |    |  | - Metricas semana  |   |
|  | - 50 flashcards    |   |    |  | - Predicciones     |   |
|  | - Progreso: 65%    |   |    |  | - Alertas          |   |
|  | - Config SM-2      |   |    |  +--------------------+   |
|  +--------------------+   |    |                            |
|  Scope: Un equipo/agente   |    |  Scope: Un equipo/agente   |
+===========================+    +===========================+
            |                                  |
            | Hereda de                        | Hereda de
            v                                  v
+===========================+    +===========================+
|     MEMORIA AGENTE        |    |     MEMORIA AGENTE        |
|     (librarian)           |    |      (analyst)            |
|  +--------------------+   |    |  +--------------------+   |
|  | - Tarea actual     |   |    |  | - Analisis en curso|   |
|  | - Ultimas busquedas|   |    |  | - Ultimos informes |   |
|  | - Contexto dialogo |   |    |  | - Contexto actual  |   |
|  +--------------------+   |    |  +--------------------+   |
|  Scope: Agente individual  |    |  Scope: Agente individual  |
+===========================+    +===========================+
```

### Tabla Comparativa

| Tipo | Scope | Ejemplo en Oposiciones | TTL |
|------|-------|------------------------|-----|
| **GLOBAL** | Sistema completo | "Hay 20 temas en el temario" | Permanente |
| **DOMAIN** | Dominio tematico | "Tema 5 trata de procedimiento administrativo" | Permanente |
| **UNIT** | Equipo de agentes | "El deck de Tema 1 tiene 50 flashcards" | Sesion |
| **AGENT** | Agente individual | "Ultima busqueda del usuario fue 'recurso'" | Corto |

### Casos de Uso por Tipo

#### Memoria Global
```yaml
uso: "Configuracion y conocimiento base"
ejemplos:
  - clave: "sistema.config"
    valor: { version: "1.0.0", temas_total: 20 }
  - clave: "temario.estructura"
    valor: { temas: [1..20], formato: "PDF" }
  - clave: "normativas.relevantes"
    valor: ["CE 1978", "LRJSP 2015"]
```

#### Memoria Dominio
```yaml
uso: "Conocimiento por tema/materia"
ejemplos:
  - clave: "tema.5.resumen"
    valor: "Procedimiento administrativo. Fases: iniciacion..."
  - clave: "tema.5.conceptos"
    valor: ["acto administrativo", "silencio administrativo"]
  - clave: "test.estadisticas.tema5"
    valor: { media: 7.5, intentos: 12 }
```

#### Memoria Unidad
```yaml
uso: "Contexto de equipo de trabajo"
ejemplos:
  - clave: "flashcards.deck.tema1"
    valor: { total: 50, pendientes: 12, facil: 20 }
  - clave: "analyst.sesion_actual"
    valor: { areas_debiles: ["tema3", "tema7"] }
```

#### Memoria Agente
```yaml
uso: "Contexto personal del agente"
ejemplos:
  - clave: "librarian.ultima_busqueda"
    valor: { query: "recurso reposicion", resultados: 5 }
  - clave: "mentor.ultimo_feedback"
    valor: { flashcard_id: 123, rating: 4 }
```

---

## Motor de Conocimiento 5 Capas

**Origen:** OPENCLAW-system

### Diagrama de Capas

```
+============================================================================+
|                           CAPA 5: WISDOM                                    |
|                        (Insights y Patrones)                                |
|  - Prediccion de areas de fallo                                            |
|  - Recomendaciones personalizadas                                          |
|  - Patrones de aprendizaje detectados                                      |
+============================================================================+
                                       ^
                                       | Deriva de
+============================================================================+
|                        CAPA 4: KNOWLEDGE                                    |
|                   (Conocimiento Estructurado)                               |
|  - Relaciones entre conceptos                                              |
|  - Mapas mentales por tema                                                 |
|  - Prerrequisitos de aprendizaje                                           |
+============================================================================+
                                       ^
                                       | Estructura
+============================================================================+
|                          CAPA 3: INDEXED                                    |
|                      (Indices y Embeddings)                                 |
|  - Embeddings Mistral 1024 dims                                            |
|  - Indice invertido de terminos                                            |
|  - Tags y categorias                                                       |
+============================================================================+
                                       ^
                                       | Procesa
+============================================================================+
|                         CAPA 2: PROCESSED                                   |
|                         (Datos Procesados)                                  |
|  - Chunks semanticos (500 tokens)                                          |
|  - Metadatos extraidos                                                     |
|  - Duplicados eliminados                                                   |
+============================================================================+
                                       ^
                                       | Extrae de
+============================================================================+
|                          CAPA 1: RAW DATA                                   |
|                          (Datos Brutos)                                     |
|  - PDFs originales                                                         |
|  - Archivos DOCX                                                           |
| - Texto sin procesar                                                       |
+============================================================================+
```

### Flujo de Procesamiento

```
PDF Original
    |
    v
+------------------+
| CAPA 1: RAW DATA |
| - Bytes del PDF  |
| - Sin estructura |
+------------------+
    |
    | PyMuPDF (fitz)
    v
+----------------------+
| CAPA 2: PROCESSED    |
| - Texto extraido     |
| - Chunks de 500 tok  |
| - Metadata (pag, etc)|
+----------------------+
    |
    | Mistral Embeddings
    v
+----------------------+
| CAPA 3: INDEXED      |
| - Vector 1024 dims   |
| - Indice invertido   |
| - Tags               |
+----------------------+
    |
    | MiniMax Analysis
    v
+----------------------+
| CAPA 4: KNOWLEDGE    |
| - Conceptos clave    |
| - Relaciones         |
| - Prerrequisitos     |
+----------------------+
    |
    | ML + Estadisticas
    v
+----------------------+
| CAPA 5: WISDOM       |
| - Predicciones       |
| - Recomendaciones    |
| - Patrones usuario   |
+----------------------+
```

### Implementacion en Oposiciones

| Capa | Componente | Datos |
|------|------------|-------|
| RAW | `/data/raw/` | PDFs originales |
| PROCESSED | `temario.db.chunks` | Chunks de texto |
| INDEXED | `temario.db.embeddings` | Vectores 1024d |
| KNOWLEDGE | `oposiciones.db.concepts` | Conceptos extraidos |
| WISDOM | `oposiciones.db.recommendations` | Recomendaciones IA |

---

## Integracion con RAG Store

### RAG Store de OPENCLAW-city

**Path:** `/opt/openclaw-memory/rag_store.py`

**Funcionalidades existentes:**
```python
class RAGStore:
    """RAG Store - OPENCLAW-city (produccion)"""

    def __init__(self, db_path: str):
        """Inicializa con path a SQLite"""

    def add_document(self, doc_id: str, chunks: List[str],
                     embeddings: List[List[float]], metadata: List[dict]):
        """Anade documento con chunks y embeddings"""

    def search(self, query_embedding: List[float], k: int = 5,
               threshold: float = 0.7) -> List[dict]:
        """Busqueda por similitud coseno"""

    def get_chunk(self, chunk_id: int) -> dict:
        """Obtiene chunk por ID"""

    def delete_document(self, doc_id: str) -> bool:
        """Elimina documento y chunks asociados"""
```

### Adaptacion para Oposiciones

```python
# Adaptacion del RAG Store existente
class TemarioRAGStore(RAGStore):
    """RAG Store adaptado para temario de oposiciones"""

    def search_by_tema(self, query: str, tema: int, k: int = 5) -> List[dict]:
        """Busca dentro de un tema especifico"""
        query_embedding = self.embed(query)  # Mistral 1024d
        results = self.search(query_embedding, k=k*2)
        return [r for r in results if r['metadata'].get('tema') == tema][:k]

    def get_weak_areas_chunks(self, weak_areas: List[str]) -> List[dict]:
        """Obtiene chunks de areas debiles"""
        chunks = []
        for area in weak_areas:
            results = self.search_by_area(area)
            chunks.extend(results)
        return chunks

    def get_random_chunks_for_test(self, tema: int, n: int) -> List[dict]:
        """Obtiene chunks aleatorios para generar test"""
        # Implementacion...
```

---

## Implementacion Tecnica

### Esquema de Base de Datos

#### temario.db (Heredado de RAG Store)

```sql
-- Documentos ingresados
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    file_type TEXT CHECK(file_type IN ('pdf', 'docx')),
    title TEXT,
    tema INTEGER,
    total_pages INTEGER DEFAULT 0,
    total_chunks INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT,
    metadata JSON
);

-- Chunks con embeddings (CAPA 2 y 3)
CREATE TABLE chunks (
    id INTEGER PRIMARY KEY,
    document_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    token_count INTEGER DEFAULT 0,
    chunk_index INTEGER DEFAULT 0,
    page_number INTEGER,
    tema INTEGER,
    apartado TEXT,
    titulo TEXT,
    embedding BLOB,  -- 1024 float32 = 4096 bytes (Mistral)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    metadata JSON,
    FOREIGN KEY (document_id) REFERENCES documents(id)
);

-- Indice para busqueda rapida
CREATE INDEX idx_chunks_document ON chunks(document_id);
CREATE INDEX idx_chunks_tema ON chunks(tema);
CREATE INDEX idx_chunks_apartado ON chunks(apartado);
```

#### oposiciones.db (Sistema de Memoria 4 Tipos)

```sql
-- Memoria Global
CREATE TABLE memory_global (
    id INTEGER PRIMARY KEY,
    key TEXT NOT NULL UNIQUE,
    value JSON NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT,
    metadata JSON
);

-- Memoria Dominio
CREATE TABLE memory_domain (
    id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,  -- "temario", "tests", "flashcards"
    key TEXT NOT NULL,
    value JSON NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT,
    metadata JSON,
    UNIQUE(domain, key)
);

CREATE INDEX idx_memory_domain ON memory_domain(domain);

-- Memoria Unidad
CREATE TABLE memory_unit (
    id INTEGER PRIMARY KEY,
    unit_id TEXT NOT NULL,  -- "flashcards-team", "analytics-team"
    key TEXT NOT NULL,
    value JSON NOT NULL,
    session_id TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    expires_at TEXT,
    metadata JSON,
    UNIQUE(unit_id, key)
);

CREATE INDEX idx_memory_unit ON memory_unit(unit_id);

-- Memoria Agente
CREATE TABLE memory_agent (
    id INTEGER PRIMARY KEY,
    agent_namespace TEXT NOT NULL,  -- "librarian", "analyst"
    key TEXT NOT NULL,
    value JSON NOT NULL,
    session_id TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    expires_at TEXT,
    metadata JSON,
    UNIQUE(agent_namespace, key)
);

CREATE INDEX idx_memory_agent ON memory_agent(agent_namespace);

-- Conocimiento estructurado (CAPA 4)
CREATE TABLE concepts (
    id INTEGER PRIMARY KEY,
    tema INTEGER NOT NULL,
    name TEXT NOT NULL,
    definition TEXT,
    related_concepts JSON,  -- [concept_id, ...]
    source_chunk_ids JSON,  -- [chunk_id, ...]
    difficulty INTEGER DEFAULT 3,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_concepts_tema ON concepts(tema);

-- Wisdom / Insights (CAPA 5)
CREATE TABLE insights (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,  -- "prediction", "recommendation", "pattern"
    scope TEXT,  -- "global", "domain", "unit", "agent"
    scope_id TEXT,
    content JSON NOT NULL,
    confidence REAL DEFAULT 0.5,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    valid_until TEXT,
    metadata JSON
);

CREATE INDEX idx_insights_type ON insights(type);
CREATE INDEX idx_insights_scope ON insights(scope, scope_id);
```

---

## APIs y Uso

### MemoryStore API

```python
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

class MemoryType(Enum):
    AGENT = "agent"
    UNIT = "unit"
    DOMAIN = "domain"
    GLOBAL = "global"

class MemoryStore:
    """
    Memory Store - Basado en /opt/openclaw-memory/memory_store.py
    Sistema de memoria de 4 tipos
    """

    def __init__(self, db_path: str = "data/oposiciones.db"):
        self.db_path = db_path
        self._init_db()

    def save(self, key: str, value: Dict, memory_type: MemoryType,
             scope_id: Optional[str] = None,
             ttl_hours: Optional[int] = None) -> int:
        """
        Guarda un valor en el nivel de memoria especificado.

        Args:
            key: Clave unica
            value: Valor a guardar (dict)
            memory_type: Nivel de memoria (AGENT, UNIT, DOMAIN, GLOBAL)
            scope_id: ID del scope (agent name, unit id, domain name)
            ttl_hours: Tiempo de vida en horas (None = permanente)

        Returns:
            ID del registro creado
        """
        table = f"memory_{memory_type.value}"
        expires_at = None
        if ttl_hours:
            expires_at = (datetime.now() + timedelta(hours=ttl_hours)).isoformat()

        # Insertar segun tipo
        # ...

    def get(self, key: str, memory_type: MemoryType,
            scope_id: Optional[str] = None) -> Optional[Dict]:
        """
        Recupera un valor del nivel de memoria.
        """
        # ...

    def search(self, query: str, scopes: List[MemoryType],
               limit: int = 10) -> List[Dict]:
        """
        Busca en multiples niveles de memoria.
        Busca en el valor JSON usando LIKE.
        """
        # ...

    def delete(self, key: str, memory_type: MemoryType,
               scope_id: Optional[str] = None) -> bool:
        """
        Elimina un valor de memoria.
        """
        # ...

    def clear_expired(self) -> int:
        """
        Limpia registros expirados.
        Returns: Numero de registros eliminados.
        """
        # ...


# Ejemplo de uso
memory = MemoryStore()

# Guardar en memoria global
memory.save(
    key="sistema.config",
    value={"version": "1.0.0", "temas_total": 20},
    memory_type=MemoryType.GLOBAL
)

# Guardar en memoria dominio
memory.save(
    key="tema.5.resumen",
    value={"resumen": "Procedimiento administrativo..."},
    memory_type=MemoryType.DOMAIN,
    scope_id="temario"
)

# Guardar en memoria agente (con TTL)
memory.save(
    key="ultima_busqueda",
    value={"query": "recurso reposicion", "resultados": 5},
    memory_type=MemoryType.AGENT,
    scope_id="librarian",
    ttl_hours=24
)

# Recuperar
config = memory.get("sistema.config", MemoryType.GLOBAL)

# Buscar en multiples niveles
results = memory.search(
    query="tema 5",
    scopes=[MemoryType.DOMAIN, MemoryType.GLOBAL]
)
```

### RAGStore API

```python
from typing import List, Dict
import numpy as np

class RAGStore:
    """
    RAG Store - Basado en /opt/openclaw-memory/rag_store.py
    Busqueda semantica con embeddings
    """

    def __init__(self, db_path: str = "data/temario.db",
                 embedding_dim: int = 1024):
        self.db_path = db_path
        self.embedding_dim = embedding_dim

    def add_chunks(self, document_id: int, chunks: List[Dict]):
        """
        Anade chunks con embeddings.

        chunks: [{"content": "...", "embedding": [...], "metadata": {...}}]
        """
        # ...

    def search(self, query_embedding: List[float], k: int = 5,
               threshold: float = 0.7, tema_filter: int = None) -> List[Dict]:
        """
        Busqueda por similitud coseno.

        Args:
            query_embedding: Vector de consulta (1024 dims)
            k: Numero de resultados
            threshold: Umbral minimo de similitud
            tema_filter: Filtrar por tema (opcional)

        Returns:
            [{"chunk_id", "content", "similarity", "metadata"}]
        """
        # ...

    def get_by_tema(self, tema: int, limit: int = 100) -> List[Dict]:
        """Obtiene todos los chunks de un tema."""
        # ...


# Ejemplo de uso
rag = RAGStore()

# Obtener embedding de consulta (via Mistral API)
query = "que es el silencio administrativo"
query_embedding = mistral_client.embed(query)  # 1024 dims

# Buscar
results = rag.search(
    query_embedding=query_embedding,
    k=5,
    tema_filter=5  # Solo en Tema 5
)

for result in results:
    print(f"[{result['similarity']:.2f}] {result['content'][:100]}...")
```

### Integracion Completa

```python
class OposicionesMemory:
    """Sistema de memoria integrado para Oposiciones"""

    def __init__(self):
        self.memory = MemoryStore("data/oposiciones.db")
        self.rag = RAGStore("data/temario.db")

    def remember_search(self, agent: str, query: str, results: List):
        """Guarda contexto de busqueda en memoria agente"""
        self.memory.save(
            key="ultima_busqueda",
            value={"query": query, "count": len(results)},
            memory_type=MemoryType.AGENT,
            scope_id=agent,
            ttl_hours=24
        )

    def get_study_context(self) -> Dict:
        """Obtiene contexto completo para sesion de estudio"""
        return {
            "global": self.memory.get("sistema.config", MemoryType.GLOBAL),
            "domain": self.memory.search("tema", [MemoryType.DOMAIN]),
            "weak_areas": self.memory.get("areas_debiles",
                                          MemoryType.GLOBAL)
        }

    def save_progress(self, session_data: Dict):
        """Guarda progreso de sesion"""
        # Memoria unidad (equipo de estudio)
        self.memory.save(
            key=f"sesion.{datetime.now().date()}",
            value=session_data,
            memory_type=MemoryType.UNIT,
            scope_id="study-team"
        )
```

---

**Fin del documento de Sistema de Memoria (v1.0.0)**
