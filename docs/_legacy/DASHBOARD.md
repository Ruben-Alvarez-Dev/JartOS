# 📊 Dashboard CLI

**Interfaz de Línea de Comandos para Observabilidad**

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Descripción General](#1-descripción-general)
2. [Comandos Disponibles](#2-comandos-disponibles)
3. [Visualización de Métricas](#3-visualización-de-métricas)
4. [Ejemplos de Uso](#4-ejemplos-de-uso)
5. [Troubleshooting](#5-troubleshooting)

---

## 1. Descripción General

El **Dashboard CLI** es una interfaz interactiva de línea de comandos para monitorear todo el sistema OpenClaw.

**Características:**
- ✅ Estado general (health check)
- ✅ Métricas detalladas
- ✅ Logs de seguridad
- ✅ Estadísticas de conversaciones
- ✅ Memorias y RAG
- ✅ Limpieza de datos antiguos

**Ubicación:** `/usr/local/bin/openclaw-dashboard`  
**Ejecución:** Interactivo o comando único

---

## 2. Comandos Disponibles

### Iniciar Dashboard Interactivo

```bash
openclaw-dashboard
```

### Comandos del Dashboard

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `status` | Estado general del sistema | `dashboard> status` |
| `metrics [hours]` | Métricas de las últimas N horas | `dashboard> metrics 24` |
| `security [limit]` | Logs de seguridad recientes | `dashboard> security 20` |
| `conversations` | Estadísticas de conversaciones | `dashboard> conversations` |
| `memories [user_id]` | Memorias guardadas | `dashboard> memories` |
| `cleanup` | Limpiar datos antiguos (>30 días) | `dashboard> cleanup` |
| `help` | Mostrar ayuda | `dashboard> help` |
| `exit` | Salir del dashboard | `dashboard> exit` |

---

## 3. Visualización de Métricas

### Comando: status

```
dashboard> status

============================================================
🦞 OPENCLAW SECURITY & HEALTH REPORT
============================================================

✅ ESTADO GENERAL: HEALTHY
🔒 SECURITY SCORE: 100/100

📊 SERVICIOS:
   ✅ openclaw: active
   ✅ openclaw-email: active
   ✅ openclaw-orchestrator: active

🌐 TAILSCALE:
   ✅ Estado: Activo
   📡 Peers: 5

🔥 UFW FIREWALL:
   ✅ Estado: active

🛡️  SECURITY AUDIT:
   🔴 Critical: 0
   🟠 Warn: 2
   🔵 Info: 1

⚠️  ANOMALÍAS DETECTADAS: 0

📈 MÉTRICAS (24h):
   • api: 50 eventos, avg: 145.30
   • bot: 120 eventos, avg: 1.00
   • security: 5 eventos, avg: 95.00

============================================================
Report generado: 2026-03-10T15:30:00
============================================================
```

---

### Comando: metrics [hours]

```
dashboard> metrics 24

📈 MÉTRICAS (últimas 24h)
============================================================

API:
  • latency_ms:
      Count: 50
      Avg: 145.30
      Min: 89.50
      Max: 312.40
  • tokens:
      Count: 50
      Avg: 1250.00
      Min: 500
      Max: 2048

BOT:
  • message_received:
      Count: 60
      Avg: 1.00
      Min: 1.00
      Max: 1.00
  • message_sent:
      Count: 60
      Avg: 1.00
      Min: 1.00
      Max: 1.00
  • command_start:
      Count: 5
      Avg: 1.00
      Min: 1.00
      Max: 1.00

SECURITY:
  • score:
      Count: 24
      Avg: 95.00
      Min: 90.00
      Max: 100.00
```

---

### Comando: security [limit]

```
dashboard> security 20

🔒 LOGS DE SEGURIDAD (últimos 20)
============================================================
✅ 2026-03-10 15:30:00 ℹ️ SECURITY_CHECK
✅ 2026-03-10 14:30:00 ℹ️ SECURITY_CHECK
✅ 2026-03-10 13:30:00 ℹ️ SECURITY_CHECK
⏳ 2026-03-10 12:15:00 ⚠️ UNAUTHORIZED_ACCESS
✅ 2026-03-10 11:30:00 ℹ️ SECURITY_CHECK
...
```

**Leyenda:**
- `✅` = Resuelto
- `⏳` = Pendiente
- `ℹ️` = Info
- `⚠️` = Warning
- `❌` = Error

---

### Comando: conversations

```
dashboard> conversations

💬 CONVERSACIONES
============================================================
  • Usuarios únicos: 1
  • Mensajes totales: 1250
  • Perfiles guardados: 1

  Últimos mensajes:
    👤 795606301: Hola, ¿me ayudas con código?... (2026-03-10 15:28)
    🤖 assistant: ¡Claro! ¿Qué necesitas?... (2026-03-10 15:28)
    👤 795606301: ¿Cómo leo un archivo JSON?... (2026-03-10 15:27)
    🤖 assistant: Usa json.load()... (2026-03-10 15:27)
    👤 795606301: Gracias, funcionó... (2026-03-10 15:26)
```

---

### Comando: memories [user_id]

```
dashboard> memories

🧠 MEMORIAS
============================================================
Memorias totales: 50

Por categoría:
  • personal: 10
  • code: 25
  • facts: 15

Últimas memorias:
  • telegram:795606301 - personal: Se llama Rubén
  • telegram:795606301 - code: def connect_db()...
  • telegram:795606301 - facts: Usa VPS con Tailscale
```

---

### Comando: cleanup

```
dashboard> cleanup

🧹 LIMPIEZA DE DATOS
============================================================
Eliminando datos antiguos (>30 días)...

  • Conversaciones eliminadas: 500
  • Métricas eliminadas: 1000
  • Security logs resueltos eliminados: 50

Espacio liberado: 2.5 MB
```

---

## 4. Ejemplos de Uso

### Ejecutar Comando Único (No Interactivo)

```bash
# Estado rápido
openclaw-dashboard <<< "status"

# Métricas de 7 días
openclaw-dashboard <<< "metrics 168"

# Últimos 50 logs de seguridad
openclaw-dashboard <<< "security 50"
```

### Script de Monitoreo

```bash
#!/bin/bash
# monitoring.sh

echo "=== OPENCLAW STATUS ==="
openclaw-dashboard <<< "status" | grep -E "(ESTADO GENERAL|SECURITY SCORE)"

echo ""
echo "=== ÚLTIMAS ALERTAS ==="
openclaw-dashboard <<< "security 10" | grep "⚠️\|❌" || echo "No hay alertas"
```

### Reporte Diario

```bash
#!/bin/bash
# daily-report.sh

TIMESTAMP=$(date +%Y%m%d)
REPORT_FILE="/var/log/openclaw/daily-report-$TIMESTAMP.txt"

{
    echo "=== OPENCLAW DAILY REPORT ==="
    echo "Date: $(date)"
    echo ""
    
    echo "=== STATUS ==="
    openclaw-dashboard <<< "status"
    
    echo ""
    echo "=== METRICS (24h) ==="
    openclaw-dashboard <<< "metrics 24"
    
    echo ""
    echo "=== SECURITY (24h) ==="
    openclaw-dashboard <<< "security 100"
} > "$REPORT_FILE"

echo "Reporte guardado: $REPORT_FILE"
```

---

## 5. Troubleshooting

### Dashboard no inicia

```bash
# Verificar permisos
ls -la /usr/local/bin/openclaw-dashboard

# Verificar dependencias Python
python3 -c "import sys; sys.path.insert(0, '/opt/openclaw-memory'); from memory_store import get_memory_store"

# Ejecutar con debug
python3 /usr/local/bin/openclaw-dashboard
```

### Error de conexión a database

```bash
# Verificar database existe
ls -la /var/lib/openclaw/memory.db

# Verificar permisos
sqlite3 /var/lib/openclaw/memory.db "SELECT 1;"

# Verificar integridad
sqlite3 /var/lib/openclaw/memory.db "PRAGMA integrity_check;"
```

### Métricas no se muestran

```bash
# Verificar si hay métricas en DB
sqlite3 /var/lib/openclaw/memory.db "SELECT COUNT(*) FROM metrics;"

# Si está vacía, esperar a que se generen (ocurren con el uso)
```

---

**Fin del documento del Dashboard**
