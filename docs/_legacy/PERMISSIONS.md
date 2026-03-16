# 🔐 Permissions

**Sistema de Permisos y Control de Acceso**

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Visión General](#1-visión-general)
2. [Permisos de Archivos](#2-permisos-de-archivos)
3. [Permisos de Directorios](#3-permisos-de-directorios)
4. [Permisos de Usuario](#4-permisos-de-usuario)
5. [Permisos de Herramientas](#5-permisos-de-herramientas)
6. [Auditoría de Permisos](#6-auditoría-de-permisos)

---

## 1. Visión General

El sistema de permisos de OpenClaw sigue el principio de **mínimo privilegio**: cada componente tiene solo los permisos necesarios para funcionar.

### Niveles de Permisos

| Nivel | Descripción | Ejemplo |
|-------|-------------|---------|
| **Sistema** | Permisos de archivos/directorios | 600, 700 |
| **Usuario** | Permisos de usuario en sistema | openclaw, root |
| **Aplicación** | Permisos de herramientas | messaging profile |
| **Canal** | Permisos por canal de comunicación | Telegram allowlist |

---

## 2. Permisos de Archivos

### Archivos Sensibles

| Archivo | Permisos | Owner | Grupo | Razón |
|---------|----------|-------|-------|-------|
| `.env` | 600 | openclaw | openclaw | Contiene tokens y API keys |
| `openclaw.json` | 600 | openclaw | openclaw | Configuración con secrets |
| `gmail.json` | 600 | openclaw | openclaw | Credenciales de email |
| `state.json` | 600 | root | root | Estado del email bridge |
| `*.tar.gz` (backups) | 600 | root | root | Backups con configuración |

### Archivos de Configuración

| Archivo | Permisos | Owner | Grupo | Razón |
|---------|----------|-------|-------|-------|
| `systemd/*.service` | 644 | root | root | Servicios systemd |
| `ufw/*.rules` | 644 | root | root | Reglas de firewall |
| `crontab` | 600 | root | root | Jobs programados |

### Archivos de Logs

| Archivo | Permisos | Owner | Grupo | Razón |
|---------|----------|-------|-------|-------|
| `*.log` | 644 | openclaw/syslog | openclaw | Logs legibles |
| `memory.db` | 644 | root | root | Database SQLite |

### Verificar Permisos

```bash
# Ver permisos de archivos sensibles
ls -la /home/openclaw/.openclaw/.env
ls -la /home/openclaw/.openclaw/openclaw.json
ls -la /home/openclaw/.openclaw/credentials/email/gmail.json

# Output esperado:
# -rw------- 1 openclaw openclaw ... .env
# -rw------- 1 openclaw openclaw ... openclaw.json
# -rw------- 1 openclaw openclaw ... gmail.json
```

### Corregir Permisos

```bash
# Script de corrección
#!/bin/bash
# fix-permissions.sh

# Archivos sensibles
chmod 600 /home/openclaw/.openclaw/.env
chmod 600 /home/openclaw/.openclaw/openclaw.json
chmod 600 /home/openclaw/.openclaw/credentials/email/gmail.json

# Directorios
chmod 700 /home/openclaw/.openclaw
chmod 700 /home/openclaw/.openclaw/agents
chmod 700 /home/openclaw/.openclaw/credentials

# Backups
chmod 700 /root/backups/openclaw
chmod 600 /root/backups/openclaw/*.tar.gz

echo "✅ Permisos corregidos"
```

---

## 3. Permisos de Directorios

### Directorios Críticos

| Directorio | Permisos | Owner | Grupo | Contenido |
|------------|----------|-------|-------|-----------|
| `/home/openclaw/.openclaw` | 700 | openclaw | openclaw | Configuración principal |
| `/home/openclaw/.openclaw/agents` | 700 | openclaw | openclaw | Agentes y sesiones |
| `/home/openclaw/.openclaw/credentials` | 700 | openclaw | openclaw | Credenciales |
| `/var/lib/openclaw` | 700 | openclaw | openclaw | Database SQLite |
| `/var/log/openclaw` | 755 | openclaw | syslog | Logs |
| `/root/backups/openclaw` | 700 | root | root | Backups |
| `/opt/openclaw-*` | 755 | root | root | Módulos Python |

### Explicación de Permisos

| Permiso | Notación | Significado |
|---------|----------|-------------|
| 700 | drwx------ | Owner: rwx, Grupo: ---, Otros: --- |
| 755 | drwxr-xr-x | Owner: rwx, Grupo: r-x, Otros: r-x |
| 600 | -rw------- | Owner: rw-, Grupo: ---, Otros: --- |
| 644 | -rw-r--r-- | Owner: rw-, Grupo: r--, Otros: r-- |

### Verificar Directorios

```bash
# Ver permisos de directorios
ls -la /home/openclaw/ | grep .openclaw
ls -la /var/lib/ | grep openclaw
ls -la /root/backups/ | grep openclaw

# Output esperado:
# drwx------ ... .openclaw
# drwx------ ... openclaw
# drwx------ ... openclaw
```

---

## 4. Permisos de Usuario

### Usuarios del Sistema

| Usuario | UID | Shell | Propósito |
|---------|-----|-------|-----------|
| `root` | 0 | /bin/bash | Administración |
| `openclaw` | 1001 | /bin/bash | Ejecución de OpenClaw |

### Usuario openclaw

**Creación:**
```bash
sudo useradd -m -s /bin/bash openclaw
```

**Permisos:**
- ✅ Puede leer/escribir en `/home/openclaw/.openclaw`
- ✅ Puede leer/escribir en `/var/lib/openclaw`
- ✅ Puede ejecutar OpenClaw CLI
- ❌ No tiene permisos sudo
- ❌ No puede leer archivos de root

**Verificación:**
```bash
# Ver información del usuario
id openclaw
# Output: uid=1001(openclaw) gid=1001(openclaw) groups=1001(openclaw)

# Ver shell
grep openclaw /etc/passwd
# Output: openclaw:x:1001:1001::/home/openclaw:/bin/bash
```

### Servicios que corren como root

| Servicio | User | Razón |
|----------|------|-------|
| `openclaw` | openclaw | Gateway (no requiere root) |
| `openclaw-email` | root | Necesita acceso a credenciales |
| `openclaw-orchestrator` | root | Necesita acceso a credenciales |

---

## 5. Permisos de Herramientas

### Tools Profile: messaging

**Configuración:**
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
    ]
  }
}
```

### Matriz de Permisos de Herramientas

| Herramienta | Permitida | Requiere Confirmación | Notas |
|-------------|-----------|----------------------|-------|
| **LLM/Chat** | ✅ Sí | ❌ No | Core functionality |
| **Browser** | ✅ Sí | ❌ No | Con SSRF protection |
| **Filesystem** | ❌ No | N/A | Denegado por profile |
| **Exec** | ⚠️ Ask | ✅ Siempre | security: deny, ask: always |
| **Cron** | ❌ No | N/A | En group:automation |
| **Webhook** | ❌ No | N/A | En group:automation |
| **Gateway** | ❌ No | N/A | Herramienta administrativa |
| **Sessions** | ⚠️ Limitado | N/A | spawn/send denegados |

### Elevated Tools

**Configuración:**
```json
{
  "elevated": {
    "enabled": false
  }
}
```

**Qué son elevated tools:**
- Herramientas que requieren privilegios de root
- Acceso a puertos privilegiados (<1024)
- Operaciones de sistema sensibles

**Por qué están desactivados:**
- ✅ Previene escalada de privilegios
- ✅ No necesarios para funcionalidad básica
- ✅ Reduce superficie de ataque

---

## 6. Auditoría de Permisos

### Script de Auditoría

```bash
#!/bin/bash
# audit-permissions.sh

echo "=== OPENCLAW PERMISSIONS AUDIT ==="
echo ""

ISSUES=0

# Verificar archivos sensibles
echo "📁 ARCHIVOS SENSIBLES:"
for file in \
    /home/openclaw/.openclaw/.env \
    /home/openclaw/.openclaw/openclaw.json \
    /home/openclaw/.openclaw/credentials/email/gmail.json
do
    if [ -f "$file" ]; then
        perms=$(stat -c "%a" "$file")
        if [ "$perms" = "600" ]; then
            echo "   ✅ $file: $perms"
        else
            echo "   ❌ $file: $perms (debería ser 600)"
            ISSUES=$((ISSUES + 1))
        fi
    else
        echo "   ⚠️  $file: No existe"
    fi
done

# Verificar directorios
echo ""
echo "📂 DIRECTORIOS:"
for dir in \
    /home/openclaw/.openclaw \
    /home/openclaw/.openclaw/agents \
    /var/lib/openclaw \
    /root/backups/openclaw
do
    if [ -d "$dir" ]; then
        perms=$(stat -c "%a" "$dir")
        if [ "$perms" = "700" ]; then
            echo "   ✅ $dir: $perms"
        else
            echo "   ❌ $dir: $perms (debería ser 700)"
            ISSUES=$((ISSUES + 1))
        fi
    else
        echo "   ⚠️  $dir: No existe"
    fi
done

# Verificar owner
echo ""
echo "👤 OWNER DE ARCHIVOS:"
for file in \
    /home/openclaw/.openclaw/.env \
    /home/openclaw/.openclaw/openclaw.json
do
    if [ -f "$file" ]; then
        owner=$(stat -c "%U:%G" "$file")
        if [ "$owner" = "openclaw:openclaw" ]; then
            echo "   ✅ $file: $owner"
        else
            echo "   ❌ $file: $owner (debería ser openclaw:openclaw)"
            ISSUES=$((ISSUES + 1))
        fi
    fi
done

# Verificar scripts
echo ""
echo "🔧 SCRIPTS:"
for script in \
    /usr/local/bin/openclaw-token \
    /usr/local/bin/openclaw-backup \
    /usr/local/bin/openclaw-watchdog \
    /usr/local/bin/openclaw-dashboard
do
    if [ -f "$script" ]; then
        perms=$(stat -c "%a" "$script")
        if [ "$perms" = "755" ]; then
            echo "   ✅ $script: $perms"
        else
            echo "   ❌ $script: $perms (debería ser 755)"
            ISSUES=$((ISSUES + 1))
        fi
    fi
done

# Resumen
echo ""
echo "=== RESUMEN ==="
if [ $ISSUES -eq 0 ]; then
    echo "✅ Todos los permisos son correctos"
else
    echo "⚠️  Se encontraron $ISSUES issues de permisos"
fi

exit $ISSUES
```

### Ejecutar Auditoría

```bash
# Hacer ejecutable
chmod +x audit-permissions.sh

# Ejecutar
./audit-permissions.sh

# Output esperado:
# === OPENCLAW PERMISSIONS AUDIT ===
# ✅ Todos los permisos son correctos
```

### Corregir Issues

```bash
# Si hay issues, ejecutar:
sudo chown -R openclaw:openclaw /home/openclaw/.openclaw
sudo chmod 700 /home/openclaw/.openclaw
sudo chmod 600 /home/openclaw/.openclaw/.env
sudo chmod 600 /home/openclaw/.openclaw/openclaw.json
```

---

## 7. Permisos de Canal (Telegram)

### dmPolicy: allowlist

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

### Matriz de Permisos de Telegram

| Acción | Permitida | Notas |
|--------|-----------|-------|
| Enviar mensajes (allowlist) | ✅ Sí | Solo usuarios autorizados |
| Enviar mensajes (no allowlist) | ❌ No | Rechazado con log |
| Comandos (/start, /help, etc.) | ✅ Sí | Solo usuarios autorizados |
| Grupos | ❌ No | groupPolicy: disabled |
| Canales | ❌ No | No soportado |

### Añadir Usuario a Allowlist

```json
{
  "channels": {
    "telegram": {
      "allowFrom": ["795606301", "123456789"]
    }
  }
}
```

**Obtener Chat ID:**
1. Enviar mensaje al bot
2. Ver logs: `journalctl -u openclaw-orchestrator -f`
3. Buscar `user_id` en logs
4. Añadir a allowlist

---

**Fin del documento de Permissions**
