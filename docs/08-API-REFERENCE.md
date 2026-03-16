# Referencia de APIs

**Version:** 0.1.0
**Ultima actualizacion:** 2026-03-16

---

## Indice

1. [CLI Commands](#1-cli-commands)
2. [Web Dashboard Endpoints](#2-web-dashboard-endpoints)
3. [Integracion Telegram Bot](#3-integracion-telegram-bot)
4. [Formato de Respuestas](#4-formato-de-respuestas)
5. [Codigos de Error](#5-codigos-de-error)

---

## 1. CLI Commands

### 1.1 Modulo Temario

#### temario ingest

Ingresa un documento PDF o DOCX al sistema.

```bash
python -m src.temario.cli ingest <filepath> [OPTIONS]
```

**Argumentos:**

| Argumento | Tipo | Requerido | Descripcion |
|-----------|------|-----------|-------------|
| filepath | str | Si | Ruta al archivo PDF o DOCX |

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--tema, -t` | int | None | Numero de tema |
| `--title` | str | None | Titulo personalizado |
| `--no-embed` | bool | False | Saltar generacion de embeddings |
| `--verbose, -v` | bool | False | Mostrar progreso detallado |

**Ejemplos:**

```bash
# Ingerir PDF basico
python -m src.temario.cli ingest documents/Tema1.pdf

# Ingerir con metadata
python -m src.temario.cli ingest documents/Tema1.pdf --tema 1 --title "La Constitucion"

# Modo verbose
python -m src.temario.cli ingest documents/Tema1.pdf -v

# Sin embeddings (mas rapido)
python -m src.temario.cli ingest documents/Tema1.pdf --no-embed
```

**Output:**

```
Ingresando documento: Tema1.pdf
+-- Extrayendo texto... OK (45 paginas)
+-- Creando chunks... OK (87 chunks)
+-- Generando embeddings... OK (batch 1/2)
+-- Generando embeddings... OK (batch 2/2)
+-- Guardando en DB... OK

Resumen:
  Documento ID: 1
  Titulo: Tema1.pdf
  Paginas: 45
  Chunks: 87
  Tiempo: 12.5s
```

---

#### temario search

Busca en el temario por similitud semantica.

```bash
python -m src.temario.cli search <query> [OPTIONS]
```

**Argumentos:**

| Argumento | Tipo | Requerido | Descripcion |
|-----------|------|-----------|-------------|
| query | str | Si | Consulta de busqueda |

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--tema, -t` | int | None | Filtrar por numero de tema |
| `--limit, -l` | int | 5 | Maximo de resultados |
| `--threshold` | float | 0.7 | Umbral de similitud minima |
| `--json` | bool | False | Output en formato JSON |

**Ejemplos:**

```bash
# Busqueda basica
python -m src.temario.cli search "constitucion espanola"

# Con filtro de tema
python -m src.temario.cli search "derechos fundamentales" --tema 1

# Mas resultados
python -m src.temario.cli search "gobierno" --limit 10

# Output JSON
python -m src.temario.cli search "constitucion" --json
```

**Output:**

```
Buscando: "constitucion espanola"
Encontrados: 3 resultados

[1] Score: 0.89 | Tema 1, Pag 5
    La Constitucion Espanola de 1978 es la norma suprema del ordenamiento
    juridico espanol...

[2] Score: 0.85 | Tema 1, Pag 12
    Los principios constitucionales fundamentales establecen...

[3] Score: 0.82 | Tema 1, Pag 8
    La Constitucion establece los derechos y libertades...
```

---

#### temario ask

Hace una pregunta al temario y obtiene respuesta con IA.

```bash
python -m src.temario.cli ask <question> [OPTIONS]
```

**Argumentos:**

| Argumento | Tipo | Requerido | Descripcion |
|-----------|------|-----------|-------------|
| question | str | Si | Pregunta en lenguaje natural |

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--tema, -t` | int | None | Filtrar por tema |
| `--context, -c` | int | 3 | Chunks de contexto |

**Ejemplos:**

```bash
# Pregunta basica
python -m src.temario.cli ask "Cuales son los derechos fundamentales?"

# Con filtro de tema
python -m src.temario.cli ask "Que es el Senado?" --tema 2

# Mas contexto
python -m src.temario.cli ask "Como se elaboran las leyes?" --context 5
```

**Output:**

```
Pregunta: Cuales son los derechos fundamentales?

Respuesta:
Los derechos fundamentales reconocidos en la Constitucion
Espanola incluyen:

1. Derecho a la vida e integridad fisica
2. Libertad ideologica y religiosa
3. Libertad de expression
4. Derecho a la educacion
5. Derecho al trabajo
...

Fuentes:
  [1] Tema 1, Pag 15 (relevancia: 0.89)
  [2] Tema 1, Pag 18 (relevancia: 0.85)
  [3] Tema 1, Pag 22 (relevancia: 0.82)
```

---

#### temario list

Lista documentos ingresados.

```bash
python -m src.temario.cli list [OPTIONS]
```

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--tema, -t` | int | None | Filtrar por tema |
| `--format, -f` | str | table | Formato: table, json |

**Ejemplos:**

```bash
# Listar todos
python -m src.temario.cli list

# Filtrar por tema
python -m src.temario.cli list --tema 1

# Formato JSON
python -m src.temario.cli list --format json
```

**Output:**

```
Documentos ingresados:

ID  | Titulo                    | Tema | Paginas | Chunks | Fecha
----|---------------------------|------|---------|--------|------------
1   | La Constitucion           | 1    | 45      | 87     | 2026-03-16
2   | La Corona                 | 2    | 32      | 65     | 2026-03-16
3   | Las Cortes Generales      | 3    | 58      | 112    | 2026-03-16

Total: 3 documentos, 264 chunks
```

---

#### temario delete

Elimina un documento y todos sus chunks.

```bash
python -m src.temario.cli delete <document_id>
```

**Argumentos:**

| Argumento | Tipo | Requerido | Descripcion |
|-----------|------|-----------|-------------|
| document_id | int | Si | ID del documento a eliminar |

**Ejemplo:**

```bash
python -m src.temario.cli delete 1
```

**Output:**

```
Eliminando documento ID: 1
+-- Eliminando chunks... OK (87 eliminados)
+-- Eliminando documento... OK

Total eliminado: 87 chunks
```

---

### 1.2 Modulo Flashcards

#### flashcards create-deck

Crea un nuevo deck de flashcards.

```bash
python -m src.flashcards.cli create-deck <name> [OPTIONS]
```

**Argumentos:**

| Argumento | Tipo | Requerido | Descripcion |
|-----------|------|-----------|-------------|
| name | str | Si | Nombre del deck |

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--tema, -t` | int | None | Asociar a tema |
| `--description, -d` | str | None | Descripcion del deck |

**Ejemplos:**

```bash
# Crear deck basico
python -m src.flashcards.cli create-deck "Tema 1"

# Con descripcion
python -m src.flashcards.cli create-deck "Tema 2" --description "La Corona"
```

**Output:**

```
Deck creado:
  ID: 1
  Nombre: Tema 1
  Descripcion: (sin descripcion)
  Cartas: 0
```

---

#### flashcards generate

Genera flashcards automaticamente desde el temario.

```bash
python -m src.flashcards.cli generate [OPTIONS]
```

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--deck, -d` | int | Requerido | ID del deck destino |
| `--tema, -t` | int | None | Generar desde tema especifico |
| `--count, -c` | int | 10 | Numero de flashcards |
| `--chunks` | str | None | IDs de chunks especificos |

**Ejemplos:**

```bash
# Generar desde tema
python -m src.flashcards.cli generate --deck 1 --tema 1 --count 20

# Generar desde chunks especificos
python -m src.flashcards.cli generate --deck 1 --chunks "42,43,44"
```

**Output:**

```
Generando flashcards para deck 1...
+-- Buscando chunks del tema 1... OK (112 encontrados)
+-- Seleccionando chunks relevantes... OK (15 seleccionados)
+-- Generando flashcards con IA... OK (20 generadas)
+-- Guardando en DB... OK

Resumen:
  Deck: 1
  Flashcards generadas: 20
  Tiempo: 45.2s
```

---

#### flashcards review

Inicia sesion de repaso de flashcards.

```bash
python -m src.flashcards.cli review [OPTIONS]
```

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--deck, -d` | int | None | Deck especifico (todos si no se indica) |
| `--limit, -l` | int | 20 | Maximo de tarjetas |
| `--due-only` | bool | True | Solo tarjetas vencidas |

**Ejemplos:**

```bash
# Repasar deck especifico
python -m src.flashcards.cli review --deck 1

# Repasar todas las vencidas
python -m src.flashcards.cli review

# Repasar con limite
python -m src.flashcards.cli review --deck 1 --limit 10

# Repasar todas (incluyendo futuras)
python -m src.flashcards.cli review --deck 1 --due-only false
```

**Output (interactivo):**

```
Sesion de repaso - Deck 1
Tarjetas pendientes: 15

================================================================================
[1/15] Facilidad: 2.5 | Proximo: hace 2 dias
--------------------------------------------------------------------------------
PREGUNTA:
Cual es el articulo 1 de la Constitucion Espanola?

[Presiona Enter para ver respuesta]
--------------------------------------------------------------------------------
RESPUESTA:
El articulo 1 establece que Espana se constituye en un Estado social
y democratico de Derecho...

Califica tu respuesta:
  0 - De nuevo (no la sabia)
  1 - Dificil (lo sabia con dificultad)
  2 - Bien (lo sabia pero con dudas)
  3 - Facil (lo sabia perfectamente)
  4 - Muy facil (lo sabia de sobra)

Tu calificacion [0-4]: 3

+-- Actualizando SM-2... Nuevo intervalo: 3 dias

================================================================================
[2/15] ...
```

---

#### flashcards stats

Muestra estadisticas de flashcards.

```bash
python -m src.flashcards.cli stats [OPTIONS]
```

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--deck, -d` | int | None | Deck especifico |

**Ejemplo:**

```bash
python -m src.flashcards.cli stats --deck 1
```

**Output:**

```
Estadisticas del Deck 1: Tema 1

Resumen:
  Total cartas: 87
  Nuevas: 42
  En aprendizaje: 18
  Repasadas: 27

Progreso:
  Facilidad promedio: 2.4
  Intervalo promedio: 4.2 dias
  Retencion estimada: 85%

Vencidas:
  Hoy: 12
  Ayer: 5
  Esta semana: 23

Proximas:
  Manana: 8
  En 3 dias: 15
  En 7 dias: 25
```

---

### 1.3 Modulo Tests

#### tests create

Crea un nuevo test de practica.

```bash
python -m src.tests.cli create [OPTIONS]
```

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--title` | str | "Test {fecha}" | Titulo del test |
| `--tema, -t` | int | None | Generar desde tema |
| `--questions, -q` | int | 10 | Numero de preguntas |
| `--type` | str | mixed | Tipo: multiple, true_false, open, mixed |

**Ejemplos:**

```bash
# Test basico
python -m src.tests.cli create --tema 1 --questions 10

# Test solo multiple choice
python -m src.tests.cli create --tema 1 --questions 20 --type multiple

# Test con titulo personalizado
python -m src.tests.cli create --title "Examen Final" --tema 3 --questions 30
```

**Output:**

```
Creando test...
+-- Buscando chunks del tema 1... OK (87 encontrados)
+-- Generando preguntas con IA... OK (10 generadas)
+-- Guardando test... OK

Test creado:
  ID: 1
  Titulo: Test 2026-03-16
  Preguntas: 10
    - Multiple choice: 5
    - Verdadero/Falso: 3
    - Abiertas: 2

Para tomar el test:
  python -m src.tests.cli take --test 1
```

---

#### tests take

Toma un test.

```bash
python -m src.tests.cli take [OPTIONS]
```

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--test, -t` | int | Requerido | ID del test |
| `--timed` | bool | False | Con tiempo limite |

**Ejemplos:**

```bash
# Tomar test
python -m src.tests.cli take --test 1

# Con tiempo
python -m src.tests.cli take --test 1 --timed
```

**Output (interactivo):**

```
================================================================================
TEST: Test 2026-03-16
Preguntas: 10 | Tiempo: ilimitado
================================================================================

[1/10] MULTIPLE CHOICE
Cual es el articulo 1 de la Constitucion Espanola?

  a) Espana se constituye en una monarquia parlamentaria
  b) Espana se constituye en un Estado social y democratico de Derecho
  c) Espana se constituye en una republica federal
  d) Espana se constituye en una democracia directa

Tu respuesta [a-d]: b

================================================================================
[2/10] VERDADERO/FALSO
La Constitucion fue aprobada en 1978.

Tu respuesta [V/F]: V

================================================================================
[3/10] PREGUNTA ABIERTA
Que establece el articulo 2 de la Constitucion?

Tu respuesta (escribe y presiona Enter dos veces para terminar):
La Constitucion reconoce el derecho a la autonomia de las nacionalidades
y regiones...

================================================================================
...
```

---

#### tests results

Muestra resultados de un test.

```bash
python -m src.tests.cli results [OPTIONS]
```

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--session, -s` | int | Requerido | ID de sesion |
| `--detailed` | bool | False | Mostrar detalle por pregunta |

**Ejemplo:**

```bash
python -m src.tests.cli results --session 1 --detailed
```

**Output:**

```
================================================================================
RESULTADOS: Test 2026-03-16
Sesion: 1 | Fecha: 2026-03-16 15:30
================================================================================

PUNTUACION GENERAL
  Correctas: 7/10 (70%)
  Tiempo: 12:45

POR TIPO:
  Multiple choice: 4/5 (80%)
  Verdadero/Falso: 2/3 (67%)
  Abiertas: 1/2 (50%) - Evaluacion automatica

AREAS DEBILES DETECTADAS:
  +-- Tema 1, Apartado 2.3 (Score: 40%)
  +-- Tema 1, Apartado 4.1 (Score: 50%)

================================================================================
DETALLE POR PREGUNTA
================================================================================

[1] MULTIPLE CHOICE | CORRECTA
    P: Cual es el articulo 1...?
    Tu respuesta: b) Espana se constituye...
    Correcta: b)

[2] VERDADERO/FALSO | INCORRECTA
    P: La Constitucion fue aprobada en 1978.
    Tu respuesta: Falso
    Correcta: Verdadero
    Explicacion: La Constitucion fue aprobada por las Cortes
    el 31 de octubre de 1978...

...
```

---

### 1.4 Modulo AI

#### ai analyze

Analiza areas debiles basandose en flashcards y tests.

```bash
python -m src.ai.cli analyze [OPTIONS]
```

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--threshold` | float | 0.6 | Umbral para considerar debil |
| `--export` | str | None | Exportar a archivo (json, csv) |

**Ejemplo:**

```bash
python -m src.ai.cli analyze
```

**Output:**

```
================================================================================
ANALISIS DE AREAS DEBILES
Fecha: 2026-03-16
================================================================================

AREAS DEBILES DETECTADAS (5):

[1] CRITICA - Tema 2: La Corona
    Score combinado: 35%
    +-- Flashcards: Facilidad promedio 1.8
    +-- Tests: 40% de aciertos
    Cartas afectadas: 12
    Tests afectados: 3
    Recomendacion: Repasar urgentemente

[2] ALTA - Tema 1, Apartado 4: Las Cortes Generales
    Score combinado: 45%
    +-- Flashcards: Facilidad promedio 2.1
    +-- Tests: 50% de aciertos
    Cartas afectadas: 8
    Tests afectados: 2

[3] MEDIA - Tema 3: El Gobierno
    Score combinado: 55%
    ...

SUGERENCIAS:
  1. Priorizar repaso de "La Corona" (12 cartas vencidas)
  2. Crear mas flashcards de "Las Cortes Generales"
  3. Tomar test de practica de "El Gobierno"
```

---

#### ai predict

Predice nivel de preparacion.

```bash
python -m src.ai.cli predict [OPTIONS]
```

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--days` | int | 30 | Dias hasta el examen |
| `--hours` | int | 2 | Horas de estudio diarias |

**Ejemplo:**

```bash
python -m src.ai.cli predict --days 60 --hours 3
```

**Output:**

```
================================================================================
PREDICCION DE PREPARACION
Dias hasta examen: 60 | Horas diarias: 3
================================================================================

NIVEL ACTUAL DE PREPARACION

  General: ████████░░ 78%
  Tema 1:  █████████░ 92%
  Tema 2:  ██████░░░░ 58%
  Tema 3:  ████████░░ 82%
  Tema 4:  █████░░░░░ 48%

PREDICCION A 60 DIAS

  Con ritmo actual (3h/dia):
  +-- General: 92% (+14%)
  +-- Confianza: 85%

  Areas a cubrir:
  +-- Tema 2: Necesita 15 horas adicionales
  +-- Tema 4: Necesita 20 horas adicionales

RECOMENDACION
  Mantener ritmo de 3h/dia
  Enfocarse en Tema 2 y Tema 4
  Prediccion de aprobado: 95%
```

---

#### ai plan

Genera plan de estudio semanal.

```bash
python -m src.ai.cli plan [OPTIONS]
```

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--hours` | int | 14 | Horas semanales |
| `--start` | str | hoy | Fecha inicio (YYYY-MM-DD) |

**Ejemplo:**

```bash
python -m src.ai.cli plan --hours 21 --start 2026-03-17
```

**Output:**

```
================================================================================
PLAN DE ESTUDIO SEMANAL
Semana del 17 al 23 de Marzo | 21 horas semanales
================================================================================

OBJETIVOS DE LA SEMANA
  1. Repasar Tema 2: La Corona (critico)
  2. Completar 50 flashcards vencidas
  3. Tomar 2 tests de practica

DISTRIBUCION DIARIA

  Lunes 17 (3h):
  +-- Flashcards: Repaso Tema 2 (1.5h, 20 cartas)
  +-- Temario: Leer Apartado 2.1-2.3 (1h)
  +-- Test: Rapido de 10 preguntas (0.5h)

  Martes 18 (3h):
  +-- Flashcards: Repaso Tema 2 (1.5h, 20 cartas)
  +-- Temario: Leer Apartado 2.4-2.6 (1h)
  +-- Flashcards: Generar nuevas (0.5h)

  Miercoles 19 (3h):
  +-- Flashcards: Repaso mixto (1.5h)
  +-- Test: Completo de Tema 2 (1.5h)

  Jueves 20 (3h):
  +-- Flashcards: Repaso Tema 1 (1.5h)
  +-- Temario: Repaso general Tema 1 (1.5h)

  Viernes 21 (3h):
  +-- Flashcards: Repaso Tema 3 (1.5h)
  +-- Test: Mixto de Temas 1-3 (1.5h)

  Sabado 22 (3h):
  +-- Flashcards: Repaso vencidas (2h)
  +-- Analisis: Revisar areas debiles (1h)

  Domingo 23 (3h):
  +-- Descanso activo: Repaso ligero (1h)
  +-- Preparacion: Plan siguiente semana (0.5h)
  +-- Libre (1.5h)

AREAS DE ENFOQUE
  [CRITICO] Tema 2: La Corona
  [ALTO] Tema 4: El Poder Judicial
```

---

#### ai recommend

Genera recomendaciones diarias.

```bash
python -m src.ai.cli recommend [OPTIONS]
```

**Opciones:**

| Opcion | Tipo | Default | Descripcion |
|--------|------|---------|-------------|
| `--limit, -l` | int | 5 | Maximo de recomendaciones |
| `--execute` | bool | False | Ejecutar primera recomendacion |

**Ejemplo:**

```bash
python -m src.ai.cli recommend
```

**Output:**

```
================================================================================
RECOMENDACIONES PARA HOY - 16 de Marzo
================================================================================

[1] CRITICA - 15 min
    Repasar 12 flashcards vencidas de "La Corona"
    Razon: Tienes cartas vencidas desde hace 3 dias
    Accion: flashcards review --deck 2

[2] ALTA - 30 min
    Completar test de practica de Tema 2
    Razon: Bajo rendimiento en tests recientes (40%)
    Accion: tests create --tema 2 --questions 10

[3] MEDIA - 20 min
    Generar nuevas flashcards de Tema 4
    Razon: Solo tienes 5 cartas de este tema
    Accion: flashcards generate --deck 4 --tema 4

[4] BAJA - 10 min
    Repasar pregunta abierta fallada
    Razon: Error en test anterior
    Accion: temario ask "Que es el Consejo General del Poder Judicial?"

[5] INFO - 5 min
    Verificar progreso semanal
    Razon: Llevas 8h de 14h planificadas
    Accion: ai stats

================================================================================
Tiempo total estimado: 80 minutos
Prioridad sugerida: 1 -> 2 -> 3
================================================================================
```

---

## 2. Web Dashboard Endpoints

### 2.1 Autenticacion

**Nota:** El sistema actual es single-user sin autenticacion. Para produccion, considerar anadir autenticacion.

### 2.2 Dashboard

#### GET /

Dashboard principal con metricas agregadas.

**Response:**

```json
{
  "stats": {
    "total_flashcards": 150,
    "due_today": 25,
    "tests_completed": 12,
    "average_score": 78
  },
  "weak_areas": [
    {"tema": "La Corona", "score": 35},
    {"tema": "Poder Judicial", "score": 48}
  ],
  "today_recommendations": [...],
  "recent_activity": [...]
}
```

#### GET /api/dashboard/stats

Estadisticas generales del sistema.

**Response:**

```json
{
  "temario": {
    "documents": 5,
    "total_chunks": 450,
    "total_pages": 250
  },
  "flashcards": {
    "total": 150,
    "new": 42,
    "learning": 38,
    "review": 70,
    "due_today": 25
  },
  "tests": {
    "total": 15,
    "completed": 12,
    "average_score": 78.5
  },
  "study_time": {
    "today_minutes": 45,
    "week_minutes": 320,
    "streak_days": 7
  }
}
```

### 2.3 Temario

#### GET /api/temario/documents

Lista documentos ingresados.

**Query Parameters:**

| Parametro | Tipo | Requerido | Descripcion |
|-----------|------|-----------|-------------|
| tema | int | No | Filtrar por tema |
| limit | int | No | Maximo resultados (default: 50) |
| offset | int | No | Offset para paginacion |

**Response:**

```json
{
  "total": 5,
  "documents": [
    {
      "id": 1,
      "filename": "Tema1.pdf",
      "title": "La Constitucion",
      "tema": 1,
      "total_pages": 45,
      "total_chunks": 87,
      "created_at": "2026-03-16T10:30:00"
    }
  ]
}
```

#### POST /api/temario/ingest

Ingresa un nuevo documento.

**Request:** `multipart/form-data`

| Campo | Tipo | Requerido | Descripcion |
|-------|------|-----------|-------------|
| file | file | Si | Archivo PDF o DOCX |
| tema | int | No | Numero de tema |
| title | str | No | Titulo personalizado |

**Response (201):**

```json
{
  "success": true,
  "document": {
    "id": 1,
    "filename": "Tema1.pdf",
    "total_chunks": 87
  },
  "duration_seconds": 12.5
}
```

#### POST /api/temario/search

Busqueda semantica.

**Request:**

```json
{
  "query": "constitucion espanola",
  "tema": 1,
  "limit": 5,
  "threshold": 0.7
}
```

**Response:**

```json
{
  "query": "constitucion espanola",
  "total_results": 3,
  "results": [
    {
      "chunk": {
        "id": 42,
        "content": "La Constitucion Espanola...",
        "tema": 1,
        "page_number": 5
      },
      "score": 0.89
    }
  ]
}
```

#### POST /api/temario/qa

Pregunta al temario.

**Request:**

```json
{
  "question": "Cuales son los derechos fundamentales?",
  "tema": 1,
  "context_limit": 3
}
```

**Response:**

```json
{
  "question": "Cuales son los derechos fundamentales?",
  "answer": "Los derechos fundamentales incluyen...",
  "sources": [
    {
      "chunk_id": 42,
      "document": "Tema1.pdf",
      "page": 15,
      "relevance": 0.89
    }
  ],
  "confidence": 0.85
}
```

#### DELETE /api/temario/documents/{id}

Elimina un documento.

**Response:**

```json
{
  "success": true,
  "deleted_chunks": 87
}
```

### 2.4 Flashcards

#### GET /api/flashcards/decks

Lista decks de flashcards.

**Response:**

```json
{
  "total": 3,
  "decks": [
    {
      "id": 1,
      "name": "Tema 1 - Constitucion",
      "card_count": 50,
      "due_count": 12,
      "created_at": "2026-03-16T10:00:00"
    }
  ]
}
```

#### POST /api/flashcards/decks

Crea un nuevo deck.

**Request:**

```json
{
  "name": "Tema 1 - Constitucion",
  "description": "Flashcards del Tema 1",
  "tema_id": 1
}
```

**Response (201):**

```json
{
  "id": 1,
  "name": "Tema 1 - Constitucion",
  "card_count": 0
}
```

#### GET /api/flashcards/decks/{id}/cards

Lista flashcards de un deck.

**Query Parameters:**

| Parametro | Tipo | Default | Descripcion |
|-----------|------|---------|-------------|
| due_only | bool | false | Solo vencidas |
| limit | int | 50 | Maximo resultados |

**Response:**

```json
{
  "total": 50,
  "cards": [
    {
      "id": 1,
      "front": "Cual es el articulo 1?",
      "back": "Espana se constituye...",
      "ease_factor": 2.5,
      "interval": 3,
      "next_review": "2026-03-19"
    }
  ]
}
```

#### POST /api/flashcards/decks/{id}/generate

Genera flashcards automaticamente.

**Request:**

```json
{
  "tema_id": 1,
  "count": 20
}
```

**Response (202):**

```json
{
  "status": "processing",
  "job_id": "abc123",
  "estimated_time": 45
}
```

#### POST /api/flashcards/review

Registra resultado de repaso.

**Request:**

```json
{
  "flashcard_id": 1,
  "rating": 3
}
```

**Response:**

```json
{
  "flashcard_id": 1,
  "new_interval": 6,
  "new_ease_factor": 2.6,
  "next_review": "2026-03-22"
}
```

### 2.5 Tests

#### GET /api/tests

Lista tests disponibles.

**Response:**

```json
{
  "total": 5,
  "tests": [
    {
      "id": 1,
      "title": "Test Tema 1",
      "question_count": 10,
      "completed": true,
      "best_score": 80,
      "created_at": "2026-03-16T10:00:00"
    }
  ]
}
```

#### POST /api/tests

Crea un nuevo test.

**Request:**

```json
{
  "title": "Test Tema 1",
  "tema_id": 1,
  "question_count": 10,
  "question_types": ["multiple_choice", "true_false"]
}
```

**Response (201):**

```json
{
  "id": 1,
  "title": "Test Tema 1",
  "questions": [
    {
      "id": 1,
      "type": "multiple_choice",
      "text": "Cual es el articulo 1?",
      "options": ["a", "b", "c", "d"]
    }
  ]
}
```

#### POST /api/tests/{id}/sessions

Inicia sesion de test.

**Response (201):**

```json
{
  "session_id": 1,
  "test_id": 1,
  "questions": [...],
  "started_at": "2026-03-16T15:00:00"
}
```

#### POST /api/tests/sessions/{id}/answer

Registra respuesta.

**Request:**

```json
{
  "question_id": 1,
  "answer": "b"
}
```

**Response:**

```json
{
  "correct": true,
  "explanation": "El articulo 1 establece..."
}
```

#### POST /api/tests/sessions/{id}/complete

Completa la sesion de test.

**Response:**

```json
{
  "session_id": 1,
  "score": 80,
  "correct": 8,
  "total": 10,
  "duration_seconds": 765,
  "weak_areas": [
    {"tema": "La Corona", "score": 40}
  ]
}
```

---

## 3. Integracion Telegram Bot

### 3.1 Comandos del Bot

| Comando | Descripcion |
|---------|-------------|
| `/start` | Inicia el bot y muestra ayuda |
| `/help` | Muestra lista de comandos |
| `/review [deck]` | Inicia sesion de repaso |
| `/due` | Muestra flashcards vencidas |
| `/stats` | Muestra estadisticas |
| `/test [tema]` | Genera test rapido |
| `/ask <pregunta>` | Pregunta al temario |
| `/recommend` | Muestra recomendaciones del dia |
| `/plan` | Muestra plan semanal |

### 3.2 Flujo de Repaso por Telegram

```
Usuario: /review 1

Bot: Repasando Deck 1: Tema 1
     [1/5] Facilidad: 2.5

     PREGUNTA:
     Cual es el articulo 1 de la Constitucion?

     [Ver respuesta]

Usuario: [Ver respuesta]

Bot: RESPUESTA:
     El articulo 1 establece que Espana se constituye
     en un Estado social y democratico de Derecho...

     Califica:
     [0] De nuevo  [1] Dificil  [2] Bien  [3] Facil

Usuario: [2] Bien

Bot: Actualizado! Nuevo intervalo: 3 dias
     Proxima tarjeta en 5 segundos...
```

### 3.3 Flujo de QA por Telegram

```
Usuario: /ask Cual es el articulo 1?

Bot: Buscando respuesta...

     RESPUESTA:
     El articulo 1 de la Constitucion Espanola establece
     que Espana se constituye en un Estado social y
     democratico de Derecho...

     Fuentes:
     - Tema 1, Pag 5
```

---

## 4. Formato de Respuestas

### 4.1 Estructura Base de Respuesta

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2026-03-16T15:30:00Z",
    "request_id": "abc123"
  }
}
```

### 4.2 Respuesta de Error

```json
{
  "success": false,
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "El documento con ID 999 no existe",
    "details": {
      "document_id": 999
    }
  },
  "meta": {
    "timestamp": "2026-03-16T15:30:00Z",
    "request_id": "abc123"
  }
}
```

### 4.3 Respuesta Paginada

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "total": 100,
    "limit": 20,
    "offset": 0,
    "has_more": true
  }
}
```

---

## 5. Codigos de Error

### 5.1 Codigos HTTP

| Codigo | Descripcion |
|--------|-------------|
| 200 | OK |
| 201 | Created |
| 202 | Accepted (procesando) |
| 400 | Bad Request |
| 404 | Not Found |
| 409 | Conflict (duplicado) |
| 422 | Unprocessable Entity (validacion) |
| 429 | Too Many Requests (rate limit) |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

### 5.2 Codigos de Error Personalizados

| Codigo | Descripcion |
|--------|-------------|
| `DOCUMENT_NOT_FOUND` | Documento no existe |
| `INVALID_FILE_TYPE` | Tipo de archivo no soportado |
| `API_KEY_INVALID` | API key invalida |
| `RATE_LIMIT_EXCEEDED` | Limite de peticiones excedido |
| `EMBEDDING_FAILED` | Error generando embeddings |
| `LLM_ERROR` | Error en LLM |
| `DATABASE_ERROR` | Error de base de datos |
| `VALIDATION_ERROR` | Error de validacion |

### 5.3 Ejemplo de Manejo de Errores

```python
import httpx

async def search_temario(query: str):
    response = httpx.post(
        "http://localhost:8000/api/temario/search",
        json={"query": query}
    )

    if response.status_code == 200:
        return response.json()["data"]

    error = response.json().get("error", {})

    if response.status_code == 429:
        # Rate limit - esperar y reintentar
        retry_after = response.headers.get("Retry-After", 60)
        await asyncio.sleep(int(retry_after))
        return await search_temario(query)

    if error.get("code") == "API_KEY_INVALID":
        raise ValueError("API key invalida - verificar configuracion")

    raise Exception(f"Error: {error.get('message')}")
```

---

**Fin del documento de Referencia de APIs**
