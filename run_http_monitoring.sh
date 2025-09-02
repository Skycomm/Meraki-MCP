#!/bin/bash
# Launch Meraki MCP HTTP/SSE Server with Monitoring profile (141 tools)
# Focused on devices, cameras, sensors, and analytics

export MCP_PROFILE=MONITORING
export SERVER_PORT=8004
export MERAKI_API_KEY="${MERAKI_API_KEY:-1ac5962056ad56da8cea908864f136adc5878a43}"
export AUTH_TOKENS_ADMIN="admin-monitoring-token"
export AUTH_TOKENS_READONLY="readonly-monitoring-token"
export MCP_READ_ONLY_MODE=false

echo "🚀 Starting Meraki MCP HTTP/SSE Server - Monitoring & Analytics Profile"
echo "   Port: 8004"
echo "   Tools: ~141 (Devices, cameras, sensors, analytics)"
echo "   URL: http://localhost:8004"
echo ""

# Run the HTTP server
.venv/bin/python http_server.py