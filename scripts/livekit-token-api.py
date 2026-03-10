#!/usr/bin/env python3
"""
LiveKit Token Generator API - OpenClaw-City
Simple API para generar tokens de acceso para el web client
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from livekit.api import AccessToken

# Configuración
LIVEKIT_API_KEY = "openclaw-54990a102ce72a4e"
LIVEKIT_API_SECRET = "YOUR_LIVEKIT_SECRET"

class TokenHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/token':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            room_name = data.get('room', 'openclaw-test')
            participant_name = data.get('name', 'Test User')
            
            # Generar token
            token = (
                AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
                .with_identity(f"user-{participant_name.lower().replace(' ', '-')}")
                .with_name(participant_name)
                .to_jwt()
            )
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {'token': token, 'room': room_name}
            self.wfile.write(json.dumps(response).encode())
            
            print(f"Token generado para {participant_name} en room {room_name}")
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[Token API] {args[0]}")

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8444), TokenHandler)
    print("LiveKit Token API running on http://127.0.0.1:8444")
    server.serve_forever()
