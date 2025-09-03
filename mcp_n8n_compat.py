#!/usr/bin/env python3
"""
MCP Server with n8n-compatible HTTP Streamable
Keeps connection open and streams responses
"""

import os
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import uvicorn

# Import the MCP app
from server.main import app as mcp_app

# Create FastAPI instance
api = FastAPI(title="Meraki MCP Server (n8n Compatible)")

@api.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "protocol": "MCP n8n-compatible"}

async def mcp_stream_handler(body: dict) -> AsyncGenerator[bytes, None]:
    """Handle MCP request with streaming response that keeps connection alive"""
    try:
        # Extract JSON-RPC fields
        method = body.get("method")
        params = body.get("params", {})
        req_id = body.get("id")
        
        # Process based on method
        result = None
        
        if method == "initialize":
            result = {
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"listChanged": False}
                },
                "serverInfo": {
                    "name": "Meraki MCP Server",
                    "version": "1.0.0"
                }
            }
            
        elif method == "tools/list":
            tools = await mcp_app.list_tools()
            result = {
                "tools": [
                    {
                        "name": str(tool.name) if hasattr(tool, 'name') else str(tool),
                        "description": str(tool.description) if hasattr(tool, 'description') else "",
                        "inputSchema": tool.input_schema if hasattr(tool, 'input_schema') else {}
                    }
                    for tool in tools
                ]
            }
            
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if not tool_name:
                raise ValueError("Missing tool name")
            
            tool_result = await mcp_app.call_tool(tool_name, tool_args)
            result = {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(tool_result, indent=2) if not isinstance(tool_result, str) else tool_result
                    }
                ]
            }
            
        elif method == "resources/list":
            resources = await mcp_app.list_resources()
            result = {
                "resources": [
                    {
                        "uri": str(r.uri) if hasattr(r, 'uri') else "",
                        "name": str(r.name) if hasattr(r, 'name') else "",
                        "description": str(r.description) if hasattr(r, 'description') else "",
                        "mimeType": str(r.mimeType) if hasattr(r, 'mimeType') else "text/plain"
                    }
                    for r in resources
                ]
            }
            
        elif method == "resources/read":
            uri = params.get("uri")
            if not uri:
                raise ValueError("Missing uri")
            
            contents = await mcp_app.read_resource(uri)
            result = {
                "contents": [
                    {
                        "uri": str(c.uri) if hasattr(c, 'uri') else uri,
                        "mimeType": str(c.mimeType) if hasattr(c, 'mimeType') else "text/plain",
                        "text": str(c.text) if hasattr(c, 'text') else ""
                    }
                    for c in contents
                ]
            }
            
        elif method == "ping":
            result = {"pong": True}
            
        else:
            # For unknown methods, return empty result
            result = {}
        
        # Create response
        response = {
            "jsonrpc": "2.0",
            "result": result,
            "id": req_id
        }
        
        # Send the response as newline-delimited JSON
        response_data = json.dumps(response) + "\n"
        yield response_data.encode('utf-8')
        
        # Keep connection alive with heartbeats
        # This helps n8n know the connection is still active
        heartbeat_count = 0
        while heartbeat_count < 5:  # Send 5 heartbeats then close
            await asyncio.sleep(1)  # Wait 1 second
            heartbeat = {
                "jsonrpc": "2.0",
                "method": "heartbeat",
                "params": {"timestamp": heartbeat_count},
                "id": None
            }
            yield (json.dumps(heartbeat) + "\n").encode('utf-8')
            heartbeat_count += 1
            
    except asyncio.CancelledError:
        # Client disconnected
        pass
    except Exception as e:
        error_response = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": str(e)
            },
            "id": body.get("id")
        }
        yield (json.dumps(error_response) + "\n").encode('utf-8')

@api.post("/mcp")
async def handle_mcp(request: Request):
    """Handle MCP requests with n8n-compatible streaming"""
    try:
        body = await request.json()
    except:
        # If no JSON body, treat as initialization request
        body = {"method": "initialize", "id": 1}
    
    # Return streaming response with proper headers
    return StreamingResponse(
        mcp_stream_handler(body),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Content-Type-Options": "nosniff"
        }
    )

# Add lenient CORS for n8n
from fastapi.middleware.cors import CORSMiddleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

if __name__ == "__main__":
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8100"))
    
    print(f"🚀 Starting MCP Server (n8n Compatible)")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔗 Endpoint: http://{host}:{port}/mcp")
    print(f"🛡️  Authentication: DISABLED")
    print(f"📊 Protocol: HTTP Streamable with keep-alive")
    print(f"💓 Heartbeat: Enabled (5 beats)")
    print("")
    print("📝 n8n MCP Client Configuration:")
    print(f"   Endpoint URL: http://meraki-mcp-server:{port}/mcp")
    print(f"   Server Transport: httpStreamable")
    print(f"   Authentication: none")
    print("")
    
    uvicorn.run(api, host=host, port=port)