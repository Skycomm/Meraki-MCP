#!/usr/bin/env python3
"""
Meraki MCP Server - Improved Python Implementation
Following best practices from mcp-mem0 and other Cole's implementations
"""

import os
import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from functools import lru_cache
import time

from mcp import FastMCP, Context
from mcp.types import Tool, TextContent
import httpx
from pydantic import BaseModel, Field

# Setup structured logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("meraki-mcp-python")

# Configuration
MERAKI_API_KEY = os.getenv("MERAKI_API_KEY", "")
MERAKI_BASE_URL = os.getenv("MERAKI_BASE_URL", "https://api.meraki.com/api/v1")
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes default
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds

# Privileged users for dangerous operations
PRIVILEGED_USERS = os.getenv("PRIVILEGED_USERS", "").split(",")

# Rate limiting storage
rate_limiter: Dict[str, List[float]] = {}

class MerakiClient:
    """Async Meraki API client with caching and error handling"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = MERAKI_BASE_URL
        self.client = httpx.AsyncClient(
            headers={
                "X-Cisco-Meraki-API-Key": api_key,
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    async def close(self):
        await self.client.aclose()
    
    @lru_cache(maxsize=100)
    def _get_cache_key(self, endpoint: str, cache_time: int) -> str:
        """Generate cache key based on endpoint and time window"""
        return f"{endpoint}:{cache_time}"
    
    async def get(self, endpoint: str, use_cache: bool = True) -> Any:
        """GET request with optional caching"""
        if use_cache:
            # Cache based on 5-minute windows
            cache_time = int(time.time() / CACHE_TTL)
            cache_key = self._get_cache_key(endpoint, cache_time)
        
        try:
            response = await self.client.get(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Meraki API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    async def post(self, endpoint: str, data: Dict[str, Any] = None) -> Any:
        """POST request"""
        try:
            response = await self.client.post(
                f"{self.base_url}{endpoint}",
                json=data or {}
            )
            response.raise_for_status()
            return response.json() if response.content else {}
        except httpx.HTTPStatusError as e:
            logger.error(f"API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Meraki API error: {e.response.status_code}")

# Global client instance
meraki_client: Optional[MerakiClient] = None

def check_rate_limit(user_id: str) -> bool:
    """Check if user has exceeded rate limit"""
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

def format_response(content: str, success: bool = True) -> List[TextContent]:
    """Format response in consistent structure"""
    return [TextContent(
        type="text",
        text=content
    )]

def check_privileges(context: Context, operation: str) -> bool:
    """Check if user has privileges for operation"""
    user_id = context.meta.get("user_id", "anonymous")
    
    if user_id in PRIVILEGED_USERS:
        logger.info(f"Privileged operation '{operation}' authorized for user {user_id}")
        return True
    
    logger.warning(f"Privileged operation '{operation}' denied for user {user_id}")
    return False

# Server lifecycle
@mcp.tool()
async def init_server() -> str:
    """Initialize the MCP server"""
    global meraki_client
    
    if not MERAKI_API_KEY:
        return "❌ Error: MERAKI_API_KEY environment variable not set"
    
    try:
        meraki_client = MerakiClient(MERAKI_API_KEY)
        logger.info("Meraki MCP server initialized successfully")
        return "✅ Server initialized"
    except Exception as e:
        logger.error(f"Failed to initialize server: {e}")
        return f"❌ Error initializing server: {str(e)}"

@mcp.tool()
async def cleanup_server() -> str:
    """Cleanup server resources"""
    global meraki_client
    
    if meraki_client:
        await meraki_client.close()
        meraki_client = None
    
    return "✅ Server cleaned up"

# Read-only tools for all users
@mcp.tool()
async def list_organizations(context: Context) -> List[TextContent]:
    """List all Meraki organizations accessible with the API key"""
    user_id = context.meta.get("user_id", "anonymous")
    
    # Rate limiting
    if not check_rate_limit(user_id):
        return format_response("❌ Rate limit exceeded. Please try again later.", False)
    
    try:
        orgs = await meraki_client.get("/organizations")
        
        result = f"# Meraki Organizations\n\n"
        result += f"**Total**: {len(orgs)}\n"
        result += f"**Requested by**: {user_id}\n\n"
        
        for org in orgs:
            result += f"## {org['name']}\n"
            result += f"- **ID**: `{org['id']}`\n"
            result += f"- **URL**: {org.get('url', 'N/A')}\n"
            if org.get('api', {}).get('enabled'):
                result += "- **API**: ✅ Enabled\n"
            result += "\n"
        
        logger.info(f"Listed {len(orgs)} organizations for user {user_id}")
        return format_response(result)
        
    except Exception as e:
        logger.error(f"Error listing organizations: {e}")
        return format_response(f"❌ Error: {str(e)}", False)

@mcp.tool()
async def get_organization_networks(
    context: Context,
    org_id: str = Field(description="Organization ID")
) -> List[TextContent]:
    """Get all networks in an organization"""
    user_id = context.meta.get("user_id", "anonymous")
    
    if not check_rate_limit(user_id):
        return format_response("❌ Rate limit exceeded. Please try again later.", False)
    
    try:
        networks = await meraki_client.get(f"/organizations/{org_id}/networks")
        
        result = f"# Networks in Organization {org_id}\n\n"
        result += f"**Total**: {len(networks)}\n\n"
        
        # Group by type
        by_type = {}
        for network in networks:
            types = network.get('productTypes', ['Unknown'])
            for ptype in types:
                if ptype not in by_type:
                    by_type[ptype] = []
                by_type[ptype].append(network)
        
        for ptype, nets in by_type.items():
            result += f"## {ptype} Networks ({len(nets)})\n"
            for net in nets:
                result += f"- **{net['name']}** (`{net['id']}`)\n"
                if net.get('tags'):
                    result += f"  - Tags: {', '.join(net['tags'])}\n"
            result += "\n"
        
        return format_response(result)
        
    except Exception as e:
        logger.error(f"Error getting networks for org {org_id}: {e}")
        return format_response(f"❌ Error: {str(e)}", False)

@mcp.tool()
async def get_uplink_loss_latency(
    context: Context,
    org_id: str = Field(description="Organization ID"),
    timespan: int = Field(default=300, description="Timespan in seconds (max 300)")
) -> List[TextContent]:
    """Get real-time packet loss and latency for organization uplinks"""
    user_id = context.meta.get("user_id", "anonymous")
    
    if not check_rate_limit(user_id):
        return format_response("❌ Rate limit exceeded. Please try again later.", False)
    
    # Validate timespan
    timespan = min(max(1, timespan), 300)
    
    try:
        endpoint = f"/organizations/{org_id}/devices/uplinks/lossAndLatency?timespan={timespan}"
        loss_latency = await meraki_client.get(endpoint, use_cache=False)  # Don't cache real-time data
        
        if not loss_latency:
            return format_response(f"No uplink data found for organization {org_id}")
        
        result = f"# 🚨 Uplink Loss & Latency Report\n\n"
        result += f"**Organization**: {org_id}\n"
        result += f"**Time Period**: Last {timespan//60} minutes\n"
        result += f"**Total Uplinks**: {len(loss_latency)}\n\n"
        
        # Group by device
        devices = {}
        for entry in loss_latency:
            serial = entry.get('serial', 'Unknown')
            if serial not in devices:
                devices[serial] = []
            devices[serial].append(entry)
        
        # Analyze each device
        alerts = []
        for serial, uplinks in devices.items():
            result += f"## Device: {serial}\n"
            
            for uplink in uplinks:
                uplink_name = uplink.get('uplink', 'Unknown')
                ip = uplink.get('ip', 'N/A')
                
                result += f"### {uplink_name.upper()} ({ip})\n"
                
                time_series = uplink.get('timeSeries', [])
                if time_series:
                    # Get latest and calculate stats
                    latest = time_series[-1]
                    current_loss = latest.get('lossPercent', 0)
                    current_latency = latest.get('latencyMs', 0)
                    
                    losses = [p.get('lossPercent', 0) for p in time_series if p.get('lossPercent') is not None]
                    latencies = [p.get('latencyMs', 0) for p in time_series if p.get('latencyMs') is not None]
                    
                    avg_loss = sum(losses) / len(losses) if losses else 0
                    max_loss = max(losses) if losses else 0
                    avg_latency = sum(latencies) / len(latencies) if latencies else 0
                    max_latency = max(latencies) if latencies else 0
                    
                    # Status indicators
                    loss_icon = "🔴" if current_loss > 5 else "🟡" if current_loss > 1 else "🟢"
                    latency_icon = "🔴" if current_latency > 150 else "🟡" if current_latency > 50 else "🟢"
                    
                    result += f"**Current**: {loss_icon} {current_loss:.1f}% loss, {latency_icon} {current_latency:.0f}ms\n"
                    result += f"**Average**: {avg_loss:.1f}% loss, {avg_latency:.0f}ms latency\n"
                    result += f"**Maximum**: {max_loss:.1f}% loss, {max_latency:.0f}ms latency\n\n"
                    
                    # Collect alerts
                    if avg_loss > 1:
                        alerts.append(f"⚠️ {serial} {uplink_name}: Average packet loss {avg_loss:.1f}%")
                    if avg_latency > 100:
                        alerts.append(f"⚠️ {serial} {uplink_name}: High latency {avg_latency:.0f}ms")
                else:
                    result += "- No data available\n\n"
        
        # Show alerts summary
        if alerts:
            result += "## ⚠️ Alerts\n"
            for alert in alerts:
                result += f"- {alert}\n"
        
        logger.info(f"Generated uplink report for org {org_id}, found {len(alerts)} alerts")
        return format_response(result)
        
    except Exception as e:
        logger.error(f"Error getting uplink data: {e}")
        return format_response(f"❌ Error: {str(e)}", False)

# Privileged tools
@mcp.tool()
async def reboot_device(
    context: Context,
    serial: str = Field(description="Device serial number"),
    confirmation: str = Field(description="Must be 'YES-REBOOT-{serial}' to proceed")
) -> List[TextContent]:
    """Reboot a Meraki device (privileged operation)"""
    user_id = context.meta.get("user_id", "anonymous")
    
    # Check privileges
    if not check_privileges(context, "reboot_device"):
        return format_response(
            f"❌ Access Denied\n\n"
            f"User '{user_id}' does not have permission to reboot devices.\n"
            f"This operation is restricted to privileged users only.",
            False
        )
    
    # Check confirmation
    expected_confirmation = f"YES-REBOOT-{serial}"
    if confirmation != expected_confirmation:
        return format_response(
            f"# ⚠️ REBOOT CONFIRMATION REQUIRED\n\n"
            f"**Device Serial**: {serial}\n"
            f"**User**: {user_id}\n\n"
            f"**WARNING**: Rebooting this device will:\n"
            f"- 🔴 Disconnect ALL users\n"
            f"- 🔴 Interrupt network services\n"
            f"- 🔴 Take 2-5 minutes to come back online\n\n"
            f"**To proceed**: Provide confirmation: `{expected_confirmation}`\n\n"
            f"⚠️ This action cannot be undone!",
            False
        )
    
    try:
        await meraki_client.post(f"/devices/{serial}/reboot")
        
        logger.warning(f"Device {serial} rebooted by user {user_id}")
        
        return format_response(
            f"✅ REBOOT INITIATED\n\n"
            f"**Device**: {serial}\n"
            f"**Initiated by**: {user_id}\n"
            f"**Timestamp**: {datetime.now().isoformat()}\n"
            f"**Expected downtime**: 2-5 minutes\n\n"
            f"Monitor device status to confirm it comes back online."
        )
        
    except Exception as e:
        logger.error(f"Error rebooting device {serial}: {e}")
        return format_response(f"❌ Error rebooting device: {str(e)}", False)

# Live tools
@mcp.tool()
async def create_ping_test(
    context: Context,
    serial: str = Field(description="Device serial number"),
    target: str = Field(description="Target IP or hostname"),
    count: int = Field(default=5, description="Number of pings (max 5)")
) -> List[TextContent]:
    """Create a ping test from a device"""
    user_id = context.meta.get("user_id", "anonymous")
    
    if not check_rate_limit(user_id):
        return format_response("❌ Rate limit exceeded. Please try again later.", False)
    
    count = min(max(1, count), 5)
    
    try:
        result = await meraki_client.post(
            f"/devices/{serial}/liveTools/ping",
            {"target": target, "count": count}
        )
        
        job_id = result.get('pingId') or result.get('id')
        if not job_id:
            return format_response(
                "❌ Failed to create ping test. Device may be offline or Live Tools not enabled.",
                False
            )
        
        return format_response(
            f"# 🏓 Ping Test Created\n\n"
            f"**Device**: {serial}\n"
            f"**Target**: {target}\n"
            f"**Count**: {count}\n"
            f"**Job ID**: `{job_id}`\n"
            f"**Status**: {result.get('status', 'pending')}\n\n"
            f"Use `get_ping_test_results` with the job ID to check results."
        )
        
    except Exception as e:
        logger.error(f"Error creating ping test: {e}")
        return format_response(f"❌ Error: {str(e)}", False)

@mcp.tool()
async def get_ping_test_results(
    context: Context,
    serial: str = Field(description="Device serial number"),
    ping_id: str = Field(description="Ping test job ID")
) -> List[TextContent]:
    """Get results of a ping test"""
    try:
        result = await meraki_client.get(f"/devices/{serial}/liveTools/ping/{ping_id}")
        
        response = f"# 🏓 Ping Test Results\n\n"
        response += f"**Status**: {result.get('status', 'Unknown')}\n\n"
        
        results = result.get('results', {})
        if results:
            loss = results.get('loss', {}).get('percentage', 0)
            received = results.get('received', 0)
            sent = results.get('sent', 0)
            
            response += f"## Summary\n"
            response += f"- **Sent**: {sent} packets\n"
            response += f"- **Received**: {received} packets\n"
            response += f"- **Loss**: {loss}%\n\n"
            
            latencies = results.get('latencies', {})
            if latencies:
                response += f"## Latency\n"
                response += f"- **Min**: {latencies.get('minimum', 0)}ms\n"
                response += f"- **Avg**: {latencies.get('average', 0)}ms\n"
                response += f"- **Max**: {latencies.get('maximum', 0)}ms\n"
        
        return format_response(response)
        
    except Exception as e:
        logger.error(f"Error getting ping results: {e}")
        return format_response(f"❌ Error: {str(e)}", False)

# Main entry point
async def main():
    """Run the MCP server"""
    # Initialize server on startup
    await init_server()
    
    # Run the server
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(
            read_stream,
            write_stream,
            mcp.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())