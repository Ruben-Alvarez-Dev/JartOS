# Contexto del Proyecto

**Última actualización:** 2026-03-16
**Versión:** 1.0.0 (Integrado)

---

## Índice

1. [Visión de JartOS](#visión-de-jartos)
2. [Fusión de Tres Sistemas](#fusión-de-tres-sistemas)
3. [Filosofía de Extensibilidad](#filosofía-de-extensibilidad)
4. [Sistemas Analizados - DATOS REALES](#sistemas-analizados---datos-reales)
5. [Casos de Uso Actuales y Futuros](#casos-de-uso-actuales-y-futuros)
6. [Objetivo Principal](#objetivo-principal)
7. [Alcance](#alcance)

---

## Visión de JartOS

**JartOS es un sistema operativo agéntico personal** que integra inteligencia artificial, automatización y productividad de forma extensible a cualquier dominio.

### ¿Qué significa "Sistema Operativo Agéntico"?

Un **sistema operativo agéntico** es una plataforma que:
1. **Coordina múltiples agentes de IA** que trabajan juntos hacia objetivos
2. **Mantiene contexto persistente** entre sesiones y dominios
3. **Automatiza tareas complejas** mediante orquestación de servicios
4. **Escala horizontalmente** añadiendo nuevos dominios sin cambios al core
5. **Aprende y se adapta** con el uso del usuario

### Principios Fundamentales

- **Extensibilidad sobre especificidad** - Diseñado para adaptarse, no para ser rígido
- **Contexto inteligente** - Memoria jerárquica que recuerda lo importante
- **Coordinación automática** - Agentes que trabajan juntos sin supervisión constante
- **Dominio-agnostic** - El core no está atado a un caso de uso específico

---

## Fusión de Tres Sistemas

JartOS nace de la fusión estratégica de tres sistemas existentes, cada uno aportando una pieza fundamental:

### 1. JartOS - Estructura y Organización
- **39 GB de conocimiento estructurado**
- **690 archivos .md documentados**
- **Sistema de 15 Tiers** - Organización jerárquica
- **Sistema de puertos 1XXYY** - Asignación predecible de servicios
- **CONVENTIONS.md v7.0** - Estándares de código

### 2. OPENCLAW-system - Arquitectura de Agentes
- **Concilio tri-agente** - Director, Ejecutor, Archivador
- **6 Catedráticos** - Roles funcionales (CKO, CEngO, COO, etc.)
- **9 Especialistas** - Agentes especializados con namespaces
- **Memoria de 4 tipos** - Jerarquía de contexto
- **Motor de conocimiento en 5 capas** - Procesamiento de información

### 3. OPENCLAW-city - Implementación en Producción
- **RAG Store funcional** - Búsqueda semántica
- **Memory Store persistente** - SQLite
- **Security Pipeline** - Validación de inputs
- **Ramiro Bot** - Base para interfaz Telegram
- **LiveKit Server** - Voz en tiempo real
- **APIs configuradas** - MiniMax M2.5 + Mistral embeddings

### Sinergia de la Fusión

| Sistema | Aporta | Resultado en JartOS |
|---------|--------|---------------------|
| **JartOS** | Estructura | Organización escalable de dominios |
| **OPENCLAW-system** | Agentes | Coordinación inteligente |
| **OPENCLAW-city** | Producción | Componentes probados y listos |

---

## Filosofía de Extensibilidad

### No es un sistema PARA algo, es un sistema PARA TODO

JartOS no está diseñado como "un sistema de oposiciones" o "un sistema de estudio". Está diseñado como una **plataforma agéntica** que puede adaptarse a cualquier dominio.

### ¿Cómo funciona la extensibilidad?

```
CORE DE JARTOS (invariante)
├── Concilio de Agentes
├── Memoria Jerárquica
├── Sistema de 15 Tiers
├── Puertos 1XXYY
└── Infraestructura común

┌─────────────────────────────────────┐
│     DOMINIOS (extensibles)          │
├─────────────────────────────────────┤
│  DOMINIO ACTUAL 1: Oposiciones     │
│  - Temario Service                  │
│  - Flashcards Service               │
│  - Tests Service                   │
│  - Analytics Service                │
├─────────────────────────────────────┤
│  DOMINIO ACTUAL 2: Desarrollo      │
│  - Code Review Service             │
│  - Documentation Service           │
│  - Testing Service                 │
├─────────────────────────────────────┤
│  DOMINIO FUTURO N: Cualquiera       │
│  - Añadir servicios específicos    │
│  - Sin tocar el core                │
└─────────────────────────────────────┘
```

### Ejemplo de Extensión

Para añadir un nuevo dominio (ej. Gestión Personal):

1. **Crear servicios específicos** en `03-SERVICES/gestion-personal/`
2. **Definir memoria de dominio** en `02-DATA/gestion-personal.db`
3. **Registrar en el Concilio** - Los agentes ya saben coordinar
4. **Añadir interfaz** si es necesario en `06-INTERFACE/`

**El core NO cambia.** Solo se añaden módulos específicos.

---

## Casos de Uso Actuales y Futuros

### Actuales

#### 1. Oposiciones (Civil Service Exams)

El uso principal actual del sistema:

- **Ingestión de temarios** - PDF/DOCX a conocimiento
- **Búsqueda semántica** - Encontrar conceptos rápidamente
- **Flashcards SM-2** - Repaso espaciado optimizado
- **Tests automáticos** - Evaluación con análisis de resultados
- **Planificación de estudio** - IA que recomienda qué estudiar

**¿Por qué funciona?**
- El Concilio planifica sesiones de estudio
- El Ejecutor genera materiales automáticamente
- El Archivador mantiene progreso y contexto
- La memoria jerárquica recuerda temas, errores, progreso

#### 2. Desarrollo de Software

Uso secundario actual:

- **Gestión de documentación** - Ingestión de specs, APIs
- **Búsqueda en código** - Búsqueda semántica de funcionalidad
- **Tests automáticos** - Generación desde specs
- **Code review** - Análisis con IA

**¿Por qué funciona?**
- Mismos agentes, diferente dominio
- Memoria de dominio para código
- Servicios específicos de desarrollo

### Futuros (Potenciales)

#### 3. Estudio General

- Preparación de cursos
- Certificaciones técnicas
- Aprendizaje de idiomas
- Formación continua

#### 4. Gestión Personal

- Tareas y proyectos
- Notas y conocimiento
- Salud y hábitos
- Finanzas personales

#### 5. Empresarial

- CRM y gestión de clientes
- Procesos de negocio
- Automatización de flujos
- Dashboard de métricas

#### 6. Cualquier Dominio

La arquitectura permite añadir **cualquier dominio** simplemente:
1. Definiendo servicios específicos
2. Creando memoria de dominio
3. Registrando en el Concilio
4. Añadiendo interfaz si es necesario

---

## Sistemas Analizados - DATOS REALES

### 1. JartOS

**Ubicación:** `/Volumes/-Documents/ARCHIVOS MAC MINI/JartOS`

**Métricas REALES:**
- **Tamaño:** 39 GB
- **Archivos .md:** 690 archivos
- **Tiers:** 15 niveles (00-FOUNDATION a 14-ARCHIVE)

**Estructura de Tiers:**
```
00-FOUNDATION/     # Configuración base, CONVENTIONS.md v7.0
01-INFRA/          # Docker, redes, puertos
02-DATA/           # Bases de datos, almacenamiento
03-SERVICES/       # Microservicios
04-AGENTS/         # Agentes de IA
05-ORCHESTRATION/  # Orquestadores
06-INTERFACE/      # UI, dashboards
07-INTEGRATION/    # APIs externas
08-AUTOMATION/     # Scripts automatizados
09-ANALYTICS/      # Métricas, logs
10-SECURITY/       # Seguridad
11-TESTING/        # Tests
12-DOCS/           # Documentación
13-EXPERIMENTAL/   # Prototipos
14-ARCHIVE/        # Archivo histórico
```

**Sistema de Puertos 1XXYY:**
- `1XXYY` donde XX = layer number, YY = service number
- Ejemplo: Layer 03 (DATA), service 01 = puerto 10301

**14 Agentes Documentados:**
| Agente | Función |
|--------|---------|
| `architect` | Diseño de arquitectura |
| `backend` | Desarrollo backend |
| `frontend` | Desarrollo frontend |
| `devops` | Deploy e infra |
| `qa` | Testing |
| `security` | Auditoría seguridad |
| `docs` | Documentación |
| `data` | Pipelines de datos |
| `ai` | Integración IA |
| `integrator` | Integraciones externas |
| `monitor` | Monitoreo |
| `optimizer` | Performance |
| `researcher` | Investigación |
| `coordinator` | Coordinación general |

**Qué aprovechar:**
- Sistema de puertos 1XXYY
- CONVENTIONS.md v7.0
- Estructura de 15 Tiers
- Patrones de agentes documentados

**Qué NO usar:**
- Automatizaciones específicas de MacOS
- Servicios no relacionados con el dominio actual

---

### 2. OPENCLAW-system

**Ubicación:** GitHub (repositorio privado)

**Arquitectura Jerárquica 4 Niveles:**
```
NIVEL 1: Concilio (3 agentes)
    |
    v
NIVEL 2: Catedra (6 Catedráticos)
    |
    v
NIVEL 3: Especialistas (9 agentes)
    |
    v
NIVEL 4: Workers (infraestructura)
```

**Concilio Tri-Agente:**
| Rol | Función | Descripción |
|-----|---------|-------------|
| **Director** | Planificar | Define objetivos, asigna tareas, prioriza |
| **Ejecutor** | Implementar | Ejecuta tareas, genera código, prueba |
| **Archivador** | Memorizar | Mantiene contexto, indexa, recupera |

**6 Catedráticos:**
| Catedrático | Función | Namespace |
|-------------|---------|-----------|
| **CKO** | Gestión conocimiento | `cko.*` |
| **CEngO** | Arquitectura técnica | `cengo.*` |
| **COO** | Operaciones diarias | `coo.*` |
| **CHO** | UX y comunicación | `cho.*` |
| **CSRO** | Seguridad | `csro.*` |
| **CCO** | Cumplimiento normas | `cco.*` |

**9 Especialistas:**
| Especialista | Namespace | Función |
|--------------|-----------|---------|
| `analyst` | `analyst.*` | Análisis de datos |
| `architect` | `architect.*` | Diseño de sistemas |
| `builder` | `builder.*` | Implementación |
| `curator` | `curator.*` | Curación de contenido |
| `guardian` | `guardian.*` | Seguridad |
| `librarian` | `librarian.*` | Gestión documental |
| `mentor` | `mentor.*` | Enseñanza |
| `scout` | `scout.*` | Investigación |
| `validator` | `validator.*` | Testing y QA |

**Sistema de Memoria 4 Tipos:**
| Tipo | Alcance | Uso |
|------|---------|-----|
| **Memoria Agente** | Individual | Contexto personal del agente |
| **Memoria Unidad** | Equipo | Compartido entre agentes de misma unidad |
| **Memoria Dominio** | Temática | Conocimiento de un dominio específico |
| **Memoria Global** | Sistema | Conocimiento transversal |

**Qué aprovechar:**
- Concilio tri-agente para coordinación
- Sistema de memoria de 4 tipos
- Namespaces para organización
- Motor de conocimiento en capas

---

### 3. OPENCLAW-city

**Ubicación:** VPS (producción) + GitHub

**Estado:** ACTIVO en producción

**Componentes REALES en Producción:**

| Componente | Path | Estado |
|------------|------|--------|
| **OpenClaw Gateway** | `/opt/openclaw-gateway/` | Activo |
| **RAG Store** | `/opt/openclaw-memory/rag_store.py` | Activo |
| **Memory Store** | `/opt/openclaw-memory/memory_store.py` | Activo |
| **Security Pipeline** | `/opt/openclaw-memory/security_pipeline.py` | Activo |
| **Ramiro Bot** | `/opt/openclaw-memory/ramiro_bot.py` | Activo |

**Bot Telegram "Ramiro" - Comandos Actuales:**
```
/start      - Iniciar bot
/help       - Mostrar ayuda
/search     - Buscar en conocimiento
/ask        - Pregunta directa a IA
/status     - Estado del sistema
/history    - Historial de conversación
/clear      - Limpiar contexto
/export     - Exportar datos
```

**LiveKit Server:**
- Estado: Activo
- Uso: Voz en tiempo real
- Integración: WebRTC

**APIs Configuradas:**
| API | Uso | Modelo |
|-----|-----|--------|
| **MiniMax M2.5** | LLM principal | Generación de texto |
| **Mistral** | Embeddings | 1024 dimensiones |

**Qué aprovechar:**
- RAG Store funcional
- Memory Store persistente
- Security Pipeline
- Ramiro Bot como base
- MiniMax M2.5 API ya configurada
- Mistral embeddings (1024 dims)

---

## Objetivo Principal

Crear un **sistema operativo agéntico personal** que permita:

### Objetivos Principales

1. **Coordinar agentes inteligentemente**
   - Concilio tri-agente para toma de decisiones
   - Catedra de especialistas por dominio
   - Comunicación A2A (Agent-to-Agent)

2. **Mantener contexto persistente**
   - Memoria jerárquica de 4 tipos
   - Búsqueda en múltiples niveles
   - Contexto entre sesiones

3. **Automatizar tareas complejas**
   - Orquestación de servicios
   - Flujos de trabajo automáticos
   - Planificación con IA

4. **Escalar horizontalmente**
   - Añadir dominios sin cambios al core
   - Modularidad extensible
   - Arquitectura de 15 Tiers

### Objetivos Secundarios

5. **Interfaz intuitiva**
   - Dashboard web general
   - CLI potente
   - Bot Telegram (basado en Ramiro)

6. **Voz opcional**
   - LiveKit para voz en tiempo real
   - Integración con el Concilio
   - Práctica oral y consultas

---

## Alcance

### Incluido (MVP - 6 semanas)

- [x] Core del sistema (Concilio, Memoria, Tiers)
- [x] Ingestión de documentos (PDF/DOCX)
- [x] Búsqueda semántica (RAG de OPENCLAW-city)
- [x] Flashcards con SM-2
- [x] Generador de tests básico
- [ ] Dashboard web mínimo
- [ ] Métricas de progreso
- [ ] Bot Telegram básico (extender Ramiro)

### Fase 2 (4 semanas adicionales)

- [ ] AI analytics completo
- [ ] Planes de estudio semanales
- [ ] Predicción de preparación
- [ ] Recomendaciones diarias
- [ ] Concilio tri-agente para coordinación

### Fase 3+ (4 semanas adicionales)

- [ ] Asistente de voz (LiveKit)
- [ ] Integración Telegram completa
- [ ] Mobile app (opcional)

### Fase 4+ (Extensibilidad)

- [ ] Framework para añadir nuevos dominios
- [ ] Documentación de extensión
- [ ] Ejemplos de dominios adicionales
- [ ] Marketplace de servicios (futuro)

---

## Restricciones

### Técnicas

- Python 3.11+ (por typing y performance)
- SQLite (heredado de OPENCLAW-city)
- APIs de IA ya configuradas (MiniMax + Mistral)
- Local-first (datos en local, no en nube)

### Presupuesto

- Mistral API: ~$0.0001/1K tokens (embeddings 1024 dims)
- MiniMax M2.5 API: ~$0.001/1K tokens (generación)
- Estimado mensual: $5-10 para uso personal

### Tiempo

- MVP: 6 semanas
- Fase 2: 4 semanas adicionales
- Fase 3: 4 semanas adicionales
- Fase 4+: Depende del dominio

---

**Fin del documento de Contexto (v1.0.0 Integrado)**
