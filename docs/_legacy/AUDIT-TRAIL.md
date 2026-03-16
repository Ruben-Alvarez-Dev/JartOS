# 📝 Audit Trail

**Logging y Auditoría del Sistema**

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Visión General](#1-visión-general)
2. [Tipos de Logs](#2-tipos-de-logs)
3. [Security Logs](#3-security-logs)
4. [Métricas y Observabilidad](#4-métricas-y-observabilidad)
5. [Retención de Logs](#5-retención-de-logs)
6. [Consultas y Análisis](#6-consultas-y-análisis)

---

## 1. Visión General

El **Audit Trail** de OpenClaw registra todas las acciones importantes del sistema para:

- ✅ **Seguridad:** Detectar accesos no autorizados
- ✅ **Auditoría:** Trazabilidad completa de acciones
- ✅ **Troubleshooting:** Diagnosticar problemas
- ✅ **Compliance:** Cumplir con políticas de seguridad
- ✅ **Análisis:** Entender patrones de uso

---

## 2. Tipos de Logs

### 2.1 Logs de Aplicación

| Log | Ubicación | Propósito | Rotación |
|-----|-----------|-----------|----------|
| **Gateway** | `journalctl -u openclaw` | Logs del servicio gateway | systemd journal |
| **Email Bridge** | `/var/log/openclaw/email_bridge.log` | Actividad de email | 30 días |
| **Orchestrator** | `/var/log/openclaw/orchestrator_bot.log` | Actividad de Telegram | 30 días |
| **Security Audit** | `/var/log/openclaw/security_audit.log` | Auditorías de seguridad | 90 días |
| **Watchdog** | `/var/log/openclaw-watchdog/` | Monitoreo de configuración | 30 días |

### 2.2 Logs de Sistema

| Log | Ubicación | Propósito |
|-----|-----------|-----------|
| **Auth** | `/var/log/auth.log` | Autenticación SSH, sudo |
| **Syslog** | `/var/log/syslog` | Logs generales del sistema |
| **UFW** | `/var/log/ufw.log` | Firewall events |
| **Tailscale** | `journalctl -u tailscaled` | Actividad de Tailscale |

### 2.3 Logs en Database

**Database:** `/var/lib/openclaw/memory.db`

| Tabla | Propósito | Retención |
|-------|-----------|-----------|
| `conversations` | Mensajes de conversaciones | Indefinida |
| `security_logs` | Eventos de seguridad | 90 días |
| `metrics` | Métricas de rendimiento | 30 días |

---

## 3. Security Logs

### 3.1 Tipos de Eventos

| Event Type | Severidad | Descripción | Ejemplo |
|------------|-----------|-------------|---------|
| `UNAUTHORIZED_ACCESS` | warn | Intento de acceso no autorizado | Usuario no en allowlist |
| `UNAUTHORIZED_MESSAGE` | warn | Mensaje de usuario no autorizado | Mensaje de Telegram rechazado |
| `MISTRAL_ERROR` | error | Error de API de Mistral | Timeout, error 500 |
| `MISTRAL_API_ERROR` | error | Error HTTP de Mistral | 401, 403, 429 |
| `MISTRAL_TIMEOUT` | warn | Timeout de Mistral | >60s sin respuesta |
| `BOT_STARTED` | info | Bot iniciado | Startup del orchestrator |
| `BOT_RUNNING` | info | Bot en ejecución | Health check exitoso |
| `SECURITY_CHECK` | info/warn | Check de seguridad | Auditoría hourly |
| `CONFIG_CHANGED` | warn | Configuración modificada | Watchdog detecta cambio |
| `HEALTH_CHECK_FAILED` | error | Health check fallido | Gateway no responde |

### 3.2 Estructura de Security Log

**Tabla:** `security_logs`

```sql
CREATE TABLE security_logs (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    event_type TEXT,
    severity TEXT,
    user_id TEXT,
    channel TEXT,
    details JSON,
    ip_address TEXT,
    resolved BOOLEAN,
    resolved_at DATETIME,
    resolved_by TEXT
);
```

### 3.3 Ejemplos de Logs

#### Unauthorized Access

```json
{
  "timestamp": "2026-03-10T15:30:00Z",
  "event_type": "UNAUTHORIZED_ACCESS",
  "severity": "warn",
  "user_id": "telegram:999999999",
  "channel": "telegram",
  "details": {
    "user": "unknown_user",
    "name": "Unknown"
  },
  "resolved": false
}
```

#### Mistral API Error

```json
{
  "timestamp": "2026-03-10T14:45:00Z",
  "event_type": "MISTRAL_API_ERROR",
  "severity": "error",
  "details": {
    "status_code": 429,
    "response": "Rate limit exceeded"
  },
  "resolved": true,
  "resolved_at": "2026-03-10T14:46:00Z"
}
```

#### Security Check

```json
{
  "timestamp": "2026-03-10T15:00:00Z",
  "event_type": "SECURITY_CHECK",
  "severity": "info",
  "details": {
    "security_score": 95,
    "anomalies_count": 0,
    "services_healthy": true
  },
  "resolved": true
}
```

### 3.4 Ver Security Logs

```bash
# Dashboard interactivo
openclaw-dashboard <<< "security 20"

# Output:
# 🔒 LOGS DE SEGURIDAD (últimos 20)
# ============================================================
# ✅ 2026-03-10 15:30:00 ℹ️ SECURITY_CHECK
# ✅ 2026-03-10 14:30:00 ℹ️ SECURITY_CHECK
# ⏳ 2026-03-10 13:15:00 ⚠️ UNAUTHORIZED_ACCESS
# ...
```

```bash
# Consultar database directamente
sqlite3 /var/lib/openclaw/memory.db <<EOF
SELECT timestamp, event_type, severity, details
FROM security_logs
ORDER BY timestamp DESC
LIMIT 20;
EOF
```

### 3.5 Resolver Eventos

```python
from memory_store import get_memory_store

memory = get_memory_store()

# Resolver evento de seguridad
memory.resolve_security_event(
    event_id=1,
    resolved_by="admin"
)
```

---

## 4. Métricas y Observabilidad

### 4.1 Tipos de Métricas

**Tabla:** `metrics`

```sql
CREATE TABLE metrics (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    metric_type TEXT,
    metric_name TEXT,
    value REAL,
    labels JSON
);
```

### 4.2 Métricas Registradas

| metric_type | metric_name | Descripción | Unidad |
|-------------|-------------|-------------|--------|
| `api` | `latency_ms` | Latencia de API de Mistral | ms |
| `api` | `tokens` | Tokens usados en llamada | count |
| `bot` | `message_received` | Mensajes recibidos | count |
| `bot` | `message_sent` | Mensajes enviados | count |
| `bot` | `command_start` | Comando /start ejecutado | count |
| `bot` | `command_help` | Comando /help ejecutado | count |
| `security` | `score` | Security score | 0-100 |
| `health` | `overall` | Health overall | 0/1 |

### 4.3 Ver Métricas

```bash
# Dashboard interactivo
openclaw-dashboard <<< "metrics 24"

# Output:
# 📈 MÉTRICAS (últimas 24h)
# ============================================================
#
# API:
#   • latency_ms:
#       Count: 50
#       Avg: 145.30
#       Min: 89.50
#       Max: 312.40
#   • tokens:
#       Count: 50
#       Avg: 1250.00
#       Min: 500
#       Max: 2048
```

```bash
# Consultar database
sqlite3 /var/lib/openclaw/memory.db <<EOF
SELECT 
    metric_type,
    metric_name,
    AVG(value) as avg_value,
    COUNT(*) as count,
    MIN(value) as min_value,
    MAX(value) as max_value
FROM metrics 
WHERE timestamp > datetime('now', '-24 hours')
GROUP BY metric_type, metric_name;
EOF
```

---

## 5. Retención de Logs

### 5.1 Políticas de Retención

| Tipo de Log | Retención | Justificación |
|-------------|-----------|---------------|
| **Application logs** | 30 días | Troubleshooting reciente |
| **Security logs (resueltos)** | 90 días | Auditoría y compliance |
| **Security logs (no resueltos)** | Indefinida | Requieren atención |
| **Metrics** | 30 días | Análisis de tendencias |
| **Conversations** | Indefinida | Contexto de usuario |
| **System logs** | 90 días | Auditoría de sistema |

### 5.2 Rotación Automática

**Archivos:** `/etc/logrotate.d/openclaw*`

```
# /etc/logrotate.d/openclaw
/var/log/openclaw/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 openclaw syslog
}

# /etc/logrotate.d/openclaw-security
/var/log/openclaw/security_audit.log {
    daily
    rotate 90
    compress
    delaycompress
    missingok
    notifempty
}
```

### 5.3 Limpieza Manual

```bash
# Limpiar logs antiguos (>30 días)
sudo find /var/log/openclaw -name "*.log" -mtime +30 -delete

# Limpiar métricas antiguas
sqlite3 /var/lib/openclaw/memory.db <<EOF
DELETE FROM metrics 
WHERE timestamp < datetime('now', '-30 days');
EOF

# Limpiar security logs resueltos antiguos
sqlite3 /var/lib/openclaw/memory.db <<EOF
DELETE FROM security_logs 
WHERE resolved = 1 
  AND resolved_at < datetime('now', '-90 days');
EOF
```

---

## 6. Consultas y Análisis

### 6.1 Consultas Comunes

```bash
# Conectar a database
sqlite3 /var/lib/openclaw/memory.db
```

#### Eventos de Seguridad por Tipo

```sql
SELECT 
    event_type,
    severity,
    COUNT(*) as count,
    MAX(timestamp) as last_occurrence
FROM security_logs
GROUP BY event_type, severity
ORDER BY count DESC;
```

#### Eventos No Resueltos

```sql
SELECT 
    id,
    timestamp,
    event_type,
    severity,
    details
FROM security_logs
WHERE resolved = 0
ORDER BY timestamp DESC;
```

#### Métricas por Día

```sql
SELECT 
    DATE(timestamp) as date,
    metric_type,
    metric_name,
    AVG(value) as avg_value,
    COUNT(*) as count
FROM metrics
WHERE timestamp > datetime('now', '-30 days')
GROUP BY DATE(timestamp), metric_type, metric_name
ORDER BY date DESC;
```

#### Conversaciones por Usuario

```sql
SELECT 
    user_id,
    channel,
    COUNT(*) as message_count,
    MIN(timestamp) as first_message,
    MAX(timestamp) as last_message
FROM conversations
GROUP BY user_id, channel
ORDER BY message_count DESC;
```

### 6.2 Exportar Logs

```bash
# Exportar security logs a JSON
sqlite3 /var/lib/openclaw/memory.db <<EOF > /root/security_logs.json
.mode json
SELECT * FROM security_logs 
WHERE timestamp > datetime('now', '-30 days')
ORDER BY timestamp DESC;
EOF

# Exportar métricas a CSV
sqlite3 /var/lib/openclaw/memory.db <<EOF > /root/metrics.csv
.mode csv
.headers on
SELECT * FROM metrics 
WHERE timestamp > datetime('now', '-30 days')
ORDER BY timestamp;
EOF
```

### 6.3 Análisis con jq

```bash
# Analizar security logs exportados
cat /root/security_logs.json | jq '.[] | select(.severity == "error")'

# Contar eventos por tipo
cat /root/security_logs.json | jq 'group_by(.event_type) | map({type: .[0].event_type, count: length})'

# Ver eventos no resueltos
cat /root/security_logs.json | jq '.[] | select(.resolved == false)'
```

### 6.4 Dashboard Personalizado

```bash
#!/bin/bash
# custom-dashboard.sh

echo "=== OPENCLAW CUSTOM DASHBOARD ==="
echo "Date: $(date)"
echo ""

# Security events (últimas 24h)
echo "🔒 SECURITY EVENTS (24h):"
sqlite3 /var/lib/openclaw/memory.db <<EOF
SELECT event_type, severity, COUNT(*) as count
FROM security_logs
WHERE timestamp > datetime('now', '-24 hours')
GROUP BY event_type, severity
ORDER BY count DESC;
EOF

echo ""
echo "📈 METRICS SUMMARY (24h):"
sqlite3 /var/lib/openclaw/memory.db <<EOF
SELECT metric_type, metric_name, AVG(value) as avg, COUNT(*) as count
FROM metrics
WHERE timestamp > datetime('now', '-24 hours')
GROUP BY metric_type, metric_name;
EOF

echo ""
echo "💬 CONVERSATION STATS:"
sqlite3 /var/lib/openclaw/memory.db <<EOF
SELECT 
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(*) as total_messages,
    COUNT(DISTINCT DATE(timestamp)) as active_days
FROM conversations;
EOF
```

---

## 7. Alertas y Notificaciones

### 7.1 Configurar Alertas

**Script:** `/usr/local/bin/openclaw-alert-monitor`

```bash
#!/bin/bash
# openclaw-alert-monitor.sh

ALERT_THRESHOLD=5  # Alertar si más de N eventos no resueltos

# Contar eventos no resueltos
unresolved=$(sqlite3 /var/lib/openclaw/memory.db <<EOF
SELECT COUNT(*) FROM security_logs WHERE resolved = 0;
EOF
)

if [ "$unresolved" -gt "$ALERT_THRESHOLD" ]; then
    # Enviar alerta por Telegram
    bot_token=$(grep OPENCLAW_TELEGRAM_BOT_TOKEN /home/openclaw/.openclaw/.env | cut -d= -f2)
    chat_id="795606301"
    
    message="⚠️ ALERTA: $unresolved eventos de seguridad no resueltos"
    
    curl -s "https://api.telegram.org/bot$bot_token/sendMessage" \
        -d "chat_id=$chat_id" \
        -d "text=$message" \
        -d "parse_mode=HTML"
fi
```

### 7.2 Cron para Alertas

```cron
*/5 * * * * /usr/local/bin/openclaw-alert-monitor >> /var/log/openclaw-alerts.log 2>&1
```

---

**Fin del documento de Audit Trail**
