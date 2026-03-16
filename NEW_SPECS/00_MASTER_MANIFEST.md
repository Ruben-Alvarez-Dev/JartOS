# 🌐 JARTOS: MASTER MANIFEST (Spec-Driven DNA)

> **ESTADO:** Única Fuente de Verdad (Single Source of Truth) - Producción.
> **DIRECTIVA CRÍTICA:** Este documento y su directorio contienen el diseño técnico estricto. Toda implementación debe obedecer el Spec-Driven Development (SDD) y estar cubierta por Test-Driven Development (TDD). **Cero mocks. Cero asunciones.**

## 1. Definición del Sistema
JartOS es un ecosistema agéntico jerárquico y aislado (TIERs) para la preparación de Oposiciones FP Hostelería y certificaciones técnicas (IA-102), con soporte para dictado/coach multimodal y una capa de seguridad ("El Guardián").

## 2. Índice del ADN Técnico

1. **`01_CONTEXT_AND_INFRASTRUCTURE.md`**: Perfil del usuario, objetivos inamovibles y topología de hardware (Mac Mini + MacBook + Periféricos).
2. **`02_ARCHITECTURE_AND_SECURITY.md`**: El Anillo Guardián, TIERs definidos, y configuración base de Docker Compose.
3. **`03_INGESTION_AND_DATA_FLOW.md`**: Esquemas reales de la Base de Datos SQLite (`temario_documents`, `temario_chunks`) y flujos INBOX/LAB.
4. **`04_AGENT_SYSTEM.md`**: Contratos técnicos de FastMCP, Maestro, Especialistas y el sistema de votación del Concilio.
5. **`05_DEVELOPMENT_ROADMAP.md`**: Sprints iterativos a ejecutar bajo el paradigma TDD (Test-First).
6. **`06_STATE_RECOVERY_PROTOCOL.md`**: Plantilla de log de estado persistente.
7. **`openapi.yaml`** (en `docs/api`): Contrato oficial de las APIs internas.

## 3. Reglas de Compromiso Inquebrantables
- **Realidad Ante Todo:** No se escriben funciones vacías ni "mocks". Si un componente necesita BD, usa `temario.db`.
- **TDD Estricto:** Antes de añadir una línea de código lógica a un TIER, se crea un test en `TIER_11_CONTROL/tests/` que debe fallar primero.
- **Respeto a lo Existente:** No se borra ni sobrescribe código funcional (ej. integraciones LiveKit/Zadarma).