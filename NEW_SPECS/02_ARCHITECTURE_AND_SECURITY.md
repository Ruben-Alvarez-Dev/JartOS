# 🏗️ ARQUITECTURA TÉCNICA Y SEGURIDAD

## 2. Gestión de Secretos (1Password Vault)
JartOS no almacena secretos en texto plano ni en archivos `.env` locales en producción.
- **Vault:** Se utiliza **1Password** como gestor de secretos oficial.
- **Inyección:** Los secretos se inyectan en tiempo de ejecución mediante la CLI de 1Password (`op`).
- **Plantilla:** `TIER_02_SECURITY/secrets.template.env` define el mapeo entre las variables de entorno y las referencias del Vault.

### Comando de ejecución en producción:
```bash
op run --env-file=TIER_02_SECURITY/secrets.template.env -- docker-compose up -d
```

## 3. La Jerarquía de los 12 TIERs (Rutas Reales)
El código reside en la raíz de `/Users/ruben/JartOS/`. La ruta antigua `src/` está deprecada.
- `TIER_00_FOUNDATION/`: Scripts base, variables `.env`.
- `TIER_01_ACCESS/`: Integraciones de red pura (Zadarma).
- `TIER_02_SECURITY/`: Contiene el binario/script de **El Guardián**.
- `TIER_03_AGENTS/`: Servidores FastMCP, `maestro.py`, `concilio.py`.
- `TIER_04_INTERFACE/`: Aplicación Web FastAPI (`/web/app.py`).
- `TIER_05_INGEST/`: Watchdogs de INBOX y LAB.
- `TIER_06_STORAGE/`: Enlaces a volúmenes físicos de datos.
- `TIER_07_FRAMEWORKS/`: -
- `TIER_08_WORKFLOWS/`: -
- `TIER_09_KNOWLEDGE/`: Lógica central (Temario parser, chunker, ai models).
- `TIER_10_USER_APPS/`: Apps como Flashcards y Tests.
- `TIER_11_CONTROL/`: `daemon.py` y `tests/` (Suite de Pytest).

## 2. El "Anillo Guardián" (Seguridad Perimetral)
JartOS es "Peligroso" por diseño si es autónomo. Se mitiga así:
- **JartOS Core:** Se ejecuta en una red Docker `internal: true`.
- **El Guardián (`TIER_02_SECURITY`):** Es una API REST ligera levantada **en el Host** (Mac Mini, expuesta solo a `localhost`).
  - Endpoint real: `POST http://127.0.0.1:8080/propose_action`
  - Solo el Guardián tiene el token de Home Assistant. Si JartOS propone, Guardián valida y ejecuta.

## 3. Especificación Docker Compose Base
```yaml
version: '3.8'
services:
  jartos-core:
    build: .
    volumes:
      - /Volumes/TU_NVME_4TB/data:/app/data
    networks:
      - jartos_internal
    environment:
      - PYTHONPATH=/app
  
  # Guardián corre en el host, no en docker-compose, o usa red 'host'.

networks:
  jartos_internal:
    internal: true
```