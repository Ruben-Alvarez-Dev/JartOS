# 🏗️ Infraestructura

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Especificaciones del VPS](#1-especificaciones-del-vps)
2. [Configuración de Tailscale](#2-configuración-de-tailscale)
3. [Reglas del Firewall UFW](#3-reglas-del-firewall-ufw)
4. [Servicios Systemd](#4-servicios-systemd)
5. [Estructura de Directorios](#5-estructura-de-directorios)

---

## 1. Especificaciones del VPS

### Hardware

| Componente | Especificación |
|------------|----------------|
| **Proveedor** | Hetzner Cloud |
| **CPU** | 4 vCPU (AMD/Intel) |
| **RAM** | 16 GB DDR4 |
| **Storage** | 160 GB NVMe SSD |
| **Network** | 1 Gbps (IPv4 + IPv6) |
| **Ubicación** | Núremberg, Alemania (nbg1) |

### Sistema Operativo

| Componente | Versión |
|------------|---------|
| **OS** | Ubuntu 22.04 LTS |
| **Kernel** | 5.15.0-generic |
| **Arquitectura** | x86_64 |
| **Init System** | systemd 249 |

### Usuarios del Sistema

| Usuario | UID | Propósito | Shell |
|---------|-----|-----------|-------|
| `root` | 0 | Administración | `/bin/bash` |
| `openclaw` | 1001 | Ejecución de OpenClaw | `/bin/bash` |
| `ubuntu` | 1000 | Usuario inicial (deshabilitado) | `/bin/bash` |

### Permisos de Directorios Clave

```bash
# Directorio de configuración de OpenClaw
/home/openclaw/.openclaw/          # 700 (drwx------)
/home/openclaw/.openclaw/.env      # 600 (-rw-------)
/home/openclaw/.openclaw/openclaw.json  # 600 (-rw-------)
/home/openclaw/.openclaw/agents/   # 700 (drwx------)

# Directorio de datos
/var/lib/openclaw/                 # 700 (drwx------)
/var/lib/openclaw/memory.db        # 644 (-rw-r--r--)

# Directorio de logs
/var/log/openclaw/                 # 755 (drwxr-xr-x)
/var/log/openclaw/*.log            # 644 (-rw-r--r--)

# Scripts y módulos
/opt/openclaw-*/                   # 755 (drwxr-xr-x)
/usr/local/bin/openclaw-*          # 755 (-rwxr-xr-x)

# Backups
/root/backups/openclaw/            # 700 (drwx------)
/root/backups/openclaw/*.tar.gz    # 600 (-rw-------)
```

---

## 2. Configuración de Tailscale

### Instalación

```bash
# Añadir repositorio de Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Iniciar Tailscale
sudo tailscale up --authkey <auth-key>

# Verificar estado
tailscale status
```

### Configuración del VPS

**Hostname:** `vpn-ruben-vps-openclaw`  
**IP Tailscale:** `100.77.1.100`  
**Tags:** `tag:server`

```bash
# Ver configuración actual
tailscale status --json

# Output relevante:
{
  "BackendState": "Running",
  "Self": {
    "HostName": "ubuntu-16gb-nbg1-1",
    "DNSName": "vpn-ruben-vps-openclaw.tail6c9810.ts.net.",
    "TailscaleIPs": ["100.77.1.100"],
    "Tags": ["tag:server"]
  }
}
```

### Tailscale Serve (Proxy HTTPS)

```bash
# Configurar serve para proxy HTTPS → localhost:18789
tailscale serve https / http://localhost:18789

# Ver configuración
tailscale serve status

# Output:
# vpn-ruben-vps-openclaw.tail6c9810.ts.net routes:
#   / proxies to http://localhost:18789
```

**URLs de acceso:**
- HTTPS: `https://vpn-ruben-vps-openclaw.tail6c9810.ts.net`
- IP directa: `https://100.77.1.100:443`

### ACLs (Access Control Lists)

**Archivo:** `tailscale.com/acls` (consola web de Tailscale)

```json
{
  "acls": [
    {
      "action": "accept",
      "src": ["*"],
      "dst": ["tag:server:*"]
    }
  ],
  "tagOwners": {
    "tag:server": ["admin@example.com"]
  }
}
```

**Flujo permitido:**
```
✅ PERMITIDO:
   Dispositivos → VPS (tag:server)
   • MacBook Pro → VPS ✅
   • Mac Mini → VPS ✅
   • Pixel → VPS ✅

❌ BLOQUEADO:
   VPS → Dispositivos locales
   • VPS → MacBook Pro ❌
   • VPS → Mac Mini ❌
   • VPS → Pixel ❌
```

### Comandos Útiles

```bash
# Ver estado
tailscale status

# Ver estado detallado (JSON)
tailscale status --json

# Ver red
tailscale netcheck

# Ver rutas
tailscale route

# Reiniciar conexión
sudo systemctl restart tailscaled
```

---

## 3. Reglas del Firewall UFW

### Estado Actual

```bash
$ sudo ufw status verbose

Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), deny (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
80/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere
22/tcp                     ALLOW IN    100.0.0.0/8
18789 on tailscale0        ALLOW IN    Anywhere
Anywhere on tailscale0     ALLOW IN    Anywhere
18795/tcp                  ALLOW IN    Anywhere
80/tcp (v6)                ALLOW IN    Anywhere (v6)
443/tcp (v6)               ALLOW IN    Anywhere (v6)
18789 (v6) on tailscale0   ALLOW IN    Anywhere (v6)
Anywhere (v6) on tailscale0 ALLOW IN    Anywhere (v6)
18795/tcp (v6)             ALLOW IN    Anywhere (v6)

Anywhere                   ALLOW OUT   Anywhere on tailscale0
Anywhere (v6)              ALLOW OUT   Anywhere (v6) on tailscale0
```

### Explicación de Reglas

| Regla | Puerto | Propósito | Justificación |
|-------|--------|-----------|---------------|
| SSH | 22/tcp | Administración remota | Solo desde Tailscale (100.0.0.0/8) |
| HTTP | 80/tcp | Redirección HTTPS | Tailscale Serve |
| HTTPS | 443/tcp | Acceso HTTPS | Tailscale Serve → OpenClaw |
| Gateway | 18789 | OpenClaw Gateway | Solo en interfaz tailscale0 |
| Tailscale | 18795/tcp | Tailscale SOCKS5 | Proxy interno de Tailscale |
| tailscale0 | all | Tráfico VPN | Permitir tráfico encriptado |

### Configuración de UFW

**Archivo:** `/etc/default/ufw`

```bash
# Configuración por defecto
IPT_SYSCTL="/etc/ufw/sysctl.conf"
DEFAULT_INPUT_POLICY="DROP"
DEFAULT_OUTPUT_POLICY="ACCEPT"
DEFAULT_FORWARD_POLICY="DROP"
```

**Archivo:** `/etc/ufw/user.rules`

```bash
*filter
:ufw-user-input - [0:0]
:ufw-user-output - [0:0]
:ufw-user-forward - [0:0]

# Reglas de entrada
-A ufw-user-input -p tcp --dport 22 -s 100.0.0.0/8 -j ACCEPT
-A ufw-user-input -p tcp --dport 80 -j ACCEPT
-A ufw-user-input -p tcp --dport 443 -j ACCEPT
-A ufw-user-input -i tailscale0 --dport 18789 -j ACCEPT
-A ufw-user-input -i tailscale0 -j ACCEPT
-A ufw-user-input -p tcp --dport 18795 -j ACCEPT

COMMIT
```

### Comandos Útiles

```bash
# Ver estado
sudo ufw status

# Ver estado detallado
sudo ufw status verbose

# Ver reglas numeradas
sudo ufw status numbered

# Habilitar UFW
sudo ufw enable

# Deshabilitar UFW
sudo ufw disable

# Resetear UFW
sudo ufw reset

# Log
sudo ufw logging on
```

---

## 4. Servicios Systemd

### openclaw.service (Gateway)

**Archivo:** `/etc/systemd/system/openclaw.service`

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

**Características:**
- Se ejecuta como usuario `openclaw` (no root)
- Carga variables de entorno desde `.env`
- Reinicio automático si falla
- `NoNewPrivileges=true` (seguridad)

---

### openclaw-email.service (Email Bridge)

**Archivo:** `/etc/systemd/system/openclaw-email.service`

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

**Características:**
- Se ejecuta como root (necesario para acceso a credenciales)
- Usa virtualenv Python
- Logs a journalctl

---

### openclaw-orchestrator.service (Telegram Bot)

**Archivo:** `/etc/systemd/system/openclaw-orchestrator.service`

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

**Características:**
- Se ejecuta como root
- Usa virtualenv Python
- Logs a journalctl

---

### tailscaled.service (Tailscale)

**Archivo:** `/lib/systemd/system/tailscaled.service` (proveído por paquete)

```ini
[Unit]
Description=Tailscale
After=network.target

[Service]
Type=notify
ExecStart=/usr/sbin/tailscaled --port=41641
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

### Comandos de Gestión

```bash
# Ver estado de todos los servicios openclaw
systemctl status openclaw openclaw-email openclaw-orchestrator

# Ver logs de un servicio
journalctl -u openclaw -f

# Reiniciar servicio
sudo systemctl restart openclaw

# Habilitar al inicio
sudo systemctl enable openclaw openclaw-email openclaw-orchestrator

# Ver dependencias
systemctl list-dependencies openclaw
```

---

## 5. Estructura de Directorios

### Árbol Completo

```
/
├── home/
│   └── openclaw/
│       └── .openclaw/                    # Configuración de OpenClaw
│           ├── openclaw.json             # Configuración principal (600)
│           ├── .env                      # Variables de entorno (600)
│           ├── agents/                   # Agentes y sesiones
│           │   └── telegram/
│           │       └── sessions/
│           ├── canvas/                   # Canvas (archivos temporales)
│           ├── credentials/              # Credenciales
│           │   └── email/
│           │       └── gmail.json
│           ├── logs/                     # Logs internos
│           └── tmp/                      # Temporal
│
├── opt/
│   ├── openclaw-email-bridge/            # Email Bridge
│   │   ├── email_bridge.py               # Script principal
│   │   ├── state.json                    # Estado (emails leídos)
│   │   └── venv/                         # Virtualenv Python
│   │
│   ├── openclaw-memory/                  # Memory & RAG Store
│   │   ├── memory_store.py               # Módulo de memoria
│   │   ├── rag_store.py                  # Módulo RAG
│   │   └── venv/                         # Virtualenv Python
│   │
│   └── openclaw-security/                # Security Pipeline
│       ├── security_pipeline.py          # Pipeline de seguridad
│       └── venv/                         # Virtualenv Python
│
├── var/
│   ├── lib/
│   │   └── openclaw/
│   │       └── memory.db                 # Base de datos SQLite
│   │
│   └── log/
│       ├── openclaw/                     # Logs de aplicaciones
│       │   ├── email_bridge.log
│       │   ├── orchestrator_bot.log
│       │   └── security_audit.log
│       │
│       └── openclaw-watchdog/            # Logs del watchdog
│           ├── alerts.log
│           ├── config.hash
│           └── watchdog.log
│
├── root/
│   └── backups/
│       └── openclaw/                     # Backups automáticos
│           ├── openclaw-backup-YYYYMMDD-HHMMSS.tar.gz
│           └── ...
│
├── usr/
│   └── local/
│       └── bin/
│           ├── openclaw-token            # Gestión de tokens
│           ├── openclaw-backup           # Backup manual
│           ├── openclaw-watchdog         # Watchdog CLI
│           ├── openclaw-alerts           # Ver alertas
│           ├── openclaw-dashboard        # Dashboard interactivo
│           └── openclaw-tailscale-serve  # Configurar Tailscale Serve
│
└── etc/
    ├── systemd/
    │   └── system/
    │       ├── openclaw.service
    │       ├── openclaw-email.service
    │       └── openclaw-orchestrator.service
    │
    └── ufw/
        ├── user.rules                    # Reglas de usuario
        └── user6.rules                   # Reglas IPv6
```

### Permisos Críticos

```bash
# Configuración sensible
chmod 600 /home/openclaw/.openclaw/.env
chmod 600 /home/openclaw/.openclaw/openclaw.json
chmod 700 /home/openclaw/.openclaw/agents/

# Base de datos
chmod 644 /var/lib/openclaw/memory.db

# Scripts
chmod 755 /usr/local/bin/openclaw-*
chmod 755 /opt/openclaw-*/**/*.py

# Backups
chmod 700 /root/backups/openclaw/
chmod 600 /root/backups/openclaw/*.tar.gz
```

---

## 6. Jobs de Cron

### Crontab de Root

**Archivo:** `/etc/crontab` o `crontab -e`

```cron
# Backup automático (diario a las 3 AM)
0 3 * * * /usr/local/bin/openclaw-backup >> /var/log/openclaw-backup.log 2>&1

# Watchdog (cada minuto)
* * * * * /usr/local/bin/openclaw-watchdog >> /var/log/openclaw-watchdog/cron.log 2>&1

# Security Pipeline (cada hora)
0 * * * * /opt/openclaw-security/security_pipeline.py >> /var/log/openclaw/security_audit.log 2>&1
```

### Explicación

| Job | Frecuencia | Propósito |
|-----|------------|-----------|
| `openclaw-backup` | Diario 3:00 AM | Backup de configuración y datos |
| `openclaw-watchdog` | Cada minuto | Monitoreo de configuración y health |
| `security_pipeline` | Cada hora | Auditoría de seguridad y scoring |

---

## 7. Comandos de Verificación

### Health Check Completo

```bash
#!/bin/bash
echo "=== OPENCLAW INFRASTRUCTURE CHECK ==="
echo ""

# Servicios
echo "📊 SERVICIOS:"
for service in openclaw openclaw-email openclaw-orchestrator tailscaled; do
    status=$(systemctl is-active $service 2>/dev/null)
    icon="❌"
    [ "$status" = "active" ] && icon="✅"
    echo "   $icon $service: $status"
done

# Tailscale
echo ""
echo "🌐 TAILSCALE:"
ts_status=$(tailscale status --json 2>/dev/null | jq -r '.BackendState')
icon="❌"
[ "$ts_status" = "Running" ] && icon="✅"
echo "   $icon Estado: $ts_status"

# UFW
echo ""
echo "🔥 UFW FIREWALL:"
ufw_status=$(sudo ufw status 2>/dev/null | head -1 | cut -d: -f2 | xargs)
icon="❌"
[ "$ufw_status" = "active" ] && icon="✅"
echo "   $icon Estado: $ufw_status"

# Gateway
echo ""
echo "🦞 GATEWAY:"
health=$(curl -s http://127.0.0.1:18789/health 2>/dev/null)
if echo "$health" | grep -q '"ok":true'; then
    echo "   ✅ Health: OK"
else
    echo "   ❌ Health: FAIL"
fi

# Backups
echo ""
echo "💾 BACKUPS:"
backup_count=$(ls /root/backups/openclaw/*.tar.gz 2>/dev/null | wc -l)
last_backup=$(ls -t /root/backups/openclaw/*.tar.gz 2>/dev/null | head -1)
echo "   • Count: $backup_count"
if [ -n "$last_backup" ]; then
    echo "   • Último: $(basename $last_backup)"
fi

echo ""
echo "=== CHECK COMPLETO ==="
```

---

**Fin del documento de Infraestructura**
