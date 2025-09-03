# Meraki MCP Server - Docker/n8n Integration

This branch contains the Docker containerized version of the Meraki MCP server configured for n8n integration via HTTP Streamable protocol.

## Features
- ✅ Docker containerized deployment
- ✅ n8n MCP Client integration via HTTP Streamable
- ✅ 128 Meraki API tools (n8n's maximum limit)
- ✅ Fixed all schema validation issues for n8n compatibility
- ✅ Authentication disabled for easy testing
- ✅ Debug server with request logging

## Quick Start

### 1. Set up environment
```bash
cp .env.example .env
# Edit .env and add your Meraki API key:
# MERAKI_API_KEY=your-api-key-here
```

### 2. Build and run the Docker container
```bash
docker build -f Dockerfile.streamable -t meraki-mcp .
docker run -d --name meraki-mcp-server \
  --env-file .env \
  -p 8100:8100 \
  --network localai_default \
  meraki-mcp
```

### 3. Configure n8n
In your n8n workflow:
1. Add an **AI Agent** node
2. Add an **OpenAI Chat Model** node (or another LLM)
3. Add an **MCP Client Tool** node with:
   - **Endpoint URL**: `http://meraki-mcp-server:8100/mcp`
   - **Server Transport**: `httpStreamable`
   - **Authentication**: None (leave empty)

## Architecture

### Key Files
- `Dockerfile.streamable` - Container definition with Python 3.11 and dependencies
- `mcp_debug_server.py` - Debug server that logs all requests and handles n8n protocol
- `docker-compose.yml` - Docker compose configuration (MCP server only)
- `.env` - Environment variables including Meraki API key

### Technical Details
- **Protocol**: HTTP Streamable (NDJSON) with SSE support
- **Port**: 8100
- **Tool Limit**: 128 (n8n's maximum)
- **Schema Fixes**:
  - Removed `title` fields that confused n8n
  - Added `required` arrays to all schemas
  - Fixed array properties with proper `items` schemas
  - Ensured all schemas have `type: "object"`

## Known Issues & Solutions

### n8n Tool Limit
n8n has a maximum limit of 128 tools. The full Meraki API has 823+ tools, so only the first 128 are exposed.

### Schema Validation
All array-type properties must have proper `items` schemas. The debug server automatically fixes:
- Empty `items` objects → `{"type": "object"}`
- Missing `items` field → adds `{"type": "object"}`
- Missing `type` in items → adds `"type": "object"`

### Docker Networking
The MCP server must be on the same Docker network as n8n:
```bash
docker network connect localai_default meraki-mcp-server
```

## Testing

### Check server health
```bash
curl http://localhost:8100/health
```

### Test tools list
```bash
curl -X POST http://localhost:8100/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"method":"tools/list","params":{},"jsonrpc":"2.0","id":1}' | \
  jq '.result.tools | length'
# Should return: 128
```

### View logs
```bash
docker logs meraki-mcp-server -f
```

## Development

### Rebuild after changes
```bash
docker stop meraki-mcp-server
docker rm meraki-mcp-server
docker build -f Dockerfile.streamable -t meraki-mcp .
docker run -d --name meraki-mcp-server \
  --env-file .env \
  -p 8100:8100 \
  --network localai_default \
  meraki-mcp
```

### Debug mode
The `mcp_debug_server.py` logs all incoming requests and responses, helpful for troubleshooting integration issues.

## Available Tools (First 128 of 823+)
- Organization management tools
- Network configuration tools  
- Device management tools
- Wireless configuration tools
- And many more...

Use the tools/list method to see all available tools and their descriptions.