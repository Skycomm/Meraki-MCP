#!/bin/bash
# Quick test script to get everything running

echo "🚀 Starting Meraki MCP Server for Testing"
echo "========================================"

# Start the server in background
echo "Starting server..."
python src/hybrid_server.py &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Get auth token
echo "Getting auth token..."
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/auth \
  -H "Content-Type: application/json" \
  -d '{"username": "david@skycomm.com"}')

TOKEN=$(echo $TOKEN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")

echo ""
echo "✅ Server is running!"
echo "===================="
echo ""
echo "🔑 Your auth token: $TOKEN"
echo ""
echo "📋 For Claude Desktop:"
echo "Update MCP_AUTH_TOKEN in claude_desktop_config.json to: $TOKEN"
echo ""
echo "📋 For n8n MCP Client Tool:"
echo "- SSE Endpoint: http://localhost:8000/sse"
echo "- Auth Type: Bearer Token"
echo "- Token: $TOKEN"
echo ""
echo "📋 Test with curl:"
echo "curl -X POST http://localhost:8000/api/v1/execute \\"
echo "  -H \"Authorization: Bearer $TOKEN\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"tool\": \"list_organizations\", \"arguments\": {}}'"
echo ""
echo "Server PID: $SERVER_PID"
echo "To stop: kill $SERVER_PID"