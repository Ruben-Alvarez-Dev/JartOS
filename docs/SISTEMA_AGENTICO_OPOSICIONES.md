# Sistema Agéntico para Oposiciones FP Hostelería

> **Documento de Arquitectura Final**  
> Versión: 1.0 | Fecha: 2025-03-16 | Estado: Planificación

---

## 1. Resumen Ejecutivo

### Objetivo del Proyecto

Construir un **sistema operativo agéntico personal** (basado en JartOS) diseñado para:

- Optimizar la preparación de **oposiciones docentes FP Hostelería** (Junio)
- Obtener la **certificación Microsoft IA-102**
- Gestionar **vida saludable** (ejercicio, dieta, descanso)

### Principios Fundamentales

| Principio | Descripción |
|-----------|-------------|
| **Seguridad** | Aislamiento de red, gestión de secrets, protección de datos |
| **Trazabilidad** | Logging enterprise, versionado atómico, "rebobinado" posible |
| **Calidad Normativa** | Validación automática contra currículo oficial (BOE) |
| **Eficiencia** | Automatización de tareas administrativas, foco en estudio de calidad |

---

## 2. Arquitectura en Tiers (JartOS)

### 2.1 Estructura de Directorios

```
/PROYECTO_OPOSICIONES/
│
├── /00_SISTEMA/
│   ├── /config/                    # Configuraciones centralizadas
│   │   ├── agentes_config.json
│   │   ├── prompts_maestros/
│   │   └── reglas_calidad.md
│   ├── /logs/                      # Sistema de logging enterprise
│   ├── /versionado/                # Control de versiones atómico
│   └── /backups/                   # Copias de seguridad
│
├── /01_PLANIFICACION/
│   ├── /roadmaps/
│   ├── /cronogramas/
│   └── /metricas/
│
├── /02_CONOCIMIENTO/
│   ├── /00_FUENTES_OFICIALES/      # Currículos BOE (verdad absoluta)
│   ├── /01_TEMARIO/                # Por dominios
│   ├── /02_APOYOS/                 # Apuntes, videos, pizarras
│   └── /03_VERIFICADO/             # Aprobado por Concilio
│
├── /03_AGENTES/
│   ├── /borradores/
│   ├── /revision/
│   └── /entregables/
│
├── /04_ESTUDIO/
│   ├── /flashcards/
│   ├── /practicas_orales/
│   └── /examenes_simulacro/
│
└── /05_PERSONAL/
    ├── /salud/
    └── /bienestar/
```

### 2.2 Tiers de JartOS Utilizados

| Tier | Nombre | Función | Componentes |
|------|--------|---------|-------------|
| **TIER-00** | FOUNDATION | Comunicación interna | NATS, Redis |
| **TIER-02** | SECURITY | Gestión de secrets | Vault, Infisical |
| **TIER-05** | INGEST | Entrada de datos | Pathway (streaming) |
| **TIER-06** | STORAGE | Persistencia | Postgres, Qdrant |
| **TIER-07** | FRAMEWORKS | Orquestación | CrewAI / LangGraph |
| **TIER-08** | WORKFLOWS | Automatización | n8n, Dify |
| **TIER-09** | KNOWLEDGE | Memoria activa | Engram, Mem0, Memento MCP |
| **TIER-10** | USER_APPS | Interfaces | Open WebUI, Home Assistant |
| **TIER-11** | CONTROL | Monitorización | Dashboard JartOS |

---

## 3. Sistema Multi-Agente

### 3.1 Arquitectura Jerárquica

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUARIO                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NIVEL ESTRATÉGICO                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    EL MAESTRO                                ││
│  │        (Orquestador Supremo con Poder de Veto)              ││
│  │                                                              ││
│  │  • Recibe objetivos del usuario                              ││
│  │  • Desglosa tareas                                           ││
│  │  • Asigna trabajo a especialistas                            ││
│  │  • Hace cumplir las "Normas Inamovibles"                     ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   REDACTOR      │ │   INVESTIGADOR  │ │    COACH        │
│   DIDÁCTICO     │ │   NORMATIVO     │ │     ORAL        │
└─────────────────┘ └─────────────────┘ └─────────────────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   NIVEL CONTROL CALIDAD                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      EL CONCILIO                             ││
│  │                                                              ││
│  │  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐     ││
│  │  │   Revisor     │ │   Revisor     │ │   Revisor     │     ││
│  │  │   Jurídico    │ │  Pedagógico   │ │   Técnico     │     ││
│  │  └───────────────┘ └───────────────┘ └───────────────┘     ││
│  │                                                              ││
│  │  Mecanismo: Votación (3/3 votos = APROBADO)                 ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NIVEL SUPERVISIÓN                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      EL DAEMON                               ││
│  │                                                              ││
│  │  • Control de versiones atómico                              ││
│  │  • Logs enterprise (timestamping)                            ││
│  │  • Detección de "deriva" (alucinaciones)                     ││
│  │  • Validación estructural automática                         ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Agentes Especialistas

| ID | Agente | Función Principal | Herramientas |
|----|--------|-------------------|--------------|
| A-01 | **Redactor Didáctico** | Creación de Programaciones y Unidades Didácticas | Plantillas, Qdrant, Normativa |
| A-02 | **Investigador Normativo** | Búsqueda de leyes, jurisprudencia, referencias oficiales | Brave Search, BOE |
| A-03 | **Coach Oral** | Simulación de oposiciones, feedback de exposición | Cámara Pixel, Micrófono, Cronómetro |
| A-04 | **Gestor de Vida** | Agenda, dieta, ejercicio, sueño | Home Assistant, Google Calendar |

### 3.3 El Concilio (Control de Calidad)

| Revisor | Criterio de Validación |
|---------|------------------------|
| **Jurídico** | ¿El contenido cita correctamente el BOE/LOE/LOMCE? ¿La terminología legislativa es exacta? |
| **Pedagógico** | ¿Los objetivos son medibles? ¿Las actividades respetan la taxonomía de Bloom? |
| **Técnico-Hostelero** | ¿El servicio descrito es correcto? ¿El vino marida bien? ¿La técnica es segura? |

**Regla de Oro**: Se necesitan **3 votos de APTO** para que el documento se archive en la "Golden RAG". Si hay rechazo, vuelve al especialista con feedback.

---

## 4. Motor de Conocimiento

### 4.1 Pipeline de Datos (Data Flywheel)

```
DATOS CRUDOS          INGESTA            STRUCTURE           MEMORY
(PDFs,Notas)    →    (Pathway+OCR)    →    (JSONs,MD)    →    (Qdrant+Engram)
                                                              │
     AGENTS    ←    QUALITY CHECK    ←    ┌────────────────────┘
  (Procesan)        (Concilio)            │
       │                                  │
       ▼                                  │
  ┌─────────┐                             │
  │Golden   │◄────────────────────────────┘
  │RAG      │      (Solo verificado)
  └─────────┘
```

### 4.2 Componentes de Memoria

| Componente | Tipo | Función |
|------------|------|---------|
| **Pathway** | Pipeline streaming | Ingesta en tiempo real. Detecta nuevos archivos, procesa y vectoriza automáticamente. |
| **Qdrant** | Vector DB | Almacena embeddings para búsqueda semántica. |
| **Engram (MCP)** | Knowledge Graph | Almacena relaciones entre conceptos. Vital para coherencia estructural. |
| **Mem0 / Memento** | Memoria conversacional | Persistencia de hechos verificados (Currículo Oficial). |

### 4.3 Capas de Conocimiento

| Capa | Contenido | Propósito |
|------|-----------|-----------|
| **Capa 1: Raw/Drafts** | PDFs sucios, OCRs, transcripciones | Inspiración (no es fuente de verdad) |
| **Capa 2: Dominios** | Material por especialidad (Vinos, Sala, Eventos) | Fusión de temario oficial + apuntes propios |
| **Capa 3: Golden RAG** | Contenido verificado por Concilio | Fuente de verdad para estudio |

---

## 5. Fuentes de Verdad Absoluta

### 5.1 Documentos Oficiales

| Fuente | Contenido | Formato |
|--------|-----------|---------|
| **todofp.es** | Currículos FP Básica, Media, Superior | JSON estructurado |
| **BOE** | Reales Decretos, Órdenes Oficiales | JSON estructurado |
| **Junta de Andalucía** | Normativa autonómica | JSON estructurado |

### 5.2 Estructura de Datos Oficiales

```json
{
  "ciclo": "GS Dirección de Servicios de Restauración",
  "modulo": "Gestión de Procesos de Servicio",
  "ra1": {
    "descripcion": "Gestiona los procesos de servicio...",
    "criterios_evaluacion": [
      "a) Se han identificado las fases del proceso...",
      "b) Se han determinado los recursos necesarios...",
      "c) Se han establecido los tiempos de ejecución..."
    ],
    "contenidos_basicos": [
      "Fases del servicio.",
      "Protocolos de servicio.",
      "Calidad en el servicio..."
    ]
  }
}
```

### 5.3 Uso en Validación

Los **Criterios de Evaluación (CE)** se usan como "test cases" en el desarrollo:

1. **Redacción**: El agente genera actividades para cumplir cada CE
2. **Validación**: El Concilio verifica que cada CE tiene su actividad correspondiente
3. **Aprobación**: Solo si todos los CE están cubiertos → Golden RAG

---

## 6. Infraestructura Crítica

### 6.1 Sistema de Logging Enterprise

#### Formato de Log

```json
{
  "timestamp": "2025-03-15T14:32:47.285632+01:00",
  "evento_id": "evt_8f7a3b2c1d",
  "tipo": "DECISION_AGENTE",
  "agente": "Opos-Redactor",
  "modulo": "gestion_sala",
  "accion": "GENERAR_UNIDAD_DIDACTICA",
  "descripcion": "Iniciando generación de UD para RA2",
  "datos_entrada": {
    "ra_id": "RA2",
    "criterios_evaluacion": ["a", "b", "c"]
  },
  "resultado": "ÉXITO",
  "archivos_generados": ["/borradores/ud_gestion_sala_v1.md"],
  "tiempo_ejecucion_ms": 4372,
  "padre_id": "evt_8f7a3b1c0d"
}
```

#### Cobertura

- Terminal (comandos ejecutados)
- Comunicaciones (mensajes entre agentes)
- Decisiones (razonamiento interno)
- Cambios de estado (transiciones de tareas)
- Cambios en archivos (modificaciones)

### 6.2 Control de Versionado Atómico

| Característica | Descripción |
|----------------|-------------|
| **Commits automáticos** | Cada cambio significativo genera commit con metadatos |
| **Backups físicos** | En NVMe 4TB además de Git |
| **Vigilancia de carpetas** | Detección automática de cambios |
| **Recuperación** | Posibilidad de rebobinar a cualquier punto |

### 6.3 Seguridad

| Medida | Implementación |
|--------|----------------|
| **Aislamiento de red** | Docker internal networks |
| **Gestión de API Keys** | Vault (TIER-02) |
| **Entornos separados** | MacBook (pruebas) / Mac Mini (producción) |
| **Firewall** | Solo puertos necesarios |

---

## 7. Flujos de Trabajo

### 7.1 Flujo de Creación de Contenido

```
1. INPUT: Usuario solicita "Unidad Didáctica para RA1"
           │
           ▼
2. MAESTRO: Recupera RA1 de Fuente de Verdad
           │ Asigna tarea a Redactor
           ▼
3. REDACTOR: Genera borrador consultando Qdrant + Engram
           │
           ▼
4. CONCILIO: Revisa contra CEs oficiales
           │
     ┌─────┴─────┐
     │           │
  APROBADO    RECHAZADO
     │           │
     ▼           ▼
5a. Golden RAG  5b. Vuelve a Redactor
                  con feedback
```

### 7.2 Flujo de Vida Sana

```
1. TRIGGER: Hora de estudio bloqueada en Calendar
           │
           ▼
2. HOME ASSISTANT: Activa "Modo Enfoque"
                   • Luces atenuadas
                   • Silencio notificaciones
                   • Música ambiental
           │
           ▼
3. MONITOR: Detecta fatiga o tiempo cumplido
           │
           ▼
4. SUGERENCIA: Pausa + ejercicio TRX
```

### 7.3 Flujo de Ingesta de Material

```
1. TRIGGER: Nuevo archivo en /02_CONOCIMIENTO/
           │
           ▼
2. PATHWAY: Procesa automáticamente
           • OCR si es imagen
           • Transcripción si es audio/video
           • Estructuración si es PDF
           │
           ▼
3. QDRANT: Indexa embeddings
           │
           ▼
4. NOTIFICACIÓN: Sistema avisa de disponibilidad
```

---

## 8. Herramientas de Creación

| Herramienta | Uso | Integración |
|-------------|-----|-------------|
| **Excalidraw** | Esquemas mano alzada (estilo pizarra) | Generación por agentes |
| **Mermaid** | Diagramas de flujo técnicos | Embebido en Markdown |
| **Draw.io** | Diagramas formales (arquitectura) | Exportación PNG/SVG |
| **NotebookLM** | Resúmenes y podcasts de audio-estudio | Via API |

---

## 9. Plan de Implementación

### Fase 0: Cimientos (2-3 días)

- [ ] Clonar y limpiar repo JartOS
- [ ] Levantar TIER-00 (NATS/Redis) y TIER-06 (Qdrant)
- [ ] Configurar sistema de logs
- [ ] Configurar versionado atómico
- [ ] Crear estructura de carpetas maestra

### Fase 1: Motor de Conocimiento (5-7 días)

- [ ] Digitalizar material (OCR, Whisper)
- [ ] Configurar Pathway para ingesta automática
- [ ] Poblar Qdrant y Engram con Fuentes de Verdad
- [ ] Procesar primeras fotos de pizarra con GPT-4 Vision

### Fase 2: Agentes (2-3 días)

- [ ] Configurar Orquestador (MAESTRO)
- [ ] Crear Especialistas (Redactor, Coach Oral)
- [ ] Implementar Concilio (Revisores)
- [ ] Definir System Prompts con normas inamovibles

### Fase 3: Práctica y Vida (Continuo)

- [ ] Integrar Home Assistant
- [ ] Configurar Pixel como cámara de coach
- [ ] Iniciar ciclo de estudio-simulación-feedback
- [ ] Crear primer agente funcional

---

## 10. Stack Tecnológico Final

### Hardware

| Dispositivo | Especificaciones | Rol |
|-------------|------------------|-----|
| **Mac Mini M1** | 16GB RAM, 256GB SSD + 4TB NVMe | Servidor de agentes y modelos locales |
| **MacBook Pro M1 Max** | 32GB RAM, 1TB SSD | Trabajo multimodal, prácticas orales |
| **Pixel 10 Pro XL** | - | Cámara auxiliar para coach oral |
| **Xiaomi Note 12 5G** | - | Móvil dedicado a IA |

### Software y Servicios

| Categoría | Herramienta | Propósito |
|-----------|-------------|-----------|
| **Orquestación** | CrewAI / LangGraph | Coordinación de agentes |
| **Memoria Vectorial** | Qdrant | Búsqueda semántica |
| **Knowledge Graph** | Engram MCP | Relaciones entre conceptos |
| **Pipeline RAG** | Pathway | Ingesta en tiempo real |
| **Automatización** | n8n | Flujos de trabajo |
| **Domótica** | Home Assistant | Rutinas de estudio/descanso |
| **Interfaces** | Open WebUI | Chat con agentes |

### Modelos LLM

| Rol | Modelo | Uso |
|-----|--------|-----|
| **LEAD** | GLM-5 (200K) | Planning & Reasoning |
| **WORKER** | MiniMax-M2.5 (205K) | Fast Execution |
| **Redacción** | Claude 3.5 Sonnet | Escritura de calidad |
| **Multimodal** | GPT-4o | Prácticas orales con visión |

---

## 11. Próximos Pasos Inmediatos

1. **Análisis del Repositorio**: Inspeccionar JartOS existente
2. **Auditoría**: Comparar realidad del repo con esta arquitectura
3. **Fusión**: Decidir qué componentes rescatar/descartar/reescribir
4. **Estandarización**: Aplicar estructura de Tiers sobre proyecto existente

---

## 12. Entidades y Relaciones Clave

### Entidades Principales

| Entidad | Descripción |
|---------|-------------|
| **Usuario** | Preparando oposiciones FP Hostelería |
| **MAESTRO** | Orquestador supremo con poder de veto |
| **Especialistas** | Agentes que ejecutan tareas específicas |
| **Concilio** | Grupo de revisores que validan calidad |
| **Daemon** | Supervisor en segundo plano |
| **Golden RAG** | Base de conocimiento verificada |
| **Fuentes de Verdad** | Currículos oficiales (BOE) |

### Relaciones Principales

```
Usuario ──solicita──▶ MAESTRO
                         │
                         ├──asigna──▶ Especialistas
                         │                │
                         │                └──genera──▶ Borradores
                         │                                │
                         └──supervisa──▶ Concilio ◀──────┘
                                              │
                                              ├──aprobar──▶ Golden RAG
                                              │
                                              └──rechazar──▶ Especialistas
                                                              (con feedback)
```

---

*Documento generado a partir del análisis de la conversación previa*  
*Versión final consolidada - 2025-03-16*