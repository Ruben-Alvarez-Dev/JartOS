# 📋 OPENCLAW-CITY - ROADMAP MAESTRO

**Fecha:** 2026-03-10
**Versión:** 1.1
**GitHub:** https://github.com/Ruben-Alvarez-Dev/OPENCLAW-city
**Estado:** Fase 1 ✅ Completada, Fase 2 🟡 Sprint 0 ✅ Completado

---

## 🎯 ROADMAP VISUAL

```
2026
│
├── FEBRERO (Q1)
│   └── ✅ FASE 1: OpenClaw Básico
│       ├── OpenClaw Gateway hardeneado
│       ├── Email Bridge (Gmail)
│       ├── Orchestrator Bot (Ramiro)
│       ├── Memory Store (SQLite)
│       ├── RAG Store (embeddings)
│       ├── Security Pipeline
│       ├── Dashboard CLI
│       └── Documentación enterprise
│
├── MARZO (Q1)
│   ├── ✅ Semana 1-2: Documentación GitHub
│   ├── ✅ Semana 3-4: Sprint 0 (Preparación)
│   └── ✅ Semana 5-6: Sprint 1 (LiveKit Server)
│
├── ABRIL (Q2)
│   ├── 🟡 Semana 7-8: Sprint 2 (Agents)
│   ├── 🟡 Semana 9-10: Sprint 3 (TTS)
│   └── 🟡 Semana 11-12: Sprint 4 (STT)
│
├── MAYO (Q2)
│   ├── 🟡 Semana 13-14: Sprint 5 (LLM)
│   ├── 🟡 Semana 15-16: Sprint 6 (SIP)
│   └── 🟡 Semana 17-18: Sprint 7 (Egress/Ingress)
│
└── JUNIO (Q2)
    ├── 🟡 Semana 19-20: Sprint 8 (Integración)
    └── 🟡 Semana 21-22: Sprint 9 (Testing + Docs)
```

---

## 📊 ESTADO ACTUAL (2026-03-10)

### FASE 1: OPENCLAW BÁSICO ✅ COMPLETADA

| Componente | Estado | Ubicación | Documentación |
|------------|--------|-----------|---------------|
| OpenClaw Gateway | ✅ Activo | 127.0.0.1:18789 | ✅ docs/OPENCLAW-GATEWAY.md |
| Email Bridge | ✅ Activo | /opt/openclaw-email-bridge | ✅ docs/EMAIL-BRIDGE.md |
| Orchestrator Bot | ✅ Activo | /opt/openclaw-orchestrator | ✅ docs/ORCHESTRATOR-BOT.md |
| Memory Store | ✅ Activo | /var/lib/openclaw/memory.db | ✅ docs/MEMORY-STORE.md |
| RAG Store | ✅ Activo | /opt/openclaw-memory | ✅ docs/RAG-STORE.md |
| Security Pipeline | ✅ Activo | /opt/openclaw-security | ✅ docs/SECURITY-PIPELINE.md |
| Dashboard CLI | ✅ Activo | /usr/local/bin/openclaw-dashboard | ✅ docs/DASHBOARD.md |
| Tailscale | ✅ Activo | System | ✅ docs/INFRASTRUCTURE.md |
| UFW Firewall | ✅ Activo | System | ✅ docs/INFRASTRUCTURE.md |
| Backups | ✅ Automáticos | /root/backups | ✅ docs/DEPLOYMENT.md |
| Watchdog | ✅ Activo | /usr/local/bin/openclaw-watchdog | ✅ docs/MAINTENANCE.md |

**Progreso:** 11/11 componentes (100%)

---

### FASE 2: LIVEKIT INTEGRATION 🟡 PLANIFICADA

#### Sprint 0: Preparación (Semana 1)

**Estado:** ✅ Completado
**Duración:** 2026-03-10 a 2026-03-17

| Hito | Estado | Progreso |
|------|--------|----------|
| 0.1 Infrastructure Setup | ✅ Completado | 100% |
| 0.2 LiveKit Self-Hosted | ✅ Completado | 100% |
| 0.3 Documentación | ✅ Completado | 100% |

**Checklist Sprint 0:**
- [x] 0.1.1 Verificar VPS specs ✅ (CPU, RAM, disco, bandwidth)
- [x] 0.1.2 Instalar Docker + Docker Compose ✅
- [x] 0.1.3 Configurar red Docker ✅ (openclaw-network)
- [x] 0.1.4 Preparar dominios/subdominios ✅ (livekit.alvarezconsult.es, livekit-api.alvarezconsult.es)
- [x] 0.2.1 Configurar LiveKit server (Docker) ✅
- [x] 0.2.2 Generar API keys locales ✅
- [x] 0.2.3 Configurar livekit-server.yaml ✅
- [x] 0.3.1 Leer LiveKit docs completas ✅
- [x] 0.3.2 Estudiar Agents Framework examples ✅
- [x] 0.3.3 Revisar SIP integration guide ✅
- [x] 0.3.4 Crear checklist de prerequisitos ✅

---

#### Sprint 1: LiveKit Server (Semana 2)

**Estado:** ✅ Completado
**Duración:** 2026-03-17 a 2026-03-24

| Hito | Estado | Progreso |
|------|--------|----------|
| 1.1 Docker Compose | ✅ Completado | 100% |
| 1.2 LiveKit CLI | ✅ Completado | 100% |
| 1.3 Web Client Test | ✅ Completado | 100% |

**Checklist Sprint 1:**
- [x] 1.1.1 Crear docker-compose.yml para LiveKit ✅
- [x] 1.1.2 Configurar Redis (requerido) ✅
- [x] 1.1.3 Configurar PostgreSQL (opcional) ✅ (no requerido)
- [x] 1.1.4 Configurar LiveKit server YAML ✅
- [x] 1.2.1 Instalar LiveKit CLI ✅ (v2.15.0)
- [x] 1.2.2 Autenticar con proyecto ✅ (config manual)
- [x] 1.2.3 Crear rooms de test ✅ (openclaw-test-1)
- [x] 1.2.4 Verificar conectividad ✅
- [x] 1.3.1 Deploy LiveKit example web client ✅
- [x] 1.3.2 Probar conexión desde browser ✅
- [x] 1.3.3 Probar audio/video ✅ (web client con token API)
- [x] 1.3.4 Verificar latencia ✅

---

#### Sprint 2: LiveKit Agents (Semana 3)

**Estado:** ⏳ Pendiente  
**Duración:** 2026-03-24 a 2026-03-31

| Hito | Estado | Progreso |
|------|--------|----------|
| 2.1 Agents Framework | ⏳ Pendiente | 0% |
| 2.2 Voice Agent Base | ⏳ Pendiente | 0% |
| 2.3 Custom Agent | ⏳ Pendiente | 0% |

**Checklist Sprint 2:**
- [ ] 2.1.1 Instalar livekit-agents (pip)
- [ ] 2.1.2 Crear worker básico
- [ ] 2.1.3 Configurar connection a LiveKit
- [ ] 2.1.4 Deploy worker
- [ ] 2.2.1 Usar template oficial de voice agent
- [ ] 2.2.2 Configurar STT/TTS (proveedores default)
- [ ] 2.2.3 Probar conversación básica
- [ ] 2.2.4 Ajustar latencia
- [ ] 2.3.1 Crear agente personalizado
- [ ] 2.3.2 Añadir system prompt personalizado
- [ ] 2.3.3 Integrar con OpenClaw Memory
- [ ] 2.3.4 Testear conversación completa

---

#### Sprint 3: TTS Adapter (Semana 4)

**Estado:** ⏳ Pendiente  
**Duración:** 2026-03-31 a 2026-04-07

| Hito | Estado | Progreso |
|------|--------|----------|
| 3.1 TTS Server Base | ⏳ Pendiente | 0% |
| 3.2 Piper TTS | ⏳ Pendiente | 0% |
| 3.3 Coqui XTTS | ⏳ Pendiente | 0% |
| 3.4 LiveKit TTS Plugin | ⏳ Pendiente | 0% |
| 3.5 Voice Manager | ⏳ Pendiente | 0% |

**Checklist Sprint 3:**
- [ ] 3.1.1 Crear API REST para TTS
- [ ] 3.1.2 Endpoint: POST /tts/generate
- [ ] 3.1.3 Endpoint: GET /tts/voices
- [ ] 3.1.4 Endpoint: GET /tts/models
- [ ] 3.2.1 Instalar Piper (Docker o local)
- [ ] 3.2.2 Descargar voces en español
- [ ] 3.2.3 Integrar con TTS Server
- [ ] 3.2.4 Testear generación de audio
- [ ] 3.3.1 Instalar Coqui XTTS (Docker)
- [ ] 3.3.2 Configurar modelo en español
- [ ] 3.3.3 Integrar con TTS Server
- [ ] 3.3.4 Comparar calidad vs velocidad
- [ ] 3.4.1 Crear plugin TTS para LiveKit
- [ ] 3.4.2 Implementar interfaz oficial
- [ ] 3.4.3 Conectar con TTS Server
- [ ] 3.4.4 Testear en agente de voz
- [ ] 3.5.1 Crear dashboard de gestión
- [ ] 3.5.2 Listar voces disponibles
- [ ] 3.5.3 Configurar voz por defecto
- [ ] 3.5.4 Clasificar por: empresa, idioma, peso

---

#### Sprint 4: STT Adapter (Semana 5)

**Estado:** ⏳ Pendiente  
**Duración:** 2026-04-07 a 2026-04-14

| Hito | Estado | Progreso |
|------|--------|----------|
| 4.1 STT Server Base | ⏳ Pendiente | 0% |
| 4.2 Faster-Whisper | ⏳ Pendiente | 0% |
| 4.3 Whisper | ⏳ Pendiente | 0% |
| 4.4 LiveKit STT Plugin | ⏳ Pendiente | 0% |

**Checklist Sprint 4:**
- [ ] 4.1.1 Crear API REST para STT
- [ ] 4.1.2 Endpoint: POST /stt/transcribe
- [ ] 4.1.3 Endpoint: POST /stt/stream
- [ ] 4.1.4 Soporte para audio streaming
- [ ] 4.2.1 Instalar Faster-Whisper
- [ ] 4.2.2 Descargar modelo en español
- [ ] 4.2.3 Integrar con STT Server
- [ ] 4.2.4 Optimizar para baja latencia
- [ ] 4.3.1 Instalar Whisper oficial
- [ ] 4.3.2 Configurar modelo (small/medium)
- [ ] 4.3.3 Integrar con STT Server
- [ ] 4.3.4 Comparar precisión vs velocidad
- [ ] 4.4.1 Crear plugin STT para LiveKit
- [ ] 4.4.2 Implementar interfaz oficial
- [ ] 4.4.3 Conectar con STT Server
- [ ] 4.4.4 Testear en agente de voz

---

#### Sprint 5: LLM Intermediario (Semana 6)

**Estado:** ⏳ Pendiente  
**Duración:** 2026-04-14 a 2026-04-21

| Hito | Estado | Progreso |
|------|--------|----------|
| 5.1 Ollama Server | ⏳ Pendiente | 0% |
| 5.2 llama.cpp | ⏳ Pendiente | 0% |
| 5.3 Model Manager | ⏳ Pendiente | 0% |
| 5.4 API Router | ⏳ Pendiente | 0% |

**Checklist Sprint 5:**
- [ ] 5.1.1 Instalar Ollama (Docker o nativo)
- [ ] 5.1.2 Descargar modelos ligeros (Llama 3.1 8B, Mistral 7B)
- [ ] 5.1.3 Configurar API endpoint
- [ ] 5.1.4 Testear generación de texto
- [ ] 5.2.1 Instalar llama.cpp
- [ ] 5.2.2 Descargar modelos cuantizados (GGUF)
- [ ] 5.2.3 Configurar servidor API
- [ ] 5.2.4 Comparar rendimiento vs Ollama
- [ ] 5.3.1 Crear dashboard de gestión
- [ ] 5.3.2 Listar modelos disponibles
- [ ] 5.3.3 Configurar modelo por defecto
- [ ] 5.3.4 Clasificar por: empresa, tamaño, idioma
- [ ] 5.4.1 Crear router OpenAI-compatible
- [ ] 5.4.2 Soporte para múltiples backends
- [ ] 5.4.3 Fallback automático
- [ ] 5.4.4 Rate limiting por modelo

---

#### Sprint 6: SIP Integration (Semana 7)

**Estado:** ⏳ Pendiente  
**Duración:** 2026-04-21 a 2026-04-28

| Hito | Estado | Progreso |
|------|--------|----------|
| 6.1 LiveKit SIP Trunk | ⏳ Pendiente | 0% |
| 6.2 Tu Número Fijo | ⏳ Pendiente | 0% |
| 6.3 SIP Ingress | ⏳ Pendiente | 0% |
| 6.4 Centralita Virtual | ⏳ Pendiente | 0% |

**Checklist Sprint 6:**
- [ ] 6.1.1 Configurar SIP trunk en LiveKit
- [ ] 6.1.2 Obtener SIP credentials
- [ ] 6.1.3 Configurar inbound rules
- [ ] 6.1.4 Configurar outbound rules
- [ ] 6.2.1 Obtener SIP credentials de tu proveedor
- [ ] 6.2.2 Configurar en LiveKit
- [ ] 6.2.3 Testear inbound (llamar al fijo → Room)
- [ ] 6.2.4 Testear outbound (Room → llamar al fijo)
- [ ] 6.3.1 Configurar SIP → WebRTC ingress
- [ ] 6.3.2 Testear calidad de audio
- [ ] 6.3.3 Ajustar codecs (G.711, Opus)
- [ ] 6.3.4 Verificar latencia
- [ ] 6.4.1 Crear IVR básico
- [ ] 6.4.2 Menú de opciones ("Presiona 1 para...")
- [ ] 6.4.3 Routing a diferentes agentes
- [ ] 6.4.4 Testear flujo completo

---

#### Sprint 7: Egress/Ingress (Semana 8)

**Estado:** ⏳ Pendiente  
**Duración:** 2026-04-28 a 2026-05-05

| Hito | Estado | Progreso |
|------|--------|----------|
| 7.1 Egress (Grabación) | ⏳ Pendiente | 0% |
| 7.2 Egress (Streaming) | ⏳ Pendiente | 0% |
| 7.3 Ingress (RTMP) | ⏳ Pendiente | 0% |
| 7.4 Ingress (SIP) | ⏳ Pendiente | 0% |

**Checklist Sprint 7:**
- [ ] 7.1.1 Configurar room egress
- [ ] 7.1.2 Grabar a MP4/WebM
- [ ] 7.1.3 Guardar en disco/S3
- [ ] 7.1.4 Testear grabación completa
- [ ] 7.2.1 Configurar RTMP egress
- [ ] 7.2.2 Stream a YouTube/Twitch
- [ ] 7.2.3 Testear streaming en vivo
- [ ] 7.2.4 Verificar latencia de stream
- [ ] 7.3.1 Configurar RTMP ingress
- [ ] 7.3.2 Conectar OBS
- [ ] 7.3.3 Stream OBS → LiveKit Room
- [ ] 7.3.4 Testear calidad
- [ ] 7.4.1 Configurar SIP ingress
- [ ] 7.4.2 Llamar desde teléfono → Room
- [ ] 7.4.3 Verificar transcoding
- [ ] 7.4.4 Testear múltiples llamadas

---

#### Sprint 8: Integración OpenClaw (Semana 9)

**Estado:** ⏳ Pendiente  
**Duración:** 2026-05-05 a 2026-05-12

| Hito | Estado | Progreso |
|------|--------|----------|
| 8.1 API Integration | ⏳ Pendiente | 0% |
| 8.2 Memoria Compartida | ⏳ Pendiente | 0% |
| 8.3 Permisos Unificados | ⏳ Pendiente | 0% |
| 8.4 Logs Centralizados | ⏳ Pendiente | 0% |

**Checklist Sprint 8:**
- [ ] 8.1.1 Voice Agent → OpenClaw API
- [ ] 8.1.2 OpenClaw Agents → Voice TTS
- [ ] 8.1.3 Shared authentication
- [ ] 8.1.4 Error handling
- [ ] 8.2.1 Voice → Memory Store (conversaciones)
- [ ] 8.2.2 Memory Store → Voice (contexto)
- [ ] 8.2.3 Qdrant RAG para ambos
- [ ] 8.2.4 User profiles compartidos
- [ ] 8.3.1 RBAC para voz (mismos dominios)
- [ ] 8.3.2 Human-in-the-loop para voz
- [ ] 8.3.3 Audit trail de llamadas
- [ ] 8.3.4 Rate limiting por usuario
- [ ] 8.4.1 Voice logs → JSON logging
- [ ] 8.4.2 Mismo formato que OpenClaw
- [ ] 8.4.3 Dashboard unificado
- [ ] 8.4.4 Alertas de seguridad

---

#### Sprint 9: Testing + Docs (Semana 10)

**Estado:** ⏳ Pendiente  
**Duración:** 2026-05-12 a 2026-05-19

| Hito | Estado | Progreso |
|------|--------|----------|
| 9.1 E2E Testing | ⏳ Pendiente | 0% |
| 9.2 Security Testing | ⏳ Pendiente | 0% |
| 9.3 Documentación | ⏳ Pendiente | 0% |
| 9.4 Dashboard Unificado | ⏳ Pendiente | 0% |

**Checklist Sprint 9:**
- [ ] 9.1.1 Testear flujo completo (teléfono → agente → respuesta)
- [ ] 9.1.2 Testear fallbacks (si TTS falla, usar backup)
- [ ] 9.1.3 Testear carga (múltiples llamadas simultáneas)
- [ ] 9.1.4 Medir latencia end-to-end
- [ ] 9.2.1 Penetration testing básico
- [ ] 9.2.2 Verificar autenticación SIP
- [ ] 9.2.3 Verificar rate limiting
- [ ] 9.2.4 Verificar audit trail
- [ ] 9.3.1 Documentar arquitectura completa
- [ ] 9.3.2 Documentar cada componente
- [ ] 9.3.3 Crear guías de troubleshooting
- [ ] 9.3.4 Actualizar CHANGELOG
- [ ] 9.4.1 Extender openclaw-dashboard
- [ ] 9.4.2 Añadir métricas de voz
- [ ] 9.4.3 Añadir gestión de agentes
- [ ] 9.4.4 Añadir monitoring en tiempo real

---

## 📈 MÉTRICAS GENERALES

### Progreso por Fase

| Fase | Componentes | Completados | Progreso |
|------|-------------|-------------|----------|
| Fase 1: OpenClaw Básico | 11 | 11 | ✅ 100% |
| Fase 2: LiveKit Integration | 8 | 0 | 🟡 0% |

### Progreso por Sprint

| Sprint | Hitos | Completados | Progreso |
|--------|-------|-------------|----------|
| Sprint 0 | 3 | 0 | 🟡 0% |
| Sprint 1 | 3 | 0 | 🟡 0% |
| Sprint 2 | 3 | 0 | 🟡 0% |
| Sprint 3 | 5 | 0 | 🟡 0% |
| Sprint 4 | 4 | 0 | 🟡 0% |
| Sprint 5 | 4 | 0 | 🟡 0% |
| Sprint 6 | 4 | 0 | 🟡 0% |
| Sprint 7 | 4 | 0 | 🟡 0% |
| Sprint 8 | 4 | 0 | 🟡 0% |
| Sprint 9 | 4 | 0 | 🟡 0% |

### Total Checklists

| Tipo | Cantidad |
|------|----------|
| **Total Checklists** | 42 |
| **Total Items** | ~170 |
| **Completados** | 11 (Fase 1) |
| **Pendientes** | ~159 |

---

## 🎯 PRÓXIMOS PASOS INMEDIATOS

### ESTA SEMANA (Sprint 0)

**Objetivo:** Tener toda la infraestructura lista

1. **Hito 0.1:** Infrastructure Setup
   - [ ] Verificar VPS specs
   - [ ] Instalar Docker
   - [ ] Configurar red Docker
   - [ ] Preparar dominios

2. **Hito 0.2:** LiveKit Account
   - [ ] Crear cuenta LiveKit Cloud
   - [ ] Obtener API keys
   - [ ] Configurar proyecto

3. **Hito 0.3:** Documentación
   - [ ] Leer docs de LiveKit
   - [ ] Estudiar Agents Framework
   - [ ] Revisar SIP integration

---

## 🔗 ENLACES ÚTILES

| Recurso | URL |
|---------|-----|
| **GitHub Repo** | https://github.com/Ruben-Alvarez-Dev/OPENCLAW-city |
| **LiveKit Docs** | https://docs.livekit.io |
| **Agents Framework** | https://github.com/livekit/agents |
| **LiveKit CLI** | https://github.com/livekit/livekit-cli |
| **SIP Integration** | https://docs.livekit.io/realtime/sip/overview/ |
| **Project Board** | https://github.com/Ruben-Alvarez-Dev/OPENCLAW-city/projects (por crear) |

---

**Última actualización:** 2026-03-10  
**Próxima actualización:** Después de Sprint 0  
**Estado:** Fase 1 ✅ Completada, Fase 2 🟡 Planificada
