# 🦞 OPENCLAW-city

**Sistema Enterprise OpenClaw con Memoria, RAG, Seguridad y Observabilidad**

[![Versión](https://img.shields.io/badge/versión-2026.3.10-blue)](https://github.com/Ruben-Alvarez-Dev/OPENCLAW-city)
[![Estado](https://img.shields.io/badge/estado-production-green)](https://github.com/Ruben-Alvarez-Dev/OPENCLAW-city)
[![Licencia](https://img.shields.io/badge/licencia-MIT-yellow)](LICENSE)

---

## 📖 Descripción

**OPENCLAW-city** es una implementación enterprise-grade del framework OpenClaw, diseñada para operar en producción con:

- ✅ **Memoria Persistente** - SQLite con conversaciones, perfiles de usuario y memorias a largo plazo
- ✅ **RAG (Retrieval-Augmented Generation)** - Búsqueda semántica con embeddings de Mistral API
- ✅ **Security Pipeline** - Auditorías automáticas, detección de anomalías y scoring de seguridad
- ✅ **Observabilidad** - Dashboard CLI, métricas, logs y health checks
- ✅ **Email Bridge** - Integración con Gmail con human-in-the-loop
- ✅ **Telegram Bot (Ramiro)** - Asistente personal con contexto de conversación
- ✅ **Hardening de Seguridad** - 4 capas de seguridad (red, autenticación, tools, aislamiento)

---

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CAPA DE ACCESO (TAILSCALE)                          │
│  • HTTPS vía Tailscale Serve (puerto 443)                                   │
│  • Túnel VPN encryptado (WireGuard)                                         │
│  • ACL: Solo dispositivos autorizados → VPS                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         OPENCLAW GATEWAY (localhost:18789)                  │
│  • Binding: 127.0.0.1 (loopback-only)                                       │
│  • Autenticación: Token requerido                                           │
│  • Tools Profile: messaging (restringido)                                   │
│  • Browser: SSRF protection activado                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
        ┌───────────────────┐ ┌─────────────────┐ ┌─────────────────┐
        │  MEMORY STORE     │ │  RAG STORE      │ │  SECURITY       │
        │  (SQLite)         │ │  (Embeddings)   │ │  PIPELINE       │
        │                   │ │                 │ │                 │
        │  • conversations  │ │  • mistral-     │ │  • audit        │
        │  • user_profiles  │ │    embed        │ │  • health check │
        │  • long_term_     │ │  • cosine       │ │  • anomaly      │
        │    memory         │ │    similarity   │ │    detection    │
        │  • security_logs  │ │  • text search  │ │  • scoring      │
        │  • metrics        │ │    fallback     │ │                 │
        └───────────────────┘ └─────────────────┘ └─────────────────┘
                    │
                    ▼
        ┌───────────────────────────────────────────────────────────┐
        │              SERVICIOS ADICIONALES                        │
        │  • Email Bridge (Gmail IMAP/SMTP + Telegram)              │
        │  • Orchestrator Bot (Ramiro - Telegram)                   │
        │  • Watchdog (monitoreo de configuración)                  │
        │  • Backup automático (diario)                             │
        └───────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerrequisitos

- VPS con Ubuntu 22.04+ o Debian 11+
- Tailscale instalado y configurado
- Node.js 18+ (para OpenClaw)
- Python 3.10+ (para módulos adicionales)
- Cuenta en Mistral AI (o OpenAI/Anthropic)

### Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/Ruben-Alvarez-Dev/OPENCLAW-city.git
cd OPENCLAW-city

# 2. Copiar configuración
cp configs/.env.example /home/openclaw/.openclaw/.env
cp configs/openclaw.json.example /home/openclaw/.openclaw/openclaw.json

# 3. Editar variables de entorno
sudo nano /home/openclaw/.openclaw/.env

# 4. Instalar dependencias
sudo ./scripts/install.sh

# 5. Iniciar servicios
sudo systemctl daemon-reload
sudo systemctl enable openclaw openclaw-email openclaw-orchestrator
sudo systemctl start openclaw openclaw-email openclaw-orchestrator

# 6. Verificar estado
sudo systemctl status openclaw
openclaw-dashboard <<< "status"
```

### Verificación

```bash
# Health check del gateway
curl http://127.0.0.1:18789/health

# Dashboard interactivo
openclaw-dashboard

# Auditoría de seguridad
openclaw security audit
```

---

## 📁 Estructura del Proyecto

```
OPENCLAW-city/
├── README.md                      # Este archivo
├── CHANGELOG.md                   # Historial de cambios
├── LICENSE                        # Licencia MIT
├── docs/                          # Documentación detallada
│   ├── ARCHITECTURE.md            # Arquitectura y ADRs
│   ├── INFRASTRUCTURE.md          # Infraestructura y VPS
│   ├── OPENCLAW-GATEWAY.md        # Configuración del gateway
│   ├── EMAIL-BRIDGE.md            # Integración con Gmail
│   ├── ORCHESTRATOR-BOT.md        # Bot de Telegram (Ramiro)
│   ├── MEMORY-STORE.md            # Sistema de memoria SQLite
│   ├── RAG-STORE.md               # Búsqueda semántica
│   ├── SECURITY-PIPELINE.md       # Auditorías y monitoreo
│   ├── DASHBOARD.md               # CLI dashboard
│   ├── DEPLOYMENT.md              # Guía de despliegue
│   ├── MAINTENANCE.md             # Mantenimiento y troubleshooting
│   ├── SECURITY-MODEL.md          # Modelo de seguridad (4 capas)
│   ├── PERMISSIONS.md             # Sistema de permisos
│   └── AUDIT-TRAIL.md             # Logging y auditoría
├── .github/                       # Templates de GitHub
│   ├── CONTRIBUTING.md            # Guía de contribución
│   ├── SECURITY.md                # Política de seguridad
│   └── CODE_OF_CONDUCT.md         # Código de conducta
├── scripts/                       # Scripts de instalación y utilidades
│   ├── install.sh                 # Instalación automática
│   ├── openclaw-token             # Gestión de tokens
│   ├── openclaw-backup            # Backups
│   ├── openclaw-watchdog          # Monitoreo
│   └── openclaw-alerts            # Alertas
├── configs/                       # Configuraciones de ejemplo
│   ├── .env.example               # Variables de entorno (template)
│   ├── openclaw.json.example      # Configuración del gateway
│   └── systemd/                   # Servicios systemd
└── src/                           # Código fuente (módulos Python)
    ├── memory_store.py            # Memoria SQLite
    ├── rag_store.py               # RAG con embeddings
    ├── security_pipeline.py       # Security pipeline
    ├── email_bridge.py            # Email bridge
    └── orchestrator_bot.py        # Telegram bot
```

---

## 🔗 Enlaces a Documentación

| Documento | Descripción |
|-----------|-------------|
| [Arquitectura](docs/ARCHITECTURE.md) | Diagramas, componentes y ADRs |
| [Infraestructura](docs/INFRASTRUCTURE.md) | VPS, Tailscale, UFW, systemd |
| [Gateway](docs/OPENCLAW-GATEWAY.md) | Configuración y hardening |
| [Email Bridge](docs/EMAIL-BRIDGE.md) | Gmail integration |
| [Orchestrator Bot](docs/ORCHESTRATOR-BOT.md) | Ramiro (Telegram) |
| [Memory Store](docs/MEMORY-STORE.md) | SQLite schema y API |
| [RAG Store](docs/RAG-STORE.md) | Embeddings y búsqueda |
| [Security Pipeline](docs/SECURITY-PIPELINE.md) | Auditorías y scoring |
| [Dashboard](docs/DASHBOARD.md) | CLI de observabilidad |
| [Deployment](docs/DEPLOYMENT.md) | Instalación paso a paso |
| [Maintenance](docs/MAINTENANCE.md) | Tareas y troubleshooting |

---

## 🛡️ Seguridad

El sistema implementa **4 capas de seguridad**:

| Capa | Componente | Estado |
|------|------------|--------|
| 1. Red | Gateway loopback + Tailscale + UFW | ✅ Activo |
| 2. Autenticación | Token gateway + Telegram allowlist | ✅ Activo |
| 3. Herramientas | Tools profile messaging + SSRF protection | ✅ Activo |
| 4. Aislamiento | Session dmScope + sandbox de agentes | ✅ Activo |

**Security Score Actual:** 100/100

Ver [docs/SECURITY-MODEL.md](docs/SECURITY-MODEL.md) para detalles completos.

---

## 📊 Estado del Sistema

### Componentes Activos

| Componente | Estado | Ubicación |
|------------|--------|-----------|
| OpenClaw Gateway | ✅ Activo | `localhost:18789` |
| Memory Store | ✅ Activo | `/var/lib/openclaw/memory.db` |
| RAG Store | ✅ Activo | `/opt/openclaw-memory/` |
| Security Pipeline | ✅ Activo (cron hourly) | `/opt/openclaw-security/` |
| Email Bridge | ✅ Activo | `/opt/openclaw-email-bridge/` |
| Orchestrator Bot | ✅ Activo | `/opt/openclaw-orchestrator/` |
| Dashboard CLI | ✅ Activo | `/usr/local/bin/openclaw-dashboard` |
| Watchdog | ✅ Activo (cron minutely) | `/usr/local/bin/openclaw-watchdog` |
| Backup | ✅ Activo (cron daily 3AM) | `/usr/local/bin/openclaw-backup` |

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

Ver [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) para detalles.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para detalles.

---

## 📞 Contacto

- **GitHub:** [@Ruben-Alvarez-Dev](https://github.com/Ruben-Alvarez-Dev)
- **Documentación Oficial OpenClaw:** https://docs.openclaw.ai
- **Reportar bugs de seguridad:** security@openclaw.ai

---

**Última actualización:** 2026-03-10  
**Versión del sistema:** 2026.3.10
