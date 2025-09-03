#!/usr/bin/env python3
"""
Debug MCP Server to see what n8n is actually sending
"""

import os
import json
import asyncio
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse, PlainTextResponse
import uvicorn
from datetime import datetime

# Import the MCP app
from server.main import app as mcp_app

# Create FastAPI instance
api = FastAPI(title="Meraki MCP Debug Server")

@api.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "protocol": "MCP Debug"}

@api.api_route("/mcp", methods=["GET", "POST", "OPTIONS"])
async def handle_all_mcp(request: Request):
    """Debug handler that logs everything and tries to respond appropriately"""
    
    # Log the request details
    print(f"\n{'='*60}")
    print(f"[{datetime.now()}] REQUEST RECEIVED")
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Headers: {dict(request.headers)}")
    
    # Handle OPTIONS for CORS
    if request.method == "OPTIONS":
        return Response(
            content="",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*"
            }
        )
    
    # Try to get body if it's a POST
    body = None
    if request.method == "POST":
        try:
            body = await request.json()
            print(f"Body (JSON): {json.dumps(body, indent=2)}")
        except:
            try:
                body_bytes = await request.body()
                print(f"Body (raw): {body_bytes}")
                body = {"method": "initialize", "id": 1}
            except:
                print("Could not read body")
                body = {"method": "initialize", "id": 1}
    else:
        # For GET requests, assume initialization
        body = {"method": "initialize", "id": 1}
        print(f"GET request - using default body: {body}")
    
    # Check what the client accepts
    accept_header = request.headers.get("accept", "").lower()
    print(f"Accept header: {accept_header}")
    
    # Prepare response
    method = body.get("method", "initialize")
    req_id = body.get("id", 1)
    
    # Simple responses for common methods
    if method == "initialize":
        # Match n8n's protocol version
        protocol_version = body.get("params", {}).get("protocolVersion", "2025-03-26")
        result = {
            "protocolVersion": protocol_version,
            "capabilities": {
                "tools": {},
                "resources": {}
            },
            "serverInfo": {
                "name": "Meraki MCP Server",
                "version": "1.0.0"
            }
        }
    elif method == "tools/list":
        tools = await mcp_app.list_tools()
        tool_list = []
        # n8n has a limit of 128 tools maximum
        for tool in tools[:128]:
            tool_dict = tool.model_dump() if hasattr(tool, 'model_dump') else {}
            
            # Extract the inputSchema - it should already be properly formatted
            schema = tool_dict.get('inputSchema', {
                "type": "object",
                "properties": {},
                "required": []
            })
            
            # Ensure required fields exist
            if not isinstance(schema, dict):
                schema = {"type": "object", "properties": {}, "required": []}
            if "type" not in schema:
                schema["type"] = "object"
            if "properties" not in schema:
                schema["properties"] = {}
            if "required" not in schema:
                schema["required"] = []
            
            # Fix array properties that are missing or have empty items field
            if isinstance(schema.get('properties'), dict):
                for prop_name, prop_value in schema['properties'].items():
                    if isinstance(prop_value, dict) and prop_value.get('type') == 'array':
                        if 'items' not in prop_value:
                            # Add a generic items schema for arrays
                            prop_value['items'] = {"type": "object"}
                        elif isinstance(prop_value['items'], dict) and not prop_value['items']:
                            # Fix empty items object
                            prop_value['items'] = {"type": "object"}
                        elif isinstance(prop_value['items'], dict) and 'type' not in prop_value['items']:
                            # Ensure items has at least a type
                            prop_value['items']['type'] = "object"
            
            # Remove optional fields that might confuse n8n
            schema.pop('title', None)
            schema.pop('additionalProperties', None)
            
            tool_list.append({
                "name": tool_dict.get('name', ''),
                "description": tool_dict.get('description', ''),
                "inputSchema": schema
            })
        
        result = {"tools": tool_list}
    else:
        result = {}
    
    response_data = {
        "jsonrpc": "2.0",
        "result": result,
        "id": req_id
    }
    
    print(f"Response prepared: {json.dumps(response_data)[:200]}...")
    
    # Return based on Accept header
    if "event-stream" in accept_header:
        print("Returning SSE response")
        async def generate():
            # Ensure proper SSE format with double newline
            yield f"data: {json.dumps(response_data)}\n\n"
        return StreamingResponse(
            generate(), 
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        )
    elif "ndjson" in accept_header or "x-ndjson" in accept_header:
        print("Returning NDJSON response")
        async def generate():
            yield json.dumps(response_data) + "\n"
        return StreamingResponse(generate(), media_type="application/x-ndjson")
    else:
        print("Returning standard JSON response")
        return response_data

@api.api_route("/mcp/sse", methods=["GET", "POST", "OPTIONS"])
async def handle_sse_endpoint(request: Request):
    """Dedicated SSE endpoint"""
    print(f"\n[{datetime.now()}] SSE ENDPOINT HIT")
    print(f"Method: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    
    if request.method == "OPTIONS":
        return Response(
            content="",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*"
            }
        )
    
    # Simple SSE response
    async def generate():
        response = {
            "jsonrpc": "2.0",
            "result": {
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"listChanged": False}
                },
                "serverInfo": {
                    "name": "Meraki MCP Server",
                    "version": "1.0.0"
                }
            },
            "id": 1
        }
        yield f"data: {json.dumps(response)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

# Add CORS middleware
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
    
    print(f"🔍 Starting MCP DEBUG Server")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔗 Endpoints:")
    print(f"   - http://{host}:{port}/mcp")
    print(f"   - http://{host}:{port}/mcp/sse")
    print(f"🛡️  Authentication: DISABLED")
    print(f"📊 This server logs ALL requests for debugging")
    print("")
    print("📝 Try these in n8n MCP Client:")
    print(f"   1. Endpoint: http://meraki-mcp-server:{port}/mcp")
    print(f"      Transport: httpStreamable or sse")
    print(f"   2. Endpoint: http://meraki-mcp-server:{port}/mcp/sse")
    print(f"      Transport: sse")
    print("")
    
    uvicorn.run(api, host=host, port=port, log_level="debug")