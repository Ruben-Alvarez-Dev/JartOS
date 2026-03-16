#!/bin/bash
# OpenClaw-city Installation Script
# Instalación automática del sistema OpenClaw-city
#
# Uso: sudo ./install.sh

set -e

echo "🦞 OPENCLAW-CITY INSTALLATION SCRIPT"
echo "======================================"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funciones de log
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar root
if [ "$EUID" -ne 0 ]; then
    log_error "Este script debe ejecutarse como root"
    exit 1
fi

# Verificar sistema operativo
if [ ! -f /etc/os-release ]; then
    log_error "No se pudo detectar el sistema operativo"
    exit 1
fi

source /etc/os-release
if [[ "$ID" != "ubuntu" && "$ID" != "debian" ]]; then
    log_error "Este script solo soporta Ubuntu/Debian"
    exit 1
fi

log_info "Sistema detectado: $NAME $VERSION"

# Paso 1: Actualizar sistema
log_info "Paso 1/10: Actualizando sistema..."
apt update && apt upgrade -y

# Paso 2: Instalar dependencias
log_info "Paso 2/10: Instalando dependencias..."
apt install -y \
    curl \
    git \
    sqlite3 \
    ufw \
    fail2ban \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    jq \
    uuid-runtime

# Paso 3: Instalar Tailscale
log_info "Paso 3/10: Instalando Tailscale..."
if ! command -v tailscale &> /dev/null; then
    curl -fsSL https://tailscale.com/install.sh | sh
    log_info "Tailscale instalado"
else
    log_info "Tailscale ya está instalado"
fi

# Paso 4: Configurar usuario openclaw
log_info "Paso 4/10: Configurando usuario openclaw..."
if ! id -u openclaw &> /dev/null; then
    useradd -m -s /bin/bash openclaw
    log_info "Usuario openclaw creado"
else
    log_info "Usuario openclaw ya existe"
fi

# Crear directorios
mkdir -p /home/openclaw/.openclaw
mkdir -p /var/lib/openclaw
mkdir -p /var/log/openclaw
mkdir -p /opt/openclaw-memory
mkdir -p /opt/openclaw-security
mkdir -p /opt/openclaw-email-bridge
mkdir -p /opt/openclaw-orchestrator
mkdir -p /root/backups/openclaw

# Establecer permisos
chown -R openclaw:openclaw /home/openclaw/.openclaw
chown -R openclaw:openclaw /var/lib/openclaw
chown -R openclaw:openclaw /var/log/openclaw
chmod 700 /home/openclaw/.openclaw
chmod 700 /var/lib/openclaw
chmod 700 /root/backups/openclaw

# Paso 5: Instalar OpenClaw CLI
log_info "Paso 5/10: Instalando OpenClaw CLI..."
npm install -g @openclaw/cli
log_info "OpenClaw CLI instalado: $(openclaw --version)"

# Paso 6: Configurar archivos de ejemplo
log_info "Paso 6/10: Configurando archivos de configuración..."
if [ ! -f /home/openclaw/.openclaw/openclaw.json ]; then
    cp configs/openclaw.json.example /home/openclaw/.openclaw/openclaw.json
    chown openclaw:openclaw /home/openclaw/.openclaw/openclaw.json
    chmod 600 /home/openclaw/.openclaw/openclaw.json
    log_info "openclaw.json creado"
else
    log_info "openclaw.json ya existe"
fi

if [ ! -f /home/openclaw/.openclaw/.env ]; then
    cp configs/.env.example /home/openclaw/.openclaw/.env
    chown openclaw:openclaw /home/openclaw/.openclaw/.env
    chmod 600 /home/openclaw/.openclaw/.env
    log_info ".env creado"
    log_warn "IMPORTANTE: Editar /home/openclaw/.openclaw/.env con tus credenciales"
else
    log_info ".env ya existe"
fi

# Paso 7: Instalar módulos Python
log_info "Paso 7/10: Instalando módulos Python..."

# Memory Store
if [ ! -d /opt/openclaw-memory/venv ]; then
    cd /opt/openclaw-memory
    python3 -m venv venv
    ./venv/bin/pip install requests
    log_info "Memory Store instalado"
else
    log_info "Memory Store ya existe"
fi

# Security Pipeline
if [ ! -d /opt/openclaw-security/venv ]; then
    cd /opt/openclaw-security
    python3 -m venv venv
    ./venv/bin/pip install requests
    log_info "Security Pipeline instalado"
else
    log_info "Security Pipeline ya existe"
fi

# Email Bridge
if [ ! -d /opt/openclaw-email-bridge/venv ]; then
    cd /opt/openclaw-email-bridge
    python3 -m venv venv
    ./venv/bin/pip install imaplib2 python-telegram-bot
    log_info "Email Bridge instalado"
else
    log_info "Email Bridge ya existe"
fi

# Orchestrator Bot
if [ ! -d /opt/openclaw-orchestrator/venv ]; then
    cd /opt/openclaw-orchestrator
    python3 -m venv venv
    ./venv/bin/pip install python-telegram-bot requests
    log_info "Orchestrator Bot instalado"
else
    log_info "Orchestrator Bot ya existe"
fi

# Paso 8: Instalar scripts
log_info "Paso 8/10: Instalando scripts..."
for script in openclaw-token openclaw-backup openclaw-watchdog openclaw-alerts openclaw-dashboard; do
    if [ -f "scripts/$script" ]; then
        cp "scripts/$script" /usr/local/bin/
        chmod 755 /usr/local/bin/$script
        log_info "Script $script instalado"
    fi
done

# Paso 9: Configurar servicios systemd
log_info "Paso 9/10: Configurando servicios systemd..."
for service in openclaw openclaw-email openclaw-orchestrator; do
    if [ -f "configs/systemd/$service.service" ]; then
        cp "configs/systemd/$service.service" /etc/systemd/system/
        log_info "Servicio $service configurado"
    fi
done

systemctl daemon-reload

# Paso 10: Configurar firewall UFW
log_info "Paso 10/10: Configurando firewall UFW..."
if ! sudo ufw status | grep -q "active"; then
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow from 100.0.0.0/8 to any port 22 proto tcp
    ufw allow in on tailscale0 from any to any
    ufw allow out on tailscale0 from any to any
    ufw --force enable
    log_info "UFW configurado y activado"
else
    log_info "UFW ya está configurado"
fi

# Configuración final
log_info "Configuración final..."

# Crear archivo de resumen
cat > /root/openclaw-install-summary.txt <<EOF
=====================================
OPENCLAW-CITY INSTALLATION SUMMARY
=====================================
Date: $(date)
Version: 2026.3.10

NEXT STEPS:
1. Edit /home/openclaw/.openclaw/.env with your credentials
2. Edit /home/openclaw/.openclaw/openclaw.json with your Chat ID
3. Enable services:
   systemctl enable openclaw openclaw-email openclaw-orchestrator
4. Start services:
   systemctl start openclaw openclaw-email openclaw-orchestrator
5. Verify installation:
   openclaw-dashboard <<< "status"

DOCUMENTATION:
- docs/README.md
- docs/DEPLOYMENT.md
- docs/MAINTENANCE.md
=====================================
EOF

log_info "Instalación completada!"
log_info "Ver resumen: cat /root/openclaw-install-summary.txt"

echo ""
echo "======================================"
echo "🦞 OPENCLAW-CITY INSTALADO CORRECTAMENTE"
echo "======================================"
