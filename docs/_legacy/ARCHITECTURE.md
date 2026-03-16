# 🏗️ Arquitectura del Sistema

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Diagrama de Arquitectura Completo](#1-diagrama-de-arquitectura-completo)
2. [Componentes y Responsabilidades](#2-componentes-y-responsabilidades)
3. [Flujos de Datos](#3-flujos-de-datos)
4. [Decisiones Arquitectónicas (ADRs)](#4-decisiones-arquitectónicas-adrs)

---

## 1. Diagrama de Arquitectura Completo

### Vista General del Sistema

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           CAPA DE ACCESO REMOTO                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    TAILSCALE (VPN WireGuard)                            │   │
│  │  • Túnel encryptado punto a punto                                       │   │
│  │  • ACL: Solo dispositivos autorizados → VPS (tag:server)                │   │
│  │  • Serve: Proxy HTTPS 443 → localhost:18789                             │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        │ HTTPS vía Tailscale
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           VPS (Ubuntu 22.04 LTS)                                │
│  IP Tailscale: 100.77.1.100                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    UFW FIREWALL (Capa de Red)                           │   │
│  │  • Default: deny incoming, allow outgoing                               │   │
│  │  • SSH (22): Solo desde 100.0.0.0/8 (Tailscale)                         │   │
│  │  • Gateway (18789): Solo en interfaz tailscale0                         │   │
│  │  • HTTPS (443): Tailscale Serve                                         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                        │
│                                        ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    OPENCLAW GATEWAY (localhost:18789)                   │   │
│  │  • Binding: 127.0.0.1 (loopback-only)                                   │   │
│  │  • Auth: Token requerido                                                │   │
│  │  • Session dmScope: per-channel-peer                                    │   │
│  │  • mDNS: off                                                            │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                        │
│         ┌──────────────────────────────┼──────────────────────────────┐        │
│         │                              │                              │        │
│         ▼                              ▼                              ▼        │
│  ┌──────────────────┐        ┌──────────────────┐          ┌─────────────────┐│
│  │  MEMORY STORE    │        │  RAG STORE       │          │  SECURITY       ││
│  │  (SQLite)        │        │  (Embeddings)    │          │  PIPELINE       ││
│  │                  │        │                  │          │                 ││
│  │  Tablas:         │        │  • Embeddings    │          │  • Audit        ││
│  │  • conversations │        │    (Mistral API) │          │  • Health       ││
│  │  • user_profiles │        │  • Cosine        │          │  • Anomaly      ││
│  │  • long_term_    │        │    similarity    │          │  • Scoring      ││
│  │    memory        │        │  • Text search   │          │                 ││
│  │  • security_logs │        │    fallback      │          │                 ││
│  │  • metrics       │        │                  │          │                 ││
│  └──────────────────┘        └──────────────────┘          └─────────────────┘│
│                                        │                                        │
│         ┌──────────────────────────────┼──────────────────────────────┐        │
│         │                              │                              │        │
│         ▼                              ▼                              ▼        │
│  ┌──────────────────┐        ┌──────────────────┐          ┌─────────────────┐│
│  │  EMAIL BRIDGE    │        │  ORCHESTRATOR    │          │  WATCHDOG       ││
│  │  (Gmail)         │        │  BOT (Telegram)  │          │  (Monitoreo)    ││
│  │                  │        │                  │          │                 ││
│  │  • IMAP polling  │        │  • Ramiro bot    │          │  • Config hash  ││
│  │  • SMTP send     │        │  • Memory int.   │          │  • Health check ││
│  │  • Human-in-     │        │  • Mistral API   │          │  • Permisos     ││
│  │    the-loop      │        │  • Contexto      │          │  • Exposición   ││
│  └──────────────────┘        └──────────────────┘          └─────────────────┘│
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Arquitectura por Capas

```
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 7: PRESENTACIÓN                                           │
│  • Telegram Bot (Ramiro)                                        │
│  • CLI Dashboard                                                │
│  • Tailscale Serve (HTTPS)                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 6: ORQUESTACIÓN                                           │
│  • Orchestrator Bot (Python + python-telegram-bot)              │
│  • Email Bridge (IMAP/SMTP + Telegram)                          │
│  • Gateway (Node.js + OpenClaw CLI)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 5: SERVICIOS                                              │
│  • Memory Store (SQLite)                                        │
│  • RAG Store (Embeddings + Búsqueda)                            │
│  • Security Pipeline (Auditorías)                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 4: DATOS                                                  │
│  • SQLite Database (/var/lib/openclaw/memory.db)                │
│  • Configuration Files (/home/openclaw/.openclaw/)              │
│  • Logs (/var/log/openclaw/)                                    │
│  • Backups (/root/backups/openclaw/)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 3: RED                                                    │
│  • Tailscale (VPN WireGuard)                                    │
│  • UFW Firewall                                                 │
│  • Systemd Networkd                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 2: SISTEMA OPERATIVO                                      │
│  • Ubuntu 22.04 LTS                                             │
│  • Systemd (gestión de servicios)                               │
│  • Usuario dedicado (openclaw)                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 1: HARDWARE                                               │
│  • VPS (Hetzner/Cloud provider)                                 │
│  • CPU, RAM, Storage                                            │
│  • Network Interface                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes y Responsabilidades

### 2.1 OpenClaw Gateway

**Ubicación:** `/usr/bin/openclaw` (CLI)  
**Configuración:** `/home/openclaw/.openclaw/openclaw.json`  
**Puerto:** `18789` (localhost only)

**Responsabilidades:**
- Ejecutar agentes de IA con herramientas restringidas
- Gestionar sesiones por canal (Telegram, etc.)
- Autenticación vía token
- Aplicar políticas de seguridad (tools, browser, filesystem)

**Configuración clave:**
```json
{
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "port": 18789,
    "auth": { "mode": "token" }
  },
  "tools": {
    "profile": "messaging",
    "deny": ["group:automation", "group:runtime", "group:fs"],
    "exec": { "security": "deny", "ask": "always" }
  }
}
```

---

### 2.2 Memory Store

**Ubicación:** `/opt/openclaw-memory/memory_store.py`  
**Database:** `/var/lib/openclaw/memory.db` (SQLite)

**Responsabilidades:**
- Almacenar conversaciones completas (usuario + asistente)
- Gestionar perfiles de usuario
- Guardar memorias a largo plazo (hechos importantes)
- Log de eventos de seguridad
- Registrar métricas de rendimiento

**Schema de tablas:**
```sql
conversations       -- Mensajes de conversaciones
user_profiles       -- Perfiles de usuario
long_term_memory    -- Memorias/hechos importantes (+ embeddings)
security_logs       -- Eventos de seguridad
metrics             -- Métricas de rendimiento
```

---

### 2.3 RAG Store

**Ubicación:** `/opt/openclaw-memory/rag_store.py`

**Responsabilidades:**
- Calcular embeddings de contenido (Mistral API)
- Almacenar embeddings en long_term_memory
- Búsqueda por similitud coseno
- Fallback a búsqueda por texto si no hay embedding

**Algoritmo:**
1. Calcular embedding del query (Mistral API, 1024 dimensiones)
2. Obtener embeddings almacenados del usuario
3. Calcular similitud coseno entre query y cada memoria
4. Retornar top-N resultados sobre threshold

**Fórmula de similitud coseno:**
```
similarity = (A · B) / (||A|| × ||B||)
```

---

### 2.4 Security Pipeline

**Ubicación:** `/opt/openclaw-security/security_pipeline.py`  
**Ejecución:** Cron hourly (`0 * * * *`)

**Responsabilidades:**
- Ejecutar `openclaw security audit` automáticamente
- Health check de servicios (gateway, email, orchestrator)
- Verificar estado de Tailscale y UFW
- Detectar anomalías en logs de seguridad
- Calcular security score (0-100)
- Log de resultados en memory_store

**Métricas calculadas:**
- `security.score`: Score 0-100
- `health.overall`: 1 si healthy, 0 si no
- Eventos de seguridad en security_logs

---

### 2.5 Email Bridge

**Ubicación:** `/opt/openclaw-email-bridge/email_bridge.py`  
**Servicio:** `openclaw-email.service`

**Responsabilidades:**
- Polling de Gmail vía IMAP (cada 60s)
- Notificar emails nuevos por Telegram
- Esperar aprobación del usuario (human-in-the-loop)
- Ejecutar acciones (responder, archivar, eliminar)
- Enviar emails vía SMTP

**Flujo:**
```
1. Polling IMAP → nuevos emails
2. Notificar Telegram con botones
3. Usuario aprueba/rechaza
4. Ejecutar acción (responder/archivar/eliminar)
5. Log en memory_store
```

---

### 2.6 Orchestrator Bot (Ramiro)

**Ubicación:** `/opt/openclaw-orchestrator/orchestrator_bot.py`  
**Servicio:** `openclaw-orchestrator.service`

**Responsabilidades:**
- Recibir mensajes de Telegram
- Guardar/recuperar contexto de memory_store
- Enviar a Mistral API con contexto y perfil
- Guardar respuesta en memory_store
- Registrar métricas (latencia, tokens)
- Extraer hechos importantes para long_term_memory

**Comandos soportados:**
- `/start` - Iniciar conversación
- `/help` - Ayuda
- `/status` - Estado del sistema
- `/clear` - Limpiar conversación
- `/tools` - Capacidades
- `/memory` - Ver memoria del usuario

---

### 2.7 Watchdog

**Ubicación:** `/usr/local/bin/openclaw-watchdog`  
**Ejecución:** Cron minutely (`* * * * *`)

**Responsabilidades:**
- Calcular hash de configuración (.env + openclaw.json)
- Detectar cambios no autorizados
- Verificar health del gateway
- Verificar permisos de archivos sensibles
- Verificar que gateway no esté expuesto públicamente
- Enviar alertas por Telegram (opcional)

---

### 2.8 Dashboard CLI

**Ubicación:** `/usr/local/bin/openclaw-dashboard`

**Responsabilidades:**
- Mostrar estado general (security pipeline)
- Visualizar métricas (últimas 24h, 7d, 30d)
- Mostrar logs de seguridad
- Estadísticas de conversaciones
- Gestionar memorias
- Limpieza de datos antiguos (>30 días)

**Comandos:**
```
dashboard> status          # Estado general
dashboard> metrics 24      # Métricas de 24h
dashboard> security 20     # Últimos 20 logs de seguridad
dashboard> conversations   # Estadísticas de conversaciones
dashboard> memories        # Memorias guardadas
dashboard> cleanup         # Limpiar datos antiguos
dashboard> help            # Ayuda
dashboard> exit            # Salir
```

---

## 3. Flujos de Datos

### 3.1 Flujo de un Mensaje de Telegram

```
┌──────────────┐
│  Usuario     │
│  (Telegram)  │
└──────┬───────┘
       │ 1. Envía mensaje
       ▼
┌──────────────────────────────────────────────────────────────┐
│  Orchestrator Bot                                            │
│  /opt/openclaw-orchestrator/orchestrator_bot.py              │
└──────┬───────────────────────────────────────────────────────┘
       │ 2. Recibe update
       ▼
┌──────────────────────────────────────────────────────────────┐
│  Memory Store                                                │
│  • add_message(user_id, channel, "user", content)            │
│  • get_context(user_id, channel, limit=20)                   │
│  • get_user_profile(user_id)                                 │
└──────┬───────────────────────────────────────────────────────┘
       │ 3. Obtiene contexto + perfil
       ▼
┌──────────────────────────────────────────────────────────────┐
│  Mistral API                                                 │
│  POST /v1/chat/completions                                   │
│  {                                                           │
│    "model": "mistral-large-latest",                          │
│    "messages": [system, context..., user],                   │
│    "max_tokens": 2048                                        │
│  }                                                           │
└──────┬───────────────────────────────────────────────────────┘
       │ 4. Recibe respuesta
       ▼
┌──────────────────────────────────────────────────────────────┐
│  Memory Store                                                │
│  • add_message(user_id, channel, "assistant", response)      │
│  • record_metric("api", "latency_ms", elapsed)               │
│  • record_metric("api", "tokens", used)                      │
└──────┬───────────────────────────────────────────────────────┘
       │ 5. Guarda respuesta + métricas
       ▼
┌──────────────┐
│  Usuario     │
│  (Telegram)  │
│  Recibe      │
│  respuesta   │
└──────────────┘
```

---

### 3.2 Flujo de Security Pipeline (Cron Hourly)

```
┌──────────────┐
│  Cron        │
│  (0 * * * *) │
└──────┬───────┘
       │ 1. Ejecuta
       ▼
┌──────────────────────────────────────────────────────────────┐
│  Security Pipeline                                           │
│  /opt/openclaw-security/security_pipeline.py                 │
└──────┬───────────────────────────────────────────────────────┘
       │
       ├────────────────────────────────────────────┐
       │                                            │
       ▼                                            ▼
┌──────────────────┐                      ┌──────────────────┐
│  Health Checks   │                      │  Security Audit  │
│  • Gateway       │                      │  openclaw        │
│  • Services      │                      │  security audit  │
│  • Tailscale     │                      │                  │
│  • UFW           │                      │                  │
└────────┬─────────┘                      └────────┬─────────┘
         │                                         │
         └──────────────────┬──────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Detect Anomalies│
                  │  • Event spikes  │
                  │  • API errors    │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │  Calculate Score │
                  │  100 - penalties │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │  Log Results     │
                  │  • security_logs │
                  │  • metrics       │
                  │  • log file      │
                  └──────────────────┘
```

---

### 3.3 Flujo de Email Bridge (Human-in-the-Loop)

```
┌──────────────┐
│  Gmail       │
│  (IMAP)      │
└──────┬───────┘
       │ 1. Polling (cada 60s)
       ▼
┌──────────────────────────────────────────────────────────────┐
│  Email Bridge                                                │
│  /opt/openclaw-email-bridge/email_bridge.py                  │
│  • Conecta IMAP                                              │
│  • Busca emails SIN LEER                                     │
│  • Marca como LEÍDO                                          │
└──────┬───────────────────────────────────────────────────────┘
       │ 2. Nuevo email detectado
       ▼
┌──────────────────────────────────────────────────────────────┐
│  Telegram Bot                                                │
│  Notificación con botones:                                   │
│  • 📖 Leer completo                                          │
│  • ✅ Responder                                              │
│  • 🗑️ Eliminar                                               │
│  • 📁 Archivar                                               │
└──────┬───────────────────────────────────────────────────────┘
       │ 3. Usuario selecciona acción
       ▼
┌──────────────────────────────────────────────────────────────┐
│  Email Bridge                                                │
│  Ejecuta acción:                                             │
│  • Leer: Muestra contenido completo                          │
│  • Responder: Pide texto → envía vía SMTP                    │
│  • Eliminar: Move to Trash                                   │
│  • Archivar: Move to Archive                                 │
└──────┬───────────────────────────────────────────────────────┘
       │ 4. Log de acción
       ▼
┌──────────────────┐
│  Memory Store    │
│  log_security_   │
│  event()         │
└──────────────────┘
```

---

## 4. Decisiones Arquitectónicas (ADRs)

### ADR-001: Gateway en Loopback (127.0.0.1)

**Fecha:** 2026-03-10  
**Estado:** Aceptado

**Contexto:**
OpenClaw Gateway puede exponerse públicamente (0.0.0.0) o solo localmente (127.0.0.1).

**Decisión:**
Gateway **solo escucha en 127.0.0.1:18789** (loopback).

**Consecuencias:**
- ✅ No accesible desde internet público
- ✅ Requiere Tailscale para acceso remoto
- ✅ Aísla capa de aplicación de red pública
- ⚠️ Requiere configuración de Tailscale Serve para HTTPS

**Alternativas rechazadas:**
- Exponer en 0.0.0.0 con autenticación: Riesgo muy alto
- Exponer en 0.0.0.0 con firewall: Configuración compleja, riesgo de error humano

---

### ADR-002: SQLite para Memory Store

**Fecha:** 2026-03-10  
**Estado:** Aceptado

**Contexto:**
Necesitamos almacenamiento persistente para conversaciones, perfiles y memorias.

**Decisión:**
Usar **SQLite** en `/var/lib/openclaw/memory.db`.

**Consecuencias:**
- ✅ Sin dependencias externas (no requiere PostgreSQL/MySQL)
- ✅ Fácil backup (archivo único)
- ✅ Suficiente para uso personal (<1M mensajes)
- ✅ Transaccional (ACID)
- ⚠️ No escala a múltiples writers concurrentes
- ⚠️ Backup requiere copiar archivo (puede bloquear lecturas)

**Alternativas rechazadas:**
- PostgreSQL: Overkill para uso personal, requiere servidor
- MongoDB: Complejidad innecesaria, sin transacciones completas
- Redis: Volátil, requiere persistencia configurada

---

### ADR-003: Mistral API para Embeddings

**Fecha:** 2026-03-10  
**Estado:** Aceptado

**Contexto:**
RAG requiere embeddings para búsqueda semántica.

**Decisión:**
Usar **Mistral API** (`mistral-embed`, 1024 dimensiones).

**Consecuencias:**
- ✅ Alta calidad de embeddings
- ✅ Sin infraestructura local (no GPU necesaria)
- ✅ Mismo proveedor que LLM (simplifica configuración)
- ⚠️ Costo por embedding (~$0.0001 por 1K tokens)
- ⚠️ Requiere conexión a internet

**Alternativas rechazadas:**
- sentence-transformers local: Requiere GPU para velocidad, embeddings de menor calidad
- OpenAI embeddings: Más caro, otro proveedor
- Ollama embeddings: Requiere modelo local, más complejo

---

### ADR-004: Tools Profile "messaging"

**Fecha:** 2026-03-10  
**Estado:** Aceptado

**Contexto:**
OpenClaw permite diferentes perfiles de herramientas con distintos niveles de acceso.

**Decisión:**
Usar perfil **`messaging`** (mínimo necesario) + denegar grupos explícitamente.

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

**Consecuencias:**
- ✅ Mínimo privilegio necesario
- ✅ Previene automatización no autorizada
- ✅ Previene ejecución de código arbitrario
- ⚠️ Limita funcionalidades avanzadas (requiere configuración explícita)

**Alternativas rechazadas:**
- Perfil `default`: Demasiados permisos por defecto
- Perfil `full`: Peligroso para producción

---

### ADR-005: Tailscale para Acceso Remoto

**Fecha:** 2026-03-10  
**Estado:** Aceptado

**Contexto:**
Necesitamos acceso remoto seguro al VPS sin exponer servicios públicamente.

**Decisión:**
Usar **Tailscale** (VPN WireGuard) con ACLs restrictivas.

**Configuración:**
- VPS con tag `tag:server`
- ACL: Solo dispositivos → VPS (no VPS → dispositivos)
- Serve: Proxy HTTPS 443 → localhost:18789

**Consecuencias:**
- ✅ Encriptación WireGuard (estado del arte)
- ✅ Autenticación mutua
- ✅ ACL granular
- ✅ Sin puertos abiertos en firewall público
- ⚠️ Dependencia de servicio externo (Tailscale)
- ⚠️ Requiere configuración inicial de ACLs

**Alternativas rechazadas:**
- VPN OpenVPN propio: Complejidad de mantenimiento
- WireGuard manual: Gestión de claves compleja
- SSH tunnel: No escala a múltiples dispositivos fácilmente

---

### ADR-006: Human-in-the-Loop para Email

**Fecha:** 2026-03-10  
**Estado:** Aceptado

**Contexto:**
El sistema puede leer y enviar emails automáticamente.

**Decisión:**
Implementar **human-in-the-loop**: Todas las acciones requieren aprobación explícita.

**Flujo:**
1. Email nuevo → Notificación Telegram
2. Usuario selecciona acción (botones inline)
3. Sistema ejecuta acción aprobada
4. Log de auditoría

**Consecuencias:**
- ✅ Previene envío accidental de emails
- ✅ Usuario tiene control total
- ✅ Audit trail completo
- ⚠️ Requiere interacción manual para cada acción
- ⚠️ No es fully automático

**Alternativas rechazadas:**
- Automático completo: Riesgo de enviar emails incorrectos
- Reglas automáticas + excepciones: Complejidad, riesgo de falsos positivos

---

### ADR-007: Security Pipeline Automatizada

**Fecha:** 2026-03-10  
**Estado:** Aceptado

**Contexto:**
Necesitamos monitoreo continuo de seguridad y salud del sistema.

**Decisión:**
Ejecutar **security pipeline** automáticamente cada hora vía cron.

**Qué hace:**
- `openclaw security audit`
- Health check de servicios
- Verificar Tailscale y UFW
- Detectar anomalías
- Calcular security score

**Consecuencias:**
- ✅ Detección temprana de problemas
- ✅ Audit trail automático
- ✅ Métricas históricas
- ⚠️ Overhead mínimo (ejecución cada hora)
- ⚠️ Logs pueden crecer (rotación necesaria)

**Alternativas rechazadas:**
- Monitoreo en tiempo real: Complejidad, overkill para uso personal
- Manual: Propenso a olvido, sin histórico

---

### ADR-008: Session dmScope "per-channel-peer"

**Fecha:** 2026-03-10  
**Estado:** Aceptado

**Contexto:**
OpenClaw permite configurar aislamiento de sesiones.

**Decisión:**
Usar **`dmScope: per-channel-peer`** para aislar sesiones por canal.

**Consecuencias:**
- ✅ Cada canal (Telegram) tiene sesión aislada
- ✅ Previene fuga de contexto entre canales
- ✅ Aísla agentes entre sí
- ⚠️ Sesiones no comparten contexto (diseño intencional)

**Alternativas rechazadas:**
- `global`: Todas las sesiones comparten contexto (inseguro)
- `per-channel`: Aislamiento solo por canal, no por peer

---

**Fin del documento de Arquitectura**
