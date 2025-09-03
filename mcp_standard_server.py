#!/usr/bin/env python3
"""
Standard MCP HTTP Server for n8n Integration
Implements JSON-RPC 2.0 with SSE/Streaming support for httpStreamable transport
"""

import os
import json
import asyncio
from fastapi import FastAPI, Request, HTTPException, Header, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from sse_starlette.sse import EventSourceResponse
from typing import Optional, Any, Dict, AsyncGenerator
import uvicorn

# Import the MCP app
from server.main import app as mcp_app

# Create FastAPI instance
api = FastAPI(title="Meraki MCP Server (httpStreamable)")

# Authentication disabled for testing
DISABLE_AUTH = True

async def verify_auth(authorization: Optional[str] = Header(None)):
    """Verify Bearer token authentication (currently disabled)"""
    if DISABLE_AUTH:
        return True
    
    AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN", "")
    if not AUTH_TOKEN:
        return True  # No auth if token not set
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    
    token = authorization.replace("Bearer ", "")
    if token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True

@api.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "protocol": "MCP JSON-RPC 2.0 with httpStreamable"}

async def process_mcp_request(method: str, params: dict, req_id: Any) -> Any:
    """Process MCP request and return result"""
    if not method:
        raise ValueError("Invalid Request: missing method")
    
    # Handle different MCP methods
    if method == "initialize":
        return {
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
        return {
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
            raise ValueError("Invalid params: missing tool name")
        
        tool_result = await mcp_app.call_tool(tool_name, tool_args)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(tool_result, indent=2) if not isinstance(tool_result, str) else tool_result
                }
            ]
        }
    
    elif method == "resources/list":
        resources = await mcp_app.list_resources()
        return {
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
            raise ValueError("Invalid params: missing uri")
        
        contents = await mcp_app.read_resource(uri)
        return {
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
        return {"pong": True}
    
    else:
        raise ValueError(f"Method not found: {method}")

async def sse_generator(body: dict) -> AsyncGenerator[str, None]:
    """Generate SSE events for streaming responses"""
    try:
        # Extract JSON-RPC fields
        jsonrpc = body.get("jsonrpc", "2.0")
        method = body.get("method")
        params = body.get("params", {})
        req_id = body.get("id")
        
        # Process the request and generate response
        result = await process_mcp_request(method, params, req_id)
        
        # Send as SSE event
        response = {
            "jsonrpc": "2.0",
            "result": result,
            "id": req_id
        }
        
        # Yield the response (EventSourceResponse adds "data: " prefix automatically)
        yield json.dumps(response)
        
        # Keep connection alive with heartbeat every 30 seconds
        # This prevents timeout issues with n8n
        while True:
            await asyncio.sleep(30)
            yield json.dumps({"jsonrpc": "2.0", "method": "heartbeat", "id": None})
            
    except asyncio.CancelledError:
        # Connection closed by client
        pass
    except Exception as e:
        error_response = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": str(e)
            },
            "id": body.get("id") if 'body' in locals() else None
        }
        yield json.dumps(error_response)

@api.post("/mcp/sse")
async def handle_mcp_sse(request: Request, auth_ok: bool = Depends(verify_auth)):
    """Handle MCP requests with Server-Sent Events (SSE) streaming"""
    body = await request.json()
    return EventSourceResponse(sse_generator(body), media_type="text/event-stream")

@api.post("/mcp")
async def handle_mcp(request: Request, auth_ok: bool = Depends(verify_auth)):
    """Handle MCP requests - supports both standard and streaming"""
    # Check if client wants SSE streaming
    accept = request.headers.get("accept", "")
    if "text/event-stream" in accept:
        body = await request.json()
        return EventSourceResponse(sse_generator(body), media_type="text/event-stream")
    
    # Standard JSON response
    try:
        body = await request.json()
        
        # Extract JSON-RPC fields
        jsonrpc = body.get("jsonrpc", "2.0")
        method = body.get("method")
        params = body.get("params", {})
        req_id = body.get("id")
        
        # Process the request
        try:
            result = await process_mcp_request(method, params, req_id)
        except ValueError as e:
            # Known errors (invalid params, method not found, etc.)
            error_code = -32601 if "Method not found" in str(e) else -32602
            return JSONResponse({
                "jsonrpc": "2.0",
                "error": {
                    "code": error_code,
                    "message": str(e)
                },
                "id": req_id
            })
        except Exception as e:
            # Internal errors
            return JSONResponse({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
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
    
    print(f"🚀 Starting MCP Server with httpStreamable Support")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔗 Endpoint: http://{host}:{port}/mcp")
    print(f"🌊 SSE Endpoint: http://{host}:{port}/mcp/sse")
    print(f"🛡️  Authentication: {'DISABLED' if DISABLE_AUTH else 'ENABLED'}")
    print(f"📊 Protocol: JSON-RPC 2.0 with httpStreamable (n8n compatible)")
    print("")
    print("📝 n8n MCP Client Configuration:")
    print(f"   Endpoint URL: http://localhost:{port}/mcp")
    print(f"   Server Transport: httpStreamable")
    print(f"   Authentication: {'none' if DISABLE_AUTH else 'headerAuth'}")
    print("")
    
    uvicorn.run(api, host=host, port=port)