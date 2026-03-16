# JartOS - Sistema Operativo Agéntico

Sistema operativo personal que integra inteligencia artificial, automatización y productividad, extensible a cualquier dominio.

[![Version](https://img.shields.io/badge/version-0.1.0-blue)](https://github.com/Ruben-Alvarez-Dev/JartOS)
[![Estado](https://img.shields.io/badge/estado-development-yellow)](https://github.com/Ruben-Alvarez-Dev/JartOS)
[![Licencia](https://img.shields.io/badge/licencia-MIT-green)](LICENSE)

---

## Descripción

**JartOS** es un sistema operativo agéntico personal diseñado para ser extensible a cualquier dominio. Actualmente se utiliza para preparación de oposiciones y desarrollo, pero su arquitectura permite adaptarse a necesidades de estudio, trabajo, gestión personal y más.

El sistema fusiona lo mejor de tres proyectos:

- **JartOS** - Sistema de automatización personal con 39GB de conocimiento estructurado
- **OPENCLAW-system** - Framework de agentes de IA con arquitectura jerárquica
- **OPENCLAW-city** - Implementación enterprise con RAG, memoria persistente y voz

### Características Principales

#### Core del Sistema Agéntico
- **Concilio Tri-Agente** - Coordinación inteligente entre Director, Ejecutor y Archivador
- **Sistema de Memoria 4 Niveles** - Contexto jerárquico (Agente, Unidad, Dominio, Global)
- **Arquitectura de 15 Tiers** - Estructura organizativa escalable
- **Sistema de Puertos 1XXYY** - Organización predecible de servicios

#### Funcionalidades Actuales
- **Temario Inteligente** - Ingestión de documentos con chunking semántico y búsqueda RAG
- **Flashcards SM-2** - Repaso espaciado con algoritmo SuperMemo optimizado
- **Generador de Tests** - Tests automáticos desde el temario con análisis de resultados
- **Dashboard Web** - Interfaz moderna para gestionar el sistema
- **IA Predictiva** - Análisis de progreso, áreas débiles y recomendaciones personalizadas
- **Asistente de Voz** - (Opcional) Práctica oral mediante LiveKit + Telegram

#### Extensibilidad
El sistema está diseñado para añadir nuevos dominios:
- **Estudio** - Preparación de exámenes, cursos, certificaciones
- **Desarrollo** - Gestión de proyectos, código, documentación
- **Personal** - Gestión de tareas, notas, salud financiera
- **Empresarial** - Procesos de negocio, CRM, automatización

---

## Arquitectura General

```
+------------------------------------------------------------------+
|                     CAPA DE PRESENTACIÓN                          |
|   +------------------+  +------------------+  +-----------------+ |
|   |   Web Dashboard  |  |   CLI Tools      |  |  Telegram Bot   | |
|   |   (FastAPI)      |  |   (typer)        |  |  (opcional)     | |
|   +------------------+  +------------------+  +-----------------+ |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                     CAPA DE SERVICIOS (Extensible)                |
|   +------------+  +------------+  +------------+  +------------+ |
|   |  Temario   |  | Flashcards |  |   Tests    |  |     AI     | |
|   |  Service   |  |   SM-2     |  |  Generator |  |  Analytics | |
|   +------------+  +------------+  +------------+  +------------+ |
|   +------------+  +------------+  +------------+  +------------+ |
|   |  Dominio X |  |  Dominio Y |  |  Dominio Z |  |     ...    | |
|   |  Service   |  |  Service   |  |  Service   |  |            | |
|   +------------+  +------------+  +------------+  +------------+ |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                     CAPA DE DATOS                                 |
|   +---------------------------+  +-----------------------------+ |
|   |   SQLite (Dominio A)       |  |   SQLite (Dominio B)        | |
|   |   - documents, chunks      |  |   - decks, flashcards       | |
|   |   - embeddings             |  |   - review_logs             | |
|   +---------------------------+  +-----------------------------+ |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                     CAPA DE IA/AGENTES                             |
|   +------------------+  +------------------+  +----------------+ |
|   |   Concilio       |  |   Catedra        |  |  Especialistas | |
|   |   (3 agentes)    |  |   (6 roles)      |  |  (9 agentes)   | |
|   +------------------+  +------------------+  +----------------+ |
|   +------------------+  +------------------+  +----------------+ |
|   |   Mistral API    |  |   MiniMax API    |  |  Local (Ollama)| |
|   |   (embeddings)   |  |   (generación)   |  |   (opcional)   | |
|   +------------------+  +------------------+  +----------------+ |
+------------------------------------------------------------------+
```

---

## Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|------------|---------|
| **Backend** | Python | 3.11+ |
| **Web Framework** | FastAPI | 0.109+ |
| **CLI** | typer + rich | 0.9+ |
| **Base de datos** | SQLite | 3.40+ |
| **Embeddings** | Mistral API (mistral-embed) | - |
| **LLM** | MiniMax (MiniMax-Text-01) | - |
| **Frontend** | HTML/CSS/JS + Tailwind | - |
| **Testing** | pytest | 8.0+ |

---

## Estructura del Repositorio

```
jartos/
+-- README.md                   # Este archivo
+-- docs/
|   +-- 01-CONTEXT.md           # Contexto y visión del sistema
|   +-- 02-ARCHITECTURE.md      # Arquitectura detallada
|   +-- 03-MODULES/             # Documentación de módulos
|   |   +-- temario-ingestion.md
|   |   +-- flashcards-sm2.md
|   |   +-- test-generator.md
|   |   +-- dashboard-web.md
|   |   +-- ai-features.md
|   +-- 04-ROADMAP.md           # Hoja de ruta
|   +-- 05-SOURCE-FILES.md      # Fuentes de referencia
|   +-- 06-FOLDER-STRUCTURE.md  # Estructura de carpetas
|   +-- 07-SETUP.md             # Guía de instalación
|   +-- 08-API-REFERENCE.md     # Referencia de API
|   +-- 09-TESTING.md           # Estrategia de testing
|   +-- 10-AGENTS-SYSTEM.md     # Sistema de agentes
|   +-- 11-MEMORY-SYSTEM.md     # Sistema de memoria
|   +-- 12-EXISTING-CODE.md     # Código existente
|   +-- 13-TELEGRAM-RAMIRO.md   # Bot Telegram
+-- src/
|   +-- core/                   # Dominio y entidades
|   +-- application/            # Lógica de aplicación
|   +-- infrastructure/         # Infraestructura técnica
|   +-- interfaces/             # APIs y UI
|   +-- agents/                 # Sistema de agentes
|   +-- memory/                 # Sistema de memoria
+-- configs/
|   +-- temario.yaml            # Configuración de temario
|   +-- openclaw.json.example   # Template de configuración
+-- data/                       # Datos locales (gitignored)
+-- documents/                  # Documentos de dominio (gitignored)
+-- cache/                      # Cache de embeddings (gitignored)
+-- logs/                       # Logs del sistema (gitignored)
+-- tests/                      # Tests de integración
+-- scripts/                    # Scripts de utilidad
+-- requirements.txt            # Dependencias Python
+-- pytest.ini                  # Configuración de pytest
+-- .env.example                # Template de variables de entorno
+-- .gitignore
```

---

## Quick Start

### Prerrequisitos

- Python 3.11+
- pip o uv (gestor de paquetes)
- Cuenta en Mistral AI (embeddings)
- Cuenta en MiniMax (generación de texto)

### Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/Ruben-Alvarez-Dev/JartOS.git
cd jartos

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# 5. Verificar instalación
python -m pytest tests/ -v
```

### Primer uso

```bash
# Ingerir documento (ejemplo: temario de oposiciones)
python -m src.core.cli ingest documents/temario/Tema1.pdf

# Buscar en el conocimiento
python -m src.core.cli search "constitucion española"

# Crear deck de flashcards
python -m src.application.cli create-deck "Tema 1 - Constitución"

# Generar flashcards automáticamente
python -m src.application.cli generate --tema 1 --count 20

# Repasar flashcards
python -m src.application.cli review "Tema 1 - Constitución"

# Generar test
python -m src.application.cli generate-test --tema 1 --questions 10

# Iniciar dashboard web
python -m src.interfaces.web.app
```

---

## Módulos Principales

### 1. Temario Ingestion ([docs/03-MODULES/temario-ingestion.md](docs/03-MODULES/temario-ingestion.md))

Sistema de ingestión de documentos con chunking semántico y embeddings.

**Características:**
- Soporte para PDF y DOCX
- Chunking inteligente por tokens (~500 tokens)
- Embeddings con Mistral API (1024 dimensiones)
- Búsqueda semántica (similitud coseno)
- Búsqueda híbrida (semántica + keyword)

### 2. Flashcards SM-2 ([docs/03-MODULES/flashcards-sm2.md](docs/03-MODULES/flashcards-sm2.md))

Sistema de flashcards con algoritmo SuperMemo 2 (SM-2).

**Características:**
- Algoritmo SM-2 completo
- Ease factor dinámico (1.3 - 3.0+)
- Intervalos adaptativos
- Generación automática desde temario
- Estadísticas de progreso

### 3. Test Generator ([docs/03-MODULES/test-generator.md](docs/03-MODULES/test-generator.md))

Generador de tests automáticos desde el temario.

**Características:**
- Preguntas de opción múltiple
- Tests de verdadero/falso
- Preguntas abiertas
- Modos: práctica y examen
- Análisis de resultados

### 4. Dashboard Web ([docs/03-MODULES/dashboard-web.md](docs/03-MODULES/dashboard-web.md))

Interfaz web para gestionar el sistema.

**Características:**
- Vista de progreso general
- Gestión de decks y flashcards
- Tomar tests interactivos
- Calendario de repaso
- Métricas y estadísticas

### 5. AI Features ([docs/03-MODULES/ai-features.md](docs/03-MODULES/ai-features.md))

Análisis predictivo y recomendaciones personalizadas.

**Características:**
- Detección de áreas débiles
- Predicción de preparación
- Planes de estudio semanales
- Recomendaciones diarias
- Métricas de aprendizaje

### 6. Sistema de Agentes ([docs/10-AGENTS-SYSTEM.md](docs/10-AGENTS-SYSTEM.md))

Arquitectura de agentes inteligentes.

**Características:**
- Concilio tri-agente (Director, Ejecutor, Archivador)
- Catedra de 6 roles funcionales
- 9 especialistas con namespaces
- Comunicación A2A (Agent-to-Agent)

### 7. Sistema de Memoria ([docs/11-MEMORY-SYSTEM.md](docs/11-MEMORY-SYSTEM.md))

Sistema de memoria jerárquico.

**Características:**
- 4 niveles de memoria (Agente, Unidad, Dominio, Global)
- Persistencia SQLite
- Búsqueda en múltiples niveles
- Contexto entre sesiones

---

## Casos de Uso

### Actual (Oposiciones)

JartOS se utiliza actualmente para preparación de oposiciones:
- Ingestión de temarios en PDF/DOCX
- Búsqueda semántica de conceptos
- Flashcards con repaso espaciado
- Tests automáticos con análisis
- Planificación de estudio con IA

### Actual (Desarrollo)

También se usa para desarrollo de software:
- Gestión de documentación técnica
- Búsqueda en código y specs
- Creación de tests automáticos
- Análisis de dependencias

### Futuro (Extensible)

La arquitectura permite añadir nuevos dominios:
- **Estudio** - Cursos, certificaciones, aprendizaje
- **Personal** - Gestión de tareas, notas, finanzas
- **Empresarial** - CRM, procesos de negocio, automatización
- **Salud** - Seguimiento de métricas, rutinas
- **Cualquier dominio** - Añadir nuevos servicios modularmente

---

## Enlaces a Documentación

| Documento | Descripción |
|-----------|-------------|
| [Contexto](docs/01-CONTEXT.md) | Origen del proyecto, visión y sistemas analizados |
| [Arquitectura](docs/02-ARCHITECTURE.md) | Arquitectura de 5 capas y decisiones de diseño |
| [Módulos](docs/03-MODULES/) | Documentación detallada de cada módulo |
| [Roadmap](docs/04-ROADMAP.md) | Fases de implementación y estimaciones |
| [Source Files](docs/05-SOURCE-FILES.md) | Fuentes de referencia y API keys |
| [Folder Structure](docs/06-FOLDER-STRUCTURE.md) | Estructura de carpetas completa |
| [Setup](docs/07-SETUP.md) | Guía de instalación detallada |
| [API Reference](docs/08-API-REFERENCE.md) | Endpoints y comandos CLI |
| [Testing](docs/09-TESTING.md) | Estrategia de testing |
| [Agents System](docs/10-AGENTS-SYSTEM.md) | Sistema de agentes IA |
| [Memory System](docs/11-MEMORY-SYSTEM.md) | Sistema de memoria y contexto |
| [Existing Code](docs/12-EXISTING-CODE.md) | Código existente a reutilizar |
| [Telegram Ramiro](docs/13-TELEGRAM-RAMIRO.md) | Bot Telegram para Ramiro |

---

## Estado del Desarrollo

| Fase | Estado | Progreso |
|------|--------|----------|
| Fase 1: Core Modules | En desarrollo | 70% |
| Fase 2: Web Dashboard | Pendiente | 0% |
| Fase 3: AI Analytics | Pendiente | 0% |
| Fase 4: Integración | Pendiente | 0% |
| Fase 5: Testing & Docs | Pendiente | 0% |
| Fase 6: Voice Mode | Opcional | 0% |
| Fase 7: Extensibilidad | Planeado | 0% |

Ver [ROADMAP.md](docs/04-ROADMAP.md) para detalles completos.

---

## Filosofía del Proyecto

JartOS no es solo un sistema para oposiciones. Es un **sistema operativo agéntico** diseñado para:

1. **Ser extensible** - Añadir nuevos dominios sin cambiar el core
2. **Mantener contexto** - Memoria jerárquica entre sesiones
3. **Coordinar tareas** - Agentes que trabajan juntos
4. **Evolucionar** - Arquitectura que crece con tus necesidades

El sistema fusiona tres proyectos maduros:
- **JartOS** (39GB de conocimiento, 690 archivos .md, 15 tiers)
- **OPENCLAW-system** (Arquitectura de agentes jerárquica)
- **OPENCLAW-city** (Producción: RAG, memoria, voz)

---

## Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

Ver [CONTRIBUTING.md](.github/CONTRIBUTING.md) para detalles.

---

## Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para detalles.

---

## Contacto

- **GitHub:** [@Ruben-Alvarez-Dev](https://github.com/Ruben-Alvarez-Dev)
- **Proyecto:** https://github.com/Ruben-Alvarez-Dev/JartOS

---

**Última actualización:** 2025-03-16
**Versión:** 0.1.0
