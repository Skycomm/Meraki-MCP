#!/usr/bin/env python3
"""
Simple MCP HTTP Server for n8n
Standard HTTP JSON-RPC 2.0 - no SSE, no streaming, just simple request/response
"""

import os
import json
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Any, Dict
import uvicorn

# Import the MCP app
from server.main import app as mcp_app

# Create FastAPI instance
api = FastAPI(title="Meraki MCP Server (Simple HTTP)")

@api.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "protocol": "MCP JSON-RPC 2.0"}

@api.post("/mcp")
async def handle_mcp(request: Request):
    """Handle MCP JSON-RPC 2.0 requests - simple HTTP, no streaming"""
    try:
        body = await request.json()
        
        # Extract JSON-RPC fields
        jsonrpc = body.get("jsonrpc", "2.0")
        method = body.get("method")
        params = body.get("params", {})
        req_id = body.get("id")
        
        if not method:
            return JSONResponse({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32600,
                    "message": "Invalid Request: missing method"
                },
                "id": req_id
            })
        
        # Handle different MCP methods
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
                return JSONResponse({
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32602,
                        "message": "Invalid params: missing tool name"
                    },
                    "id": req_id
                })
            
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
                return JSONResponse({
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32602,
                        "message": "Invalid params: missing uri"
                    },
                    "id": req_id
                })
            
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
            return JSONResponse({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                },
                "id": req_id
            })
        
        # Return successful response
        return JSONResponse({
            "jsonrpc": "2.0",
            "result": result,
            "id": req_id
        })
        
    except json.JSONDecodeError:
        return JSONResponse({
            "jsonrpc": "2.0",
            "error": {
                "code": -32700,
                "message": "Parse error"
            },
            "id": None
        })
    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            },
            "id": body.get("id") if 'body' in locals() else None
        })

# Add CORS middleware for n8n
from fastapi.middleware.cors import CORSMiddleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8100"))
    
    print(f"🚀 Starting Simple MCP HTTP Server")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔗 Endpoint: http://{host}:{port}/mcp")
    print(f"🛡️  Authentication: DISABLED")
    print(f"📊 Protocol: Standard JSON-RPC 2.0 (no streaming)")
    print("")
    print("📝 n8n MCP Client Configuration:")
    print(f"   Endpoint URL: http://meraki-mcp-server:{port}/mcp")
    print(f"   Server Transport: http")
    print(f"   Authentication: none")
    print("")
    
    uvicorn.run(api, host=host, port=port)