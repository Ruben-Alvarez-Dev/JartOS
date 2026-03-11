# 🎯 OPENCLAW + LIVEKIT + ZADARMA - PLAN MAESTRO

**Fecha:** 2026-03-11  
**Estado General:** 🟡 En progreso  
**Prioridad:** Zadarma SIP → LiveKit → OpenClaw Integration

---

## 📊 ESTADO POR COMPONENTE

| Componente | Estado | Completado | Notas |
|------------|--------|------------|-------|
| **OpenClaw Gateway** | ✅ Funcionando | 100% | Puerto 18789 |
| **Ramiro (Telegram)** | ✅ Funcionando | 100% | MiniMax M2.5 |
| **LiveKit Server** | ✅ Funcionando | 90% | Sin TURN configurado |
| **A2A Protocol** | ✅ Funcionando | 100% | Puerto 18790 |
| **Zadarma SIP** | ⏳ Pendiente | 50% | Credenciales guardadas, falta activar desvío |
| **Voice Agent** | ⏳ Pendiente | 30% | Worker creado, falta integrar |
| **TTS/STT** | ⏳ Pendiente | 0% | Sprint 3-4 |
| **LLM Local** | ⏳ Pendiente | 0% | Sprint 5 (Ollama) |

---

## 🎯 OBJETIVOS INMEDIATOS (ESTA SEMANA)

### 1. ✅ ZADARMA SIP TRUNK FUNCIONANDO
- [x] Firewall configurado (puertos 5060, 10000-20000)
- [x] Credenciales guardadas (`/etc/openclaw/secrets/`)
- [ ] **PENDIENTE:** Activar desvío en panel Zadarma
- [ ] **PENDIENTE:** Testear llamada entrante
- [ ] **PENDIENTE:** Enrutar a LiveKit room

### 2. ✅ LIVEKIT VOICE AGENT
- [x] LiveKit Server activo
- [x] livekit-agents instalado (v1.4.4)
- [ ] **PENDIENTE:** Worker conectado a LiveKit
- [ ] **PENDIENTE:** STT configurado (Silero)
- [ ] **PENDIENTE:** TTS configurado
- [ ] **PENDIENTE:** Integración con OpenClaw Memory

### 3. ✅ OPENCLAW INTEGRATION
- [x] A2A Protocol funcionando
- [x] MiniMax LLM configurado
- [ ] **PENDIENTE:** Voice Agent → OpenClaw API
- [ ] **PENDIENTE:** OpenClaw Memory → Voice context
- [ ] **PENDIENTE:** RAG search para respuestas

---

## 📅 SPRINTS RESTANTES

### Sprint 2 (ACTUAL): LiveKit Agents + OpenClaw
**Duración:** 2026-03-10 a 2026-03-17  
**Estado:** 🟡 60% completado

**Pendientes:**
1. Activar Zadarma SIP trunk
2. Deploy voice agent worker
3. Integrar con OpenClaw Memory/RAG
4. Test end-to-end

### Sprint 3: TTS Adapter
**Duración:** 2026-03-17 a 2026-03-24

**Objetivos:**
- [ ] Piper TTS (ligero, español)
- [ ] Coqui XTTS (pesado, calidad)
- [ ] LiveKit TTS Plugin
- [ ] Voice Manager dashboard

### Sprint 4: STT Adapter
**Duración:** 2026-03-24 a 2026-03-31

**Objetivos:**
- [ ] Faster-Whisper (español)
- [ ] Whisper oficial
- [ ] LiveKit STT Plugin
- [ ] Streaming STT

### Sprint 5: LLM Intermediario
**Duración:** 2026-03-31 a 2026-04-07

**Objetivos:**
- [ ] Ollama Server
- [ ] llama.cpp
- [ ] Model Manager
- [ ] API Router OpenAI-compatible

### Sprint 6: SIP Integration
**Duración:** 2026-04-07 a 2026-04-14

**Objetivos:**
- [ ] LiveKit SIP Trunk
- [ ] Número fijo → SIP
- [ ] SIP Ingress → Room
- [ ] IVR básico

### Sprint 7: Egress/Ingress
**Duración:** 2026-04-14 a 2026-04-21

**Objetivos:**
- [ ] Room Egress (grabación)
- [ ] RTMP Egress (streaming)
- [ ] RTMP Ingress (OBS)
- [ ] SIP Ingress múltiple

### Sprint 8: Integración OpenClaw Completa
**Duración:** 2026-04-21 a 2026-04-28

**Objetivos:**
- [ ] Voice Agent ↔ OpenClaw API
- [ ] Memoria compartida
- [ ] Permisos unificados
- [ ] Logs centralizados

### Sprint 9: Testing + Docs
**Duración:** 2026-04-28 a 2026-05-05

**Objetivos:**
- [ ] E2E Testing
- [ ] Security Testing
- [ ] Documentación completa
- [ ] Dashboard unificado

---

## 🔥 PRIORIDADES ACTUALES (ORDEN)

1. **Zadarma SIP Trunk** (activar en panel)
2. **LiveKit Voice Agent** (deploy worker)
3. **OpenClaw Integration** (Memory/RAG)
4. **TTS/STT** (Sprint 3-4)
5. **LLM Local** (Sprint 5)

---

## 📊 MÉTRICAS GENERALES

| Métrica | Valor |
|---------|-------|
| **Total Sprints** | 9 |
| **Completados** | 1 (Sprint 0-1) |
| **En progreso** | 1 (Sprint 2) |
| **Pendientes** | 7 |
| **Progreso Total** | 24% (30/127 TODOs) |

---

## 🔒 SEGURIDAD

| Componente | Estado | Notas |
|------------|--------|-------|
| **Secrets** | ✅ Asegurados | `/etc/openclaw/secrets/` (600) |
| **Git** | ✅ Protegido | .gitignore actualizado |
| **Monitorización** | ✅ Activa | Cada 5 minutos |
| **Incidente 2026-03-11** | ✅ Mitigado | Keys expuestas → monitorizadas |

---

## 📝 NOTAS IMPORTANTES

### Zadarma
- API keys NO se pueden revocar
- Credenciales en `/etc/openclaw/secrets/openclaw.env`
- Monitorizar uso por si hay abuso

### LiveKit
- Server funcionando SIN TURN (suficiente para testing)
- TURN se puede añadir después con certificados válidos

### MiniMax
- API Key expuesta en git (no revocable)
- Monitorizar uso en dashboard de MiniMax
- Considerar crear nueva cuenta si hay abuso

### Ramiro
- Usando MiniMax M2.5
- Temperatura 0.1 (fija)
- Historial 100 mensajes
- **USAR CONSTANTEMENTE** para todo

---

## 🎯 CRITERIOS DE COMPLETACIÓN

### Zadarma SIP Trunk ✅
- [ ] Llamada entrante → LiveKit room
- [ ] Llamada saliente → LiveKit → Zadarma
- [ ] Audio bidireccional funcionando

### Voice Agent ✅
- [ ] Worker conectado a LiveKit
- [ ] STT transcribiendo audio
- [ ] LLM generando respuestas
- [ ] TTS hablando respuestas
- [ ] Latencia total < 3 segundos

### OpenClaw Integration ✅
- [ ] Voice Agent consulta Memory Store
- [ ] Voice Agent usa RAG Store
- [ ] Conversaciones guardadas en Memory
- [ ] Contexto persistente entre llamadas

---

**Última actualización:** 2026-03-11  
**Próxima revisión:** Después de activar Zadarma SIP trunk
