# 👤 CONTEXTO, OBJETIVOS E INFRAESTRUCTURA

## 1. Perfil del Usuario ("El Jefe")

### Situación Personal
- **Profesión actual:** Service Desk L1 (actualmente de baja)
- **Formación:** Estudiante de Ingeniería Informática
- **Experiencia previa:** 20 años en hostelería de lujo (Director, Formador, Michelin)
- **Nivel técnico:** Base fullstack, comprensión arquitectónica, NO programador diario (Python novato)
- **Urgencia:** CRÍTICA - Se necesita sistema operativo "YA"

### Objetivos Críticos
| Objetivo | Deadline | Descripción |
|----------|----------|-------------|
| **Oposiciones FP Hostelería** | Junio 2026 | GS Dirección de Servicios de Restauración |
| **Certificación IA-102** | Pendiente | Microsoft AI Engineer |
| **Inglés C1** | Continuo | Preparación via Loora |

### Partes del Temario de Oposiciones
1. **Teoría** - Conocimiento teórico
2. **Programación Didáctica** - Documento estructurado anual
3. **Unidad Didáctica** - Diseño de unidad didáctica
4. **Práctica de Sala** - Demostración práctica de habilidades
5. **Oral** - Defensa ante tribunal (10-15 minutos)

---

## 2. Topología Física y Hardware

### Servidor Principal: Mac Mini M1
| Componente | Especificación |
|------------|----------------|
| CPU | Apple M1 (8 cores) |
| RAM | 16 GB unified |
| SSD interno | 256 GB |
| **Almacenamiento externo** | **4 TB NVMe** (RAG, documentos, BD vectoriales) |
| Red | Gigabit Ethernet |
| Rol | Host Docker, servicios self-hosted, BD |

**Servicios actuales en Mac Mini:**
- n8n (automatización)
- Dify (plataforma LLM)
- Open WebUI
- LobeChat
- Affine
- ConvertX
- **Home Assistant** (crítico - domótica)

### Estación de Trabajo: MacBook Pro M1 Max
| Componente | Especificación |
|------------|----------------|
| CPU | Apple M1 Max (10 cores) |
| RAM | 32 GB unified |
| SSD | 1 TB |
| Rol | Trabajo intensivo, multimodal, desarrollo |

### Periféricos Multimodales
| Dispositivo | Función | Uso en JartOS |
|-------------|---------|---------------|
| Logitech Brio 4K | Cámara | Coach Oral (análisis video) |
| Mikro Anker 360° | Micrófono | Coach Oral (audio, detección muletillas) |
| Google Nest x2 | Altavoces | Feedback de audio |
| Pantallas 27" + 32" | Visualización | Dashboard, estudio |

### Dispositivos Móviles/Tablets
| Dispositivo | Rol |
|-------------|-----|
| Xiaomi Note 12 5G | Dedicado a IA/Sistema |
| Xiaomi Pad 5 | Dashboard de estudio |
| Samsung S9 FE+ | Dashboard de control |
| Pixel 10 Pro XL | Uso general |

---

## 3. Infraestructura de Red y Seguridad

### Configuración de Red
- **Firewall:** UFW (deny incoming, allow outgoing)
- **VPN:** Tailscale (acceso remoto seguro via WireGuard)
- **HTTPS:** Tailscale Serve
- **Bind:** Todos los servicios en `127.0.0.1` (localhost)

### Stack de Seguridad (4 Capas)
| Capa | Componente | Función |
|------|------------|---------|
| 1 | Network | UFW Firewall + Tailscale |
| 2 | Authentication | Token-based + ACLs |
| 3 | Tools | Perfiles restringidos |
| 4 | Isolation | Docker + Sandbox |

### Topología de Red JartOS
```
INTERNET
    │
    ▼
┌─────────────────────────────────────────────────┐
│  TAILSCALE VPN (acceso remoto seguro)           │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│  Mac Mini M1 (Host)                             │
│  ┌───────────────────────────────────────────┐  │
│  │  EL GUARDIÁN (localhost:8080)             │  │
│  │  - Fuera de Docker                        │  │
│  │  - Único con token Home Assistant        │  │
│  └───────────────────────────────────────────┘  │
│                    │                             │
│                    ▼                             │
│  ┌───────────────────────────────────────────┐  │
│  │  DOCKER NETWORK (internal: true)          │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │  JartOS Core                        │  │  │
│  │  │  - Maestro (FastMCP :18789)        │  │  │
│  │  │  - Especialistas                   │  │  │
│  │  │  - Concilio                        │  │  │
│  │  │  - Daemon (logs)                   │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │  LiteLLM Proxy                      │  │  │
│  │  │  - Gestiona API keys               │  │  │
│  │  │  - Habla con Anthropic/OpenAI      │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  Apps Self-Hosted (protegidas):                  │
│  - Home Assistant                               │
│  - n8n                                          │
│  - Dify                                         │
└─────────────────────────────────────────────────┘
```

---

## 4. Topología Lógica (El "Por Qué")

El sistema debe procesar:
- **9 autores de temario** (PDFs crudos)
- **Leyes del BOE** (documentos oficiales)
- **Currículos TODOFP** (fuentes oficiales)

El usuario no puede perder tiempo buscando documentos; necesita que JartOS le diga:
> "El autor A dice Y, pero el BOE dice Z"

De forma instantánea, contrastada y verificada.

---

## 5. Modelos de LLM Configurados

| Rol | Modelo | Contexto | Función |
|-----|--------|----------|---------|
| LEAD | GLM-5 | 200K tokens | Planning & Reasoning |
| WORKER | MiniMax-M2.5-highspeed | 205K tokens | Fast Execution |
| PLANNING | GLM-5 | 200K tokens | Strategic Planning |
| TDD Developer | codestral-latest | - | Desarrollo TDD |
| Tech Lead | mistral-large-latest | - | Liderazgo técnico |
| Backend/DevOps | MiniMax-M2.5 | - | Implementación |

### Proveedores API
- Anthropic (Claude)
- OpenAI (GPT)
- MiniMax
- Mistral
- GLM (vía LiteLLM proxy)

---

## 6. Riesgos Identificados y Mitigaciones

### Riesgos de OpenClaw (base original)
| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| CVE-2026-25253, CVE-2026-25157 (RCE) | CRÍTICA | Aislamiento Docker `internal: true` |
| ClawHub skills maliciosos | ALTA | Pin de versiones, revisión código |
| Exposición 0.0.0.0 por defecto | ALTA | Bind solo 127.0.0.1 |
| Acceso total sistema | CRÍTICA | Contenedor no-root, read-only, cap_drop ALL |
