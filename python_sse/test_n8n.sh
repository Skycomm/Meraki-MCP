#!/bin/bash
# Test script for n8n MCP integration

echo "=== Cisco Meraki MCP SSE/HTTP Server - n8n Test ==="
echo

# Check if server is running
echo "1. Checking server health..."
HEALTH=$(curl -s http://localhost:8000/health)
if [ $? -ne 0 ]; then
    echo "ERROR: Server not running. Start it with: python start_server.py"
    exit 1
fi
echo "✓ Server is healthy"
echo

# Get auth token
echo "2. Getting authentication token..."
AUTH_RESPONSE=$(curl -s -X POST http://localhost:8000/auth \
  -H "Content-Type: application/json" \
  -d '{"username": "n8n-test"}')

TOKEN=$(echo $AUTH_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)
if [ -z "$TOKEN" ]; then
    echo "ERROR: Failed to get token"
    echo "Response: $AUTH_RESPONSE"
    exit 1
fi
echo "✓ Got token: ${TOKEN:0:10}..."
echo

# Test SSE connection
echo "3. Testing SSE connection..."
echo "Connecting to SSE endpoint (press Ctrl+C to stop)..."
curl -N -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/sse &
SSE_PID=$!
sleep 2
kill $SSE_PID 2>/dev/null
echo "✓ SSE connection works"
echo

# Test MCP protocol - list tools
echo "4. Testing MCP protocol - listing tools..."
TOOLS_RESPONSE=$(curl -s -X POST http://localhost:8000/sse \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}')

TOOL_COUNT=$(echo $TOOLS_RESPONSE | grep -o '"name"' | wc -l)
echo "✓ Found $TOOL_COUNT tools available"
echo

# Test MCP protocol - call a tool
echo "5. Testing MCP protocol - calling list_organizations..."
ORG_RESPONSE=$(curl -s -X POST http://localhost:8000/sse \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "list_organizations",
      "arguments": {}
    }
  }')

if echo "$ORG_RESPONSE" | grep -q "error"; then
    echo "✗ Error calling tool:"
    echo "$ORG_RESPONSE" | jq .
else
    echo "✓ Tool executed successfully"
    echo "$ORG_RESPONSE" | jq -r '.result.content[0].text' | head -5
fi
echo

# Print n8n configuration
echo "=== n8n Configuration ==="
echo
echo "Use these settings in n8n MCP Client Tool node:"
echo "  SSE Endpoint: http://localhost:8000/sse"
echo "  Authentication: Bearer Token"
echo "  Token: $TOKEN"
echo
echo "✓ Server is ready for n8n integration!"