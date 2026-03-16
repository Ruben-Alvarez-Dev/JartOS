# 📚 INGESTA (INBOX/LAB) Y FLUJO DE DATOS (RAG)

El conocimiento se almacena usando SQLite como Base Vectorial local mediante la tabla `temario_documents` y `temario_chunks`.

## 1. Esquema Real de Base de Datos (`temario.db`)
El módulo `TIER_09_KNOWLEDGE.temario.store` define el esquema en producción:
- **Tabla `temario_documents`**:
  - `id` (TEXT, PK)
  - `title` (TEXT)
  - `author` (TEXT)
  - `created_at` (TEXT)
  - `metadata` (TEXT, JSON)
- **Tabla `temario_chunks`**:
  - `id` (TEXT, PK)
  - `document_id` (TEXT, FK)
  - `content` (TEXT)
  - `metadata` (TEXT, JSON)
  - `embedding` (TEXT) - *(Almacena el vector JSON convertido)*

## 2. Pipelines Físicos de Ingesta

### Directorio `/data/INBOX` (Verdad Oficial)
Todo lo que el usuario mueve aquí es oficial (PDFs del BOE, Temario de autores oficiales).
1. Un script (`TIER_05_INGEST/watchdog.py`) detecta el archivo.
2. Llama a `DocumentParser` (`TIER_09_KNOWLEDGE/temario/parser.py`).
3. Llama a `TextChunker` para dividir el texto.
4. Llama a `MistralEmbedder` (o modelo configurado) para vectorizar.
5. Llama a `TemarioStore` y lo guarda en `temario.db`.

### Directorio `/data/LAB` (Zona de Discusión)
Apuntes o información de dudosa procedencia.
1. El archivo es detectado.
2. Se procesa el texto, pero **no se inserta el embedding**.
3. Se envía una notificación/alerta al usuario (vía Web UI o Telegram).
4. Un Agente Especialista genera un resumen: *"¿Integrar estos apuntes sobre vinos en el Tema 12?"*.
5. Tras confirmación explícita (Endpoint `/api/lab/approve`), se vectoriza e inserta en la DB.