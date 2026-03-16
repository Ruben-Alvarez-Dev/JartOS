# Guia de Instalacion

**Version:** 0.1.0
**Ultima actualizacion:** 2025-03-16

---

## Indice

1. [Requisitos Previos](#1-requisitos-previos)
2. [Instalacion Paso a Paso](#2-instalacion-paso-a-paso)
3. [Configuracion de API Keys](#3-configuracion-de-api-keys)
4. [Verificacion del Entorno](#4-verificacion-del-entorno)
5. [Troubleshooting Comun](#5-troubleshooting-comun)
6. [Docker Setup (Opcional)](#6-docker-setup-opcional)

---

## 1. Requisitos Previos

### 1.1 Sistema Operativo

| Sistema | Soporte | Notas |
|---------|---------|-------|
| macOS 12+ | Completo | Recomendado |
| Ubuntu 20.04+ | Completo | - |
| Windows 10/11 | Completo | Usar WSL2 o PowerShell |
| Fedora 36+ | Completo | - |

### 1.2 Software Requerido

| Software | Version Minima | Version Recomendada | Verificacion |
|----------|----------------|---------------------|--------------|
| **Python** | 3.10 | 3.11+ | `python --version` |
| **pip** | 22.0 | 24.0+ | `pip --version` |
| **Git** | 2.30 | 2.40+ | `git --version` |
| **curl** | Cualquiera | - | `curl --version` |

### 1.3 Software Opcional

| Software | Uso | Instalacion |
|----------|-----|-------------|
| **Docker** | Containerizacion | [docker.com](https://docs.docker.com/get-docker/) |
| **Ollama** | LLM local | [ollama.ai](https://ollama.ai) |
| **make** | Automatizacion | Sistema: `apt install make` / Mac: incluido |

### 1.4 Verificar Requisitos

```bash
# =============================================================================
# VERIFICACION DE REQUISITOS
# =============================================================================

# Verificar Python (>= 3.10)
python --version
# Output esperado: Python 3.10.x o superior

# Verificar pip
pip --version
# Output esperado: pip 22.x o superior

# Verificar Git
git --version
# Output esperado: git version 2.30 o superior

# Verificar espacio en disco (minimo 500MB libre)
df -h .

# Verificar memoria RAM (minimo 4GB recomendado)
# En macOS:
sysctl hw.memsize
# En Linux:
free -h
# En Windows (PowerShell):
(Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize / 1MB
```

### 1.5 Dependencias del Sistema

#### macOS

```bash
# Instalar Homebrew si no esta instalado
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python@3.11

# Instalar Git
brew install git

# Instalar herramientas opcionales
brew install curl wget
```

#### Ubuntu/Debian

```bash
# Actualizar paquetes
sudo apt update && sudo apt upgrade -y

# Instalar Python y pip
sudo apt install -y python3.11 python3.11-venv python3-pip

# Instalar Git
sudo apt install -y git

# Instalar herramientas opcionales
sudo apt install -y curl wget build-essential

# Dependencias para PyMuPDF (PDF parsing)
sudo apt install -y libmupdf-dev mupdf-tools
```

#### Fedora

```bash
# Actualizar sistema
sudo dnf upgrade -y

# Instalar Python
sudo dnf install -y python3.11 python3.11-pip

# Instalar Git
sudo dnf install -y git

# Herramientas opcionales
sudo dnf install -y curl wget gcc
```

#### Windows (WSL2)

```powershell
# Instalar WSL2
wsl --install

# Reiniciar el equipo si es necesario

# Dentro de WSL2 (Ubuntu):
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip git
```

---

## 2. Instalacion Paso a Paso

### 2.1 Clonar el Repositorio

```bash
# =============================================================================
# PASO 1: CLONAR REPOSITORIO
# =============================================================================

# Navegar al directorio de proyectos
cd ~/Projects  # o ~/Documents, o donde prefieras

# Clonar el repositorio
git clone https://github.com/Ruben-Alvarez-Dev/JartOS.git

# Entrar al directorio
cd JartOS

# Verificar contenido
ls -la
```

### 2.2 Crear Virtual Environment

```bash
# =============================================================================
# PASO 2: VIRTUAL ENVIRONMENT
# =============================================================================

# Crear virtual environment
python3 -m venv .venv

# Activar virtual environment
# En macOS/Linux:
source .venv/bin/activate

# En Windows (PowerShell):
# .\.venv\Scripts\Activate.ps1

# En Windows (CMD):
# .\.venv\Scripts\activate.bat

# Verificar activacion (debe mostrar path a .venv)
which python  # macOS/Linux
# where python  # Windows

# Actualizar pip
pip install --upgrade pip setuptools wheel
```

### 2.3 Instalar Dependencias

```bash
# =============================================================================
# PASO 3: INSTALAR DEPENDENCIAS
# =============================================================================

# Instalar dependencias principales
pip install -e .

# Instalar dependencias de desarrollo
pip install -e ".[dev]"

# Verificar instalacion
pip list | grep -E "(typer|rich|fastapi|pydantic|pymupdf)"

# Output esperado:
# typer               0.9.0
# rich               13.7.0
# fastapi            0.109.0
# pydantic            2.5.0
# pymupdf            1.23.0
```

### 2.4 Configurar Variables de Entorno

```bash
# =============================================================================
# PASO 4: CONFIGURAR ENVIRONMENT
# =============================================================================

# Copiar template
cp .env.example .env

# Editar con las API keys
nano .env  # o vim, code, etc.

# Contenido del .env:
# -------------------
# MISTRAL_API_KEY=tu_api_key_aqui
# MINIMAX_API_KEY=tu_api_key_aqui
# MINIMAX_GROUP_ID=tu_group_id_aqui
# TELEGRAM_BOT_TOKEN=tu_token_aqui  # Opcional
# ENVIRONMENT=development
# LOG_LEVEL=INFO
```

### 2.5 Crear Bases de Datos

```bash
# =============================================================================
# PASO 5: CREAR BASES DE DATOS
# =============================================================================

# Crear directorios necesarios
mkdir -p data logs backups documents/temario

# Crear bases de datos (el script las crea con el schema correcto)
python scripts/seed_data.py --init-db

# Verificar creacion
ls -la data/
# Output esperado:
# temario.db
# oposiciones.db
```

### 2.6 Verificar Instalacion

```bash
# =============================================================================
# PASO 6: VERIFICAR INSTALACION
# =============================================================================

# Ejecutar tests (deben pasar)
pytest -v

# Ejecutar CLI de temario
python -m src.temario.cli --help

# Ejecutar CLI de flashcards
python -m src.flashcards.cli --help

# Iniciar servidor web (verificar que inicia)
python scripts/run_web.py &
# Verificar en navegador: http://127.0.0.1:8000
# Detener: Ctrl+C
```

---

## 3. Configuracion de API Keys

### 3.1 Mistral API (Embeddings)

#### Obtener API Key

1. Ir a [https://console.mistral.ai/](https://console.mistral.ai/)
2. Crear cuenta o iniciar sesion
3. Navegar a **API Keys**
4. Crear nueva API key
5. Copiar la key

#### Configurar

```bash
# En .env
MISTRAL_API_KEY=your_mistral_api_key_here
```

#### Verificar

```python
# test_mistral.py
import os
import httpx

api_key = os.getenv("MISTRAL_API_KEY")

response = httpx.post(
    "https://api.mistral.ai/v1/embeddings",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "mistral-embed",
        "input": ["Hola mundo"]
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

```bash
# Ejecutar test
python test_mistral.py
# Output esperado: Status: 200
```

### 3.2 MiniMax API (Generacion de Texto)

#### Obtener API Key y Group ID

1. Ir a [https://www.minimaxi.com/](https://www.minimaxi.com/)
2. Crear cuenta o iniciar sesion
3. Navegar a **API Management**
4. Crear nueva aplicacion
5. Copiar **API Key** y **Group ID**

#### Configurar

```bash
# En .env
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_GROUP_ID=your_minimax_group_id_here
```

#### Verificar

```python
# test_minimax.py
import os
import httpx

api_key = os.getenv("MINIMAX_API_KEY")
group_id = os.getenv("MINIMAX_GROUP_ID")

response = httpx.post(
    f"https://api.minimax.chat/v1/text/chatcompletion?GroupId={group_id}",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "MiniMax-Text-01",
        "messages": [{"role": "user", "content": "Hola"}],
        "temperature": 0.1
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

```bash
# Ejecutar test
python test_minimax.py
# Output esperado: Status: 200
```

### 3.3 Telegram Bot (Opcional)

#### Obtener Bot Token

1. Abrir Telegram
2. Buscar **@BotFather**
3. Enviar `/newbot`
4. Seguir instrucciones
5. Copiar el token

#### Configurar

```bash
# En .env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

#### Verificar

```bash
# Verificar con curl
curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe"

# Output esperado: {"ok":true,"result":{"id":...}}
```

### 3.4 Ollama Local (Fallback Opcional)

#### Instalar Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar modelo
ollama pull llama3
```

#### Configurar

```bash
# En .env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

#### Verificar

```bash
# Verificar que Ollama esta corriendo
ollama list

# Test basico
ollama run llama3 "Hola"
```

---

## 4. Verificacion del Entorno

### 4.1 Checklist de Verificacion

```bash
# =============================================================================
# CHECKLIST DE VERIFICACION
# =============================================================================

echo "=== Verificando Python ==="
python --version
# Esperado: Python 3.10+

echo "=== Verificando Virtual Environment ==="
which python | grep -q ".venv" && echo "OK: venv activo" || echo "ERROR: venv no activo"

echo "=== Verificando Dependencias ==="
python -c "import typer; print('OK: typer')"
python -c "import rich; print('OK: rich')"
python -c "import fastapi; print('OK: fastapi')"
python -c "import pydantic; print('OK: pydantic')"
python -c "import fitz; print('OK: pymupdf')"
python -c "import docx; print('OK: python-docx')"

echo "=== Verificando API Keys ==="
test -n "$MISTRAL_API_KEY" && echo "OK: MISTRAL_API_KEY" || echo "ERROR: MISTRAL_API_KEY"
test -n "$MINIMAX_API_KEY" && echo "OK: MINIMAX_API_KEY" || echo "ERROR: MINIMAX_API_KEY"
test -n "$MINIMAX_GROUP_ID" && echo "OK: MINIMAX_GROUP_ID" || echo "ERROR: MINIMAX_GROUP_ID"

echo "=== Verificando Bases de Datos ==="
test -f data/temario.db && echo "OK: temario.db" || echo "ERROR: temario.db"
test -f data/oposiciones.db && echo "OK: oposiciones.db" || echo "ERROR: oposiciones.db"

echo "=== Verificando Directorios ==="
test -d logs && echo "OK: logs/" || echo "ERROR: logs/"
test -d backups && echo "OK: backups/" || echo "ERROR: backups/"
test -d documents/temario && echo "OK: documents/temario/" || echo "ERROR: documents/temario/"

echo "=== Verificando Configuracion ==="
test -f configs/config.yaml && echo "OK: config.yaml" || echo "ERROR: config.yaml"

echo "=== Ejecutando Tests ==="
pytest --tb=short -q
```

### 4.2 Script de Verificacion Completa

```bash
#!/bin/bash
# =============================================================================
# verify_setup.sh - Verificacion completa del entorno
# =============================================================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

pass=0
fail=0

check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[PASS]${NC} $1"
        ((pass++))
    else
        echo -e "${RED}[FAIL]${NC} $1"
        ((fail++))
    fi
}

echo "========================================"
echo "  VERIFICACION DE ENTORNO"
echo "========================================"
echo ""

# Python
python --version > /dev/null 2>&1
check "Python instalado"

# Virtual environment
echo $VIRTUAL_ENV | grep -q "JartOS"
check "Virtual environment activo"

# Dependencias Python
python -c "import typer" 2>/dev/null
check "typer instalado"

python -c "import rich" 2>/dev/null
check "rich instalado"

python -c "import fastapi" 2>/dev/null
check "fastapi instalado"

python -c "import pydantic" 2>/dev/null
check "pydantic instalado"

python -c "import fitz" 2>/dev/null
check "pymupdf instalado"

python -c "import docx" 2>/dev/null
check "python-docx instalado"

# API Keys (solo verificar que existen, no mostrar contenido)
test -n "$MISTRAL_API_KEY"
check "MISTRAL_API_KEY configurada"

test -n "$MINIMAX_API_KEY"
check "MINIMAX_API_KEY configurada"

test -n "$MINIMAX_GROUP_ID"
check "MINIMAX_GROUP_ID configurado"

# Archivos y directorios
test -f data/temario.db
check "Base de datos temario.db"

test -f data/oposiciones.db
check "Base de datos oposiciones.db"

test -f configs/config.yaml
check "Archivo config.yaml"

test -d logs
check "Directorio logs/"

test -d backups
check "Directorio backups/"

# Tests
pytest --tb=no -q > /dev/null 2>&1
check "Tests pasan"

echo ""
echo "========================================"
echo "  RESULTADO"
echo "========================================"
echo -e "Pasaron: ${GREEN}$pass${NC}"
echo -e "Fallaron: ${RED}$fail${NC}"

if [ $fail -eq 0 ]; then
    echo -e "${GREEN}Entorno configurado correctamente!${NC}"
    exit 0
else
    echo -e "${RED}Hay errores en la configuracion.${NC}"
    exit 1
fi
```

---

## 5. Troubleshooting Comun

### 5.1 Error: Python version incompatibility

```
Error: Python 3.9 detected, but 3.10+ required
```

**Solucion:**

```bash
# Instalar Python 3.11
# macOS:
brew install python@3.11

# Ubuntu:
sudo apt install python3.11 python3.11-venv

# Crear venv con Python especifico
python3.11 -m venv .venv
source .venv/bin/activate
```

### 5.2 Error: pip install fails

```
Error: Failed building wheel for pymupdf
```

**Solucion:**

```bash
# Instalar dependencias del sistema

# Ubuntu/Debian:
sudo apt install -y libmupdf-dev mupdf-tools

# Fedora:
sudo dnf install -y mupdf-devel

# macOS:
brew install mupdf

# Reinstalar
pip install pymupdf --no-cache-dir
```

### 5.3 Error: SQLite database locked

```
sqlite3.OperationalError: database is locked
```

**Solucion:**

```bash
# Verificar que no hay otros procesos usando la DB
lsof data/temario.db

# Cerrar conexiones pendientes
# Reiniciar la aplicacion

# Si persiste, restaurar backup
cp backups/temario_YYYYMMDD.db.bak data/temario.db
```

### 5.4 Error: API key invalid

```
Error: 401 Unauthorized - Invalid API key
```

**Solucion:**

```bash
# Verificar que la API key esta configurada
echo $MISTRAL_API_KEY

# Verificar formato en .env (sin espacios, sin comillas)
# CORRECTO:
MISTRAL_API_KEY=abc123xyz
# INCORRECTO:
MISTRAL_API_KEY="abc123xyz"
MISTRAL_API_KEY = abc123xyz

# Regenerar API key si es necesario
# Ir a la consola del proveedor y crear nueva key
```

### 5.5 Error: Port already in use

```
Error: [Errno 48] Address already in use (127.0.0.1:8000)
```

**Solucion:**

```bash
# Encontrar proceso usando el puerto
lsof -i :8000

# Matar proceso
kill -9 <PID>

# O usar otro puerto
python scripts/run_web.py --port 8001
```

### 5.6 Error: Module not found

```
ModuleNotFoundError: No module named 'src.temario'
```

**Solucion:**

```bash
# Verificar que el venv esta activo
which python

# Verificar instalacion
pip install -e .

# Verificar estructura
ls -la src/temario/

# Agregar path si es necesario
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 5.7 Error: Permission denied

```
PermissionError: [Errno 13] Permission denied: 'data/temario.db'
```

**Solucion:**

```bash
# Verificar permisos
ls -la data/

# Corregir permisos
chmod 644 data/*.db
chmod 755 data/

# Si el directorio es del root (mal)
sudo chown -R $USER:$USER data/
```

### 5.8 Error: Tests failing

```
FAILED tests/temario/test_embedder.py - ConnectionError
```

**Solucion:**

```bash
# Verificar conectividad a API
curl https://api.mistral.ai/v1/models

# Verificar API key
python -c "import os; print('SET' if os.getenv('MISTRAL_API_KEY') else 'NOT SET')"

# Ejecutar tests sin los de API (mock)
pytest -v -m "not integration"
```

---

## 6. Docker Setup (Opcional)

### 6.1 Dockerfile

```dockerfile
# =============================================================================
# Dockerfile - JartOS
# =============================================================================

FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libmupdf-dev \
    mupdf-tools \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY pyproject.toml .

# Instalar dependencias Python
RUN pip install --no-cache-dir -e .

# Copiar codigo fuente
COPY src/ ./src/
COPY configs/ ./configs/
COPY scripts/ ./scripts/

# Crear directorios necesarios
RUN mkdir -p data logs backups documents/temario

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Puerto expuesto
EXPOSE 8000

# Comando por defecto
CMD ["python", "scripts/run_web.py"]
```

### 6.2 docker-compose.yml

```yaml
# =============================================================================
# docker-compose.yml - JartOS
# =============================================================================

version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./backups:/app/backups
      - ./documents:/app/documents
    environment:
      - MISTRAL_API_KEY=${MISTRAL_API_KEY}
      - MINIMAX_API_KEY=${MINIMAX_API_KEY}
      - MINIMAX_GROUP_ID=${MINIMAX_GROUP_ID}
      - ENVIRONMENT=production
    restart: unless-stopped
```

### 6.3 Comandos Docker

```bash
# =============================================================================
# COMANDOS DOCKER
# =============================================================================

# Construir imagen
docker build -t JartOS .

# Iniciar con docker-compose
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Ejecutar comando en contenedor
docker-compose exec web python -m src.temario.cli --help

# Backup de base de datos
docker-compose exec web python scripts/backup_db.py
```

---

## 7. Proximos Pasos

Despues de completar la instalacion:

1. **Ingerir primer documento:**
   ```bash
   python -m src.temario.cli ingest documents/temario/Tema1.pdf --tema 1
   ```

2. **Crear primer deck de flashcards:**
   ```bash
   python -m src.flashcards.cli create-deck "Tema 1 - Constitucion"
   python -m src.flashcards.cli generate --deck 1 --tema 1 --count 20
   ```

3. **Iniciar dashboard web:**
   ```bash
   python scripts/run_web.py
   # Abrir: http://127.0.0.1:8000
   ```

4. **Revisar documentacion:**
   - `docs/04-ROADMAP.md` - Plan de desarrollo
   - `docs/08-API-REFERENCE.md` - Referencia de comandos

---

**Fin del documento de Instalacion**
