# 🌐 JARTOS: MANIFIESTO MAESTRO
## Sistema Operativo Agéntico para Oposiciones FP Hostelería

> **VERSIÓN:** 2.0.0 (Evolucionada)
> **ESTADO:** Producción - Single Source of Truth
> **FECHA:** 2026-03-17

---

## 1. Definición del Sistema

**JartOS** es un ecosistema agéntico jerárquico diseñado para:
- **Preparación de Oposiciones FP Hostelería** (GS Dirección de Servicios de Restauración)
- **Certificación Microsoft IA-102**
- **Entrenamiento multimodal** (Coach Oral con LiveKit)
- **Gestión de vida integrada** (Home Assistant, agenda, rutinas)

---

## 2. Fuentes de Este Documento (Fusión)

Este manifiesto consolida **4 fuentes evolucionadas**:

| Fuente | Tipo | Contribución |
|--------|------|--------------|
| **JartOS (base)** | Repo GitHub | Estructura TIERs, código base |
| **OPENCLAW-city** | Repo paralelo | Seguridad enterprise (4 capas), LiveKit, RAG |
| **OPENCLAW-system** | Repo paralelo | Arquitectura 4 niveles, tri-agente, catedráticos |
| **Conversación Gemini** | hilo + JSON | Reglas, acuerdos, especificaciones finales |

---

## 3. Reglas de Compromiso Inquebrantables

Estas reglas son **PERMANENTES y TRANSVERSALES** - aplican a TODO, SIEMPRE:

### 🔴 Regla Suprema de Veracidad
```
JAMÁS, bajo ninguna circunstancia:
• Usar datos mockup, demo, de prueba o falsos
• Todo debe ser 100% REAL - estamos en PRODUCCIÓN
• JAMÁS afirmar algo sin haberlo COMPROBADO antes
• NO mentiras, NO suposiciones, NO dar NADA por sentado
• NO inventar cosas por cuenta propia
• NO modificar cosas que ya funcionan sin autorización
• Ceñirse 100% a lo pedido y a la realidad
```

### 🔵 Metodología SDD + TDD
1. **Spec-Driven Development (SDD):** Este documento (NEW_SPECS) es la Única Fuente de Verdad
2. **Test-Driven Development (TDD):** Test primero (Red) → Implementar (Green) → Optimizar (Refactor)
3. **PROHIBIDO pasar al siguiente sprint sin tests al 100%**

### 🟢 Gestión de Secretos
- **NUNCA** hardcodear secretos
- **Vault oficial:** 1Password
- **Si hay leak en Git:** `git filter-branch` de raíz, NO parche

### 🟡 Sistema de Calidad (El Concilio)
- **3/3 votos APTO requeridos** (Jurídico, Pedagógico, Técnico)
- Si CUALQUIER voto es NO_APTO → Documento RECHAZADO

### 🟣 Golden RAG (Conocimiento Verificado)
- **5 escalones de destilación** para llegar a Golden RAG
- Alto grado de inmutabilidad, pero NO absoluto (un BOE puede revocar otro)
- Mecanismo de reserva debe existir para casos excepcionales

---

## 4. Índice del ADN Técnico

| # | Documento | Contenido |
|---|-----------|-----------|
| 01 | `01_CONTEXT_AND_INFRASTRUCTURE.md` | Perfil usuario, hardware, objetivos |
| 02 | `02_ARCHITECTURE_AND_SECURITY.md` | TIERs, Anillo Guardián, Docker, 1Password |
| 03 | `03_INGESTION_AND_DATA_FLOW.md` | INBOX/LAB, SQLite, RAG, 5 escalones |
| 04 | `04_AGENT_SYSTEM.md` | Maestro, Especialistas, Concilio, Tri-agente |
| 05 | `05_DEVELOPMENT_ROADMAP.md` | Fases, Sprints TDD |
| 06 | `06_STATE_RECOVERY_PROTOCOL.md` | Formato log estado |
| 07 | `07_API_CONTRACTS.md` | OpenAPI, endpoints |
| 08 | `08_KNOWLEDGE_LAYERS.md` | Motor conocimiento 5 capas |

---

## 5. Hardware del Usuario

| Dispositivo | Specs | Rol |
|-------------|-------|-----|
| **Mac Mini M1** | 16GB, 256GB SSD + 4TB NVMe | Servidor principal, Docker, BD vectoriales |
| **MacBook Pro M1 Max** | 32GB, 1TB SSD | Trabajo intensivo, multimodal |
| **Logitech Brio 4K** | Cámara | Coach Oral (video) |
| **Mikro Anker 360** | Micrófono | Coach Oral (audio) |
| **Home Assistant** | - | Automatización hogar |
| **Tablets/Móviles** | Xiaomi Pad 5, Samsung S9 FE+, Pixel 10 | Dashboards, estudio |

---

## 6. Visión Final (Punto B)

```
┌─────────────────────────────────────────────────────────────────┐
│                    JARTOS - SISTEMA OPERATIVO AGÉNTICO          │
├─────────────────────────────────────────────────────────────────┤
│  ANILLO EXTERNO (El Guardián)                                   │
│  └── API REST localhost:8080                                    │
│  └── Único con token Home Assistant                            │
│  └── Valida y EJECUTA propuestas                               │
├─────────────────────────────────────────────────────────────────┤
│  ANILLO INTERNO (JartOS Core)                                   │
│  └── Docker network: internal: true                            │
│  └── MAESTRO (Orquestador)                                     │
│  └── ESPECIALISTAS (Redactor, Investigador, Coach, Gestor)     │
│  └── CONCILIO (3 votos: Jurídico, Pedagógico, Técnico)        │
│  └── DAEMON (Supervisor, logs)                                 │
├─────────────────────────────────────────────────────────────────┤
│  GOLDEN RAG (Conocimiento Verificado)                           │
│  └── 5 escalones de destilación                                │
│  └── SQLite + Qdrant                                           │
│  └── INBOX (verdad oficial) / LAB (discusión)                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Comando de Producción

```bash
op run --env-file=TIER_02_SECURITY/secrets.template.env -- docker-compose up -d
```
