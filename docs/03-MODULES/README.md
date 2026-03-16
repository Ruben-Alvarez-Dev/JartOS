# Modulos del Sistema

Especificaciones detalladas de cada modulo principal de JartOS.

## Modulos

### 1. [temario-ingestion.md](temario-ingestion.md)
**Ingesta de temarios**

- Formatos soportados: PDF, DOCX, MD
- Extraccion de texto y estructura
- Chunking inteligente
- Indexacion para RAG

### 2. [flashcards-sm2.md](flashcards-sm2.md)
**Sistema de flashcards**

- Algoritmo SM-2 para repeticion espaciada
- Generacion automatica de flashcards
- Tracking de progreso
- Exportacion a Anki

### 3. [test-generator.md](test-generator.md)
**Generador de tests**

- Tests por tema, subtema o aleatorios
- Simulacros de examen
- Estadisticas de rendimiento
- Modo estudio vs modo examen

### 4. [dashboard-web.md](dashboard-web.md)
**Dashboard web**

- Next.js 15 + React 19
- Visualizacion de progreso
- Estadisticas de estudio
- Gestion de temarios

## Dependencias entre Modulos

```
temario-ingestion
       |
       v
   flashcards-sm2  <----+
       |                 |
       v                 |
  test-generator         |
       |                 |
       +-----------------+
       |
       v
  dashboard-web
```

## Capas de cada Modulo

Cada modulo sigue la arquitectura de 5 capas:

1. **Core/Domain**: Entidades y logica de negocio
2. **Application**: Casos de uso
3. **Infrastructure**: Implementaciones concretas
4. **Interface**: API y CLI
5. **Presentation**: UI (solo dashboard-web)

## Progreso de Implementacion

| Modulo | Core | App | Infra | Interface | Estado |
|--------|------|-----|-------|-----------|--------|
| temario-ingestion | Planificado | - | - | - | Fase 1 |
| flashcards-sm2 | Planificado | - | - | - | Fase 2 |
| test-generator | Planificado | - | - | - | Fase 2 |
| dashboard-web | Planificado | - | - | - | Fase 3 |

---

*Ver [04-ROADMAP.md](../04-ROADMAP.md) para el plan completo de desarrollo*
