# Modulo: Dashboard Web

**Version:** 0.1.0
**Ultima actualizacion:** 2026-03-16

---

## Indice

1. [Descripcion](#1-descripcion)
2. [User Stories](#2-user-stories)
3. [Requirements (RFC 2119)](#3-requirements-rfc-2119)
4. [API Spec](#4-api-spec)
5. [Paginas y Rutas](#5-paginas-y-rutas)
6. [Componentes UI](#6-componentes-ui)
7. [Tecnologias Frontend](#7-tecnologias-frontend)

---

## 1. Descripcion

El modulo de **Dashboard Web** proporciona una interfaz web moderna e intuitiva para gestionar el estudio de oposiciones, permitiendo acceder a todas las funcionalidades del sistema desde el navegador.

### Funcionalidades Principales

- Dashboard principal con vista general de progreso
- Gestion de temario (ingestion, busqueda, QA)
- Gestion de decks y flashcards
- Sesiones de repaso interactivas
- Tomar tests con feedback
- Calendario de repaso
- Metricas y estadisticas detalladas
- Configuracion del sistema

### Componentes

```
src/web/
+-- __init__.py           # App factory
+-- app.py                # FastAPI application
+-- routes/
|   +-- __init__.py
|   +-- dashboard.py      # Dashboard principal
|   +-- temario.py        # Rutas de temario
|   +-- flashcards.py     # Rutas de flashcards
|   +-- tests.py          # Rutas de tests
+-- static/
|   +-- css/
|   |   +-- styles.css
|   +-- js/
|     +-- app.js
+-- templates/
|   +-- base.html
|   +-- dashboard/
|   |   +-- index.html
|   +-- temario/
|   |   +-- list.html
|   |   +-- search.html
|   +-- flashcards/
|   |   +-- decks.html
|   |   +-- review.html
|   +-- tests/
|     +-- take.html
|     +-- results.html
```

---

## 2. User Stories

### US-WD-001: Ver dashboard principal

**Como** opositor
**Quiero** ver un dashboard con mi progreso general
**Para** tener una vision rapida de mi estado de preparacion

**Criterios de Aceptacion:**
- GIVEN que he usado el sistema
- WHEN accedo al dashboard
- THEN veo:
  - Total de flashcards y debidas hoy
  - Puntuaciones de tests recientes
  - Streak de dias de estudio
  - Progreso por tema
  - Recomendaciones del dia

---

### US-WD-002: Ingerir documento desde web

**Como** opositor
**Quiero** subir un documento PDF desde la web
**Para** ingerirlo al sistema sin usar CLI

**Criterios de Aceptacion:**
- GIVEN un archivo PDF valido
- WHEN lo subo mediante el formulario
- THEN el sistema lo procesa
- AND muestra progreso de ingestion
- AND confirma cuando termina

---

### US-WD-003: Repasar flashcards en web

**Como** opositor
**Quiero** repasar flashcards desde el navegador
**Para** estudiar sin depender de CLI

**Criterios de Aceptacion:**
- GIVEN un deck con flashcards debidas
- WHEN inicio una sesion de repaso
- THEN veo la tarjeta con la pregunta
- AND puedo mostrar la respuesta
- AND puedo calificar (0-5)
- AND veo progreso de la sesion

---

### US-WD-004: Tomar test en web

**Como** opositor
**Quiero** tomar un test desde el navegador
**Para** evaluar mi conocimiento comodamente

**Criterios de Aceptacion:**
- GIVEN un test generado
- WHEN inicio el test
- THEN veo las preguntas secuencialmente
- AND puedo responder
- AND veo feedback (si modo practica)
- AND veo resultados al final

---

### US-WD-005: Ver calendario de repaso

**Como** opositor
**Quiero** ver un calendario con mis repasos programados
**Para** planificar mi tiempo de estudio

**Criterios de Aceptacion:**
- GIVEN flashcards con fechas de repaso
- WHEN accedo al calendario
- THEN veo cada dia con cantidad de tarjetas debidas
- AND puedo hacer clic para ver detalles
- AND puedo filtrar por deck

---

## 3. Requirements (RFC 2119)

### Requerimientos Funcionales

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| FR-WD-001 | El sistema MUST proveer interfaz web responsive | Alta |
| FR-WD-002 | El sistema MUST mostrar dashboard principal | Alta |
| FR-WD-003 | El sistema SHALL permitir subir documentos | Alta |
| FR-WD-004 | El sistema SHALL permitir repaso de flashcards | Alta |
| FR-WD-005 | El sistema SHALL permitir tomar tests | Alta |
| FR-WD-006 | El sistema SHOULD mostrar calendario de repaso | Media |
| FR-WD-007 | El sistema SHOULD mostrar graficos de progreso | Media |
| FR-WD-008 | El sistema MAY permitir exportar datos | Baja |
| FR-WD-009 | El sistema SHALL soportar modo oscuro | Media |
| FR-WD-010 | El sistema SHALL ser accesible (WCAG 2.1 AA) | Media |

### Requerimientos No Funcionales

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| NFR-WD-001 | La pagina SHALL cargar en <2s | Alta |
| NFR-WD-002 | El server SHALL soportar 10 usuarios concurrentes | Media |
| NFR-WD-003 | La interfaz SHALL ser responsive (mobile-first) | Alta |
| NFR-WD-004 | El servidor SHALL correr en localhost:8000 | Alta |

---

## 4. API Spec

### Endpoints REST (adicionales a modulos)

#### GET /api/dashboard/summary

Obtiene resumen del dashboard.

**Response (200 OK):**
```json
{
  "total_flashcards": 450,
  "flashcards_due_today": 15,
  "total_tests": 12,
  "tests_passed": 10,
  "study_streak_days": 7,
  "total_study_hours": 45.5,
  "progress_by_tema": [
    {"tema": 1, "progress": 85},
    {"tema": 2, "progress": 60},
    {"tema": 3, "progress": 40}
  ],
  "recent_activity": [
    {"date": "2026-03-16", "type": "review", "count": 25},
    {"date": "2026-03-15", "type": "test", "score": 85}
  ],
  "recommendations": [
    {"type": "review", "message": "Tienes 15 tarjetas debidas hoy"},
    {"type": "weak_area", "message": "Refuerza Tema 3, Apartado 2"}
  ]
}
```

---

#### GET /api/calendar/{year}/{month}

Obtiene calendario de repaso.

**Response (200 OK):**
```json
{
  "year": 2026,
  "month": 3,
  "days": [
    {
      "day": 16,
      "due_cards": 15,
      "decks": [1, 2]
    },
    {
      "day": 17,
      "due_cards": 8,
      "decks": [1]
    }
  ]
}
```

---

#### GET /api/stats/weekly

Obtiene estadisticas semanales.

**Response (200 OK):**
```json
{
  "week_start": "2026-03-10",
  "week_end": "2026-03-16",
  "total_reviews": 150,
  "total_tests": 3,
  "avg_test_score": 78,
  "study_time_hours": 12.5,
  "cards_learned": 25,
  "daily_breakdown": [
    {"day": "Mon", "reviews": 20, "tests": 0},
    {"day": "Tue", "reviews": 25, "tests": 1}
  ]
}
```

---

## 5. Paginas y Rutas

### Rutas Principales

| Ruta | Plantilla | Descripcion |
|------|-----------|-------------|
| `/` | `dashboard/index.html` | Dashboard principal |
| `/temario` | `temario/list.html` | Lista de documentos |
| `/temario/search` | `temario/search.html` | Busqueda semantica |
| `/temario/qa` | `temario/qa.html` | Preguntar al temario |
| `/flashcards` | `flashcards/decks.html` | Lista de decks |
| `/flashcards/{id}` | `flashcards/deck.html` | Detalle de deck |
| `/flashcards/{id}/review` | `flashcards/review.html` | Sesion de repaso |
| `/tests` | `tests/list.html` | Lista de tests |
| `/tests/{id}` | `tests/take.html` | Tomar test |
| `/tests/results/{id}` | `tests/results.html` | Resultados |
| `/calendar` | `calendar/index.html` | Calendario de repaso |
| `/stats` | `stats/index.html` | Estadisticas |

---

## 6. Componentes UI

### Componentes Principales

#### Dashboard Card

```html
<div class="dashboard-card">
  <h3>Flashcards</h3>
  <div class="stat">
    <span class="value">450</span>
    <span class="label">Total</span>
  </div>
  <div class="stat">
    <span class="value highlight">15</span>
    <span class="label">Due Today</span>
  </div>
</div>
```

#### Progress Bar

```html
<div class="progress-bar">
  <div class="progress" style="width: 75%"></div>
  <span class="label">75% Complete</span>
</div>
```

#### Flashcard Review

```html
<div class="flashcard-container">
  <div class="flashcard" id="card">
    <div class="front">
      <p>{{ question }}</p>
      <button onclick="showAnswer()">Show Answer</button>
    </div>
    <div class="back hidden">
      <p>{{ answer }}</p>
      <div class="rating-buttons">
        <button onclick="rate(0)">Again</button>
        <button onclick="rate(3)">Good</button>
        <button onclick="rate(5)">Easy</button>
      </div>
    </div>
  </div>
</div>
```

#### Test Question

```html
<div class="test-question">
  <h4>Question {{ index }}/{{ total }}</h4>
  <p class="question-text">{{ question }}</p>
  <ul class="options">
    {% for option in options %}
    <li>
      <label>
        <input type="radio" name="answer" value="{{ loop.index0 }}">
        {{ option }}
      </label>
    </li>
    {% endfor %}
  </ul>
  <button onclick="submitAnswer()">Submit</button>
</div>
```

---

## 7. Tecnologias Frontend

### Stack Frontend

| Componente | Tecnologia | Version |
|------------|------------|---------|
| Templates | Jinja2 | 3.1+ |
| CSS Framework | Tailwind CSS | 4.0+ |
| JavaScript | Alpine.js | 3.x |
| Graficos | Chart.js | 4.x |
| Iconos | Lucide Icons | - |

### Estructura CSS (Tailwind)

```css
/* custom.css - clases personalizadas */
:root {
  --primary: #3b82f6;
  --secondary: #64748b;
  --success: #22c55e;
  --warning: #f59e0b;
  --error: #ef4444;
}

.flashcard {
  @apply bg-white rounded-lg shadow-lg p-8 min-h-[200px];
}

.flashcard.flipping {
  @apply animate-flip;
}

.rating-btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors;
}

.rating-btn.again {
  @apply bg-red-100 text-red-700 hover:bg-red-200;
}

.rating-btn.good {
  @apply bg-blue-100 text-blue-700 hover:bg-blue-200;
}

.rating-btn.easy {
  @apply bg-green-100 text-green-700 hover:bg-green-200;
}
```

### JavaScript (Alpine.js)

```javascript
// Flashcard Review Component
document.addEventListener('alpine:init', () => {
  Alpine.data('flashcardReview', () => ({
    cards: [],
    currentIndex: 0,
    showAnswer: false,

    get currentCard() {
      return this.cards[this.currentIndex]
    },

    flip() {
      this.showAnswer = !this.showAnswer
    },

    async rate(rating) {
      await fetch(`/api/flashcards/cards/${this.currentCard.id}/review`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({rating})
      })

      this.currentIndex++
      this.showAnswer = false
    }
  }))
})
```

---

**Fin del documento del Modulo Dashboard Web**
