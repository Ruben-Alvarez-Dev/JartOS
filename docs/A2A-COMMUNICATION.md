# 🤝 LIVEKIT ↔ OPENCLAW - COMUNICACIÓN A2A (Agent-to-Agent)

**Fecha:** 2026-03-10  
**Tipo:** Handshake inicial - Sprint 2  
**Participantes:** LiveKit Agents Worker ↔ OpenClaw Gateway

---

## 📋 MENSAJE DE INICIALIZACIÓN

### De: LiveKit Agents Worker
### Para: OpenClaw Gateway

```json
{
  "message_type": "A2A_HANDSHAKE",
  "timestamp": "2026-03-10T21:00:00Z",
  "sender": {
    "name": "LiveKit Agents Worker",
    "version": "0.8.0",
    "capabilities": [
      "voice_processing",
      "stt",
      "tts",
      "realtime_communication"
    ],
    "endpoint": "http://localhost:8445"
  },
  "recipient": {
    "name": "OpenClaw Gateway",
    "version": "2026.3.10",
    "endpoint": "http://127.0.0.1:18789"
  },
  "purpose": "Establecer canal de comunicación para integración de voz",
  "requested_services": [
    {
      "service": "memory_store",
      "operations": ["read", "write"],
      "description": "Acceso a memoria de conversaciones para contexto de voz"
    },
    {
      "service": "rag_store",
      "operations": ["search"],
      "description": "Búsqueda semántica para respuestas contextualizadas"
    },
    {
      "service": "user_profiles",
      "operations": ["read"],
      "description": "Preferencias de usuario para personalización de voz"
    }
  ],
  "authentication": {
    "method": "api_key",
    "api_key": "openclaw-54990a102ce72a4e"
  },
  "proposed_workflow": {
    "step_1": "Usuario habla → LiveKit STT → texto",
    "step_2": "Texto → OpenClaw Memory → contexto histórico",
    "step_3": "Texto + Contexto → OpenClaw RAG → información relevante",
    "step_4": "Texto + Contexto + RAG → LLM → respuesta",
    "step_5": "Respuesta → LiveKit TTS → audio",
    "step_6": "Audio → Usuario",
    "step_7": "Conversación → OpenClaw Memory → guardado"
  }
}
```

---

## 📋 RESPUESTA ESPERADA

### De: OpenClaw Gateway
### Para: LiveKit Agents Worker

```json
{
  "message_type": "A2A_HANDSHAKE_RESPONSE",
  "timestamp": "2026-03-10T21:00:01Z",
  "status": "accepted",
  "sender": {
    "name": "OpenClaw Gateway",
    "version": "2026.3.10",
    "capabilities": [
      "memory_management",
      "rag_search",
      "user_profiles",
      "conversation_history",
      "security_pipeline"
    ],
    "endpoint": "http://127.0.0.1:18789"
  },
  "granted_services": [
    {
      "service": "memory_store",
      "operations": ["read", "write"],
      "endpoint": "/api/memory/{user_id}",
      "rate_limit": "100 requests/minute"
    },
    {
      "service": "rag_store",
      "operations": ["search"],
      "endpoint": "/api/rag/search",
      "rate_limit": "50 requests/minute"
    },
    {
      "service": "user_profiles",
      "operations": ["read"],
      "endpoint": "/api/users/{user_id}/profile",
      "rate_limit": "100 requests/minute"
    }
  ],
  "authentication": {
    "method": "bearer_token",
    "token_endpoint": "/api/token",
    "token_ttl": "24h"
  },
  "accepted_workflow": {
    "acknowledged": true,
    "modifications": [
      "Paso 2: Memory se consulta ANTES de LLM para contexto",
      "Paso 3: RAG search con threshold 0.7 mínimo",
      "Paso 7: Guardado asíncrono para no bloquear respuesta"
    ]
  },
  "security_requirements": {
    "encryption": "TLS 1.3",
    "audit_logging": true,
    "rate_limiting": true,
    "human_in_the_loop": "requerido para acciones críticas"
  }
}
```

---

## 🔄 FLUJO DE COMUNICACIÓN

### 1. Handshake Inicial

```
┌─────────────────┐                          ┌─────────────────┐
│  LiveKit Agent  │                          │  OpenClaw GW    │
└────────┬────────┘                          └────────┬────────┘
         │                                            │
         │  POST /api/a2a/handshake                   │
         │  {handshake_request}                       │
         │───────────────────────────────────────────>│
         │                                            │
         │  Valida API key                            │
         │  Registra en audit log                     │
         │                                            │
         │  POST /api/a2a/handshake/response          │
         │  {handshake_response}                      │
         │<───────────────────────────────────────────│
         │                                            │
```

### 2. Flujo de Voz en Tiempo Real

```
Usuario → LiveKit STT → Texto
              │
              ▼
    ┌─────────────────┐
    │  OpenClaw API   │
    │  GET /memory    │
    └────────┬────────┘
             │
             ▼
    Contexto histórico
             │
             ▼
    ┌─────────────────┐
    │  OpenClaw RAG   │
    │  POST /search   │
    └────────┬────────┘
             │
             ▼
    Información relevante
             │
             ▼
    ┌─────────────────┐
    │  LLM (Mistral)  │
    │  + System Prompt│
    └────────┬────────┘
             │
             ▼
    Respuesta de texto
             │
             ▼
    LiveKit TTS → Audio → Usuario
```

---

## 📊 ESTADO DE LA INTEGRACIÓN

| Componente | Estado | Progreso |
|------------|--------|----------|
| **Handshake Protocol** | 🟡 En diseño | 50% |
| **Memory Store API** | ✅ Disponible | 100% |
| **RAG Store API** | ✅ Disponible | 100% |
| **Voice Agent Worker** | ⏳ Pendiente | 0% |
| **STT Integration** | ⏳ Pendiente | 0% |
| **TTS Integration** | ⏳ Pendiente | 0% |
| **Audit Logging** | ✅ Disponible | 100% |

---

## 🎯 PRÓXIMOS PASOS INMEDIATOS

### Esta semana (Sprint 2)

1. **Implementar handshake API** en OpenClaw Gateway
   - Endpoint: `POST /api/a2a/handshake`
   - Validación de API key
   - Registro en audit log

2. **Crear LiveKit Agents Worker**
   - Instalar `livekit-agents`
   - Configurar worker básico
   - Conectar a LiveKit server

3. **Implementar OpenClaw Connector**
   - Cliente HTTP para OpenClaw API
   - Manejo de tokens
   - Reintentos y fallbacks

4. **Test de integración end-to-end**
   - Voz → STT → Memory → RAG → LLM → TTS → Voz
   - Medir latencia total
   - Ajustar thresholds

---

## 🔗 ENLACES RELACIONADOS

- [LiveKit Agents Docs](https://docs.livekit.io/agents/)
- [OpenClaw Gateway Docs](./docs/OPENCLAW-GATEWAY.md)
- [OpenClaw Memory Store](./docs/MEMORY-STORE.md)
- [OpenClaw RAG Store](./docs/RAG-STORE.md)
- [LIVEKIT-OPENCLAW-INTEGRATION.md](./LIVEKIT-OPENCLAW-INTEGRATION.md)

---

**Estado:** 🟡 En progreso (Sprint 2)  
**Última actualización:** 2026-03-10  
**Próxima actualización:** Después de implementar handshake API
