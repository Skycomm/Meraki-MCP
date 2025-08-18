#!/bin/bash
# Quick Start Script for Meraki MCP Hybrid Server

echo "🚀 Meraki MCP Hybrid Server Quick Start"
echo "======================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your MERAKI_API_KEY"
    echo "   Then run this script again."
    exit 1
fi

# Check if MERAKI_API_KEY is set
source .env
if [ -z "$MERAKI_API_KEY" ] || [ "$MERAKI_API_KEY" = "your-meraki-api-key-here" ]; then
    echo "❌ Error: MERAKI_API_KEY not configured in .env"
    echo "Please edit .env and add your actual API key"
    exit 1
fi

# Get server IP
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    SERVER_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')
else
    # Linux
    SERVER_IP=$(hostname -I | awk '{print $1}')
fi

echo "✅ Configuration OK"
echo "📍 Server IP: $SERVER_IP"
echo ""

# Start the server
echo "Starting server with Docker Compose..."
docker-compose -f docker-compose.hybrid.yml up -d

# Wait for server to start
echo "Waiting for server to be ready..."
sleep 5

# Check health
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Server is healthy!"
else
    echo "❌ Server health check failed"
    echo "Check logs: docker-compose -f docker-compose.hybrid.yml logs"
    exit 1
fi

# Get auth token
echo ""
echo "Getting authentication token..."
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/auth \
  -H "Content-Type: application/json" \
  -d '{"username": "quickstart@example.com"}')

TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Failed to get auth token"
    exit 1
fi

echo "✅ Got auth token!"
echo ""
echo "========================================="
echo "🎉 Server is ready!"
echo "========================================="
echo ""
echo "Server URL: http://$SERVER_IP:8000"
echo "Auth Token: $TOKEN"
echo ""
echo "📋 Claude Desktop Configuration:"
echo "Add this to your claude_desktop_config.json:"
echo ""
cat << EOF
{
  "mcpServers": {
    "meraki": {
      "command": "node",
      "args": ["$HOME/mcp-tools/meraki-mcp-client.js"],
      "env": {
        "MCP_SERVER_URL": "http://$SERVER_IP:8000",
        "MCP_AUTH_TOKEN": "$TOKEN"
      }
    }
  }
}
EOF
echo ""
echo "📋 n8n Configuration:"
echo "- URL: http://$SERVER_IP:8000/api/v1/execute"
echo "- Header: Authorization = Bearer $TOKEN"
echo ""
echo "📋 Test with curl:"
echo "curl -X POST http://$SERVER_IP:8000/api/v1/execute \\"
echo "  -H \"Authorization: Bearer $TOKEN\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"tool\": \"list_organizations\", \"arguments\": {}}'"
echo ""
echo "View logs: docker-compose -f docker-compose.hybrid.yml logs -f"
echo "Stop server: docker-compose -f docker-compose.hybrid.yml down"