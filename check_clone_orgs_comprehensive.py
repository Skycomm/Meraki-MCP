#!/usr/bin/env python3
"""
Script to perform comprehensive checks on the Clone organizations.
Uses the new check_organization_comprehensive and compare_organizations tools.
"""

import json
import asyncio
from mcp.client.stdio import stdio_client

async def main():
    # The Clone organization IDs
    clone_org_1 = "726205439913493748"
    clone_org_2 = "726205439913493749"
    main_org = "726205439913493746"  # Skycomm Production
    
    print("Cisco Meraki Clone Organizations Comprehensive Check")
    print("=" * 60)
    
    async with stdio_client() as (read_stream, write_stream):
        # Initialize the MCP client
        await write_stream.send({
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "clone-org-checker",
                    "version": "1.0.0"
                }
            },
            "id": 1
        })
        
        # Wait for initialization response
        response = await read_stream.recv()
        
        print("\n1. Checking Clone Organization 1 (ID: 726205439913493748)")
        print("-" * 60)
        
        # Check first clone organization
        await write_stream.send({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "check_organization_comprehensive",
                "arguments": {
                    "org_id": clone_org_1,
                    "check_type": "all"
                }
            },
            "id": 2
        })
        
        response = await read_stream.recv()
        if response.get("result"):
            print(response["result"].get("content", [{}])[0].get("text", "No data"))
        else:
            print(f"Error: {response.get('error', 'Unknown error')}")
        
        print("\n2. Checking Clone Organization 2 (ID: 726205439913493749)")
        print("-" * 60)
        
        # Check second clone organization
        await write_stream.send({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "check_organization_comprehensive",
                "arguments": {
                    "org_id": clone_org_2,
                    "check_type": "all"
                }
            },
            "id": 3
        })
        
        response = await read_stream.recv()
        if response.get("result"):
            print(response["result"].get("content", [{}])[0].get("text", "No data"))
        else:
            print(f"Error: {response.get('error', 'Unknown error')}")
        
        print("\n3. Comparing Both Clone Organizations")
        print("-" * 60)
        
        # Compare the two clone organizations
        await write_stream.send({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "compare_organizations",
                "arguments": {
                    "org_id_1": clone_org_1,
                    "org_id_2": clone_org_2
                }
            },
            "id": 4
        })
        
        response = await read_stream.recv()
        if response.get("result"):
            print(response["result"].get("content", [{}])[0].get("text", "No data"))
        else:
            print(f"Error: {response.get('error', 'Unknown error')}")
        
        print("\n4. Comparing Clone with Main Skycomm Organization")
        print("-" * 60)
        
        # Compare clone with main organization
        await write_stream.send({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "compare_organizations",
                "arguments": {
                    "org_id_1": main_org,
                    "org_id_2": clone_org_1
                }
            },
            "id": 5
        })
        
        response = await read_stream.recv()
        if response.get("result"):
            print(response["result"].get("content", [{}])[0].get("text", "No data"))
        else:
            print(f"Error: {response.get('error', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(main())