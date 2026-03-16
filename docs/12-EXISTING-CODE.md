# Codigo Existente a Reutilizar

**Ultima actualizacion:** 2025-03-16
**Version:** 1.0.0
**Origen:** OPENCLAW-city (Produccion) + OPENCLAW-system + JartOS

---

## Indice

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Codigo OPENCLAW-city (Produccion)](#codigo-openclaw-city-produccion)
3. [Codigo OPENCLAW-system (GitHub)](#codigo-openclaw-system-github)
4. [Codigo JartOS (Local)](#codigo-jartos-local)
5. [Tabla de Reutilizacion](#tabla-de-reutilizacion)
6. [Plan de Migracion](#plan-de-migracion)

---

## Resumen Ejecutivo

### Cantidad de Codigo Reutilizable

| Sistema | Ubicacion | Archivos Clave | Reutilizacion |
|---------|-----------|----------------|---------------|
| **OPENCLAW-city** | VPS `/opt/openclaw-memory/` | 4 archivos Python | 70% directo |
| **OPENCLAW-system** | GitHub | Arquitectura agentes | 50% adaptar |
| **JartOS** | `/Volumes/-Documents/ARCHIVOS MAC MINI/JartOS` | 690 archivos .md | Patrones |

### Decision Clave

**Reutilizar antes que reescribir** - El codigo de OPENCLAW-city esta en produccion y funciona.

---

## Codigo OPENCLAW-city (Produccion)

### Archivos Existentes en VPS

```
/opt/openclaw-memory/
├── rag_store.py           # RAG Store - Busqueda semantica
├── memory_store.py        # Memory Store - Persistencia
├── security_pipeline.py   # Security Pipeline - Validacion
├── ramiro_bot.py          # Bot Telegram "Ramiro"
├── config.py              # Configuracion
└── requirements.txt       # Dependencias
```

---

### 1. RAG Store

**Path Original:** `/opt/openclaw-memory/rag_store.py`
**Reutilizacion:** 80% directo
**Destino:** `03-SERVICES/temario-service/rag_store.py`

#### Funciones a Copiar

| Funcion | Descripcion | Copiar? |
|---------|-------------|---------|
| `__init__(db_path)` | Inicializa conexion SQLite | Si |
| `add_document(doc_id, chunks, embeddings, metadata)` | Anade documento con chunks | Si |
| `search(query_embedding, k, threshold)` | Busqueda por similitud coseno | Si |
| `get_chunk(chunk_id)` | Obtiene chunk por ID | Si |
| `delete_document(doc_id)` | Elimina documento | Si |
| `_cosine_similarity(a, b)` | Calcula similitud | Si |

#### Adaptaciones Necesarias

```python
# ANTES (OPENCLAW-city)
class RAGStore:
    def __init__(self, db_path: str = "/data/openclaw/rag.db"):
        # ...

# DESPUES (Oposiciones)
class TemarioRAGStore(RAGStore):
    def __init__(self, db_path: str = "data/temario.db"):
        super().__init__(db_path)

    # NUEVO: Filtrar por tema
    def search_by_tema(self, query_embedding, tema: int, k: int = 5):
        results = self.search(query_embedding, k=k*2)
        return [r for r in results if r['metadata'].get('tema') == tema][:k]

    # NUEVO: Obtener chunks aleatorios para test
    def get_random_chunks(self, tema: int, n: int):
        # ...
```

---

### 2. Memory Store

**Path Original:** `/opt/openclaw-memory/memory_store.py`
**Reutilizacion:** 70% directo
**Destino:** `03-SERVICES/memory-service/memory_store.py`

#### Funciones a Copiar

| Funcion | Descripcion | Copiar? |
|---------|-------------|---------|
| `save(key, value, scope)` | Guarda en memoria | Si, adaptar scope |
| `get(key, scope)` | Recupera de memoria | Si |
| `search(query, scopes)` | Busca en memoria | Si |
| `delete(key, scope)` | Elimina registro | Si |
| `_serialize(value)` | Serializa JSON | Si |
| `_deserialize(data)` | Deserializa | Si |

#### Adaptaciones Necesarias

```python
# ANTES (OPENCLAW-city) - 2 tipos de memoria
class MemoryStore:
    SCOPE_SESSION = "session"
    SCOPE_PERSISTENT = "persistent"

# DESPUES (Oposiciones) - 4 tipos de memoria
from enum import Enum

class MemoryType(Enum):
    AGENT = "agent"
    UNIT = "unit"
    DOMAIN = "domain"
    GLOBAL = "global"

class OposicionesMemoryStore(MemoryStore):
    def save(self, key, value, memory_type: MemoryType, scope_id=None):
        table = f"memory_{memory_type.value}"
        # Adaptar logica para 4 tablas
```

---

### 3. Security Pipeline

**Path Original:** `/opt/openclaw-memory/security_pipeline.py`
**Reutilizacion:** 90% directo
**Destino:** `10-SECURITY/validation/security_pipeline.py`

#### Funciones a Copiar

| Funcion | Descripcion | Copiar? |
|---------|-------------|---------|
| `validate_input(data, schema)` | Valida datos contra schema | Si |
| `sanitize_text(text)` | Limpia texto de entrada | Si |
| `check_rate_limit(user_id)` | Verifica rate limiting | Si, adaptar |
| `log_access(user_id, action)` | Registra acceso | Si |
| `validate_file_upload(file)` | Valida archivo subido | Si |

#### Adaptaciones Minimas

```python
# ANTES (OPENCLAW-city)
SECURITY_CONFIG = {
    "max_file_size": 50 * 1024 * 1024,  # 50MB
    "allowed_extensions": [".pdf", ".docx", ".txt", ".md"]
}

# DESPUES (Oposiciones) - Mismo codigo
SECURITY_CONFIG = {
    "max_file_size": 50 * 1024 * 1024,  # 50MB
    "allowed_extensions": [".pdf", ".docx"],  # Solo documentos
    "max_chunks_per_doc": 1000,
    "max_query_length": 500
}
```

---

### 4. Ramiro Bot (Telegram)

**Path Original:** `/opt/openclaw-memory/ramiro_bot.py`
**Reutilizacion:** 60% como base
**Destino:** `06-INTERFACE/telegram/oposiciones_bot.py`

#### Comandos Actuales de Ramiro

| Comando | Funcion | Reutilizar? |
|---------|---------|-------------|
| `/start` | Iniciar bot | Si |
| `/help` | Mostrar ayuda | Si, adaptar |
| `/search` | Buscar en conocimiento | Si, para temario |
| `/ask` | Pregunta a IA | Si, para flashcards |
| `/status` | Estado del sistema | Si |
| `/history` | Historial conversacion | Si |
| `/clear` | Limpiar contexto | Si |
| `/export` | Exportar datos | Si |

#### Comandos Nuevos para Oposiciones

```python
# NUEVOS comandos especificos
@bot.message_handler(commands=['review'])
def cmd_review(message):
    """Iniciar sesion de repaso de flashcards"""
    # ...

@bot.message_handler(commands=['test'])
def cmd_test(message):
    """Generar test rapido"""
    # ...

@bot.message_handler(commands=['progress'])
def cmd_progress(message):
    """Ver progreso de estudio"""
    # ...

@bot.message_handler(commands=['deck'])
def cmd_deck(message):
    """Gestionar decks de flashcards"""
    # ...

@bot.message_handler(commands=['weak'])
def cmd_weak_areas(message):
    """Ver areas debiles detectadas"""
    # ...
```

---

### 5. Configuracion

**Path Original:** `/opt/openclaw-memory/config.py`
**Reutilizacion:** 50% como template
**Destino:** `00-FOUNDATION/config.py`

#### Configuracion Actual

```python
# OPENCLAW-city config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # APIs
    MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
    MINIMAX_GROUP_ID = os.getenv("MINIMAX_GROUP_ID")
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

    # Database
    DB_PATH = os.getenv("DB_PATH", "/data/openclaw/memory.db")

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
```

#### Configuracion Adaptada

```python
# Oposiciones config.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Base path
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "02-DATA" / "databases"

    # APIs (heredado)
    MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
    MINIMAX_GROUP_ID = os.getenv("MINIMAX_GROUP_ID")
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

    # Database paths (nuevo)
    TEMARIO_DB = str(DATA_DIR / "temario.db")
    OPOSICIONES_DB = str(DATA_DIR / "oposiciones.db")

    # Telegram (heredado)
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # Nuevos settings
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
    EMBEDDING_DIM = 1024  # Mistral fijo
    SM2_EASE_FACTOR = 2.5

    # Logging (heredado)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = str(BASE_DIR / "logs" / "oposiciones.log")
```

---

## Codigo OPENCLAW-system (GitHub)

### Arquitectura de Agentes

**Reutilizacion:** Patrones y conceptos (no codigo directo)

#### Concilio Tri-Agente

| Componente | Implementar? | Ubicacion Destino |
|------------|--------------|-------------------|
| Director | Si | `04-AGENTS/concilio/director/` |
| Ejecutor | Si | `04-AGENTS/concilio/ejecutor/` |
| Archivador | Si | `04-AGENTS/concilio/archivador/` |

#### Catedra (6 Catedraticos)

| Catedratico | Implementar? | Fase |
|-------------|--------------|------|
| CKO | Si | MVP |
| CEngO | Si | MVP |
| COO | Si | Fase 2 |
| CHO | Fase 2 | Fase 2 |
| CSRO | Si | MVP |
| CCO | Fase 2 | Fase 2 |

#### Especialistas (9 Agentes)

| Especialista | MVP? | Funcion en Oposiciones |
|--------------|------|------------------------|
| librarian | Si | Indexacion temario |
| builder | Si | Generacion flashcards/tests |
| analyst | Si | Deteccion areas debiles |
| validator | Si | Validacion contenido |
| curator | Fase 2 | Curacion calidad |
| mentor | Fase 2 | Feedback educativo |
| architect | Fase 2 | Optimizacion rutas |
| guardian | MVP | Seguridad |
| scout | Fase 3 | Investigacion |

---

## Codigo JartOS (Local)

### Patrones a Reutilizar

**Path:** `/Volumes/-Documents/ARCHIVOS MAC MINI/JartOS`

#### CONVENTIONS.md v7.0

**Path:** `JartOS/00-FOUNDATION/CONVENTIONS.md`
**Reutilizacion:** Copiar y adaptar
**Destino:** `00-FOUNDATION/CONVENTIONS.md`

```markdown
# Convenciones de Codigo - v7.0 (Adaptado)

## Estructura de Archivos
- 15 Tiers: 00-FOUNDATION a 14-ARCHIVE
- Nomenclatura: {tier}-{componente}-{modulo}

## Sistema de Puertos
- Formato: 1XXYY (Tier XX, Servicio YY)
- Ejemplo: 10301 = Tier 03, Servicio 01

## Naming Conventions
- Archivos: snake_case
- Clases: PascalCase
- Funciones: snake_case
- Constantes: UPPER_SNAKE_CASE

## Documentacion
- Todo archivo debe tener header con:
  - Descripcion
  - Autor
  - Fecha
  - Version
```

#### Sistema de Puertos 1XXYY

**Reutilizacion:** 100%
**Destino:** Aplicar a todos los servicios

```
01-FOUNDATION:  101xx
02-DATA:        102xx
03-SERVICES:    10301, 10302, 10303, 10304
04-AGENTS:      10401
05-ORCH:        10501
06-INTERFACE:   18000, 18001
07-INTEGRATION: 10701, 10702
08-AUTOMATION:  10801
09-ANALYTICS:   10901
10-SECURITY:    11001
11-TESTING:     11101
12-DOCS:        (sin puerto)
13-EXPERIMENTAL: 11301 (LiveKit)
14-ARCHIVE:     (sin puerto)
```

#### Estructura de Agentes

**Path:** `JartOS/project/normas/agents/`
**Reutilizacion:** Patrones de documentacion

Los 14 agentes documentados sirven como template para documentar los 18 agentes de OPENCLAW (3 Concilio + 6 Catedra + 9 Especialistas).

---

## Tabla de Reutilizacion

### Resumen Completo

| Archivo Original | Path Real | Destino | % Reutilizar | Accion |
|------------------|-----------|---------|--------------|--------|
| `rag_store.py` | `/opt/openclaw-memory/rag_store.py` | `03-SERVICES/temario-service/rag_store.py` | 80% | Copiar + Adaptar |
| `memory_store.py` | `/opt/openclaw-memory/memory_store.py` | `03-SERVICES/memory-service/memory_store.py` | 70% | Copiar + Adaptar |
| `security_pipeline.py` | `/opt/openclaw-memory/security_pipeline.py` | `10-SECURITY/validation/security_pipeline.py` | 90% | Copiar directo |
| `ramiro_bot.py` | `/opt/openclaw-memory/ramiro_bot.py` | `06-INTERFACE/telegram/oposiciones_bot.py` | 60% | Usar como base |
| `config.py` | `/opt/openclaw-memory/config.py` | `00-FOUNDATION/config.py` | 50% | Adaptar template |
| `CONVENTIONS.md` | `JartOS/00-FOUNDATION/CONVENTIONS.md` | `00-FOUNDATION/CONVENTIONS.md` | 80% | Copiar + Adaptar |

### Funciones Especificas a Copiar

#### De rag_store.py

```python
# COPIAR DIRECTO
def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
    """Calcula similitud coseno entre dos vectores"""
    np_a = np.array(a)
    np_b = np.array(b)
    return np.dot(np_a, np_b) / (np.linalg.norm(np_a) * np.linalg.norm(np_b))

def search(self, query_embedding: List[float], k: int = 5,
           threshold: float = 0.7) -> List[dict]:
    """Busqueda semantica por similitud coseno"""
    # ... implementacion completa copiar
```

#### De memory_store.py

```python
# COPIAR DIRECTO
def _serialize(self, value: dict) -> str:
    """Serializa diccionario a JSON"""
    return json.dumps(value, ensure_ascii=False, default=str)

def _deserialize(self, data: str) -> dict:
    """Deserializa JSON a diccionario"""
    return json.loads(data)
```

#### De security_pipeline.py

```python
# COPIAR DIRECTO
def sanitize_text(self, text: str) -> str:
    """Limpia texto de caracteres peligrosos"""
    # Remover SQL injection patterns
    text = re.sub(r"[';\"\\]", "", text)
    # Remover HTML/JS
    text = re.sub(r"<[^>]*>", "", text)
    # Limitar longitud
    return text[:1000]

def validate_file_upload(self, file) -> Tuple[bool, str]:
    """Valida archivo subido"""
    if file.size > self.max_file_size:
        return False, "Archivo demasiado grande"
    if file.extension not in self.allowed_extensions:
        return False, "Extension no permitida"
    return True, "OK"
```

---

## Plan de Migracion

### Fase 1: Copia Base (Semana 1)

```bash
# 1. Crear estructura de carpetas
mkdir -p 03-SERVICES/{temario-service,memory-service}
mkdir -p 06-INTERFACE/telegram
mkdir -p 10-SECURITY/validation
mkdir -p 00-FOUNDATION

# 2. Copiar archivos de OPENCLAW-city
# (Desde VPS o backup local)
cp /opt/openclaw-memory/rag_store.py 03-SERVICES/temario-service/
cp /opt/openclaw-memory/memory_store.py 03-SERVICES/memory-service/
cp /opt/openclaw-memory/security_pipeline.py 10-SECURITY/validation/
cp /opt/openclaw-memory/ramiro_bot.py 06-INTERFACE/telegram/base_bot.py
cp /opt/openclaw-memory/config.py 00-FOUNDATION/config_template.py

# 3. Copiar CONVENTIONS de JartOS
cp "/Volumes/-Documents/ARCHIVOS MAC MINI/JartOS/00-FOUNDATION/CONVENTIONS.md" \
   00-FOUNDATION/CONVENTIONS.md
```

### Fase 2: Adaptaciones (Semana 2)

1. **rag_store.py** -> Anadir metodos `search_by_tema()`, `get_random_chunks()`
2. **memory_store.py** -> Cambiar de 2 scopes a 4 tipos (AGENT, UNIT, DOMAIN, GLOBAL)
3. **ramiro_bot.py** -> Anadir comandos `/review`, `/test`, `/progress`, `/deck`, `/weak`
4. **config.py** -> Adaptar paths y anadir settings de oposiciones

### Fase 3: Tests (Semana 3)

1. Crear tests unitarios para cada modulo adaptado
2. Verificar compatibilidad con datos existentes
3. Integrar con CI/CD

### Checklist de Migracion

- [ ] Copiar `rag_store.py` a `03-SERVICES/temario-service/`
- [ ] Adaptar `rag_store.py` con metodos de tema
- [ ] Copiar `memory_store.py` a `03-SERVICES/memory-service/`
- [ ] Adaptar `memory_store.py` a 4 tipos de memoria
- [ ] Copiar `security_pipeline.py` a `10-SECURITY/validation/`
- [ ] Copiar `ramiro_bot.py` como base
- [ ] Anadir comandos nuevos al bot
- [ ] Copiar `config.py` y adaptar
- [ ] Copiar `CONVENTIONS.md`
- [ ] Crear tests unitarios
- [ ] Verificar integracion

---

**Fin del documento de Codigo Existente (v1.0.0)**
