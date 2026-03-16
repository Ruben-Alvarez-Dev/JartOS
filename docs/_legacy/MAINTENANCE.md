# 🔧 Maintenance

**Mantenimiento y Troubleshooting del Sistema**

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Tareas Diarias](#1-tareas-diarias)
2. [Tareas Semanales](#2-tareas-semanales)
3. [Tareas Mensuales](#3-tareas-mensuales)
4. [Monitoreo](#4-monitoreo)
5. [Troubleshooting Guide](#5-troubleshooting-guide)
6. [Ubicación de Logs](#6-ubicación-de-logs)

---

## 1. Tareas Diarias

### Automáticas

Estas tareas se ejecutan automáticamente vía cron:

| Tarea | Hora | Script | Log |
|-------|------|--------|-----|
| **Watchdog** | Cada minuto | `openclaw-watchdog` | `/var/log/openclaw-watchdog/cron.log` |
| **Security Pipeline** | Cada hora | `security_pipeline.py` | `/var/log/openclaw/security_audit.log` |
| **Backup** | 3:00 AM | `openclaw-backup` | `/var/log/openclaw-backup.log` |

### Verificación Rápida (Recomendada)

```bash
# Ejecutar cada mañana
openclaw-dashboard <<< "status"

# Verificar:
# ✅ ESTADO GENERAL: HEALTHY
# 🔒 SECURITY SCORE: 90-100
# ✅ Todos los servicios: active
```

### Verificar Alertas

```bash
# Ver alertas del watchdog
openclaw-alerts

# Si hay alertas, investigar:
tail -50 /var/log/openclaw-watchdog/alerts.log
```

---

## 2. Tareas Semanales

### Auditoría de Seguridad

```bash
# Ejecutar auditoría completa
openclaw security audit --deep

# Ver reporte completo
openclaw-dashboard <<< "security 100"
```

### Revisar Métricas

```bash
# Métricas de los últimos 7 días
openclaw-dashboard <<< "metrics 168"

# Ver tendencias:
# • Latencia de API (¿aumentó?)
# • Errores de Mistral (¿hay picos?)
# • Security score (¿disminuyó?)
```

### Verificar Backups

```bash
# Listar backups disponibles
ls -lh /root/backups/openclaw/

# Verificar el más reciente
tar -tzf /root/backups/openclaw/openclaw-backup-*.tar.gz | head -10

# Verificar integridad
tar -tzf /root/backups/openclaw/openclaw-backup-$(date +%Y%m%d-030000).tar.gz > /dev/null && echo "✅ OK" || echo "❌ CORRUPTO"
```

### Limpiar Logs Antiguos

```bash
# Logs mayores a 30 días
sudo find /var/log/openclaw -name "*.log" -mtime +30 -delete

# Rotar logs manualmente (si es necesario)
sudo logrotate -f /etc/logrotate.d/openclaw
```

---

## 3. Tareas Mensuales

### Rotar Tokens (Opcional, Recomendado)

```bash
# Generar nuevo token de gateway
uuidgen
# Output: nuevo-uuid-aqui

# Actualizar token
sudo openclaw-token gateway token "nuevo-uuid"

# Verificar que funciona
curl -H "Authorization: Bearer nuevo-uuid" http://127.0.0.1:18789/health
```

### Backup de Memoria

```bash
# Backup manual de la database de memoria
cp /var/lib/openclaw/memory.db /root/backups/memory-$(date +%Y%m).db

# Verificar integridad
sqlite3 /root/backups/memory-$(date +%Y%m).db "PRAGMA integrity_check;"
```

### Revisar Permisos

```bash
# Verificar permisos de archivos sensibles
echo "=== PERMISOS DE ARCHIVOS SENSIBLES ==="
ls -la /home/openclaw/.openclaw/.env
ls -la /home/openclaw/.openclaw/openclaw.json
ls -la /home/openclaw/.openclaw/credentials/

# Deberían ser:
# .env: 600 (-rw-------)
# openclaw.json: 600 (-rw-------)
# credentials/: 700 (drwx------)
```

### Actualizar Sistema

```bash
# Actualizar paquetes del sistema
sudo apt update && sudo apt upgrade -y

# Actualizar Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Actualizar OpenClaw (si hay nueva versión)
sudo npm update -g @openclaw/cli

# Reiniciar servicios después de actualizaciones
sudo systemctl restart openclaw openclaw-email openclaw-orchestrator
```

---

## 4. Monitoreo

### Comandos de Monitoreo

```bash
# Estado en tiempo real (actualiza cada 2s)
watch -n 2 'systemctl is-active openclaw openclaw-email openclaw-orchestrator'

# Logs en vivo
tail -f /var/log/openclaw/orchestrator_bot.log

# Conexiones activas
watch -n 2 'ss -tunap | grep openclaw'

# Uso de recursos
htop

# Espacio en disco
df -h /var/lib/openclaw /home/openclaw
```

### Dashboard de Monitoreo

```bash
# Script de monitoreo continuo
while true; do
    clear
    echo "=== OPENCLAW MONITORING ==="
    echo "Time: $(date)"
    echo ""
    openclaw-dashboard <<< "status" | grep -E "(ESTADO GENERAL|SECURITY SCORE|SERVICIOS)"
    echo ""
    echo "Presiona Ctrl+C para salir"
    sleep 30
done
```

### Alertas Personalizadas

Crear script `/usr/local/bin/openclaw-monitor`:

```bash
#!/bin/bash
# openclaw-monitor - Verificación rápida

ALERT=0

# Verificar servicios
for service in openclaw openclaw-email openclaw-orchestrator; do
    if ! systemctl is-active --quiet $service; then
        echo "❌ $service no está activo"
        ALERT=1
    fi
done

# Verificar gateway
if ! curl -s http://127.0.0.1:18789/health | grep -q '"ok":true'; then
    echo "❌ Gateway no responde correctamente"
    ALERT=1
fi

# Verificar UFW
if ! sudo ufw status | grep -q "active"; then
    echo "❌ UFW no está activo"
    ALERT=1
fi

# Verificar Tailscale
if ! tailscale status | grep -q "Running"; then
    echo "❌ Tailscale no está activo"
    ALERT=1
fi

if [ $ALERT -eq 0 ]; then
    echo "✅ Todo OK"
else
    echo "⚠️ Hay problemas que requieren atención"
fi

exit $ALERT
```

---

## 5. Troubleshooting Guide

### Problema: Gateway no inicia

**Síntomas:**
```bash
systemctl status openclaw
# Output: Failed to start OpenClaw Gateway
```

**Diagnóstico:**
```bash
# Ver logs de error
sudo journalctl -u openclaw -n 50

# Verificar configuración
openclaw security audit

# Verificar puerto en uso
ss -tlnp | grep 18789
```

**Soluciones:**

1. **Puerto ya en uso:**
   ```bash
   # Matar proceso que usa el puerto
   sudo kill $(sudo lsof -t -i:18789)
   
   # Reiniciar servicio
   sudo systemctl restart openclaw
   ```

2. **Configuración inválida:**
   ```bash
   # Validar JSON
   cat /home/openclaw/.openclaw/openclaw.json | jq .
   
   # Corregir errores
   sudo nano /home/openclaw/.openclaw/openclaw.json
   ```

3. **Token inválido:**
   ```bash
   # Regenerar token
   uuidgen
   
   # Actualizar
   sudo openclaw-token gateway token "nuevo-token"
   ```

---

### Problema: Bot de Telegram no responde

**Síntomas:**
- Mensajes no reciben respuesta
- Comandos no funcionan

**Diagnóstico:**
```bash
# Verificar servicio
sudo systemctl status openclaw-orchestrator

# Ver logs
sudo journalctl -u openclaw-orchestrator -f

# Verificar token
grep OPENCLAW_TELEGRAM_BOT_TOKEN /home/openclaw/.openclaw/.env
```

**Soluciones:**

1. **Token expirado/inválido:**
   ```bash
   # Obtener nuevo token de @BotFather
   # Actualizar
   sudo openclaw-token telegram bot_token "nuevo-token"
   ```

2. **Chat ID no autorizado:**
   ```bash
   # Ver logs para ver tu chat ID
   sudo journalctl -u openclaw-orchestrator | grep "user_id"
   
   # Actualizar en orchestrator_bot.py
   sudo nano /opt/openclaw-orchestrator/orchestrator_bot.py
   # Cambiar CHAT_ID_AUTORIZADO
   ```

3. **Error de Mistral API:**
   ```bash
   # Verificar API key
   curl -H "Authorization: Bearer $OPENCLAW_MISTRAL_API_KEY" \
        https://api.mistral.ai/v1/models
   
   # Si falla, regenerar API key
   ```

---

### Problema: Email Bridge no funciona

**Síntomas:**
- Emails no se notifican
- Error de autenticación IMAP

**Diagnóstico:**
```bash
# Verificar servicio
sudo systemctl status openclaw-email

# Ver logs
sudo journalctl -u openclaw-email -f

# Verificar credenciales
cat /home/openclaw/.openclaw/credentials/email/gmail.json | jq
```

**Soluciones:**

1. **App Password expirado:**
   ```bash
   # Ir a https://myaccount.google.com/security
   # Generar nueva App Password
   # Actualizar gmail.json
   sudo nano /home/openclaw/.openclaw/credentials/email/gmail.json
   
   # Reiniciar servicio
   sudo systemctl restart openclaw-email
   ```

2. **IMAP no habilitado en Gmail:**
   ```bash
   # Ir a Gmail → Configuración → Reenvío y correo POP/IMAP
   # Habilitar IMAP
   ```

3. **State file corrupto:**
   ```bash
   # Detener servicio
   sudo systemctl stop openclaw-email
   
   # Backup y resetear estado
   cp /opt/openclaw-email-bridge/state.json /root/backups/
   echo '{"last_checked": null, "processed_emails": []}' > /opt/openclaw-email-bridge/state.json
   
   # Iniciar servicio
   sudo systemctl start openclaw-email
   ```

---

### Problema: Security Score bajo

**Síntomas:**
```bash
openclaw-dashboard <<< "status"
# 🔒 SECURITY SCORE: 65/100
```

**Diagnóstico:**
```bash
# Ver auditoría detallada
openclaw security audit --deep

# Ver anomalías
/opt/openclaw-security/security_pipeline.py --json | jq '.anomalies'

# Ver logs de seguridad
openclaw-dashboard <<< "security 100"
```

**Causas Comunes:**

| Causa | Score Impact | Solución |
|-------|--------------|----------|
| Critical issues | -50 | Resolver inmediatamente |
| Warnings | -10 c/u | Revisar y corregir |
| Anomalías | -5 c/u | Investigar causa |
| Servicios caídos | Variable | Reiniciar servicios |

---

### Problema: Database de Memoria corrupta

**Síntomas:**
```bash
sqlite3 /var/lib/openclaw/memory.db "SELECT 1;"
# Error: database disk image is malformed
```

**Diagnóstico:**
```bash
# Verificar integridad
sqlite3 /var/lib/openclaw/memory.db "PRAGMA integrity_check;"
```

**Soluciones:**

1. **Backup reciente disponible:**
   ```bash
   # Detener servicios
   sudo systemctl stop openclaw openclaw-email openclaw-orchestrator
   
   # Restaurar backup
   cp /root/backups/openclaw/memory-backup-YYYYMM.db /var/lib/openclaw/memory.db
   
   # Iniciar servicios
   sudo systemctl start openclaw openclaw-email openclaw-orchestrator
   ```

2. **Sin backup (reparar):**
   ```bash
   # Intentar reparar
   sqlite3 /var/lib/openclaw/memory.db "PRAGMA writable_schema = 1;"
   sqlite3 /var/lib/openclaw/memory.db "PRAGMA integrity_check;"
   sqlite3 /var/lib/openclaw/memory.db "PRAGMA writable_schema = 0;"
   ```

---

## 6. Ubicación de Logs

### Logs del Sistema

| Log | Ubicación | Propósito |
|-----|-----------|-----------|
| **Gateway** | `journalctl -u openclaw` | Logs del servicio gateway |
| **Email Bridge** | `/var/log/openclaw/email_bridge.log` | Logs del email bridge |
| **Orchestrator** | `/var/log/openclaw/orchestrator_bot.log` | Logs del bot de Telegram |
| **Security Audit** | `/var/log/openclaw/security_audit.log` | Auditorías de seguridad |
| **Watchdog** | `/var/log/openclaw-watchdog/` | Monitoreo de configuración |
| **Backup** | `/var/log/openclaw-backup.log` | Logs de backups |

### Comandos Útiles

```bash
# Ver logs de gateway en vivo
sudo journalctl -u openclaw -f

# Ver logs de email bridge
tail -f /var/log/openclaw/email_bridge.log

# Ver logs de orchestrator
tail -f /var/log/openclaw/orchestrator_bot.log

# Buscar errores
grep -i error /var/log/openclaw/*.log

# Ver logs de las últimas 24h
journalctl --since "24 hours ago" -u openclaw

# Exportar logs
journalctl -u openclaw --since "2026-03-01" > /root/openclaw-march.log
```

### Rotación de Logs

**Archivos:** `/etc/logrotate.d/openclaw*`

```
/var/log/openclaw/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 openclaw openclaw
}
```

---

**Fin del documento de Maintenance**
