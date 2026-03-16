# 🦞 OpenClaw Gateway

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Descripción General](#1-descripción-general)
2. [Configuración](#2-configuración)
3. [Security Hardening](#3-security-hardening)
4. [Tokens y Autenticación](#4-tokens-y-autenticación)
5. [Canales Configurados](#5-canales-configurados)
6. [Comandos Útiles](#6-comandos-útiles)

---

## 1. Descripción General

El **OpenClaw Gateway** es el componente central que ejecuta agentes de IA y gestiona herramientas. En nuestra implementación:

- **Binding:** Solo localhost (127.0.0.1:18789)
- **Autenticación:** Token requerido
- **Tools Profile:** messaging (mínimo privilegio)
- **Session Isolation:** per-channel-peer

---

## 2. Configuración

### Archivo Principal

**Ubicación:** `/home/openclaw/.openclaw/openclaw.json`

```json
{
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "port": 18789,
    "auth": {
      "mode": "token",
      "token": "${OPENCLAW_GATEWAY_TOKEN}"
    }
  },
  "session": {
    "dmScope": "per-channel-peer"
  },
  "tools": {
    "profile": "messaging",
    "deny": [
      "group:automation",
      "group:runtime",
      "group:fs",
      "sessions_spawn",
      "sessions_send"
    ],
    "fs": {
      "workspaceOnly": true
    },
    "exec": {
      "security": "deny",
      "ask": "always"
    },
    "elevated": {
      "enabled": false
    }
  },
  "browser": {
    "ssrfPolicy": {
      "dangerouslyAllowPrivateNetwork": false,
      "hostnameAllowlist": [
        "*.google.com",
        "*.googleapis.com",
        "*.mistral.ai"
      ]
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "${OPENCLAW_TELEGRAM_BOT_TOKEN}",
      "dmPolicy": "allowlist",
      "allowFrom": ["795606301"],
      "groupPolicy": "disabled"
    }
  },
  "models": {
    "providers": {
      "mistral": {
        "baseUrl": "${OPENCLAW_MISTRAL_BASE_URL}",
        "api": "openai-responses",
        "apiKey": "${OPENCLAW_MISTRAL_API_KEY}",
        "models": [
          {
            "id": "mistral-large-latest",
            "name": "Mistral Large",
            "reasoning": true,
            "input": ["text"],
            "contextWindow": 128000,
            "maxTokens": 4096
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": "mistral/mistral-large-latest",
      "sandbox": {
        "mode": "non-main",
        "workspaceAccess": "none"
      }
    }
  },
  "discovery": {
    "mdns": {
      "mode": "off"
    }
  }
}
```

### Variables de Entorno

**Archivo:** `/home/openclaw/.openclaw/.env`

```bash
# OpenClaw Credentials
# Permisos: 600 (solo owner puede leer)

OPENCLAW_GATEWAY_TOKEN=<uuid-v4>
OPENCLAW_TELEGRAM_BOT_TOKEN=<telegram-bot-token>
OPENCLAW_MISTRAL_API_KEY=<mistral-api-key>
OPENCLAW_MISTRAL_BASE_URL=https://api.mistral.ai/v1
```

---

## 3. Security Hardening

### 3.1 Gateway Binding

```json
{
  "gateway": {
    "mode": "local",
    "bind": "loopback"
  }
}
```

**Qué hace:**
- ✅ Gateway solo escucha en 127.0.0.1
- ✅ No accesible desde red externa
- ✅ Requiere Tailscale para acceso remoto

**Verificación:**
```bash
# Ver puerto escuchando
ss -tlnp | grep 18789
# Debe mostrar: 127.0.0.1:18789

# NO debe mostrar: 0.0.0.0:18789
```

---

### 3.2 Tools Restringidos

```json
{
  "tools": {
    "profile": "messaging",
    "deny": [
      "group:automation",
      "group:runtime",
      "group:fs",
      "sessions_spawn",
      "sessions_send"
    ],
    "exec": {
      "security": "deny",
      "ask": "always"
    },
    "elevated": {
      "enabled": false
    }
  }
}
```

**Herramientas denegadas:**

| Herramienta | Grupo | Razón |
|-------------|-------|-------|
| Automation | `group:automation` | Previene automatización no autorizada |
| Runtime | `group:runtime` | Previene ejecución de código arbitrario |
| Filesystem | `group:fs` | Previene acceso a archivos del sistema |
| sessions_spawn | Individual | Previene crear sesiones no autorizadas |
| sessions_send | Individual | Previene enviar mensajes a otras sesiones |
| exec | Individual | Requiere confirmación siempre |
| elevated | Individual | Sin privilegios elevados |

---

### 3.3 Browser SSRF Protection

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
- ✅ Previene SSRF a red local (10.x.x.x, 192.168.x.x)
- ✅ Previene acceso a servicios internos del VPS
- ✅ Solo permite dominios explícitos

**Dominios permitidos:**
- `*.google.com` - Búsquedas web
- `*.googleapis.com` - APIs de Google
- `*.mistral.ai` - LLM API

---

### 3.4 Session Isolation

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

---

### 3.5 Agent Sandboxing

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

### 3.6 Discovery Desactivado

```json
{
  "discovery": {
    "mdns": {
      "mode": "off"
    }
  }
}
```

**Qué hace:**
- ✅ Desactiva mDNS (multicast DNS)
- ✅ Previene descubrimiento en red local
- ✅ No necesario para deployment en VPS

---

## 4. Tokens y Autenticación

### 4.1 Gateway Token

**Generar nuevo token:**
```bash
# Generar UUID v4
uuidgen
# Output: a856ff89-bcc1-4e56-8b71-e81c38c726cc

# Actualizar token
sudo openclaw-token gateway token "nuevo-token-aqui"
```

**Usar token:**
```bash
# Health check con autenticación
curl -H "Authorization: Bearer <token>" http://127.0.0.1:18789/health
```

### 4.2 Telegram Bot Token

**Obtener token:**
1. Abrir Telegram
2. Buscar @BotFather
3. `/newbot` - Crear nuevo bot
4. Seguir instrucciones
5. Copiar token

**Actualizar token:**
```bash
sudo openclaw-token telegram bot_token "<nuevo-token>"
```

### 4.3 Mistral API Key

**Obtener API key:**
1. Ir a https://console.mistral.ai
2. API Keys → Create new key
3. Copiar key

**Actualizar API key:**
```bash
sudo openclaw-token mistral api_key "<nueva-api-key>"
```

---

## 5. Canales Configurados

### 5.1 Telegram

**Configuración:**
```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "${OPENCLAW_TELEGRAM_BOT_TOKEN}",
      "dmPolicy": "allowlist",
      "allowFrom": ["795606301"],
      "groupPolicy": "disabled"
    }
  }
}
```

**Explicación:**

| Parámetro | Valor | Significado |
|-----------|-------|-------------|
| `enabled` | `true` | Canal activado |
| `botToken` | `${...}` | Token del bot |
| `dmPolicy` | `allowlist` | Solo usuarios en lista |
| `allowFrom` | `["795606301"]` | User IDs permitidos |
| `groupPolicy` | `disabled` | Grupos deshabilitados |

**Obtener User ID:**
1. Enviar mensaje al bot
2. Ver logs: `journalctl -u openclaw-orchestrator -f`
3. Buscar `user_id` en logs

---

## 6. Comandos Útiles

### Gestión del Servicio

```bash
# Iniciar
sudo systemctl start openclaw

# Detener
sudo systemctl stop openclaw

# Reiniciar
sudo systemctl restart openclaw

# Ver estado
sudo systemctl status openclaw

# Ver logs
sudo journalctl -u openclaw -f

# Habilitar al inicio
sudo systemctl enable openclaw
```

### Health Check

```bash
# Health endpoint
curl http://127.0.0.1:18789/health

# Con autenticación
curl -H "Authorization: Bearer <token>" http://127.0.0.1:18789/health

# Ver respuesta completa
curl -s http://127.0.0.1:18789/health | jq
```

### Auditoría de Seguridad

```bash
# Auditoría básica
openclaw security audit

# Auditoría profunda
openclaw security audit --deep

# Auto-fix (cuando disponible)
openclaw security audit --fix
```

### Ver Configuración

```bash
# Ver configuración actual
cat /home/openclaw/.openclaw/openclaw.json

# Ver variables de entorno (cuidado - contiene secrets)
sudo cat /home/openclaw/.openclaw/.env

# Ver permisos
ls -la /home/openclaw/.openclaw/
```

### Verificar Binding

```bash
# Ver puerto escuchando
ss -tlnp | grep 18789

# Debe mostrar: 127.0.0.1:18789
# NO debe mostrar: 0.0.0.0:18789

# Ver conexiones activas
ss -tunap | grep openclaw
```

---

## 7. Troubleshooting

### Gateway no inicia

```bash
# Ver logs de error
sudo journalctl -u openclaw -n 50

# Verificar configuración
openclaw security audit

# Verificar puerto en uso
ss -tlnp | grep 18789
```

### Gateway expuesto públicamente

```bash
# Verificar binding
ss -tlnp | grep 18789

# Si muestra 0.0.0.0, corregir openclaw.json:
# "bind": "loopback"

# Reiniciar gateway
sudo systemctl restart openclaw
```

### Tools no funcionan

```bash
# Verificar configuración de tools
grep -A20 '"tools"' /home/openclaw/.openclaw/openclaw.json

# Verificar que profile es "messaging"
# Verificar que deny no bloquea herramientas necesarias
```

---

**Fin del documento del Gateway**
