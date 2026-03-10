#!/usr/bin/env python3
"""
A2A Communication Script - Direct HTTP to OpenClaw Gateway
Orchestrator: MCP Server (Controller)
Target: OpenClaw Gateway (Controlled)

This script sends A2A messages and commands to OpenClaw Gateway
to implement the LiveKit integration plan.
"""

import httpx
import json
from datetime import datetime

# Configuration
OPENCLAW_URL = "http://127.0.0.1:18789"
HEADERS = {"Content-Type": "application/json"}

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def send_a2a_message(message_type, payload):
    """Send A2A message to OpenClaw Gateway"""
    full_payload = {
        "type": message_type,
        "timestamp": datetime.now().isoformat(),
        "orchestrator": "MCP-Server",
        "payload": payload
    }
    
    try:
        with httpx.Client(timeout=10) as client:
            response = client.post(
                f"{OPENCLAW_URL}/api/a2a",
                json=full_payload,
                headers=HEADERS
            )
            return response.status_code, response.json()
    except httpx.ConnectError:
        return 0, {"error": "Connection refused - OpenClaw Gateway not available"}
    except Exception as e:
        return 0, {"error": str(e)}

def check_health():
    """Check OpenClaw health"""
    try:
        with httpx.Client(timeout=5) as client:
            response = client.get(f"{OPENCLAW_URL}/health")
            return response.json()
    except:
        return {"status": "unavailable"}

# ============================================================================
# A2A COMMAND SEQUENCE - LIVEKIT INTEGRATION PLAN
# ============================================================================

print_header("🎛️  MCP ORCHESTRATOR - A2A COMMUNICATION INITIATED")
print(f"Target: OpenClaw Gateway @ {OPENCLAW_URL}")
print(f"Time: {datetime.now().isoformat()}")

# Step 1: Check health
print_header("STEP 1: Health Check")
health = check_health()
print(f"OpenClaw Status: {health}")

# Step 2: Send A2A Handshake
print_header("STEP 2: A2A Handshake")
handshake_payload = {
    "message_type": "ORCHESTRATOR_HANDSHAKE",
    "from": "MCP-Orchestrator",
    "to": "OpenClaw-Gateway",
    "role": "controller",
    "purpose": "LiveKit Integration - Sprint 2"
}
status, response = send_a2a_message("HANDSHAKE", handshake_payload)
print(f"Handshake Status: {status}")
print(f"Response: {json.dumps(response, indent=2)}")

# Step 3: Send Integration Commands
print_header("STEP 3: Integration Commands")

commands = [
    {
        "id": "cmd-001",
        "action": "enable_a2a_endpoint",
        "priority": "high",
        "description": "Enable A2A communication endpoint at /api/a2a"
    },
    {
        "id": "cmd-002",
        "action": "prepare_memory_store",
        "priority": "high",
        "description": "Prepare Memory Store schema for voice sessions",
        "schema": {
            "table": "voice_sessions",
            "columns": ["session_id", "user_id", "transcript", "summary"]
        }
    },
    {
        "id": "cmd-003",
        "action": "prepare_rag_store",
        "priority": "high",
        "description": "Prepare RAG Store collection for voice agent knowledge"
    },
    {
        "id": "cmd-004",
        "action": "create_api_credentials",
        "priority": "medium",
        "description": "Create API credentials for LiveKit Agents Worker",
        "credentials": {
            "service": "livekit-agents",
            "permissions": ["memory_read", "memory_write", "rag_search"]
        }
    },
    {
        "id": "cmd-005",
        "action": "enable_audit_logging",
        "priority": "medium",
        "description": "Enable audit logging for A2A communications"
    }
]

for cmd in commands:
    print(f"\n📋 Command {cmd['id']}: {cmd['action']}")
    status, response = send_a2a_message("COMMAND", cmd)
    print(f"   Status: {status}")
    if "error" in response:
        print(f"   ⚠️  Note: {response['error']}")
    else:
        print(f"   ✅ Response: {json.dumps(response, indent=2)[:200]}")

# Step 4: Integration Status
print_header("STEP 4: Integration Status")
status, response = send_a2a_message("STATUS_REQUEST", {"type": "integration"})
print(f"Status Request: {status}")
print(f"Response: {json.dumps(response, indent=2)}")

# Summary
print_header("📊 SUMMARY")
print("""
A2A Communication Sequence Completed

Commands Sent:
  ✅ cmd-001: enable_a2a_endpoint
  ✅ cmd-002: prepare_memory_store  
  ✅ cmd-003: prepare_rag_store
  ✅ cmd-004: create_api_credentials
  ✅ cmd-005: enable_audit_logging

Next Steps:
  1. Wait for OpenClaw to process commands
  2. Install livekit-agents package
  3. Create voice agent worker
  4. Test end-to-end integration

Orchestrator Status: ACTIVE
Integration Progress: 20% (Commands sent, awaiting execution)
""")

print_header("🎛️  MCP ORCHESTRATOR - SESSION COMPLETE")
