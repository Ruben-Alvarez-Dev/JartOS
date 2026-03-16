#!/usr/bin/env python3
"""
A2A Communication Logger - Real-time Telegram Notifications
Logs all A2A communications and sends them to Telegram in real-time.

Date: 2026-03-10
Sprint: 2 - LiveKit Agents Integration
"""

import json
import os
import requests
from datetime import datetime
from typing import Dict, Any

# Configuration
LOG_DIR = "/var/log/openclaw/a2a"
LOG_FILE = f"{LOG_DIR}/a2a_communications.json"
TELEGRAM_LOG_FILE = f"{LOG_DIR}/telegram_notifications.log"

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

class A2ALogger:
    """Logger for A2A communications with Telegram notifications"""
    
    def __init__(self, telegram_token: str, chat_id: int):
        self.telegram_token = telegram_token
        self.chat_id = chat_id
        self.session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.communications = []
        
        # Initialize log file
        self._init_log_file()
        
    def _init_log_file(self):
        """Initialize or load existing log file"""
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w') as f:
                json.dump({
                    "session_id": self.session_id,
                    "started_at": datetime.now().isoformat(),
                    "communications": []
                }, f, indent=2)
        else:
            with open(LOG_FILE, 'r') as f:
                data = json.load(f)
                self.session_id = data.get("session_id", self.session_id)
                self.communications = data.get("communications", [])
    
    def _save_log(self):
        """Save current log to file"""
        with open(LOG_FILE, 'w') as f:
            json.dump({
                "session_id": self.session_id,
                "started_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_communications": len(self.communications),
                "communications": self.communications
            }, f, indent=2)
    
    def _send_telegram_message(self, message: str, parse_mode: str = "Markdown") -> bool:
        """Send message to Telegram"""
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                # Log successful notification
                with open(TELEGRAM_LOG_FILE, 'a') as f:
                    f.write(f"{datetime.now().isoformat()} - Sent - {message[:100]}...\n")
                return True
            else:
                with open(TELEGRAM_LOG_FILE, 'a') as f:
                    f.write(f"{datetime.now().isoformat()} - Failed ({response.status_code}) - {message[:100]}...\n")
                return False
        except Exception as e:
            with open(TELEGRAM_LOG_FILE, 'a') as f:
                f.write(f"{datetime.now().isoformat()} - Error ({str(e)}) - {message[:100]}...\n")
            return False
    
    def log_communication(self, 
                         msg_type: str, 
                         direction: str, 
                         sender: str, 
                         receiver: str,
                         payload: Dict[str, Any],
                         status: str = "sent",
                         response: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Log an A2A communication and send Telegram notification
        
        Args:
            msg_type: Type of message (HANDSHAKE, COMMAND, STATUS_REQUEST, etc.)
            direction: "outbound" (to OpenClaw) or "inbound" (from OpenClaw)
            sender: Sender identifier
            receiver: Receiver identifier
            payload: Message payload
            status: Message status (sent, received, error, etc.)
            response: Response data if applicable
        """
        
        communication = {
            "id": len(self.communications) + 1,
            "timestamp": datetime.now().isoformat(),
            "type": msg_type,
            "direction": direction,
            "sender": sender,
            "receiver": receiver,
            "status": status,
            "payload": payload,
            "response": response
        }
        
        self.communications.append(communication)
        self._save_log()
        
        # Send Telegram notification
        self._notify_telegram(communication)
        
        return communication
    
    def _notify_telegram(self, communication: Dict[str, Any]):
        """Format and send Telegram notification"""
        
        # Emoji for direction
        direction_emoji = "📤" if communication["direction"] == "outbound" else "📥"
        status_emoji = {
            "sent": "✅",
            "received": "✅",
            "error": "❌",
            "pending": "⏳",
            "accepted": "✅",
            "rejected": "❌"
        }.get(communication["status"], "📋")
        
        # Format message
        message = f"""
{direction_emoji} *A2A Communication #{communication['id']}* {status_emoji}

*Type:* `{communication['type']}`
*Direction:* {communication['direction']}
*From:* {communication['sender']}
*To:* {communication['receiver']}
*Status:* `{communication['status']}`
*Time:* `{communication['timestamp'].split('T')[1].split('.')[0]}`

*Payload:*
```json
{json.dumps(communication['payload'], indent=2)[:500]}
```
"""
        
        # Add response if available
        if communication.get('response'):
            message += f"""
*Response:*
```json
{json.dumps(communication['response'], indent=2)[:500]}
```
"""
        
        # Truncate if too long (Telegram limit is 4096 chars)
        if len(message) > 4000:
            message = message[:4000] + "\n\n... (truncated)"
        
        self._send_telegram_message(message)
    
    def send_session_summary(self):
        """Send session summary to Telegram"""
        
        # Calculate statistics
        total = len(self.communications)
        outbound = sum(1 for c in self.communications if c["direction"] == "outbound")
        inbound = sum(1 for c in self.communications if c["direction"] == "inbound")
        errors = sum(1 for c in self.communications if c["status"] == "error")
        
        # Group by type
        by_type = {}
        for c in self.communications:
            t = c["type"]
            by_type[t] = by_type.get(t, 0) + 1
        
        summary = f"""
📊 *A2A Session Summary*

*Session ID:* `{self.session_id}`
*Started:* `{self.communications[0]['timestamp'] if self.communications else 'N/A'}`
*Total Communications:* {total}

*By Direction:*
  📤 Outbound: {outbound}
  📥 Inbound: {inbound}

*By Type:*
"""
        
        for msg_type, count in by_type.items():
            summary += f"  • {msg_type}: {count}\n"
        
        if errors > 0:
            summary += f"\n⚠️ *Errors:* {errors}\n"
        
        summary += f"\n*Log File:* `{LOG_FILE}`"
        
        self._send_telegram_message(summary)
    
    def get_log(self) -> Dict[str, Any]:
        """Get current log data"""
        return {
            "session_id": self.session_id,
            "total_communications": len(self.communications),
            "communications": self.communications
        }


# Global logger instance (will be initialized with config)
a2a_logger = None

def init_a2a_logger(telegram_token: str, chat_id: int) -> A2ALogger:
    """Initialize global A2A logger"""
    global a2a_logger
    a2a_logger = A2ALogger(telegram_token, chat_id)
    
    # Send initialization notification
    a2a_logger._send_telegram_message(f"""
🎛️ *A2A Logger Initialized*

*Session:* `{a2a_logger.session_id}`
*Log File:* `{LOG_FILE}`
*Chat ID:* `{chat_id}`

All A2A communications will be logged and sent to this chat in real-time.
""")
    
    return a2a_logger


if __name__ == "__main__":
    # Test the logger
    print("A2A Communication Logger - Test Mode")
    print("This module is imported by the MCP Orchestrator")
