#!/bin/bash
#
# Run Cisco Meraki MCP Server for N8N with HTTP Streamable transport
# Uses N8N_ESSENTIALS profile (97 tools) - perfect for N8N automation
#

export MCP_PROFILE=N8N_ESSENTIALS
export SERVER_HOST=0.0.0.0
export SERVER_PORT=8100

echo "🚀 Starting Cisco Meraki MCP Server for N8N"
echo "🎯 Profile: N8N_ESSENTIALS (97 tools)"
echo "🌐 Transport: HTTP Streamable"
echo "📡 Endpoint: http://localhost:8100/mcp"
echo "💡 Perfect for: N8N automation workflows"
echo ""
echo "🔍 Your N8N workflow will have access to:"
echo "   ✅ Client/Organization lookup tools"
echo "   ✅ Network device discovery"
echo "   ✅ Performance diagnostics (latency, packet loss)"
echo "   ✅ Health monitoring and alerts"
echo "   ✅ Custom diagnostic helpers"
echo ""

# Run the server with HTTP transport
.venv/bin/python -c "
import os
os.environ['MCP_PROFILE'] = 'N8N_ESSENTIALS'
from server.main import app
import uvicorn
print('🎯 Loading N8N_ESSENTIALS profile...')
print('🌐 Starting HTTP server on port 8100...')
uvicorn.run(app.streamable_http_app, host='0.0.0.0', port=8100)
"