# n8n Integration Instructions for Meraki MCP Server

## MCP Server Details

Your Meraki MCP Server is now running as a Docker container with the following details:

- **URL**: `http://localhost:8100/mcp`
- **Port**: 8100
- **Auth Token**: `test-token-123`
- **Protocol**: Custom HTTP adapter (not standard MCP JSON-RPC)

## Docker Container

The server is running in Docker with:
- Container name: `meraki-mcp-server`
- Network: `meraki-mcp-network`
- Exposed on port 8100

To manage the container:
```bash
# View logs
docker logs meraki-mcp-server

# Restart
docker compose restart

# Stop
docker compose down

# Start with rebuild
docker compose up -d --build
```

## n8n Configuration

Unfortunately, this MCP server uses a custom HTTP adapter format that is **NOT compatible** with n8n's standard MCP Client Tool which expects JSON-RPC 2.0 protocol.

### The Issue

- n8n MCP Client expects standard MCP protocol: `{"jsonrpc":"2.0","method":"tools/list","id":1}`
- This server uses custom format: `{"action":"list_tools"}`

### Solution Options

1. **Use HTTP Request Node** (Recommended)
   - Instead of MCP Client Tool, use the HTTP Request node in n8n
   - Configure it to call the MCP server directly
   - Example configuration:
     ```
     Method: POST
     URL: http://localhost:8100/mcp
     Authentication: Header Auth
     Header Name: Authorization
     Header Value: Bearer test-token-123
     Body Type: JSON
     Body: {"action":"list_tools"}
     ```

2. **Create Custom n8n Node**
   - Build a custom n8n node specifically for this MCP server
   - This would translate between n8n's expectations and the server's format

3. **Modify the Server**
   - Update the server to use standard MCP JSON-RPC protocol
   - This would require significant changes to the adapters/mcp_http.py

## Available Actions

The server supports these actions:

- `ping` - Health check
- `list_tools` - List all available tools (816+ Meraki tools)
- `call_tool` - Execute a specific tool
  - Requires: `name` (tool name) and `args` (tool arguments)
- `list_resources` - List available resources
- `read_resource` - Read a specific resource
  - Requires: `uri` parameter

## Example API Calls

### List all tools:
```bash
curl -X POST http://localhost:8100/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token-123" \
  -d '{"action":"list_tools"}'
```

### Call a tool (example: get organizations):
```bash
curl -X POST http://localhost:8100/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token-123" \
  -d '{
    "action": "call_tool",
    "name": "get_organizations",
    "args": {}
  }'
```

## Environment Variables

The server uses your Meraki API key from the .env file:
- `MERAKI_API_KEY=07947d21682606e2bbadf1c8942a25fafae4aeba`

## Next Steps

Since the standard n8n MCP Client Tool won't work with this custom adapter, you'll need to:

1. Use HTTP Request nodes in n8n to interact with the server
2. Or wait for the server to be updated to support standard MCP protocol
3. Or create a middleware that translates between the two protocols

The server is fully functional with 816+ Meraki tools available - it just uses a non-standard protocol for communication.