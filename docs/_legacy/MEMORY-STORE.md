# 🧠 Memory Store

**Sistema de Memoria Persistente con SQLite**

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Descripción General](#1-descripción-general)
2. [Schema de Base de Datos](#2-schema-de-base-de-datos)
3. [API Reference (Python)](#3-api-reference-python)
4. [Políticas de Retención](#4-políticas-de-retención)
5. [Backup y Restauración](#5-backup-y-restauración)

---

## 1. Descripción General

El **Memory Store** es el sistema de memoria persistente de OpenClaw, implementado con SQLite.

**Características:**
- ✅ Almacena conversaciones completas
- ✅ Gestiona perfiles de usuario
- ✅ Guarda memorias a largo plazo (con embeddings)
- ✅ Log de eventos de seguridad
- ✅ Registro de métricas de rendimiento

**Ubicación:** `/opt/openclaw-memory/memory_store.py`  
**Database:** `/var/lib/openclaw/memory.db`

---

## 2. Schema de Base de Datos

### 2.1 Tabla: conversations

Almacena todos los mensajes de conversaciones.

```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,           -- ej: "telegram:795606301"
    channel TEXT NOT NULL,            -- ej: "telegram"
    message_index INTEGER NOT NULL,   -- índice secuencial
    role TEXT NOT NULL,               -- "user", "assistant", "system"
    content TEXT NOT NULL,            -- contenido del mensaje
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    metadata JSON,                    -- metadata opcional
    UNIQUE(user_id, channel, message_index)
);

CREATE INDEX idx_conversations_user 
ON conversations(user_id, channel, message_index DESC);
```

**Campos:**

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `id` | INTEGER | ID único autoincremental | 1, 2, 3... |
| `user_id` | TEXT | ID del usuario | `telegram:795606301` |
| `channel` | TEXT | Canal de comunicación | `telegram`, `web` |
| `message_index` | INTEGER | Índice secuencial por conversación | 0, 1, 2... |
| `role` | TEXT | Rol del mensaje | `user`, `assistant`, `system` |
| `content` | TEXT | Contenido del mensaje | "Hola, ¿cómo estás?" |
| `timestamp` | DATETIME | Fecha/hora de creación | `2026-03-10 15:30:00` |
| `metadata` | JSON | Metadata adicional | `{"tokens": 150}` |

---

### 2.2 Tabla: user_profiles

Almacena perfiles de usuario.

```sql
CREATE TABLE user_profiles (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    username TEXT,
    channel TEXT,
    preferences JSON DEFAULT '{}',
    metadata JSON DEFAULT '{}',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Campos:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `user_id` | TEXT | ID único (PK) |
| `name` | TEXT | Nombre del usuario |
| `username` | TEXT | Username (Telegram, etc.) |
| `channel` | TEXT | Canal principal |
| `preferences` | JSON | Preferencias del usuario |
| `metadata` | JSON | Metadata adicional |
| `created_at` | DATETIME | Fecha de creación |
| `updated_at` | DATETIME | Última actualización |

---

### 2.3 Tabla: long_term_memory

Almacena memorias a largo plazo (hechos importantes) con embeddings.

```sql
CREATE TABLE long_term_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    category TEXT NOT NULL,           -- ej: "personal", "code", "facts"
    fact_type TEXT NOT NULL,          -- ej: "name", "preference"
    content TEXT NOT NULL,            -- contenido de la memoria
    embedding JSON,                   -- vector de embedding (1024 dims)
    confidence REAL DEFAULT 1.0,      -- confianza (0-1)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 1
);

CREATE INDEX idx_memory_user 
ON long_term_memory(user_id, category);
```

**Campos:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | ID único |
| `user_id` | TEXT | ID del usuario |
| `category` | TEXT | Categoría de la memoria |
| `fact_type` | TEXT | Tipo de hecho |
| `content` | TEXT | Contenido de la memoria |
| `embedding` | JSON | Vector de embedding (lista de floats) |
| `confidence` | REAL | Confianza en la memoria |
| `created_at` | DATETIME | Fecha de creación |
| `last_accessed` | DATETIME | Último acceso |
| `access_count` | INTEGER | Número de accesos |

---

### 2.4 Tabla: security_logs

Almacena logs de eventos de seguridad.

```sql
CREATE TABLE security_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT NOT NULL,         -- ej: "UNAUTHORIZED_ACCESS"
    severity TEXT NOT NULL,           -- "info", "warn", "error"
    user_id TEXT,
    channel TEXT,
    details JSON,
    ip_address TEXT,
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at DATETIME,
    resolved_by TEXT
);

CREATE INDEX idx_security_type 
ON security_logs(event_type, severity, timestamp DESC);
```

**Campos:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | ID único |
| `timestamp` | DATETIME | Fecha/hora del evento |
| `event_type` | TEXT | Tipo de evento |
| `severity` | TEXT | Severidad |
| `user_id` | TEXT | ID del usuario (si aplica) |
| `channel` | TEXT | Canal (si aplica) |
| `details` | JSON | Detalles del evento |
| `ip_address` | TEXT | IP (si aplica) |
| `resolved` | BOOLEAN | ¿Resuelto? |
| `resolved_at` | DATETIME | Fecha de resolución |
| `resolved_by` | TEXT | Quién resolvió |

**Tipos de Eventos:**

| Event Type | Severidad | Descripción |
|------------|-----------|-------------|
| `UNAUTHORIZED_ACCESS` | warn | Intento de acceso no autorizado |
| `UNAUTHORIZED_MESSAGE` | warn | Mensaje de usuario no autorizado |
| `MISTRAL_ERROR` | error | Error de API de Mistral |
| `MISTRAL_API_ERROR` | error | Error HTTP de Mistral |
| `MISTRAL_TIMEOUT` | warn | Timeout de Mistral |
| `BOT_STARTED` | info | Bot iniciado |
| `BOT_RUNNING` | info | Bot en ejecución |
| `SECURITY_CHECK` | info/warn | Check de seguridad |

---

### 2.5 Tabla: metrics

Almacena métricas de rendimiento.

```sql
CREATE TABLE metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    metric_type TEXT NOT NULL,        -- ej: "api", "bot", "security"
    metric_name TEXT NOT NULL,        -- ej: "latency_ms", "tokens"
    value REAL NOT NULL,              -- valor de la métrica
    labels JSON DEFAULT '{}'          -- labels adicionales
);

CREATE INDEX idx_metrics_type 
ON metrics(metric_type, timestamp DESC);
```

**Campos:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | ID único |
| `timestamp` | DATETIME | Fecha/hora de la métrica |
| `metric_type` | TEXT | Tipo de métrica |
| `metric_name` | TEXT | Nombre de la métrica |
| `value` | REAL | Valor numérico |
| `labels` | JSON | Labels adicionales |

**Métricas Comunes:**

| metric_type | metric_name | Descripción |
|-------------|-------------|-------------|
| `api` | `latency_ms` | Latencia de API (ms) |
| `api` | `tokens` | Tokens usados |
| `bot` | `message_received` | Mensajes recibidos |
| `bot` | `message_sent` | Mensajes enviados |
| `bot` | `command_start` | Comando /start |
| `bot` | `command_help` | Comando /help |
| `security` | `score` | Security score (0-100) |
| `health` | `overall` | Health overall (0/1) |

---

## 3. API Reference (Python)

### Inicialización

```python
from memory_store import get_memory_store

# Obtener instancia singleton
memory = get_memory_store()

# Database path
print(memory.db_path)  # /var/lib/openclaw/memory.db
```

---

### Conversaciones

#### add_message

```python
memory.add_message(
    user_id="telegram:795606301",
    channel="telegram",
    role="user",           # "user", "assistant", "system"
    content="Hola, ¿cómo estás?",
    metadata={"tokens": 10}  # opcional
)
```

#### get_context

```python
# Obtener últimos N mensajes
context = memory.get_context(
    user_id="telegram:795606301",
    channel="telegram",
    limit=20
)

# Output:
# [
#   {"role": "user", "content": "...", "timestamp": "..."},
#   {"role": "assistant", "content": "...", "timestamp": "..."},
#   ...
# ]
```

#### clear_conversation

```python
# Limpiar conversación de un usuario
memory.clear_conversation(
    user_id="telegram:795606301",
    channel="telegram"
)
```

---

### Perfiles de Usuario

#### save_user_profile

```python
memory.save_user_profile(
    user_id="telegram:795606301",
    name="Rubén",
    username="ruben",
    channel="telegram",
    preferences={"language": "es"},
    metadata={"timezone": "Europe/Madrid"}
)
```

#### get_user_profile

```python
profile = memory.get_user_profile("telegram:795606301")

# Output:
# {
#   "user_id": "telegram:795606301",
#   "name": "Rubén",
#   "username": "ruben",
#   "channel": "telegram",
#   "preferences": {"language": "es"},
#   "metadata": {"timezone": "Europe/Madrid"},
#   "created_at": "...",
#   "updated_at": "..."
# }
```

---

### Memorias a Largo Plazo

#### add_memory

```python
memory.add_memory(
    user_id="telegram:795606301",
    category="personal",
    fact_type="name",
    content="Se llama Rubén",
    embedding=[0.1, 0.2, ...],  # opcional, vector de 1024 dims
    confidence=0.9
)
```

#### get_memories

```python
# Obtener memorias de un usuario
memories = memory.get_memories(
    user_id="telegram:795606301",
    category="personal",  # opcional
    limit=10
)

# Output:
# [
#   {
#     "id": 1,
#     "user_id": "telegram:795606301",
#     "category": "personal",
#     "fact_type": "name",
#     "content": "Se llama Rubén",
#     "confidence": 0.9,
#     "created_at": "...",
#     "access_count": 5
#   },
#   ...
# ]
```

#### search_memories

```python
# Búsqueda por texto (fallback si no hay embedding)
results = memory.search_memories(
    user_id="telegram:795606301",
    query="nombre del usuario",
    limit=5
)
```

---

### Security Logs

#### log_security_event

```python
memory.log_security_event(
    event_type="UNAUTHORIZED_ACCESS",
    severity="warn",
    details={
        "user": "unknown",
        "chat_id": "123456"
    },
    user_id="telegram:123456",
    channel="telegram"
)
```

#### get_security_logs

```python
# Obtener logs de seguridad
logs = memory.get_security_logs(
    limit=20,
    unresolved_only=True  # solo no resueltos
)

# Output:
# [
#   {
#     "id": 1,
#     "timestamp": "...",
#     "event_type": "UNAUTHORIZED_ACCESS",
#     "severity": "warn",
#     "details": {...},
#     "resolved": False
#   },
#   ...
# ]
```

#### resolve_security_event

```python
memory.resolve_security_event(
    event_id=1,
    resolved_by="admin"
)
```

---

### Métricas

#### record_metric

```python
memory.record_metric(
    metric_type="api",
    metric_name="latency_ms",
    value=150.5,
    labels={"model": "mistral-large-latest"}
)
```

#### get_metrics

```python
# Obtener métricas de las últimas N horas
metrics = memory.get_metrics(hours=24)

# Output:
# [
#   {
#     "id": 1,
#     "timestamp": "...",
#     "metric_type": "api",
#     "metric_name": "latency_ms",
#     "value": 150.5,
#     "labels": {"model": "mistral-large-latest"}
#   },
#   ...
# ]
```

---

### Utilidades

#### cleanup_old_data

```python
# Eliminar datos antiguos (>30 días)
memory.cleanup_old_data(days=30)

# Elimina:
# - Conversaciones antiguas
# - Métricas antiguas
# - Security logs resueltos antiguos
```

#### get_stats

```python
# Obtener estadísticas
stats = memory.get_stats()

# Output:
# {
#   "total_conversations": 1000,
#   "total_users": 5,
#   "total_memories": 50,
#   "total_security_events": 10,
#   "db_size_bytes": 131072
# }
```

---

## 4. Políticas de Retención

### Conversaciones

| Tipo | Retención | Justificación |
|------|-----------|---------------|
| Activas | Indefinida | Contexto de conversación |
| Inactivas (>90 días) | Limpiable | Ahorrar espacio |

### Métricas

| Tipo | Retención | Justificación |
|------|-----------|---------------|
| Recientes (<30 días) | Conservar | Análisis reciente |
| Antiguas (>30 días) | Limpiable | Ahorrar espacio |

### Security Logs

| Tipo | Retención | Justificación |
|------|-----------|---------------|
| No resueltos | Indefinida | Requieren atención |
| Resueltos (>90 días) | Limpiable | Histórico completado |

### Memorias a Largo Plazo

| Tipo | Retención | Justificación |
|------|-----------|---------------|
| Todas | Indefinida | Información importante |

---

## 5. Backup y Restauración

### Backup Manual

```bash
# Detener servicios
sudo systemctl stop openclaw openclaw-email openclaw-orchestrator

# Copiar database
cp /var/lib/openclaw/memory.db /root/backups/memory-backup-$(date +%Y%m%d).db

# Iniciar servicios
sudo systemctl start openclaw openclaw-email openclaw-orchestrator
```

### Backup Automático

El script `openclaw-backup` incluye la database:

```bash
# Ejecutar backup
sudo openclaw-backup

# Backups se guardan en:
# /root/backups/openclaw/openclaw-backup-YYYYMMDD-HHMMSS.tar.gz
```

### Restaurar Backup

```bash
# Detener servicios
sudo systemctl stop openclaw openclaw-email openclaw-orchestrator

# Restaurar database
tar -xzf /root/backups/openclaw/openclaw-backup-YYYYMMDD-HHMMSS.tar.gz -C /

# Iniciar servicios
sudo systemctl start openclaw openclaw-email openclaw-orchestrator
```

### Verificar Integridad

```bash
# Verificar database SQLite
sqlite3 /var/lib/openclaw/memory.db "PRAGMA integrity_check;"

# Debe devolver: ok
```

---

## 6. Consultas Útiles

```bash
# Conectar a database
sqlite3 /var/lib/openclaw/memory.db

# Contar conversaciones
SELECT COUNT(*) FROM conversations;

# Contar usuarios únicos
SELECT COUNT(DISTINCT user_id) FROM conversations;

# Ver últimos mensajes
SELECT user_id, role, content, timestamp 
FROM conversations 
ORDER BY timestamp DESC 
LIMIT 10;

# Ver perfiles de usuario
SELECT * FROM user_profiles;

# Ver memorias
SELECT user_id, category, content, confidence 
FROM long_term_memory 
ORDER BY created_at DESC 
LIMIT 10;

# Ver eventos de seguridad recientes
SELECT timestamp, event_type, severity, details 
FROM security_logs 
ORDER BY timestamp DESC 
LIMIT 20;

# Ver métricas de las últimas 24h
SELECT metric_type, metric_name, AVG(value) as avg_value, COUNT(*) as count
FROM metrics 
WHERE timestamp > datetime('now', '-24 hours')
GROUP BY metric_type, metric_name;

# Tamaño de la database
SELECT page_count * page_size as size_bytes 
FROM pragma_page_count(), pragma_page_size();
```

---

**Fin del documento del Memory Store**
