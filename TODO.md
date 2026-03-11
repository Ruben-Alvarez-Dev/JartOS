# ✅ TODO - OPENCLAW-CITY

**Fecha:** 2026-03-10  
**Estado:** Sprint 0 en progreso  
**GitHub:** https://github.com/Ruben-Alvarez-Dev/OPENCLAW-city

---

## 🎯 TODO MAESTRO (TODOS LOS SPRINTS)

### SPRINT 0: PREPARACIÓN (Semana 1)

**Estado:** ✅ Completado

```
INFRASTRUCTURE SETUP
[x] 0.1.1 - Verificar VPS specs ✅ (CPU, RAM, disco, bandwidth)
[x] 0.1.2 - Instalar Docker + Docker Compose ✅
[x] 0.1.3 - Configurar red Docker ✅ (openclaw-network)
[x] 0.1.4 - Preparar dominios/subdominios ✅ (livekit.alvarezconsult.es)

LIVEKIT SELF-HOSTED SETUP
[x] 0.2.1 - Configurar LiveKit server (Docker) ✅
[x] 0.2.2 - Generar API keys locales ✅
[x] 0.2.3 - Configurar livekit-server.yaml ✅

DOCUMENTACIÓN
[x] 0.3.1 - Leer LiveKit docs completas ✅
[x] 0.3.2 - Estudiar Agents Framework examples ✅
[x] 0.3.3 - Revisar SIP integration guide ✅
[x] 0.3.4 - Crear checklist de prerequisitos ✅
```

---

### SPRINT 1: LIVEKIT SERVER (Semana 2)

**Estado:** ✅ Completado

```
DOCKER COMPOSE
[x] 1.1.1 - Crear docker-compose.yml para LiveKit ✅ (network_mode: host)
[x] 1.1.2 - Configurar Redis (requerido) ✅ (redis:7-alpine)
[x] 1.1.3 - Configurar PostgreSQL (opcional) ✅ (no requerido)
[x] 1.1.4 - Configurar LiveKit server YAML ✅ (config.yaml oficial)

LIVEKIT CLI
[x] 1.2.1 - Instalar LiveKit CLI ✅ (v2.15.0 oficial)
[x] 1.2.2 - Autenticar con proyecto ✅ (config ~/.config/livekit/livekit.toml)
[x] 1.2.3 - Crear rooms de test ✅ (openclaw-test-1)
[x] 1.2.4 - Verificar conectividad ✅

WEB CLIENT TEST
[x] 1.3.1 - Deploy LiveKit example web client ✅
[x] 1.3.2 - Probar conexión desde browser ✅
[x] 1.3.3 - Probar audio/video ✅ (web client con token API)
[x] 1.3.4 - Verificar latencia ✅

SSL/TLS (Oficial LiveKit Docs)
[x] 1.4.1 - Instalar certbot ✅
[x] 1.4.2 - Obtener certificado Let's Encrypt ✅ (válido hasta 2026-06-08)
[x] 1.4.3 - Configurar TLS en LiveKit ✅ (certs en /opt/livekit/certs/)
[x] 1.4.4 - Configurar TURN server ✅ (puerto 5349 TLS)
[x] 1.4.5 - Configurar firewall ✅ (443, 7881, 5349, 50000-60000/udp)
[x] 1.4.6 - Configurar Caddy reverse proxy ✅
[x] 1.4.7 - Configurar Tailscale Serve ✅ (HTTPS tailnet)
```

---

### SPRINT 2: LIVEKIT AGENTS (Semana 3)

**Estado:** 🟡 En progreso

```
AGENTS FRAMEWORK
[x] 2.1.1 - Instalar livekit-agents (pip) ✅ (v1.4.4)
[x] 2.1.2 - Crear worker básico ✅ (voice_agent_worker.py)
[ ] 2.1.3 - Configurar connection a LiveKit ⏳ (pendiente: A2A endpoint)
[ ] 2.1.4 - Deploy worker ⏳ (pendiente: configuración completa)

VOICE AGENT BASE
[ ] 2.2.1 - Usar template oficial de voice agent ⏳
[ ] 2.2.2 - Configurar STT/TTS (proveedores default) ⏳
[ ] 2.2.3 - Probar conversación básica ⏳
[ ] 2.2.4 - Ajustar latencia ⏳

CUSTOM AGENT + OPENCLAW
[ ] 2.3.1 - Crear agente personalizado ⏳
[ ] 2.3.2 - Añadir system prompt personalizado ⏳
[ ] 2.3.3 - Integrar con OpenClaw Memory ⏳ (pendiente: A2A endpoint)
[ ] 2.3.4 - Integrar con OpenClaw RAG ⏳ (pendiente: A2A endpoint)
[ ] 2.3.5 - Testear conversación completa ⏳

ORQUESTACIÓN MCP
[x] 3.1.1 - Instalar MCP ✅
[x] 3.1.2 - Crear MCP orchestrator ✅
[x] 3.1.3 - Crear A2A communication script ✅
[x] 3.1.4 - Enviar comandos a OpenClaw ✅ (5 commands sent)
[ ] 3.1.5 - OpenClaw A2A endpoint ⏳ (pendiente implementación)
### SPRINT 2: LIVEKIT AGENTS + SIP (Semana 3)

**Estado:** 🟡 70% completado

```
AGENTS FRAMEWORK
[x] 2.1.1 - Instalar livekit-agents (pip) ✅ (v1.4.4)
[x] 2.1.2 - Crear worker básico ✅ (voice_agent_worker.py)
[x] 2.1.3 - Configurar connection a LiveKit ✅ (ws_url, api_key)
[x] 2.1.4 - Deploy worker ✅ (voice-agent.service activo)

VOICE AGENT BASE
[ ] 2.2.1 - Usar template oficial de voice agent ⏳ (API cambió)
[ ] 2.2.2 - Configurar STT/TTS (proveedores default) ⏳
[ ] 2.2.3 - Probar conversación básica ⏳
[ ] 2.2.4 - Ajustar latencia ⏳

CUSTOM AGENT + OPENCLAW
[x] 2.3.1 - Crear agente personalizado ✅ (voice_agent_worker.py)
[ ] 2.3.2 - Añadir system prompt personalizado ⏳
[x] 2.3.3 - Integrar con OpenClaw Memory ⏳ (A2A establecido)
[ ] 2.3.4 - Integrar con OpenClaw RAG ⏳
[ ] 2.3.5 - Testear conversación completa ⏳

SIP TRUNKING
[x] 3.1.1 - Investigar LiveKit SIP API ✅
[x] 3.1.2 - Crear script de configuración ✅ (configure_livekit_sip.py)
[ ] 3.1.3 - Configurar SIP Inbound Trunk ⏳ (Redis issue)
[ ] 3.1.4 - Configurar SIP Dispatch Rule ⏳
[ ] 3.1.5 - Testear con Zadarma ⏳

A2A COORDINATION
[x] 4.1.1 - Establecer canal A2A ✅ (localhost:18790)
[x] 4.1.2 - Enviar comandos a Ramiro ✅ (msg-0013 a msg-0016)
[x] 4.1.3 - Compartir progreso ✅ (vía A2A endpoint)
[ ] 4.1.4 - Recibir respuesta de Ramiro ⏳
```
```

---

### SPRINT 3: TTS ADAPTER (Semana 4)

**Estado:** ⏳ Pendiente

```
TTS SERVER BASE
[ ] 3.1.1 - Crear API REST para TTS
[ ] 3.1.2 - Endpoint: POST /tts/generate
[ ] 3.1.3 - Endpoint: GET /tts/voices
[ ] 3.1.4 - Endpoint: GET /tts/models

PIPER TTS (ligero)
[ ] 3.2.1 - Instalar Piper (Docker o local)
[ ] 3.2.2 - Descargar voces en español
[ ] 3.2.3 - Integrar con TTS Server
[ ] 3.2.4 - Testear generación de audio

COQUI XTTS (pesado)
[ ] 3.3.1 - Instalar Coqui XTTS (Docker)
[ ] 3.3.2 - Configurar modelo en español
[ ] 3.3.3 - Integrar con TTS Server
[ ] 3.3.4 - Comparar calidad vs velocidad

LIVEKIT TTS PLUGIN
[ ] 3.4.1 - Crear plugin TTS para LiveKit
[ ] 3.4.2 - Implementar interfaz oficial
[ ] 3.4.3 - Conectar con TTS Server
[ ] 3.4.4 - Testear en agente de voz

VOICE MANAGER
[ ] 3.5.1 - Crear dashboard de gestión
[ ] 3.5.2 - Listar voces disponibles
[ ] 3.5.3 - Configurar voz por defecto
[ ] 3.5.4 - Clasificar por: empresa, idioma, peso
```

---

### SPRINT 4: STT ADAPTER (Semana 5)

**Estado:** ⏳ Pendiente

```
STT SERVER BASE
[ ] 4.1.1 - Crear API REST para STT
[ ] 4.1.2 - Endpoint: POST /stt/transcribe
[ ] 4.1.3 - Endpoint: POST /stt/stream
[ ] 4.1.4 - Soporte para audio streaming

FASTER-WHISPER
[ ] 4.2.1 - Instalar Faster-Whisper
[ ] 4.2.2 - Descargar modelo en español
[ ] 4.2.3 - Integrar con STT Server
[ ] 4.2.4 - Optimizar para baja latencia

WHISPER (OpenAI)
[ ] 4.3.1 - Instalar Whisper oficial
[ ] 4.3.2 - Configurar modelo (small/medium)
[ ] 4.3.3 - Integrar con STT Server
[ ] 4.3.4 - Comparar precisión vs velocidad

LIVEKIT STT PLUGIN
[ ] 4.4.1 - Crear plugin STT para LiveKit
[ ] 4.4.2 - Implementar interfaz oficial
[ ] 4.4.3 - Conectar con STT Server
[ ] 4.4.4 - Testear en agente de voz
```

---

### SPRINT 5: LLM INTERMEDIARIO (Semana 6)

**Estado:** ⏳ Pendiente

```
OLLAMA SERVER
[ ] 5.1.1 - Instalar Ollama (Docker o nativo)
[ ] 5.1.2 - Descargar modelos ligeros (Llama 3.1 8B, Mistral 7B)
[ ] 5.1.3 - Configurar API endpoint
[ ] 5.1.4 - Testear generación de texto

LLAMA.CPP
[ ] 5.2.1 - Instalar llama.cpp
[ ] 5.2.2 - Descargar modelos cuantizados (GGUF)
[ ] 5.2.3 - Configurar servidor API
[ ] 5.2.4 - Comparar rendimiento vs Ollama

MODEL MANAGER
[ ] 5.3.1 - Crear dashboard de gestión
[ ] 5.3.2 - Listar modelos disponibles
[ ] 5.3.3 - Configurar modelo por defecto
[ ] 5.3.4 - Clasificar por: empresa, tamaño, idioma

API ROUTER
[ ] 5.4.1 - Crear router OpenAI-compatible
[ ] 5.4.2 - Soporte para múltiples backends
[ ] 5.4.3 - Fallback automático
[ ] 5.4.4 - Rate limiting por modelo
```

---

### SPRINT 6: SIP INTEGRATION (Semana 7)

**Estado:** ⏳ Pendiente

```
LIVEKIT SIP TRUNK
[ ] 6.1.1 - Configurar SIP trunk en LiveKit
[ ] 6.1.2 - Obtener SIP credentials
[ ] 6.1.3 - Configurar inbound rules
[ ] 6.1.4 - Configurar outbound rules

TU NÚMERO FIJO
[ ] 6.2.1 - Obtener SIP credentials de tu proveedor
[ ] 6.2.2 - Configurar en LiveKit
[ ] 6.2.3 - Testear inbound (llamar al fijo → Room)
[ ] 6.2.4 - Testear outbound (Room → llamar al fijo)

SIP INGRESS
[ ] 6.3.1 - Configurar SIP → WebRTC ingress
[ ] 6.3.2 - Testear calidad de audio
[ ] 6.3.3 - Ajustar codecs (G.711, Opus)
[ ] 6.3.4 - Verificar latencia

CENTRALITA VIRTUAL (IVR)
[ ] 6.4.1 - Crear IVR básico
[ ] 6.4.2 - Menú de opciones ("Presiona 1 para...")
[ ] 6.4.3 - Routing a diferentes agentes
[ ] 6.4.4 - Testear flujo completo
```

---

### SPRINT 7: EGRESS/INGRESS (Semana 8)

**Estado:** ⏳ Pendiente

```
EGRESS (GRABACIÓN)
[ ] 7.1.1 - Configurar room egress
[ ] 7.1.2 - Grabar a MP4/WebM
[ ] 7.1.3 - Guardar en disco/S3
[ ] 7.1.4 - Testear grabación completa

EGRESS (STREAMING)
[ ] 7.2.1 - Configurar RTMP egress
[ ] 7.2.2 - Stream a YouTube/Twitch
[ ] 7.2.3 - Testear streaming en vivo
[ ] 7.2.4 - Verificar latencia de stream

INGRESS (RTMP)
[ ] 7.3.1 - Configurar RTMP ingress
[ ] 7.3.2 - Conectar OBS
[ ] 7.3.3 - Stream OBS → LiveKit Room
[ ] 7.3.4 - Testear calidad

INGRESS (SIP)
[ ] 7.4.1 - Configurar SIP ingress
[ ] 7.4.2 - Llamar desde teléfono → Room
[ ] 7.4.3 - Verificar transcoding
[ ] 7.4.4 - Testear múltiples llamadas
```

---

### SPRINT 8: INTEGRACIÓN OPENCLAW (Semana 9)

**Estado:** ⏳ Pendiente

```
API INTEGRATION
[ ] 8.1.1 - Voice Agent → OpenClaw API
[ ] 8.1.2 - OpenClaw Agents → Voice TTS
[ ] 8.1.3 - Shared authentication
[ ] 8.1.4 - Error handling

MEMORIA COMPARTIDA
[ ] 8.2.1 - Voice → Memory Store (conversaciones)
[ ] 8.2.2 - Memory Store → Voice (contexto)
[ ] 8.2.3 - Qdrant RAG para ambos
[ ] 8.2.4 - User profiles compartidos

PERMISOS UNIFICADOS
[ ] 8.3.1 - RBAC para voz (mismos dominios)
[ ] 8.3.2 - Human-in-the-loop para voz
[ ] 8.3.3 - Audit trail de llamadas
[ ] 8.3.4 - Rate limiting por usuario

LOGS CENTRALIZADOS
[ ] 8.4.1 - Voice logs → JSON logging
[ ] 8.4.2 - Mismo formato que OpenClaw
[ ] 8.4.3 - Dashboard unificado
[ ] 8.4.4 - Alertas de seguridad
```

---

### SPRINT 9: TESTING + DOCS (Semana 10)

**Estado:** ⏳ Pendiente

```
END-TO-END TESTING
[ ] 9.1.1 - Testear flujo completo (teléfono → agente → respuesta)
[ ] 9.1.2 - Testear fallbacks (si TTS falla, usar backup)
[ ] 9.1.3 - Testear carga (múltiples llamadas simultáneas)
[ ] 9.1.4 - Medir latencia end-to-end

SECURITY TESTING
[ ] 9.2.1 - Penetration testing básico
[ ] 9.2.2 - Verificar autenticación SIP
[ ] 9.2.3 - Verificar rate limiting
[ ] 9.2.4 - Verificar audit trail

DOCUMENTACIÓN
[ ] 9.3.1 - Documentar arquitectura completa
[ ] 9.3.2 - Documentar cada componente
[ ] 9.3.3 - Crear guías de troubleshooting
[ ] 9.3.4 - Actualizar CHANGELOG

DASHBOARD UNIFICADO
[ ] 9.4.1 - Extender openclaw-dashboard
[ ] 9.4.2 - Añadir métricas de voz
[ ] 9.4.3 - Añadir gestión de agentes
[ ] 9.4.4 - Añadir monitoring en tiempo real
```

---

## 📊 RESUMEN DE TODOs

### Por Sprint

| Sprint | TODOs | Completados | Progreso |
|--------|-------|-------------|----------|
| Sprint 0 | 10 | 7 | 70% |
| Sprint 1 | 11 | 0 | 0% |
| Sprint 2 | 11 | 0 | 0% |
| Sprint 3 | 17 | 0 | 0% |
| Sprint 4 | 13 | 0 | 0% |
| Sprint 5 | 13 | 0 | 0% |
| Sprint 6 | 13 | 0 | 0% |
| Sprint 7 | 13 | 0 | 0% |
| Sprint 8 | 13 | 0 | 0% |
| Sprint 9 | 13 | 0 | 0% |
| **TOTAL** | **127** | **7** | **5%** |

---

## 🎯 PRÓXIMOS 5 TODOs (INMEDIATOS)

1. `[ ] 0.3.1 - Leer LiveKit docs completas`
2. `[ ] 0.3.2 - Estudiar Agents Framework examples`
3. `[ ] 0.3.3 - Revisar SIP integration guide`
4. `[ ] 0.3.4 - Crear checklist de prerequisitos`
5. `[ ] 1.1.1 - Crear docker-compose.yml para LiveKit` (ya está hecho, falta documentar)

---

## 📝 CÓMO USAR ESTE TODO

### Marcar como completado
```markdown
Cambiar: [x] 0.1.1 - Verificar VPS specs ✅
Por:     [x] 0.1.1 - Verificar VPS specs ✅
```

### Actualizar progreso
```bash
# Después de completar hitos, actualizar ROADMAP.md
git add TODO.md ROADMAP.md CHANGELOG.md
git commit -m "chore: actualizar progreso del Sprint 0"
git push
```

---

**Última actualización:** 2026-03-10
**Próxima actualización:** Después de completar Sprint 1
**Estado:** Sprint 0 ✅ Completado (7/10 tareas - 70%)
