# Sistema de Agentes

**Ultima actualizacion:** 2025-03-16
**Version:** 1.0.0
**Origen:** OPENCLAW-system + JartOS

---

## Indice

1. [Visión General](#vision-general)
2. [Concilio Tri-Agente](#concilio-tri-agente)
3. [Catedra - 6 Catedraticos](#catedra---6-catedraticos)
4. [Especialistas - 9 Agentes](#especialistas---9-agentes)
5. [Adaptacion para Oposiciones](#adaptacion-para-oposiciones)
6. [Protocolo de Comunicacion](#protocolo-de-comunicacion)
7. [Namespaces](#namespaces)

---

## Vision General

### Jerarquia 4 Niveles

```
NIVEL 1: CONCILIO (Decision estrategica)
    |
    +-- Director: Planifica objetivos
    +-- Ejecutor: Implementa soluciones
    +-- Archivador: Mantiene memoria
    |
    v
NIVEL 2: CATEDRA (Gestion funcional)
    |
    +-- CKO: Conocimiento
    +-- CEngO: Ingenieria
    +-- COO: Operaciones
    +-- CHO: Experiencia usuario
    +-- CSRO: Seguridad
    +-- CCO: Cumplimiento
    |
    v
NIVEL 3: ESPECIALISTAS (Ejecucion)
    |
    +-- 9 especialistas con namespaces
    |
    v
NIVEL 4: WORKERS (Infraestructura)
    |
    +-- RAG Store, Memory Store, APIs
```

---

## Concilio Tri-Agente

**Origen:** OPENCLAW-system
**Proposito:** Coordinacion estrategica de alto nivel

### Director

| Atributo | Valor |
|----------|-------|
| **Rol** | Planificador estrategico |
| **Namespace** | `director.*` |
| **Prioridad** | Alta (toma decisiones) |

**Responsabilidades:**
- Define objetivos del sistema
- Asigna prioridades a tareas
- Coordina Catedraticos
- Toma decisiones de arquitectura
- Aproueba planes de accion

**Output tipico:**
```yaml
plan:
  objetivo: "Completar ingresión de Tema 5"
  prioridad: 1
  tareas:
    - agente: ejecutor
      tarea: "ingest_documento"
      params:
        file: "tema5.pdf"
        tema: 5
    - agente: archivador
      tarea: "actualizar_indice"
```

### Ejecutor

| Atributo | Valor |
|----------|-------|
| **Rol** | Implementador |
| **Namespace** | `ejecutor.*` |
| **Prioridad** | Media |

**Responsabilidades:**
- Ejecuta tareas asignadas
- Genera codigo y configuraciones
- Ejecuta tests
- Produce documentacion
- Reporta resultados

**Output tipico:**
```yaml
resultado:
  tarea: "ingest_documento"
  estado: "completado"
  metricas:
    chunks_creados: 45
    embeddings_generados: 45
    tiempo_segundos: 12.3
  errores: []
```

### Archivador

| Atributo | Valor |
|----------|-------|
| **Rol** | Gestor de memoria |
| **Namespace** | `archivador.*` |
| **Prioridad** | Media |

**Responsabilidades:**
- Mantiene contexto historico
- Indexa conocimiento
- Recupera informacion relevante
- Gestiona embeddings
- Actualiza base de conocimiento

**Output tipico:**
```yaml
contexto:
  consulta: "tema 5 derecho administrativo"
  resultados:
    - chunk_id: 234
      similitud: 0.92
      contenido: "El procedimiento administrativo..."
    - chunk_id: 237
      similitud: 0.87
      contenido: "Los recursos administrativos..."
```

### Flujo del Concilio

```
+-------------+     +-------------+     +-------------+
|   DIRECTOR  |---->|   EJECUTOR  |---->| ARCHIVADOR  |
|             |     |             |     |             |
| 1. Planifica|     | 2. Ejecuta  |     | 3. Registra |
|              |     |              |     |              |
| Recibe       |     | Implementa   |     | Guarda       |
| solicitud    |     | solucion     |     | resultado    |
+-------------+     +-------------+     +-------------+
      ^                                        |
      |                                        |
      +----------------------------------------+
                    4. Feedback
```

---

## Catedra - 6 Catedraticos

**Origen:** OPENCLAW-system
**Proposito:** Gestion por dominios funcionales

### CKO (Chief Knowledge Officer)

| Atributo | Valor |
|----------|-------|
| **Namespace** | `cko.*` |
| **Dominio** | Gestion del conocimiento |
| **Especialistas** | librarian, curator |

**Responsabilidades en Oposiciones:**
- Gestion del temario
- Organizacion de flashcards
- Indexacion de contenido
- Curacion de calidad

**Metricas que supervisa:**
- Total de chunks indexados
- Cobertura de temas
- Calidad de embeddings

### CEngO (Chief Engineering Officer)

| Atributo | Valor |
|----------|-------|
| **Namespace** | `cengo.*` |
| **Dominio** | Arquitectura tecnica |
| **Especialistas** | architect, builder |

**Responsabilidades en Oposiciones:**
- Arquitectura del sistema
- APIs y servicios
- Performance
- Integraciones tecnicas

**Metricas que supervisa:**
- Latencia de respuestas
- Uptime de servicios
- Errores de sistema

### COO (Chief Operations Officer)

| Atributo | Valor |
|----------|-------|
| **Namespace** | `coo.*` |
| **Dominio** | Operaciones diarias |
| **Especialistas** | analyst, validator |

**Responsabilidades en Oposiciones:**
- Flujos de estudio
- Programacion de repasos
- Generacion de tests
- Procesos automatizados

**Metricas que supervisa:**
- Flashcards pendientes de repaso
- Tests generados hoy
- Sesiones de estudio

### CHO (Chief Human Officer)

| Atributo | Valor |
|----------|-------|
| **Namespace** | `cho.*` |
| **Dominio** | Experiencia de usuario |
| **Especialistas** | mentor, scout |

**Responsabilidades en Oposiciones:**
- UX del dashboard
- Feedback de usuario
- Onboarding
- Documentacion de usuario

**Metricas que supervisa:**
- Satisfaccion de usuario
- Tiempo en plataforma
- Completacion de tareas

### CSRO (Chief Security & Risk Officer)

| Atributo | Valor |
|----------|-------|
| **Namespace** | `csro.*` |
| **Dominio** | Seguridad |
| **Especialistas** | guardian |

**Responsabilidades en Oposiciones:**
- Proteccion de datos
- Validacion de inputs
- Auditoria de acceso
- Backups

**Metricas que supervisa:**
- Intentos de acceso fallidos
- Vulnerabilidades
- Backups realizados

### CCO (Chief Compliance Officer)

| Atributo | Valor |
|----------|-------|
| **Namespace** | `cco.*` |
| **Dominio** | Cumplimiento de normas |
| **Especialistas** | validator |

**Responsabilidades en Oposiciones:**
- Validacion de contenido
- Adecuacion a normativas
- Calidad de preguntas
- Etica de IA

**Metricas que supervisa:**
- Contenido validado
- Errores de calidad
- Incidencias

---

## Especialistas - 9 Agentes

**Origen:** OPENCLAW-system
**Proposito:** Ejecucion especializada

### Tabla de Especialistas

| Especialista | Namespace | Funcion General | Uso en Oposiciones |
|--------------|-----------|-----------------|-------------------|
| **analyst** | `analyst.*` | Analisis de datos | Detecta areas debiles, analiza progreso |
| **architect** | `architect.*` | Diseno de sistemas | Disena flujos de estudio |
| **builder** | `builder.*` | Implementacion | Genera flashcards, tests |
| **curator** | `curator.*` | Curacion | Selecciona mejor contenido |
| **guardian** | `guardian.*` | Seguridad | Valida inputs, protege datos |
| **librarian** | `librarian.*` | Documentacion | Indexa temario, gestiona RAG |
| **mentor** | `mentor.*` | Ensenanza | Explica conceptos, da feedback |
| **scout** | `scout.*` | Investigacion | Busca recursos, compara |
| **validator** | `validator.*` | QA | Valida calidad de contenido |

### Detalle por Especialista

#### analyst

```yaml
namespace: analyst.*
funcion: "Analisis de datos y metricas"
catedratico_supervisor: COO

tareas_oposiciones:
  - analizar_progreso:
      input: historial_estudio
      output: informe_progreso
  - detectar_areas_debiles:
      input: resultados_tests, flashcard_ease
      output: lista_areas_debiles
  - predecir_preparacion:
      input: metricas_agregadas
      output: score_preparacion

herramientas:
  - pandas (analisis)
  - sqlite3 (consultas)
  - matplotlib (visualizacion)
```

#### architect

```yaml
namespace: architect.*
funcion: "Diseno de sistemas y flujos"
catedratico_supervisor: CEngO

tareas_oposiciones:
  - disenar_flujo_estudio:
      input: objetivos, disponibilidad
      output: plan_estudio
  - optimizar_ruta_aprendizaje:
      input: dependencias_temas
      output: orden_optimo
  - disenar_estructura_db:
      input: requerimientos
      output: esquema_sql

herramientas:
  - diagramas (mermaid)
  - sql (diseno)
  - yaml (configuracion)
```

#### builder

```yaml
namespace: builder.*
funcion: "Implementacion y generacion"
catedratico_supervisor: CEngO

tareas_oposiciones:
  - generar_flashcards:
      input: chunk_texto
      output: lista_flashcards
      api: MiniMax M2.5
  - generar_test:
      input: tema, num_preguntas
      output: test_completo
      api: MiniMax M2.5
  - crear_embedding:
      input: texto
      output: vector_1024
      api: Mistral

herramientas:
  - MiniMax API
  - Mistral API
  - PyMuPDF (PDFs)
```

#### curator

```yaml
namespace: curator.*
funcion: "Curacion de contenido"
catedratico_supervisor: CKO

tareas_oposiciones:
  - filtrar_contenido_relevante:
      input: chunks_crudos
      output: chunks_curados
  - priorizar_flashcards:
      input: flashcards_generadas
      output: flashcards_priorizadas
  - detectar_duplicados:
      input: base_conocimiento
      output: lista_duplicados

herramientas:
  - similitud_coseno
  - clustering
```

#### guardian

```yaml
namespace: guardian.*
funcion: "Seguridad y proteccion"
catedratico_supervisor: CSRO

tareas_oposiciones:
  - validar_input:
      input: datos_usuario
      output: datos_sanitizados
  - audit_acceso:
      input: logs
      output: informe_auditoria
  - backup_datos:
      input: bases_datos
      output: archivo_backup

herramientas:
  - Security Pipeline (/opt/openclaw-memory/security_pipeline.py)
  - bcrypt (hashing)
  - sqlite3 (backup)
```

#### librarian

```yaml
namespace: librarian.*
funcion: "Gestion documental"
catedratico_supervisor: CKO

tareas_oposiciones:
  - indexar_documento:
      input: archivo_pdf
      output: chunks_indexados
  - buscar_semantico:
      input: consulta
      output: resultados_ranking
  - actualizar_indice:
      input: nuevos_chunks
      output: indice_actualizado

herramientas:
  - RAG Store (/opt/openclaw-memory/rag_store.py)
  - Mistral embeddings
  - sqlite3
```

#### mentor

```yaml
namespace: mentor.*
funcion: "Ensenanza y feedback"
catedratico_supervisor: CHO

tareas_oposiciones:
  - explicar_concepto:
      input: termino, contexto
      output: explicacion
  - dar_feedback:
      input: respuesta_usuario, correcta
      output: feedback_educativo
  - generar_pista:
      input: pregunta, dificultad
      output: pista_progresiva

herramientas:
  - MiniMax M2.5
  - templates de feedback
```

#### scout

```yaml
namespace: scout.*
funcion: "Investigacion y descubrimiento"
catedratico_supervisor: CHO

tareas_oposiciones:
  - buscar_recursos:
      input: tema
      output: lista_recursos
  - comparar_fuentes:
      input: multiples_textos
      output: comparacion
  - detectar_novedades:
      input: ultimas_actualizaciones
      output: cambios_relevantes

herramientas:
  - web search (MCP)
  - comparacion de textos
```

#### validator

```yaml
namespace: validator.*
funcion: "Validacion y QA"
catedratico_supervisor: CCO

tareas_oposiciones:
  - validar_flashcard:
      input: flashcard
      output: validacion + score
  - validar_test:
      input: test
      output: validacion + errores
  - verificar_respuesta:
      input: respuesta, correcta
      output: evaluacion

herramientas:
  - reglas de validacion
  - tests automatizados
```

---

## Adaptacion para Oposiciones

### Mapeo de Funcionalidades

| Funcionalidad Oposiciones | Agentes Involucrados | Flujo |
|---------------------------|---------------------|-------|
| Ingestion de temario | Director, librarian, builder | Director planifica -> librarian indexa -> builder crea embeddings |
| Generacion de flashcards | Director, builder, curator, validator | Director ordena -> builder genera -> curator prioriza -> validator aprueba |
| Repaso SM-2 | COO, analyst, mentor | COO programa -> analyst detecta debiles -> mentor explica |
| Generacion de tests | Director, builder, validator | Director define -> builder crea -> validator revisa |
| Analisis de progreso | analyst, archivador | analyst procesa -> archivador guarda |
| Bot Telegram | guardian, mentor, librarian | guardian valida -> librarian busca -> mentor responde |

### Workflows Especificos

#### Workflow: Ingestion Completa de Tema

```yaml
workflow: ingest_tema
concilio:
  director:
    - recibir_solicitud(tema_id, archivo)
    - crear_plan("ingestion")
    - asignar_tareas

  ejecutor:
    - tarea: librarian.indexar_documento
    - tarea: builder.crear_embeddings
    - tarea: curator.filtrar_contenido

  archivador:
    - registrar_proceso
    - actualizar_indice_global
    - notificar_completado
```

#### Workflow: Generacion de Flashcards

```yaml
workflow: generar_flashcards
concilio:
  director:
    - definir_objetivo(deck_id, tema_id, cantidad)
    - priorizar_chunks

  ejecutor:
    - tarea: builder.generar_flashcards
      api: MiniMax M2.5
      batch_size: 10
    - tarea: curator.priorizar
    - tarea: validator.validar_lote

  archivador:
    - almacenar_flashcards
    - actualizar_metricas_deck
```

#### Workflow: Sesion de Repaso

```yaml
workflow: sesion_repaso
concilio:
  director:
    - determinar_flashcards_debidas
    - configurar_sesion

  ejecutor:
    - tarea: analyst.calcular_dificultad
    - tarea: mentor.preparar_feedback

  archivador:
    - registrar_respuestas
    - actualizar_parametros_sm2
```

---

## Protocolo de Comunicacion

### Formato de Mensajes

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class MessageType(Enum):
    TASK = "task"           # Asignacion de tarea
    QUERY = "query"         # Consulta
    RESULT = "result"       # Resultado
    CONTEXT = "context"     # Contexto compartido
    ERROR = "error"         # Error
    FEEDBACK = "feedback"   # Retroalimentacion

@dataclass
class AgentMessage:
    """Mensaje entre agentes"""
    id: str
    from_agent: str        # namespace del emisor
    to_agent: str          # namespace del receptor | "broadcast"
    message_type: MessageType
    priority: int          # 1=critico, 2=alto, 3=medio, 4=bajo, 5=info
    payload: dict
    timestamp: datetime
    correlation_id: str    # Para追踪 respuestas
```

### Ejemplo de Conversacion

```yaml
# Director -> Builder: Asignar tarea
- id: msg-001
  from: director
  to: builder
  type: task
  priority: 2
  payload:
    tarea: generar_flashcards
    params:
      tema: 5
      cantidad: 20
  timestamp: 2025-03-16T10:00:00

# Builder -> Curator: Solicitar curacion
- id: msg-002
  from: builder
  to: curator
  type: task
  priority: 3
  payload:
    tarea: priorizar_chunks
    params:
      tema: 5
  timestamp: 2025-03-16T10:01:00
  correlation_id: msg-001

# Builder -> Director: Reportar resultado
- id: msg-003
  from: builder
  to: director
  type: result
  priority: 3
  payload:
    tarea: generar_flashcards
    estado: completado
    flashcards_creadas: 20
    errores: []
  timestamp: 2025-03-16T10:15:00
  correlation_id: msg-001
```

---

## Namespaces

### Convencion

```
{nivel}.{rol}.{funcion}

Ejemplos:
- concilio.director.planificar
- catedra.cko.gestion
- specialist.librarian.indexar
```

### Arbol de Namespaces

```
concilio/
├── director/
│   ├── planificar
│   ├── asignar
│   └── coordinar
├── ejecutor/
│   ├── implementar
│   ├── testear
│   └── documentar
└── archivador/
    ├── guardar
    ├── recuperar
    └── indexar

catedra/
├── cko/
│   ├── conocimiento
│   └── documentacion
├── cengo/
│   ├── arquitectura
│   └── integracion
├── coo/
│   ├── operaciones
│   └── procesos
├── cho/
│   ├── ux
│   └── comunicacion
├── csro/
│   ├── seguridad
│   └── auditoria
└── cco/
    ├── validacion
    └── cumplimiento

specialist/
├── analyst/
│   ├── analizar
│   ├── detectar
│   └── predecir
├── architect/
│   ├── disenar
│   └── optimizar
├── builder/
│   ├── generar
│   ├── crear
│   └── implementar
├── curator/
│   ├── filtrar
│   ├── priorizar
│   └── curar
├── guardian/
│   ├── validar
│   ├── proteger
│   └── auditar
├── librarian/
│   ├── indexar
│   ├── buscar
│   └── organizar
├── mentor/
│   ├── explicar
│   ├── ensenar
│   └── feedback
├── scout/
│   ├── investigar
│   ├── buscar
│   └── comparar
└── validator/
    ├── validar
    ├── verificar
    └── aprobar
```

---

**Fin del documento de Sistema de Agentes (v1.0.0)**
