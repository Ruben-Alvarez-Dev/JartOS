# 🗺️ ROADMAP DE DESARROLLO (TDD & SDD)

Este roadmap es nuestra guía paso a paso. Se prohíbe pasar al siguiente sprint sin que los tests unitarios (`TIER_11_CONTROL/tests/`) del sprint actual pasen al 100%.

## [Fase 1] - Robustez del Conocimiento (INGESTA)
- [ ] **Sprint 1.1:** Completar cobertura de tests para `TIER_09_KNOWLEDGE.temario.store`. Validar inserción de embeddings reales.
- [ ] **Sprint 1.2:** Crear `TIER_05_INGEST/watchdog.py`. Escribir su test con directorios temporales, y luego su lógica.
- [ ] **Sprint 1.3:** Crear el endpoint de "Aprobación de LAB" en `TIER_04_INTERFACE/web/routes/`.

## [Fase 2] - Anillo de Seguridad
- [ ] **Sprint 2.1:** Crear `TIER_02_SECURITY/guardian.py` (FastAPI en puerto 8080).
- [ ] **Sprint 2.2:** Crear test unitario simulando peticiones maliciosas (ej. borrar BD de Home Assistant). Deben ser rechazadas.
- [ ] **Sprint 2.3:** Integrar webhook real hacia n8n/Home Assistant.

## [Fase 3] - Cerebro y Concilio
- [ ] **Sprint 3.1:** Implementar la clase real de `Concilio` (`TIER_03_AGENTS/concilio.py`) que haga 3 llamadas LLM usando la librería `openai` o `httpx`.
- [ ] **Sprint 3.2:** Integrar el Concilio en el flujo del Maestro.
- [ ] **Sprint 3.3:** Test de Integración: Maestro -> Genera Doc -> Concilio Rechaza -> Maestro Corrige.

## [Fase 4] - Multimodalidad
- [ ] **Sprint 4.1:** Consolidar el Web Dashboard (`TIER_04_INTERFACE`) para que muestre el progreso de los tests y flashcards visualmente.
- [ ] **Sprint 4.2:** Activar el `voice_agent_worker.py` (LiveKit) con el System Prompt del "Coach Oral".