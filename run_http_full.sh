#!/bin/bash
# Launch Meraki MCP HTTP/SSE Server with FULL profile (833 tools)
# Complete Meraki API coverage - all tools enabled

export MCP_PROFILE=FULL
export SERVER_PORT=8000
export MERAKI_API_KEY="${MERAKI_API_KEY:-1ac5962056ad56da8cea908864f136adc5878a43}"
export AUTH_TOKENS_ADMIN="admin-full-token"
export AUTH_TOKENS_READONLY="readonly-full-token"
export MCP_READ_ONLY_MODE=false

echo "🚀 Starting Meraki MCP HTTP/SSE Server - Full Profile"
echo "   Port: 8000"
echo "   Tools: 833 (ALL TOOLS)"
echo "   URL: http://localhost:8000"
echo "   ⚠️  WARNING: May approach Claude Desktop's tool limit"
echo ""

# Run the HTTP server
.venv/bin/python http_server.py