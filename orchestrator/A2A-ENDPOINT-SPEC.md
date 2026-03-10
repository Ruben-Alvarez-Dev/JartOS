# 📡 ESPECIFICACIÓN TÉCNICA: Endpoint A2A para OpenClaw Gateway

**Fecha:** 2026-03-10  
**Prioridad:** ALTA  
**Estado:** ⏳ Pendiente de implementación en OpenClaw Gateway

---

## 🎯 OBJETIVO

Implementar endpoint `/api/a2a` en OpenClaw Gateway para recibir comunicaciones del MCP Orchestrator (LiveKit Integration).

---

## 📋 ESPECIFICACIÓN DEL ENDPOINT

### POST /api/a2a

**Propósito:** Recibir mensajes A2A (Agent-to-Agent) del MCP Orchestrator

**Request:**
```json
{
  "type": "HANDSHAKE|COMMAND|STATUS_REQUEST",
  "timestamp": "ISO8601",
  "orchestrator": "MCP-Server",
  "payload": {
    // Variable según tipo de mensaje
  }
}
```

**Response:**
```json
{
  "status": "accepted|rejected|pending",
  "message_id": "string",
  "result": {}
}
```

---

## 🔧 TIPOS DE MENSAJES

### 1. HANDSHAKE

**Propósito:** Establecer canal de comunicación A2A

**Payload:**
```json
{
  "message_type": "ORCHESTRATOR_HANDSHAKE",
  "from": "MCP-Orchestrator",
  "to": "OpenClaw-Gateway",
  "role": "controller",
  "purpose": "LiveKit Integration - Sprint 2"
}
```

**Respuesta esperada:**
```json
{
  "status": "accepted",
  "message_id": "handshake-001",
  "result": {
    "a2a_channel": "established",
    "gateway_version": "2026.3.10",
    "capabilities": ["memory_store", "rag_store", "user_profiles"]
  }
}
```

---

### 2. COMMAND

**Propósito:** Ejecutar un comando específico

**Payload:**
```json
{
  "id": "cmd-001",
  "action": "enable_a2a_endpoint",
  "priority": "high",
  "description": "Enable A2A communication endpoint at /api/a2a"
}
```

**Comandos soportados:**

| ID | Action | Descripción |
|----|--------|-------------|
| cmd-001 | enable_a2a_endpoint | Habilitar endpoint A2A |
| cmd-002 | prepare_memory_store | Preparar schema para voice sessions |
| cmd-003 | prepare_rag_store | Preparar colección para voice knowledge |
| cmd-004 | create_api_credentials | Crear credenciales para LiveKit Agents |
| cmd-005 | enable_audit_logging | Habilitar logging para A2A |

**Respuesta esperada:**
```json
{
  "status": "accepted",
  "message_id": "cmd-001",
  "result": {
    "command": "enable_a2a_endpoint",
    "execution": "pending",
    "estimated_time": "5s"
  }
}
```

---

### 3. STATUS_REQUEST

**Propósito:** Solicitar estado de integración

**Payload:**
```json
{
  "type": "integration"
}
```

**Respuesta esperada:**
```json
{
  "status": "accepted",
  "message_id": "status-001",
  "result": {
    "integration_status": "in_progress",
    "sprint": 2,
    "completed_steps": ["install_livekit_agents"],
    "pending_steps": ["deploy_voice_agent", "test_integration"]
  }
}
```

---

## 🛠️ IMPLEMENTACIÓN EN OPENCLAW GATEWAY

### Código de ejemplo (Node.js/TypeScript)

```typescript
// Añadir a gateway/src/api/a2a.ts

import { Router } from 'express';
import { v4 as uuidv4 } from 'uuid';

const router = Router();

// Almacenar estado de sesión A2A
const a2aSession = {
  established: false,
  orchestrator: null,
  commands: []
};

/**
 * POST /api/a2a
 * Recibir mensajes A2A del MCP Orchestrator
 */
router.post('/', async (req, res) => {
  const { type, timestamp, orchestrator, payload } = req.body;
  
  // Validar request
  if (!type || !orchestrator) {
    return res.status(400).json({
      status: 'rejected',
      error: 'Missing required fields: type, orchestrator'
    });
  }
  
  // Generar ID de mensaje
  const messageId = uuidv4();
  
  // Log para audit
  console.log(`[A2A] Received ${type} from ${orchestrator}:`, payload);
  
  // Procesar según tipo
  switch (type) {
    case 'HANDSHAKE':
      a2aSession.established = true;
      a2aSession.orchestrator = orchestrator;
      
      res.json({
        status: 'accepted',
        message_id: messageId,
        result: {
          a2a_channel: 'established',
          gateway_version: '2026.3.10',
          capabilities: ['memory_store', 'rag_store', 'user_profiles']
        }
      });
      break;
      
    case 'COMMAND':
      const { id, action, priority, description } = payload;
      
      // Guardar comando para procesamiento
      a2aSession.commands.push({
        id,
        action,
        priority,
        description,
        received_at: new Date().toISOString(),
        status: 'queued'
      });
      
      res.json({
        status: 'accepted',
        message_id: messageId,
        result: {
          command: id,
          execution: 'queued',
          position: a2aSession.commands.length
        }
      });
      break;
      
    case 'STATUS_REQUEST':
      res.json({
        status: 'accepted',
        message_id: messageId,
        result: {
          integration_status: 'in_progress',
          sprint: 2,
          a2a_established: a2aSession.established,
          commands_received: a2aSession.commands.length,
          completed_steps: ['install_livekit_agents'],
          pending_steps: ['deploy_voice_agent', 'test_integration']
        }
      });
      break;
      
    default:
      res.status(400).json({
        status: 'rejected',
        error: `Unknown message type: ${type}`
      });
  }
});

export default router;
```

### Registrar endpoint en gateway

```typescript
// En gateway/src/index.ts o similar
import a2aRouter from './api/a2a';

app.use('/api/a2a', a2aRouter);
```

---

## 🧪 TESTING

### Test con curl

```bash
# Handshake
curl -X POST http://127.0.0.1:18789/api/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "type": "HANDSHAKE",
    "timestamp": "2026-03-10T21:00:00Z",
    "orchestrator": "MCP-Server",
    "payload": {
      "message_type": "ORCHESTRATOR_HANDSHAKE",
      "from": "MCP-Orchestrator",
      "to": "OpenClaw-Gateway",
      "role": "controller",
      "purpose": "LiveKit Integration - Sprint 2"
    }
  }'

# Command
curl -X POST http://127.0.0.1:18789/api/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "type": "COMMAND",
    "timestamp": "2026-03-10T21:00:00Z",
    "orchestrator": "MCP-Server",
    "payload": {
      "id": "cmd-001",
      "action": "enable_a2a_endpoint",
      "priority": "high",
      "description": "Enable A2A communication endpoint"
    }
  }'

# Status Request
curl -X POST http://127.0.0.1:18789/api/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "type": "STATUS_REQUEST",
    "timestamp": "2026-03-10T21:00:00Z",
    "orchestrator": "MCP-Server",
    "payload": {
      "type": "integration"
    }
  }'
```

---

## 📊 ESTADO ACTUAL

| Endpoint | Estado | Response Actual | Response Esperado |
|----------|--------|-----------------|-------------------|
| POST /api/a2a | ❌ 404 Not Found | `{"error": "Not Found"}` | `{"status": "accepted", ...}` |

---

## 🎯 PRÓXIMOS PASOS

1. **Implementar endpoint `/api/a2a`** en OpenClaw Gateway
2. **Reiniciar OpenClaw Gateway** para aplicar cambios
3. **Testear con curl** para verificar funcionamiento
4. **Ejecutar `a2a_communication.py`** para verificar integración completa

---

**Documentación relacionada:**
- [A2A Communication Protocol](./docs/A2A-COMMUNICATION.md)
- [LiveKit-OpenClaw Integration](./docs/LIVEKIT-OPENCLAW-INTEGRATION.md)
