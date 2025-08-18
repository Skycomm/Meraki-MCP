# Meraki MCP Server - Current Status

## Architecture Overview

We have two server implementations:

### 1. Original STDIO Server (Recommended for Claude Desktop)
- **Location**: `/Users/david/docker/cisco-meraki-mcp-server-tvi/`
- **Protocol**: stdio (standard input/output)
- **Tools**: All 97 tools with full MCP protocol support
- **Use**: Claude Desktop config entry `"meraki-mcp"`

### 2. Hybrid HTTP Server (For n8n and Network Access)
- **Location**: `/Users/david/docker/cisco-meraki-mcp-server-tvi/python/src/hybrid_server.py`
- **Running at**: http://10.0.5.188:8000
- **Auth Token**: zmGlz_WLbMJU-sFdz6k4AW-CnKHItcGby7wiSMSo5Oc
- **Tools**: All 97 tools available via REST API

## Endpoints

### REST API (Works perfectly)
- **POST /api/v1/execute** - Execute any tool
- **GET /api/v1/tools** - List all available tools
- **POST /auth** - Get authentication token

### MCP Protocol Endpoints (Experimental)
- **POST /mcp** - HTTP Stream endpoint (partial implementation)
- **GET /sse** - Server-Sent Events (legacy, partial implementation)
- **POST /sse** - SSE message handler

## Current Limitations

1. **MCP Protocol**: The hybrid server has basic MCP protocol support, but not the full bidirectional streaming that Claude Desktop expects. This is why we see JSON parsing errors.

2. **Transport Mismatch**: Claude Desktop expects stdio transport, while our hybrid server provides HTTP-based transports (SSE/Stream).

## Recommended Usage

### For Claude Desktop
Use the original stdio server:
```json
"meraki-mcp": {
  "command": "/bin/bash",
  "args": ["/Users/david/docker/cisco-meraki-mcp-server-tvi/run_meraki_server.sh"],
  "cwd": "/Users/david/docker/cisco-meraki-mcp-server-tvi",
  "env": {
    "MERAKI_API_KEY": "1ac5962056ad56da8cea908864f136adc5878a43"
  }
}
```

### For n8n
Use the hybrid server's REST API:
1. **HTTP Request Node**: 
   - URL: http://10.0.5.188:8000/api/v1/execute
   - Method: POST
   - Auth: Bearer zmGlz_WLbMJU-sFdz6k4AW-CnKHItcGby7wiSMSo5Oc

2. **MCP Client Tool** (if it supports HTTP):
   - Try /mcp endpoint at http://10.0.5.188:8000/mcp
   - Or /sse endpoint at http://10.0.5.188:8000/sse

## Why This Approach?

1. **Claude Desktop** works best with stdio transport (original server)
2. **n8n** works best with HTTP/REST APIs (hybrid server)
3. Full MCP-over-HTTP implementation requires complex bidirectional streaming that's non-trivial to implement

## All 97 Available Tools

Both servers provide the same 97 tools across these categories:
- Organization Management (6 tools)
- Network Management (7 tools)
- Device Management (8 tools)
- Monitoring & Analytics (10 tools)
- Security & Policy (12 tools)
- Wireless (9 tools)
- Switch (5 tools)
- Camera (6 tools)
- Systems Manager (7 tools)
- Live Tools (10 tools)
- Licensing (6 tools)
- Beta Features (6 tools)
- Appliance (5 tools)