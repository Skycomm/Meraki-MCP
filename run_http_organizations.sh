#!/bin/bash
# Launch Meraki MCP HTTP/SSE Server with Organizations profile (126 tools)
# Focused on organization-level management and configuration

export MCP_PROFILE=ORGANIZATIONS
export SERVER_PORT=8003
export MERAKI_API_KEY="${MERAKI_API_KEY:-1ac5962056ad56da8cea908864f136adc5878a43}"
export AUTH_TOKENS_ADMIN="admin-org-token"
export AUTH_TOKENS_READONLY="readonly-org-token"
export MCP_READ_ONLY_MODE=false

echo "🚀 Starting Meraki MCP HTTP/SSE Server - Organizations Admin Profile"
echo "   Port: 8003"
echo "   Tools: ~126 (Org admin, policies, licensing)"
echo "   URL: http://localhost:8003"
echo ""

# Run the HTTP server
.venv/bin/python http_server.py