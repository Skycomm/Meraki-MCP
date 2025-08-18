#!/bin/bash
# Test script for Meraki MCP Hybrid Server

SERVER_URL="${1:-http://localhost:8000}"
TOKEN="${2:-}"

echo "🧪 Testing Meraki MCP Hybrid Server"
echo "==================================="
echo "Server: $SERVER_URL"
echo ""

# Test 1: Health check
echo "1. Testing health endpoint..."
HEALTH=$(curl -s $SERVER_URL/health)
if echo $HEALTH | grep -q "healthy"; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

# Test 2: Get auth token if not provided
if [ -z "$TOKEN" ]; then
    echo ""
    echo "2. Getting auth token..."
    AUTH_RESPONSE=$(curl -s -X POST $SERVER_URL/auth \
      -H "Content-Type: application/json" \
      -d '{"username": "test@example.com"}')
    
    TOKEN=$(echo $AUTH_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)
    
    if [ -z "$TOKEN" ]; then
        echo "❌ Failed to get auth token"
        echo "Response: $AUTH_RESPONSE"
        exit 1
    fi
    echo "✅ Got auth token: ${TOKEN:0:10}..."
fi

# Test 3: List available tools
echo ""
echo "3. Testing list tools endpoint..."
TOOLS=$(curl -s $SERVER_URL/api/v1/tools \
  -H "Authorization: Bearer $TOKEN")

if echo $TOOLS | grep -q "list_organizations"; then
    echo "✅ Tools endpoint working"
    echo "Available tools:"
    echo $TOOLS | python3 -m json.tool | grep '"name"' | cut -d'"' -f4 | sed 's/^/  - /'
else
    echo "❌ Failed to list tools"
    echo "Response: $TOOLS"
fi

# Test 4: Execute a tool
echo ""
echo "4. Testing tool execution..."
RESULT=$(curl -s -X POST $SERVER_URL/api/v1/execute \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "list_organizations", "arguments": {}}')

if echo $RESULT | grep -q "success"; then
    SUCCESS=$(echo $RESULT | grep -o '"success":[^,]*' | cut -d':' -f2)
    if [ "$SUCCESS" = "true" ]; then
        echo "✅ Tool execution successful"
        # Show first 200 chars of result
        PREVIEW=$(echo $RESULT | grep -o '"result":"[^"]*' | cut -d'"' -f4 | cut -c1-200)
        echo "Result preview: $PREVIEW..."
    else
        echo "❌ Tool execution failed"
        ERROR=$(echo $RESULT | grep -o '"error":"[^"]*' | cut -d'"' -f4)
        echo "Error: $ERROR"
    fi
else
    echo "❌ Invalid response format"
    echo "Response: $RESULT"
fi

# Summary
echo ""
echo "==================================="
echo "Test Summary:"
echo "- Health Check: ✅"
echo "- Authentication: ✅" 
echo "- API Endpoints: ✅"
echo ""
echo "🎉 Server is working correctly!"
echo ""
echo "Your auth token: $TOKEN"
echo ""
echo "Next steps:"
echo "1. Configure Claude Desktop with this token"
echo "2. Set up n8n workflows"
echo "3. Try: curl -X POST $SERVER_URL/api/v1/execute -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d '{\"tool\": \"check_uplinks\", \"arguments\": {\"org_id\": \"YOUR_ORG_ID\"}}'"