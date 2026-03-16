# Modulo: Flashcards SM-2

**Version:** 0.1.0
**Ultima actualizacion:** 2026-03-16

---

## Indice

1. [Descripcion](#1-descripcion)
2. [Algoritmo SM-2](#2-algoritmo-sm-2)
3. [User Stories](#3-user-stories)
4. [Requirements (RFC 2119)](#4-requirements-rfc-2119)
5. [API Spec](#5-api-spec)
6. [CLI Spec](#6-cli-spec)
7. [Data Models](#7-data-models)
8. [Diagramas de Flujo](#8-diagramas-de-flujo)

---

## 1. Descripcion

El modulo de **Flashcards SM-2** implementa un sistema de repaso espaciado basado en el algoritmo SuperMemo 2 (SM-2), permitiendo la creacion, gestion y repaso de flashcards con intervalos optimizados para la retencion a largo plazo.

### Funcionalidades Principales

- Creacion y gestion de decks de flashcards
- Algoritmo SM-2 completo para repaso espaciado
- Generacion automatica de flashcards desde temario
- Sesiones de repaso interactivas
- Estadisticas y metricas de progreso
- Sincronizacion de facilidad (ease factor)

### Componentes

```
src/flashcards/
+-- __init__.py      # Exporta componentes principales
+-- models.py        # Data models (Deck, Flashcard, ReviewLog)
+-- store.py         # SQLite database operations
+-- scheduler.py     # SM-2 algorithm implementation
+-- generator.py     # AI-powered flashcard generation
+-- reviewer.py      # Review session management
+-- cli.py           # CLI commands
```

---

## 2. Algoritmo SM-2

### Descripcion General

SM-2 (SuperMemo 2) es un algoritmo de repeticion espaciada desarrollado por Piotr Wozniak en 1987. El algoritmo programa el repaso de cada tarjeta basandose en:

1. **Ease Factor (EF)** - Factor de facilidad (1.3 - 3.0+)
2. **Interval** - Dias hasta el siguiente repaso
3. **Repetitions** - Numero de repasos exitosos consecutivos
4. **Quality (q)** - Calidad de la respuesta (0-5)

### Escala de Calidad (0-5)

| Rating | Nombre | Descripcion |
|--------|--------|-------------|
| 0 | Again | Fallo completo, no recordaba nada |
| 1 | Hard | Incorrecto, pero reconocia la respuesta |
| 2 | Hard2 | Incorrecto, pero facil de recordar |
| 3 | Good | Correcto con dificultad |
| 4 | Easy | Correcto con pequena hesitation |
| 5 | Very Easy | Respuesta perfecta, inmediata |

### Formulas SM-2

#### Si q < 3 (fallo):

```
interval = 1
repetitions = 0
EF = max(1.3, EF - 0.2)  # Reduce ease factor
```

#### Si q >= 3 (exito):

```
if repetitions == 0:
    interval = 1
elif repetitions == 1:
    interval = 6
else:
    interval = interval * EF  # Multiplica por ease factor

repetitions += 1
EF = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
EF = max(1.3, EF)  # Minimo 1.3
```

### Ejemplo de Intervalos

| Repeticion | q=3 (Good) | q=4 (Easy) | q=5 (Very Easy) |
|------------|------------|------------|-----------------|
| 1 | 1 dia | 1 dia | 1 dia |
| 2 | 6 dias | 6 dias | 6 dias |
| 3 | 15 dias | 18 dias | 21 dias |
| 4 | 37 dias | 54 dias | 73 dias |
| 5 | 92 dias | 162 dias | 255 dias |

---

## 3. User Stories

### US-FC-001: Crear deck de flashcards

**Como** opositor
**Quiero** crear un deck de flashcards para un tema
**Para** organizar mis tarjetas de estudio

**Criterios de Aceptacion:**
- GIVEN un nombre para el deck
- WHEN ejecuto el comando de creacion
- THEN el sistema crea el deck
- AND asigna un ID unico
- AND lo muestra en la lista de decks

---

### US-FC-002: Generar flashcards automaticamente

**Como** opositor
**Quiero** generar flashcards automaticamente desde el temario
**Para** ahorrar tiempo en creacion manual

**Criterios de Aceptacion:**
- GIVEN un tema con chunks en el temario
- WHEN ejecuto el comando de generacion
- THEN el sistema selecciona chunks relevantes
- AND genera p pregunta-respuesta con IA
- AND crea las flashcards en el deck
- AND muestra resumen de lo generado

---

### US-FC-003: Repasar flashcards

**Como** opositor
**Quiero** repasar las flashcards que estan vencidas
**Para** reforzar mi conocimiento

**Criterios de Aceptacion:**
- GIVEN flashcards con next_review <= hoy
- WHEN inicio sesion de repaso
- THEN el sistema muestra cada flashcard
- AND permite calificar la respuesta (0-5)
- AND actualiza intervalo segun SM-2
- AND muestra estadisticas al final

---

### US-FC-004: Ver estadisticas de deck

**Como** opositor
**Quiero** ver estadisticas de un deck
**Para** conocer mi progreso

**Criterios de Aceptacion:**
- GIVEN un deck con flashcards
- WHEN solicito estadisticas
- THEN el sistema muestra:
  - Total de tarjetas
  - Nuevas vs aprendidas
  - Tarjetas debidas hoy
  - Ease factor promedio
  - Total de repasos

---

### US-FC-005: Editar flashcard

**Como** opositor
**Quiero** editar una flashcard existente
**Para** corregir o mejorar su contenido

**Criterios de Aceptacion:**
- GIVEN una flashcard existente
- WHEN solicito editar
- THEN el sistema permite modificar:
  - Frente (pregunta)
  - Reverso (respuesta)
- AND mantiene parametros SM-2

---

## 4. Requirements (RFC 2119)

### Requerimientos Funcionales

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| FR-FC-001 | El sistema MUST permitir crear decks | Alta |
| FR-FC-002 | El sistema MUST permitir crear flashcards manuales | Alta |
| FR-FC-003 | El sistema SHALL generar flashcards desde temario con IA | Alta |
| FR-FC-004 | El sistema MUST implementar algoritmo SM-2 completo | Alta |
| FR-FC-005 | El sistema SHALL calcular intervalos segun SM-2 | Alta |
| FR-FC-006 | El sistema SHALL actualizar ease factor dinamicamente | Alta |
| FR-FC-007 | El sistema MUST permitir calificar respuestas (0-5) | Alta |
| FR-FC-008 | El sistema SHALL mostrar tarjetas debidas | Alta |
| FR-FC-009 | El sistema SHALL registrar logs de repaso | Media |
| FR-FC-010 | El sistema SHOULD mostrar estadisticas de deck | Media |
| FR-FC-011 | El sistema SHOULD permitir editar flashcards | Media |
| FR-FC-012 | El sistema MAY permitir eliminar flashcards | Baja |

### Requerimientos No Funcionales

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| NFR-FC-001 | El repaso SHALL responder en <100ms por tarjeta | Alta |
| NFR-FC-002 | El sistema SHALL soportar >10K flashcards por deck | Media |
| NFR-FC-003 | Los logs de repaso SHALL persistir indefinidamente | Alta |
| NFR-FC-004 | La generacion SHALL completar en <30s por 20 tarjetas | Media |

---

## 5. API Spec

### Endpoints REST

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

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Tema 1 - Constitucion",
  "description": "Flashcards del Tema 1",
  "tema_id": 1,
  "card_count": 0,
  "created_at": "2026-03-16T10:00:00"
}
```

---

#### GET /api/flashcards/decks

Lista todos los decks.

**Response (200 OK):**
```json
{
  "decks": [
    {
      "id": 1,
      "name": "Tema 1 - Constitucion",
      "card_count": 45,
      "new_cards": 10,
      "due_cards": 5,
      "created_at": "2026-03-16T10:00:00"
    }
  ],
  "total": 1
}
```

---

#### POST /api/flashcards/decks/{deck_id}/cards

Crea una flashcard manual.

**Request:**
```json
{
  "front": "Que es la Constitucion Espanola?",
  "back": "La norma suprema del ordenamiento juridico espanol, aprobada en 1978.",
  "source_chunk_id": 42
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "deck_id": 1,
  "front": "Que es la Constitucion Espanola?",
  "back": "La norma suprema del ordenamiento juridico espanol, aprobada en 1978.",
  "ease_factor": 2.5,
  "interval": 0,
  "repetitions": 0,
  "next_review": null,
  "created_at": "2026-03-16T10:05:00"
}
```

---

#### POST /api/flashcards/decks/{deck_id}/generate

Genera flashcards automaticamente desde temario.

**Request:**
```json
{
  "tema": 1,
  "count": 20,
  "difficulty": "medium"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "cards_created": 20,
  "cards": [
    {
      "id": 1,
      "front": "Que es la Constitucion Espanola?",
      "back": "La norma suprema..."
    }
  ],
  "duration_seconds": 15.3
}
```

---

#### GET /api/flashcards/decks/{deck_id}/due

Obtiene flashcards debidas para repaso.

**Response (200 OK):**
```json
{
  "deck_id": 1,
  "deck_name": "Tema 1 - Constitucion",
  "due_count": 5,
  "cards": [
    {
      "id": 1,
      "front": "Que es la Constitucion Espanola?",
      "interval": 6,
      "repetitions": 2
    }
  ]
}
```

---

#### POST /api/flashcards/cards/{card_id}/review

Registra una revision de flashcard.

**Request:**
```json
{
  "rating": 4
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "card": {
    "id": 1,
    "interval_before": 6,
    "interval_after": 15,
    "ease_factor_before": 2.5,
    "ease_factor_after": 2.6,
    "next_review": "2026-04-01"
  },
  "review_log_id": 123
}
```

---

#### GET /api/flashcards/decks/{deck_id}/stats

Obtiene estadisticas de un deck.

**Response (200 OK):**
```json
{
  "deck_id": 1,
  "deck_name": "Tema 1 - Constitucion",
  "total_cards": 45,
  "new_cards": 10,
  "due_cards": 5,
  "learned_cards": 30,
  "average_ease_factor": 2.45,
  "total_reviews": 250,
  "accuracy_rate": 0.78
}
```

---

## 6. CLI Spec

### Comandos

#### flashcards create-deck

Crea un nuevo deck.

```bash
python -m src.flashcards.cli create-deck <name> [OPTIONS]
```

**Argumentos:**
| Argumento | Requerido | Descripcion |
|-----------|-----------|-------------|
| name | Si | Nombre del deck |

**Opciones:**
| Opcion | Default | Descripcion |
|--------|---------|-------------|
| --tema, -t | None | ID del tema asociado |
| --desc, -d | "" | Descripcion del deck |

---

#### flashcards generate

Genera flashcards automaticamente.

```bash
python -m src.flashcards.cli generate --deck <deck_id> --tema <tema> [OPTIONS]
```

**Opciones:**
| Opcion | Default | Descripcion |
|--------|---------|-------------|
| --deck, -d | Requerido | ID del deck destino |
| --tema, -t | Requerido | Tema del que generar |
| --count, -c | 10 | Numero de flashcards |
| --difficulty | medium | Dificultad (easy/medium/hard) |

---

#### flashcards add

Anade una flashcard manual.

```bash
python -m src.flashcards.cli add --deck <deck_id> --front "<pregunta>" --back "<respuesta>"
```

---

#### flashcards review

Inicia sesion de repaso.

```bash
python -m src.flashcards.cli review <deck_name> [OPTIONS]
```

**Opciones:**
| Opcion | Default | Descripcion |
|--------|---------|-------------|
| --limit, -l | 20 | Maximo de tarjetas |
| --new-only | False | Solo tarjetas nuevas |

**Interaccion:**
```
$ python -m src.flashcards.cli review "Tema 1"

Sesion de repaso: Tema 1 - Constitucion
Tarjetas debidas: 5

[1/5] ========================================

FRENTE:
Que es la Constitucion Espanola?

[Presiona Enter para ver la respuesta]

REVES:
La norma suprema del ordenamiento juridico espanol, aprobada en 1978.

Califica tu respuesta:
  0 - Again (fallo completo)
  1 - Hard (incorrecto, reconocia)
  2 - Hard2 (incorrecto, facil de recordar)
  3 - Good (correcto con dificultad)
  4 - Easy (correcto con hesitation)
  5 - Very Easy (perfecto)

Tu calificacion [0-5]: 4

+ Intervalo: 1 dia -> 6 dias
+ Ease Factor: 2.50 -> 2.60

[2/5] ========================================
...
```

---

#### flashcards stats

Muestra estadisticas.

```bash
python -m src.flashcards.cli stats <deck_name>
```

**Output:**
```
Estadisticas: Tema 1 - Constitucion
=====================================

Total tarjetas:     45
Nuevas:             10
Aprendidas:         30
Debidas hoy:        5

Ease Factor promedio: 2.45
Total repasos:       250
Precision:           78%

Proxima revision: 5 tarjetas en 2 horas
```

---

#### flashcards list

Lista decks.

```bash
python -m src.flashcards.cli list
```

---

## 7. Data Models

### Deck

```python
@dataclass
class Deck:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    tema_id: Optional[int] = None
    card_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
```

### Flashcard

```python
@dataclass
class Flashcard:
    id: Optional[int] = None
    deck_id: int = 0
    front: str = ""
    back: str = ""
    # SM-2 fields
    ease_factor: float = 2.5      # 1.3 - 3.0+
    interval: int = 0             # Days until next review
    repetitions: int = 0          # Successful reviews count
    next_review: Optional[str] = None  # ISO date
    # Metadata
    source_chunk_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @property
    def is_new(self) -> bool:
        return self.repetitions == 0

    @property
    def is_due(self) -> bool:
        if not self.next_review:
            return True
        return date.fromisoformat(self.next_review) <= date.today()
```

### ReviewLog

```python
@dataclass
class ReviewLog:
    id: Optional[int] = None
    flashcard_id: int = 0
    rating: int = 0               # 0-5
    interval_before: int = 0
    interval_after: int = 0
    ease_factor_before: float = 2.5
    ease_factor_after: float = 2.5
    reviewed_at: Optional[str] = None
```

### ReviewSession

```python
@dataclass
class ReviewSession:
    deck_id: int
    deck_name: str
    cards_reviewed: int = 0
    cards_correct: int = 0
    cards_again: int = 0
    duration_seconds: float = 0.0
    review_logs: List[ReviewLog] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        if self.cards_reviewed == 0:
            return 0.0
        return (self.cards_correct / self.cards_reviewed) * 100
```

### DeckStats

```python
@dataclass
class DeckStats:
    deck_id: int
    deck_name: str
    total_cards: int = 0
    new_cards: int = 0
    due_cards: int = 0
    learned_cards: int = 0
    average_ease_factor: float = 2.5
    total_reviews: int = 0
```

---

## 8. Diagramas de Flujo

### Flujo de Repaso

```
+-------------+     +-------------+     +-------------+
|   Usuario   |---->|   Reviewer  |---->|  Get Due    |
|  (inicia)   |     |   (CLI)     |     |   Cards     |
+-------------+     +-------------+     +-------------+
                                               |
                                               v
+-------------+     +-------------+     +-------------+
|   Mostrar   |<----|  Hay mas?   |<----|   Deck DB   |
|   Card      |     |             |     |             |
+-------------+     +-------------+     +-------------+
       |
       v
+-------------+
|  Usuario    |
|  califica   |
|  (0-5)      |
+-------------+
       |
       v
+-------------+     +-------------+
|  Scheduler  |---->|  Update     |
|  (SM-2)     |     |  Card       |
+-------------+     +-------------+
       |                   |
       v                   v
+-------------+     +-------------+
|  Log Review |     |  Next Card  |
+-------------+     +-------------+
```

### Flujo de Generacion

```
+-------------+     +-------------+     +-------------+
|   Usuario   |---->|  Generator  |---->|  Search     |
|  (solicita) |     |   (CLI)     |     |  Chunks     |
+-------------+     +-------------+     +-------------+
                                               |
                                               v
                                        +-------------+
                                        |  Temario DB |
                                        |  (chunks)   |
                                        +-------------+
                                               |
                                               v
+-------------+     +-------------+     +-------------+
|  Save       |<----|  Parse      |<----|  MiniMax    |
|  Cards      |     |  Response   |     |  API        |
+-------------+     +-------------+     +-------------+
       |
       v
+-------------+
|  Flashcard  |
|  DB         |
+-------------+
```

---

**Fin del documento del Modulo Flashcards SM-2**
