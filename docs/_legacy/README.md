# Documentacion Legacy - OPENCLAW-city

Esta carpeta contiene documentacion del proyecto original **OPENCLAW-city**, del cual **oposiciones-system** deriva parte de su infraestructura.

## Contexto

OPENCLAW-city era un sistema de agentes IA para automatizacion de estudios juridicos. Algunos componentes han sido adaptados para oposiciones-system:

- Sistema de agentes (adaptado a preparacion de oposiciones)
- Sistema de memoria (adaptado a temarios y flashcards)
- Comunicacion A2A (Agent-to-Agent)
- Infraestructura de despliegue

## Archivos Legacy

| Archivo | Descripcion Original | Relevancia |
|---------|---------------------|------------|
| ARCHITECTURE.md | Arquitectura original del sistema | Historica |
| A2A-COMMUNICATION.md | Comunicacion entre agentes | Adaptada |
| AUDIT-TRAIL.md | Registro de auditoria | Historica |
| DASHBOARD.md | Dashboard original | Reemplazado |
| DEPLOYMENT.md | Guia de despliegue | Parcialmente util |
| EMAIL-BRIDGE.md | Puente de correo electronico | No utilizada |
| INFRASTRUCTURE.md | Infraestructura cloud | Historica |
| LIVEKIT-OPENCLAW-INTEGRATION.md | Integracion con LiveKit | No utilizada |
| LIVEKIT-SETUP.md | Configuracion de LiveKit | No utilizada |
| MAINTENANCE.md | Guia de mantenimiento | Parcialmente util |
| MEMORY-STORE.md | Almacen de memoria | Adaptada |
| OPENCLAW-GATEWAY.md | Gateway principal | No utilizada |
| ORCHESTRATOR-BOT.md | Bot orquestador | Adaptado |
| PERMISSIONS.md | Sistema de permisos | Historica |
| RAG-STORE.md | Almacen RAG | Adaptado |
| SECURITY-MODEL.md | Modelo de seguridad | Historica |
| SECURITY-PIPELINE.md | Pipeline de seguridad | Historica |
| ZADARMA-LIVEKIT-INTEGRATION.md | Integracion telefonica | No utilizada |

## Que Se Ha Mantenido

1. **Sistema de agentes**: La arquitectura de agentes se mantiene pero simplificada
2. **Sistema de memoria**: Engram + Graphiti adaptados para temarios
3. **Patrones de comunicacion**: A2A para coordinacion entre agentes

## Que Se Ha Cambiado

1. **Dominio**: De juridico a oposiciones
2. **Interfaz**: De gateway telefonico a CLI + Dashboard web
3. **Alcance**: Sistema personal vs multi-tenant

## Nota

Estos documentos se mantienen como referencia historica y para entender decisiones de diseno originales. Para la documentacion actual del proyecto, ver los archivos numerados en `docs/`.

---

*Proyecto original: OPENCLAW-city (2024-2025)*
*Proyecto actual: oposiciones-system (2026)*
