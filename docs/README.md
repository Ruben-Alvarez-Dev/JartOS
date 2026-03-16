# Oposiciones System - Documentacion

Sistema de preparacion de oposiciones con IA, flashcards SM-2, generacion de tests y dashboard web.

## Indice de Documentacion

### Documentos Principales

| Archivo | Descripcion |
|---------|-------------|
| [01-CONTEXT.md](01-CONTEXT.md) | Contexto del proyecto, objetivos y sistemas originales |
| [02-ARCHITECTURE.md](02-ARCHITECTURE.md) | Arquitectura de 5 capas del sistema |
| [03-MODULES/](03-MODULES/) | Especificaciones de cada modulo |
| [04-ROADMAP.md](04-ROADMAP.md) | Roadmap de desarrollo en 6 fases |
| [05-SOURCE-FILES.md](05-SOURCE-FILES.md) | Archivos fuente a copiar y adaptar |
| [06-FOLDER-STRUCTURE.md](06-FOLDER-STRUCTURE.md) | Estructura de carpetas del proyecto |
| [07-SETUP.md](07-SETUP.md) | Guia de instalacion y configuracion |
| [08-API-REFERENCE.md](08-API-REFERENCE.md) | Referencia de CLI y API |
| [09-TESTING.md](09-TESTING.md) | Estrategia de testing |
| [10-AGENTS-SYSTEM.md](10-AGENTS-SYSTEM.md) | Sistema de agentes IA |
| [11-MEMORY-SYSTEM.md](11-MEMORY-SYSTEM.md) | Sistema de memoria y contexto |
| [12-EXISTING-CODE.md](12-EXISTING-CODE.md) | Codigo existente a reutilizar |
| [13-TELEGRAM-RAMIRO.md](13-TELEGRAM-RAMIRO.md) | Bot Telegram para Ramiro |

### Modulos (03-MODULES/)

| Archivo | Descripcion |
|---------|-------------|
| [temario-ingestion.md](03-MODULES/temario-ingestion.md) | Ingesta de temarios (PDF, DOCX, MD) |
| [flashcards-sm2.md](03-MODULES/flashcards-sm2.md) | Sistema de flashcards con algoritmo SM-2 |
| [test-generator.md](03-MODULES/test-generator.md) | Generador de tests automaticos |
| [dashboard-web.md](03-MODULES/dashboard-web.md) | Dashboard web con Next.js 15 |

### Documentacion Legacy

La carpeta [_legacy/](legacy/) contiene documentacion del proyecto original **OPENCLAW-city**, del cual este proyecto deriva parte de su infraestructura.

## Flujo de Trabajo Rapido

```
1. Leer 01-CONTEXT.md    -> Entender el proyecto
2. Leer 02-ARCHITECTURE.md -> Entender la arquitectura
3. Leer 04-ROADMAP.md    -> Ver el plan de desarrollo
4. Leer 07-SETUP.md      -> Instalar el proyecto
5. Leer 03-MODULES/      -> Detalles de cada modulo
```

## Estructura del Proyecto

```
oposiciones-system/
├── docs/                    # Esta documentacion
├── src/
│   ├── core/               # Capa 1: Dominio
│   ├── application/        # Capa 2: Aplicacion
│   ├── infrastructure/     # Capa 3: Infraestructura
│   └── interfaces/         # Capa 4: Interfaces
├── agents/                 # Agentes IA
├── memory/                 # Sistema de memoria
└── cli/                    # Interfaz de linea de comandos
```

## Contacto y Contribucion

Proyecto privado de preparacion de oposiciones. Desarrollado por Ruben.

---

*Ultima actualizacion: Marzo 2026*
