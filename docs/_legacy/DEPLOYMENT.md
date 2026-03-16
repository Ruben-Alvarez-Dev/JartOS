# 🚀 Deployment

**Guía de Instalación y Configuración**

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Prerrequisitos](#1-prerrequisitos)
2. [Instalación Paso a Paso](#2-instalación-paso-a-paso)
3. [Archivos de Configuración](#3-archivos-de-configuración)
4. [Variables de Entorno](#4-variables-de-entorno)
5. [Servicios Systemd](#5-servicios-systemd)
6. [Procedimiento de Backup](#6-procedimiento-de-backup)

---

## 1. Prerrequisitos

### Hardware

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| **CPU** | 2 vCPU | 4 vCPU |
| **RAM** | 4 GB | 8-16 GB |
| **Storage** | 40 GB | 80+ GB |
| **Network** | 100 Mbps | 1 Gbps |

### Software

| Componente | Versión | Notas |
|------------|---------|-------|
| **OS** | Ubuntu 22.04 LTS | o Debian 11+ |
| **Node.js** | 18+ | Para OpenClaw |
| **Python** | 3.10+ | Para módulos adicionales |
| **SQLite** | 3.35+ | Incluido en Ubuntu |
| **Tailscale** | Latest | VPN requerida |

### Cuentas Externas

- ✅ **Tailscale** - https://tailscale.com
- ✅ **Mistral AI** - https://console.mistral.ai
- ✅ **Telegram** - Para crear bot (@BotFather)
- ✅ **Gmail** - Con IMAP habilitado (opcional)

---

## 2. Instalación Paso a Paso

### 2.1 Preparar el VPS

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias básicas
sudo apt install -y \
    curl \
    git \
    sqlite3 \
    ufw \
    fail2ban \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm
```

---

### 2.2 Instalar Tailscale

```bash
# Instalar Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Iniciar Tailscale
sudo tailscale up --authkey <ts-auth-key>

# Verificar estado
tailscale status

# Configurar hostname (opcional)
sudo tailscale set --hostname=vpn-ruben-vps-openclaw
```

---

### 2.3 Configurar Firewall UFW

```bash
# Resetear UFW (si es necesario)
sudo ufw reset

# Configurar políticas por defecto
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Permitir SSH solo desde Tailscale
sudo ufw allow from 100.0.0.0/8 to any port 22 proto tcp

# Permitir tráfico Tailscale
sudo ufw allow in on tailscale0 from any to any
sudo ufw allow out on tailscale0 from any to any

# Habilitar UFW
sudo ufw enable

# Verificar estado
sudo ufw status verbose
```

---

### 2.4 Crear Usuario openclaw

```bash
# Crear usuario
sudo useradd -m -s /bin/bash openclaw

# Crear directorios
sudo mkdir -p /home/openclaw/.openclaw
sudo mkdir -p /var/lib/openclaw
sudo mkdir -p /var/log/openclaw
sudo mkdir -p /opt/openclaw-memory
sudo mkdir -p /opt/openclaw-security
sudo mkdir -p /opt/openclaw-email-bridge
sudo mkdir -p /opt/openclaw-orchestrator
sudo mkdir -p /root/backups/openclaw

# Establecer permisos
sudo chown -R openclaw:openclaw /home/openclaw/.openclaw
sudo chown -R openclaw:openclaw /var/lib/openclaw
sudo chown -R openclaw:openclaw /var/log/openclaw
sudo chmod 700 /home/openclaw/.openclaw
sudo chmod 700 /var/lib/openclaw
sudo chmod 700 /root/backups/openclaw
```

---

### 2.5 Instalar OpenClaw

```bash
# Instalar OpenClaw CLI
npm install -g @openclaw/cli

# Verificar instalación
openclaw --version
```

---

### 2.6 Configurar OpenClaw

```bash
# Copiar configuración de ejemplo
sudo -u openclaw cp /path/to/configs/openclaw.json.example /home/openclaw/.openclaw/openclaw.json
sudo -u openclaw cp /path/to/configs/.env.example /home/openclaw/.openclaw/.env

# Editar configuración
sudo nano /home/openclaw/.openclaw/openclaw.json
sudo nano /home/openclaw/.openclaw/.env

# Establecer permisos
sudo chmod 600 /home/openclaw/.openclaw/.env
sudo chmod 600 /home/openclaw/.openclaw/openclaw.json
```

---

### 2.7 Instalar Módulos Python

```bash
# Memory Store
cd /opt/openclaw-memory
sudo python3 -m venv venv
sudo ./venv/bin/pip install requests

# Security Pipeline
cd /opt/openclaw-security
sudo python3 -m venv venv
sudo ./venv/bin/pip install requests

# Email Bridge
cd /opt/openclaw-email-bridge
sudo python3 -m venv venv
sudo ./venv/bin/pip install imaplib2 python-telegram-bot

# Orchestrator Bot
cd /opt/openclaw-orchestrator
sudo python3 -m venv venv
sudo ./venv/bin/pip install python-telegram-bot requests
```

---

### 2.8 Instalar Scripts

```bash
# Copiar scripts
sudo cp scripts/openclaw-token /usr/local/bin/
sudo cp scripts/openclaw-backup /usr/local/bin/
sudo cp scripts/openclaw-watchdog /usr/local/bin/
sudo cp scripts/openclaw-alerts /usr/local/bin/
sudo cp scripts/openclaw-dashboard /usr/local/bin/

# Establecer permisos
sudo chmod 755 /usr/local/bin/openclaw-*
```

---

### 2.9 Configurar Servicios Systemd

```bash
# Copiar servicios
sudo cp configs/systemd/openclaw.service /etc/systemd/system/
sudo cp configs/systemd/openclaw-email.service /etc/systemd/system/
sudo cp configs/systemd/openclaw-orchestrator.service /etc/systemd/system/

# Recargar systemd
sudo systemctl daemon-reload

# Habilitar servicios
sudo systemctl enable openclaw openclaw-email openclaw-orchestrator

# Iniciar servicios
sudo systemctl start openclaw openclaw-email openclaw-orchestrator

# Verificar estado
sudo systemctl status openclaw openclaw-email openclaw-orchestrator
```

---

### 2.10 Configurar Cron Jobs

```bash
# Editar crontab de root
sudo crontab -e

# Añadir jobs:
# Backup automático (diario a las 3 AM)
0 3 * * * /usr/local/bin/openclaw-backup >> /var/log/openclaw-backup.log 2>&1

# Watchdog (cada minuto)
* * * * * /usr/local/bin/openclaw-watchdog >> /var/log/openclaw-watchdog/cron.log 2>&1

# Security Pipeline (cada hora)
0 * * * * /opt/openclaw-security/security_pipeline.py >> /var/log/openclaw/security_audit.log 2>&1
```

---

### 2.11 Verificar Instalación

```bash
# Health check del gateway
curl http://127.0.0.1:18789/health

# Dashboard interactivo
openclaw-dashboard <<< "status"

# Auditoría de seguridad
openclaw security audit
```

---

## 3. Archivos de Configuración

### 3.1 openclaw.json

**Ubicación:** `/home/openclaw/.openclaw/openclaw.json`

Ver [configs/openclaw.json.example](configs/openclaw.json.example) para template completo.

---

### 3.2 .env

**Ubicación:** `/home/openclaw/.openclaw/.env`

```bash
# OpenClaw Credentials
# Permisos: 600 (solo owner puede leer)

OPENCLAW_GATEWAY_TOKEN=<uuid-v4>
OPENCLAW_TELEGRAM_BOT_TOKEN=<telegram-bot-token>
OPENCLAW_MISTRAL_API_KEY=<mistral-api-key>
OPENCLAW_MISTRAL_BASE_URL=https://api.mistral.ai/v1
```

---

### 3.3 gmail.json (opcional)

**Ubicación:** `/home/openclaw/.openclaw/credentials/email/gmail.json`

```json
{
  "email": "tu.email@gmail.com",
  "password": "app-password-16-chars",
  "imap_server": "imap.gmail.com",
  "imap_port": 993,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587
}
```

---

## 4. Variables de Entorno

### Requeridas

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `OPENCLAW_GATEWAY_TOKEN` | Token de autenticación del gateway | `a856ff89-bcc1-...` |
| `OPENCLAW_TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | `8425106517:AAG...` |
| `OPENCLAW_MISTRAL_API_KEY` | API key de Mistral | `zGehHJuRShmZ...` |
| `OPENCLAW_MISTRAL_BASE_URL` | URL base de Mistral API | `https://api.mistral.ai/v1` |

### Opcionales

| Variable | Descripción | Default |
|----------|-------------|---------|
| `OPENCLAW_LOG_LEVEL` | Nivel de logging | `info` |
| `OPENCLAW_DEBUG` | Modo debug | `false` |

---

## 5. Servicios Systemd

### openclaw.service

```ini
[Unit]
Description=OpenClaw Gateway
Documentation=https://docs.openclaw.ai
After=network-online.target tailscaled.service docker.service
Wants=network-online.target

[Service]
Type=simple
User=openclaw
Group=openclaw
WorkingDirectory=/home/openclaw
EnvironmentFile=-/home/openclaw/.openclaw/.env
ExecStart=/usr/bin/openclaw gateway run --bind loopback --port 18789
Restart=always
RestartSec=5
Environment=NODE_ENV=production
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
Environment=OPENCLAW_NO_RESPAWN=1
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

---

### openclaw-email.service

```ini
[Unit]
Description=OpenClaw Email Bridge (Gmail con Human-in-the-Loop)
Documentation=https://docs.openclaw.ai
After=network-online.target openclaw.service
Wants=network-online.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/opt/openclaw-email-bridge
ExecStart=/opt/openclaw-email-bridge/venv/bin/python3 /opt/openclaw-email-bridge/email_bridge.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=openclaw-email

[Install]
WantedBy=multi-user.target
```

---

### openclaw-orchestrator.service

```ini
[Unit]
Description=OpenClaw Orchestrator Bot (Telegram)
Documentation=https://docs.openclaw.ai
After=network-online.target openclaw.service
Wants=network-online.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/opt/openclaw-orchestrator
ExecStart=/opt/openclaw-orchestrator/venv/bin/python3 /opt/openclaw-orchestrator/orchestrator_bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=openclaw-orchestrator

[Install]
WantedBy=multi-user.target
```

---

## 6. Procedimiento de Backup

### Backup Manual

```bash
# Ejecutar backup
sudo openclaw-backup

# Output:
# ✅ Backup completed: /root/backups/openclaw/openclaw-backup-20260310-153000.tar.gz
#    Size: 1.2M
```

### Backup Automático

Configurado en cron (diario a las 3 AM):

```cron
0 3 * * * /usr/local/bin/openclaw-backup >> /var/log/openclaw-backup.log 2>&1
```

### Contenido del Backup

```bash
# Ver contenido
tar -tzf /root/backups/openclaw/openclaw-backup-YYYYMMDD-HHMMSS.tar.gz

# Incluye:
# /home/openclaw/.openclaw/openclaw.json
# /home/openclaw/.openclaw/.env
# /home/openclaw/.openclaw/agents/
# /home/openclaw/.openclaw/credentials/
# (excluye: *.log, tmp/*)
```

### Restaurar Backup

```bash
# 1. Detener servicios
sudo systemctl stop openclaw openclaw-email openclaw-orchestrator

# 2. Restaurar
sudo tar -xzf /root/backups/openclaw/openclaw-backup-YYYYMMDD-HHMMSS.tar.gz -C /

# 3. Iniciar servicios
sudo systemctl start openclaw openclaw-email openclaw-orchestrator

# 4. Verificar
sudo systemctl status openclaw
```

### Retención

- **Automática:** 7 días (el script elimina backups antiguos)
- **Recomendada:** 30 días (para recovery a largo plazo)

---

## 7. Verificación Post-Instalación

### Checklist

```bash
#!/bin/bash
echo "=== OPENCLAW INSTALLATION CHECK ==="
echo ""

# 1. Servicios
echo "📊 SERVICIOS:"
for service in openclaw openclaw-email openclaw-orchestrator; do
    status=$(systemctl is-active $service 2>/dev/null)
    icon="❌"
    [ "$status" = "active" ] && icon="✅"
    echo "   $icon $service: $status"
done

# 2. Gateway
echo ""
echo "🦞 GATEWAY:"
health=$(curl -s http://127.0.0.1:18789/health 2>/dev/null)
if echo "$health" | grep -q '"ok":true'; then
    echo "   ✅ Health: OK"
else
    echo "   ❌ Health: FAIL"
fi

# 3. Tailscale
echo ""
echo "🌐 TAILSCALE:"
ts_status=$(tailscale status --json 2>/dev/null | jq -r '.BackendState')
icon="❌"
[ "$ts_status" = "Running" ] && icon="✅"
echo "   $icon Estado: $ts_status"

# 4. UFW
echo ""
echo "🔥 UFW:"
ufw_status=$(sudo ufw status 2>/dev/null | head -1 | cut -d: -f2 | xargs)
icon="❌"
[ "$ufw_status" = "active" ] && icon="✅"
echo "   $icon Estado: $ufw_status"

# 5. Backups
echo ""
echo "💾 BACKUPS:"
backup_count=$(ls /root/backups/openclaw/*.tar.gz 2>/dev/null | wc -l)
echo "   • Count: $backup_count"

# 6. Permisos
echo ""
echo "🔒 PERMISOS:"
env_perms=$(stat -c "%a" /home/openclaw/.openclaw/.env 2>/dev/null)
icon="❌"
[ "$env_perms" = "600" ] && icon="✅"
echo "   $icon .env: $env_perms (debería ser 600)"

echo ""
echo "=== CHECK COMPLETO ==="
```

---

**Fin del documento de Deployment**
