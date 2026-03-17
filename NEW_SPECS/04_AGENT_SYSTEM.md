# 🤖 SISTEMA DE AGENTES

## 1. Arquitectura Jerárquica

JartOS implementa un **sistema de gobierno de 3 poderes**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PODER EJECUTIVO                              │
│                    EL MAESTRO (Orquestador)                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  - Recibe objetivos del usuario                           │  │
│  │  - Desglosa tareas complejas                              │  │
│  │  - Delega a especialistas                                 │  │
│  │  - Coordina flujos de trabajo                             │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PODER LEGISLATIVO/OPERATIVO                  │
│                    ESPECIALISTAS (Ejecutores)                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │ REDACTOR    │ │INVESTIGADOR │ │ COACH ORAL  │ │  GESTOR   │ │
│  │ DIDÁCTICO   │ │  NORMATIVO  │ │  MULTIMODAL │ │  DE VIDA  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PODER JUDICIAL                               │
│                    EL CONCILIO (Control de Calidad)             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ REVISOR     │ │ REVISOR     │ │ REVISOR     │              │
│  │  JURÍDICO   │ │ PEDAGÓGICO  │ │  TÉCNICO    │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│                                                                 │
│  REGLA: 3/3 votos APTO requeridos para aprobar                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. El Maestro (Orquestador Principal)

### Especificación
| Aspecto | Valor |
|---------|-------|
| **Framework** | FastMCP (Model Context Protocol) |
| **Puerto** | `18789` |
| **Ubicación** | `TIER_03_AGENTS/maestro_orchestrator.py` |

### Herramientas MCP Registradas
```python
@mcp.tool()
def delegate_to_specialist(specialist_id: str, task: dict) -> dict:
    """Delega una tarea a un especialista específico."""
    pass

@mcp.tool()
def query_temario(query_string: str) -> list:
    """Consulta la base de conocimiento (Golden RAG)."""
    pass

@mcp.tool()
def request_concilio_validation(document: dict) -> dict:
    """Solicita validación del Concilio para un documento."""
    pass

@mcp.tool()
def propose_action(action: str, params: dict) -> dict:
    """Propone una acción al Guardián (Home Assistant, etc.)."""
    pass
```

### Personalidad del Maestro
```
Rol: "Jefe de Gabinete" del sistema
Personalidad: Analítico, ordenado, directivo pero servicial
Funciones:
  - Gestión de agenda (Google Calendar)
  - Time Blocking inteligente
  - Enrutamiento de tareas a especialistas
  - Monitorización proactiva de fechas límite
  - Visión holística: equilibra estudio, trabajo, vida personal
```

---

## 3. Especialistas

### A-01: Redactor Didáctico
| Aspecto | Descripción |
|---------|-------------|
| **Rol** | Especialista en pedagogía y redacción técnica |
| **Funciones** | Programaciones Didácticas, Unidades Didácticas, exámenes, flashcards |
| **Estilo** | Lenguaje técnico-pedagógico, formal, jerga oficial FP |
| **Herramientas** | Plantillas, Qdrant, normativa curricular |

**Prompt base:** `TIER_00_FOUNDATION/prompts/redactor_didactico.prompt`

### A-02: Investigador Normativo
| Aspecto | Descripción |
|---------|-------------|
| **Rol** | Analista de datos y buscador de información |
| **Funciones** | Investigación legislativa, síntesis de documentación, esquemas |
| **Herramientas** | Web Browsing (controlado), lectura PDFs, BOE |

**Prompt base:** `TIER_00_FOUNDATION/prompts/investigador_normativo.prompt`

### A-03: Coach Oral (Multimodal)
| Aspecto | Descripción |
|---------|-------------|
| **Rol** | Preparador de pruebas orales y prácticas |
| **Funciones** | Simulacros de defensa, análisis comunicación no verbal, feedback voz |
| **Hardware** | Logitech Brio 4K (video), Mikro Anker 360 (audio) |
| **Tecnología** | LiveKit, STT/TTS |

**Prompt base:** `TIER_00_FOUNDATION/prompts/coach_oral.prompt`

**Capacidades específicas:**
- Temporizador de exposición (10-15 min)
- Detección de muletillas ("ehh", "bueno", "pues")
- Análisis de velocidad de habla
- Feedback de comunicación no verbal (cámara)

### A-04: Gestor de Vida
| Aspecto | Descripción |
|---------|-------------|
| **Rol** | Soporte para gestión personal |
| **Funciones** | Agenda, dieta, ejercicio, sueño, rutinas |
| **Herramientas** | Home Assistant (vía Guardián), Calendar |

**Prompt base:** `TIER_00_FOUNDATION/prompts/gestor_vida.prompt`

---

## 4. El Concilio (Control de Calidad)

### Especificación
| Aspecto | Valor |
|---------|-------|
| **Ubicación** | `TIER_03_AGENTS/concilio.py` |
| **Mecanismo** | 3 llamadas LLM concurrentes |
| **Regla** | **3/3 votos APTO** requeridos |

### Los Tres Revisores

| Revisor | Archivo Prompt | Verifica |
|---------|----------------|----------|
| **Jurídico** | `prompt_juridico.md` | Citas legales (LOE, FP), normativa |
| **Pedagógico** | `prompt_pedagogico.md` | Alineación RA/CE, metodología |
| **Técnico** | `prompt_tecnico.md` | Veracidad técnica en hostelería |

### Flujo de Validación
```python
def validate_content(document: dict) -> dict:
    """
    Valida un documento mediante los 3 revisores del Concilio.
    Retorna: {"approved": bool, "votes": [...], "feedback": str}
    """
    results = await asyncio.gather(
        llm_call(PROMPT_JURIDICO, document),
        llm_call(PROMPT_PEDAGOGICO, document),
        llm_call(PROMPT_TECNICO, document)
    )

    votes = [r["apto"] for r in results]

    if all(votes):  # 3/3 APTO
        return {"approved": True, "votes": results}
    else:
        feedback = [r["feedback"] for r in results if not r["apto"]]
        return {"approved": False, "votes": results, "feedback": feedback}
```

### Respuesta de Rechazo
```json
{
  "approved": false,
  "votes": [
    {"revisor": "juridico", "apto": true},
    {"revisor": "pedagogico", "apto": false, "feedback": "Falta citar el RA 3.2"},
    {"revisor": "tecnico", "apto": true}
  ],
  "feedback": "Revisar RA 3.2 según currículo TODOFP"
}
```

---

## 5. El Daemon (Supervisor)

### Especificación
| Aspecto | Valor |
|---------|-------|
| **Ubicación** | `TIER_11_CONTROL/daemon.py` |
| **Tipo** | Proceso background (systemd) |

### Funciones
1. **Logging de decisiones:** Todas las acciones de agentes
2. **Detección de deriva:** Alertas si un agente alucina
3. **Control de versiones atómico:** Snapshots automáticos
4. **Salud del sistema:** Monitorización de servicios

### Formato de Log
```
[2026-03-17 14:32:15] 🤖 AGENT: Maestro recibió objetivo "crear programación didáctica"
[2026-03-17 14:32:18] 📤 DELEGATE: Maestro → Redactor (task_id: t_001)
[2026-03-17 14:35:42] 📥 RESULT: Redactor completó documento (18923 tokens)
[2026-03-17 14:35:43] 🔍 CONCILIO: Iniciando validación
[2026-03-17 14:36:01] ✅ CONCILIO: 3/3 APTO - Documento aprobado
```

---

## 6. Integración con LiveKit (Coach Oral)

### Arquitectura Voice Agent
```
┌─────────────────────────────────────────────────────────────────┐
│  LIVEKIT SERVER (TIER_03_AGENTS/orchestrator/)                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  voice_agent_worker.py                                   │   │
│  │  - STT (Speech-to-Text): Whisper                        │   │
│  │  - TTS (Text-to-Speech): OpenAI/ElevenLabs              │   │
│  │  - VAD (Voice Activity Detection)                       │   │
│  │  - Timer de exposición                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Hardware Integration
- **Brio 4K:** Análisis de gestos, contacto visual
- **Mikro Anker:** Detección de muletillas, velocidad de habla
- **Google Nest:** Feedback de audio

---

## 7. Comunicación Entre Agentes (A2A)

### Protocolo
```json
{
  "from": "maestro",
  "to": "redactor_didactico",
  "task_id": "t_20260317_001",
  "action": "create_programacion",
  "params": {
    "modulo": "Dirección de Servicios de Restauración",
    "horas": 160,
    "referencias": ["BOE_12345", "TODOFP_GS_001"]
  },
  "priority": "high",
  "deadline": "2026-03-18T10:00:00Z"
}
```

### Endpoint A2A
```http
POST /api/v1/a2a/message
Content-Type: application/json
Authorization: Bearer {GUARDIAN_SECRET_KEY}
```
