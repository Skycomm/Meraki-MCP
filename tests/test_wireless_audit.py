#!/usr/bin/env python3
"""
Test wireless audit as an MCP client for Skycomm org Reserve St network.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json

async def test_wireless_audit():
    """Test wireless audit functionality."""
    
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["meraki_server.py"],
        env=None
    )
    
    print("🚀 Testing Wireless Audit for Skycomm - Reserve St Network")
    print("=" * 60)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # First, search for the organization
            print("\n1️⃣ Searching for Skycomm organization...")
            result = await session.call_tool(
                "search_organizations_by_name",
                arguments={"name": "skycomm"}
            )
            print(f"Organization search result: {result.content[0].text[:200]}...")
            
            # Get organization ID from the result
            # Assuming we know the org ID for testing
            org_id = "1374235"  # Skycomm org ID from CLAUDE.md
            
            # Search for Reserve St network
            print("\n2️⃣ Searching for Reserve St network...")
            result = await session.call_tool(
                "get_organization_networks",
                arguments={"organization_id": org_id}
            )
            print(f"Networks found: {result.content[0].text[:300]}...")
            
            # Use the known Reserve St network ID
            network_id = "L_709951935762302054"
            
            # Perform wireless health check
            print("\n3️⃣ Running wireless health check...")
            result = await session.call_tool(
                "get_composite_wireless_health",
                arguments={
                    "network_id": network_id,
                    "check_ssids": True,
                    "check_clients": True,
                    "check_aps": True,
                    "check_rf": True
                }
            )
            print("\n📊 Wireless Health Check Results:")
            print("-" * 60)
            print(result.content[0].text)
            
            # Get wireless SSIDs
            print("\n4️⃣ Getting SSID configurations...")
            result = await session.call_tool(
                "get_network_wireless_ssids",
                arguments={"network_id": network_id}
            )
            print("\n📡 SSID Configuration:")
            print("-" * 60)
            print(result.content[0].text[:500])
            
            # Get access points status
            print("\n5️⃣ Checking access points status...")
            result = await session.call_tool(
                "get_network_wireless_access_points",
                arguments={"network_id": network_id}
            )
            print("\n🔧 Access Points Status:")
            print("-" * 60)
            print(result.content[0].text[:500])
            
            # Get RF profiles
            print("\n6️⃣ Checking RF profiles...")
            result = await session.call_tool(
                "get_network_wireless_rf_profiles",
                arguments={"network_id": network_id}
            )
            print("\n📻 RF Profiles:")
            print("-" * 60)
            print(result.content[0].text[:500])
            
            # Get wireless clients
            print("\n7️⃣ Getting connected clients...")
            result = await session.call_tool(
                "get_network_wireless_clients",
                arguments={
                    "network_id": network_id,
                    "timespan": 300  # Last 5 minutes
                }
            )
            print("\n👥 Connected Clients:")
            print("-" * 60)
            print(result.content[0].text[:500])
            
            # Get failed connections
            print("\n8️⃣ Checking failed connections...")
            result = await session.call_tool(
                "get_network_wireless_failed_connections",
                arguments={
                    "network_id": network_id,
                    "timespan": 86400  # Last 24 hours
                }
            )
            print("\n❌ Failed Connections:")
            print("-" * 60)
            print(result.content[0].text[:500])
            
            # Get channel utilization
            print("\n9️⃣ Checking channel utilization...")
            result = await session.call_tool(
                "get_network_wireless_channel_utilization_history",
                arguments={
                    "network_id": network_id,
                    "timespan": 3600  # Last hour
                }
            )
            print("\n📊 Channel Utilization:")
            print("-" * 60)
            print(result.content[0].text[:500])
            
            print("\n" + "=" * 60)
            print("✅ Wireless Audit Complete for Reserve St Network!")
            print("=" * 60)
            
            return True

if __name__ == "__main__":
    success = asyncio.run(test_wireless_audit())
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n❌ Test failed")