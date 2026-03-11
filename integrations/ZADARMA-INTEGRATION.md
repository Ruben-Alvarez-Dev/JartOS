# 📞 ZADARMA INTEGRATION - GUÍA COMPLETA

**Fecha:** 2026-03-10  
**Estado:** ✅ IMPLEMENTADA  
**Sprint:** 2 - Zadarma + LiveKit + OpenClaw

---

## 📋 RESUMEN

Integración completa de **Zadarma** (telefonía VoIP) con **LiveKit** (voz/video) y **OpenClaw** (agentes AI).

---

## 🏗️ ARQUITECTURA

```
┌─────────────────────────────────────────────────────────────────┐
│  ZADARMA (Telefonía VoIP)                                       │
│  • SIP Trunking                                                 │
│  • Números Virtuales                                            │
│  • SMS                                                          │
│  • PBX / IVR                                                    │
└─────────────────────────────────────────────────────────────────┘
         │
         │ Webhooks / API REST
         ▼
┌─────────────────────────────────────────────────────────────────┐
│  ZADARMA WEBHOOK HANDLER (puerto 18791)                         │
│  • Recepción de eventos                                         │
│  • Forward a OpenClaw A2A                                       │
└─────────────────────────────────────────────────────────────────┘
         │
         │ A2A Protocol
         ▼
┌─────────────────────────────────────────────────────────────────┐
│  OPENCLAW A2A (puerto 18790)                                    │
│  • Enrutamiento de eventos                                      │
│  • Logging y auditoría                                          │
└─────────────────────────────────────────────────────────────────┘
         │
         │ WebSocket / HTTP
         ▼
┌─────────────────────────────────────────────────────────────────┐
│  LIVEKIT (Voz/Video)                                            │
│  • Voice Agents                                                 │
│  • Rooms de conferencia                                         │
│  • STT / TTS                                                    │
└─────────────────────────────────────────────────────────────────┘
         │
         │ Memoria / RAG
         ▼
┌─────────────────────────────────────────────────────────────────┐
│  OPENCLAW GATEWAY (18789)                                       │
│  • Memory Store                                                 │
│  • RAG Store                                                    │
│  • Agentes AI                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 COMPONENTES

### 1. Zadarma API Client (`integrations/zadarma_client.py`)

```python
from integrations.zadarma_client import ZadarmaClient, ZadarmaOpenClawIntegration

# Inicializar cliente Zadarma
zadarma = ZadarmaClient(
    user_key="TU_USER_KEY",
    secret="TU_SECRET"
)

# Obtener balance
balance = zadarma.get_balance()
print(f"Balance: {balance}")

# Obtener números SIP
sip_numbers = zadarma.get_sip_numbers()

# Integración con OpenClaw
integration = ZadarmaOpenClawIntegration(zadarma)

# Enviar notificación A2A
integration.send_a2a_notification("test_event", {"data": "test"})
```

### 2. Zadarma Webhook Handler (`integrations/zadarma_webhook.py`)

Servidor Flask que recibe webhooks de Zadarma en puerto **18791**.

**Endpoints:**
- `POST /webhook/zadarma/call` - Eventos de llamadas
- `POST /webhook/zadarma/sms` - SMS recibidos
- `POST /webhook/zadarma/number_lookup` - Búsqueda de números
- `POST /webhook/zadarma/speech_recognition` - Reconocimiento de voz

---

## 📡 WEBHOOKS DE ZADARMA

### Configurar en Zadarma

1. Ve a tu panel de Zadarma
2. Configuración → PBX → Webhooks
3. Añade URL: `http://YOUR_SENSITIVE_IP:18791/webhook/zadarma/call`
4. Selecciona eventos:
   - ✅ notify_start (inicio de llamada)
   - ✅ notify_answer (contestada)
   - ✅ notify_end (finalizada)
   - ✅ notify_record (grabación disponible)
   - ✅ notify_ivr (interacción con IVR)

### Eventos Recibidos

```json
{
  "event": "notify_start",
  "call_id": "abc123",
  "from": "+34600000000",
  "to": "+34900000000",
  "sip": "1001",
  "timestamp": "2026-03-10T21:00:00Z"
}
```

---

## 🎤 FLUJO DE LLAMADA CON VOICE AGENT

### 1. Llamada Entrante

```
Usuario → Zadarma SIP → Webhook → OpenClaw A2A → LiveKit Room → Voice Agent
```

### 2. Configuración de Enrutamiento

```python
from integrations.zadarma_client import ZadarmaOpenClawIntegration

integration = ZadarmaOpenClawIntegration(zadarma)

# Enrutar llamadas al Voice Agent de LiveKit
integration.create_voice_agent_route(
    phone_number="+34900000000",
    livekit_room="voice-agent-001"
)
```

### 3. Voice Agent Responde

```python
# En voice_agent_worker.py
from livekit.plugins import silero

async def entrypoint(ctx: JobContext):
    await ctx.connect()
    
    # Cuando Zadarma enruta la llamada
    stt = silero.STT()  # Transcribir audio
    
    # Enviar texto a OpenClaw para contexto
    # Obtener respuesta del LLM
    # TTS para responder
```

---

## 📱 ENVÍO DE SMS

```python
from integrations.zadarma_client import ZadarmaClient

zadarma = ZadarmaClient(user_key="KEY", secret="SECRET")

# Enviar SMS
result = zadarma.send_sms(
    phone="+34600000000",
    message="Tu código de verificación es: 123456",
    sender="OpenClaw"
)

print(f"SMS enviado: {result}")
```

---

## 🔍 CONSULTA DE ESTADÍSTICAS

```python
# Estadísticas de llamadas
stats = zadarma.get_statistics(
    date_from="2026-03-01",
    date_to="2026-03-10"
)

# Estadísticas de PBX
pbx_stats = zadarma.get_pbx_statistics(
    pbx_id="1",
    date_from="2026-03-01",
    date_to="2026-03-10"
)
```

---

## 🛠️ INSTALACIÓN Y CONFIGURACIÓN

### 1. Instalar dependencias

```bash
pip3 install --break-system-packages requests flask httpx
```

### 2. Configurar credenciales

```bash
cat > /root/.openclaw/zadarma.env << 'EOF'
ZADARMA_USER_KEY=tu_user_key
ZADARMA_SECRET=tu_secret
ZADARMA_WEBHOOK_URL=http://YOUR_SENSITIVE_IP:18791
EOF
chmod 600 /root/.openclaw/zadarma.env
```

### 3. Iniciar Webhook Handler

```bash
cd /root/OPENCLAW-city/integrations
nohup python3 zadarma_webhook.py > /var/log/openclaw/zadarma/webhook.log 2>&1 &
```

### 4. Crear servicio systemd

```bash
cat > /etc/systemd/system/zadarma-webhook.service << 'EOF'
[Unit]
Description=Zadarma Webhook Handler
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/OPENCLAW-city/integrations
ExecStart=/usr/bin/python3 /root/OPENCLAW-city/integrations/zadarma_webhook.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable zadarma-webhook
systemctl start zadarma-webhook
```

---

## 📊 EVENTOS A2A

| Evento | Descripción | Payload |
|--------|-------------|---------|
| `call_notify_start` | Llamada iniciada | `{call_id, from, to, sip}` |
| `call_notify_answer` | Llamada contestada | `{call_id, duration}` |
| `call_notify_end` | Llamada finalizada | `{call_id, duration, cost}` |
| `call_notify_record` | Grabación disponible | `{call_id, record_url}` |
| `call_notify_ivr` | Interacción IVR | `{call_id, ivr_option}` |
| `sms_received` | SMS recibido | `{from, message, timestamp}` |
| `speech_recognition` | Transcripción | `{call_id, text}` |

---

## 🧪 TESTING

### Test de conexión

```bash
# Verificar Zadarma API
curl -X GET "https://api.zadarma.com/v1/info/balance/" \
  -H "Authorization: USER_KEY:SIGNATURE"

# Verificar Webhook Handler
curl http://localhost:18791/health

# Verificar A2A
curl http://localhost:18790/health
```

### Test de webhook

```bash
# Simular webhook de llamada
curl -X POST http://localhost:18791/webhook/zadarma/call \
  -H "Content-Type: application/json" \
  -d '{
    "event": "notify_start",
    "call_id": "test-123",
    "from": "+34600000000",
    "to": "+34900000000"
  }'
```

---

## 🔗 ENLACES RELACIONADOS

- [Zadarma API Docs](https://zadarma.com/en/support/api/)
- [Zadarma GitHub](https://github.com/Zadarma)
- [OpenClaw A2A Protocol](./docs/A2A-COMMUNICATION.md)
- [LiveKit Agents](https://docs.livekit.io/agents/)

---

**Estado:** ✅ IMPLEMENTADA  
**Próximo:** Configurar credenciales reales y probar con llamadas entrantes
