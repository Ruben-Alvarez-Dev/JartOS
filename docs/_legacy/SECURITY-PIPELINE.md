# 🛡️ Security Pipeline

**Auditorías Automatizadas y Monitoreo de Seguridad**

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Descripción General](#1-descripción-general)
2. [Security Audits Automatizados](#2-security-audits-automatizados)
3. [Health Checks](#3-health-checks)
4. [Detección de Anomalías](#4-detección-de-anomalías)
5. [Security Scoring (0-100)](#5-security-scoring-0-100)
6. [API Reference](#6-api-reference)

---

## 1. Descripción General

La **Security Pipeline** es el sistema automatizado de auditoría y monitoreo de seguridad.

**Características:**
- ✅ Security audit de OpenClaw (automático, cada hora)
- ✅ Health check de servicios
- ✅ Verificación de Tailscale y UFW
- ✅ Detección de anomalías
- ✅ Score de seguridad (0-100)
- ✅ Log en memory_store y archivos

**Ubicación:** `/opt/openclaw-security/security_pipeline.py`  
**Ejecución:** Cron hourly (`0 * * * *`)

---

## 2. Security Audits Automatizados

### Ejecución Manual

```bash
# Auditoría básica
openclaw security audit

# Auditoría profunda
openclaw security audit --deep

# Auto-fix (cuando disponible)
openclaw security audit --fix
```

### Ejecución Automática

**Cron job:**
```cron
0 * * * * /opt/openclaw-security/security_pipeline.py >> /var/log/openclaw/security_audit.log 2>&1
```

### Output de Auditoría

```
OpenClaw Security Audit
========================

Gateway Configuration:
  ✅ Binding: loopback (127.0.0.1)
  ✅ Authentication: token required
  ✅ Session isolation: per-channel-peer

Tools Configuration:
  ✅ Profile: messaging (restricted)
  ✅ Exec security: deny
  ✅ Elevated tools: disabled

Browser Configuration:
  ✅ SSRF protection: enabled
  ✅ Private network: blocked

Discovery:
  ✅ mDNS: disabled

Summary:
  🔴 Critical: 0
  🟠 Warn: 2
  🔵 Info: 1
```

### Parsear Output

```python
def run_security_audit() -> dict:
    """Ejecutar security audit de OpenClaw"""
    try:
        result = subprocess.run(
            ["openclaw", "security", "audit"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout + result.stderr
        
        # Extraer resumen
        summary = {"critical": 0, "warn": 0, "info": 0}
        if "Summary:" in output:
            for line in output.split('\n'):
                if "Summary:" in line:
                    # Parsear: "Summary: 0 critical · 2 warn · 1 info"
                    parts = line.split('·')
                    for part in parts:
                        if 'critical' in part:
                            summary['critical'] = int(part.split()[0].strip())
                        elif 'warn' in part:
                            summary['warn'] = int(part.split()[0].strip())
                        elif 'info' in part:
                            summary['info'] = int(part.split()[0].strip())
        
        return {
            "success": True,
            "summary": summary,
            "output": output[:5000],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

---

## 3. Health Checks

### Gateway Health

```python
def check_gateway_health() -> dict:
    """Verificar salud del Gateway"""
    try:
        response = requests.get("http://127.0.0.1:18789/health", timeout=5)
        data = response.json()
        
        return {
            "healthy": data.get('ok', False),
            "status": data.get('status', 'unknown'),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "healthy": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

**Endpoint:** `GET /health`  
**Respuesta exitosa:**
```json
{
  "ok": true,
  "status": "live"
}
```

---

### Servicios Systemd

```python
def check_services() -> dict:
    """Verificar estado de servicios"""
    services = [
        "openclaw",
        "openclaw-email",
        "openclaw-orchestrator"
    ]
    
    results = {}
    for service in services:
        try:
            result = subprocess.run(
                ["systemctl", "is-active", service],
                capture_output=True,
                text=True,
                timeout=5
            )
            results[service] = result.stdout.strip()
        except:
            results[service] = "error"
    
    return {
        "services": results,
        "all_healthy": all(s == "active" for s in results.values()),
        "timestamp": datetime.now().isoformat()
    }
```

**Estados posibles:**
- `active` - Servicio corriendo
- `inactive` - Servicio detenido
- `failed` - Servicio falló
- `error` - Error al verificar

---

### Tailscale Status

```python
def check_tailscale() -> dict:
    """Verificar estado de Tailscale"""
    try:
        result = subprocess.run(
            ["tailscale", "status", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        data = json.loads(result.stdout)
        
        return {
            "active": data.get('BackendState') == 'Running',
            "self": data.get('Self', {}),
            "peer_count": len(data.get('Peer', {})),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "active": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

---

### UFW Status

```python
def check_ufw() -> dict:
    """Verificar estado de UFW"""
    try:
        result = subprocess.run(
            ["ufw", "status"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        status = "inactive"
        if "Status: active" in result.stdout:
            status = "active"
        
        return {
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

---

## 4. Detección de Anomalías

### Detectar Picos de Eventos

```python
def detect_anomalies() -> list:
    """Detectar anomalías en logs de seguridad"""
    anomalies = []
    
    # Obtener logs de seguridad no resueltos
    logs = memory.get_security_logs(limit=100, unresolved_only=True)
    
    # Contar eventos por tipo
    event_counts = {}
    for log in logs:
        event_type = log.get('event_type', 'unknown')
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
    
    # Detectar picos de eventos sospechosos
    suspicious_events = ['UNAUTHORIZED_ACCESS', 'UNAUTHORIZED_MESSAGE', 'MISTRAL_ERROR']
    
    for event_type in suspicious_events:
        count = event_counts.get(event_type, 0)
        if count > 5:  # Más de 5 eventos no resueltos
            anomalies.append({
                "type": "SECURITY_EVENT_SPIKE",
                "severity": "warn",
                "details": {
                    "event_type": event_type,
                    "count": count
                }
            })
    
    # Detectar errores de API repetidos
    error_count = event_counts.get('MISTRAL_API_ERROR', 0)
    if error_count > 3:
        anomalies.append({
            "type": "API_ERROR_RATE",
            "severity": "warn",
            "details": {
                "error_type": "MISTRAL_API_ERROR",
                "count": error_count
            }
        })
    
    return anomalies
```

### Tipos de Anomalías

| Tipo | Severidad | Descripción |
|------|-----------|-------------|
| `SECURITY_EVENT_SPIKE` | warn | Pico de eventos de seguridad |
| `API_ERROR_RATE` | warn | Tasa alta de errores de API |
| `SERVICE_DOWN` | error | Servicio caído |
| `GATEWAY_UNHEALTHY` | error | Gateway no responde |
| `FIREWALL_INACTIVE` | warn | Firewall inactivo |

---

## 5. Security Scoring (0-100)

### Cálculo del Score

```python
def calculate_security_score(audit: dict, anomalies: list) -> int:
    """Calcular score de seguridad (0-100)"""
    
    score = 100
    
    # Penalizar issues críticos
    if audit.get('summary', {}).get('critical', 0) > 0:
        score -= 50
    
    # Penalizar warnings
    if audit.get('summary', {}).get('warn', 0) > 0:
        score -= (audit['summary']['warn'] * 10)
    
    # Penalizar anomalías
    if len(anomalies) > 0:
        score -= (len(anomalies) * 5)
    
    # Asegurar rango 0-100
    return max(0, min(100, score))
```

### Interpretación del Score

| Rango | Estado | Acción |
|-------|--------|--------|
| 90-100 | ✅ Excelente | Mantener |
| 70-89 | 🟡 Bueno | Revisar warnings |
| 50-69 | 🟠 Regular | Atención requerida |
| 0-49 | 🔴 Crítico | Acción inmediata |

### Ejemplo de Cálculo

```python
# Auditoría: 0 critical, 2 warn, 1 info
# Anomalías: 1 detectada

score = 100
score -= 0  # 0 critical
score -= 20  # 2 warn × 10
score -= 5   # 1 anomaly × 5
score = 75   # Score final
```

---

## 6. API Reference

### run_full_check

```python
from security_pipeline import run_full_check

# Ejecutar chequeo completo
result = run_full_check()

# Output:
# {
#   "overall_healthy": True,
#   "security_score": 95,
#   "gateway": {"healthy": True, "status": "live"},
#   "services": {
#     "services": {
#       "openclaw": "active",
#       "openclaw-email": "active",
#       "openclaw-orchestrator": "active"
#     },
#     "all_healthy": True
#   },
#   "tailscale": {"active": True, "peer_count": 5},
#   "ufw": {"status": "active"},
#   "audit": {"success": True, "summary": {"critical": 0, "warn": 2, "info": 1}},
#   "anomalies": [],
#   "metrics": {...},
#   "timestamp": "2026-03-10T15:30:00"
# }
```

### print_report

```python
from security_pipeline import run_full_check, print_report

# Ejecutar y imprimir reporte
result = run_full_check()
print_report(result)

# Output:
# ============================================================
# 🦞 OPENCLAW SECURITY & HEALTH REPORT
# ============================================================
#
# ✅ ESTADO GENERAL: HEALTHY
# 🔒 SECURITY SCORE: 95/100
#
# 📊 SERVICIOS:
#    ✅ openclaw: active
#    ✅ openclaw-email: active
#    ✅ openclaw-orchestrator: active
#
# 🌐 TAILSCALE:
#    ✅ Estado: Activo
#    📡 Peers: 5
#
# 🔥 UFW FIREWALL:
#    ✅ Estado: active
#
# 🛡️  SECURITY AUDIT:
#    🔴 Critical: 0
#    🟠 Warn: 2
#    🔵 Info: 1
#
# ⚠️  ANOMALÍAS DETECTADAS: 0
#
# 📈 MÉTRICAS (24h):
#    • api: 50 eventos, avg: 145.30
#    • bot: 120 eventos, avg: 1.00
#    • security: 5 eventos, avg: 95.00
```

### Output JSON

```bash
# Ejecutar con output JSON
/opt/openclaw-security/security_pipeline.py --json

# Output:
# {
#   "overall_healthy": true,
#   "security_score": 95,
#   ...
# }
```

---

## 7. Logs

### Ubicación

**Archivo:** `/var/log/openclaw/security_audit.log`

### Ver Logs

```bash
# Ver logs en vivo
tail -f /var/log/openclaw/security_audit.log

# Ver últimas 50 líneas
tail -50 /var/log/openclaw/security_audit.log

# Buscar errores
grep -i error /var/log/openclaw/security_audit.log
```

### Rotación de Logs

**Archivo:** `/etc/logrotate.d/openclaw-security`

```
/var/log/openclaw/security_audit.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
}
```

---

## 8. Alertas

### Configurar Alertas por Telegram

```python
def send_telegram_alert(message: str):
    """Enviar alerta por Telegram"""
    bot_token = os.environ.get('OPENCLAW_TELEGRAM_BOT_TOKEN')
    chat_id = "795606301"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    requests.post(url, json=data, timeout=10)
```

### Cuándo Enviar Alertas

| Condición | Severidad | Enviar Alerta |
|-----------|-----------|---------------|
| Score < 50 | error | ✅ Sí |
| Service down | error | ✅ Sí |
| Gateway unhealthy | error | ✅ Sí |
| Score 50-70 | warn | ⚠️ Opcional |
| Anomalías > 3 | warn | ⚠️ Opcional |

---

## 9. Troubleshooting

### Security Pipeline no se ejecuta

```bash
# Verificar cron job
crontab -l | grep security

# Verificar permisos del script
ls -la /opt/openclaw-security/security_pipeline.py

# Ejecutar manualmente
/opt/openclaw-security/security_pipeline.py
```

### Falso positivo en auditoría

```bash
# Ejecutar auditoría manual para verificar
openclaw security audit

# Si el issue persiste, revisar configuración
cat /home/openclaw/.openclaw/openclaw.json
```

### Score bajo inexplicablemente

```bash
# Ver logs de seguridad
openclaw-dashboard <<< "security 100"

# Ver anomalías detectadas
/opt/openclaw-security/security_pipeline.py --json | jq '.anomalies'
```

---

**Fin del documento del Security Pipeline**
