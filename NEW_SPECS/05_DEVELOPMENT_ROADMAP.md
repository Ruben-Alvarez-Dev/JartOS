# 🗺️ ROADMAP DE DESARROLLO (TDD & SDD)

> **REGLA CRÍTICA:** Se prohíbe pasar al siguiente sprint sin que los tests unitarios (`TIER_11_CONTROL/tests/`) del sprint actual pasen al **100%**.

---

## FASE 0: CIMIENTOS (COMPLETADO ✅)

| Sprint | Estado | Descripción |
|--------|--------|-------------|
| 0.1 | ✅ | Estructura 12 TIERs creada |
| 0.2 | ✅ | Código migrado de `src/` a TIERs |
| 0.3 | ✅ | 162 tests pasando |
| 0.4 | ✅ | Historial Git purgado de secretos |
| 0.5 | ✅ | Template 1Password creado |
| 0.6 | ✅ | Force push a GitHub completado |

---

## FASE 1: ROBUSTEZ DEL CONOCIMIENTO (INGESTA)

### Sprint 1.1: Cobertura Temario Store
**Objetivo:** Completar cobertura de tests para `TIER_09_KNOWLEDGE.temario.store`

**Tests a crear:**
```python
# TIER_11_CONTROL/tests/test_temario_store.py
def test_insert_document():
    """Test inserción de documento en temario_documents"""

def test_insert_chunk_with_embedding():
    """Test inserción de chunk con embedding vectorizado"""

def test_query_by_similarity():
    """Test búsqueda por similitud coseno"""

def test_mark_as_verified():
    """Test marcado de chunk como verificado (Golden RAG)"""
```

**Criterio de éxito:** `pytest TIER_11_CONTROL/tests/test_temario_store.py -v` → 100% pass

---

### Sprint 1.2: Watchdog INBOX
**Objetivo:** Crear `TIER_05_INGEST/watchdog_inbox.py`

**Tests primero:**
```python
# TIER_11_CONTROL/tests/test_watchdog_inbox.py
def test_detect_new_pdf(tmp_path):
    """Test detección de nuevo PDF en INBOX"""

def test_process_pdf_calls_parser(mocker):
    """Test que watchdog llama a DocumentParser"""

def test_processed_file_moved(tmp_path):
    """Test que archivo procesado se mueve a /processed"""
```

**Implementación:**
```python
# TIER_05_INGEST/watchdog_inbox.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class INBOXHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(('.pdf', '.docx', '.txt')):
            process_inbox_document(event.src_path)
```

---

### Sprint 1.3: Endpoint Aprobación LAB
**Objetivo:** Crear endpoint `/api/v1/lab/approve` en FastAPI

**Tests primero:**
```python
# TIER_11_CONTROL/tests/test_lab_api.py
def test_approve_endpoint_returns_200(client):
    """Test endpoint responde correctamente"""

def test_approve_triggers_vectorization(mocker, client):
    """Test aprobación dispara vectorización"""

def test_reject_archives_document(mocker, client):
    """Test rechazo archiva documento"""
```

**Implementación:**
```python
# TIER_04_INTERFACE/web/routes/lab.py
@router.post("/approve")
async def approve_document(request: LabApprovalRequest):
    if request.approved:
        await vectorize_and_insert(request.document_id)
        return {"status": "approved", "vectorized": True}
    else:
        archive_document(request.document_id)
        return {"status": "rejected", "archived": True}
```

---

## FASE 2: ANILLO DE SEGURIDAD

### Sprint 2.1: El Guardián
**Objetivo:** Crear `TIER_02_SECURITY/guardian.py` (FastAPI puerto 8080)

**Tests primero:**
```python
# TIER_11_CONTROL/tests/test_guardian.py
def test_guardian_health_check(client):
    """Test /health responde"""

def test_valid_action_approved(client):
    """Test acción válida es aprobada"""

def test_malicious_action_rejected(client):
    """Test acción maliciosa (borrar BD HA) es rechazada"""

def test_guardian_requires_auth(client):
    """Test endpoint requiere token válido"""
```

**Implementación base:**
```python
# TIER_02_SECURITY/guardian.py
from fastapi import FastAPI, HTTPException, Header

app = FastAPI(title="El Guardián")

ALLOWED_ACTIONS = [
    "home_assistant_call",
    "notification_send",
    "calendar_event_create"
]

BLOCKED_PATTERNS = [
    "delete", "drop", "rm", "format",
    "homeassistant/config", "database"
]

@app.post("/propose_action")
async def propose_action(
    request: ActionRequest,
    authorization: str = Header(None)
):
    if not validate_token(authorization):
        raise HTTPException(401, "Unauthorized")

    if any(p in str(request).lower() for p in BLOCKED_PATTERNS):
        return {"approved": False, "reason": "Action blocked by policy"}

    # Ejecutar acción válida
    result = await execute_safe_action(request)
    return {"approved": True, "executed": True, "result": result}
```

---

### Sprint 2.2: Tests de Seguridad
**Objetivo:** Tests de peticiones maliciosas

**Casos de prueba:**
- Intento de borrar BD de Home Assistant
- Intento de acceder a credenciales
- Intento de ejecutar comandos shell
- Intento de modificar configuración del sistema
- SQL injection en parámetros
- Path traversal en rutas de archivos

---

### Sprint 2.3: Webhook Home Assistant
**Objetivo:** Integrar webhook real hacia n8n/Home Assistant

**Flujo:**
```
JartOS propone acción
    → Guardián valida
    → Si aprobado: POST a Home Assistant API
    → Log de ejecución en Daemon
```

---

## FASE 3: CEREBRO Y CONCILIO

### Sprint 3.1: Concilio Real
**Objetivo:** Implementar clase `Concilio` con 3 llamadas LLM reales

**Tests primero:**
```python
# TIER_11_CONTROL/tests/test_concilio.py
@pytest.mark.asyncio
async def test_concilio_returns_three_votes():
    """Test Concilio retorna exactamente 3 votos"""

async def test_concilio_3_3_approves():
    """Test 3/3 APTO aprueba documento"""

async def test_concilio_2_3_rejects():
    """Test 2/3 APTO rechaza con feedback"""

async def test_concilio_handles_llm_error(mocker):
    """Test manejo de error en llamada LLM"""
```

---

### Sprint 3.2: Integración Maestro-Concilio
**Objetivo:** Integrar Concilio en flujo del Maestro

**Flujo:**
```
Maestro recibe objetivo
    → Delega a Especialista
    → Especialista genera documento
    → Maestro envía a Concilio
    → Si aprobado: guardar en Golden RAG
    → Si rechazado: devolver a Especialista con feedback
```

---

### Sprint 3.3: Test de Integración Completo
**Objetivo:** Test end-to-end del flujo completo

**Test:**
```python
@pytest.mark.integration
async def test_full_flow_maestro_to_golden_rag():
    """Test flujo completo: objetivo → documento → concilio → golden rag"""

    # 1. Enviar objetivo al Maestro
    response = await client.post("/api/v1/orchestrator/task", json={
        "objective": "Crear Programación Didáctica para GS Restauración"
    })

    # 2. Verificar que se delegó al Redactor
    assert response.json()["delegated_to"] == "redactor_didactico"

    # 3. Esperar documento generado
    document = await wait_for_document(response.json()["task_id"])

    # 4. Verificar validación del Concilio
    assert document["concilio_approved"] == True

    # 5. Verificar guardado en Golden RAG
    golden_doc = await query_golden_rag(document["id"])
    assert golden_doc is not None
```

---

## FASE 4: MULTIMODALIDAD

### Sprint 4.1: Web Dashboard
**Objetivo:** Dashboard FastAPI que muestre progreso y flashcards

**Features:**
- Panel de estado del sistema
- Progreso de tests
- Flashcards interactivas
- Histórico de documentos generados

---

### Sprint 4.2: Voice Agent (Coach Oral)
**Objetivo:** Activar `voice_agent_worker.py` con LiveKit

**Features:**
- Simulacro de exposición oral
- Temporizador de 10-15 minutos
- Detección de muletillas
- Feedback de velocidad y tono

---

## MÉTRICAS DE PROGRESO

| Métrica | Meta | Actual |
|---------|------|--------|
| Tests unitarios | >200 | 162 |
| Cobertura código | >80% | ~60% |
| Documentos en Golden RAG | >100 | 0 |
| Especialistas activos | 4 | 0 |
| Concilio operativo | Sí | No |

---

## PRÓXIMO SPRINT

**Sprint 1.1: Cobertura Temario Store**

```bash
# Comandos a ejecutar
cd /Users/ruben/JartOS
pytest TIER_11_CONTROL/tests/test_temario_store.py -v --cov=TIER_09_KNOWLEDGE.temario.store
```
