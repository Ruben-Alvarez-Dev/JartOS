# Oposiciones System

Sistema integral de preparacion de oposiciones con IA, repaso espaciado y analisis predictivo.

[![Version](https://img.shields.io/badge/version-0.1.0-blue)](https://github.com/Ruben-Alvarez-Dev/oposiciones-system)
[![Estado](https://img.shields.io/badge/estado-development-yellow)](https://github.com/Ruben-Alvarez-Dev/oposiciones-system)
[![Licencia](https://img.shields.io/badge/licencia-MIT-green)](LICENSE)

---

## Descripcion

**Oposiciones System** es una plataforma completa para la preparacion de oposiciones que integra:

- **Temario Inteligente** - Ingestion de documentos con chunking semantico y busqueda RAG
- **Flashcards SM-2** - Repaso espaciado con algoritmo SuperMemo optimizado
- **Generador de Tests** - Tests automaticos desde el temario con analisis de resultados
- **Dashboard Web** - Interfaz moderna para gestionar el estudio
- **IA Predictiva** - Analisis de progreso, areas debiles y recomendaciones personalizadas
- **Asistente de Voz** - (Opcional) Practica oral mediante LiveKit + Telegram

---

## Arquitectura General

```
+------------------------------------------------------------------+
|                     CAPA DE PRESENTACION                          |
|   +------------------+  +------------------+  +-----------------+ |
|   |   Web Dashboard  |  |   CLI Tools      |  |  Telegram Bot   | |
|   |   (FastAPI)      |  |   (typer)        |  |  (opcional)     | |
|   +------------------+  +------------------+  +-----------------+ |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                     CAPA DE SERVICIOS                             |
|   +------------+  +------------+  +------------+  +------------+ |
|   |  Temario   |  | Flashcards |  |   Tests    |  |     AI     | |
|   |  Ingestion |  |   SM-2     |  |  Generator |  |  Analytics | |
|   +------------+  +------------+  +------------+  +------------+ |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                     CAPA DE DATOS                                 |
|   +---------------------------+  +-----------------------------+ |
|   |   SQLite (Temario)        |  |   SQLite (Flashcards/Tests) | |
|   |   - documents             |  |   - decks, flashcards       | |
|   |   - chunks + embeddings   |  |   - review_logs             | |
|   +---------------------------+  +-----------------------------+ |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                     CAPA DE IA/LLM                                |
|   +------------------+  +------------------+  +----------------+ |
|   |   Mistral API    |  |   MiniMax API    |  |  Local (Ollama)| |
|   |   (embeddings)   |  |   (generacion)   |  |   (opcional)   | |
|   +------------------+  +------------------+  +----------------+ |
+------------------------------------------------------------------+
```

---

## Stack Tecnologico

| Componente | Tecnologia | Version |
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
oposiciones-system/
+-- README.md                   # Este archivo
+-- docs/
|   +-- 01-CONTEXT.md           # Contexto y decision de fusion
|   +-- 02-ARCHITECTURE.md      # Arquitectura detallada
|   +-- 03-MODULES/             # Documentacion de modulos
|   |   +-- temario-ingestion.md
|   |   +-- flashcards-sm2.md
|   |   +-- test-generator.md
|   |   +-- dashboard-web.md
|   |   +-- ai-features.md
|   +-- 04-ROADMAP.md           # Hoja de ruta
|   +-- 05-SOURCE-FILES.md      # Fuentes de referencia
|   +-- 06-FOLDER-STRUCTURE.md  # Estructura de carpetas
|   +-- 07-SETUP.md             # Guia de instalacion
|   +-- 08-API-REFERENCE.md     # Referencia de API
|   +-- 09-TESTING.md           # Estrategia de testing
+-- src/
|   +-- temario/                # Ingestion de temario
|   +-- flashcards/             # Sistema de flashcards
|   +-- tests/                  # Generador de tests
|   +-- web/                    # Dashboard web
|   +-- ai/                     # Analisis y predicciones
|   +-- conftest.py             # Configuracion de pytest
+-- configs/
|   +-- temario.yaml            # Configuracion de temario
|   +-- openclaw.json.example   # Template de configuracion
+-- data/                       # Datos locales (gitignored)
+-- documents/                  # Documentos de temario (gitignored)
+-- cache/                      # Cache de embeddings (gitignored)
+-- logs/                       # Logs del sistema (gitignored)
+-- tests/                      # Tests de integracion
+-- scripts/                    # Scripts de utilidad
+-- requirements.txt            # Dependencias Python
+-- pytest.ini                  # Configuracion de pytest
+-- .env.example                # Template de variables de entorno
+-- .gitignore
```

---

## Quick Start

### Prerrequisitos

- Python 3.11+
- pip o uv (gestor de paquetes)
- Cuenta en Mistral AI (embeddings)
- Cuenta en MiniMax (generacion de texto)

### Instalacion

```bash
# 1. Clonar repositorio
git clone https://github.com/Ruben-Alvarez-Dev/oposiciones-system.git
cd oposiciones-system

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# 5. Verificar instalacion
python -m pytest tests/ -v
```

### Primer uso

```bash
# Ingerir documento de temario
python -m src.temario.cli ingest documents/temario/Tema1.pdf

# Buscar en el temario
python -m src.temario.cli search "constitucion espanola"

# Crear deck de flashcards
python -m src.flashcards.cli create-deck "Tema 1 - Constitucion"

# Generar flashcards automaticamente
python -m src.flashcards.cli generate --tema 1 --count 20

# Repasar flashcards
python -m src.flashcards.cli review "Tema 1 - Constitucion"

# Generar test
python -m src.tests.cli generate --tema 1 --questions 10

# Iniciar dashboard web
python -m src.web.app
```

---

## Modulos Principales

### 1. Temario Ingestion ([docs/03-MODULES/temario-ingestion.md](docs/03-MODULES/temario-ingestion.md))

Sistema de ingestion de documentos con chunking semantico y embeddings.

**Caracteristicas:**
- Soporte para PDF y DOCX
- Chunking inteligente por tokens (~500 tokens)
- Embeddings con Mistral API (1024 dimensiones)
- Busqueda semantica (similitud coseno)
- Busqueda hibrida (semantica + keyword)

### 2. Flashcards SM-2 ([docs/03-MODULES/flashcards-sm2.md](docs/03-MODULES/flashcards-sm2.md))

Sistema de flashcards con algoritmo SuperMemo 2 (SM-2).

**Caracteristicas:**
- Algoritmo SM-2 completo
- Ease factor dinamico (1.3 - 3.0+)
- Intervalos adaptativos
- Generacion automatica desde temario
- Estadisticas de progreso

### 3. Test Generator ([docs/03-MODULES/test-generator.md](docs/03-MODULES/test-generator.md))

Generador de tests automaticos desde el temario.

**Caracteristicas:**
- Preguntas de opcion multiple
- Tests de verdadero/falso
- Preguntas abiertas
- Modos: practica y examen
- Analisis de resultados

### 4. Dashboard Web ([docs/03-MODULES/dashboard-web.md](docs/03-MODULES/dashboard-web.md))

Interfaz web para gestionar el estudio.

**Caracteristicas:**
- Vista de progreso general
- Gestion de decks y flashcards
- Tomar tests interactivos
- Calendario de repaso
- Metricas y estadisticas

### 5. AI Features ([docs/03-MODULES/ai-features.md](docs/03-MODULES/ai-features.md))

Analisis predictivo y recomendaciones personalizadas.

**Caracteristicas:**
- Deteccion de areas debiles
- Prediccion de preparacion
- Planes de estudio semanales
- Recomendaciones diarias
- Metricas de aprendizaje

---

## Enlaces a Documentacion

| Documento | Descripcion |
|-----------|-------------|
| [Contexto](docs/01-CONTEXT.md) | Origen del proyecto y sistemas analizados |
| [Arquitectura](docs/02-ARCHITECTURE.md) | Arquitectura de 5 capas y decisiones de diseno |
| [Modulos](docs/03-MODULES/) | Documentacion detallada de cada modulo |
| [Roadmap](docs/04-ROADMAP.md) | Fases de implementacion y estimaciones |
| [Source Files](docs/05-SOURCE-FILES.md) | Fuentes de referencia y API keys |
| [Folder Structure](docs/06-FOLDER-STRUCTURE.md) | Estructura de carpetas completa |
| [Setup](docs/07-SETUP.md) | Guia de instalacion detallada |
| [API Reference](docs/08-API-REFERENCE.md) | Endpoints y comandos CLI |
| [Testing](docs/09-TESTING.md) | Estrategia de testing |

---

## Estado del Desarrollo

| Fase | Estado | Progreso |
|------|--------|----------|
| Fase 1: Core Modules | En desarrollo | 70% |
| Fase 2: Web Dashboard | Pendiente | 0% |
| Fase 3: AI Analytics | Pendiente | 0% |
| Fase 4: Integracion | Pendiente | 0% |
| Fase 5: Testing & Docs | Pendiente | 0% |
| Fase 6: Voice Mode | Opcional | 0% |

Ver [ROADMAP.md](docs/04-ROADMAP.md) para detalles completos.

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

Este proyecto esta bajo la Licencia MIT. Ver [LICENSE](LICENSE) para detalles.

---

## Contacto

- **GitHub:** [@Ruben-Alvarez-Dev](https://github.com/Ruben-Alvarez-Dev)
- **Proyecto:** https://github.com/Ruben-Alvarez-Dev/oposiciones-system

---

**Ultima actualizacion:** 2026-03-16
**Version:** 0.1.0
