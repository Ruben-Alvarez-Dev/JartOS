#!/usr/bin/env python3
"""
A2A Endpoint Server for OpenClaw Gateway (using http.server - no dependencies)
Intercepts A2A communications and processes them.

Date: 2026-03-10
"""

import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

# Configuration
A2A_PORT = 18790
LOG_DIR = "/var/log/openclaw/a2a"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/a2a_endpoint.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# A2A Session State
a2a_session = {
    "established": False,
    "orchestrator": None,
    "established_at": None,
    "commands": [],
    "messages_processed": 0
}

commands_queue = []

class A2AHandler(BaseHTTPRequestHandler):
    """HTTP Handler for A2A endpoint"""
    
    def do_POST(self):
        """Handle POST requests"""
        
        if self.path == '/api/a2a':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "rejected",
                    "error": "Invalid JSON"
                }).encode())
                return
            
            self.handle_a2a_message(data)
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        
        if self.path == '/api/a2a/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "session": a2a_session,
                "commands_queue": commands_queue,
                "timestamp": datetime.now().isoformat()
            }).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "status": "live", "a2a": "ready"}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_a2a_message(self, data):
        """Process A2A message"""
        
        msg_type = data.get('type')
        orchestrator = data.get('orchestrator')
        payload = data.get('payload', {})
        
        if not msg_type or not orchestrator:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "rejected",
                "error": "Missing required fields: type, orchestrator"
            }).encode())
            return
        
        message_id = f"msg-{a2a_session['messages_processed'] + 1:04d}"
        a2a_session['messages_processed'] += 1
        
        logger.info(f"[A2A] Received {msg_type} from {orchestrator}: {message_id}")
        
        if msg_type == 'HANDSHAKE':
            self.send_handshake_response(message_id, payload)
        elif msg_type == 'COMMAND':
            self.send_command_response(message_id, payload)
        elif msg_type == 'STATUS_REQUEST':
            self.send_status_response(message_id, payload)
        else:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "rejected",
                "error": f"Unknown message type: {msg_type}"
            }).encode())
    
    def send_handshake_response(self, message_id, payload):
        """Send handshake response"""
        
        a2a_session['established'] = True
        a2a_session['orchestrator'] = payload.get('from', 'MCP-Orchestrator')
        a2a_session['established_at'] = datetime.now().isoformat()
        
        logger.info(f"[A2A] Handshake established with {a2a_session['orchestrator']}")
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "accepted",
            "message_id": message_id,
            "result": {
                "a2a_channel": "established",
                "gateway_version": "2026.3.10",
                "capabilities": ["memory_store", "rag_store", "user_profiles", "email_bridge"],
                "session_id": a2a_session['established_at']
            }
        }).encode())
    
    def send_command_response(self, message_id, payload):
        """Send command response"""
        
        cmd_id = payload.get('id', 'unknown')
        action = payload.get('action', 'unknown')
        priority = payload.get('priority', 'medium')
        description = payload.get('description', '')
        
        command = {
            "id": cmd_id,
            "action": action,
            "priority": priority,
            "description": description,
            "received_at": datetime.now().isoformat(),
            "status": "queued",
            "message_id": message_id
        }
        
        commands_queue.append(command)
        a2a_session['commands'].append(command)
        
        logger.info(f"[A2A] Command queued: {cmd_id} - {action}")
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "accepted",
            "message_id": message_id,
            "result": {
                "command": cmd_id,
                "action": action,
                "execution": "queued",
                "position": len(commands_queue),
                "estimated_time": "5s"
            }
        }).encode())
    
    def send_status_response(self, message_id, payload):
        """Send status response"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "accepted",
            "message_id": message_id,
            "result": {
                "integration_status": "in_progress",
                "sprint": 2,
                "a2a_established": a2a_session['established'],
                "orchestrator": a2a_session['orchestrator'],
                "commands_received": len(a2a_session['commands']),
                "messages_processed": a2a_session['messages_processed'],
                "completed_steps": ["install_livekit_agents", "create_voice_agent_worker"],
                "pending_steps": ["deploy_voice_agent", "test_integration"],
                "livekit_status": "ready",
                "openclaw_status": "ready"
            }
        }).encode())
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info("%s - %s", self.address_string(), format % args)

def run_server():
    """Run A2A endpoint server"""
    server_address = ('0.0.0.0', A2A_PORT)
    httpd = HTTPServer(server_address, A2AHandler)
    logger.info(f"[A2A] Starting endpoint server on port {A2A_PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
