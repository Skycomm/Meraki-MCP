# Native FastMCP Streamable HTTP Setup

## Overview
This implementation uses FastMCP's **native HTTP transport** with streaming support, providing the official MCP protocol over HTTP as specified in the 2025 standard. No custom adapters or wrappers needed - just pure FastMCP.

## Key Advantages

### ✅ Protocol Compliant
- **JSON-RPC 2.0**: Full compliance with MCP specification
- **Streamable HTTP**: Supports chunked transfer encoding for long operations
- **Proper Error Handling**: Standard JSON-RPC error responses
- **Authentication**: Built-in auth support

### ✅ Native n8n Integration
- Works with n8n's MCP Client Tool directly
- No custom JSON structure needed
- Standard MCP protocol communication
- Streaming responses for real-time updates

### ✅ Simplified Architecture
- **Before**: Custom FastAPI wrapper + adapter (200+ lines)
- **Now**: Native FastMCP HTTP mode (50 lines)
- Less code = fewer bugs
- Better performance

## Quick Start

### 1. Setup Environment

```bash
cd SC-Meraki-MCP
cp .env.example .env
# Edit .env and add your MERAKI_API_KEY
```

### 2. Start with Docker

```bash
# Build and start the streamable server
docker-compose -f docker-compose.streamable.yml up -d

# Check status
docker-compose -f docker-compose.streamable.yml ps

# View logs
docker-compose -f docker-compose.streamable.yml logs -f
```

### 3. Access Services

- **MCP Server**: http://localhost:8100/mcp
- **n8n UI**: http://localhost:5678
  - Username: admin
  - Password: changeme

## Testing the Server

### Test with curl (JSON-RPC)

```bash
# List available tools
curl -X POST http://localhost:8100/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'

# Call a tool
curl -X POST http://localhost:8100/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_organizations",
      "arguments": {}
    },
    "id": 2
  }'
```

### Test with n8n

1. Import `n8n-workflows/meraki-streamable-test.json`
2. Execute the workflow
3. Check the test report for:
   - 816+ tools available
   - Organizations retrieved
   - Protocol compliance confirmed

## MCP Protocol Details

### Request Format (JSON-RPC 2.0)

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "tool_name",
    "arguments": {
      "param1": "value1"
    }
  },
  "id": 1
}
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "result": {
    // Tool response data
  },
  "id": 1
}
```

### Streaming Response (text/event-stream)

```
data: {"jsonrpc":"2.0","method":"progress","params":{"message":"Processing..."}}\n\n
data: {"jsonrpc":"2.0","result":{...},"id":1}\n\n
```

## Configuration Options

### Environment Variables

```env
# Required
MERAKI_API_KEY=your-api-key

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8100

# Optional Authentication
MCP_AUTH_TOKEN=your-secure-token

# Options
MCP_READ_ONLY_MODE=false
LOG_LEVEL=INFO
```

### With Authentication

```bash
# Set token in .env
MCP_AUTH_TOKEN=secure-token-here

# Use in requests
curl -X POST http://localhost:8100/mcp \
  -H "Authorization: Bearer secure-token-here" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

## n8n Integration Methods

### Method 1: Native MCP Client Tool (Recommended)

If n8n has the MCP Client Tool available:

1. Add **MCP Client Tool** node
2. Configure:
   - URL: `http://meraki-mcp-streamable:8100/mcp`
   - Protocol: MCP
   - Authentication: None (or Bearer if configured)
3. Select tools to expose
4. Connect to AI agents or use directly

### Method 2: HTTP Request with JSON-RPC

For direct JSON-RPC calls:

1. Add **HTTP Request** node
2. Configure:
   - URL: `http://meraki-mcp-streamable:8100/mcp`
   - Method: POST
   - Headers:
     - Content-Type: `application/json`
     - Accept: `application/json, text/event-stream`
3. Body: JSON-RPC formatted request

## Available Tools

The server provides **816+ Meraki API tools** including:

### Organization Management (173 tools)
- `get_organizations`
- `get_organization_networks`
- `create_organization_admin`
- `get_organization_devices`
- And 169 more...

### Wireless Management (116 tools)
- `get_network_wireless_ssids`
- `update_network_wireless_ssid`
- `get_network_wireless_clients`
- `get_network_wireless_rf_profiles`
- And 112 more...

### Network Management (114 tools)
- `get_network_devices`
- `get_network_events`
- `get_network_topology`
- And 111 more...

### Plus 400+ more tools across:
- Appliance (130 tools)
- Switch (101 tools)
- Camera (45 tools)
- Systems Manager (49 tools)
- Devices (27 tools)
- Cellular Gateway (24 tools)
- Sensors (18 tools)
- Licensing (8 tools)
- Insight (7 tools)

## Troubleshooting

### Server won't start

```bash
# Check if FastMCP is installed
docker exec meraki-mcp-streamable pip list | grep fastmcp

# Check logs
docker-compose -f docker-compose.streamable.yml logs meraki-mcp-streamable

# Test locally
python meraki_http_streamable.py
```

### Connection refused

```bash
# Check container is running
docker ps | grep meraki-mcp-streamable

# Test health endpoint
curl http://localhost:8100/health

# Check network
docker network inspect sc-meraki-mcp_meraki-network
```

### Authentication errors

```bash
# Check token is set
echo $MCP_AUTH_TOKEN

# Test without auth first
MCP_AUTH_TOKEN="" docker-compose -f docker-compose.streamable.yml up
```

### n8n can't connect

- Use service name `meraki-mcp-streamable` not `localhost`
- Check both containers are on same network
- Verify MCP endpoint: `http://meraki-mcp-streamable:8100/mcp`

## Comparison with Legacy Approach

| Aspect | Legacy (Custom Wrapper) | Native (Streamable HTTP) |
|--------|-------------------------|-------------------------|
| **Code Lines** | 200+ | 50 |
| **Protocol** | Custom JSON | Standard JSON-RPC 2.0 |
| **Streaming** | Fake SSE | Real streaming |
| **n8n Support** | Custom adapter | Native MCP |
| **Maintenance** | High | Low |
| **Performance** | Extra layer | Direct |
| **Compliance** | Partial | Full MCP 2025 |

## Production Deployment

### With PostgreSQL for n8n

```bash
# Enable production profile
docker-compose -f docker-compose.streamable.yml \
  --profile production up -d
```

### SSL/TLS with Traefik

```yaml
# Add to docker-compose.streamable.yml
traefik:
  image: traefik:v2.10
  command:
    - "--providers.docker=true"
    - "--entrypoints.websecure.address=:443"
  ports:
    - "443:443"
  labels:
    - "traefik.http.routers.mcp.tls=true"
```

### Monitoring

```bash
# Prometheus metrics
curl http://localhost:8100/metrics

# Health check
curl http://localhost:8100/health

# n8n metrics
curl http://localhost:5678/metrics
```

## Summary

This native FastMCP Streamable HTTP implementation provides:

1. ✅ **Full MCP protocol compliance**
2. ✅ **Native n8n integration**
3. ✅ **Real streaming support**
4. ✅ **816+ Meraki tools available**
5. ✅ **Simplified architecture**
6. ✅ **Production ready**

The server is now running with proper MCP protocol over Streamable HTTP, ready for n8n integration!