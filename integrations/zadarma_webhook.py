#!/usr/bin/env python3
"""
Zadarma Webhook Handler - OpenClaw Integration
Receives webhooks from Zadarma and forwards to OpenClaw A2A

Date: 2026-03-10
"""

from flask import Flask, request, jsonify
import logging
import httpx
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
LOG_DIR = "/var/log/openclaw/zadarma"
os.makedirs(LOG_DIR, exist_ok=True)
A2A_URL = "http://localhost:18790/api/a2a"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/webhooks.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def send_to_a2a(event_type: str, data: dict) -> dict:
    """Forward event to OpenClaw A2A"""
    msg = {
        "type": "ZADARMA_EVENT",
        "timestamp": datetime.now().isoformat(),
        "orchestrator": "Zadarma-Webhook",
        "payload": {
            "event": event_type,
            "data": data
        }
    }
    
    try:
        with httpx.Client(timeout=10) as client:
            response = client.post(A2A_URL, json=msg)
            return response.json()
    except Exception as e:
        logger.error(f"A2A error: {e}")
        return {"status": "error", "error": str(e)}

@app.route('/webhook/zadarma/call', methods=['POST'])
def call_webhook():
    """Handle call webhooks from Zadarma"""
    data = request.json
    
    event_type = data.get('event', 'unknown')
    logger.info(f"Call webhook: {event_type}")
    
    # Forward to A2A
    result = send_to_a2a(f"call_{event_type}", data)
    
    return jsonify({"status": "ok", "a2a_result": result})

@app.route('/webhook/zadarma/sms', methods=['POST'])
def sms_webhook():
    """Handle SMS webhooks from Zadarma"""
    data = request.json
    
    logger.info(f"SMS webhook from: {data.get('from', 'unknown')}")
    
    # Forward to A2A
    result = send_to_a2a("sms_received", data)
    
    return jsonify({"status": "ok", "a2a_result": result})

@app.route('/webhook/zadarma/number_lookup', methods=['POST'])
def number_lookup_webhook():
    """Handle number lookup webhooks"""
    data = request.json
    
    logger.info(f"Number lookup: {data.get('phone', 'unknown')}")
    
    # Forward to A2A
    result = send_to_a2a("number_lookup", data)
    
    return jsonify({"status": "ok", "a2a_result": result})

@app.route('/webhook/zadarma/speech_recognition', methods=['POST'])
def speech_recognition_webhook():
    """Handle speech recognition webhooks"""
    data = request.json
    
    logger.info(f"Speech recognition result: {data.get('text', '')[:50]}...")
    
    # Forward to A2A
    result = send_to_a2a("speech_recognition", data)
    
    return jsonify({"status": "ok", "a2a_result": result})

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"ok": True, "service": "zadarma-webhook"})

if __name__ == '__main__':
    logger.info("Starting Zadarma Webhook Handler on port 18791")
    app.run(host='0.0.0.0', port=18791, debug=False, threaded=True)
