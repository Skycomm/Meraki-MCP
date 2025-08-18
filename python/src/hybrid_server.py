#!/usr/bin/env python3
"""
Hybrid Meraki MCP Server - Best of All Worlds
Supports both MCP protocol (for Claude) and REST API (for n8n)
Based on Cole's remote-mcp-server-with-auth patterns
"""

import os
import json
import asyncio
import logging
from typing import Optional, Dict, Any, List
import time
from datetime import datetime
import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.types as types

# Import all Meraki tools
from meraki_tools_simple import set_meraki_client, ALL_TOOLS
from mcp_sse_bridge import MCPSSEHandler

# Configuration
PRIVILEGED_USERS = os.getenv("PRIVILEGED_USERS", "").split(",")
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60

# Rate limiting storage
rate_limiter: Dict[str, List[float]] = {}

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

# Meraki client class
class MerakiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.meraki.com/api/v1"
        self.client = None
    
    async def _ensure_client(self):
        if not self.client:
            import httpx
            self.client = httpx.AsyncClient(
                headers={
                    "X-Cisco-Meraki-API-Key": self.api_key,
                    "Content-Type": "application/json"
                },
                timeout=30.0
            )
    
    async def get(self, endpoint: str, use_cache: bool = True):
        await self._ensure_client()
        response = await self.client.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return response.json()
    
    async def post(self, endpoint: str, data: Dict = None):
        await self._ensure_client()
        response = await self.client.post(f"{self.base_url}{endpoint}", json=data or {})
        response.raise_for_status()
        return response.json() if response.content else {}
    
    async def close(self):
        if self.client:
            await self.client.aclose()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Auth tokens storage
AUTH_TOKENS: Dict[str, Dict[str, Any]] = {}

# Security
security = HTTPBearer()

# Global Meraki client
meraki_client: Optional[MerakiClient] = None

# Note: MCP protocol is handled via SSE bridge, not the mcp.Server directly

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage server lifecycle"""
    global meraki_client
    
    # Startup
    api_key = os.getenv("MERAKI_API_KEY")
    if not api_key:
        logger.error("MERAKI_API_KEY not set!")
    else:
        meraki_client = MerakiClient(api_key)
        logger.info("Meraki client initialized")
        
        # Set meraki_client in tools module
        set_meraki_client(meraki_client)
        logger.info("Meraki client set in tools module")
    
    yield
    
    # Shutdown
    if meraki_client:
        await meraki_client.close()
        logger.info("Meraki client closed")

# Create FastAPI app
app = FastAPI(
    title="Meraki MCP Hybrid Server",
    description="Works with both Claude Desktop (MCP) and n8n (REST API)",
    lifespan=lifespan
)

# CORS for n8n
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class AuthRequest(BaseModel):
    username: str
    password: Optional[str] = None  # Optional, we use simple auth

class ToolRequest(BaseModel):
    tool: str
    arguments: Dict[str, Any] = Field(default_factory=dict)

class ToolResponse(BaseModel):
    success: bool
    result: Optional[str] = None
    error: Optional[str] = None
    timestamp: str
    user: str

# Authentication dependency
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Verify auth token"""
    token = credentials.credentials
    
    if token not in AUTH_TOKENS:
        raise HTTPException(401, "Invalid authentication token")
    
    return AUTH_TOKENS[token]

# Tools are already imported from meraki_tools_simple

# REST API Endpoints
@app.get("/")
async def home():
    """Home page with documentation"""
    return HTMLResponse("""
    <html>
        <head>
            <title>Meraki MCP Hybrid Server</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; }
                code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
                pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
                .endpoint { margin: 20px 0; padding: 15px; border-left: 3px solid #0366d6; }
            </style>
        </head>
        <body>
            <h1>🌐 Meraki MCP Hybrid Server</h1>
            <p>This server supports both MCP protocol (Claude Desktop) and REST API (n8n).</p>
            
            <h2>Quick Start</h2>
            
            <h3>1. Get Auth Token</h3>
            <div class="endpoint">
                <pre>curl -X POST http://localhost:8000/auth \\
  -H "Content-Type: application/json" \\
  -d '{"username": "your-name"}'</pre>
            </div>
            
            <h3>2. For n8n: Use REST API</h3>
            <div class="endpoint">
                <pre>curl -X POST http://localhost:8000/api/v1/execute \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "tool": "list_organizations",
    "arguments": {}
  }'</pre>
            </div>
            
            <h3>3. For Claude Desktop: Use MCP</h3>
            <div class="endpoint">
                <pre>{
  "mcpServers": {
    "meraki": {
      "command": "curl",
      "args": ["-N", "-H", "Authorization: Bearer YOUR_TOKEN", 
               "http://localhost:8000/sse"],
      "transport": "sse"
    }
  }
}</pre>
            </div>
            
            <h2>Available Tools (97 Total)</h2>
            <p>The server provides access to all 97 Meraki API tools across these categories:</p>
            
            <h3>📋 Organization Management (8 tools)</h3>
            <ul>
                <li>List, create, update, delete organizations</li>
                <li>Manage firmware, alerts, and networks</li>
            </ul>
            
            <h3>🌐 Network Management (6 tools)</h3>
            <ul>
                <li>List, create, update, delete networks</li>
                <li>Get network devices and clients</li>
            </ul>
            
            <h3>📡 Device Management (6 tools)</h3>
            <ul>
                <li>Get device info, status, clients</li>
                <li>Update settings, reboot devices</li>
            </ul>
            
            <h3>🔔 Alerts & Webhooks (6 tools)</h3>
            <ul>
                <li>Configure webhooks and alert settings</li>
                <li>Manage notification destinations</li>
            </ul>
            
            <h3>📊 Analytics & Monitoring (10 tools)</h3>
            <ul>
                <li>Uplink loss/latency, connection stats</li>
                <li>CPU/memory usage, API analytics</li>
            </ul>
            
            <h3>🔒 Security & Policy (12 tools)</h3>
            <ul>
                <li>Firewall rules, content filtering</li>
                <li>VPN, malware protection, intrusion detection</li>
                <li>Policy objects and groups</li>
            </ul>
            
            <h3>🎥 Camera Management (6 tools)</h3>
            <ul>
                <li>Video links, snapshots, settings</li>
                <li>Analytics zones and sense data</li>
            </ul>
            
            <h3>📱 Systems Manager (7 tools)</h3>
            <ul>
                <li>Device management, apps, profiles</li>
                <li>Performance history and reboots</li>
            </ul>
            
            <h3>🔌 Switch Management (5 tools)</h3>
            <ul>
                <li>Port configuration and status</li>
                <li>VLAN management</li>
            </ul>
            
            <h3>📶 Wireless Management (9 tools)</h3>
            <ul>
                <li>SSID configuration and passwords</li>
                <li>RF profiles, Air Marshal, usage stats</li>
            </ul>
            
            <h3>🧪 Live Tools (10 tools)</h3>
            <ul>
                <li>Ping, throughput, cable tests</li>
                <li>Wake-on-LAN, MAC tables, LED blink</li>
            </ul>
            
            <h3>📜 Licensing (6 tools)</h3>
            <ul>
                <li>License management and renewal</li>
                <li>Co-term licensing operations</li>
            </ul>
            
            <h3>🚀 Beta Features (6 tools)</h3>
            <ul>
                <li>Early access features management</li>
                <li>Beta API status checks</li>
            </ul>
            
            <p>Use <code>GET /api/v1/tools</code> to see the complete list with arguments.</p>
        </body>
    </html>
    """)

@app.post("/auth")
async def authenticate(auth_req: AuthRequest):
    """Simple authentication"""
    token = secrets.token_urlsafe(32)
    
    AUTH_TOKENS[token] = {
        "username": auth_req.username,
        "created_at": datetime.now().isoformat(),
        "is_privileged": auth_req.username in PRIVILEGED_USERS
    }
    
    return {
        "token": token,
        "username": auth_req.username,
        "is_privileged": AUTH_TOKENS[token]["is_privileged"]
    }

@app.post("/api/v1/execute")
async def execute_tool(
    request: ToolRequest,
    user_data: Dict = Depends(verify_token)
) -> ToolResponse:
    """Execute tool via REST API (for n8n)"""
    username = user_data["username"]
    
    # Check rate limit
    if not check_rate_limit(username):
        return ToolResponse(
            success=False,
            error="Rate limit exceeded",
            timestamp=datetime.now().isoformat(),
            user=username
        )
    
    # Execute tool
    try:
        # Check if tool exists
        if request.tool not in ALL_TOOLS:
            return ToolResponse(
                success=False,
                error=f"Unknown tool: {request.tool}",
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
        
        if request.tool in dangerous_tools and not user_data["is_privileged"]:
            return ToolResponse(
                success=False,
                error="Permission denied: privileged operation",
                timestamp=datetime.now().isoformat(),
                user=username
            )
        
        # Get the tool function
        tool_func = ALL_TOOLS[request.tool]
        
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
        logger.error(f"Error executing {request.tool}: {e}")
        return ToolResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat(),
            user=username
        )

@app.get("/api/v1/tools")
async def list_tools(user_data: Dict = Depends(verify_token)):
    """List available tools"""
    import inspect
    
    tools = []
    dangerous_tools = [
        "reboot_device", "confirm_reboot_device", 
        "reboot_network_sm_devices", "confirm_reboot_network_sm_devices",
        "delete_organization", "delete_network",
        "delete_organization_policy_object"
    ]
    
    # Get all tools and their signatures
    for name, func in sorted(ALL_TOOLS.items()):
        # Skip dangerous tools for non-privileged users
        if name in dangerous_tools and not user_data["is_privileged"]:
            continue
            
        # Get function signature
        sig = inspect.signature(func)
        args = {}
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':  # Skip self parameter
                continue
                
            # Determine parameter type and requirement
            param_info = str(param.annotation) if param.annotation != param.empty else "string"
            param_info = param_info.replace("<class '", "").replace("'>", "")
            
            if param.default == param.empty:
                args[param_name] = param_info  # Required parameter
            else:
                args[param_name] = f"{param_info} (optional, default: {param.default})"
        
        # Get description from docstring
        description = func.__doc__.strip() if func.__doc__ else name.replace('_', ' ').title()
        
        # Mark dangerous tools
        if name in dangerous_tools:
            description += " ⚠️ DANGEROUS"
        
        tools.append({
            "name": name,
            "description": description,
            "arguments": args
        })
    
    return {
        "tools": tools, 
        "total": len(tools),
        "user": user_data["username"],
        "is_privileged": user_data["is_privileged"]
    }

@app.get("/sse")
async def handle_sse(request: Request):
    """SSE endpoint for MCP protocol (Claude Desktop and n8n)"""
    # Get token from header or query
    auth = request.headers.get("authorization", "")
    token = auth.replace("Bearer ", "") if auth else request.query_params.get("token")
    
    if not token or token not in AUTH_TOKENS:
        raise HTTPException(401, "Invalid token")
    
    username = AUTH_TOKENS[token]["username"]
    logger.info(f"SSE connection from {username}")
    
    # Create MCP handler
    mcp_handler = MCPSSEHandler(ALL_TOOLS)
    
    # SSE event generator
    async def event_generator():
        # Wait for initialization request from client
        # For SSE, we need to send the initialization response immediately
        init_response = {
            "jsonrpc": "2.0",
            "id": 0,
            "result": {
                "protocolVersion": "0.1.0",
                "serverInfo": {
                    "name": "meraki-hybrid",
                    "version": "1.0.0"
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
            # Send keepalive as a notification (no id)
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
    # This is needed for n8n's MCP Client Tool and Claude Desktop
    auth = request.headers.get("authorization", "")
    token = auth.replace("Bearer ", "") if auth else None
    
    if not token or token not in AUTH_TOKENS:
        raise HTTPException(401, "Invalid token")
    
    # Handle the MCP message
    data = await request.json()
    logger.info(f"MCP message received: {data.get('method', 'unknown')}")
    
    # Create handler and process message
    mcp_handler = MCPSSEHandler(ALL_TOOLS)
    response = await mcp_handler.handle_message(data)
    
    return response

@app.post("/mcp")
async def handle_mcp_stream(request: Request):
    """HTTP Stream endpoint for MCP protocol (recommended for Claude Desktop and n8n)"""
    # Get token from header
    auth = request.headers.get("authorization", "")
    token = auth.replace("Bearer ", "") if auth else None
    
    if not token or token not in AUTH_TOKENS:
        raise HTTPException(401, "Invalid token")
    
    username = AUTH_TOKENS[token]["username"]
    logger.info(f"MCP stream connection from {username}")
    
    # Handle the MCP message
    data = await request.json()
    logger.info(f"MCP stream message: {data.get('method', 'unknown')}")
    
    # Create handler and process message
    mcp_handler = MCPSSEHandler(ALL_TOOLS)
    response = await mcp_handler.handle_message(data)
    
    # Return response with proper headers for streaming
    return Response(
        content=json.dumps(response),
        media_type="application/json",
        headers={
            "Transfer-Encoding": "chunked",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "meraki_connected": meraki_client is not None,
        "timestamp": datetime.now().isoformat()
    }

# n8n Workflow Examples
@app.get("/n8n/examples")
async def n8n_examples():
    """Get n8n workflow examples"""
    return {
        "monitor_uplinks": {
            "name": "Monitor Meraki Uplinks",
            "description": "Check uplinks every 5 minutes and alert on packet loss",
            "nodes": [
                {
                    "type": "n8n-nodes-base.schedule",
                    "parameters": {"rule": {"interval": [{"field": "minutes", "minutesInterval": 5}]}}
                },
                {
                    "type": "n8n-nodes-base.httpRequest",
                    "parameters": {
                        "method": "POST",
                        "url": "http://your-server:8000/api/v1/execute",
                        "authentication": "genericCredentialType",
                        "genericAuthType": "httpHeaderAuth",
                        "sendHeaders": True,
                        "headerParameters": {
                            "parameters": [
                                {"name": "Authorization", "value": "Bearer YOUR_TOKEN"}
                            ]
                        },
                        "sendBody": True,
                        "bodyParameters": {
                            "parameters": [
                                {"name": "tool", "value": "check_uplinks"},
                                {"name": "arguments", "value": {"org_id": "YOUR_ORG_ID"}}
                            ]
                        }
                    }
                }
            ]
        }
    }

def main():
    """Run the hybrid server"""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    logger.info(f"Starting Meraki MCP Hybrid Server on {host}:{port}")
    logger.info("Supports both REST API (n8n) and MCP protocol (Claude)")
    
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()