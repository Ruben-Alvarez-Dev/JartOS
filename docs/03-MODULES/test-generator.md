# Modulo: Test Generator

**Version:** 0.1.0
**Ultima actualizacion:** 2025-03-16

---

## Indice

1. [Descripcion](#1-descripcion)
2. [User Stories](#2-user-stories)
3. [Requirements (RFC 2119)](#3-requirements-rfc-2119)
4. [API Spec](#4-api-spec)
5. [CLI Spec](#5-cli-spec)
6. [Data Models](#6-data-models)
7. [Diagramas de Flujo](#7-diagramas-de-flujo)

---

## 1. Descripcion

El modulo de **Test Generator** permite crear tests automaticos desde el temario, tomar tests en diferentes modos (practica/examen), y analizar los resultados para detectar areas debiles.

### Funcionalidades Principales

- Generacion automatica de preguntas desde temario
- Multiples tipos de preguntas (opcion multiple, verdadero/falso, abiertas)
- Modos de test (practica con feedback, examen sin feedback)
- Analisis de resultados con deteccion de areas debiles
- Historial de sesiones de test
- Exportacion de resultados

### Componentes

```
src/tests/
+-- __init__.py      # Exporta componentes principales
+-- models.py        # Data models (Test, Question, Session, Result)
+-- store.py         # SQLite database operations
+-- generator.py     # AI-powered question generation
+-- solver.py        # Answer evaluation
+-- analyzer.py      # Result analysis
+-- cli.py           # CLI commands
```

---

## 2. User Stories

### US-TG-001: Generar test de practica

**Como** opositor
**Quiero** generar un test de practica de un tema
**Para** evaluar mi conocimiento y recibir feedback inmediato

**Criterios de Aceptacion:**
- GIVEN un tema con chunks en el sistema
- WHEN solicito generar un test de practica
- THEN el sistema genera preguntas desde el temario
- AND crea un test con la configuracion especificada
- AND me permite responder con feedback inmediato
- AND muestra la respuesta correcta al fallar

---

### US-TG-002: Tomar test en modo examen

**Como** opositor
**Quiero** tomar un test en modo examen
**Para** simular condiciones reales de oposicion

**Criterios de Aceptacion:**
- GIVEN un test generado
- WHEN inicio el test en modo examen
- THEN el sistema muestra preguntas sin feedback
- AND registra tiempo por pregunta
- AND solo muestra resultados al finalizar
- AND calcula puntuacion final

---

### US-TG-003: Ver analisis de resultados

**Como** opositor
**Quiero** ver un analisis detallado de mis resultados
**Para** identificar areas que necesito reforzar

**Criterios de Aceptacion:**
- GIVEN una sesion de test completada
- WHEN solicito el analisis
- THEN el sistema muestra:
  - Puntuacion general
  - Preguntas correctas/incorrectas
  - Tiempo promedio por pregunta
  - Areas debiles detectadas
  - Recomendaciones de estudio

---

### US-TG-004: Revisar historial de tests

**Como** opositor
**Quiero** ver mi historial de tests tomados
**Para** seguir mi progreso a lo largo del tiempo

**Criterios de Aceptacion:**
- GIVEN tests completados previamente
- WHEN solicito el historial
- THEN el sistema muestra lista de sesiones
- AND permite filtrar por tema/fecha
- AND muestra tendencias de puntuacion

---

### US-TG-005: Crear pregunta personalizada

**Como** opositor
**Quiero** anadir preguntas personalizadas a un test
**Para** incluir preguntas especificas de mi interes

**Criterios de Aceptacion:**
- GIVEN un deck o test existente
- WHEN creo una pregunta personalizada
- THEN el sistema permite definir:
  - Texto de la pregunta
  - Opciones (si aplica)
  - Respuesta correcta
  - Explicacion
- AND la anade al test

---

## 3. Requirements (RFC 2119)

### Requerimientos Funcionales

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| FR-TG-001 | El sistema MUST generar preguntas de opcion multiple | Alta |
| FR-TG-002 | El sistema SHOULD generar preguntas de verdadero/falso | Media |
| FR-TG-003 | El sistema MAY generar preguntas abiertas | Baja |
| FR-TG-004 | El sistema MUST soportar modo practica con feedback | Alta |
| FR-TG-005 | El sistema MUST soportar modo examen sin feedback | Alta |
| FR-TG-006 | El sistema SHALL calcular puntuacion automaticamente | Alta |
| FR-TG-007 | El sistema SHALL detectar areas debiles | Alta |
| FR-TG-008 | El sistema SHALL registrar tiempo por pregunta | Media |
| FR-TG-009 | El sistema SHOULD permitir configurar dificultad | Media |
| FR-TG-010 | El sistema SHOULD permitir limite de tiempo global | Media |
| FR-TG-011 | El sistema SHALL almacenar historial de sesiones | Alta |
| FR-TG-012 | El sistema SHOULD exportar resultados a PDF/JSON | Baja |

### Requerimientos No Funcionales

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| NFR-TG-001 | La generacion SHALL completar en <30s para 20 preguntas | Alta |
| NFR-TG-002 | El test SHALL responder en <100ms por interaccion | Alta |
| NFR-TG-003 | El analisis SHALL completar en <5s | Alta |
| NFR-TG-004 | El sistema SHALL soportar tests de hasta 100 preguntas | Media |

---

## 4. API Spec

### Endpoints REST

#### POST /api/tests/generate

Genera un nuevo test.

**Request:**
```json
{
  "title": "Test Tema 1 - Constitucion",
  "question_count": 10,
  "question_types": ["multiple_choice"],
  "difficulty": "medium",
  "temas": [1],
  "mode": "practice",
  "time_limit_minutes": null
}
```

**Response (201 Created):**
```json
{
  "id": "test_abc123",
  "title": "Test Tema 1 - Constitucion",
  "config": {
    "question_count": 10,
    "question_types": ["multiple_choice"],
    "difficulty": "medium",
    "temas": [1],
    "mode": "practice"
  },
  "questions": [
    {
      "id": "q1",
      "question_type": "multiple_choice",
      "text": "En que ano se aprobo la Constitucion Espanola?",
      "options": [
        "1975",
        "1978",
        "1982",
        "1986"
      ]
    }
  ],
  "created_at": "2025-03-16T10:00:00"
}
```

---

#### POST /api/tests/{test_id}/start

Inicia una sesion de test.

**Response (200 OK):**
```json
{
  "session_id": "sess_xyz789",
  "test_id": "test_abc123",
  "status": "in_progress",
  "current_question_index": 0,
  "started_at": "2025-03-16T10:05:00",
  "time_limit_minutes": null
}
```

---

#### POST /api/tests/sessions/{session_id}/answer

Envia respuesta a una pregunta.

**Request:**
```json
{
  "question_id": "q1",
  "answer_index": 1
}
```

**Response (200 OK) - Modo Practica:**
```json
{
  "is_correct": true,
  "correct_index": 1,
  "explanation": "La Constitucion Espanola fue aprobada por las Cortes el 31 de octubre de 1978...",
  "current_question_index": 1,
  "score_so_far": {
    "correct": 1,
    "total": 1
  }
}
```

**Response (200 OK) - Modo Examen:**
```json
{
  "recorded": true,
  "current_question_index": 1
}
```

---

#### POST /api/tests/sessions/{session_id}/complete

Completa la sesion de test.

**Response (200 OK):**
```json
{
  "session_id": "sess_xyz789",
  "test_id": "test_abc123",
  "status": "completed",
  "completed_at": "2025-03-16T10:35:00",
  "result": {
    "total_questions": 10,
    "correct_answers": 8,
    "incorrect_answers": 2,
    "unanswered": 0,
    "score_percentage": 80.0,
    "time_spent_seconds": 1800,
    "passed": true
  }
}
```

---

#### GET /api/tests/sessions/{session_id}/analysis

Obtiene analisis detallado de la sesion.

**Response (200 OK):**
```json
{
  "session_id": "sess_xyz789",
  "score_percentage": 80.0,
  "time_spent_seconds": 1800,
  "average_time_per_question": 180,
  "weak_areas": [
    {
      "tema": "1",
      "apartado": "1.3",
      "questions_wrong": 2,
      "topic": "Principios constitucionales"
    }
  ],
  "strong_areas": [
    {
      "tema": "1",
      "apartado": "1.1",
      "questions_correct": 3,
      "topic": "Historia constitucional"
    }
  ],
  "recommendations": [
    "Repasar el apartado 1.3 sobre principios constitucionales",
    "Considera crear flashcards del tema 1.3"
  ]
}
```

---

#### GET /api/tests/history

Obtiene historial de tests.

**Query Parameters:**
| Parametro | Default | Descripcion |
|-----------|---------|-------------|
| tema | null | Filtrar por tema |
| limit | 20 | Maximo de resultados |
| offset | 0 | Offset para paginacion |

**Response (200 OK):**
```json
{
  "sessions": [
    {
      "session_id": "sess_xyz789",
      "test_title": "Test Tema 1 - Constitucion",
      "score_percentage": 80.0,
      "completed_at": "2025-03-16T10:35:00",
      "time_spent_seconds": 1800
    }
  ],
  "total": 15,
  "average_score": 75.5
}
```

---

## 5. CLI Spec

### Comandos

#### tests generate

Genera un nuevo test.

```bash
python -m src.tests.cli generate [OPTIONS]
```

**Opciones:**
| Opcion | Default | Descripcion |
|--------|---------|-------------|
| --tema, -t | Requerido | Tema del test |
| --questions, -q | 10 | Numero de preguntas |
| --type | multiple_choice | Tipo de pregunta |
| --difficulty | medium | Dificultad (easy/medium/hard) |
| --mode | practice | Modo (practice/exam) |
| --time, -m | null | Limite de tiempo en minutos |

---

#### tests take

Toma un test existente.

```bash
python -m src.tests.cli take <test_id>
```

---

#### tests history

Muestra historial de tests.

```bash
python -m src.tests.cli history [OPTIONS]
```

**Opciones:**
| Opcion | Default | Descripcion |
|--------|---------|-------------|
| --tema, -t | null | Filtrar por tema |
| --limit, -l | 10 | Maximo de resultados |

---

#### tests analyze

Analiza una sesion completada.

```bash
python -m src.tests.cli analyze <session_id>
```

---

## 6. Data Models

### TestConfig

```python
@dataclass
class TestConfig:
    question_count: int = 10
    question_types: list[QuestionType] = field(
        default_factory=lambda: [QuestionType.MULTIPLE_CHOICE]
    )
    difficulty: str = "medium"
    temas: list[str] = field(default_factory=list)
    mode: TestMode = TestMode.PRACTICE
    time_limit_minutes: Optional[int] = None
```

### Question

```python
class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    OPEN_ENDED = "open_ended"

@dataclass
class Question:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    test_id: str = ""
    question_type: QuestionType = QuestionType.MULTIPLE_CHOICE
    text: str = ""
    options: list[str] = field(default_factory=list)
    correct_index: int = 0
    explanation: str = ""
    difficulty: str = "medium"
    source_chunk_ids: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def check_answer(self, answer_index: int) -> bool:
        return answer_index == self.correct_index
```

### Test

```python
@dataclass
class Test:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    config: TestConfig = field(default_factory=TestConfig)
    questions: list[Question] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def question_count(self) -> int:
        return len(self.questions)
```

### SessionAnswer

```python
@dataclass
class SessionAnswer:
    question_id: str
    answer_index: int
    is_correct: bool
    time_spent_seconds: float = 0.0
    answered_at: datetime = field(default_factory=datetime.now)
```

### TestSession

```python
@dataclass
class TestSession:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    test_id: str = ""
    status: str = "in_progress"  # in_progress, completed, abandoned
    answers: dict[str, SessionAnswer] = field(default_factory=dict)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    current_question_index: int = 0

    def record_answer(self, question_id: str, answer_index: int,
                      is_correct: bool, time_spent: float = 0.0):
        self.answers[question_id] = SessionAnswer(
            question_id=question_id,
            answer_index=answer_index,
            is_correct=is_correct,
            time_spent_seconds=time_spent,
        )

    def complete(self):
        self.status = "completed"
        self.completed_at = datetime.now()
```

### TestResult

```python
@dataclass
class TestResult:
    session_id: str = ""
    test_id: str = ""
    total_questions: int = 0
    correct_answers: int = 0
    incorrect_answers: int = 0
    unanswered: int = 0
    score_percentage: float = 0.0
    time_spent_seconds: float = 0.0
    weak_areas: list[str] = field(default_factory=list)
    strong_areas: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def passed(self) -> bool:
        return self.score_percentage >= 60.0
```

---

## 7. Diagramas de Flujo

### Flujo de Generacion

```
+-------------+     +-------------+     +-------------+
|   Config    |---->|   Search    |---->|  Select     |
|   (params)  |     |   Chunks    |     |  Chunks     |
+-------------+     +-------------+     +-------------+
                                               |
                                               v
+-------------+     +-------------+     +-------------+
|   Store     |<----|  Parse      |<----|  MiniMax    |
|   Test      |     |  Response   |     |  API        |
+-------------+     +-------------+     +-------------+
       |
       v
+-------------+
|   Return    |
|   Test ID   |
+-------------+
```

### Flujo de Test Interactivo

```
+-------------+     +-------------+     +-------------+
|   Start     |---->|   Create    |---->|   Show      |
|   Test      |     |   Session   |     |   Question  |
+-------------+     +-------------+     +-------------+
                                               |
                       +-----------------------+
                       |
                       v
+-------------+     +-------------+     +-------------+
|   Next      |<----|   Feedback  |<----|   Submit    |
|   Question  |     |   (si pract)|     |   Answer    |
+-------------+     +-------------+     +-------------+
       |
       v
+-------------+     +-------------+
|   Complete  |---->|   Analyze   |
|   Session   |     |   Results   |
+-------------+     +-------------+
       |
       v
+-------------+
|   Save      |
|   Results   |
+-------------+
```

---

**Fin del documento del Modulo Test Generator**
