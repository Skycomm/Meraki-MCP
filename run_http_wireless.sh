#!/bin/bash
# Launch Meraki MCP HTTP/SSE Server with Wireless profile (179 tools)
# Focused on wireless, RF profiles, and SSID management

export MCP_PROFILE=WIRELESS
export SERVER_PORT=8001
export MERAKI_API_KEY="${MERAKI_API_KEY:-1ac5962056ad56da8cea908864f136adc5878a43}"
export AUTH_TOKENS_ADMIN="admin-wireless-token"
export AUTH_TOKENS_READONLY="readonly-wireless-token"
export MCP_READ_ONLY_MODE=false

echo "🚀 Starting Meraki MCP HTTP/SSE Server - Wireless Profile"
echo "   Port: 8001"
echo "   Tools: ~179 (Wireless, RF, SSIDs)"
echo "   URL: http://localhost:8001"
echo ""

# Run the HTTP server
.venv/bin/python http_server.py