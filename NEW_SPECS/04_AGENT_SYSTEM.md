# 🤖 EL SISTEMA DE AGENTES (MAESTRO Y CONCILIO)

El comportamiento de los agentes NO es un script monolítico, es un orquestador basado en **FastMCP** (Model Context Protocol).

## 1. El Maestro (Orquestador Principal)
Implementado en `TIER_03_AGENTS/maestro_orchestrator.py` (usando `mcp_orchestrator.py` como base).
- **Entrada:** Recibe objetivos vía API o Web.
- **Acción:** Posee herramientas (tools) registradas en MCP.
  - `@mcp.tool() def delegate_to_specialist(specialist_id, task)`
  - `@mcp.tool() def query_temario(query_string)`
- Delega el trabajo "sucio" a los especialistas y pide autorización al Concilio.

## 2. El Concilio (Control de Calidad Estricto)
Implementado en `TIER_03_AGENTS/concilio.py`.
Todo documento o plan crítico debe pasar por la función `validate_content()`.
- **Mecanismo Real:** Llama al LLM configurado (ej. Claude o GPT) pasando 3 system prompts diferentes de manera concurrente:
  1. `prompt_juridico.md`: Comprueba leyes (LOE, FP).
  2. `prompt_pedagogico.md`: Comprueba RA, CE.
  3. `prompt_tecnico.md`: Comprueba veracidad de hostelería.
- **Regla:** Si cualquier respuesta JSON contiene `"apto": false`, el documento es rebotado al Maestro con la llave `"feedback"`.

## 3. FastMCP y LiveKit (El Coach Oral)
El Coach Oral se basa en los scripts actuales de `TIER_03_AGENTS/orchestrator` (`voice_agent_worker.py`).
Conecta STT (Speech-to-Text) y TTS (Text-to-Speech) mediante el servidor LiveKit, utilizando la Brio y el Mikro Anker. El agente escucha, calcula tiempos de exposición en milisegundos, e interrumpe o da feedback vocal.