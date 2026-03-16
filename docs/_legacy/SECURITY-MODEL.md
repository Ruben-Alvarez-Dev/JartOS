# 🔐 Security Model

**Modelo de Seguridad de 4 Capas**

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Visión General](#1-visión-general)
2. [Capa 1: Red](#2-capa-1-red)
3. [Capa 2: Autenticación](#3-capa-2-autenticación)
4. [Capa 3: Herramientas](#4-capa-3-herramientas)
5. [Capa 4: Aislamiento](#5-capa-4-aislamiento)
6. [Defensa en Profundidad](#6-defensa-en-profundidad)

---

## 1. Visión General

El modelo de seguridad de OpenClaw implementa **4 capas de defensa** para proteger el sistema contra accesos no autorizados y fugas de datos.

```
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 1: RED                                                    │
│  • Gateway loopback (127.0.0.1)                                 │
│  • Tailscale VPN (WireGuard)                                    │
│  • UFW Firewall                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 2: AUTENTICACIÓN                                          │
│  • Token de gateway                                             │
│  • Telegram dmPolicy: allowlist                                 │
│  • Chat ID autorizado                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 3: HERRAMIENTAS                                           │
│  • Tools profile: messaging                                     │
│  • Grupos denegados (automation, runtime, fs)                   │
│  • Exec security: deny                                          │
│  • Browser SSRF protection                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 4: AISLAMIENTO                                            │
│  • Session dmScope: per-channel-peer                            │
│  • Agent sandbox: non-main                                      │
│  • mDNS: off                                                    │
│  • Permisos de archivos (600/700)                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Capa 1: Red

### 2.1 Gateway Loopback

**Configuración:**
```json
{
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "port": 18789
  }
}
```

**Qué protege:**
- ✅ Gateway solo accesible desde localhost (127.0.0.1)
- ✅ No expuesto a internet público
- ✅ Requiere Tailscale para acceso remoto

**Verificación:**
```bash
# Ver puerto escuchando
ss -tlnp | grep 18789
# Debe mostrar: 127.0.0.1:18789
# NO debe mostrar: 0.0.0.0:18789
```

---

### 2.2 Tailscale VPN

**Configuración:**
- **Hostname:** `vpn-ruben-vps-openclaw`
- **IP Tailscale:** `100.77.1.100`
- **Tags:** `tag:server`
- **Serve:** HTTPS 443 → localhost:18789

**ACLs:**
```json
{
  "acls": [
    {
      "action": "accept",
      "src": ["*"],
      "dst": ["tag:server:*"]
    }
  ]
}
```

**Qué protege:**
- ✅ Encriptación WireGuard (estado del arte)
- ✅ Autenticación mutua
- ✅ Solo dispositivos autorizados pueden conectar
- ✅ VPS no puede iniciar conexiones a dispositivos locales

**Verificación:**
```bash
# Ver estado de Tailscale
tailscale status

# Ver ACLs
tailscale acl --json
```

---

### 2.3 UFW Firewall

**Configuración:**
```bash
# Políticas por defecto
ufw default deny incoming
ufw default allow outgoing

# Reglas específicas
ufw allow from 100.0.0.0/8 to any port 22 proto tcp  # SSH solo Tailscale
ufw allow in on tailscale0 from any to any           # Tráfico VPN
ufw allow out on tailscale0 from any to any          # Salida VPN
```

**Estado actual:**
```
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing)

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    100.0.0.0/8
18789 on tailscale0        ALLOW IN    Anywhere
Anywhere on tailscale0     ALLOW IN    Anywhere
```

**Qué protege:**
- ✅ SSH solo desde Tailscale
- ✅ Gateway solo en interfaz tailscale0
- ✅ Todo otro incoming bloqueado

**Verificación:**
```bash
# Ver estado
sudo ufw status verbose

# Probar firewall
nmap -p 22,18789 <IP-PUBLICA-VPS>
# Debería mostrar todos los puertos filtrados
```

---

## 3. Capa 2: Autenticación

### 3.1 Token de Gateway

**Configuración:**
```json
{
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "${OPENCLAW_GATEWAY_TOKEN}"
    }
  }
}
```

**Uso:**
```bash
# Health check con autenticación
curl -H "Authorization: Bearer <token>" http://127.0.0.1:18789/health
```

**Qué protege:**
- ✅ Requiere token para todas las operaciones
- ✅ Previene acceso no autorizado al gateway
- ✅ Token se rota periódicamente

**Mejores Prácticas:**
- Generar UUID v4 seguro
- Rotar token mensualmente
- Nunca commitear token a Git

---

### 3.2 Telegram dmPolicy: allowlist

**Configuración:**
```json
{
  "channels": {
    "telegram": {
      "dmPolicy": "allowlist",
      "allowFrom": ["795606301"]
    }
  }
}
```

**Qué protege:**
- ✅ Solo usuarios en allowlist pueden usar el bot
- ✅ Previene uso no autorizado del bot
- ✅ Bloquea mensajes de grupos (groupPolicy: disabled)

**Verificación:**
```bash
# Ver logs de intentos no autorizados
grep "UNAUTHORIZED" /var/log/openclaw/orchestrator_bot.log
```

---

### 3.3 Chat ID Autorizado

**Configuración:**
```python
# orchestrator_bot.py
CHAT_ID_AUTORIZADO = 795606301
```

**Qué protege:**
- ✅ Doble verificación de autorización
- ✅ A nivel de código + configuración

---

## 4. Capa 3: Herramientas

### 4.1 Tools Profile: messaging

**Configuración:**
```json
{
  "tools": {
    "profile": "messaging"
  }
}
```

**Permisos del profile messaging:**
| Herramienta | Permitida |
|-------------|-----------|
| Chat/LLM | ✅ Sí |
| Browser | ✅ Sí (con restricciones) |
| Filesystem | ❌ No |
| Runtime | ❌ No |
| Automation | ❌ No |
| Gateway control | ❌ No |

**Qué protege:**
- ✅ Mínimo privilegio necesario
- ✅ Previene acceso a filesystem
- ✅ Previene ejecución de código arbitrario

---

### 4.2 Grupos Denegados

**Configuración:**
```json
{
  "tools": {
    "deny": [
      "group:automation",
      "group:runtime",
      "group:fs",
      "sessions_spawn",
      "sessions_send"
    ]
  }
}
```

**Qué protege cada grupo:**

| Grupo | Herramientas | Riesgo si habilitado |
|-------|--------------|---------------------|
| `group:automation` | Cron, webhooks | Automatización no autorizada |
| `group:runtime` | Exec, eval | Ejecución de código arbitrario |
| `group:fs` | Filesystem | Acceso a archivos del sistema |
| `sessions_spawn` | Spawn sessions | Crear sesiones no autorizadas |
| `sessions_send` | Send messages | Enviar mensajes a otras sesiones |

---

### 4.3 Exec Security: deny

**Configuración:**
```json
{
  "tools": {
    "exec": {
      "security": "deny",
      "ask": "always"
    }
  }
}
```

**Qué protege:**
- ✅ Ejecución de comandos denegada por defecto
- ✅ Requiere confirmación explícita siempre
- ✅ Previene ejecución accidental o maliciosa

---

### 4.4 Browser SSRF Protection

**Configuración:**
```json
{
  "browser": {
    "ssrfPolicy": {
      "dangerouslyAllowPrivateNetwork": false,
      "hostnameAllowlist": [
        "*.google.com",
        "*.googleapis.com",
        "*.mistral.ai"
      ]
    }
  }
}
```

**Qué protege:**
- ✅ Previene SSRF (Server-Side Request Forgery)
- ✅ Bloquea acceso a red local (10.x.x.x, 192.168.x.x)
- ✅ Bloquea acceso a servicios internos del VPS
- ✅ Solo permite dominios explícitos en allowlist

**Riesgo SSRF:**
```
Sin protección:
  Agente → http://169.254.169.254/latest/meta-data/  # AWS metadata
  Agente → http://localhost:6379                      # Redis interno
  Agente → http://192.168.1.1                         # Router local

Con protección:
  ❌ Todos bloqueados
```

---

## 5. Capa 4: Aislamiento

### 5.1 Session dmScope: per-channel-peer

**Configuración:**
```json
{
  "session": {
    "dmScope": "per-channel-peer"
  }
}
```

**Qué hace:**
- ✅ Aísla sesiones por canal y peer
- ✅ Previene fuga de contexto entre usuarios
- ✅ Cada conversación es independiente

**Alternativas:**
| dmScope | Aislamiento | Uso recomendado |
|---------|-------------|-----------------|
| `global` | Ninguno | ❌ No usar |
| `per-channel` | Por canal | ⚠️ Parcial |
| `per-channel-peer` | Por canal + peer | ✅ Recomendado |

---

### 5.2 Agent Sandbox

**Configuración:**
```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "workspaceAccess": "none"
      }
    }
  }
}
```

**Qué hace:**
- ✅ Ejecuta agentes en sandbox no-privilegiado
- ✅ Sin acceso a filesystem (`workspaceAccess: "none"`)
- ✅ Aísla agentes del sistema principal

---

### 5.3 mDNS Desactivado

**Configuración:**
```json
{
  "discovery": {
    "mdns": {
      "mode": "off"
    }
  }
}
```

**Qué protege:**
- ✅ Previene descubrimiento en red local
- ✅ No necesario para deployment en VPS
- ✅ Reduce superficie de ataque

---

### 5.4 Permisos de Archivos

**Configuración:**
```bash
# Archivos sensibles
chmod 600 /home/openclaw/.openclaw/.env
chmod 600 /home/openclaw/.openclaw/openclaw.json
chmod 700 /home/openclaw/.openclaw/agents/

# Database
chmod 644 /var/lib/openclaw/memory.db

# Backups
chmod 600 /root/backups/openclaw/*.tar.gz
```

**Qué protege:**
- ✅ Solo owner puede leer archivos sensibles
- ✅ Previene lectura de tokens por otros usuarios
- ✅ Backups protegidos

---

## 6. Defensa en Profundidad

### Escenario: Atacante obtiene acceso al VPS

| Capa | Protección | Resultado |
|------|------------|-----------|
| 1. Red | Gateway en loopback | ❌ No puede acceder directamente al gateway |
| 2. Autenticación | Token requerido | ❌ Necesita token (no en plaintext) |
| 3. Herramientas | Tools restringidos | ❌ No puede ejecutar comandos |
| 4. Aislamiento | Sandbox + permisos | ❌ No puede leer archivos sensibles |

### Escenario: Agente comprometido intenta fuga de datos

| Capa | Protección | Resultado |
|------|------------|-----------|
| 1. Red | UFW outbound allow | ⚠️ Podría salir a internet |
| 2. Autenticación | N/A | N/A |
| 3. Herramientas | SSRF protection + hostname allowlist | ❌ Solo puede acceder a dominios permitidos |
| 4. Aislamiento | Sandbox | ❌ No puede leer archivos del sistema |

### Mejoras Adicionales (Opcionales)

| Mejora | Capa | Complejidad | Impacto |
|--------|------|-------------|---------|
| UFW outbound restrict | 1 | Media | 🔒 Bloquea salidas no autorizadas |
| Vault para secrets | 2 | Alta | 🔒 Gestiona secrets centralizadamente |
| SELinux/AppArmor | 4 | Alta | 🔒 Mandatory access control |
| Audit logging centralizado | 4 | Media | 🔍 Mejor visibilidad |

---

## 7. Verificación de Seguridad

### Script de Verificación

```bash
#!/bin/bash
# security-check.sh

echo "=== OPENCLAW SECURITY CHECK ==="
echo ""

# Capa 1: Red
echo "🔒 CAPA 1: RED"
if ss -tlnp | grep 18789 | grep -q 127.0.0.1; then
    echo "   ✅ Gateway en loopback"
else
    echo "   ❌ Gateway expuesto"
fi

if sudo ufw status | grep -q "active"; then
    echo "   ✅ UFW activo"
else
    echo "   ❌ UFW inactivo"
fi

if tailscale status | grep -q "Running"; then
    echo "   ✅ Tailscale activo"
else
    echo "   ❌ Tailscale inactivo"
fi

# Capa 2: Autenticación
echo ""
echo "🔑 CAPA 2: AUTENTICACIÓN"
if grep -q '"mode": "token"' /home/openclaw/.openclaw/openclaw.json; then
    echo "   ✅ Token auth activado"
else
    echo "   ❌ Token auth desactivado"
fi

if grep -q '"dmPolicy": "allowlist"' /home/openclaw/.openclaw/openclaw.json; then
    echo "   ✅ Telegram allowlist activado"
else
    echo "   ❌ Telegram allowlist desactivado"
fi

# Capa 3: Herramientas
echo ""
echo "🛠️  CAPA 3: HERRAMIENTAS"
if grep -q '"profile": "messaging"' /home/openclaw/.openclaw/openclaw.json; then
    echo "   ✅ Tools profile: messaging"
else
    echo "   ❌ Tools profile no restringido"
fi

if grep -q '"dangerouslyAllowPrivateNetwork": false' /home/openclaw/.openclaw/openclaw.json; then
    echo "   ✅ SSRF protection activado"
else
    echo "   ❌ SSRF protection desactivado"
fi

# Capa 4: Aislamiento
echo ""
echo "🔒 CAPA 4: AISLAMIENTO"
if grep -q '"dmScope": "per-channel-peer"' /home/openclaw/.openclaw/openclaw.json; then
    echo "   ✅ Session isolation activado"
else
    echo "   ❌ Session isolation desactivado"
fi

if stat -c "%a" /home/openclaw/.openclaw/.env | grep -q "600"; then
    echo "   ✅ Permisos .env correctos"
else
    echo "   ❌ Permisos .env incorrectos"
fi

echo ""
echo "=== CHECK COMPLETO ==="
```

---

**Fin del documento del Security Model**
