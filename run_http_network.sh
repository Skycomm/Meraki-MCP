#!/bin/bash
# Launch Meraki MCP HTTP/SSE Server with Network Infrastructure profile (402 tools)
# Focused on switch, appliance, networks, and VPN management

export MCP_PROFILE=NETWORK
export SERVER_PORT=8002
export MERAKI_API_KEY="${MERAKI_API_KEY:-1ac5962056ad56da8cea908864f136adc5878a43}"
export AUTH_TOKENS_ADMIN="admin-network-token"
export AUTH_TOKENS_READONLY="readonly-network-token"
export MCP_READ_ONLY_MODE=false

echo "🚀 Starting Meraki MCP HTTP/SSE Server - Network Infrastructure Profile"
echo "   Port: 8002"
echo "   Tools: ~402 (Switch, Appliance, Networks, VPN)"
echo "   URL: http://localhost:8002"
echo ""

# Run the HTTP server
.venv/bin/python http_server.py