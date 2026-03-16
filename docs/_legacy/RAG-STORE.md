# 🔍 RAG Store

**Búsqueda Semántica con Embeddings**

**Última actualización:** 2026-03-10  
**Versión:** 2026.3.10

---

## 📋 Índice

1. [Descripción General](#1-descripción-general)
2. [Embeddings (Mistral API)](#2-embeddings-mistral-api)
3. [Implementación de Búsqueda Vectorial](#3-implementación-de-búsqueda-vectorial)
4. [Similitud Coseno](#4-similitud-coseno)
5. [Fallback a Búsqueda de Texto](#5-fallback-a-búsqueda-de-texto)
6. [API Reference](#6-api-reference)

---

## 1. Descripción General

El **RAG Store** (Retrieval-Augmented Generation) permite búsqueda semántica de información usando embeddings vectoriales.

**Características:**
- ✅ Embeddings con Mistral API (1024 dimensiones)
- ✅ Búsqueda por similitud coseno
- ✅ Fallback a búsqueda por texto si no hay embedding
- ✅ Integrado con Memory Store
- ✅ Por usuario y categoría

**Ubicación:** `/opt/openclaw-memory/rag_store.py`

---

## 2. Embeddings (Mistral API)

### Configuración

```python
EMBEDDING_MODE = "api"  # "api" o "local"
EMBEDDING_API_URL = "https://api.mistral.ai/v1/embeddings"
EMBEDDING_MODEL = "mistral-embed"
EMBEDDING_DIMENSIONS = 1024
```

### Calcular Embedding

```python
import requests
import json

def get_mistral_api_key():
    """Obtener API key del .env"""
    with open("/home/openclaw/.openclaw/.env", 'r') as f:
        for line in f:
            if line.startswith('OPENCLAW_MISTRAL_API_KEY='):
                return line.split('=', 1)[1].strip().strip('"')
    return ""

def compute_embedding_api(text: str) -> list:
    """Calcular embedding usando Mistral API"""
    api_key = get_mistral_api_key()
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "model": "mistral-embed",
        "input": text,
        "encoding_format": "float"
    }
    
    response = requests.post(
        "https://api.mistral.ai/v1/embeddings",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['data'][0]['embedding']  # Lista de 1024 floats
    
    return None
```

### Ejemplo de Embedding

```python
text = "El usuario se llama Rubén y es developer"
embedding = compute_embedding_api(text)

# Resultado (simplificado):
# [0.0123, -0.0456, 0.0789, ..., -0.0321]  # 1024 dimensiones
```

### Costos

| Modelo | Precio por 1K tokens | Dimensiones |
|--------|---------------------|-------------|
| mistral-embed | $0.0001 | 1024 |

**Ejemplo:**
- 1000 memorias × 50 tokens cada una = 50K tokens
- Costo: 50 × $0.0001 = $0.005 (medio centavo)

---

## 3. Implementación de Búsqueda Vectorial

### Añadir Contenido a RAG

```python
def add_to_rag(user_id: str, category: str, content: str, 
               metadata: dict = None, compute_embed: bool = True):
    """Añadir contenido a RAG"""
    
    # Calcular embedding (opcional)
    embedding = None
    if compute_embed:
        embedding = compute_embedding_api(content)
    
    # Guardar en long_term_memory (Memory Store)
    memory.add_memory(
        user_id=user_id,
        category=category,
        fact_type="rag_content",
        content=content,
        embedding=embedding,
        confidence=1.0
    )
    
    return True
```

### Búsqueda por Similitud

```python
def search_rag(user_id: str, query: str, category: str = None, 
               limit: int = 10, threshold: float = 0.5):
    """Buscar contenido similar"""
    
    # 1. Calcular embedding del query
    query_embedding = compute_embedding_api(query)
    if not query_embedding:
        return search_rag_text(user_id, query, category, limit)  # Fallback
    
    # 2. Obtener memorias del usuario
    memories = memory.get_memories(user_id, category)
    
    # 3. Calcular similitud con cada memoria
    results = []
    for mem in memories:
        if mem.get('embedding'):
            similarity = cosine_similarity(query_embedding, mem['embedding'])
            
            if similarity >= threshold:
                results.append({
                    'memory': mem,
                    'similarity': similarity
                })
    
    # 4. Ordenar por similitud (descendente)
    results.sort(key=lambda x: x['similarity'], reverse=True)
    
    # 5. Retornar top-N
    return results[:limit]
```

---

## 4. Similitud Coseno

### Fórmula

```
similarity = cos(θ) = (A · B) / (||A|| × ||B||)
```

Donde:
- `A · B` = producto punto de los vectores
- `||A||` = norma (magnitud) del vector A
- `||B||` = norma (magnitud) del vector B

### Implementación

```python
import math

def cosine_similarity(a: list, b: list) -> float:
    """Calcular similitud coseno entre dos vectores"""
    
    if not a or not b:
        return 0.0
    
    # Producto punto
    dot_product = sum(x * y for x, y in zip(a, b))
    
    # Normas
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    # Similitud
    return dot_product / (norm_a * norm_b)
```

### Interpretación

| Valor | Interpretación |
|-------|----------------|
| 1.0 | Idénticos (mismo vector) |
| 0.8 - 0.99 | Muy similares |
| 0.5 - 0.79 | Moderadamente similares |
| 0.3 - 0.49 | Ligeramente similares |
| 0.0 - 0.29 | No similares |
| -1.0 | Opuestos |

### Ejemplo

```python
# Dos vectores de ejemplo (simplificados a 3D)
a = [0.5, 0.3, 0.8]
b = [0.6, 0.2, 0.7]

similarity = cosine_similarity(a, b)
print(f"Similitud: {similarity:.3f}")  # Output: 0.987

# En la práctica (1024 dimensiones):
# query: "¿Cómo se llama el usuario?"
# memoria: "El usuario se llama Rubén"
# similitud: 0.85 (alta)
```

---

## 5. Fallback a Búsqueda de Texto

### Cuándo Usar Fallback

- Embedding API no disponible
- Error de cálculo de embedding
- Búsqueda rápida sin costo

### Implementación

```python
def search_rag_text(user_id: str, query: str, category: str = None, limit: int = 10):
    """Búsqueda por texto (fallback)"""
    
    # Obtener memorias
    memories = memory.get_memories(user_id, category)
    
    # Búsqueda por texto simple (case-insensitive)
    query_lower = query.lower()
    results = []
    
    for mem in memories:
        content_lower = mem['content'].lower()
        
        # Contar palabras del query que aparecen en el contenido
        matches = sum(1 for word in query_lower.split() if word in content_lower)
        
        if matches > 0:
            results.append({
                'memory': mem,
                'similarity': matches / len(query_lower.split())  # Score simple
            })
    
    # Ordenar por score
    results.sort(key=lambda x: x['similarity'], reverse=True)
    
    return results[:limit]
```

### Comparación

| Método | Ventajas | Desventajas |
|--------|----------|-------------|
| **Embeddings** | Búsqueda semántica, entiende significado | Costo API, latencia |
| **Texto** | Gratis, rápido | Solo matching literal, no semántico |

---

## 6. API Reference

### Funciones Principales

#### add_to_rag

```python
from rag_store import add_to_rag

# Añadir contenido
add_to_rag(
    user_id="telegram:795606301",
    category="code",
    content="def hello(): print('Hello World')",
    metadata={"language": "python"},
    compute_embed=True  # Calcular embedding
)
```

#### search_rag

```python
from rag_store import search_rag

# Buscar contenido similar
results = search_rag(
    user_id="telegram:795606301",
    query="función que imprime saludo",
    category="code",
    limit=10,
    threshold=0.5  # Mínima similitud
)

# Output:
# [
#   {
#     'memory': {...},
#     'similarity': 0.85
#   },
#   ...
# ]
```

#### get_rag_stats

```python
from rag_store import get_rag_stats

# Obtener estadísticas de RAG
stats = get_rag_stats("telegram:795606301")

# Output:
# {
#   "total": 50,
#   "with_embedding": 45,
#   "categories": {
#     "personal": 10,
#     "code": 20,
#     "facts": 15
#   }
# }
```

#### index_conversation

```python
from rag_store import index_conversation

# Indexar conversación completa en RAG
index_conversation(
    user_id="telegram:795606301",
    channel="telegram",
    category="conversation"
)
```

---

## 7. Casos de Uso

### 7.1 Recordar Información del Usuario

```python
# Usuario dice: "Trabajo con Python y Django"
add_to_rag(
    user_id="telegram:795606301",
    category="personal",
    content="Trabaja con Python y Django",
    compute_embed=True
)

# Más tarde, usuario pregunta: "¿Qué lenguajes uso?"
results = search_rag(
    user_id="telegram:795606301",
    query="lenguajes de programación que usa"
)

# Resultado: "Trabaja con Python y Django" (similitud: 0.82)
```

### 7.2 Búsqueda de Código

```python
# Guardar snippet de código
add_to_rag(
    user_id="telegram:795606301",
    category="code",
    content="def connect_db(): return sqlite3.connect('app.db')",
    metadata={"language": "python"}
)

# Buscar código similar
results = search_rag(
    user_id="telegram:795606301",
    query="conexión a base de datos SQLite"
)

# Resultado: Snippet de connect_db (similitud: 0.88)
```

### 7.3 Contexto para LLM

```python
# Antes de enviar a Mistral, buscar contexto relevante
user_query = "¿Cómo configuro el gateway?"

# Buscar información relevante
context = search_rag(
    user_id="telegram:795606301",
    query=user_query,
    limit=5
)

# Construir prompt con contexto
context_text = "\n".join([r['memory']['content'] for r in context])

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "system", "content": f"Contexto relevante:\n{context_text}"},
    {"role": "user", "content": user_query}
]

# Enviar a Mistral
response = call_mistral(messages)
```

---

## 8. Optimización

### Threshold de Similitud

| Caso de Uso | Threshold Recomendado |
|-------------|----------------------|
| Búsqueda precisa | 0.7 - 0.8 |
| Búsqueda general | 0.5 - 0.6 |
| Búsqueda exploratoria | 0.3 - 0.4 |

### Batch de Embeddings

```python
# Calcular múltiples embeddings de una vez
def compute_embeddings_batch(texts: list) -> list:
    """Calcular embeddings en batch (más eficiente)"""
    api_key = get_mistral_api_key()
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "model": "mistral-embed",
        "input": texts,  # Lista de textos
        "encoding_format": "float"
    }
    
    response = requests.post(
        "https://api.mistral.ai/v1/embeddings",
        headers=headers,
        json=payload,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        return [item['embedding'] for item in result['data']]
    
    return []
```

---

## 9. Troubleshooting

### Error de API

```
Error computing embedding: 401 Unauthorized
```

**Solución:**
1. Verificar API key en `.env`
2. Verificar key no ha expirado
3. Regenerar key en https://console.mistral.ai

### Embedding muy lento

**Causa:** Llamadas API individuales para cada memoria

**Solución:**
```python
# Usar batch en lugar de individual
embeddings = compute_embeddings_batch(texts)  # 100 textos en 1 llamada
```

### Resultados no relevantes

**Causa:** Threshold muy bajo

**Solución:**
```python
# Aumentar threshold
results = search_rag(query, threshold=0.7)  # En lugar de 0.5
```

---

**Fin del documento del RAG Store**
