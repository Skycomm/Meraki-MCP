#!/usr/bin/env python3
"""
Cisco Meraki MCP Server - SSE/HTTP Implementation
Supports MCP protocol over SSE, Streamable HTTP, and REST API
"""

import os
import json
import asyncio
import logging
import secrets
from typing import Optional, Dict, Any, List
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import our modules
from config import MERAKI_API_KEY, SERVER_NAME, SERVER_VERSION
from meraki_client import MerakiClient
from tool_registry import ALL_TOOLS, TOOL_METADATA, set_meraki_client
from mcp_protocol import MCPHandler

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
meraki_client: Optional[MerakiClient] = None
auth_tokens: Dict[str, Dict[str, Any]] = {}
rate_limiter: Dict[str, List[float]] = {}

# Configuration
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
PRIVILEGED_USERS = os.getenv("PRIVILEGED_USERS", "").split(",")

# Security
security = HTTPBearer()

# Request/Response models
class AuthRequest(BaseModel):
    username: str
    password: Optional[str] = None

class ToolRequest(BaseModel):
    tool: str
    arguments: Dict[str, Any] = Field(default_factory=dict)

class ToolResponse(BaseModel):
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    timestamp: str
    user: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage server lifecycle"""
    global meraki_client
    
    # Startup
    logger.info("Starting Meraki MCP SSE/HTTP Server")
    
    if not MERAKI_API_KEY:
        logger.error("MERAKI_API_KEY not set!")
    else:
        meraki_client = MerakiClient()
        set_meraki_client(meraki_client)
        logger.info("Meraki client initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Meraki MCP SSE/HTTP Server")

# Create FastAPI app
app = FastAPI(
    title="Cisco Meraki MCP Server - SSE/HTTP",
    description="MCP server for Cisco Meraki with SSE, Streamable HTTP, and REST API support",
    version=SERVER_VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_rate_limit(user_id: str) -> bool:
    """Check if user has exceeded rate limit"""
    import time
    now = time.time()
    user_requests = rate_limiter.get(user_id, [])
    
    # Filter requests within the time window
    recent_requests = [t for t in user_requests if now - t < RATE_LIMIT_WINDOW]
    
    if len(recent_requests) >= RATE_LIMIT_REQUESTS:
        return False
    
    # Add current request
    recent_requests.append(now)
    rate_limiter[user_id] = recent_requests
    
    return True

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Verify auth token"""
    token = credentials.credentials
    
    if token not in auth_tokens:
        raise HTTPException(401, "Invalid authentication token")
    
    return auth_tokens[token]

@app.get("/")
async def home():
    """Home page with information"""
    return {
        "name": SERVER_NAME,
        "version": SERVER_VERSION,
        "description": "Cisco Meraki MCP Server with SSE/HTTP support",
        "endpoints": {
            "auth": "POST /auth - Get authentication token",
            "sse": "GET/POST /sse - MCP protocol over SSE",
            "mcp": "POST /mcp - Streamable HTTP endpoint",
            "rest": "POST /api/v1/tools/{tool_name} - Direct tool access",
            "tools": "GET /api/v1/tools - List available tools"
        }
    }

@app.post("/auth")
async def authenticate(auth_req: AuthRequest):
    """Simple authentication"""
    token = secrets.token_urlsafe(32)
    
    auth_tokens[token] = {
        "username": auth_req.username,
        "created_at": datetime.now().isoformat(),
        "is_privileged": auth_req.username in PRIVILEGED_USERS
    }
    
    return {
        "token": token,
        "username": auth_req.username,
        "is_privileged": auth_tokens[token]["is_privileged"]
    }

@app.get("/api/v1/tools")
async def list_tools(user_data: Dict = Depends(verify_token)):
    """List all available tools"""
    tools = []
    
    dangerous_tools = [
        "reboot_device", "confirm_reboot_device",
        "reboot_network_sm_devices", "confirm_reboot_network_sm_devices",
        "delete_organization", "delete_network",
        "delete_organization_policy_object"
    ]
    
    for tool_name in sorted(ALL_TOOLS.keys()):
        # Skip dangerous tools for non-privileged users
        if tool_name in dangerous_tools and not user_data["is_privileged"]:
            continue
        
        metadata = TOOL_METADATA.get(tool_name, {})
        tools.append({
            "name": tool_name,
            "description": metadata.get("description", ""),
            "parameters": metadata.get("parameters", [])
        })
    
    return {
        "tools": tools,
        "total": len(tools),
        "user": user_data["username"],
        "is_privileged": user_data["is_privileged"]
    }

@app.post("/api/v1/tools/{tool_name}")
async def execute_tool(
    tool_name: str,
    request: ToolRequest,
    user_data: Dict = Depends(verify_token)
) -> ToolResponse:
    """Execute a specific tool via REST API"""
    username = user_data["username"]
    
    # Check rate limit
    if not check_rate_limit(username):
        return ToolResponse(
            success=False,
            error="Rate limit exceeded",
            timestamp=datetime.now().isoformat(),
            user=username
        )
    
    # Check if tool exists
    if tool_name not in ALL_TOOLS:
        return ToolResponse(
            success=False,
            error=f"Unknown tool: {tool_name}",
            timestamp=datetime.now().isoformat(),
            user=username
        )
    
    # Check privileges for dangerous operations
    dangerous_tools = [
        "reboot_device", "confirm_reboot_device",
        "reboot_network_sm_devices", "confirm_reboot_network_sm_devices",
        "delete_organization", "delete_network",
        "delete_organization_policy_object"
    ]
    
    if tool_name in dangerous_tools and not user_data["is_privileged"]:
        return ToolResponse(
            success=False,
            error="Permission denied: privileged operation",
            timestamp=datetime.now().isoformat(),
            user=username
        )
    
    # Execute tool
    try:
        tool_func = ALL_TOOLS[tool_name]
        
        # Execute with or without arguments
        if request.arguments:
            result = await tool_func(**request.arguments)
        else:
            result = await tool_func()
        
        return ToolResponse(
            success=True,
            result=result,
            timestamp=datetime.now().isoformat(),
            user=username
        )
        
    except Exception as e:
        logger.error(f"Error executing {tool_name}: {e}")
        return ToolResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat(),
            user=username
        )

@app.get("/sse")
async def handle_sse(request: Request):
    """SSE endpoint for MCP protocol"""
    # Get token from header or query
    auth = request.headers.get("authorization", "")
    token = auth.replace("Bearer ", "") if auth else request.query_params.get("token")
    
    if not token or token not in auth_tokens:
        raise HTTPException(401, "Invalid token")
    
    username = auth_tokens[token]["username"]
    logger.info(f"SSE connection from {username}")
    
    # Create MCP handler
    mcp_handler = MCPHandler(ALL_TOOLS, TOOL_METADATA)
    
    # SSE event generator
    async def event_generator():
        # Send initialization response
        init_response = {
            "jsonrpc": "2.0",
            "id": 0,
            "result": {
                "protocolVersion": "2025-03-26",
                "serverInfo": {
                    "name": SERVER_NAME,
                    "version": SERVER_VERSION
                },
                "capabilities": {
                    "tools": {}
                }
            }
        }
        yield f"data: {json.dumps(init_response)}\n\n"
        
        # Keep connection alive
        while True:
            await asyncio.sleep(30)
            # Send keepalive
            keepalive = {
                "jsonrpc": "2.0",
                "method": "ping",
                "params": {}
            }
            yield f"data: {json.dumps(keepalive)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive"
        }
    )

@app.post("/sse")
async def handle_sse_post(request: Request):
    """Handle SSE POST requests for bidirectional MCP communication"""
    auth = request.headers.get("authorization", "")
    token = auth.replace("Bearer ", "") if auth else None
    
    if not token or token not in auth_tokens:
        raise HTTPException(401, "Invalid token")
    
    user_data = auth_tokens[token]
    
    # Handle the MCP message
    data = await request.json()
    logger.info(f"MCP message received: {data.get('method', 'unknown')}")
    
    # Create handler and process message
    mcp_handler = MCPHandler(ALL_TOOLS, TOOL_METADATA)
    response = await mcp_handler.handle_message(data, user_data)
    
    return JSONResponse(response)

@app.post("/mcp")
async def handle_mcp_stream(request: Request):
    """Streamable HTTP endpoint for MCP protocol"""
    # Get token and session ID from headers
    auth = request.headers.get("authorization", "")
    token = auth.replace("Bearer ", "") if auth else None
    session_id = request.headers.get("mcp-session-id")
    
    if not token or token not in auth_tokens:
        raise HTTPException(401, "Invalid token")
    
    user_data = auth_tokens[token]
    username = user_data["username"]
    logger.info(f"MCP stream connection from {username} (session: {session_id})")
    
    # Handle the MCP message
    data = await request.json()
    logger.info(f"MCP stream message: {data.get('method', 'unknown')}")
    
    # Create handler and process message
    mcp_handler = MCPHandler(ALL_TOOLS, TOOL_METADATA)
    response = await mcp_handler.handle_message(data, user_data)
    
    # Add session ID to header if this is initialization
    headers = {}
    if data.get("method") == "initialize" and not session_id:
        headers["Mcp-Session-Id"] = secrets.token_urlsafe(32)
    
    return JSONResponse(response, headers=headers)

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "meraki_connected": meraki_client is not None,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)