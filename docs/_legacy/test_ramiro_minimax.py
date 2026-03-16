#!/usr/bin/env python3
"""Test Ramiro con MiniMax"""
import requests
import json

# Leer token
with open('/home/openclaw/.openclaw/.env') as f:
    for line in f:
        if 'OPENCLAW_GATEWAY_TOKEN' in line:
            token = line.split('=')[1].strip().strip('"')
            break

print("=== HABLANDO CON RAMIRO ===\n")
print(f"Token: {token[:20]}...\n")

# Enviar mensaje
response = requests.post(
    'http://127.0.0.1:18789/api/chat',
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    },
    json={
        'message': 'Hola Ramiro, ¿qué modelo LLM estás usando?',
        'session': 'test'
    },
    timeout=30
)

print("Respuesta de Ramiro:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
