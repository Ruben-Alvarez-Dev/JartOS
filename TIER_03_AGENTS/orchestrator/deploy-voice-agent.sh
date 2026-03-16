#!/bin/bash
# Voice Agent Deployment Script
# Created by Qwen-Code for LiveKit + Zadarma integration

set -e

echo "🎤 Deploying Voice Agent Worker..."

# Check if worker exists
WORKER_FILE="/root/OPENCLAW-city/orchestrator/voice_agent_worker.py"
if [ ! -f "$WORKER_FILE" ]; then
    echo "❌ Voice agent worker not found at $WORKER_FILE"
    exit 1
fi

# Check dependencies
echo "📦 Checking dependencies..."
python3 -c "from livekit.agents import JobContext" 2>/dev/null || {
    echo "❌ livekit-agents not installed"
    exit 1
}

# Create systemd service
echo "📝 Creating systemd service..."
cat > /etc/systemd/system/voice-agent.service << 'EOF'
[Unit]
Description=LiveKit Voice Agent Worker
After=network.target livekit-server.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/OPENCLAW-city/orchestrator
ExecStart=/usr/bin/python3 /root/OPENCLAW-city/orchestrator/voice_agent_worker.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
echo "🚀 Starting voice agent..."
systemctl daemon-reload
systemctl enable voice-agent
systemctl restart voice-agent

sleep 3

# Check status
echo ""
echo "=== VOICE AGENT STATUS ==="
systemctl is-active voice-agent
systemctl status voice-agent --no-pager -n 5

echo ""
echo "✅ Voice Agent deployment complete!"
