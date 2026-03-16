# Arquitectura del Sistema

**Ultima actualizacion:** 2026-03-16
**Version:** 1.0.0 (Integrado con JartOS + OPENCLAW)

---

## Indice

1. [Diagrama de Arquitectura Integrada](#1-diagrama-de-arquitectura-integrada)
2. [Sistema de 15 Tiers (JartOS)](#2-sistema-de-15-tiers-jartos)
3. [Sistema de Puertos 1XXYY](#3-sistema-de-puertos-1xxyy)
4. [Arquitectura 4 Niveles (OPENCLAW)](#4-arquitectura-4-niveles-openclaw)
5. [Concilio Tri-Agente](#5-concilio-tri-agente)
6. [Sistema de Memoria 4 Tipos](#6-sistema-de-memoria-4-tipos)
7. [Flujo de Datos](#7-flujo-de-datos)
8. [Integracion con LiveKit](#8-integracion-con-livekit)
9. [Decisiones de Diseno (ADRs)](#9-decisiones-de-diseno-adrs)

---

## 1. Diagrama de Arquitectura Integrada

### Vista General - Fusion de 3 Sistemas

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
|  | NIVEL 2: CATEDRA (6 Catedraticos)                                      | |
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
|                    COMPONENTES OPENCLAW-city (Produccion)                   |
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
|                    CAPA DE PRESENTACION                                     |
|  +-------------------------+  +-------------------------+  +--------------+ |
|  |    Web Dashboard        |  |    CLI Tools            |  | Telegram Bot | |
|  |    Puerto: 18000        |  |    (typer + rich)       |  | (basado en   | |
|  |    (1XXYY: 18=UI, 00=1) |  |                         |  |  Ramiro)     | |
|  +-------------------------+  +-------------------------+  +--------------+ |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                    CAPA DE SERVICIOS (Puertos 1XXYY)                        |
|  +-------------+  +-------------+  +-------------+  +-------------+        |
|  |  Temario    |  |  Flashcards |  |   Tests     |  |     AI      |        |
|  |  Service    |  |   Service   |  |  Service    |  |  Service    |        |
|  |  :10301     |  |  :10302     |  |  :10303     |  |  :10304     |        |
|  +-------------+  +-------------+  +-------------+  +-------------+        |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                    CAPA DE DATOS                                            |
|  +---------------------------+  +-----------------------------+             |
|  |   temario.db              |  |   oposiciones.db            |             |
|  |   (heredado RAG Store)    |  |   (heredado Memory Store)   |             |
|  +---------------------------+  +-----------------------------+             |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                    CAPA DE EXTERNAL SERVICES                                |
|  +------------------+  +------------------+  +------------------+           |
|  |   Mistral API    |  |   MiniMax M2.5   |  |  LiveKit Server  |           |
|  |   (embeddings)   |  |   (LLM principal)|  |  (voz, opcional) |           |
|  |   1024 dims      |  |   32K context    |  |  WebRTC          |           |
|  +------------------+  +------------------+  +------------------+           |
+============================================================================+
```

---

## 2. Sistema de 15 Tiers (JartOS)

**Origen:** JartOS - Sistema de carpetas jerarquico

### Estructura de Tiers

```
oposiciones-system/
├── 00-FOUNDATION/         # Configuracion base
│   ├── CONVENTIONS.md     # Estandares v7.0
│   ├── .env.example
│   └── config.yaml
│
├── 01-INFRA/              # Infraestructura
│   ├── docker/
│   ├── docker-compose.yml
│   └── Makefile
│
├── 02-DATA/               # Datos y persistencia
│   ├── databases/
│   │   ├── temario.db
│   │   └── oposiciones.db
│   ├── embeddings/
│   └── exports/
│
├── 03-SERVICES/           # Microservicios
│   ├── temario-service/   # Puerto 10301
│   ├── flashcards-service/# Puerto 10302
│   ├── tests-service/     # Puerto 10303
│   └── ai-service/        # Puerto 10304
│
├── 04-AGENTS/             # Agentes de IA
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
├── 05-ORCHESTRATION/      # Orquestadores
│   ├── workflows/
│   └── schedulers/
│
├── 06-INTERFACE/          # Interfaces usuario
│   ├── web/               # Puerto 18000
│   ├── cli/
│   └── telegram/
│
├── 07-INTEGRATION/        # APIs externas
│   ├── minimax/
│   ├── mistral/
│   └── livekit/
│
├── 08-AUTOMATION/         # Scripts
│   ├── ingestion/
│   └── maintenance/
│
├── 09-ANALYTICS/          # Metricas
│   ├── dashboards/
│   └── reports/
│
├── 10-SECURITY/           # Seguridad
│   ├── auth/
│   └── validation/
│
├── 11-TESTING/            # Tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── 12-DOCS/               # Documentacion
│   ├── api/
│   └── guides/
│
├── 13-EXPERIMENTAL/       # Prototipos
│   └── voice-agent/
│
└── 14-ARCHIVE/            # Archivo
    └── deprecated/
```

### Convencion de Nombres

```
{tier}-{componente}-{modulo}

Ejemplo:
03-services-temario
04-agents-concilio-director
06-interface-web-dashboard
```

---

## 3. Sistema de Puertos 1XXYY

**Origen:** JartOS - Sistema de asignacion de puertos

### Formula

```
Puerto = 1XXYY

Donde:
  XX = Numero de Tier (01-14)
  YY = Numero de servicio dentro del tier (01-99)
```

### Puertos Asignados

| Tier | Servicio | Puerto | Descripcion |
|------|----------|--------|-------------|
| 01 | INFRA-base | 10101 | Configuracion base |
| 02 | DATA-temario | 10201 | Base de datos temario |
| 02 | DATA-oposiciones | 10202 | Base de datos oposiciones |
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

### Configuracion Docker

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

## 4. Arquitectura 4 Niveles (OPENCLAW)

**Origen:** OPENCLAW-system

### Diagrama de Jerarquia

```
+============================================================================+
|                              NIVEL 1: CONCILIO                              |
|                         (Toma de decisiones estrategicas)                   |
|  +---------------------------+  +---------------------------+              |
|  |       DIRECTOR            |  |       EJECUTOR            |              |
|  |  - Define objetivos       |  |  - Implementa tareas      |              |
|  |  - Asigna prioridades     |  |  - Genera codigo          |              |
|  |  - Coordina catedraticos  |  |  - Ejecuta pruebas        |              |
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
|                      (Gestion por dominios funcionales)                     |
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
|                         (Ejecucion especializada)                           |
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

## 5. Concilio Tri-Agente

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

### Protocolo de Comunicacion

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

### Aplicacion a Oposiciones

| Concilio | Funcion en Oposiciones |
|----------|------------------------|
| **Director** | Planifica sesiones de estudio, define objetivos diarios |
| **Ejecutor** | Genera flashcards, crea tests, ejecuta ingestion |
| **Archivador** | Mantiene historial de progreso, recupera contexto |

---

## 6. Sistema de Memoria 4 Tipos

**Origen:** OPENCLAW-system

### Diagrama de Alcance

```
+============================================================================+
|                         MEMORIA GLOBAL                                      |
|              (Conocimiento transversal del sistema)                         |
|  - Normativas de oposiciones                                               |
|  - Estructura del temario                                                  |
|  - Configuracion del sistema                                               |
|  - Patrones de estudio generales                                           |
+============================================================================+
            |                                  |
            | Hereda                           | Hereda
            v                                  v
+===========================+    +===========================+
|     MEMORIA DOMINIO       |    |     MEMORIA DOMINIO       |
|      (Temario)            |    |      (Tests)              |
| - Tema 1: Derecho Const.  |    | - Estadisticas de tests   |
| - Tema 2: Derecho Admin.  |    | - Patrones de errores     |
| - Conceptos por tema      |    | - Preguntas frecuentes    |
+===========================+    +===========================+
            |                                  |
            | Hereda                           | Hereda
            v                                  v
+===========================+    +===========================+
|     MEMORIA UNIDAD        |    |     MEMORIA UNIDAD        |
|   (Equipo Flashcards)     |    |    (Equipo Analytics)     |
| - Decks activos           |    | - Metricas actuales       |
| - Progreso del deck       |    | - Predicciones            |
| - Configuracion SM-2      |    | - Recomendaciones         |
+===========================+    +===========================+
            |                                  |
            | Hereda                           | Hereda
            v                                  v
+===========================+    +===========================+
|     MEMORIA AGENTE        |    |     MEMORIA AGENTE        |
|     (librarian)           |    |      (analyst)            |
| - Contexto individual     |    | - Contexto individual     |
| - Tareas asignadas        |    | - Analisis en curso       |
| - Historial personal      |    | - Historial personal      |
+===========================+    +===========================+
```

### Implementacion

```python
class MemoryType(Enum):
    AGENT = "agent"       # Contexto individual
    UNIT = "unit"         # Compartido en equipo
    DOMAIN = "domain"     # Conocimiento tematico
    GLOBAL = "global"     # Sistema completo

class MemoryStore:
    """Heredado de /opt/openclaw-memory/memory_store.py"""

    def save(self, key: str, value: dict, memory_type: MemoryType):
        """Guarda en el nivel de memoria apropiado"""

    def get(self, key: str, memory_type: MemoryType) -> dict:
        """Recupera del nivel de memoria"""

    def search(self, query: str, scope: List[MemoryType]) -> List[dict]:
        """Busca en multiples niveles"""
```

---

## 7. Flujo de Datos

### 7.1 Ingestion de Documento (con componentes reales)

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

### 7.2 Busqueda Semantica (con RAG Store)

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
                                    | temario.db     |
                                    | chunks table   |
                                    +----------------+
```

### 7.3 Flujo del Concilio para Oposiciones

```
+----------------+    +----------------+    +----------------+
|   DIRECTOR     |--->|   EJECUTOR     |--->|  ARCHIVADOR    |
|                |    |                |    |                |
| "Generar test  |    | Usa MiniMax    |    | Guarda test    |
|  del Tema 3"   |    | M2.5 API       |    | en memoria     |
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
```

---

## 8. Integracion con LiveKit

**Origen:** OPENCLAW-city (activo en produccion)

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
|  |   Comunicacion Agent-to-Agent para coordinacion                        | |
|  +------------------------------------------------------------------------+ |
+============================================================================+
                                       |
                                       v
+============================================================================+
|                       CONCILIO + CATEDRA                                    |
|   Procesamiento de preguntas de voz con el sistema de agentes               |
+============================================================================+
```

### Uso en Oposiciones (Fase 3)

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
| Inicia sesion  |
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
| Evalua         |
| respuestas     |
+----------------+
```

---

## 9. Decisiones de Diseno (ADRs)

### ADR-001: Sistema de 15 Tiers

**Estado:** Aceptado

**Contexto:**
Necesitamos estructura de carpetas escalable.

**Decision:**
Adoptar sistema de **15 Tiers de JartOS**.

**Justificacion:**
- Probado en 39GB de datos
- Organizacion clara por funcion
- Compatible con sistema de puertos 1XXYY

---

### ADR-002: Sistema de Puertos 1XXYY

**Estado:** Aceptado

**Contexto:**
Necesitamos asignacion consistente de puertos.

**Decision:**
Usar **sistema 1XXYY** (Tier + Servicio).

**Justificacion:**
- Predecible: 10301 = Tier 03, servicio 01
- Evita conflictos
- Facil de documentar

---

### ADR-003: Concilio Tri-Agente

**Estado:** Aceptado

**Contexto:**
Necesitamos coordinacion entre modulos.

**Decision:**
Adoptar **Concilio de OPENCLAW-system** (Director + Ejecutor + Archivador).

**Justificacion:**
- Separacion clara de responsabilidades
- Probado en produccion
- Facilita automatizacion

---

### ADR-004: Memoria 4 Tipos

**Estado:** Aceptado

**Contexto:**
Necesitamos sistema de memoria jerarquico.

**Decision:**
Usar **4 tipos de memoria** (Agente, Unidad, Dominio, Global).

**Justificacion:**
- Permite contexto especifico por nivel
- Evita contaminacion de contexto
- Compatible con Memory Store existente

---

### ADR-005: Reutilizar Codigo OPENCLAW-city

**Estado:** Aceptado

**Contexto:**
Hay codigo funcional en produccion.

**Decision:**
Reutilizar componentes de `/opt/openclaw-memory/`.

**Justificacion:**
- Ya probados en produccion
- RAG Store funcional
- Memory Store funcional
- Security Pipeline funcional
- Ramiro Bot como base

---

**Fin del documento de Arquitectura (v1.0.0 Integrado)**
