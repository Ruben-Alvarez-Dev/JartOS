# 💾 PROTOCOLO DE RECUPERACIÓN DE ESTADO

## 1. Propósito

Este protocolo permite **recuperar el contexto** del proyecto después de:
- Cierre de sesión
- Cambio de modelo/IA
- Pérdida de contexto
- Reinicio del sistema

---

## 2. Archivo de Estado

**Ubicación:** `/Users/ruben/JartOS/STATE_LOG.md`

### Formato Obligatorio

```markdown
# ESTADO ACTUAL (JARTOS)

**Fecha:** 2026-03-17 14:30:00
**Versión NEW_SPECS:** 2.0.0
**Fase/Sprint Activo:** Sprint 1.1 - Cobertura Temario Store

## Última Acción Completada
- Commiteado y pusheado NEW_SPECS completo (7 documentos)
- Actualizado 00_MASTER_MANIFEST.md con reglas fusionadas
- Actualizado 01-05 con especificaciones completas

## Siguiente Paso Técnico Exacto
1. Crear test `test_temario_store.py` en `TIER_11_CONTROL/tests/`
2. Test: `test_insert_document()`
3. Test: `test_insert_chunk_with_embedding()`
4. Ejecutar: `pytest TIER_11_CONTROL/tests/test_temario_store.py -v`

## Estado de Infraestructura
| Componente | Estado | Notas |
|------------|--------|-------|
| Docker | Pendiente | No configurado |
| SQLite (temario.db) | Activo | En TIER_06_STORAGE/data/ |
| 1Password CLI | Activo | Conectado al vault |
| GitHub | Sincronizado | main@78e2395 |
| Tests | 162 pasando | Pytest con asyncio |

## Archivos Críticos Modificados Recientemente
| Archivo | Cambio | Fecha |
|---------|--------|-------|
| NEW_SPECS/*.md | Reescritos completos | 2026-03-17 |
| JARTOS_RULES.md | Creado en memoria | 2026-03-17 |
| secrets.template.env | Creado | 2026-03-16 |

## Notas para la IA
- PYTHONPATH debe apuntar al root del proyecto
- Los tests web levantan Popen local en puerto 8765
- Buscar credenciales en vault "GitHub" de 1Password, NO en "Personal"
- Golden RAG tiene 5 escalones de destilación
- Concilio requiere 3/3 votos APTO

## Bloqueos Conocidos
- Ninguno actualmente

## Deuda Técnica
- [ ] Docker compose no configurado
- [ ] Qdrant no levantado
- [ ] LiteLLM proxy no configurado
```

---

## 3. Regla de Actualización

**OBLIGATORIO** actualizar `STATE_LOG.md`:
- Al final de cada sesión de trabajo
- Después de cada sprint completado
- Antes de cualquier cambio de contexto
- Al detectar un bug o bloqueo

---

## 4. Comandos de Recuperación

Si la IA pierde contexto, debe ejecutar:

```bash
# 1. Leer estado actual
cat /Users/ruben/JartOS/STATE_LOG.md

# 2. Leer reglas
cat ~/.claude/projects/-Users-ruben-JartOS/memory/JARTOS_RULES.md

# 3. Leer master manifest
cat /Users/ruben/JartOS/NEW_SPECS/00_MASTER_MANIFEST.md

# 4. Verificar estado de tests
pytest TIER_11_CONTROL/tests/ --collect-only
```

---

## 5. Formato de Log del Daemon

El Daemon (`TIER_11_CONTROL/daemon.py`) registra eventos en JSONL:

```json
{"timestamp": "2026-03-17T14:30:00Z", "type": "AGENT_DECISION", "agent": "maestro", "action": "delegate", "target": "redactor", "task_id": "t_001"}
{"timestamp": "2026-03-17T14:35:00Z", "type": "CONCILIO_VOTE", "document_id": "d_123", "juridico": true, "pedagogico": true, "tecnico": true, "result": "approved"}
{"timestamp": "2026-03-17T14:40:00Z", "type": "GUARDIAN_ACTION", "action": "home_assistant_call", "approved": true, "executed": true}
```

---

## 6. Snapshot Atómico

El sistema debe crear snapshots automáticos:

| Trigger | Acción |
|---------|--------|
| Cada 50 cambios en código | `git commit -m "snapshot: auto"` |
| Cada 10 minutos de actividad | Backup a NVMe |
| Cada sprint completado | Tag: `v0.X.Y-sprint-N` |

---

## 7. Contacto de Emergencia

En caso de pérdida total de contexto:

1. Leer este archivo (`06_STATE_RECOVERY_PROTOCOL.md`)
2. Leer `STATE_LOG.md`
3. Leer `JARTOS_RULES.md` en memoria de Claude
4. Verificar tests: `pytest TIER_11_CONTROL/tests/ -v`
5. Continuar desde "Siguiente Paso Técnico" del STATE_LOG
