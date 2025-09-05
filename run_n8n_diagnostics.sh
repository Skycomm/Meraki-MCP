#!/bin/bash
#
# Run Cisco Meraki MCP Server with N8N_DIAGNOSTICS profile
# Perfect for N8N automation - exactly 128 tools for network diagnostics
#

export MCP_PROFILE=N8N_DIAGNOSTICS

echo "🚀 Starting Cisco Meraki MCP Server"
echo "📊 Profile: N8N Network Diagnostics (128 tools)"
echo "🎯 Features: Latency, packet loss, health checks, device discovery"
echo "💡 Perfect for: Automated support ticket diagnostics"
echo ""

.venv/bin/python meraki_server.py