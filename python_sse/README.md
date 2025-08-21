# Cisco Meraki MCP Server - SSE/HTTP Implementation

This is a complete SSE/HTTP implementation of the Cisco Meraki MCP server, extracted from the stdio server with all 97 tools and 400+ functions.

## Features

- ✅ **Full MCP Protocol Support** - Compatible with Claude Desktop, n8n, and OpenWebUI
- ✅ **All 97 Meraki Tools** - Complete functionality from the stdio server
- ✅ **Multiple Transports** - SSE, Streamable HTTP, and REST API
- ✅ **Authentication** - Bearer token based security
- ✅ **Rate Limiting** - Prevent API abuse
- ✅ **Privileged Operations** - Role-based access control

## Quick Start

### 1. Install Dependencies

```bash
cd python_sse
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export MERAKI_API_KEY="your-meraki-api-key"
export PRIVILEGED_USERS="user1@example.com,user2"
```

Or create a `.env` file:
```env
MERAKI_API_KEY=your-meraki-api-key
PRIVILEGED_USERS=user1@example.com,user2
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### 3. Start the Server

```bash
python start_server.py
```

The server will start on `http://localhost:8000`

## n8n Integration

### 1. Get Authentication Token

```bash
curl -X POST http://localhost:8000/auth \
  -H "Content-Type: application/json" \
  -d '{"username": "your-username"}'
```

Save the token from the response.

### 2. Configure n8n MCP Client Tool

1. Add **MCP Client Tool** node to your workflow
2. Configure:
   - **SSE Endpoint**: `http://localhost:8000/sse`
   - **Authentication**: Bearer Token
   - **Token**: Your token from step 1
   - **Tools to Include**: All (or select specific tools)

3. Connect to an AI Agent node
4. The agent can now use all 97 Meraki tools!

### Example n8n Workflow

```javascript
// In your AI Agent prompt:
"List all Meraki organizations"
"Find client SKY-THOMAS-01 in all networks"
"Check uplink packet loss for organization 686470"
```

## OpenWebUI Integration (via mcpo)

### 1. Install mcpo

```bash
pip install mcpo
```

### 2. Start mcpo Proxy

```bash
uvx mcpo --port 8001 --api-key "openwebui-key" -- \
  python start_server.py
```

### 3. Configure OpenWebUI

1. Add OpenAPI server: `http://localhost:8001`
2. Use the API key: `openwebui-key`
3. Test at: `http://localhost:8001/docs`

## Available Endpoints

### Authentication
- `POST /auth` - Get authentication token

### MCP Protocol
- `GET /sse` - SSE stream for MCP protocol
- `POST /sse` - Handle MCP messages
- `POST /mcp` - Streamable HTTP endpoint (with session support)

### REST API
- `GET /api/v1/tools` - List all available tools
- `POST /api/v1/tools/{tool_name}` - Execute a specific tool

### Utility
- `GET /` - Server information
- `GET /health` - Health check

## Tool Categories (97 Total)

- **Organizations** (8 tools) - Manage organizations, firmware, networks
- **Networks** (6 tools) - Network operations and client management
- **Devices** (6 tools) - Device control, status, and reboots
- **Wireless** (9 tools) - SSID, RF profiles, Air Marshal
- **Switch** (5 tools) - Port configuration, VLANs
- **Analytics** (4 tools) - Uplink monitoring, connection stats
- **Alerts** (6 tools) - Webhooks and alert configuration
- **Appliance** (6 tools) - Firewall, VPN, content filtering
- **Camera** (6 tools) - Video links, snapshots, analytics
- **Systems Manager** (7 tools) - Device management, profiles
- **Licensing** (6 tools) - License management and renewal
- **Policy** (6 tools) - Policy objects and groups
- **Monitoring** (6 tools) - Enhanced 2025 monitoring features
- **Beta** (6 tools) - Early access features
- **Live Tools** (10 tools) - Ping, throughput, cable tests

## Testing

### Test SSE Connection

```bash
# Get token
TOKEN=$(curl -s -X POST http://localhost:8000/auth \
  -H "Content-Type: application/json" \
  -d '{"username": "test"}' | jq -r .token)

# Test SSE stream
curl -N -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/sse
```

### Test MCP Protocol

```bash
# List tools
curl -X POST http://localhost:8000/sse \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'

# Call a tool
curl -X POST http://localhost:8000/sse \
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
  }'
```

### Test REST API

```bash
# List tools
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/tools

# Execute tool
curl -X POST http://localhost:8000/api/v1/tools/list_organizations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tool": "list_organizations", "arguments": {}}'
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY start_server.py .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "start_server.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  meraki-mcp-sse:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MERAKI_API_KEY=${MERAKI_API_KEY}
      - PRIVILEGED_USERS=${PRIVILEGED_USERS}
    restart: unless-stopped
```

## Troubleshooting

### "MERAKI_API_KEY not set"
- Set the environment variable: `export MERAKI_API_KEY="your-key"`
- Or create a `.env` file with the key

### "Invalid token" errors
- Get a new token using the `/auth` endpoint
- Ensure you're using "Bearer " prefix in the Authorization header

### Tools not showing in n8n
- Check the SSE endpoint URL is correct
- Verify the token is valid
- Look at server logs for errors

### Rate limit errors
- Wait 60 seconds for the limit to reset
- Increase `RATE_LIMIT_REQUESTS` if needed

## License

MIT License - See LICENSE file for details