# Arquitectura del Sistema

**Última actualización:** 2026-03-16
**Versión:** 1.0.0 (Integrado con JartOS + OPENCLAW)

---

## Índice

1. [Filosofía de Arquitectura](#filosofía-de-arquitectura)
2. [Diagrama de Arquitectura Integrada](#2-diagrama-de-arquitectura-integrada)
3. [Sistema de 15 Tiers (JartOS)](#3-sistema-de-15-tiers-jartos)
4. [Sistema de Puertos 1XXYY](#4-sistema-de-puertos-1xxyy)
5. [Arquitectura 4 Niveles (OPENCLAW)](#5-arquitectura-4-niveles-openclaw)
6. [Concilio Tri-Agente](#6-concilio-tri-agente)
7. [Sistema de Memoria 4 Tipos](#7-sistema-de-memoria-4-tipos)
8. [Extensibilidad de Dominios](#8-extensibilidad-de-dominios)
9. [Flujo de Datos](#9-flujo-de-datos)
10. [Integración con LiveKit](#10-integración-con-livekit)
11. [Decisiones de Diseño (ADRs)](#11-decisiones-de-diseno-adrs)

---

## Filosofía de Arquitectura

### Principios Fundamentales

1. **Dominio-Agnostic** - El core no está atado a un caso de uso específico
2. **Modular y Extensible** - Añadir dominios sin modificar el core
3. **Coordinación Automática** - Agentes que trabajan juntos
4. **Contexto Persistente** - Memoria jerárquica entre sesiones
5. **Escalabilidad Horizontal** - Crecer añadiendo, no cambiando

### Arquitectura en Capas

```
┌─────────────────────────────────────────────────────────┐
│           CAPA DE PRESENTACIÓN (Extensible)              │
│  Web Dashboard | CLI | Telegram | Voz (opcional)       │
└─────────────────────────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────┐
│           CAPA DE SERVICIOS (Extensible)                 │
│  Dominio A | Dominio B | Dominio C | Dominio N          │
└─────────────────────────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────┐
│           CAPA DE AGENTES (Invariante)                   │
│  Concilio | Catedra | Especialistas | Workers            │
└─────────────────────────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────┐
│           CAPA DE MEMORIA (Invariante)                   │
│  4 Tipos: Agente | Unidad | Dominio | Global            │
└─────────────────────────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────┐
│           CAPA DE INFRAESTRUCTURA (Invariante)            │
│  SQLite | APIs IA | File System | Cache                  │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Diagrama de Arquitectura Integrada

### Vista General - Fusión de 3 Sistemas

```
+============================================================================+
|                    15 TIERS (JartOS) - Estructura de Carpetas               |
|  00-FOUNDATION | 01-INFRA | 02-DATA | ... | 14-ARCHIVE                     |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                    4 NIVELES JERARQUICOS (OPENCLAW-system)                  |
|  +------------------------------------------------------------------------+ |
|  | NIVEL 1: CONCILIO                                                      | |
|  |   Director <---> Ejecutor <---> Archivador                            | |
|  +------------------------------------------------------------------------+ |
|                          |                                                 |
|                          v                                                 |
|  +------------------------------------------------------------------------+ |
|  | NIVEL 2: CATEDRA (6 Catedráticos)                                      | |
|  |   CKO | CEngO | COO | CHO | CSRO | CCO                                | |
|  +------------------------------------------------------------------------+ |
|                          |                                                 |
|                          v                                                 |
|  +------------------------------------------------------------------------+ |
|  | NIVEL 3: ESPECIALISTAS (9 agentes con namespaces)                      | |
|  |   analyst.* | architect.* | builder.* | curator.* | guardian.*        | |
|  |   librarian.* | mentor.* | scout.* | validator.*                      | |
|  +------------------------------------------------------------------------+ |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                    COMPONENTES OPENCLAW-city (Producción)                   |
|  +---------------------------+  +---------------------------+              |
|  | RAG Store                 |  | Memory Store              |              |
|  | /opt/openclaw-memory/     |  | /opt/openclaw-memory/     |              |
|  | rag_store.py              |  | memory_store.py           |              |
|  +---------------------------+  +---------------------------+              |
|  +---------------------------+  +---------------------------+              |
|  | Security Pipeline         |  | Ramiro Bot                |              |
|  | /opt/openclaw-memory/     |  | /opt/openclaw-memory/     |              |
|  | security_pipeline.py      |  | ramiro_bot.py             |              |
|  +---------------------------+  +---------------------------+              |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                    CAPA DE PRESENTACIÓN (Extensible)                       |
|  +-------------------------+  +-------------------------+  +--------------+ |
|  |    Web Dashboard        |  |    CLI Tools            |  | Telegram Bot | |
|  |    Puerto: 18000        |  |    (typer + rich)       |  | (basado en   | |
|  |    (1XXYY: 18=UI, 00=1) |  |                         |  |  Ramiro)     | |
|  +-------------------------+  +-------------------------+  +--------------+ |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                    CAPA DE SERVICIOS (Extensible - Puertos 1XXYY)           |
|  +-------------+  +-------------+  +-------------+  +-------------+        |
|  |  Dominio A  |  |  Dominio B  |  |  Dominio C  |  |  Dominio N  |        |
|  |  Service    |  |  Service    |  |  Service    |  |  Service    |        |
|  |  :10301     |  |  :10302     |  |  :10303     |  |  :1030N     |        |
|  +-------------+  +-------------+  +-------------+  +-------------+        |
|  |  Temario    |  |  Flashcards |  |   Tests     |  |     AI      |        |
|  |  (Actual)   |  |  (Actual)   |  |  (Actual)   |  |  (Actual)   |        |
|  +-------------+  +-------------+  +-------------+  +-------------+        |
|  |  DevOps     |  |  Personal   |  |  Salud      |  |     ...     |        |
|  |  (Futuro)   |  |  (Futuro)   |  |  (Futuro)   |  |             |        |
|  +-------------+  +-------------+  +-------------+  +-------------+        |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                    CAPA DE DATOS (Extensible)                               |
|  +---------------------------+  +-----------------------------+             |
|  |   dominio_a.db            |  |   dominio_b.db              |             |
|  |   (heredado RAG Store)    |  |   (heredado Memory Store)   |             |
|  +---------------------------+  +-----------------------------+             |
|  +---------------------------+  +-----------------------------+             |
|  |   dominio_c.db            |  |   dominio_n.db              |             |
|  +---------------------------+  +-----------------------------+             |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                    CAPA DE AGENTES (Invariante)                              |
|  +------------------+  +------------------+  +------------------+           |
|  |   Concilio       |  |   Catedra        |  |  Especialistas   |           |
|  |   (3 agentes)    |  |   (6 roles)      |  |  (9 agentes)     |           |
|  +------------------+  +------------------+  +------------------+           |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                    CAPA DE MEMORIA (Invariante)                              |
|  +---------------------------+  +-----------------------------+             |
|  |   4 Tipos de Memoria      |  |   SQLite (Persistencia)     |             |
|  |   Agente | Unidad | Domain |   |   - agent_memory           |             |
|  |   Global                   |   |   - unit_memory             |             |
|  +---------------------------+  |   - domain_memory            |             |
|  |                           |   |   - global_memory           |             |
|  +---------------------------+  +-----------------------------+             |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                    CAPA DE EXTERNAL SERVICES (Invariante)                   |
|  +------------------+  +------------------+  +------------------+           |
|  |   Mistral API    |  |   MiniMax M2.5   |  |  LiveKit Server  |           |
|  |   (embeddings)   |  |   (LLM principal)|  |  (voz, opcional) |           |
|  |   1024 dims      |  |   32K context    |  |  WebRTC          |           |
|  +------------------+  +------------------+  +------------------+           |
+============================================================================+
```

---

## 3. Sistema de 15 Tiers (JartOS)

**Origen:** JartOS - Sistema de carpetas jerárquico

### Estructura de Tiers

```
jartos/
├── 00-FOUNDATION/         # Configuración base
│   ├── CONVENTIONS.md     # Estándares v7.0
│   ├── .env.example
│   └── config.yaml
│
├── 01-INFRA/              # Infraestructura
│   ├── docker/
│   ├── docker-compose.yml
│   └── Makefile
│
├── 02-DATA/               # Datos y persistencia (Extensible)
│   ├── databases/
│   │   ├── dominio_a.db
│   │   ├── dominio_b.db
│   │   └── ...
│   ├── embeddings/
│   └── exports/
│
├── 03-SERVICES/           # Microservicios (Extensible)
│   ├── dominio-a-service/  # Puerto 10301
│   ├── dominio-b-service/  # Puerto 10302
│   ├── dominio-c-service/  # Puerto 10303
│   └── ...
│
├── 04-AGENTS/             # Agentes de IA (Invariante)
│   ├── concilio/
│   │   ├── director/
│   │   ├── ejecutor/
│   │   └── archivador/
│   ├── catedra/
│   │   ├── cko/
│   │   ├── cengo/
│   │   └── ...
│   └── specialists/
│       ├── analyst/
│       ├── librarian/
│       └── ...
│
├── 05-ORCHESTRATION/      # Orquestadores (Invariante)
│   ├── workflows/
│   └── schedulers/
│
├── 06-INTERFACE/          # Interfaces usuario (Extensible)
│   ├── web/               # Puerto 18000
│   ├── cli/
│   └── telegram/
│
├── 07-INTEGRATION/        # APIs externas (Invariante)
│   ├── minimax/
│   ├── mistral/
│   └── livekit/
│
├── 08-AUTOMATION/         # Scripts (Extensible)
│   ├── ingestion/
│   └── maintenance/
│
├── 09-ANALYTICS/          # Métricas (Extensible)
│   ├── dashboards/
│   └── reports/
│
├── 10-SECURITY/           # Seguridad (Invariante)
│   ├── auth/
│   └── validation/
│
├── 11-TESTING/            # Tests (Invariante)
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── 12-DOCS/               # Documentación (Invariante)
│   ├── api/
│   └── guides/
│
├── 13-EXPERIMENTAL/       # Prototipos (Extensible)
│   └── voice-agent/
│
└── 14-ARCHIVE/            # Archivo (Invariante)
    └── deprecated/
```

### Convención de Nombres

```
{tier}-{componente}-{modulo}

Ejemplo:
03-services-dominio-a
04-agents-concilio-director
06-interface-web-dashboard
```

### Tiers Invariantes vs Extensibles

| Tier | Tipo | Descripción |
|------|------|-------------|
| 00-FOUNDATION | Invariante | Configuración base del sistema |
| 01-INFRA | Invariante | Infraestructura común |
| 02-DATA | Extensible | Bases de datos por dominio |
| 03-SERVICES | Extensible | Servicios por dominio |
| 04-AGENTS | Invariante | Sistema de agentes |
| 05-ORCHESTRATION | Invariante | Orquestación de tareas |
| 06-INTERFACE | Extensible | Interfaces por dominio |
| 07-INTEGRATION | Invariante | Integraciones comunes |
| 08-AUTOMATION | Extensible | Automatizaciones por dominio |
| 09-ANALYTICS | Extensible | Analíticas por dominio |
| 10-SECURITY | Invariante | Seguridad común |
| 11-TESTING | Invariante | Testing común |
| 12-DOCS | Invariante | Documentación común |
| 13-EXPERIMENTAL | Extensible | Prototipos por dominio |
| 14-ARCHIVE | Invariante | Archivo histórico |

---

## 4. Sistema de Puertos 1XXYY

**Origen:** JartOS - Sistema de asignación de puertos

### Fórmula

```
Puerto = 1XXYY

Donde:
  XX = Número de Tier (01-14)
  YY = Número de servicio dentro del tier (01-99)
```

### Puertos Asignados (Actuales)

| Tier | Servicio | Puerto | Descripción |
|------|----------|--------|-------------|
| 01 | INFRA-base | 10101 | Configuración base |
| 02 | DATA-oposiciones | 10201 | Base de datos oposiciones |
| 02 | DATA-desarrollo | 10202 | Base de datos desarrollo |
| 03 | SERVICES-temario | 10301 | Servicio de temario |
| 03 | SERVICES-flashcards | 10302 | Servicio de flashcards |
| 03 | SERVICES-tests | 10303 | Servicio de tests |
| 03 | SERVICES-ai | 10304 | Servicio de IA |
| 04 | AGENTS-gateway | 10401 | Gateway de agentes |
| 05 | ORCH-scheduler | 10501 | Scheduler de tareas |
| 06 | INTERFACE-web | 18000 | Dashboard web |
| 06 | INTERFACE-api | 18001 | API REST |
| 07 | INTEGRATION-minimax | 10701 | Proxy MiniMax |
| 07 | INTEGRATION-mistral | 10702 | Proxy Mistral |
| 13 | EXPERIMENTAL-livekit | 11301 | LiveKit server |

### Configuración Docker

```yaml
# docker-compose.yml
services:
  temario-service:
    ports:
      - "10301:10301"

  flashcards-service:
    ports:
      - "10302:10302"

  web-dashboard:
    ports:
      - "18000:18000"
```

---

## 5. Arquitectura 4 Niveles (OPENCLAW)

**Origen:** OPENCLAW-system

### Diagrama de Jerarquía

```
+============================================================================+
|                              NIVEL 1: CONCILIO                              |
|                         (Toma de decisiones estratégicas)                   |
|  +---------------------------+  +---------------------------+              |
|  |       DIRECTOR            |  |       EJECUTOR            |              |
|  |  - Define objetivos       |  |  - Implementa tareas      |              |
|  |  - Asigna prioridades     |  |  - Genera código          |              |
|  |  - Coordina catedráticos  |  |  - Ejecuta pruebas        |              |
|  +---------------------------+  +---------------------------+              |
|                                  +---------------------------+              |
|                                  |      ARCHIVADOR           |              |
|                                  |  - Mantiene contexto      |              |
|                                  |  - Indexa conocimiento    |              |
|                                  |  - Recupera historial     |              |
|                                  +---------------------------+              |
+============================================================================+
                                       |
                                       | Delega a
                                       v
+============================================================================+
|                             NIVEL 2: CATEDRA                                |
|                      (Gestión por dominios funcionales)                     |
|  +---------+  +---------+  +---------+  +---------+  +---------+  +------+ |
|  |   CKO   |  |  CEngO  |  |   COO   |  |   CHO   |  |  CSRO   |  | CCO  | |
|  |Knowledge|  |Engineer |  |Operation|  |  Human  |  | Security|  |Comply| |
|  +---------+  +---------+  +---------+  +---------+  +---------+  +------+ |
+============================================================================+
                                       |
                                       | Supervisa
                                       v
+============================================================================+
|                           NIVEL 3: ESPECIALISTAS                            |
|                         (Ejecución especializada)                           |
|  +---------+  +---------+  +---------+  +---------+  +---------+          |
|  | analyst |  |architect|  | builder |  | curator |  | guardian|          |
|  +---------+  +---------+  +---------+  +---------+  +---------+          |
|  +---------+  +---------+  +---------+  +---------+                        |
|  |librarian|  | mentor  |  |  scout  |  |validator|                        |
|  +---------+  +---------+  +---------+  +---------+                        |
+============================================================================+
                                       |
                                       | Usa
                                       v
+============================================================================+
|                            NIVEL 4: WORKERS                                 |
|                        (Infraestructura y herramientas)                     |
|  +-----------------+  +-----------------+  +-----------------+             |
|  |   RAG Store     |  |  Memory Store   |  | Security Pipeline|             |
|  +-----------------+  +-----------------+  +-----------------+             |
|  +-----------------+  +-----------------+                                  |
|  |   API Clients   |  |   File System   |                                  |
|  +-----------------+  +-----------------+                                  |
+============================================================================+
```

---

## 6. Concilio Tri-Agente

**Origen:** OPENCLAW-system

### Roles del Concilio

```
+-------------------+     +-------------------+     +-------------------+
|     DIRECTOR      |     |     EJECUTOR      |     |    ARCHIVADOR     |
+-------------------+     +-------------------+     +-------------------+
|                   |     |                   |     |                   |
| PLANIFICA         |     | IMPLEMENTA        |     | MEMORIZA          |
| - Objetivos       |     | - Codigo          |     | - Contexto        |
| - Prioridades     |     | - Tests           |     | - Historial       |
| - Recursos        |     | - Documentos      |     | - Indices         |
|                   |     |                   |     |                   |
| OUTPUT:           |     | OUTPUT:           |     | OUTPUT:           |
| Plan de accion    |     | Entregables       |     | Base de           |
|                   |     |                   |     | conocimiento      |
+-------------------+     +-------------------+     +-------------------+
        |                         |                         |
        +-----------+-------------+-----------+-------------+
                    |                         |
                    v                         v
           +----------------+       +----------------+
           |  Comunicacion  |<----->|   Memoria      |
           |  entre agentes |       |   Compartida   |
           +----------------+       +----------------+
```

### Protocolo de Comunicación

```python
class ConcilioMessage:
    """Mensaje entre agentes del Concilio"""
    from_agent: str      # "director" | "ejecutor" | "archivador"
    to_agent: str        # "director" | "ejecutor" | "archivador" | "all"
    message_type: str    # "task" | "query" | "result" | "context"
    priority: int        # 1-5 (1=urgente)
    payload: dict        # Datos del mensaje
    timestamp: datetime  # Cuando se envio
```

### Aplicación a Cualquier Dominio

El Concilio es **dominio-agnóstico**:

| Concilio | Función (Genérica) | Ejemplo: Oposiciones | Ejemplo: Desarrollo |
|----------|-------------------|---------------------|---------------------|
| **Director** | Planifica objetivos | Planifica sesiones de estudio | Planifica sprints |
| **Ejecutor** | Implementa tareas | Genera flashcards, tests | Genera código, tests |
| **Archivador** | Mantiene contexto | Historial de progreso | Historial de commits |

---

## 7. Sistema de Memoria 4 Tipos

**Origen:** OPENCLAW-system

### Diagrama de Alcance

```
+============================================================================+
|                         MEMORIA GLOBAL                                      |
|              (Conocimiento transversal del sistema)                         |
|  - Configuración del sistema                                               |
|  - Normativas y estándares                                                 |
|  - Patrones generales                                                      |
|  - Configuración de APIs                                                    |
+============================================================================+
            |                                  |
            | Hereda                           | Hereda
            v                                  v
+===========================+    +===========================+
|     MEMORIA DOMINIO A     |    |     MEMORIA DOMINIO B     |
|      (Oposiciones)        |    |      (Desarrollo)        |
| - Tema 1: Derecho Const.  |    | - Proyecto X: Specs      |
| - Tema 2: Derecho Admin.  |    | - Proyecto Y: API       |
| - Conceptos por tema      |    | - Documentación técnica  |
+===========================+    +===========================+
            |                                  |
            | Hereda                           | Hereda
            v                                  v
+===========================+    +===========================+
|     MEMORIA UNIDAD A      |    |     MEMORIA UNIDAD B      |
|   (Equipo Flashcards)     |    |    (Equipo Testing)       |
| - Decks activos           |    | - Suite de tests         |
| - Progreso del deck       |    | - Resultados             |
| - Configuración SM-2      |    | - Cobertura               |
+===========================+    +===========================+
            |                                  |
            | Hereda                           | Hereda
            v                                  v
+===========================+    +===========================+
|     MEMORIA AGENTE A      |    |     MEMORIA AGENTE B      |
|     (librarian)           |    |      (validator)          |
| - Contexto individual     |    | - Contexto individual     |
| - Tareas asignadas        |    | - Tests en curso         |
| - Historial personal      |    | - Historial personal     |
+===========================+    +===========================+
```

### Implementación

```python
class MemoryType(Enum):
    AGENT = "agent"       # Contexto individual
    UNIT = "unit"         # Compartido en equipo
    DOMAIN = "domain"     # Conocimiento temático
    GLOBAL = "global"     # Sistema completo

class MemoryStore:
    """Heredado de /opt/openclaw-memory/memory_store.py"""

    def save(self, key: str, value: dict, memory_type: MemoryType):
        """Guarda en el nivel de memoria apropiado"""

    def get(self, key: str, memory_type: MemoryType) -> dict:
        """Recupera del nivel de memoria"""

    def search(self, query: str, scope: List[MemoryType]) -> List[dict]:
        """Busca en múltiples niveles"""
```

---

## 8. Extensibilidad de Dominios

### Añadir un Nuevo Dominio

Para añadir un nuevo dominio (ej. Gestión Personal):

```
1. Crear servicio específico
   └── 03-SERVICES/gestion-personal/ (Puerto 10305)

2. Crear base de datos
   └── 02-DATA/databases/gestion-personal.db

3. Definir memoria de dominio
   └── Memoria type: DOMAIN, scope: "gestion-personal"

4. Registrar en Concilio (opcional, si requiere coordinación)
   └── Director ya sabe coordinar

5. Añadir interfaz (opcional)
   └── 06-INTERFACE/web/gestion-personal/
```

### Ejemplo de Extensión

```python
# 03-SERVICES/gestion-personal/service.py
class GestionPersonalService:
    """Servicio de gestión personal"""

    def __init__(self, db_path: str):
        self.db = sqlite3.connect(db_path)
        self.memory = MemoryStore()

    def add_task(self, task: Task):
        """Añadir tarea"""
        # Guardar en DB
        # Guardar en memoria de dominio
        self.memory.save(
            key=f"task:{task.id}",
            value=task.dict(),
            memory_type=MemoryType.DOMAIN
        )

    def get_recommendations(self):
        """Obtener recomendaciones (via Concilio)"""
        # El Director puede coordinar esto
        pass
```

---

## 9. Flujo de Datos

### 9.1 Ingestión de Documento (con componentes reales)

```
+--------+    +--------+    +--------+    +--------+    +--------+
|  PDF   |--->| Parser |--->|Chunker |--->|Embedder|--->| Store  |
|  File  |    |        |    |        |    |        |    |   DB   |
+--------+    +--------+    +--------+    +--------+    +--------+
     |             |             |             |             |
     v             v             v             v             v
  [bytes]    [texto]      [chunks]     [embeddings]   [saved]
                  |                          |
                  +----> Mistral API <--------+
                        (1024 dims)
                        [HEREDADO de OPENCLAW-city]
```

### 9.2 Búsqueda Semántica (con RAG Store)

```
+--------+    +------------------+    +-----------------+    +--------+
| Query  |--->|    Embedder      |--->|   RAG Store     |--->|Results |
| (text) |    |    (Mistral)     |    | (/opt/.../      |    |        |
+--------+    +------------------+    |  rag_store.py)  |    +--------+
     |             |                 +-----------------+          |
     v             v                         |                    v
  [string]   [embedding]              [cosine sim]          [ranked]
                                            |
                                            v
                                    +----------------+
                                    | dominio_a.db  |
                                    | chunks table  |
                                    +----------------+
```

### 9.3 Flujo del Concilio para Cualquier Dominio

```
+----------------+    +----------------+    +----------------+
|   DIRECTOR     |--->|   EJECUTOR     |--->|  ARCHIVADOR    |
|                |    |                |    |                |
| "Generar test  |    | Usa MiniMax    |    | Guarda test    |
|  del Tema 3"   |    | M2.5 API       |    | en memoria     |
|  (Oposiciones) |    |                |    |                |
+----------------+    +----------------+    +----------------+
        |                     |                     |
        v                     v                     v
   [Plan]              [Preguntas]           [Contexto]
        |                     |                     |
        +---------------------+---------------------+
                              |
                              v
                      +----------------+
                      |   Test listo   |
                      |   para usuario |
                      +----------------+

+----------------+    +----------------+    +----------------+
|   DIRECTOR     |--->|   EJECUTOR     |--->|  ARCHIVADOR    |
|                |    |                |    |                |
| "Generar test  |    | Usa specs      |    | Guarda test    |
|  del API X"    |    | del proyecto   |    | en memoria     |
|  (Desarrollo)  |    |                |    |                |
+----------------+    +----------------+    +----------------+
```

---

## 10. Integración con LiveKit

**Origen:** OPENCLAW-city (activo en producción)

### Arquitectura Voice Agent

```
+============================================================================+
|                         LIVEKIT SERVER                                      |
|                         Puerto: 11301 (1XXYY)                               |
|  +---------------------------+  +---------------------------+              |
|  |   WebRTC Handler          |  |   Room Manager            |              |
|  +---------------------------+  +---------------------------+              |
+============================================================================+
                                       |
                                       | SIP/WebRTC
                                       v
+============================================================================+
|                       VOICE AGENT WORKER                                    |
|  +---------------------------+  +---------------------------+              |
|  |   Speech-to-Text          |  |   Text-to-Speech          |              |
|  |   (Whisper/Deepgram)      |  |   (ElevenLabs/MiniMax)    |              |
|  +---------------------------+  +---------------------------+              |
|  +------------------------------------------------------------------------+ |
|  |                         A2A Protocol                                   | |
|  |   Comunicación Agent-to-Agent para coordinación                        | |
|  +------------------------------------------------------------------------+ |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                       CONCILIO + CATEDRA                                    |
|   Procesamiento de preguntas de voz con el sistema de agentes               |
|   (Dominio-agnóstico: funciona para cualquier uso)                         |
+============================================================================+
```

### Uso en Diferentes Dominios

```
Usuario: "Dame un repaso oral del Tema 3"
    |
    v
+----------------+
| Telegram Bot   | (basado en Ramiro)
| /opt/.../      |
| ramiro_bot.py  |
+----------------+
    |
    v
+----------------+
| LiveKit Server |
| Inicia sesión  |
| de voz         |
+----------------+
    |
    v
+----------------+
| Voice Agent    |
| Hace preguntas |
| orales         |
+----------------+
    |
    v
+----------------+
| Concilio       |
| Evalúa         |
| respuestas     |
| (Oposiciones)  |
+----------------+


Usuario: "Dame un repaso oral de la API X"
    |
    v
+----------------+
| Telegram Bot   |
+----------------+
    |
    v
+----------------+
| LiveKit Server |
+----------------+
    |
    v
+----------------+
| Voice Agent    |
| Hace preguntas |
| de código      |
+----------------+
    |
    v
+----------------+
| Concilio       |
| Evalúa         |
| respuestas     |
| (Desarrollo)   |
+----------------+
```

---

## 11. Decisiones de Diseño (ADRs)

### ADR-001: Sistema de 15 Tiers

**Estado:** Aceptado

**Contexto:**
Necesitamos estructura de carpetas escalable y extensible.

**Decisión:**
Adoptar sistema de **15 Tiers de JartOS** con separación entre invariantes y extensibles.

**Justificación:**
- Probado en 39GB de datos
- Organización clara por función
- Compatible con sistema de puertos 1XXYY
- Tiers extensibles permiten añadir dominios sin tocar el core

---

### ADR-002: Sistema de Puertos 1XXYY

**Estado:** Aceptado

**Contexto:**
Necesitamos asignación consistente de puertos para múltiples dominios.

**Decisión:**
Usar **sistema 1XXYY** (Tier + Servicio).

**Justificación:**
- Predecible: 10301 = Tier 03, servicio 01
- Evita conflictos entre dominios
- Fácil de documentar y mantener
- Escala horizontalmente

---

### ADR-003: Concilio Tri-Agente

**Estado:** Aceptado

**Contexto:**
Necesitamos coordinación entre módulos y dominios.

**Decisión:**
Adoptar **Concilio de OPENCLAW-system** (Director + Ejecutor + Archivador).

**Justificación:**
- Separación clara de responsabilidades
- Probado en producción
- Facilita automatización
- **Dominio-agnóstico**: funciona para cualquier caso de uso

---

### ADR-004: Memoria 4 Tipos

**Estado:** Aceptado

**Contexto:**
Necesitamos sistema de memoria jerárquico para múltiples dominios.

**Decisión:**
Usar **4 tipos de memoria** (Agente, Unidad, Dominio, Global).

**Justificación:**
- Permite contexto específico por nivel
- Evita contaminación de contexto entre dominios
- Compatible con Memory Store existente
- Escala con nuevos dominios

---

### ADR-005: Arquitectura Dominio-Agnóstica

**Estado:** Aceptado

**Contexto:**
El sistema debe poder adaptarse a cualquier dominio sin cambios al core.

**Decisión:**
El **core del sistema (Concilio, Memoria, Infraestructura) es invariante**. Solo se extienden los servicios y datos por dominio.

**Justificación:**
- Máxima extensibilidad
- Mínimo mantenimiento del core
- Fácil añadir nuevos casos de uso
- Evita "technical debt" por hardcoding de dominio

---

### ADR-006: Reutilizar Código OPENCLAW-city

**Estado:** Aceptado

**Contexto:**
Hay código funcional en producción.

**Decisión:**
Reutilizar componentes de `/opt/openclaw-memory/`.

**Justificación:**
- Ya probados en producción
- RAG Store funcional
- Memory Store funcional
- Security Pipeline funcional
- Ramiro Bot como base

---

**Fin del documento de Arquitectura (v1.0.0 Integrado)**
