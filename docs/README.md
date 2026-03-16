# JartOS - Documentación

Sistema operativo agéntico personal con inteligencia artificial, automatización y productividad, extensible a cualquier dominio.

## Índice de Documentación

### Documentos Principales

| Archivo | Descripción |
|---------|-------------|
| [01-CONTEXT.md](01-CONTEXT.md) | Contexto del proyecto, visión de sistema operativo agéntico y fusión de 3 sistemas |
| [02-ARCHITECTURE.md](02-ARCHITECTURE.md) | Arquitectura modular y extensible del sistema |
| [03-MODULES/](03-MODULES/) | Especificaciones de cada módulo actual |
| [04-ROADMAP.md](04-ROADMAP.md) | Roadmap de desarrollo en 6 fases |
| [05-SOURCE-FILES.md](05-SOURCE-FILES.md) | Archivos fuente a copiar y adaptar |
| [06-FOLDER-STRUCTURE.md](06-FOLDER-STRUCTURE.md) | Estructura de carpetas del proyecto |
| [07-SETUP.md](07-SETUP.md) | Guía de instalación y configuración |
| [08-API-REFERENCE.md](08-API-REFERENCE.md) | Referencia de CLI y API |
| [09-TESTING.md](09-TESTING.md) | Estrategia de testing |
| [10-AGENTS-SYSTEM.md](10-AGENTS-SYSTEM.md) | Sistema de agentes IA |
| [11-MEMORY-SYSTEM.md](11-MEMORY-SYSTEM.md) | Sistema de memoria y contexto |
| [12-EXISTING-CODE.md](12-EXISTING-CODE.md) | Código existente a reutilizar |
| [13-TELEGRAM-RAMIRO.md](13-TELEGRAM-RAMIRO.md) | Bot Telegram para Ramiro |

### Módulos Actuales (03-MODULES/)

Estos módulos representan el **dominio actual de Oposiciones**. La arquitectura permite añadir módulos para otros dominios.

| Archivo | Descripción | Dominio |
|---------|-------------|---------|
| [temario-ingestion.md](03-MODULES/temario-ingestion.md) | Ingesta de temarios (PDF, DOCX, MD) | Oposiciones |
| [flashcards-sm2.md](03-MODULES/flashcards-sm2.md) | Sistema de flashcards con algoritmo SM-2 | Oposiciones |
| [test-generator.md](03-MODULES/test-generator.md) | Generador de tests automáticos | Oposiciones |
| [dashboard-web.md](03-MODULES/dashboard-web.md) | Dashboard web con Next.js 15 | General |

### Documentación Legacy

La carpeta [_legacy/](legacy/) contiene documentación del proyecto original **OPENCLAW-city**, del cual este proyecto deriva parte de su infraestructura.

## Filosofía de JartOS

### Sistema Operativo Agéntico

JartOS es un **sistema operativo agéntico personal** que integra:

1. **Inteligencia Artificial** - Agentes coordinados que trabajan juntos
2. **Automatización** - Orquestación de tareas complejas
3. **Productividad** - Herramientas para cualquier dominio

### Extensibilidad Total

El sistema está diseñado para **no estar limitado a un dominio específico**:

```
CORE INVARIANTE:
├── Concilio de Agentes (Director, Ejecutor, Archivador)
├── Memoria Jerárquica (4 tipos)
├── Sistema de 15 Tiers
├── Puertos 1XXYY
└── Infraestructura común

DOMINIOS EXTENSIBLES:
├── Oposiciones (Actual)
│   ├── Temario Service
│   ├── Flashcards Service
│   ├── Tests Service
│   └── Analytics Service
├── Desarrollo (Actual)
│   ├── Code Review Service
│   ├── Documentation Service
│   └── Testing Service
└── Cualquier Dominio Futuro
    ├── Servicio específico 1
    ├── Servicio específico 2
    └── ...
```

### Casos de Uso Actuales

#### 1. Oposiciones (Civil Service Exams)

El uso principal actual del sistema:

- **Ingestión de temarios** - PDF/DOCX a conocimiento
- **Búsqueda semántica** - Encontrar conceptos rápidamente
- **Flashcards SM-2** - Repaso espaciado optimizado
- **Tests automáticos** - Evaluación con análisis de resultados
- **Planificación de estudio** - IA que recomienda qué estudiar

#### 2. Desarrollo de Software

Uso secundario actual:

- **Gestión de documentación** - Ingestión de specs, APIs
- **Búsqueda en código** - Búsqueda semántica de funcionalidad
- **Tests automáticos** - Generación desde specs
- **Code review** - Análisis con IA

### Casos de Uso Futuros (Potenciales)

La arquitectura permite añadir **cualquier dominio** simplemente definiendo:

1. Servicios específicos del dominio
2. Memoria de dominio
3. Interfaz (opcional)

Ejemplos:
- **Estudio General** - Cursos, certificaciones, idiomas
- **Gestión Personal** - Tareas, notas, finanzas, salud
- **Empresarial** - CRM, procesos de negocio, automatización
- **Cualquier otro dominio** - Añadir módulos sin tocar el core

## Flujo de Trabajo Rápido

```
1. Leer 01-CONTEXT.md    -> Entender la visión y extensibilidad
2. Leer 02-ARCHITECTURE.md -> Entender la arquitectura modular
3. Leer 04-ROADMAP.md    -> Ver el plan de desarrollo
4. Leer 07-SETUP.md      -> Instalar el proyecto
5. Leer 03-MODULES/      -> Detalles de cada módulo actual
```

## Estructura del Proyecto

```
jartos/
├── docs/                    # Esta documentación
│   ├── 01-CONTEXT.md        # Visión y contexto
│   ├── 02-ARCHITECTURE.md   # Arquitectura
│   ├── 03-MODULES/          # Módulos actuales
│   ├── 10-AGENTS-SYSTEM.md  # Sistema de agentes
│   ├── 11-MEMORY-SYSTEM.md  # Sistema de memoria
│   └── ...
├── src/
│   ├── core/                # Capa 1: Dominio (invariante)
│   ├── application/         # Capa 2: Aplicación (extensible)
│   ├── infrastructure/      # Capa 3: Infraestructura (invariante)
│   ├── interfaces/          # Capa 4: Interfaces (extensible)
│   ├── agents/              # Sistema de agentes (invariante)
│   └── memory/              # Sistema de memoria (invariante)
├── 03-SERVICES/            # Servicios por dominio (extensible)
│   ├── oposiciones/         # Dominio actual 1
│   ├── desarrollo/          # Dominio actual 2
│   └── [futuro-dominio]/    # Dominios futuros
├── agents/                 # Agentes IA
├── memory/                 # Sistema de memoria
└── cli/                    # Interfaz de línea de comandos
```

## Fusion de 3 Sistemas

JartOS nace de la fusión estratégica de tres sistemas:

### 1. JartOS (Original)
- **39 GB de conocimiento estructurado**
- **690 archivos .md documentados**
- **Sistema de 15 Tiers** - Organización jerárquica
- **Sistema de puertos 1XXYY** - Asignación predecible

### 2. OPENCLAW-system
- **Concilio tri-agente** - Director, Ejecutor, Archivador
- **6 Catedráticos** - Roles funcionales
- **9 Especialistas** - Agentes especializados
- **Memoria de 4 tipos** - Jerarquía de contexto

### 3. OPENCLAW-city
- **RAG Store funcional** - Búsqueda semántica
- **Memory Store persistente** - SQLite
- **Security Pipeline** - Validación de inputs
- **Ramiro Bot** - Base para interfaz Telegram
- **LiveKit Server** - Voz en tiempo real

## Principios de Diseño

1. **Extensibilidad** - Añadir dominios sin cambios al core
2. **Contexto Inteligente** - Memoria jerárquica persistente
3. **Coordinación Automática** - Agentes que trabajan juntos
4. **Dominio-Agnóstico** - El core no está atado a un caso de uso
5. **Escalabilidad Horizontal** - Crecer añadiendo, no cambiando

## Contacto y Contribución

- **Desarrollador:** Ruben
- **Licencia:** MIT
- **Filosofía:** Sistema abierto para cualquier dominio

---

*Última actualización: Marzo 2026*
*Versión: 1.0.0 - Sistema Operativo Agéntico*
