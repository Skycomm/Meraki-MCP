#!/usr/bin/env python3
"""
MCP HTTP Bridge for Network Deployment
Provides MCP-over-HTTP/SSE for Claude Desktop and other clients
Based on remote-mcp-server-with-auth patterns
"""

import os
import json
import asyncio
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import secrets

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from sse_starlette.sse import EventSourceResponse
import uvicorn

from mcp import FastMCP
from mcp.server.sse import SSEServerTransport
from mcp.server.models import InitializationOptions
from mcp.types import TextContent

from .server import (
    meraki_client,
    init_server,
    cleanup_server,
    list_organizations,
    get_organization_networks,
    get_uplink_loss_latency,
    create_ping_test,
    get_ping_test_results,
    reboot_device,
    PRIVILEGED_USERS
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Meraki MCP Server - Network Edition",
    description="MCP server accessible over your private network"
)

# Auth tokens storage (in production, use Redis or database)
AUTH_TOKENS: Dict[str, Dict[str, Any]] = {}

# Initialize MCP server
mcp = FastMCP("meraki-mcp-network")

# Re-register all tools for network access
@mcp.tool()
async def network_list_organizations(context) -> list:
    """List all Meraki organizations"""
    return await list_organizations(context)

@mcp.tool()
async def network_get_organization_networks(context, org_id: str) -> list:
    """Get networks in organization"""
    return await get_organization_networks(context, org_id)

@mcp.tool()
async def network_get_uplink_loss_latency(context, org_id: str, timespan: int = 300) -> list:
    """Get uplink loss and latency"""
    return await get_uplink_loss_latency(context, org_id, timespan)

@mcp.tool()
async def network_create_ping_test(context, serial: str, target: str, count: int = 5) -> list:
    """Create ping test"""
    return await create_ping_test(context, serial, target, count)

@mcp.tool()
async def network_get_ping_test_results(context, serial: str, ping_id: str) -> list:
    """Get ping test results"""
    return await get_ping_test_results(context, serial, ping_id)

@mcp.tool()
async def network_reboot_device(context, serial: str, confirmation: str) -> list:
    """Reboot device (privileged)"""
    return await reboot_device(context, serial, confirmation)

@app.on_event("startup")
async def startup():
    """Initialize on startup"""
    await init_server()
    logger.info(f"MCP Network Server started - listening on all interfaces")

@app.on_event("shutdown") 
async def shutdown():
    """Cleanup on shutdown"""
    await cleanup_server()

@app.get("/")
async def home():
    """Home page with setup instructions"""
    server_ip = "YOUR_SERVER_IP"
    
    html = f"""
    <html>
        <head>
            <title>Meraki MCP Network Server</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; }}
                code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
                pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                .step {{ margin: 20px 0; padding: 15px; border-left: 3px solid #0366d6; }}
                .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>🌐 Meraki MCP Network Server</h1>
            <p>This server is running on your private network and accessible to all clients.</p>
            
            <div class="warning">
                <strong>⚠️ Important:</strong> Replace {server_ip} with your actual server IP address!
            </div>
            
            <h2>Step 1: Get Authentication Token</h2>
            <div class="step">
                <p>From any machine on your network:</p>
                <pre>curl -X POST http://{server_ip}:8000/auth \\
  -H "Content-Type: application/json" \\
  -d '{{"username": "your-name@company.com"}}'</pre>
                <p>Save the token from the response.</p>
            </div>
            
            <h2>Step 2: Configure Claude Desktop</h2>
            <div class="step">
                <p>Add this to your Claude Desktop config:</p>
                <pre>{{
  "mcpServers": {{
    "meraki-network": {{
      "command": "node",
      "args": [
        "/path/to/mcp-sse-client.js",
        "http://{server_ip}:8000/sse"
      ],
      "env": {{
        "MCP_AUTH_TOKEN": "your-token-here"
      }}
    }}
  }}
}}</pre>
            </div>
            
            <h2>Available Tools</h2>
            <ul>
                <li><code>network_list_organizations</code> - List all organizations</li>
                <li><code>network_get_organization_networks</code> - Get networks</li>
                <li><code>network_get_uplink_loss_latency</code> - Check uplinks</li>
                <li><code>network_create_ping_test</code> - Start ping test</li>
                <li><code>network_get_ping_test_results</code> - Get ping results</li>
                <li><code>network_reboot_device</code> - Reboot device (privileged only)</li>
            </ul>
            
            <h2>Test Connection</h2>
            <div class="step">
                <p>Test that you can reach the server:</p>
                <pre>curl http://{server_ip}:8000/health</pre>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.post("/auth")
async def authenticate(request: Request):
    """Simple authentication endpoint"""
    data = await request.json()
    username = data.get("username", "anonymous")
    
    # Generate token
    token = secrets.token_urlsafe(32)
    
    # Store token
    AUTH_TOKENS[token] = {
        "username": username,
        "created_at": datetime.now().isoformat(),
        "is_privileged": username in PRIVILEGED_USERS
    }
    
    logger.info(f"User {username} authenticated from {request.client.host}")
    
    return {
        "token": token,
        "username": username,
        "is_privileged": username in PRIVILEGED_USERS,
        "message": "Use this token in your MCP client configuration"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "server": "meraki-mcp-network",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.options("/sse")
async def sse_options():
    """Handle CORS preflight for SSE"""
    return Response(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
        }
    )

@app.get("/sse")
async def handle_sse(request: Request):
    """SSE endpoint for MCP protocol"""
    # Get auth token from header
    auth_header = request.headers.get("authorization", "")
    token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else None
    
    # Check token from query params as fallback
    if not token:
        token = request.query_params.get("token")
    
    # Validate token
    user_data = AUTH_TOKENS.get(token, {})
    if not user_data:
        raise HTTPException(401, "Invalid or missing authentication token")
    
    username = user_data.get("username", "anonymous")
    logger.info(f"SSE connection from {username}")
    
    # Create transport
    transport = SSEServerTransport("/sse", request)
    
    # Create user context
    class UserContext:
        def __init__(self, username):
            self.meta = {"user_id": username}
    
    # Inject user context into MCP
    mcp._context = UserContext(username)
    
    # Connect and run
    await mcp.connect(transport)
    
    return transport.response

@app.post("/sse")
async def handle_sse_post(request: Request):
    """Handle SSE POST requests for MCP protocol"""
    return await handle_sse(request)

# Create MCP SSE client helper script
MCP_SSE_CLIENT = """#!/usr/bin/env node
// MCP SSE Client for Claude Desktop
// Save this as mcp-sse-client.js

const EventSource = require('eventsource');
const readline = require('readline');

const serverUrl = process.argv[2];
const token = process.env.MCP_AUTH_TOKEN;

if (!serverUrl || !token) {
    console.error('Usage: MCP_AUTH_TOKEN=token node mcp-sse-client.js <server-url>');
    process.exit(1);
}

// Create SSE connection
const eventSource = new EventSource(`${serverUrl}?token=${token}`);

// Handle messages from server
eventSource.onmessage = (event) => {
    process.stdout.write(event.data + '\\n');
};

eventSource.onerror = (error) => {
    console.error('SSE Error:', error);
    process.exit(1);
};

// Read from stdin and forward to server
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

rl.on('line', async (line) => {
    try {
        // For SSE, we need to make POST requests for each command
        const response = await fetch(serverUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: line
        });
        
        if (!response.ok) {
            console.error('Request failed:', response.statusText);
        }
    } catch (error) {
        console.error('Error sending command:', error);
    }
});
"""

@app.get("/mcp-sse-client.js")
async def get_client_script():
    """Download the MCP SSE client script"""
    return Response(
        content=MCP_SSE_CLIENT,
        media_type="application/javascript",
        headers={
            "Content-Disposition": "attachment; filename=mcp-sse-client.js"
        }
    )

def run_network_server():
    """Run the network server"""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    logger.info(f"Starting Meraki MCP Network Server on {host}:{port}")
    logger.info(f"Privileged users: {', '.join(PRIVILEGED_USERS) if PRIVILEGED_USERS else 'None configured'}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    run_network_server()