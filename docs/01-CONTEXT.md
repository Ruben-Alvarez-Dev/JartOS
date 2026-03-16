# Contexto del Proyecto

**Ultima actualizacion:** 2026-03-16
**Version:** 1.0.0 (Integrado)

---

## Indice

1. [Origen del Proyecto](#origen-del-proyecto)
2. [Sistemas Analizados - DATOS REALES](#sistemas-analizados---datos-reales)
3. [Decision de Fusion (Opcion C)](#decision-de-fusion-opcion-c)
4. [Objetivo Principal](#objetivo-principal)
5. [Alcance](#alcance)

---

## Origen del Proyecto

Oposiciones System nace de la fusion de tres sistemas existentes desarrollados por separado:

1. **JartOS** - Sistema de automatizacion personal (39GB, 690 archivos .md)
2. **OPENCLAW-system** - Framework de agentes de IA (GitHub)
3. **OPENCLAW-city** - Implementacion enterprise con LiveKit (VPS en produccion)

El objetivo es crear un sistema unificado para la preparacion de oposiciones, aprovechando lo mejor de cada sistema.

---

## Sistemas Analizados - DATOS REALES

### 1. JartOS

**Ubicacion:** `/Volumes/-Documents/ARCHIVOS MAC MINI/JartOS`

**Metricas REALES:**
- **Tamano:** 39 GB
- **Archivos .md:** 690 archivos
- **Tiers:** 15 niveles (00-FOUNDATION a 14-ARCHIVE)

**Estructura de Tiers:**
```
00-FOUNDATION/     # Configuracion base, CONVENTIONS.md v7.0
01-INFRA/          # Docker, redes, puertos
02-DATA/           # Bases de datos, almacenamiento
03-SERVICES/       # Microservicios
04-AGENTS/         # Agentes de IA
05-ORCHESTRATION/  # Orquestadores
06-INTERFACE/      # UI, dashboards
07-INTEGRATION/    # APIs externas
08-AUTOMATION/     # Scripts automatizados
09-ANALYTICS/      # Metricas, logs
10-SECURITY/       # Seguridad
11-TESTING/        # Tests
12-DOCS/           # Documentacion
13-EXPERIMENTAL/   # Prototipos
14-ARCHIVE/        # Archivo historico
```

**Sistema de Puertos 1XXYY:**
- `1XXYY` donde XX = layer number, YY = service number
- Ejemplo: Layer 03 (DATA), service 01 = puerto 10301
- Usado en todos los servicios Docker

**14 Agentes Documentados** en `project/normas/agents/`:
| Agente | Funcion | Path |
|--------|---------|------|
| `architect` | Diseno de arquitectura | `project/normas/agents/architect.md` |
| `backend` | Desarrollo backend | `project/normas/agents/backend.md` |
| `frontend` | Desarrollo frontend | `project/normas/agents/frontend.md` |
| `devops` | Deploy e infra | `project/normas/agents/devops.md` |
| `qa` | Testing | `project/normas/agents/qa.md` |
| `security` | Auditoria seguridad | `project/normas/agents/security.md` |
| `docs` | Documentacion | `project/normas/agents/docs.md` |
| `data` | Pipelines de datos | `project/normas/agents/data.md` |
| `ai` | Integracion IA | `project/normas/agents/ai.md` |
| `integrator` | Integraciones externas | `project/normas/agents/integrator.md` |
| `monitor` | Monitoreo | `project/normas/agents/monitor.md` |
| `optimizer` | Performance | `project/normas/agents/optimizer.md` |
| `researcher` | Investigacion | `project/normas/agents/researcher.md` |
| `coordinator` | Coordinacion general | `project/normas/agents/coordinator.md` |

**Stack Tecnologico:**
- Docker Compose para orquestacion
- Python 3.11+ para servicios
- Node.js para interfaces
- Ollama para LLM local

**Que aprovechar:**
- Sistema de puertos 1XXYY
- CONVENTIONS.md v7.0 (estandares de codigo)
- Estructura de 15 Tiers
- Patrones de agentes documentados

**Que NO usar:**
- Automatizaciones especificas de MacOS
- Servicios no relacionados con estudio

---

### 2. OPENCLAW-system

**Ubicacion:** GitHub (repositorio privado)

**Arquitectura Jerarquica 4 Niveles:**
```
NIVEL 1: Concilio (3 agentes)
    |
    v
NIVEL 2: Catedra (6 Catedraticos)
    |
    v
NIVEL 3: Especialistas (9 agentes)
    |
    v
NIVEL 4: Workers (infraestructura)
```

**Concilio Tri-Agente:**
| Rol | Funcion | Descripcion |
|-----|---------|-------------|
| **Director** | Planificar | Define objetivos, asigna tareas, prioriza |
| **Ejecutor** | Implementar | Ejecuta tareas, genera codigo, prueba |
| **Archivador** | Memorizar | Mantiene contexto, indexa, recupera |

**6 Catedraticos:**
| Catedratico | Funcion | Namespace |
|-------------|---------|-----------|
| **CKO** (Chief Knowledge Officer) | Gestion conocimiento | `cko.*` |
| **CEngO** (Chief Engineering Officer) | Arquitectura tecnica | `cengo.*` |
| **COO** (Chief Operations Officer) | Operaciones diarias | `coo.*` |
| **CHO** (Chief Human Officer) | UX y comunicacion | `cho.*` |
| **CSRO** (Chief Security Officer) | Seguridad | `csro.*` |
| **CCO** (Chief Compliance Officer) | Cumplimiento normas | `cco.*` |

**9 Especialistas con Namespaces:**
| Especialista | Namespace | Funcion |
|--------------|-----------|---------|
| `analyst` | `analyst.*` | Analisis de datos |
| `architect` | `architect.*` | Diseno de sistemas |
| `builder` | `builder.*` | Implementacion |
| `curator` | `curator.*` | Curacion de contenido |
| `guardian` | `guardian.*` | Seguridad |
| `librarian` | `librarian.*` | Gestion documental |
| `mentor` | `mentor.*` | Ensenanza |
| `scout` | `scout.*` | Investigacion |
| `validator` | `validator.*` | Testing y QA |

**Sistema de Memoria 4 Tipos:**
| Tipo | Alcance | Uso |
|------|---------|-----|
| **Memoria Agente** | Individual | Contexto personal del agente |
| **Memoria Unidad** | Equipo | Compartido entre agentes de misma unidad |
| **Memoria Dominio** | Tematica | Conocimiento de un dominio especifico |
| **Memoria Global** | Sistema | Conocimiento transversal |

**Motor de Conocimiento 5 Capas:**
1. Raw Data (datos brutos)
2. Processed (datos procesados)
3. Indexed (indices y embeddings)
4. Knowledge (conocimiento estructurado)
5. Wisdom (insights y patrones)

**Validacion 5 Capas:**
1. Syntax (sintaxis)
2. Schema (estructura)
3. Logic (logica)
4. Business (reglas de negocio)
5. Security (seguridad)

**Que aprovechar:**
- Concilio tri-agente para coordinacion
- Sistema de memoria de 4 tipos
- Namespaces para organizacion
- Motor de conocimiento en capas

**Que NO usar:**
- Integracion de email
- Telegram bot generico

---

### 3. OPENCLAW-city

**Ubicacion:** VPS (produccion) + GitHub

**Estado:** ACTIVO en produccion

**Componentes REALES en Produccion:**

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
/history    - Historial de conversacion
/clear      - Limpiar contexto
/export     - Exportar datos
```

**LiveKit Server:**
- Estado: Activo
- Uso: Voz en tiempo real
- Integracion: WebRTC

**Voice Agent Worker:**
- Servicio de procesamiento de voz
- Integracion con A2A Protocol

**A2A Protocol:**
- Agent-to-Agent communication
- Mensajeria entre agentes

**APIs Configuradas:**
| API | Uso | Modelo |
|-----|-----|--------|
| **MiniMax M2.5** | LLM principal | Generacion de texto |
| **Mistral** | Embeddings | 1024 dimensiones |

**Que aprovechar:**
- `/opt/openclaw-memory/rag_store.py` - RAG funcional
- `/opt/openclaw-memory/memory_store.py` - Persistencia
- `/opt/openclaw-memory/security_pipeline.py` - Seguridad
- `/opt/openclaw-memory/ramiro_bot.py` - Base del bot
- MiniMax M2.5 API ya configurada
- Mistral embeddings (1024 dims)

**Que NO usar:**
- SIP trunking (fase posterior)
- VPS completo (desarrollo local primero)

---

## Decision de Fusion (Opcion C)

Se selecciono la **Opcion C: Fusion Selectiva** despues de analizar las alternativas:

### Matriz de Componentes Seleccionados

| Componente | Origen | Path Real | Uso en Oposiciones |
|------------|--------|-----------|-------------------|
| Memory Store | OPENCLAW-city | `/opt/openclaw-memory/memory_store.py` | Adaptar para flashcards |
| RAG Store | OPENCLAW-city | `/opt/openclaw-memory/rag_store.py` | Busqueda temario |
| Security Pipeline | OPENCLAW-city | `/opt/openclaw-memory/security_pipeline.py` | Validacion inputs |
| Ramiro Bot | OPENCLAW-city | `/opt/openclaw-memory/ramiro_bot.py` | Base Telegram bot |
| Concilio Tri-Agente | OPENCLAW-system | Arquitectura | Coordinacion modulos |
| Sistema Memoria 4 Tipos | OPENCLAW-system | Arquitectura | Contexto estudio |
| Sistema Puertos 1XXYY | JartOS | Arquitectura | Organizacion servicios |
| 15 Tiers | JartOS | Arquitectura | Estructura carpetas |
| CONVENTIONS.md v7.0 | JartOS | `00-FOUNDATION/` | Estandares codigo |
| MiniMax M2.5 API | OPENCLAW-city | Configuracion | Generacion tests/flashcards |
| Mistral Embeddings | OPENCLAW-city | Configuracion | Busqueda semantica |

---

## Objetivo Principal

Crear un **sistema integral de preparacion de oposiciones** que permita:

### Objetivos Primarios

1. **Gestionar el temario de forma inteligente**
   - Ingerir PDFs/DOCX automaticamente
   - Buscar informacion por semantica (RAG Store)
   - Mantener contexto entre sesiones (Memory Store 4 tipos)

2. **Optimizar el repaso con SM-2**
   - Flashcards con repaso espaciado
   - Generacion automatica desde temario (MiniMax M2.5)
   - Seguimiento de progreso

3. **Evaluar el conocimiento**
   - Tests automaticos por tema
   - Diferentes tipos de preguntas
   - Analisis de resultados

4. **Proporcionar insights de IA**
   - Detectar areas debiles
   - Predecir nivel de preparacion
   - Recomendar plan de estudio

### Objetivos Secundarios

5. **Dashboard web intuitivo**
   - Vista general del progreso
   - Gestion de flashcards/tests
   - Calendario de repaso

6. **Bot Telegram (basado en Ramiro)**
   - Extender comandos existentes
   - Flashcards por Telegram
   - Tests rapidos

---

## Alcance

### Incluido (MVP - 6 semanas)

- [x] Ingestion de temario (PDF/DOCX)
- [x] Busqueda semantica (RAG de OPENCLAW-city)
- [x] Flashcards con SM-2
- [x] Generador de tests basicos
- [ ] Dashboard web minimo
- [ ] Metricas de progreso
- [ ] Bot Telegram basico (extender Ramiro)

### Fase 2 (4 semanas adicionales)

- [ ] AI analytics completo
- [ ] Planes de estudio semanales
- [ ] Prediccion de preparacion
- [ ] Recomendaciones diarias
- [ ] Concilio tri-agente para coordinacion

### Fase 3+ (4 semanas adicionales)

- [ ] Asistente de voz (LiveKit)
- [ ] Integracion Telegram completa
- [ ] Mobile app (opcional)

---

## Restricciones

### Tecnicas

- Python 3.11+ (por typing y performance)
- SQLite (heredado de OPENCLAW-city)
- APIs de IA ya configuradas (MiniMax + Mistral)
- Local-first (datos en local, no en nube)

### Presupuesto

- Mistral API: ~$0.0001/1K tokens (embeddings 1024 dims)
- MiniMax M2.5 API: ~$0.001/1K tokens (generacion)
- Estimado mensual: $5-10 para uso personal

### Tiempo

- MVP: 6 semanas
- Fase 2: 4 semanas adicionales
- Fase 3: 4 semanas adicionales

---

**Fin del documento de Contexto (v1.0.0 Integrado)**
