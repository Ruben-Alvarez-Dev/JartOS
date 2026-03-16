# Roadmap de Implementacion

**Version:** 0.1.0
**Ultima actualizacion:** 2025-03-16

---

## Indice

1. [Vision General](#1-vision-general)
2. [Fase 1: Fundacion (Sprint 1-2)](#2-fase-1-fundacion-sprint-1-2)
3. [Fase 2: Temario Core (Sprint 3-4)](#3-fase-2-temario-core-sprint-3-4)
4. [Fase 3: Flashcards SM-2 (Sprint 5-6)](#4-fase-3-flashcards-sm-2-sprint-5-6)
5. [Fase 4: Tests y Evaluacion (Sprint 7-8)](#5-fase-4-tests-y-evaluacion-sprint-7-8)
6. [Fase 5: AI Analytics (Sprint 9-10)](#6-fase-5-ai-analytics-sprint-9-10)
7. [Fase 6: Dashboard Web (Sprint 11-12)](#7-fase-6-dashboard-web-sprint-11-12)
8. [Metricas de Exito](#8-metricas-de-exito)
9. [Gestion de Riesgos](#9-gestion-de-riesgos)

---

## 1. Vision General

### Cronograma Total

```
+============================================================================+
|                         ROADMAP OPOSICIONES-SYSTEM                          |
+============================================================================+
|                                                                            |
|  SEMANA:   1   2   3   4   5   6   7   8   9  10  11  12                   |
|            |---|---|---|---|---|---|---|---|---|---|---|                    |
|                                                                            |
|  FASE 1:   [========]                                                      |
|  Fundacion                                                                  |
|                                                                            |
|  FASE 2:           [========]                                              |
|  Temario Core                                                               |
|                                                                            |
|  FASE 3:                   [========]                                      |
|  Flashcards SM-2                                                            |
|                                                                            |
|  FASE 4:                           [========]                              |
|  Tests y Evaluacion                                                        |
|                                                                            |
|  FASE 5:                                   [========]                      |
|  AI Analytics                                                               |
|                                                                            |
|  FASE 6:                                           [========]              |
|  Dashboard Web                                                              |
|                                                                            |
+============================================================================+
|                                                                            |
|  MVP RELEASE: Fin de Fase 4 (Semana 8)                                     |
|  v1.0 RELEASE: Fin de Fase 6 (Semana 12)                                   |
|                                                                            |
+============================================================================+
```

### Dependencias entre Fases

```
+------------+      +------------+      +------------+
|   FASE 1   |----->|   FASE 2   |----->|   FASE 3   |
| Fundacion  |      |Temario Core|      |Flashcards  |
+------------+      +------------+      +------------+
                           |                   |
                           v                   v
                    +------------+      +------------+
                    |   FASE 4   |      |   FASE 5   |
                    |   Tests    |----->|AI Analytics|
                    +------------+      +------------+
                           |                   |
                           +--------+----------+
                                    |
                                    v
                             +------------+
                             |   FASE 6   |
                             |  Dashboard |
                             +------------+
```

---

## 2. Fase 1: Fundacion (Sprint 1-2)

**Duracion:** 2 semanas
**Objetivo:** Establecer la infraestructura base del proyecto

### 2.1 Checklist de Tareas

#### Sprint 1: Setup Inicial

| ID | Tarea | Prioridad | Estimacion | Dependencias |
|----|-------|-----------|------------|--------------|
| F1-001 | Crear estructura de carpetas | Alta | 2h | - |
| F1-002 | Inicializar repositorio Git | Alta | 0.5h | F1-001 |
| F1-003 | Configurar .gitignore | Alta | 0.5h | F1-002 |
| F1-004 | Crear pyproject.toml | Alta | 1h | F1-001 |
| F1-005 | Configurar virtual environment | Alta | 0.5h | F1-004 |
| F1-006 | Instalar dependencias core | Alta | 1h | F1-005 |
| F1-007 | Configurar linter (ruff) | Media | 0.5h | F1-006 |
| F1-008 | Configurar formatter (black) | Media | 0.5h | F1-006 |
| F1-009 | Crear archivo .env.example | Alta | 0.5h | F1-001 |
| F1-010 | Documentar en README.md | Media | 1h | F1-002 |

#### Sprint 2: Infraestructura

| ID | Tarea | Prioridad | Estimacion | Dependencias |
|----|-------|-----------|------------|--------------|
| F1-011 | Crear modulo de configuracion (YAML) | Alta | 3h | F1-006 |
| F1-012 | Implementar logging basico | Alta | 2h | F1-006 |
| F1-013 | Crear esquema de base de datos (temario.db) | Alta | 3h | F1-006 |
| F1-014 | Crear esquema de base de datos (oposiciones.db) | Alta | 3h | F1-013 |
| F1-015 | Implementar conexion SQLite | Alta | 2h | F1-013, F1-014 |
| F1-016 | Crear tests de conexion DB | Media | 1h | F1-015 |
| F1-017 | Configurar pytest | Alta | 1h | F1-006 |
| F1-018 | Crear conftest.py con fixtures | Media | 2h | F1-017 |
| F1-019 | Configurar CI basico (GitHub Actions) | Baja | 2h | F1-017 |
| F1-020 | Obtener API keys (Mistral, MiniMax) | Alta | 1h | - |

### 2.2 Entregables

- [ ] Estructura de proyecto completa
- [ ] Entorno de desarrollo configurado
- [ ] Bases de datos creadas (vacías)
- [ ] Tests ejecutándose (aunque sea vacíos)
- [ ] CI pipeline básico

### 2.3 Dependencias Externas

| Dependencia | Tipo | Proveedor |
|-------------|------|-----------|
| MISTRAL_API_KEY | API Key | https://console.mistral.ai |
| MINIMAX_API_KEY | API Key | https://www.minimaxi.com |
| MINIMAX_GROUP_ID | API Key | https://www.minimaxi.com |

### 2.4 Criterios de Aceptacion

- [ ] `pytest` ejecuta sin errores
- [ ] Las bases de datos se crean correctamente
- [ ] El logging funciona y escribe a archivo
- [ ] La configuracion se carga desde YAML

---

## 3. Fase 2: Temario Core (Sprint 3-4)

**Duracion:** 2 semanas
**Objetivo:** Implementar ingestion y busqueda de temario

### 3.1 Checklist de Tareas

#### Sprint 3: Parsing y Chunking

| ID | Tarea | Prioridad | Estimacion | Dependencias |
|----|-------|-----------|------------|--------------|
| F2-001 | Implementar PDF parser (PyMuPDF) | Alta | 4h | F1-015 |
| F2-002 | Implementar DOCX parser | Alta | 3h | F1-015 |
| F2-003 | Crear modelo Document | Alta | 1h | F1-013 |
| F2-004 | Crear modelo Chunk | Alta | 1h | F1-013 |
| F2-005 | Implementar chunker por tokens | Alta | 4h | F2-004 |
| F2-006 | Implementar deteccion de metadata | Media | 2h | F2-001 |
| F2-007 | Crear store.py para documentos | Alta | 3h | F2-003 |
| F2-008 | Tests de parser | Alta | 2h | F2-001, F2-002 |
| F2-009 | Tests de chunker | Alta | 2h | F2-005 |
| F2-010 | Tests de store | Alta | 2h | F2-007 |

#### Sprint 4: Embeddings y Busqueda

| ID | Tarea | Prioridad | Estimacion | Dependencias |
|----|-------|-----------|------------|--------------|
| F2-011 | Implementar Mistral embedder | Alta | 4h | F1-020 |
| F2-012 | Implementar batch embedding | Alta | 2h | F2-011 |
| F2-013 | Crear modelo SearchResult | Alta | 1h | F2-004 |
| F2-014 | Implementar searcher (cosine similarity) | Alta | 4h | F2-012 |
| F2-015 | Implementar almacenamiento de embeddings | Alta | 2h | F2-012 |
| F2-016 | Implementar orquestador ingest.py | Alta | 3h | F2-007, F2-012 |
| F2-017 | Implementar QA con LLM | Media | 3h | F2-014 |
| F2-018 | Tests de embedder | Alta | 2h | F2-011 |
| F2-019 | Tests de searcher | Alta | 2h | F2-014 |
| F2-020 | Crear CLI de temario | Alta | 3h | F2-016 |

### 3.2 Entregables

- [ ] Modulo temario completo
- [ ] CLI funcional para ingest y search
- [ ] Tests con >80% cobertura
- [ ] Documentacion de API

### 3.3 Dependencias

- **Fase 1 completada**: Base de datos y configuracion
- **API Keys**: Mistral API key activa

### 3.4 Criterios de Aceptacion

- [ ] `python -m src.temario.cli ingest doc.pdf` funciona
- [ ] `python -m src.temario.cli search "query"` retorna resultados
- [ ] Los chunks se almacenan con embeddings
- [ ] La busqueda semantica retorna resultados relevantes

---

## 4. Fase 3: Flashcards SM-2 (Sprint 5-6)

**Duracion:** 2 semanas
**Objetivo:** Sistema de flashcards con repaso espaciado

### 4.1 Checklist de Tareas

#### Sprint 5: Modelos y Generacion

| ID | Tarea | Prioridad | Estimacion | Dependencias |
|----|-------|-----------|------------|--------------|
| F3-001 | Crear modelo Deck | Alta | 1h | F1-014 |
| F3-002 | Crear modelo Flashcard | Alta | 1h | F1-014 |
| F3-003 | Crear modelo ReviewLog | Alta | 1h | F1-014 |
| F3-004 | Implementar store de flashcards | Alta | 3h | F3-001, F3-002 |
| F3-005 | Implementar generador con IA | Alta | 4h | F2-014 |
| F3-006 | Crear prompt templates | Alta | 2h | F3-005 |
| F3-007 | Tests de modelos | Alta | 1h | F3-001, F3-002 |
| F3-008 | Tests de store | Alta | 2h | F3-004 |
| F3-009 | Tests de generador | Alta | 2h | F3-005 |
| F3-010 | Integracion con MiniMax | Alta | 2h | F3-005 |

#### Sprint 6: SM-2 y Review

| ID | Tarea | Prioridad | Estimacion | Dependencias |
|----|-------|-----------|------------|--------------|
| F3-011 | Implementar algoritmo SM-2 | Alta | 4h | F3-002 |
| F3-012 | Implementar scheduler | Alta | 3h | F3-011 |
| F3-013 | Implementar reviewer | Alta | 3h | F3-012 |
| F3-014 | Implementar estadisticas de deck | Media | 2h | F3-004 |
| F3-015 | Crear CLI de flashcards | Alta | 3h | F3-013 |
| F3-016 | Tests de SM-2 | Alta | 2h | F3-011 |
| F3-017 | Tests de scheduler | Alta | 2h | F3-012 |
| F3-018 | Tests de reviewer | Alta | 2h | F3-013 |
| F3-019 | Integracion con temario | Alta | 2h | F3-005, F2-016 |
| F3-020 | Documentacion de uso | Media | 1h | F3-015 |

### 4.2 Entregables

- [ ] Modulo flashcards completo
- [ ] CLI funcional para crear, listar, repasar
- [ ] Algoritmo SM-2 implementado
- [ ] Tests con >80% cobertura

### 4.3 Dependencias

- **Fase 2 completada**: Temario disponible
- **API Keys**: MiniMax API key activa

### 4.4 Criterios de Aceptacion

- [ ] `python -m src.flashcards.cli create-deck "Tema 1"` funciona
- [ ] `python -m src.flashcards.cli generate --deck 1 --tema 1` funciona
- [ ] `python -m src.flashcards.cli review --deck 1` funciona
- [ ] El SM-2 actualiza intervalos correctamente

---

## 5. Fase 4: Tests y Evaluacion (Sprint 7-8)

**Duracion:** 2 semanas
**Objetivo:** Sistema de generacion y evaluacion de tests

### 5.1 Checklist de Tareas

#### Sprint 7: Generacion de Tests

| ID | Tarea | Prioridad | Estimacion | Dependencias |
|----|-------|-----------|------------|--------------|
| F4-001 | Crear modelo Test | Alta | 1h | F1-014 |
| F4-002 | Crear modelo Question | Alta | 1h | F1-014 |
| F4-003 | Crear modelo TestSession | Alta | 1h | F1-014 |
| F4-004 | Implementar store de tests | Alta | 3h | F4-001, F4-002 |
| F4-005 | Implementar generador de preguntas | Alta | 4h | F2-014 |
| F4-006 | Implementar tipos de preguntas | Alta | 3h | F4-005 |
|   | - Multiple choice | | | |
|   | - Verdadero/Falso | | | |
|   | - Pregunta abierta | | | |
| F4-007 | Crear prompt templates para preguntas | Alta | 2h | F4-005 |
| F4-008 | Tests de modelos | Alta | 1h | F4-001, F4-002 |
| F4-009 | Tests de store | Alta | 2h | F4-004 |
| F4-010 | Tests de generador | Alta | 2h | F4-005 |

#### Sprint 8: Evaluacion y Analisis

| ID | Tarea | Prioridad | Estimacion | Dependencias |
|----|-------|-----------|------------|--------------|
| F4-011 | Implementar solver de tests | Alta | 3h | F4-003 |
| F4-012 | Implementar evaluador de respuestas | Alta | 3h | F4-011 |
| F4-013 | Implementar analizador de resultados | Alta | 4h | F4-012 |
| F4-014 | Crear deteccion de areas debiles | Alta | 3h | F4-013 |
| F4-015 | Crear CLI de tests | Alta | 3h | F4-011 |
| F4-016 | Tests de solver | Alta | 2h | F4-011 |
| F4-017 | Tests de evaluador | Alta | 2h | F4-012 |
| F4-018 | Tests de analizador | Alta | 2h | F4-013 |
| F4-019 | Integracion con flashcards | Media | 2h | F4-014, F3-011 |
| F4-020 | MVP Release preparation | Alta | 3h | - |

### 5.2 Entregables

- [ ] Modulo tests completo
- [ ] CLI funcional para crear, ejecutar, evaluar tests
- [ ] Deteccion de areas debiles
- [ ] **MVP RELEASE**

### 5.3 Dependencias

- **Fase 2 completada**: Temario disponible
- **Fase 3 completada**: Flashcards disponible (opcional)
- **API Keys**: MiniMax API key activa

### 5.4 Criterios de Aceptacion

- [ ] `python -m src.tests.cli create --tema 1 --questions 10` funciona
- [ ] `python -m src.tests.cli take --test 1` funciona
- [ ] `python -m src.tests.cli results --session 1` funciona
- [ ] El analizador detecta areas debiles

---

## 6. Fase 5: AI Analytics (Sprint 9-10)

**Duracion:** 2 semanas
**Objetivo:** Sistema de analisis predictivo y recomendaciones

### 6.1 Checklist de Tareas

#### Sprint 9: Analisis y Prediccion

| ID | Tarea | Prioridad | Estimacion | Dependencias |
|----|-------|-----------|------------|--------------|
| F5-001 | Crear modelo WeakArea | Alta | 1h | F1-014 |
| F5-002 | Crear modelo StudyPlan | Alta | 1h | F1-014 |
| F5-003 | Crear modelo DailyRecommendation | Alta | 1h | F1-014 |
| F5-004 | Implementar store de analytics | Alta | 3h | F5-001 |
| F5-005 | Implementar analyzer de areas debiles | Alta | 4h | F4-014, F3-011 |
| F5-006 | Implementar predictor de preparacion | Alta | 4h | F5-005 |
| F5-007 | Crear algoritmo de scoring | Alta | 3h | F5-006 |
| F5-008 | Tests de modelos | Alta | 1h | F5-001, F5-002 |
| F5-009 | Tests de analyzer | Alta | 2h | F5-005 |
| F5-010 | Tests de predictor | Alta | 2h | F5-006 |

#### Sprint 10: Planes y Recomendaciones

| ID | Tarea | Prioridad | Estimacion | Dependencias |
|----|-------|-----------|------------|--------------|
| F5-011 | Implementar planner semanal | Alta | 4h | F5-005 |
| F5-012 | Implementar recomendador diario | Alta | 3h | F5-011 |
| F5-013 | Crear templates de planes | Media | 2h | F5-011 |
| F5-014 | Implementar sistema de prioridades | Media | 2h | F5-012 |
| F5-015 | Crear CLI de AI | Alta | 3h | F5-012 |
| F5-016 | Tests de planner | Alta | 2h | F5-011 |
| F5-017 | Tests de recomendador | Alta | 2h | F5-012 |
| F5-018 | Integracion completa | Alta | 3h | F5-005, F5-011, F5-012 |
| F5-019 | Calibracion de algoritmos | Media | 4h | F5-018 |
| F5-020 | Documentacion de AI | Media | 2h | F5-015 |

### 6.2 Entregables

- [ ] Modulo AI completo
- [ ] Prediccion de preparacion
- [ ] Planes de estudio semanales
- [ ] Recomendaciones diarias

### 6.3 Dependencias

- **Fase 3 completada**: Datos de flashcards
- **Fase 4 completada**: Datos de tests

### 6.4 Criterios de Aceptacion

- [ ] `python -m src.ai.cli analyze` muestra areas debiles
- [ ] `python -m src.ai.cli predict` muestra prediccion
- [ ] `python -m src.ai.cli plan --week` genera plan semanal
- [ ] `python -m src.ai.cli recommend` muestra recomendaciones del dia

---

## 7. Fase 6: Dashboard Web (Sprint 11-12)

**Duracion:** 2 semanas
**Objetivo:** Interfaz web completa

### 7.1 Checklist de Tareas

#### Sprint 11: Backend y API

| ID | Tarea | Prioridad | Estimacion | Dependencias |
|----|-------|-----------|------------|--------------|
| F6-001 | Crear aplicacion FastAPI | Alta | 2h | F1-006 |
| F6-002 | Implementar rutas de temario | Alta | 3h | F2-016 |
| F6-003 | Implementar rutas de flashcards | Alta | 3h | F3-013 |
| F6-004 | Implementar rutas de tests | Alta | 3h | F4-011 |
| F6-005 | Implementar rutas de dashboard | Alta | 3h | F5-012 |
| F6-006 | Crear modelos Pydantic | Alta | 2h | F6-001 |
| F6-007 | Implementar manejo de errores | Alta | 2h | F6-001 |
| F6-008 | Implementar validacion | Alta | 2h | F6-006 |
| F6-009 | Tests de API endpoints | Alta | 3h | F6-002, F6-003, F6-004 |
| F6-010 | Documentacion OpenAPI | Media | 1h | F6-001 |

#### Sprint 12: Frontend y Deploy

| ID | Tarea | Prioridad | Estimacion | Dependencias |
|----|-------|-----------|------------|--------------|
| F6-011 | Crear templates Jinja2 base | Alta | 2h | F6-001 |
| F6-012 | Implementar pagina dashboard | Alta | 4h | F6-011 |
| F6-013 | Implementar pagina flashcards | Alta | 4h | F6-011 |
| F6-014 | Implementar pagina tests | Alta | 4h | F6-011 |
| F6-015 | Implementar pagina temario | Alta | 3h | F6-011 |
| F6-016 | Anadir Tailwind CSS | Media | 2h | F6-011 |
| F6-017 | Anadir Alpine.js para interactividad | Media | 3h | F6-011 |
| F6-018 | Tests de integracion web | Alta | 3h | F6-012 |
| F6-019 | Configurar Docker (opcional) | Baja | 3h | F6-001 |
| F6-020 | **v1.0 RELEASE** | Alta | 2h | - |

### 7.2 Entregables

- [ ] Web dashboard funcional
- [ ] API REST documentada
- [ ] Tests de integracion
- [ ] **v1.0 RELEASE**

### 7.3 Dependencias

- **Fases 1-5 completadas**: Todos los modulos
- **FastAPI**: pip install fastapi uvicorn

### 7.4 Criterios de Aceptacion

- [ ] `python scripts/run_web.py` inicia el servidor
- [ ] El dashboard muestra metricas agregadas
- [ ] Se pueden gestionar flashcards desde la web
- [ ] Se pueden crear y ejecutar tests desde la web

---

## 8. Metricas de Exito

### 8.1 Metricas por Fase

| Fase | Metrica | Target | Medicion |
|------|---------|--------|----------|
| 1 | Tiempo de setup | <4h | Tiempo real |
| 2 | Chunks/documento | 50-100 | Promedio |
| 2 | Tiempo de ingestion | <60s/doc | Benchmark |
| 2 | Precision de busqueda | >80% | Evaluacion manual |
| 3 | Flashcards generadas | 10-20/tema | Conteo |
| 3 | Tiempo de repaso | <15min/dia | Tracking |
| 4 | Tests generados | >5/tema | Conteo |
| 4 | Cobertura de tests | >80% | pytest-cov |
| 5 | Precision prediccion | >70% | Validacion |
| 6 | Latencia API | <500ms | Benchmark |

### 8.2 Metricas Globales

| Metrica | Target MVP | Target v1.0 |
|---------|------------|-------------|
| Cobertura de codigo | >70% | >80% |
| Tiempo de ejecucion tests | <60s | <60s |
| Documentacion completa | 80% | 100% |
| Bugs criticos | 0 | 0 |
| Features implementadas | 60% | 100% |

### 8.3 Health Checks

```bash
# Verificar que todo funciona
pytest --cov=src --cov-report=term-missing

# Verificar linting
ruff check src/

# Verificar formateo
black --check src/

# Verificar tipos (si se usa mypy)
mypy src/
```

---

## 9. Gestion de Riesgos

### 9.1 Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigacion | Contingencia |
|--------|--------------|---------|------------|--------------|
| API de IA no disponible | Media | Alto | Retry con backoff | Usar Ollama local |
| Costo de APIs excesivo | Media | Alto | Monitorear uso | Limitar llamadas |
| Tiempo de desarrollo excedido | Alta | Medio | MVP minimalista | Cortar features |
| Calidad de embeddings baja | Baja | Alto | Probar modelos | Cambiar proveedor |
| Datos de temario no disponibles | Baja | Alto | Usar PDFs publicos | Crear contenido dummy |

### 9.2 Plan de Contingencia

**Escenario: APIs de IA no disponibles**

```
1. Implementar Ollama como fallback
2. Reducir funcionalidad de IA
3. Usar embeddings locales (sentence-transformers)
4. Priorizar features sin IA
```

**Escenario: Tiempo excedido**

```
1. Cortar Fase 5 (AI Analytics)
2. Simplificar Dashboard Web
3. Mantener solo CLI para MVP
4. Posponer a v1.1
```

### 9.3 Puntos de Decision

| Semana | Decision | Criterio |
|--------|----------|----------|
| 4 | Continuar con AI? | APIs funcionando + presupuesto OK |
| 8 | Release MVP? | Features core funcionando |
| 10 | Incluir Dashboard? | Tiempo disponible + estabilidad |

---

## 10. Sprints Detallados

### Sprint Template

```
SPRINT X: [Nombre]
Duracion: 2 semanas

Objetivos:
- [ ] Objetivo 1
- [ ] Objetivo 2

Tareas:
- [ ] Tarea 1 (Xh)
- [ ] Tarea 2 (Xh)

Bloqueadores:
- [ ] Bloqueador 1

Notas:
- Nota importante
```

### Sprint 1-2: Fundacion

**Objetivo:** Proyecto listo para desarrollo

**Definition of Done:**
- [ ] Todos los tests pasan
- [ ] Codigo formateado y linted
- [ ] Documentacion actualizada
- [ ] Commit en main branch

### Sprint 3-4: Temario Core

**Objetivo:** Ingestion y busqueda funcionales

**Definition of Done:**
- [ ] `temario ingest` funciona
- [ ] `temario search` funciona
- [ ] Tests >80% cobertura
- [ ] Un documento de prueba ingresado

### Sprint 5-6: Flashcards

**Objetivo:** Sistema de flashcards completo

**Definition of Done:**
- [ ] Crear deck desde CLI
- [ ] Generar flashcards con IA
- [ ] Repasar con SM-2
- [ ] Tests >80% cobertura

### Sprint 7-8: Tests (MVP)

**Objetivo:** Sistema de evaluacion + MVP Release

**Definition of Done:**
- [ ] Crear test desde CLI
- [ ] Ejecutar test
- [ ] Ver resultados
- [ ] Deteccion de areas debiles
- [ ] **MVP RELEASE TAG**

### Sprint 9-10: AI Analytics

**Objetivo:** Insights inteligentes

**Definition of Done:**
- [ ] Analisis de areas debiles
- [ ] Prediccion de preparacion
- [ ] Planes semanales
- [ ] Recomendaciones diarias

### Sprint 11-12: Dashboard (v1.0)

**Objetivo:** Interfaz web + v1.0 Release

**Definition of Done:**
- [ ] Dashboard web funcional
- [ ] API REST documentada
- [ ] Tests de integracion
- [ ] **v1.0 RELEASE TAG**

---

**Fin del documento de Roadmap**
