# 📞 ZADARMA + LIVEKIT INTEGRATION

**Fecha:** 2026-03-11  
**Estado:** 🟡 En progreso  
**Sprint:** 2

---

## 🎯 OBJETIVO

Enrutar llamadas PSTN desde Zadarma → LiveKit → Voice Agent → OpenClaw

---

## 📋 ARQUITECTURA

```
┌─────────────┐      SIP       ┌─────────────┐
│  ZADARMA    │ ─────────────► │   LIVEKIT   │
│  +349199... │    5060/UDP    │   SERVER    │
│  PSTN       │                │ 46.224.204  │
└─────────────┘                └──────┬──────┘
                                      │
                                      │ WebRTC
                                      ▼
                               ┌─────────────┐
                               │VOICE AGENT  │
                               │ livekit-    │
                               │ agents      │
                               └──────┬──────┘
                                      │
                                      │ A2A / HTTP
                                      ▼
                               ┌─────────────┐
                               │  OPENCLAW   │
                               │  Memory/RAG │
                               └─────────────┘
```

---

## 🔧 CONFIGURACIÓN ZADARMA

### 1. Número Virtual

```
Número: +34919935163
Estado: Activo hasta 26.02.2027
Coste: 1.7€/mes
```

### 2. Línea Externa Complementaria

```
Nombre: livekit
Servidor: YOUR_SENSITIVE_IP
Puerto: 5060
Usuario: livekit
Contraseña: livekit
```

### 3. Configuración en Panel Zadarma

```
Servicios → Números de teléfono → +34919935163 → Ajustes

Servidor externo: ACTIVADO
Dirección: +34919935163@YOUR_SENSITIVE_IP:5060
```

---

## 🔧 CONFIGURACIÓN LIVEKIT

### 1. Docker Compose

```yaml
services:
  livekit:
    image: livekit/livekit-server:latest
    ports:
      - "5060:5060/udp"   # SIP
      - "5061:5061/tcp"   # SIP TLS
      - "7880:7880"       # HTTP
      - "7881:7881"       # RTC TCP
      - "7882:7882/udp"   # RTC UDP
    environment:
      LIVEKIT_REDIS_URL: "redis://localhost:6379"
      LIVEKIT_KEYS: "openclaw-...: e60d2b7..."
      LIVEKIT_SIP_ENABLED: "true"
      LIVEKIT_SIP_PORT: "5060"
      LIVEKIT_SIP_TLS_PORT: "5061"
      LIVEKIT_SIP_EXTERNAL_IP: "YOUR_SENSITIVE_IP"
```

### 2. SIP Inbound Trunk

```python
from livekit.api import LiveKitAPI, CreateSIPInboundTrunkRequest

api = LiveKitAPI(url, api_key, api_secret)

trunk = await api.sip.create_inbound_trunk(
    CreateSIPInboundTrunkRequest(
        trunk={
            "name": "Zadarma-Inbound",
            "numbers": ["+34919935163"],
            "allowed_addresses": ["YOUR_SENSITIVE_IP"],
            "auth_username": "livekit",
            "auth_password": "livekit"
        }
    )
)
```

### 3. SIP Dispatch Rule

```python
rule = await api.sip.create_dispatch_rule(
    CreateSIPDispatchRuleRequest(
        rule={
            "trunk_ids": [trunk.id],
            "rule": {
                "dispatch_rule_direct": {
                    "room_prefix": "call-",
                    "pin": ""
                }
            }
        }
    )
)
```

---

## 🔥 PROBLEMAS CONOCIDOS

### 1. "sip not connected (redis required)"

**Error:**
```
TwirpError(code=internal, message=sip not connected (redis required))
```

**Intentos fallidos:**
- Variables de entorno `LIVEKIT_SIP_*`
- Config YAML con sección `sip:`
- Reiniciar LiveKit Server

**Posible causa:**
- LiveKit Server necesita configuración específica de Redis para SIP
- El módulo SIP puede requerir inicialización especial

**Investigando...**

---

## 📊 ESTADO ACTUAL

| Componente | Estado | Notas |
|------------|--------|-------|
| Zadarma Config | ✅ Listo | Número + SIP trunk configurados |
| LiveKit SIP | 🟡 Pendiente | Redis issue |
| Voice Agent | ✅ Deployado | voice-agent.service activo |
| Dispatch Rule | ⏳ Pendiente | Esperando SIP funcional |
| Test de llamada | ⏳ Pendiente | Esperando SIP funcional |

---

## 📝 PRÓXIMOS PASOS

1. [ ] Resolver SIP + Redis connection
2. [ ] Crear SIP Inbound Trunk
3. [ ] Crear SIP Dispatch Rule
4. [ ] Testear llamada entrante
5. [ ] Integrar con Voice Agent
6. [ ] Añadir TTS/STT

---

## 🔗 REFERENCIAS

- [LiveKit SIP Docs](https://docs.livekit.io/realtime/sip/)
- [LiveKit API SIP](https://github.com/livekit/protocol/blob/main/sip.proto)
- [Zadarma API](https://zadarma.com/es/support/api/)
- [livekit-agents](https://github.com/livekit/agents)

---

**Última actualización:** 2026-03-11
