# 👤 CONTEXTO, OBJETIVOS E INFRAESTRUCTURA

## 1. Perfil del Usuario "El Jefe"
- **Hostelería (20 años):** Director, formador, restaurantes Michelin. Experto barista y coctelería.
- **IT:** Service Desk L1, estudiante Ingeniería Informática. Conocimiento arquitectónico (Docker, YAML, APIs), pero delega el código rutinario en el sistema.
- **Meta Crítica:** Oposiciones FP Hostelería (Junio). Entregables: Programación, Unidad Didáctica, Oral, Práctica.
- **Meta Secundaria:** Certificación Microsoft IA-102. Inglés C1.

## 2. Topología Física y Hardware

| Dispositivo | Especificaciones | Rol Asignado |
| :--- | :--- | :--- |
| **Mac Mini M1** | 16GB RAM, 256GB + **4TB NVMe Externo** | Servidor de JartOS. Aloja Docker, SQLite (`temario.db`), RAG y el Guardián. |
| **MacBook Pro M1 Max**| 32GB RAM, 1TB SSD | Cliente Multimodal. Interface principal. |
| **Logitech Brio 4K** | Webcam Ultra-HD | Input de Video para el "Coach Oral". |
| **Mikro Anker 360°** | Micrófono de Conferencia | Input de Audio (LiveKit/STT) para simulacros. |
| **Xiaomi Pad 5 / S9 FE+**| Tablets Android | Dashboards (Home Assistant / JartOS Web). |

## 3. Topología Lógica (El "Por Qué")
El sistema debe procesar PDFs crudos (9 autores de temario), leyes del BOE y currículos TODOFP. El usuario no puede perder tiempo buscando el documento X; necesita que JartOS le diga "El autor A dice Y, pero el BOE dice Z" de forma instantánea.