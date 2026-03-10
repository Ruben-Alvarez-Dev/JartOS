# 📱 A2A TELEGRAM NOTIFICATIONS - GUÍA DE USO

**Fecha:** 2026-03-10  
**Estado:** ✅ Funcionando  
**Telegram Chat ID:** 795606301

---

## 📋 RESUMEN

Todas las comunicaciones A2A entre el **MCP Orchestrator** y **OpenClaw Gateway** se registran y envían en tiempo real a Telegram.

---

## 🔧 COMPONENTES

### 1. A2A Logger (`orchestrator/a2a_logger.py`)

Clase principal que gestiona:
- Registro de todas las comunicaciones en JSON
- Notificaciones Telegram en tiempo real
- Resúmenes de sesión automáticos

### 2. A2A Communication Script (`orchestrator/a2a_communication.py`)

Script que:
- Envía comandos A2A a OpenClaw
- Registra cada comunicación
- Notifica cada evento por Telegram

### 3. Logs

| Archivo | Ubicación | Propósito |
|---------|-----------|-----------|
| **Comunicaciones** | `/var/log/openclaw/a2a/a2a_communications.json` | Log completo en JSON |
| **Notificaciones** | `/var/log/openclaw/a2a/telegram_notifications.log` | Log de envíos Telegram |

---

## 📱 MENSAJES TELEGRAM

### Formato de Notificación

Cada comunicación A2A genera un mensaje como:

```
📤 A2A Communication #1 ✅

Type: `HANDSHAKE`
Direction: outbound
From: MCP-Orchestrator
To: OpenClaw-Gateway
Status: `sent`
Time: `21:33:24`

Payload:
```json
{
  "type": "HANDSHAKE",
  "timestamp": "2026-03-10T21:33:24...",
  "orchestrator": "MCP-Server",
  "payload": {...}
}
```
```

### Emojis por Dirección

| Emoji | Significado |
|-------|-------------|
| 📤 | Outbound (MCP → OpenClaw) |
| 📥 | Inbound (OpenClaw → MCP) |
| ✅ | Success (sent/received/accepted) |
| ❌ | Error (error/rejected) |
| ⏳ | Pending |

---

## 📊 RESUMEN DE SESIÓN

Al final de cada sesión, se envía un resumen:

```
📊 A2A Session Summary

Session ID: `session-20260310-213324`
Started: `2026-03-10T21:33:24`
Total Communications: 14

By Direction:
  📤 Outbound: 7
  📥 Inbound: 7

By Type:
  • HANDSHAKE: 2
  • COMMAND: 10
  • STATUS_REQUEST: 2

Log File: `/var/log/openclaw/a2a/a2a_communications.json`
```

---

## 🔍 CONSULTAR LOGS

### Ver comunicaciones recientes

```bash
# Últimas 10 comunicaciones
cat /var/log/openclaw/a2a/a2a_communications.json | python3 -m json.tool | tail -50

# Comunicaciones por tipo
cat /var/log/openclaw/a2a/a2a_communications.json | \
  python3 -c "import json,sys; d=json.load(sys.stdin); \
  print(f\"Total: {d['total_communications']}\"); \
  types={}; [types.update({c['type']: types.get(c['type'],0)+1}) for c in d['communications']]; \
  print(types)"
```

### Ver notificaciones Telegram

```bash
# Últimas notificaciones
tail -20 /var/log/openclaw/a2a/telegram_notifications.log

# Notificaciones fallidas
grep "Failed" /var/log/openclaw/a2a/telegram_notifications.log
```

---

## 🛠️ COMANDOS ÚTILES

### Reiniciar notificaciones

```bash
cd /root/OPENCLAW-city/orchestrator
python3 a2a_communication.py
```

### Ver estado del logger

```bash
python3 -c "
import json
with open('/var/log/openclaw/a2a/a2a_communications.json') as f:
    data = json.load(f)
    print(f\"Session: {data['session_id']}\")
    print(f\"Total: {data['total_communications']}\")
    print(f\"Started: {data['started_at']}\")
"
```

---

## 📊 ESTADÍSTICAS EN TIEMPO REAL

```bash
# Comunicaciones por minuto
watch -n 5 'cat /var/log/openclaw/a2a/telegram_notifications.log | wc -l'

# Errores recientes
grep "Error\|Failed" /var/log/openclaw/a2a/telegram_notifications.log | tail -10
```

---

## 🔗 ENLACES RELACIONADOS

- [A2A Communication Protocol](./docs/A2A-COMMUNICATION.md)
- [LiveKit-OpenClaw Integration](./docs/LIVEKIT-OPENCLAW-INTEGRATION.md)
- [MCP Orchestrator](./orchestrator/mcp_orchestrator.py)

---

**Última actualización:** 2026-03-10  
**Estado:** ✅ Funcionando  
**Total Comunicaciones Registradas:** 14  
**Notificaciones Telegram Enviadas:** 14+
