# Bot Telegram - Ramiro

**Ultima actualizacion:** 2025-03-16
**Version:** 1.0.0
**Origen:** OPENCLAW-city (Produccion)

---

## Indice

1. [Estado Actual](#estado-actual)
2. [Comandos Existentes](#comandos-existentes)
3. [Arquitectura del Bot](#arquitectura-del-bot)
4. [Extensiones para Oposiciones](#extensiones-para-oposiciones)
5. [Integracion con Sistema](#integracion-con-sistema)
6. [Flujos de Usuario](#flujos-de-usuario)
7. [Configuracion y Deploy](#configuracion-y-deploy)

---

## Estado Actual

### Informacion del Bot

| Atributo | Valor |
|----------|-------|
| **Nombre** | Ramiro |
| **Username** | @ramiro_openclaw_bot |
| **Path Original** | `/opt/openclaw-memory/ramiro_bot.py` |
| **Estado** | Activo en produccion |
| **Framework** | python-telegram-bot |
| **API LLM** | MiniMax M2.5 |

### Capactidades Actuales

```
+---------------------------+
|   RAMIRO BOT (Actual)     |
+---------------------------+
| - Chat basico con IA      |
| - Busqueda en conocimiento|
| - Historial de conversacion|
| - Exportar datos          |
| - Status del sistema      |
+---------------------------+
```

---

## Comandos Existentes

### Comandos Basicos

| Comando | Descripcion | Estado |
|---------|-------------|--------|
| `/start` | Inicia el bot y muestra bienvenida | Activo |
| `/help` | Muestra lista de comandos | Activo |
| `/status` | Muestra estado del sistema | Activo |

### Comandos de Conocimiento

| Comando | Descripcion | Estado |
|---------|-------------|--------|
| `/search <query>` | Busca en base de conocimiento | Activo |
| `/ask <pregunta>` | Pregunta directa a la IA | Activo |

### Comandos de Sesion

| Comando | Descripcion | Estado |
|---------|-------------|--------|
| `/history` | Muestra historial de conversacion | Activo |
| `/clear` | Limpia el contexto de la sesion | Activo |
| `/export` | Exporta datos del usuario | Activo |

### Implementacion Actual

```python
# /opt/openclaw-memory/ramiro_bot.py (simplificado)

import telebot
from config import Config

bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message,
        "Hola! Soy Ramiro, tu asistente de OpenClaw.\n"
        "Usa /help para ver los comandos disponibles."
    )

@bot.message_handler(commands=['help'])
def handle_help(message):
    help_text = """
    Comandos disponibles:
    /start - Iniciar bot
    /help - Mostrar esta ayuda
    /search <query> - Buscar en conocimiento
    /ask <pregunta> - Preguntar a IA
    /status - Estado del sistema
    /history - Historial
    /clear - Limpiar contexto
    /export - Exportar datos
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['search'])
def handle_search(message):
    query = message.text.replace('/search', '').strip()
    if not query:
        bot.reply_to(message, "Uso: /search <termino>")
        return

    # Usar RAG Store para buscar
    results = rag_store.search(query)
    response = format_search_results(results)
    bot.reply_to(message, response)

@bot.message_handler(commands=['ask'])
def handle_ask(message):
    question = message.text.replace('/ask', '').strip()
    if not question:
        bot.reply_to(message, "Uso: /ask <pregunta>")
        return

    # Usar MiniMax para responder
    response = minimax_client.chat(question)
    bot.reply_to(message, response)

# ... mas handlers
```

---

## Arquitectura del Bot

### Componentes

```
+============================================================================+
|                         RAMIRO BOT ARCHITECTURE                             |
+============================================================================+
                                       |
           +---------------------------+---------------------------+
           |                           |                           |
           v                           v                           v
+----------------------+    +----------------------+    +----------------------+
|   TELEGRAM API       |    |   MESSAGE HANDLER    |    |   CONTEXT MANAGER    |
|                      |    |                      |    |                      |
| - Recibe mensajes    |    | - Procesa comandos   |    | - Mantiene sesion    |
| - Envía respuestas   |    | - Delega a servicios |    | - Historial usuario  |
| - Webhook/Polling    |    | - Formatea output    |    | - Memoria conversacion|
+----------------------+    +----------------------+    +----------------------+
           |                           |                           |
           +---------------------------+---------------------------+
                                       |
                                       v
+============================================================================+
|                         SERVICIOS INTEGRADOS                                |
|  +---------------------------+  +---------------------------+              |
|  |   RAG Store               |  |   MiniMax M2.5            |              |
|  |   Busqueda semantica      |  |   Generacion de texto     |              |
|  +---------------------------+  +---------------------------+              |
|  +---------------------------+  +---------------------------+              |
|  |   Memory Store            |  |   Security Pipeline       |              |
|  |   Contexto persistente    |  |   Validacion inputs       |              |
|  +---------------------------+  +---------------------------+              |
+============================================================================+
```

### Flujo de Mensaje

```
Usuario envia mensaje
        |
        v
+------------------+
| Telegram API     |
| Recibe update    |
+------------------+
        |
        v
+------------------+
| Message Handler  |
| Identifica tipo  |
| - Comando?       |
| - Pregunta?      |
| - Feedback?      |
+------------------+
        |
        +-----> Si es comando -----> Ejecuta handler especifico
        |
        +-----> Si es pregunta -----> Procesa con IA
        |
        v
+------------------+
| Security Pipeline|
| Valida input     |
| Sanitiza texto   |
+------------------+
        |
        v
+------------------+
| Servicio Apropiado|
| - RAG Store      |
| - MiniMax API    |
| - Memory Store   |
+------------------+
        |
        v
+------------------+
| Response Builder |
| Formatea respuesta|
| Anade botones    |
+------------------+
        |
        v
+------------------+
| Telegram API     |
| Envia mensaje    |
+------------------+
```

---

## Extensiones para Oposiciones

### Nuevos Comandos

| Comando | Descripcion | Prioridad |
|---------|-------------|-----------|
| `/review [deck]` | Iniciar sesion de repaso de flashcards | Alta |
| `/test [tema]` | Generar test rapido del tema | Alta |
| `/progress` | Ver estadisticas de progreso | Alta |
| `/deck` | Gestionar decks de flashcards | Media |
| `/weak` | Ver areas debiles detectadas | Media |
| `/plan` | Ver plan de estudio semanal | Media |
| `/cards [n]` | Ver N flashcards pendientes | Media |
| `/stats` | Estadisticas detalladas | Baja |

### Comando: /review

```python
@bot.message_handler(commands=['review'])
def handle_review(message):
    """
    Inicia sesion de repaso de flashcards.

    Uso:
      /review          - Repasa deck por defecto
      /review tema5    - Repasa deck "tema5"
    """
    args = message.text.replace('/review', '').strip()
    deck_name = args if args else "default"

    # Obtener flashcards debidas
    due_cards = flashcard_service.get_due_cards(
        user_id=message.chat.id,
        deck_name=deck_name,
        limit=10
    )

    if not due_cards:
        bot.reply_to(message, "No tienes flashcards pendientes de repaso.")
        return

    # Guardar estado de sesion
    context_manager.start_review_session(
        user_id=message.chat.id,
        cards=due_cards
    )

    # Mostrar primera flashcard
    show_flashcard(message.chat.id, due_cards[0])

def show_flashcard(chat_id, card):
    """Muestra una flashcard con botones de rating"""
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton("0", callback_data=f"rate_0_{card.id}"),
        telebot.types.InlineKeyboardButton("1", callback_data=f"rate_1_{card.id}"),
        telebot.types.InlineKeyboardButton("2", callback_data=f"rate_2_{card.id}"),
        telebot.types.InlineKeyboardButton("3", callback_data=f"rate_3_{card.id}"),
        telebot.types.InlineKeyboardButton("4", callback_data=f"rate_4_{card.id}"),
        telebot.types.InlineKeyboardButton("5", callback_data=f"rate_5_{card.id}"),
    )

    bot.send_message(
        chat_id,
        f"*PREGUNTA:*\n{card.front}",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith('rate_'))
def handle_rating(callback):
    """Procesa el rating de una flashcard"""
    _, rating, card_id = callback.data.split('_')
    rating = int(rating)

    # Actualizar SM-2
    flashcard_service.process_review(card_id, rating)

    # Siguiente flashcard o terminar
    next_card = context_manager.get_next_card(callback.message.chat.id)
    if next_card:
        show_flashcard(callback.message.chat.id, next_card)
    else:
        bot.send_message(
            callback.message.chat.id,
            "Sesion de repaso completada!"
        )
```

### Comando: /test

```python
@bot.message_handler(commands=['test'])
def handle_test(message):
    """
    Genera un test rapido del tema especificado.

    Uso:
      /test           - Test de todos los temas (5 preguntas)
      /test 5         - Test del Tema 5 (5 preguntas)
      /test 5 10      - Test del Tema 5 (10 preguntas)
    """
    args = message.text.replace('/test', '').strip().split()
    tema = int(args[0]) if args else None
    num_questions = int(args[1]) if len(args) > 1 else 5

    bot.send_message(message.chat.id, "Generando test...")

    # Generar test
    test = test_service.generate_test(
        tema=tema,
        num_questions=num_questions
    )

    # Guardar sesion de test
    session_id = test_service.create_session(
        user_id=message.chat.id,
        test_id=test.id
    )

    # Mostrar primera pregunta
    show_question(message.chat.id, test.questions[0], session_id)

def show_question(chat_id, question, session_id):
    """Muestra una pregunta de test con opciones"""
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i, option in enumerate(question.options):
        keyboard.add(
            telebot.types.InlineKeyboardButton(
                f"{chr(65+i)}. {option}",
                callback_data=f"answer_{session_id}_{question.id}_{i}"
            )
        )

    text = f"*Pregunta {question.number}/{question.total}:*\n{question.text}"
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda c: c.data.startswith('answer_'))
def handle_answer(callback):
    """Procesa la respuesta a una pregunta"""
    _, session_id, question_id, answer_index = callback.data.split('_')
    answer_index = int(answer_index)

    # Registrar respuesta
    result = test_service.submit_answer(
        session_id=session_id,
        question_id=question_id,
        answer_index=answer_index
    )

    # Mostrar feedback
    if result.correct:
        feedback = "Correcto!"
    else:
        feedback = f"Incorrecto. La respuesta correcta era: {result.correct_answer}"

    bot.answer_callback_query(callback.id, feedback)

    # Siguiente pregunta o resultados
    next_question = test_service.get_next_question(session_id)
    if next_question:
        show_question(callback.message.chat.id, next_question, session_id)
    else:
        show_test_results(callback.message.chat.id, session_id)

def show_test_results(chat_id, session_id):
    """Muestra los resultados del test"""
    results = test_service.get_results(session_id)

    text = f"""
*RESULTADOS DEL TEST*

Preguntas: {results.total}
Correctas: {results.correct}
Incorrectas: {results.incorrect}
Puntuacion: {results.score:.1f}/10

Areas debiles detectadas:
{chr(10).join('- ' + area for area in results.weak_areas)}
"""
    bot.send_message(chat_id, text, parse_mode="Markdown")
```

### Comando: /progress

```python
@bot.message_handler(commands=['progress'])
def handle_progress(message):
    """Muestra estadisticas de progreso del usuario"""
    stats = analytics_service.get_user_stats(message.chat.id)

    text = f"""
*TU PROGRESO*

*Flashcards:*
- Total: {stats.flashcards_total}
- Aprendidas: {stats.flashcards_learned}
- Pendientes: {stats.flashcards_due}
- Faciles: {stats.flashcards_easy}

*Tests:*
- Completados: {stats.tests_completed}
- Puntuacion media: {stats.test_avg_score:.1f}/10

*Areas debiles:*
{chr(10).join('- ' + area for area in stats.weak_areas[:5])}

*Racha actual:* {stats.streak} dias
"""
    bot.send_message(message.chat.id, text, parse_mode="Markdown")
```

### Comando: /weak

```python
@bot.message_handler(commands=['weak'])
def handle_weak(message):
    """Muestra areas debiles detectadas"""
    weak_areas = analytics_service.get_weak_areas(message.chat.id)

    if not weak_areas:
        bot.reply_to(message, "No hay areas debiles detectadas aun.")
        return

    text = "*AREAS DEBILES DETECTADAS*\n\n"
    for area in weak_areas:
        text += f"*{area.nombre}*\n"
        text += f"  - Score: {area.score:.1f}/10\n"
        text += f"  - Flashcards afectadas: {area.cards_affected}\n"
        text += f"  - Tests afectados: {area.tests_affected}\n\n"

    # Boton para generar plan de mejora
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            "Generar plan de mejora",
            callback_data=f"improve_plan"
        )
    )

    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=keyboard)
```

---

## Integracion con Sistema

### Servicios Utilizados

```python
# servicios.py - Inyeccion de dependencias

class BotServices:
    """Servicios disponibles para el bot"""

    def __init__(self):
        # Heredados de OPENCLAW-city
        self.rag_store = RAGStore("data/temario.db")
        self.memory_store = MemoryStore("data/oposiciones.db")
        self.security = SecurityPipeline()

        # Nuevos para Oposiciones
        self.flashcard_service = FlashcardService()
        self.test_service = TestService()
        self.analytics_service = AnalyticsService()

        # IA
        self.minimax = MiniMaxClient()

# Inyectar en handlers
services = BotServices()
```

### Integracion con Concilio

```python
class BotConcilioIntegration:
    """Integra el bot con el sistema de agentes"""

    def __init__(self):
        self.director = DirectorAgent()
        self.ejecutor = EjecutorAgent()
        self.archivador = ArchivadorAgent()

    async def process_complex_query(self, query: str, user_id: int) -> str:
        """Procesa consultas complejas usando el Concilio"""

        # 1. Director planifica
        plan = await self.director.analyze(query)

        # 2. Ejecutor implementa
        result = await self.ejecutor.execute(plan)

        # 3. Archivador registra
        await self.archivador.save(user_id, query, result)

        return result.response

# Uso en handler
@bot.message_handler(func=lambda m: True)
def handle_complex(message):
    """Handler para mensajes complejos"""
    # Determinar si necesita Concilio
    if is_complex_query(message.text):
        response = concilio.process_complex_query(
            message.text,
            message.chat.id
        )
    else:
        response = services.minimax.chat(message.text)

    bot.reply_to(message, response)
```

---

## Flujos de Usuario

### Flujo: Repaso de Flashcards

```
Usuario: /review tema5
    |
    v
Bot: "Iniciando sesion de repaso del deck 'tema5'..."
Bot: "Tienes 12 flashcards pendientes."
    |
    v
Bot: *PREGUNTA:*
     "Que es el silencio administrativo?"
     [0] [1] [2] [3] [4] [5]
    |
    v
Usuario: [3] (click en boton)
    |
    v
Bot: "Guardado. Siguiente..."
    |
    v
Bot: *PREGUNTA:*
     "Cuales son los plazos del silencio administrativo?"
     [0] [1] [2] [3] [4] [5]
    |
    v
... (continua hasta completar)
    |
    v
Bot: "*SESION COMPLETADA*"
     "Repasaste 12 flashcards"
     "Facil: 5 | Bueno: 4 | Dificil: 3"
     "Siguiente repaso: manana"
```

### Flujo: Test Rapido

```
Usuario: /test 5
    |
    v
Bot: "Generando test del Tema 5..."
    |
    v
Bot: *Pregunta 1/5:*
     "Cual es el plazo maximo para resolver un procedimiento ordinario?"
     A. 1 mes
     B. 3 meses
     C. 6 meses
     D. 12 meses
    |
    v
Usuario: [B. 3 meses] (click)
    |
    v
Bot: "Correcto!"
    |
    v
Bot: *Pregunta 2/5:*
     "Que tipo de silencio se produce en un procedimiento de autorizacion?"
     A. Positivo
     B. Negativo
     ...
    |
    v
... (continua)
    |
    v
Bot: "*RESULTADOS*"
     "Correctas: 4/5"
     "Puntuacion: 8.0/10"
     "Area debil: Plazos"
     "[Ver explicacion] [Nuevo test]"
```

### Flujo: Consulta de Progreso

```
Usuario: /progress
    |
    v
Bot: *TU PROGRESO*

     *Flashcards:*
     - Total: 250
     - Aprendidas: 180
     - Pendientes: 25
     - Faciles: 120

     *Tests:*
     - Completados: 15
     - Puntuacion media: 7.5/10

     *Areas debiles:*
     - Tema 5: Procedimiento (score: 5.2)
     - Tema 12: Contratos (score: 6.1)

     *Racha:* 7 dias

     [Ver detalles] [Generar plan]
```

---

## Configuracion y Deploy

### Variables de Entorno

```bash
# .env

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here

# APIs
MINIMAX_API_KEY=your_minimax_key
MINIMAX_GROUP_ID=your_group_id
MISTRAL_API_KEY=your_mistral_key

# Database
TEMARIO_DB=data/temario.db
OPOSICIONES_DB=data/oposiciones.db

# Bot Settings
BOT_POLLING_INTERVAL=1
BOT_MAX_MESSAGES_PER_MINUTE=30
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  telegram-bot:
    build:
      context: .
      dockerfile: Dockerfile.bot
    container_name: oposiciones-telegram
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - MINIMAX_API_KEY=${MINIMAX_API_KEY}
      - MINIMAX_GROUP_ID=${MINIMAX_GROUP_ID}
      - MISTRAL_API_KEY=${MISTRAL_API_KEY}
    volumes:
      - ./02-DATA/databases:/app/data
      - ./logs:/app/logs
    depends_on:
      - temario-service
    networks:
      - oposiciones-network
    ports:
      - "10601:10601"  # Puerto para webhook (opcional)
```

### Dockerfile

```dockerfile
# Dockerfile.bot
FROM python:3.11-slim

WORKDIR /app

# Dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Codigo
COPY 06-INTERFACE/telegram/ ./bot/
COPY 03-SERVICES/ ./services/
COPY 00-FOUNDATION/ ./config/

# Run
CMD ["python", "bot/oposiciones_bot.py"]
```

### Comandos de Deploy

```bash
# Desarrollo
python 06-INTERFACE/telegram/oposiciones_bot.py

# Docker
docker-compose up -d telegram-bot

# Ver logs
docker-compose logs -f telegram-bot

# Reiniciar
docker-compose restart telegram-bot
```

---

## Migracion desde Ramiro Original

### Pasos

1. **Copiar base**
   ```bash
   cp /opt/openclaw-memory/ramiro_bot.py 06-INTERFACE/telegram/base_ramiro.py
   ```

2. **Crear nuevo bot**
   ```bash
   cp 06-INTERFACE/telegram/base_ramiro.py 06-INTERFACE/telegram/oposiciones_bot.py
   ```

3. **Anadir imports**
   ```python
   # Nuevos imports
   from services.flashcard_service import FlashcardService
   from services.test_service import TestService
   from services.analytics_service import AnalyticsService
   ```

4. **Anadir handlers** (ver secciones anteriores)

5. **Actualizar config**
   ```python
   # config.py - anadir
   TEMARIO_DB = "data/temario.db"
   OPOSICIONES_DB = "data/oposiciones.db"
   ```

6. **Testear**
   ```bash
   python 06-INTERFACE/telegram/oposiciones_bot.py
   ```

7. **Deploy**
   ```bash
   docker-compose up -d telegram-bot
   ```

---

**Fin del documento de Bot Telegram Ramiro (v1.0.0)**
