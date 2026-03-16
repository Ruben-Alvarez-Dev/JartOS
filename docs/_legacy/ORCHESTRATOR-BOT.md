# 🤖 Orchestrator Bot (Ramiro)

**Asistente Personal de IA en Telegram**

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Descripción General](#1-descripción-general)
2. [Identidad y Personalidad](#2-identidad-y-personalidad)
3. [Integración con Memoria](#3-integración-con-memoria)
4. [Contexto de Conversación](#4-contexto-de-conversación)
5. [Perfiles de Usuario](#5-perfiles-de-usuario)
6. [Comandos Disponibles](#6-comandos-disponibles)
7. [Configuración](#7-configuración)

---

## 1. Descripción General

**Ramiro** es el asistente personal de IA que opera en Telegram, conectado directamente a:

- ✅ **Mistral Large** - LLM de última generación
- ✅ **Memory Store** - Memoria persistente de conversaciones
- ✅ **RAG Store** - Búsqueda semántica de información
- ✅ **Email Bridge** - Gestión de emails con aprobación
- ✅ **VPS** - Monitorización del sistema

**Ubicación:** `/opt/openclaw-orchestrator/orchestrator_bot.py`  
**Servicio:** `openclaw-orchestrator.service`

---

## 2. Identidad y Personalidad

### System Prompt

```python
SYSTEM_PROMPT = """
Eres RAMIRO, el asistente personal de IA de Rubén.

TU IDENTIDAD:
- Nombre: Ramiro
- Eres el asistente personal de Rubén, un developer y técnico de sistemas
- Hablas en español de forma cercana pero profesional
- Eres útil, proactivo, pero siempre pides confirmación para acciones críticas

TUS CAPACIDADES:
- Chatear y responder preguntas
- Gestionar emails (Gmail con aprobación)
- Buscar información en web
- Escribir y revisar código
- Monitorizar el sistema (VPS, Tailscale, servicios)

TU PERSONALIDAD:
- Amigable pero profesional
- Conciso pero completo
- Proactivo: anticipas necesidades
- Seguro: verificas antes de actuar

REGLAS:
- NUNCA digas "voy a delegar a un agente" o "uso una herramienta"
- Di "déjame revisar", "ya lo hice", "estoy en ello"
- Los agentes internos son herramientas, no los menciones
- Recuerda que Rubén usa Telegram, Gmail, VPS con Tailscale
"""
```

### Estilo de Comunicación

| Característica | Descripción | Ejemplo |
|----------------|-------------|---------|
| **Tono** | Cercano pero profesional | "¡Hola Rubén! ¿En qué ayudo?" |
| **Longitud** | Conciso pero completo | Párrafos cortos, bullets |
| **Proactividad** | Anticipa necesidades | "¿Quieres que revise tus emails?" |
| **Confirmación** | Pide para acciones críticas | "¿Envío este email?" |
| **Transparencia** | Explica qué hace | "Estoy buscando información sobre..." |

---

## 3. Integración con Memoria

### Memory Store

**Módulo:** `/opt/openclaw-memory/memory_store.py`

**Operaciones:**

```python
from memory_store import get_memory_store

memory = get_memory_store()

# 1. Guardar mensaje del usuario
memory.add_message(
    user_id="telegram:795606301",
    channel="telegram",
    role="user",
    content="Hola Ramiro, ¿cómo estás?"
)

# 2. Obtener contexto (últimos 20 mensajes)
context = memory.get_context(
    user_id="telegram:795606301",
    channel="telegram",
    limit=20
)

# 3. Obtener perfil de usuario
profile = memory.get_user_profile("telegram:795606301")

# 4. Guardar respuesta del asistente
memory.add_message(
    user_id="telegram:795606301",
    channel="telegram",
    role="assistant",
    content="¡Hola Rubén! Estoy bien, ¿en qué ayudo?"
)

# 5. Registrar métricas
memory.record_metric(
    metric_type="bot",
    metric_name="message_received",
    value=1,
    labels={"user_id": "795606301"}
)
```

### Flujo de un Mensaje

```
1. Usuario envía mensaje por Telegram
   │
   ▼
2. Orchestrator recibe update
   │
   ├─→ Verifica autorización (chat_id)
   │
   ├─→ Guarda mensaje en memory_store
   │
   ├─→ Obtiene contexto (últimos 20 mensajes)
   │
   ├─→ Obtiene perfil de usuario
   │
   ├─→ Construye prompt para Mistral
   │     (system + contexto + perfil + mensaje)
   │
   ├─→ Envía a Mistral API
   │
   ├─→ Recibe respuesta
   │
   ├─→ Guarda respuesta en memory_store
   │
   ├─→ Registra métricas (latencia, tokens)
   │
   ├─→ Extrae hechos importantes (opcional)
   │     → Guarda en long_term_memory
   │
   └─→ Responde por Telegram
```

---

## 4. Contexto de Conversación

### Ventana de Contexto

- **Tamaño:** Últimos 20 mensajes
- **Formato:** Lista de mensajes (role + content)
- **Orden:** Cronológico (más antiguo → más reciente)

### Ejemplo de Contexto

```python
context = [
    {"role": "user", "content": "Hola, ¿me ayudas con Python?"},
    {"role": "assistant", "content": "¡Claro! ¿Qué necesitas?"},
    {"role": "user", "content": "¿Cómo leo un archivo JSON?"},
    # ... más mensajes ...
    {"role": "user", "content": "Gracias, funcionó"}
]
```

### Construcción del Prompt

```python
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

# Añadir info del perfil si existe
if profile and profile.get('name'):
    messages.append({
        "role": "system",
        "content": f"El usuario se llama {profile['name']}."
    })

# Añadir historial de conversación
messages.extend(context[-10:])  # Últimos 10 mensajes

# Añadir mensaje actual
messages.append({"role": "user", "content": user_message})
```

---

## 5. Perfiles de Usuario

### Estructura del Perfil

**Tabla:** `user_profiles`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `user_id` | TEXT | ID único (ej: `telegram:795606301`) |
| `name` | TEXT | Nombre del usuario |
| `username` | TEXT | Username de Telegram |
| `channel` | TEXT | Canal (telegram, web, etc.) |
| `preferences` | JSON | Preferencias del usuario |
| `metadata` | JSON | Metadata adicional |
| `created_at` | DATETIME | Fecha de creación |
| `updated_at` | DATETIME | Última actualización |

### Guardar/Actualizar Perfil

```python
# Al iniciar conversación (/start)
memory.save_user_profile(
    user_id="telegram:795606301",
    name="Rubén",
    username="ruben",
    channel="telegram",
    metadata={
        "language": "es",
        "timezone": "Europe/Madrid"
    }
)
```

### Extraer Hechos del Perfil

```python
# Si usuario dice "me llamo Rubén"
if "me llamo" in user_message.lower():
    # Extraer nombre
    name = extract_name(user_message)
    memory.add_memory(
        user_id="telegram:795606301",
        category="personal",
        fact_type="name",
        content=f"Se llama {name}",
        confidence=0.9
    )
```

---

## 6. Comandos Disponibles

### /start

**Descripción:** Iniciar/reiniciar conversación

**Respuesta:**
```
🦞 ¡Hola Rubén! Soy Ramiro

Soy tu asistente personal de IA. Estoy conectado a:
- ✅ Mistral Large (LLM)
- ✅ Gmail (emails con tu aprobación)
- ✅ Tu VPS (monitorización)
- ✅ Tailscale (red segura)

¿Qué puedo hacer?
• 🤖 Chatear y responder preguntas
• 📧 Gestionar emails ("revisa mis emails")
• 💻 Ayudar con código ("escribe una función en Python")
• 🌐 Buscar información ("busca sobre X")
• 📊 Monitorizar sistema ("¿cómo está el VPS?")

Comandos:
/start - Reiniciar conversación
/help - Ayuda completa
/status - Estado del sistema
/clear - Limpiar memoria
/tools - Capacidades
/memory - Ver mi memoria de ti

¡Escribe tu mensaje y empezamos!
```

**Acciones:**
- Guarda/actualiza perfil de usuario
- Limpia conversación anterior
- Envía mensaje de bienvenida
- Registra métrica `command_start`

---

### /help

**Descripción:** Mostrar ayuda completa

**Respuesta:**
```
📚 Ayuda - Comandos de Ramiro

Conversación:
/start - Iniciar/reiniciar bot
/clear - Limpiar conversación actual
/memory - Ver qué recuerdo de ti

Estado:
/status - Estado del sistema
/tools - Capacidades disponibles

Acciones:
• "Revisa mis emails" - Leo Gmail
• "Busca sobre X" - Búsqueda web
• "Escribe código..." - Ayuda con código
• "¿Cómo está el sistema?" - Monitorización

💡 Consejos:
• Sé natural, habla como conmigo
• Puedo recordar contexto de conversación
• Pido aprobación para emails importantes
• Todo queda registrado (observabilidad)
```

---

### /status

**Descripción:** Mostrar estado del sistema

**Respuesta:**
```
📊 Estado del Sistema

Servicios:
Mistral API: ✅ Online
OpenClaw Gateway: ✅ Online
Email Bridge: ✅ Online
Telegram Bot: ✅ Online

Usuario:
Nombre: Rubén
Chat ID: 795606301
Mensajes en conversación: 42

Memoria:
DB: /var/lib/openclaw/memory.db
Tamaño: 128.5 KB
```

**Verificaciones:**
- Mistral API (HTTP GET /models)
- OpenClaw Gateway (HTTP GET /health)
- Email Bridge (systemctl is-active)
- Telegram Bot (online por definición)

---

### /clear

**Descripción:** Limpiar conversación actual

**Respuesta:**
```
🧹 Conversación limpiada. Nueva conversación iniciada.
```

**Acciones:**
- Limpia mensajes de la conversación
- Mantiene perfil de usuario
- Mantiene memorias a largo plazo
- Inicia nueva conversación

---

### /tools

**Descripción:** Mostrar capacidades disponibles

**Respuesta:**
```
🔧 Capacidades de Ramiro

✅ Activas:
• Chat con Mistral Large (LLM)
• Email (Gmail con aprobación)
• Búsqueda web (browser protegido)
• Código (Python, JS, Bash, etc.)
• Monitorización (VPS, servicios)

🔒 Seguridad:
• Human-in-the-loop para emails
• SSRF protection en browser
• Tools restringidos (messaging profile)
• Gateway en loopback (no expuesto)
• Tailscale para acceso remoto

📊 Observabilidad:
• Logs de todas las acciones
• Métricas de rendimiento
• Auditoría de seguridad
• Backups automáticos
```

---

### /memory

**Descripción:** Ver memoria almacenada del usuario

**Respuesta:**
```
🧠 Mi Memoria de Ti

Perfil:
• Nombre: Rubén
• Usuario: ruben
• Canal: telegram

Memorias (5):
• Se llama Rubén...
• Es developer...
• Usa VPS con Tailscale...
• Prefiere español...
• Trabaja con Python...

Últimos mensajes:
• user: Hola, ¿cómo estás?...
• assistant: ¡Bien! ¿En qué ayudo?...
• user: ¿Me ayudas con código?...
```

---

## 7. Configuración

### Variables de Entorno

**Archivo:** `/home/openclaw/.openclaw/.env`

```bash
OPENCLAW_TELEGRAM_BOT_TOKEN=<telegram-bot-token>
OPENCLAW_MISTRAL_API_KEY=<mistral-api-key>
OPENCLAW_MISTRAL_BASE_URL=https://api.mistral.ai/v1
```

### Chat ID Autorizado

**Código:** `orchestrator_bot.py`

```python
CHAT_ID_AUTORIZADO = 795606301
```

**Obtener tu Chat ID:**
1. Enviar mensaje al bot
2. Ver logs: `journalctl -u openclaw-orchestrator -f`
3. Buscar línea con `user_id`
4. Copiar número

### Parámetros de Mistral

```python
MISTRAL_BASE_URL = "https://api.mistral.ai/v1"
MISTRAL_MODEL = "mistral-large-latest"
MAX_TOKENS = 2048
TEMPERATURE = 0.7
```

---

## 8. Troubleshooting

### Bot no responde

```bash
# Verificar servicio
sudo systemctl status openclaw-orchestrator

# Ver logs
sudo journalctl -u openclaw-orchestrator -f

# Verificar token
grep OPENCLAW_TELEGRAM_BOT_TOKEN /home/openclaw/.openclaw/.env
```

### Error de Mistral API

```
ERROR - Error de Mistral: 401 - Invalid API key
```

**Solución:**
1. Verificar API key en `.env`
2. Verificar key no ha expirado
3. Regenerar key en https://console.mistral.ai
4. Actualizar con `openclaw-token mistral api_key <nueva-key>`

### Mensajes no se guardan

```bash
# Verificar database
sqlite3 /var/lib/openclaw/memory.db "SELECT COUNT(*) FROM conversations;"

# Verificar permisos
ls -la /var/lib/openclaw/memory.db
```

---

**Fin del documento del Orchestrator Bot**
