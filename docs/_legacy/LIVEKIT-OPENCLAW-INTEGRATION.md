# 🤝 LIVEKIT + OPENCLAW - INTEGRACIÓN

**Fecha:** 2025-03-10  
**Estado:** 🟡 En progreso (Sprint 2)  
**Documentación Oficial:** Basada en [LiveKit Agents](https://docs.livekit.io/agents/) y [OpenClaw API](./docs/OPENCLAW-GATEWAY.md)

---

## 📋 RESUMEN EJECUTIVO

Este documento describe la integración entre **LiveKit** (voz/video en tiempo real) y **OpenClaw** (agentes AI enterprise).

### Arquitectura de Integración

```
┌─────────────────────────────────────────────────────────────────┐
│  USUARIO (Teléfono, Browser, App)                               │
└─────────────────────────────────────────────────────────────────┘
         │
         │ WebRTC / SIP
         ▼
┌─────────────────────────────────────────────────────────────────┐
│  LIVEKIT SERVER (Self-Hosted)                                   │
│  • Rooms de voz/video                                           │
│  • STT (Speech-to-Text)                                         │
│  • TTS (Text-to-Speech)                                         │
│  • Agents Framework                                             │
└─────────────────────────────────────────────────────────────────┘
         │
         │ WebSocket / HTTP
         ▼
┌─────────────────────────────────────────────────────────────────┐
│  LIVEKIT AGENTS WORKER                                          │
│  • Voice Agent personalizado                                    │
│  • System prompt configurado                                    │
│  • Integración con OpenClaw API                                 │
└─────────────────────────────────────────────────────────────────┘
         │
         │ HTTP/gRPC
         ▼
┌─────────────────────────────────────────────────────────────────┐
│  OPENCLAW GATEWAY (localhost:18789)                             │
│  • Autenticación                                                │
│  • Routing a agentes                                            │
│  • Memory Store                                                 │
│  • RAG Store                                                    │
└─────────────────────────────────────────────────────────────────┘
         │
         │ SQLite / Qdrant
         ▼
┌─────────────────────────────────────────────────────────────────┐
│  OPENCLAW MEMORY & RAG                                          │
│  • Conversaciones históricas                                    │
│  • User profiles                                                │
│  • Embeddings vectoriales                                       │
│  • Contexto para Voice Agent                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 COMPONENTES DE LA INTEGRACIÓN

### 1. LiveKit Server

| Componente | Estado | URL |
|------------|--------|-----|
| **Server** | ✅ Running | `wss://vpn-ruben-vps-openclaw.tail6c9810.ts.net` |
| **API** | ✅ Running | `https://livekit.alvarezconsult.es` |
| **TURN** | ✅ Configurado | Puerto 5349 TLS |
| **SSL/TLS** | ✅ Let's Encrypt | Válido hasta 2025-06-08 |

### 2. OpenClaw Gateway

| Componente | Estado | URL |
|------------|--------|-----|
| **Gateway** | ✅ Running | `http://127.0.0.1:18789` |
| **Memory Store** | ✅ Running | `/var/lib/openclaw/memory.db` |
| **RAG Store** | ✅ Running | Qdrant embeddings |
| **Auth** | ✅ Token-based | `${OPENCLAW_GATEWAY_TOKEN}` |

### 3. LiveKit Agents Worker (🟡 En desarrollo)

| Componente | Estado | Ubicación |
|------------|--------|-----------|
| **Worker** | ⏳ Pendiente | `/opt/livekit-agents/` |
| **Voice Agent** | ⏳ Pendiente | `voice_agent.py` |
| **OpenClaw Connector** | ⏳ Pendiente | `openclaw_connector.py` |

---

## 📝 SPRINT 2: INTEGRACIÓN LIVEKIT + OPENCLAW

### Objetivos del Sprint

1. ✅ Instalar livekit-agents (pip)
2. ✅ Crear worker básico de agentes
3. ✅ Configurar conexión a LiveKit
4. ✅ Deploy worker de agentes
5. ⏳ Integrar con OpenClaw Memory Store
6. ⏳ Integrar con OpenClaw RAG Store
7. ⏳ Voice Agent → OpenClaw API

### Checklist Detallada

#### 2.1 Agents Framework

- [ ] 2.1.1 Instalar livekit-agents (pip)
  ```bash
  pip install livekit-agents livekit-plugins-silero
  ```

- [ ] 2.1.2 Crear worker básico
  ```python
  from livekit.agents import Worker, JobRequest
  
  async def entrypoint(ctx: JobContext):
      # Voice agent logic here
      pass
  
  if __name__ == "__main__":
      Worker(entrypoint).run()
  ```

- [ ] 2.1.3 Configurar conexión a LiveKit
  ```bash
  export LIVEKIT_URL="wss://vpn-ruben-vps-openclaw.tail6c9810.ts.net"
  export LIVEKIT_API_KEY="openclaw-54990a102ce72a4e"
  export LIVEKIT_API_SECRET="YOUR_LIVEKIT_SECRET"
  ```

- [ ] 2.1.4 Deploy worker
  ```bash
  systemctl enable livekit-agents
  systemctl start livekit-agents
  ```

#### 2.2 Voice Agent Base

- [ ] 2.2.1 Usar template oficial de voice agent
- [ ] 2.2.2 Configurar STT/TTS (proveedores default)
- [ ] 2.2.3 Probar conversación básica
- [ ] 2.2.4 Ajustar latencia

#### 2.3 Custom Agent + OpenClaw

- [ ] 2.3.1 Crear agente personalizado
- [ ] 2.3.2 Añadir system prompt personalizado
- [ ] 2.3.3 Integrar con OpenClaw Memory
  ```python
  # Obtener contexto de Memory Store
  memory = await openclaw.get_user_memory(user_id)
  context = memory.get("conversation_history", [])
  ```
- [ ] 2.3.4 Integrar con OpenClaw RAG
  ```python
  # Búsqueda semántica
  results = await openclaw.rag_search(query, top_k=3)
  ```
- [ ] 2.3.5 Testear conversación completa

---

## 🔌 API DE INTEGRACIÓN

### OpenClaw Memory Store API

```python
# Obtener memoria de usuario
GET /api/memory/{user_id}
Response: {
    "user_id": "string",
    "conversation_history": [...],
    "preferences": {...},
    "long_term_memory": [...]
}

# Guardar conversación
POST /api/memory/{user_id}/conversation
Body: {
    "role": "user|assistant",
    "content": "string",
    "timestamp": "ISO8601"
}
```

### OpenClaw RAG Store API

```python
# Búsqueda semántica
POST /api/rag/search
Body: {
    "query": "string",
    "top_k": 3,
    "threshold": 0.7
}
Response: {
    "results": [
        {
            "content": "string",
            "score": 0.95,
            "metadata": {...}
        }
    ]
}

# Insertar documento
POST /api/rag/documents
Body: {
    "content": "string",
    "metadata": {...}
}
```

### LiveKit Agents API

```python
# Crear room
POST /twirp/livekit.room.RoomService/CreateRoom
Body: {
    "name": "voice-session-{user_id}",
    "emptyTimeout": 300
}

# Generar token de acceso
POST /api/token
Body: {
    "room": "voice-session-{user_id}",
    "name": "User Name"
}
Response: {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
/opt/livekit-agents/
├── worker.py                    # Worker principal
├── voice_agent.py               # Voice agent personalizado
├── openclaw_connector.py        # Conector OpenClaw API
├── config.py                    # Configuración
├── requirements.txt             # Dependencias Python
└── systemd/
    └── livekit-agents.service   # Servicio systemd
```

### requirements.txt

```txt
livekit-agents>=0.8.0
livekit-plugins-silero>=0.6.0
livekit-plugins-openai>=0.8.0
httpx>=0.25.0
python-dotenv>=1.0.0
```

### livekit-agents.service

```ini
[Unit]
Description=LiveKit Agents Worker
After=network.target livekit-server.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/livekit-agents
EnvironmentFile=/opt/livekit-agents/.env
ExecStart=/opt/livekit-agents/venv/bin/python /opt/livekit-agents/worker.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## 🔒 SEGURIDAD

### Autenticación

1. **LiveKit → OpenClaw**
   - Token JWT de LiveKit
   - API Key en headers

2. **OpenClaw → LiveKit**
   - Token de acceso por room
   - Identity validation

### Permisos

| Rol | LiveKit | OpenClaw |
|-----|---------|----------|
| **Voice Agent** | room_join, publish, subscribe | memory_read, memory_write, rag_search |
| **Usuario** | room_join, publish, subscribe | memory_read (propio) |

---

## 🧪 TESTING

### Test de Integración

```bash
# 1. Iniciar worker
python /opt/livekit-agents/worker.py

# 2. Crear room de test
lk room create test-voice-session

# 3. Conectar cliente de test
python /opt/livekit-agents/test_client.py

# 4. Verificar logs
journalctl -u livekit-agents -f
```

### Métricas de Calidad

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| **Latencia STT** | < 200ms | livekit-agents logs |
| **Latencia TTS** | < 300ms | livekit-agents logs |
| **Latencia LLM** | < 1000ms | OpenClaw logs |
| **Latencia Total** | < 2000ms | End-to-end test |

---

## 📊 MONITORING

### Prometheus Metrics

```
# LiveKit
livekit_server_rooms_total
livekit_server_participants_total
livekit_server_track_published_total

# OpenClaw
openclaw_gateway_requests_total
openclaw_memory_queries_total
openclaw_rag_searches_total

# Agents
livekit_agents_jobs_active
livekit_agents_stt_latency_seconds
livekit_agents_tts_latency_seconds
```

### Logs Centralizados

```bash
# LiveKit Agents
journalctl -u livekit-agents -f

# OpenClaw Gateway
journalctl -u openclaw -f

# Combinados
journalctl -t livekit-agents -t openclaw -f
```

---

## 🔗 ENLACES RELACIONADOS

- [LiveKit Agents Docs](https://docs.livekit.io/agents/)
- [LiveKit Agents GitHub](https://github.com/livekit/agents)
- [OpenClaw Gateway Docs](./docs/OPENCLAW-GATEWAY.md)
- [OpenClaw Memory Store](./docs/MEMORY-STORE.md)
- [OpenClaw RAG Store](./docs/RAG-STORE.md)
- [ROADMAP.md](./ROADMAP.md)

---

**Última actualización:** 2025-03-10  
**Próxima actualización:** Después de Sprint 2  
**Estado:** 🟡 En progreso (Sprint 2)
