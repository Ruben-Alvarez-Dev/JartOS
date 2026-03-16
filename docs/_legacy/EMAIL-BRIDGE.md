# 📧 Email Bridge

**Integración con Gmail con Human-in-the-Loop**

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Descripción General](#1-descripción-general)
2. [Configuración de Gmail](#2-configuración-de-gmail)
3. [Flujo Human-in-the-Loop](#3-flujo-human-in-the-loop)
4. [Configuración IMAP/SMTP](#4-configuración-imapsmtp)
5. [Notificaciones Telegram](#5-notificaciones-telegram)
6. [Comandos y Troubleshooting](#6-comandos-y-troubleshooting)

---

## 1. Descripción General

El **Email Bridge** es un servicio que conecta Gmail con Telegram, permitiendo:

- ✅ Leer emails nuevos automáticamente
- ✅ Notificar por Telegram con botones interactivos
- ✅ Ejecutar acciones con aprobación del usuario (human-in-the-loop)
- ✅ Responder, archivar o eliminar emails
- ✅ Log de todas las acciones en memory_store

**Ubicación:** `/opt/openclaw-email-bridge/email_bridge.py`  
**Servicio:** `openclaw-email.service`

---

## 2. Configuración de Gmail

### 2.1 Requisitos de Gmail

Para que el Email Bridge funcione, necesitas:

1. **Cuenta Gmail** con IMAP habilitado
2. **App Password** (contraseña de aplicación)
3. **Forwarding** (opcional, para emails específicos)

### 2.2 Habilitar IMAP en Gmail

1. Ir a Gmail → Configuración (engranaje)
2. Ver todas las configuraciones
3. Pestaña "Reenvío y correo POP/IMAP"
4. Sección "Acceso IMAP":
   - ✅ **Habilitar IMAP**
5. Guardar cambios

### 2.3 Crear App Password

**Importante:** Gmail requiere App Password si tienes 2FA activado.

1. Ir a https://myaccount.google.com/security
2. Sección "Iniciar sesión en Google"
3. **Verificación en 2 pasos** (debe estar activado)
4. **Contraseñas de aplicaciones**:
   - Seleccionar app: "Correo"
   - Seleccionar dispositivo: "Otro (nombre personalizado)"
   - Nombre: "OpenClaw Email Bridge"
   - Generar
5. **Copiar contraseña** (16 caracteres, sin espacios)

**Formato:** `xxxx xxxx xxxx xxxx` (16 caracteres)

### 2.4 Configuración de Credenciales

**Archivo:** `/home/openclaw/.openclaw/credentials/email/gmail.json`

```json
{
  "email": "tu.email@gmail.com",
  "password": "xxxx xxxx xxxx xxxx",
  "imap_server": "imap.gmail.com",
  "imap_port": 993,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587
}
```

**Permisos:**
```bash
sudo chmod 600 /home/openclaw/.openclaw/credentials/email/gmail.json
```

---

## 3. Flujo Human-in-the-Loop

### Diagrama de Flujo

```
┌──────────────┐
│  Gmail       │
│  (IMAP)      │
└──────┬───────┘
       │ 1. Polling (cada 60s)
       │    • Conecta IMAP
       │    • Busca emails SIN LEER
       │    • Marca como LEÍDO
       ▼
┌──────────────────────────────────────────────────────────────┐
│  Email Bridge                                                │
│  • Parsea email (asunto, remitente, cuerpo)                  │
│  • Genera ID único para tracking                             │
│  • Guarda estado en state.json                               │
└──────┬───────────────────────────────────────────────────────┘
       │ 2. Notificar
       ▼
┌──────────────────────────────────────────────────────────────┐
│  Telegram Bot                                                │
│  Mensaje con botones inline:                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 📧 Nuevo Email                                          │ │
│  │ De: john@example.com                                    │ │
│  │ Asunto: Reunión mañana                                  │ │
│  │                                                         │ │
│  │ [📖 Leer] [✅ Responder] [🗑️ Eliminar] [📁 Archivar]   │ │
│  └────────────────────────────────────────────────────────┘ │
└──────┬───────────────────────────────────────────────────────┘
       │ 3. Usuario selecciona acción
       ▼
┌──────────────────────────────────────────────────────────────┐
│  Email Bridge                                                │
│  Ejecuta acción seleccionada:                                │
│  • 📖 Leer: Muestra contenido completo                       │
│  • ✅ Responder: Pide texto → envía vía SMTP                 │
│  • 🗑️ Eliminar: Move to Trash                                │
│  • 📁 Archivar: Move to Archive                              │
└──────┬───────────────────────────────────────────────────────┘
       │ 4. Log de acción
       ▼
┌──────────────────┐
│  Memory Store    │
│  log_security_   │
│  event()         │
└──────────────────┘
```

### Estados del Email

**Archivo:** `/opt/openclaw-email-bridge/state.json`

```json
{
  "last_checked": "2026-03-10T15:30:00Z",
  "processed_emails": [
    {
      "id": "msg-001",
      "message_id": "<abc123@gmail.com>",
      "from": "john@example.com",
      "subject": "Reunión mañana",
      "received": "2026-03-10T15:29:00Z",
      "notified": true,
      "action": null,
      "action_timestamp": null
    }
  ]
}
```

---

## 4. Configuración IMAP/SMTP

### 4.1 Parámetros de Conexión

| Parámetro | Valor Gmail | Descripción |
|-----------|-------------|-------------|
| **IMAP Server** | `imap.gmail.com` | Servidor de entrada |
| **IMAP Port** | `993` | Puerto IMAP SSL |
| **SMTP Server** | `smtp.gmail.com` | Servidor de salida |
| **SMTP Port** | `587` | Puerto SMTP TLS |
| **Username** | `tu.email@gmail.com` | Email completo |
| **Password** | App Password | Contraseña de aplicación |

### 4.2 Configuración en el Código

**Fragmento de `email_bridge.py`:**

```python
class GmailBridge:
    def __init__(self):
        self.config = self.load_config()
        self.imap_server = self.config['imap_server']
        self.imap_port = self.config['imap_port']
        self.smtp_server = self.config['smtp_server']
        self.smtp_port = self.config['smtp_port']
        self.email = self.config['email']
        self.password = self.config['password']
```

### 4.3 Conexión IMAP

```python
import imaplib2

# Conectar a IMAP
imap = imaplib2.IMAP4_SSL(self.imap_server, self.imap_port)
imap.login(self.email, self.password)

# Seleccionar bandeja de entrada
imap.select('INBOX')

# Buscar emails SIN LEER
status, messages = imap.search(None, 'UNSEEN')

# Para cada email no leído
for msg_id in messages[0].split():
    # Obtener email completo
    status, msg_data = imap.fetch(msg_id, '(RFC822)')
    
    # Parsear email
    email_message = email.message_from_bytes(msg_data[0][1])
    
    # Extraer datos
    subject = email_message['subject']
    from_email = email_message['from']
    body = self.get_email_body(email_message)
    
    # Marcar como leído
    imap.store(msg_id, '+FLAGS', '\\Seen')
```

### 4.4 Envío SMTP

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to, subject, body, in_reply_to=None):
    # Crear mensaje
    msg = MIMEMultipart()
    msg['From'] = self.email
    msg['To'] = to
    msg['Subject'] = subject
    
    if in_reply_to:
        msg['In-Reply-To'] = in_reply_to
        msg['References'] = in_reply_to
    
    msg.attach(MIMEText(body, 'html'))
    
    # Conectar a SMTP
    smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
    smtp.starttls()
    smtp.login(self.email, self.password)
    
    # Enviar
    smtp.send_message(msg)
    smtp.quit()
```

---

## 5. Notificaciones Telegram

### 5.1 Configuración del Bot

**Token:** `${OPENCLAW_TELEGRAM_BOT_TOKEN}` (mismo que gateway)  
**Chat ID:** `795606301` (usuario autorizado)

### 5.2 Mensaje de Notificación

**Formato:**
```html
📧 <b>Nuevo Email</b>

<b>De:</b> john@example.com
<b>Asunto:</b> Reunión mañana
<b>Fecha:</b> 10/03/2026 15:29

<b>Vista previa:</b>
Hola, ¿podemos reunirnos mañana a las 10am?

<b>Acciones:</b>
```

### 5.3 Botones Inline

**Configuración:**
```python
buttons = {
    'inline_keyboard': [
        [
            {'text': '📖 Leer', 'callback_data': 'email_read_msg-001'},
            {'text': '✅ Responder', 'callback_data': 'email_reply_msg-001'}
        ],
        [
            {'text': '🗑️ Eliminar', 'callback_data': 'email_delete_msg-001'},
            {'text': '📁 Archivar', 'callback_data': 'email_archive_msg-001'}
        ]
    ]
}
```

### 5.4 Manejo de Callbacks

```python
async def handle_callback(update, context):
    query = update.callback_query
    data = query.data  # ej: "email_reply_msg-001"
    
    # Parsear acción y ID
    action, msg_id = data.split('_')[1], data.split('_')[2]
    
    if action == 'read':
        await show_full_email(msg_id)
    elif action == 'reply':
        await ask_reply_text(msg_id)
    elif action == 'delete':
        await delete_email(msg_id)
    elif action == 'archive':
        await archive_email(msg_id)
    
    # Acknowledge callback
    await query.answer()
```

---

## 6. Comandos y Troubleshooting

### 6.1 Gestión del Servicio

```bash
# Iniciar
sudo systemctl start openclaw-email

# Detener
sudo systemctl stop openclaw-email

# Reiniciar
sudo systemctl restart openclaw-email

# Ver estado
sudo systemctl status openclaw-email

# Ver logs
sudo journalctl -u openclaw-email -f

# Habilitar al inicio
sudo systemctl enable openclaw-email
```

### 6.2 Ver Estado

```bash
# Ver state.json
cat /opt/openclaw-email-bridge/state.json | jq

# Ver últimos emails procesados
cat /opt/openclaw-email-bridge/state.json | jq '.processed_emails[-5:]'
```

### 6.3 Logs

**Ubicación:** `/var/log/openclaw/email_bridge.log`

```bash
# Ver logs en vivo
tail -f /var/log/openclaw/email_bridge.log

# Ver errores
grep -i error /var/log/openclaw/email_bridge.log

# Ver últimas 50 líneas
tail -50 /var/log/openclaw/email_bridge.log
```

### 6.4 Problemas Comunes

#### Error de Autenticación IMAP

```
ERROR - Error connecting to IMAP: [AUTHENTICATIONFAILED]
```

**Solución:**
1. Verificar App Password es correcta
2. Verificar 2FA está activado en Gmail
3. Regenerar App Password
4. Actualizar `gmail.json`

#### Error de Conexión SMTP

```
ERROR - SMTP connection failed: Connection timed out
```

**Solución:**
1. Verificar firewall permite salida puerto 587
2. Verificar credenciales SMTP
3. Probar conexión manual:
   ```bash
   telnet smtp.gmail.com 587
   ```

#### Emails no se notifican

**Verificar:**
```bash
# Ver último check
cat /opt/openclaw-email-bridge/state.json | jq '.last_checked'

# Ver si hay emails SIN LEER en Gmail
# Ir a Gmail → Buscar: is:unread
```

#### Botones no responden

**Verificar:**
1. Bot token es correcto
2. Chat ID está en allowlist
3. Logs del orchestrator:
   ```bash
   journalctl -u openclaw-orchestrator -f
   ```

### 6.5 Resetear Estado

```bash
# Detener servicio
sudo systemctl stop openclaw-email

# Backup del estado
cp /opt/openclaw-email-bridge/state.json /root/backups/

# Resetear estado
echo '{"last_checked": null, "processed_emails": []}' > /opt/openclaw-email-bridge/state.json

# Iniciar servicio
sudo systemctl start openclaw-email
```

---

## 7. Seguridad

### 7.1 Credenciales

| Archivo | Permisos | Contenido |
|---------|----------|-----------|
| `gmail.json` | 600 | Email, password, servidores |
| `.env` | 600 | Telegram bot token |

### 7.2 Logs

- ✅ No loguear passwords
- ✅ No loguear contenido completo de emails
- ✅ Loguear solo metadata (asunto, remitente)

### 7.3 State File

- ✅ Guardar solo IDs de mensaje (no contenido)
- ✅ Marcar emails como procesados
- ✅ Permitir re-procesamiento si se borra estado

---

**Fin del documento del Email Bridge**
