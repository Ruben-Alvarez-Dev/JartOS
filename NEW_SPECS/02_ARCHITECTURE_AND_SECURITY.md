# 🏗️ ARQUITECTURA TÉCNICA Y SEGURIDAD

## 1. Visión General

JartOS adopta una **arquitectura de Anillo de Seguridad** donde el sistema agéntico está aislado y solo puede "proponer" acciones. Un componente externo (**El Guardián**) valida y ejecuta.

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANILLO DE SEGURIDAD JARTOS                   │
├─────────────────────────────────────────────────────────────────┤
│  ANILLO EXTERNO (El Guardián)                                   │
│  └── FastAPI en Host (Mac Mini)                                 │
│  └── Puerto: localhost:8080                                     │
│  └── Único con token Home Assistant                            │
│  └── Valida propuestas → EJECUTA si son seguras                │
├─────────────────────────────────────────────────────────────────┤
│  ANILLO INTERNO (JartOS Core - Docker aislado)                  │
│  └── Docker network: internal: true                            │
│  └── SIN acceso directo a internet                             │
│  └── SIN API keys (usa LiteLLM proxy)                          │
│  └── MAESTRO → ESPECIALISTAS → CONCILIO                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Gestión de Secretos (1Password Vault)

JartOS **NO** almacena secretos en texto plano ni en archivos `.env` locales en producción.

| Aspecto | Detalle |
|---------|---------|
| **Vault oficial** | 1Password |
| **Inyección** | CLI `op` en runtime |
| **Plantilla** | `TIER_02_SECURITY/secrets.template.env` |

### Comando de Producción
```bash
op run --env-file=TIER_02_SECURITY/secrets.template.env -- docker-compose up -d
```

### Búsqueda en 1Password (Regla)
1. Buscar vaults con nombre **exacto, similar, parecido o sugerente** al servicio
2. **JAMÁS tocar vault "Personal"** - es temporal, solo lectura, último recurso
3. Si el nombre del vault no tiene nada que ver → saltar

---

## 3. Los 12 TIERs (Jerarquía de Capas)

| TIER | Nombre | Función | Contenido |
|------|--------|---------|-----------|
| **00** | FOUNDATION | Configuración base | Scripts, `.env`, system prompts |
| **01** | ACCESS | Integraciones de red | Zadarma, APIs externas |
| **02** | SECURITY | Seguridad perimetral | **El Guardián**, gestión secretos |
| **03** | AGENTS | Núcleo agéntico | Maestro, Especialistas, Concilio |
| **04** | INTERFACE | Interfaz usuario | FastAPI Web, Dashboard |
| **05** | INGEST | Sistema de ingesta | Watchdogs INBOX/LAB |
| **06** | STORAGE | Almacenamiento | Volúmenes físicos, BD |
| **07** | FRAMEWORKS | Frameworks | (Reservado) |
| **08** | WORKFLOWS | Flujos de trabajo | (Reservado) |
| **09** | KNOWLEDGE | Conocimiento | **Golden RAG**, Temario, AI |
| **10** | USER_APPS | Apps de usuario | Flashcards, Tests |
| **11** | CONTROL | Supervisión | Daemon, logs, Pytest |

### Mapeo de Código Real
| Código Original | Nueva Ubicación |
|-----------------|-----------------|
| `src/temario/store.py` | `TIER_06_STORAGE/sqlite_store.py` |
| `src/temario/cli.py` | `TIER_05_INGEST/cli.py` |
| `orchestrator/mcp_orchestrator.py` | `TIER_03_AGENTS/livekit_orchestrator.py` |
| `src/ai/*` | `TIER_09_KNOWLEDGE/ai/` |
| `src/tests/*` | `TIER_10_USER_APPS/tests/` |
| `src/flashcards/*` | `TIER_10_USER_APPS/flashcards/` |
| `src/web/*` | `TIER_04_INTERFACE/web/` |

---

## 4. El Guardián (Anillo Externo)

### Especificación
| Aspecto | Valor |
|---------|-------|
| **Framework** | FastAPI |
| **Puerto** | `127.0.0.1:8080` (solo localhost) |
| **Ubicación** | Host (Mac Mini), FUERA de Docker |
| **Token HA** | Único componente con acceso |

### Endpoint Principal
```http
POST http://127.0.0.1:8080/propose_action
Content-Type: application/json

{
  "action": "home_assistant_call",
  "service": "light.turn_on",
  "entity_id": "light.estudio",
  "params": {}
}
```

### Respuesta
```json
{
  "approved": true,
  "executed": true,
  "result": {...},
  "log_id": "20260317_001"
}
```

### Acciones Rechazadas (Ejemplos)
- Borrar BD de Home Assistant
- Ejecutar comandos shell arbitrarios
- Acceder a credenciales
- Modificar configuración del sistema

---

## 5. Docker Compose Base

```yaml
version: '3.8'

services:
  jartos-core:
    build: .
    container_name: jartos-core
    volumes:
      - /Volumes/NVME_4TB/jartos-data:/app/data
      - ./TIER_09_KNOWLEDGE:/app/TIER_09_KNOWLEDGE:ro
    networks:
      - jartos_internal
    environment:
      - PYTHONPATH=/app
      - LITELLM_URL=http://litellm-proxy:4000
    user: "1000:1000"
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true

  litellm-proxy:
    image: ghcr.io/berriai/litellm:main-latest
    container_name: litellm-proxy
    ports:
      - "127.0.0.1:4000:4000"
    volumes:
      - ./config/litellm.yaml:/app/config.yaml
    environment:
      - LITELLM_MASTER_KEY=${LITELLM_MASTER_KEY}
    networks:
      - jartos_internal

  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    ports:
      - "127.0.0.1:6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - jartos_internal

networks:
  jartos_internal:
    internal: true

volumes:
  qdrant_data:
```

---

## 6. Hardening de Contenedor (Obligatorio)

```yaml
# En cada servicio Docker
user: "1000:1000"           # No root
read_only: true              # Filesystem inmutable
cap_drop:
  - ALL                      # Sin capacidades Linux
security_opt:
  - no-new-privileges:true   # Sin escalada de privilegios
```

### Bins Prohibidos (safe-bin policy)
- `mkfs`, `fdisk`, `dd`
- `iptables`, `ip6tables`
- `nc`, `netcat`
- `chmod`, `chown` (en producción)

---

## 7. LiteLLM Proxy (Gestión de APIs)

El proxy LiteLLM es el **único** componente con acceso a las API keys reales.

```yaml
# config/litellm.yaml
model_list:
  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-sonnet-4-6-20250514
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: gpt-4
    litellm_params:
      model: openai/gpt-4-turbo
      api_key: os.environ/OPENAI_API_KEY

  - model_name: minimax
    litellm_params:
      model: minimax/abab6.5s-chat
      api_key: os.environ/MINIMAX_API_KEY
```

**Los agentes NUNCA ven las API keys reales.**
