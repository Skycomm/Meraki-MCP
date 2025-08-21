#!/bin/bash
# Setup script for OpenWebUI integration via mcpo

echo "=== OpenWebUI Setup via mcpo ==="
echo

# Check if mcpo is installed
if ! command -v mcpo &> /dev/null && ! command -v uvx &> /dev/null; then
    echo "Installing mcpo..."
    pip install mcpo
fi

# Get auth token first
echo "1. Getting authentication token from Meraki MCP server..."
AUTH_RESPONSE=$(curl -s -X POST http://localhost:8000/auth \
  -H "Content-Type: application/json" \
  -d '{"username": "openwebui"}')

TOKEN=$(echo $AUTH_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)
if [ -z "$TOKEN" ]; then
    echo "ERROR: Failed to get token. Is the server running?"
    echo "Start it with: cd python_sse && python start_server.py"
    exit 1
fi

echo "✓ Got token: ${TOKEN:0:10}..."
echo

# Start mcpo proxy
echo "2. Starting mcpo proxy..."
echo
echo "Run this command in a new terminal:"
echo
echo "uvx mcpo --port 8001 --api-key \"openwebui-secret\" -- \\"
echo "  curl -N -H \"Authorization: Bearer $TOKEN\" \\"
echo "  http://localhost:8000/sse"
echo
echo "Or if you have mcpo installed:"
echo
echo "mcpo --port 8001 --api-key \"openwebui-secret\" -- \\"
echo "  curl -N -H \"Authorization: Bearer $TOKEN\" \\"
echo "  http://localhost:8000/sse"
echo
echo "=== OpenWebUI Configuration ==="
echo
echo "Once mcpo is running, configure OpenWebUI:"
echo "1. Go to OpenWebUI settings"
echo "2. Add OpenAPI server: http://localhost:8001"
echo "3. API Key: openwebui-secret"
echo "4. Test the tools at: http://localhost:8001/docs"
echo
echo "The OpenAPI documentation will show all 97 Meraki tools!"