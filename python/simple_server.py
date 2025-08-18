#!/usr/bin/env python3
"""
Simple Meraki MCP Server - Based on Cole's patterns
REST API for n8n + SSE for Claude Desktop
"""

import os
import json
import secrets
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import httpx

# Configuration
MERAKI_API_KEY = os.getenv("MERAKI_API_KEY", "")
PRIVILEGED_USERS = os.getenv("PRIVILEGED_USERS", "").split(",")

# Simple auth storage
AUTH_TOKENS: Dict[str, Dict[str, Any]] = {}

# Create FastAPI app
app = FastAPI(title="Meraki MCP Server")

# CORS for n8n
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class AuthRequest(BaseModel):
    username: str

class ToolRequest(BaseModel):
    tool: str
    arguments: Dict[str, Any] = {}

# Meraki client
class MerakiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.meraki.com/api/v1"
        self.client = httpx.AsyncClient(
            headers={
                "X-Cisco-Meraki-API-Key": api_key,
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    async def get(self, endpoint: str):
        response = await self.client.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return response.json()
    
    async def post(self, endpoint: str, data: Dict = None):
        response = await self.client.post(f"{self.base_url}{endpoint}", json=data or {})
        response.raise_for_status()
        return response.json() if response.content else {}

# Global client
meraki_client: Optional[MerakiClient] = None

# Tools implementation
async def list_organizations():
    """List all Meraki organizations"""
    orgs = await meraki_client.get("/organizations")
    
    result = f"# Meraki Organizations\\n\\n"
    result += f"Total: {len(orgs)}\\n\\n"
    
    for org in orgs:
        result += f"## {org['name']}\\n"
        result += f"- ID: `{org['id']}`\\n"
        if org.get('api', {}).get('enabled'):
            result += f"- API: ✅ Enabled\\n"
        result += "\\n"
    
    return result

async def get_networks(org_id: str):
    """Get networks in organization"""
    networks = await meraki_client.get(f"/organizations/{org_id}/networks")
    
    result = f"# Networks in Organization {org_id}\\n\\n"
    result += f"Total: {len(networks)}\\n\\n"
    
    for net in networks:
        result += f"- **{net['name']}** (`{net['id']}`)"
        if net.get('productTypes'):
            result += f" - {', '.join(net['productTypes'])}"
        result += "\\n"
    
    return result

async def check_uplinks(org_id: str, timespan: int = 300):
    """Check uplink loss and latency"""
    timespan = min(timespan, 300)
    data = await meraki_client.get(
        f"/organizations/{org_id}/devices/uplinks/lossAndLatency?timespan={timespan}"
    )
    
    result = f"# Uplink Report\\n\\n"
    alerts = []
    
    for entry in data:
        serial = entry.get('serial', 'Unknown')
        uplink = entry.get('uplink', 'Unknown') 
        time_series = entry.get('timeSeries', [])
        
        if time_series:
            losses = [p.get('lossPercent', 0) for p in time_series if p.get('lossPercent') is not None]
            if losses:
                avg_loss = sum(losses) / len(losses)
                if avg_loss > 1:
                    alerts.append(f"⚠️ {serial} {uplink}: {avg_loss:.1f}% loss")
    
    if alerts:
        result += "## Alerts\\n"
        for alert in alerts:
            result += f"- {alert}\\n"
    else:
        result += "✅ All uplinks healthy\\n"
    
    return result

# Routes
@app.get("/")
async def home():
    return HTMLResponse("""
    <h1>Meraki MCP Server</h1>
    <p>REST API for n8n and SSE for Claude Desktop</p>
    <h2>Get Started:</h2>
    <pre>
    1. POST /auth with {"username": "your-name"}
    2. Use token for /api/v1/execute or /sse
    </pre>
    """)

@app.post("/auth")
async def authenticate(auth_req: AuthRequest):
    """Get auth token"""
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
async def execute_tool(request: ToolRequest, authorization: str = Header(None)):
    """Execute tool - REST API for n8n"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing auth")
    
    token = authorization[7:]
    if token not in AUTH_TOKENS:
        raise HTTPException(401, "Invalid token")
    
    try:
        # Execute tools
        if request.tool == "list_organizations":
            result = await list_organizations()
        elif request.tool == "get_networks":
            result = await get_networks(request.arguments.get("org_id"))
        elif request.tool == "check_uplinks":
            result = await check_uplinks(
                request.arguments.get("org_id"),
                request.arguments.get("timespan", 300)
            )
        else:
            raise HTTPException(404, f"Unknown tool: {request.tool}")
        
        return {
            "success": True,
            "result": result,
            "user": AUTH_TOKENS[token]["username"]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "user": AUTH_TOKENS[token]["username"]
        }

@app.get("/sse")
async def sse_endpoint(request: Request):
    """SSE endpoint for Claude Desktop MCP"""
    # Get token
    auth = request.headers.get("authorization", "")
    token = auth.replace("Bearer ", "") if auth else request.query_params.get("token")
    
    if not token or token not in AUTH_TOKENS:
        raise HTTPException(401, "Invalid token")
    
    async def event_generator():
        # Send initial message
        yield f"data: {json.dumps({'type': 'connected', 'user': AUTH_TOKENS[token]['username']})}\\n\\n"
        
        # Keep alive
        while True:
            await asyncio.sleep(30)
            yield f"data: {json.dumps({'type': 'ping'})}\\n\\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )

@app.on_event("startup")
async def startup():
    global meraki_client
    if MERAKI_API_KEY:
        meraki_client = MerakiClient(MERAKI_API_KEY)
        print(f"✅ Meraki client initialized")

@app.on_event("shutdown")
async def shutdown():
    if meraki_client:
        await meraki_client.client.aclose()

@app.get("/health")
async def health():
    return {"status": "healthy", "time": datetime.now().isoformat()}

if __name__ == "__main__":
    print("🚀 Starting Simple Meraki MCP Server")
    print("   REST API: http://localhost:8000/api/v1/execute")
    print("   SSE/MCP: http://localhost:8000/sse")
    uvicorn.run(app, host="0.0.0.0", port=8000)