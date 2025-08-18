#!/usr/bin/env python3
"""
Remote MCP Server with FastAPI
Provides HTTP/WebSocket endpoints for remote MCP access
"""

import os
import json
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

from fastapi import FastAPI, HTTPException, Header, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field
import uvicorn

from .server import (
    MerakiClient,
    check_rate_limit,
    format_response,
    check_privileges,
    PRIVILEGED_USERS
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Meraki MCP Remote Server",
    description="Remote access to Meraki MCP tools via HTTP/WebSocket",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Meraki client
meraki_client: Optional[MerakiClient] = None

# Authentication tokens (in production, use a database)
AUTH_TOKENS: Dict[str, Dict[str, Any]] = {}

class ToolRequest(BaseModel):
    """Request model for tool execution"""
    tool: str
    params: Dict[str, Any] = Field(default_factory=dict)

class AuthRequest(BaseModel):
    """Authentication request"""
    username: str
    api_key: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize server on startup"""
    global meraki_client
    
    api_key = os.getenv("MERAKI_API_KEY")
    if not api_key:
        logger.error("MERAKI_API_KEY not set")
        return
    
    meraki_client = MerakiClient(api_key)
    logger.info("Remote MCP server started")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global meraki_client
    
    if meraki_client:
        await meraki_client.close()
    
    logger.info("Remote MCP server stopped")

def get_user_context(auth_token: str) -> Dict[str, Any]:
    """Get user context from auth token"""
    if auth_token.startswith("Bearer "):
        auth_token = auth_token[7:]
    
    user_data = AUTH_TOKENS.get(auth_token, {})
    return {
        "user_id": user_data.get("username", "anonymous"),
        "is_privileged": user_data.get("username") in PRIVILEGED_USERS,
        "created_at": user_data.get("created_at")
    }

@app.get("/")
async def home():
    """Home page with information"""
    html_content = """
    <html>
        <head>
            <title>Meraki MCP Remote Server</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
                pre { background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
                .endpoint { margin: 20px 0; padding: 10px; border-left: 3px solid #0366d6; }
            </style>
        </head>
        <body>
            <h1>🌐 Meraki MCP Remote Server</h1>
            <p>This server provides remote access to Meraki MCP tools via HTTP and WebSocket protocols.</p>
            
            <h2>Authentication</h2>
            <div class="endpoint">
                <code>POST /auth</code> - Authenticate and get access token
                <pre>{
  "username": "your-username",
  "api_key": "optional-override-api-key"
}</pre>
            </div>
            
            <h2>Tool Execution</h2>
            <div class="endpoint">
                <code>POST /api/v1/execute</code> - Execute MCP tool
                <pre>Headers: { "Authorization": "Bearer YOUR_TOKEN" }
Body: {
  "tool": "list_organizations",
  "params": {}
}</pre>
            </div>
            
            <h2>WebSocket (for Claude)</h2>
            <div class="endpoint">
                <code>WS /ws</code> - WebSocket endpoint for MCP protocol
            </div>
            
            <h2>Available Tools</h2>
            <ul>
                <li><code>list_organizations</code> - List all Meraki organizations</li>
                <li><code>get_organization_networks</code> - Get networks in an organization</li>
                <li><code>get_uplink_loss_latency</code> - Check uplink packet loss and latency</li>
                <li><code>create_ping_test</code> - Start a ping test from a device</li>
                <li><code>get_ping_test_results</code> - Get ping test results</li>
                <li><code>reboot_device</code> - Reboot a device (privileged users only)</li>
            </ul>
            
            <h2>Configuration for Claude Desktop</h2>
            <pre>{
  "mcpServers": {
    "meraki-remote": {
      "command": "npx",
      "args": ["@modelcontextprotocol/mcp-client-ws", "ws://your-server:8000/ws"],
      "env": {
        "AUTH_TOKEN": "your-auth-token"
      }
    }
  }
}</pre>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/auth")
async def authenticate(auth_request: AuthRequest):
    """Authenticate user and return token"""
    import secrets
    
    # Generate token
    token = secrets.token_urlsafe(32)
    
    # Store token (in production, use database)
    AUTH_TOKENS[token] = {
        "username": auth_request.username,
        "api_key": auth_request.api_key,
        "created_at": datetime.now().isoformat()
    }
    
    logger.info(f"User {auth_request.username} authenticated")
    
    return {
        "token": token,
        "username": auth_request.username,
        "is_privileged": auth_request.username in PRIVILEGED_USERS
    }

@app.post("/api/v1/execute")
async def execute_tool(
    request: ToolRequest,
    authorization: str = Header(None)
):
    """Execute an MCP tool"""
    if not authorization:
        raise HTTPException(401, "Authorization required")
    
    # Get user context
    context = get_user_context(authorization)
    user_id = context["user_id"]
    
    if user_id == "anonymous":
        raise HTTPException(401, "Invalid token")
    
    # Check rate limit
    if not check_rate_limit(user_id):
        raise HTTPException(429, "Rate limit exceeded")
    
    # Create mock context object for tools
    class MockContext:
        def __init__(self, meta):
            self.meta = meta
    
    mock_context = MockContext({"user_id": user_id})
    
    # Execute tool
    try:
        if request.tool == "list_organizations":
            from .server import list_organizations
            result = await list_organizations(mock_context)
            
        elif request.tool == "get_organization_networks":
            from .server import get_organization_networks
            result = await get_organization_networks(
                mock_context,
                org_id=request.params.get("org_id")
            )
            
        elif request.tool == "get_uplink_loss_latency":
            from .server import get_uplink_loss_latency
            result = await get_uplink_loss_latency(
                mock_context,
                org_id=request.params.get("org_id"),
                timespan=request.params.get("timespan", 300)
            )
            
        elif request.tool == "create_ping_test":
            from .server import create_ping_test
            result = await create_ping_test(
                mock_context,
                serial=request.params.get("serial"),
                target=request.params.get("target"),
                count=request.params.get("count", 5)
            )
            
        elif request.tool == "get_ping_test_results":
            from .server import get_ping_test_results
            result = await get_ping_test_results(
                mock_context,
                serial=request.params.get("serial"),
                ping_id=request.params.get("ping_id")
            )
            
        elif request.tool == "reboot_device":
            # Check if user is privileged
            if not context["is_privileged"]:
                raise HTTPException(403, "Permission denied: privileged operation")
            
            from .server import reboot_device
            result = await reboot_device(
                mock_context,
                serial=request.params.get("serial"),
                confirmation=request.params.get("confirmation")
            )
            
        else:
            raise HTTPException(404, f"Tool '{request.tool}' not found")
        
        # Convert TextContent to dict
        return {
            "success": True,
            "result": result[0].text if result else "No result",
            "user": user_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error executing tool {request.tool}: {e}")
        return {
            "success": False,
            "error": str(e),
            "user": user_id,
            "timestamp": datetime.now().isoformat()
        }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for MCP protocol"""
    await websocket.accept()
    
    try:
        # First message should be authentication
        auth_msg = await websocket.receive_json()
        token = auth_msg.get("token")
        
        if not token or token not in AUTH_TOKENS:
            await websocket.send_json({
                "error": "Authentication required",
                "code": "AUTH_REQUIRED"
            })
            await websocket.close()
            return
        
        user_context = get_user_context(f"Bearer {token}")
        logger.info(f"WebSocket connected: {user_context['user_id']}")
        
        # Handle MCP messages
        while True:
            message = await websocket.receive_json()
            
            # Process MCP protocol messages
            msg_type = message.get("type")
            
            if msg_type == "tool_call":
                # Execute tool via REST endpoint logic
                request = ToolRequest(
                    tool=message.get("tool"),
                    params=message.get("params", {})
                )
                
                # Mock authorization header
                auth_header = f"Bearer {token}"
                
                # Execute tool
                result = await execute_tool(request, auth_header)
                
                # Send response
                await websocket.send_json({
                    "type": "tool_response",
                    "id": message.get("id"),
                    "result": result
                })
                
            elif msg_type == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })
                
            else:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Unknown message type: {msg_type}"
                })
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "meraki_connected": meraki_client is not None
    }

# SSE endpoint for MCP-over-SSE
@app.get("/sse")
async def sse_endpoint(authorization: str = Header(None)):
    """Server-Sent Events endpoint for MCP protocol"""
    if not authorization:
        raise HTTPException(401, "Authorization required")
    
    context = get_user_context(authorization)
    if context["user_id"] == "anonymous":
        raise HTTPException(401, "Invalid token")
    
    async def event_generator():
        """Generate SSE events"""
        # Send initial connection event
        yield f"data: {json.dumps({'type': 'connected', 'user': context['user_id']})}\n\n"
        
        # Keep connection alive
        while True:
            await asyncio.sleep(30)
            yield f"data: {json.dumps({'type': 'ping', 'timestamp': datetime.now().isoformat()})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

def main():
    """Run the server"""
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()