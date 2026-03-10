# 📝 Changelog

**Historial de Cambios de OpenClaw-city**

---

## [2026.3.10] - 2026-03-10

### 🎉 Lanzamiento Inicial

Primer release completo del sistema OpenClaw-city con todas las funcionalidades enterprise.

### ✨ Features Agregadas

#### Core System
- ✅ OpenClaw Gateway configurado en loopback (127.0.0.1:18789)
- ✅ Autenticación por token para gateway
- ✅ Tools profile: messaging (mínimo privilegio)
- ✅ Session isolation: per-channel-peer
- ✅ Browser con SSRF protection
- ✅ Agent sandboxing (non-main, workspaceAccess: none)

#### Memoria y RAG
- ✅ Memory Store con SQLite (`/var/lib/openclaw/memory.db`)
- ✅ Tablas: conversations, user_profiles, long_term_memory, security_logs, metrics
- ✅ RAG Store con embeddings de Mistral API (1024 dimensiones)
- ✅ Búsqueda por similitud coseno
- ✅ Fallback a búsqueda por texto

#### Seguridad
- ✅ Security Pipeline automatizada (cron hourly)
- ✅ Health checks de servicios
- ✅ Detección de anomalías
- ✅ Security scoring (0-100)
- ✅ 4 capas de seguridad implementadas
- ✅ UFW firewall configurado
- ✅ Tailscale VPN con ACLs restrictivas

#### Integraciones
- ✅ Telegram Bot (Ramiro) con memoria
- ✅ Email Bridge con Gmail (IMAP/SMTP)
- ✅ Human-in-the-loop para emails
- ✅ Mistral Large como LLM principal

#### Observabilidad
- ✅ Dashboard CLI interactivo
- ✅ Métricas de rendimiento (latencia, tokens, etc.)
- ✅ Logs de seguridad en database
- ✅ Watchdog para monitoreo de configuración
- ✅ Alertas configurables

#### Scripts y Utilidades
- ✅ `openclaw-token` - Gestión de tokens
- ✅ `openclaw-backup` - Backups automáticos
- ✅ `openclaw-watchdog` - Monitoreo de configuración
- ✅ `openclaw-alerts` - Ver alertas
- ✅ `openclaw-dashboard` - Dashboard interactivo
- ✅ `openclaw-tailscale-serve` - Configurar Tailscale Serve

#### Servicios Systemd
- ✅ `openclaw.service` - Gateway
- ✅ `openclaw-email.service` - Email Bridge
- ✅ `openclaw-orchestrator.service` - Telegram Bot

#### Cron Jobs
- ✅ Backup automático (diario 3 AM)
- ✅ Watchdog (cada minuto)
- ✅ Security Pipeline (cada hora)

### 📚 Documentación

- ✅ README.md principal
- ✅ docs/ARCHITECTURE.md - Arquitectura y ADRs
- ✅ docs/INFRASTRUCTURE.md - Infraestructura y VPS
- ✅ docs/OPENCLAW-GATEWAY.md - Configuración del gateway
- ✅ docs/EMAIL-BRIDGE.md - Integración con Gmail
- ✅ docs/ORCHESTRATOR-BOT.md - Bot de Telegram
- ✅ docs/MEMORY-STORE.md - Sistema de memoria
- ✅ docs/RAG-STORE.md - Búsqueda semántica
- ✅ docs/SECURITY-PIPELINE.md - Auditorías y monitoreo
- ✅ docs/DASHBOARD.md - CLI dashboard
- ✅ docs/DEPLOYMENT.md - Guía de despliegue
- ✅ docs/MAINTENANCE.md - Mantenimiento y troubleshooting
- ✅ docs/SECURITY-MODEL.md - Modelo de seguridad
- ✅ docs/PERMISSIONS.md - Sistema de permisos
- ✅ docs/AUDIT-TRAIL.md - Logging y auditoría
- ✅ .github/CONTRIBUTING.md - Guía de contribución
- ✅ .github/SECURITY.md - Política de seguridad
- ✅ .github/CODE_OF_CONDUCT.md - Código de conducta

### 🔧 Configuración

#### Archivos de Configuración
- ✅ `/home/openclaw/.openclaw/openclaw.json` - Configuración principal
- ✅ `/home/openclaw/.openclaw/.env` - Variables de entorno
- ✅ `/home/openclaw/.openclaw/credentials/email/gmail.json` - Credenciales de email

#### Permisos
- ✅ Archivos sensibles: 600
- ✅ Directorios sensibles: 700
- ✅ Scripts: 755
- ✅ Logs: 644

### 🛡️ Seguridad

#### Capa 1: Red
- ✅ Gateway en loopback (127.0.0.1)
- ✅ Tailscale VPN (WireGuard)
- ✅ UFW firewall (deny incoming, allow outgoing)
- ✅ SSH solo desde Tailscale (100.0.0.0/8)

#### Capa 2: Autenticación
- ✅ Token de gateway requerido
- ✅ Telegram dmPolicy: allowlist
- ✅ Chat ID autorizado

#### Capa 3: Herramientas
- ✅ Tools profile: messaging
- ✅ Grupos denegados (automation, runtime, fs)
- ✅ Exec security: deny
- ✅ Browser SSRF protection

#### Capa 4: Aislamiento
- ✅ Session dmScope: per-channel-peer
- ✅ Agent sandbox: non-main
- ✅ mDNS: off
- ✅ Permisos de archivos correctos

### 📊 Métricas Iniciales

| Métrica | Valor |
|---------|-------|
| Security Score | 100/100 |
| Servicios Activos | 3/3 |
| Tailscale Peers | 5 |
| UFW Status | active |
| Backups Configurados | ✅ |

---

## [2026.3.8] - 2026-03-08

### Pre-Lanzamiento

#### Configuración Inicial
- ✅ VPS provisionado (Hetzner, 4 vCPU, 16GB RAM)
- ✅ Ubuntu 22.04 LTS instalado
- ✅ Tailscale configurado
- ✅ UFW firewall básico

#### OpenClaw Instalado
- ✅ OpenClaw CLI instalado
- ✅ Gateway configurado
- ✅ Telegram channel habilitado

---

## Próximas Funcionalidades (Roadmap)

### v2026.4.x
- [ ] Webhooks configurables
- [ ] Múltiples usuarios de Telegram
- [ ] Interfaz web de administración
- [ ] Exportación de conversaciones
- [ ] Integración con más proveedores de LLM

### v2026.5.x
- [ ] RAG con embeddings locales (sentence-transformers)
- [ ] Búsqueda híbrida (vector + texto)
- [ ] Dashboard web
- [ ] API REST para métricas
- [ ] Alertas por email

### v2027.x.x
- [ ] Soporte para múltiples VPS
- [ ] Clustering de gateways
- [ ] Load balancing
- [ ] High availability

---

## Convención de Versiones

Este proyecto sigue [Semantic Versioning](https://semver.org/):

- **YYYY.M.D** - Basado en fecha (año.mes.día)
- **MAJOR.MINOR.PATCH** para releases específicos

### Tipos de Cambios

- **MAJOR** (YYYY): Cambios incompatibles hacia atrás
- **MINOR** (.M): Nuevas features compatibles
- **PATCH** (.D): Bug fixes compatibles

---

## Autores

- **Rubén Álvarez** - [@Ruben-Alvarez-Dev](https://github.com/Ruben-Alvarez-Dev)

---

## Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para detalles.
