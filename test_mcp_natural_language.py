#!/usr/bin/env python3
"""
Test Meraki MCP SSE Server with Natural Language Questions
This simulates how an MCP client would interact with the server
"""

import json
import httpx
import asyncio
from typing import Dict, Any, List

# Server configuration
BASE_URL = "http://localhost:8000"
TOKEN = None

async def get_auth_token():
    """Get authentication token"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/auth",
            json={"username": "test-user"}
        )
        return response.json()["token"]

async def call_mcp_tool(tool_name: str, arguments: Dict[str, Any] = None):
    """Call an MCP tool via the SSE endpoint"""
    global TOKEN
    if not TOKEN:
        TOKEN = await get_auth_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/sse",
            headers={"Authorization": f"Bearer {TOKEN}"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments or {}
                }
            }
        )
        return response.json()

async def list_available_tools():
    """List all available MCP tools"""
    global TOKEN
    if not TOKEN:
        TOKEN = await get_auth_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/sse",
            headers={"Authorization": f"Bearer {TOKEN}"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list"
            }
        )
        return response.json()

# Test scenarios with natural language descriptions
TEST_SCENARIOS = [
    {
        "category": "Organization Management",
        "tests": [
            {
                "question": "Show me all the Meraki organizations I have access to",
                "tool": "list_organizations",
                "args": {}
            },
            {
                "question": "What firmware upgrades are available for my organizations?",
                "tool": "get_organization_firmware_upgrades",
                "args": {"organization_id": "686470"}
            },
            {
                "question": "List all networks in organization 686470",
                "tool": "get_organization_networks",
                "args": {"org_id": "686470"}
            }
        ]
    },
    {
        "category": "Network Management",
        "tests": [
            {
                "question": "Find a client named SKY-THOMAS-01 across all my networks",
                "tool": "find_client_by_name",
                "args": {"name": "SKY-THOMAS-01"}
            },
            {
                "question": "Show me all clients connected to network L_686470299674978369",
                "tool": "get_network_clients",
                "args": {"network_id": "L_686470299674978369"}
            },
            {
                "question": "What's the traffic analytics for network L_686470299674978369?",
                "tool": "get_network_traffic_analysis",
                "args": {"network_id": "L_686470299674978369"}
            }
        ]
    },
    {
        "category": "Device Management",
        "tests": [
            {
                "question": "Show me the status of device with serial Q3FD-XXXX-XXXX",
                "tool": "get_device",
                "args": {"serial": "Q3FD-XXXX-XXXX"}
            },
            {
                "question": "List all devices in network L_686470299674978369",
                "tool": "get_network_devices",
                "args": {"network_id": "L_686470299674978369"}
            },
            {
                "question": "Get management interface settings for device Q3FD-XXXX-XXXX",
                "tool": "get_device_management_interface",
                "args": {"serial": "Q3FD-XXXX-XXXX"}
            }
        ]
    },
    {
        "category": "Wireless Configuration",
        "tests": [
            {
                "question": "List all SSIDs configured in network L_686470299674978369",
                "tool": "get_network_ssids",
                "args": {"network_id": "L_686470299674978369"}
            },
            {
                "question": "Show me the RF profile settings for network L_686470299674978369",
                "tool": "get_network_wireless_rf_profiles",
                "args": {"network_id": "L_686470299674978369"}
            },
            {
                "question": "Get Air Marshal security events for network L_686470299674978369",
                "tool": "get_network_wireless_air_marshal",
                "args": {"network_id": "L_686470299674978369"}
            }
        ]
    },
    {
        "category": "Analytics & Monitoring",
        "tests": [
            {
                "question": "Check uplink packet loss for organization 686470",
                "tool": "monitor_uplink_packet_loss",
                "args": {"organization_id": "686470"}
            },
            {
                "question": "Show connection stats for network L_686470299674978369",
                "tool": "get_network_wireless_connection_stats",
                "args": {"network_id": "L_686470299674978369"}
            },
            {
                "question": "Get latency statistics for network L_686470299674978369",
                "tool": "get_network_wireless_latency_stats",
                "args": {"network_id": "L_686470299674978369"}
            }
        ]
    },
    {
        "category": "Alerts & Webhooks",
        "tests": [
            {
                "question": "Show me all configured webhooks for network L_686470299674978369",
                "tool": "get_network_webhooks_http_servers",
                "args": {"network_id": "L_686470299674978369"}
            },
            {
                "question": "What alert settings are configured for network L_686470299674978369?",
                "tool": "get_network_alerts_settings",
                "args": {"network_id": "L_686470299674978369"}
            },
            {
                "question": "List all sensor alerts for network L_686470299674978369",
                "tool": "get_network_sensor_alerts_profiles",
                "args": {"network_id": "L_686470299674978369"}
            }
        ]
    },
    {
        "category": "Camera & Video",
        "tests": [
            {
                "question": "Generate a video link for camera Q3FD-XXXX-XXXX",
                "tool": "get_device_camera_video_link",
                "args": {"serial": "Q3FD-XXXX-XXXX"}
            },
            {
                "question": "Take a snapshot from camera Q3FD-XXXX-XXXX",
                "tool": "generate_device_camera_snapshot",
                "args": {"serial": "Q3FD-XXXX-XXXX"}
            },
            {
                "question": "Show analytics zones for camera Q3FD-XXXX-XXXX",
                "tool": "get_device_camera_analytics_zones",
                "args": {"serial": "Q3FD-XXXX-XXXX"}
            }
        ]
    },
    {
        "category": "Systems Manager",
        "tests": [
            {
                "question": "List all managed devices in network L_686470299674978369",
                "tool": "get_network_sm_devices",
                "args": {"network_id": "L_686470299674978369"}
            },
            {
                "question": "Show profiles configured for network L_686470299674978369",
                "tool": "get_network_sm_profiles",
                "args": {"network_id": "L_686470299674978369"}
            },
            {
                "question": "Get trusted access configs for network L_686470299674978369",
                "tool": "get_network_sm_trusted_access_configs",
                "args": {"network_id": "L_686470299674978369"}
            }
        ]
    },
    {
        "category": "Licensing",
        "tests": [
            {
                "question": "Show license overview for organization 686470",
                "tool": "get_organization_licenses_overview",
                "args": {"organization_id": "686470"}
            },
            {
                "question": "List all licenses in organization 686470",
                "tool": "get_organization_licenses",
                "args": {"organization_id": "686470"}
            },
            {
                "question": "Check license renewal countdown for organization 686470",
                "tool": "countdown_organization_licenses_renewal",
                "args": {"organization_id": "686470"}
            }
        ]
    },
    {
        "category": "Live Diagnostics",
        "tests": [
            {
                "question": "Run a ping test from device Q3FD-XXXX-XXXX to 8.8.8.8",
                "tool": "create_device_live_tools_ping",
                "args": {"serial": "Q3FD-XXXX-XXXX", "target": "8.8.8.8"}
            },
            {
                "question": "Perform a cable test on port 1 of switch Q3FD-XXXX-XXXX",
                "tool": "create_device_live_tools_cable_test",
                "args": {"serial": "Q3FD-XXXX-XXXX", "ports": ["1"]}
            },
            {
                "question": "Run throughput test on device Q3FD-XXXX-XXXX",
                "tool": "create_device_live_tools_throughput_test",
                "args": {"serial": "Q3FD-XXXX-XXXX"}
            }
        ]
    }
]

async def run_tests():
    """Run all test scenarios"""
    print("=" * 80)
    print("MERAKI MCP SSE SERVER - NATURAL LANGUAGE TEST SUITE")
    print("=" * 80)
    print(f"\nServer: {BASE_URL}")
    print("Getting authentication token...")
    
    global TOKEN
    TOKEN = await get_auth_token()
    print(f"Token obtained: {TOKEN[:20]}...")
    
    # First, list available tools
    print("\n" + "=" * 80)
    print("LISTING AVAILABLE TOOLS")
    print("=" * 80)
    
    try:
        tools_response = await list_available_tools()
        if "result" in tools_response and "tools" in tools_response["result"]:
            tools = tools_response["result"]["tools"]
            print(f"\nTotal tools available: {len(tools)}")
            
            # Group tools by category
            categories = {}
            for tool in tools:
                # Extract category from tool name
                parts = tool["name"].split("_")
                if len(parts) > 1:
                    category = parts[1] if parts[0] in ["get", "create", "update", "delete", "list", "find", "monitor"] else parts[0]
                else:
                    category = "misc"
                
                if category not in categories:
                    categories[category] = []
                categories[category].append(tool["name"])
            
            print("\nTools by category:")
            for cat, tool_names in sorted(categories.items()):
                print(f"  {cat}: {len(tool_names)} tools")
    except Exception as e:
        print(f"Error listing tools: {e}")
    
    # Run test scenarios
    total_tests = sum(len(scenario["tests"]) for scenario in TEST_SCENARIOS)
    test_num = 0
    passed = 0
    failed = 0
    errors = []
    
    for scenario in TEST_SCENARIOS:
        print("\n" + "=" * 80)
        print(f"TESTING: {scenario['category']}")
        print("=" * 80)
        
        for test in scenario["tests"]:
            test_num += 1
            print(f"\n[{test_num}/{total_tests}] Question: {test['question']}")
            print(f"    Tool: {test['tool']}")
            print(f"    Args: {test['args']}")
            
            try:
                result = await call_mcp_tool(test["tool"], test["args"])
                
                if "error" in result:
                    print(f"    [FAILED] {result['error'].get('message', 'Unknown error')}")
                    failed += 1
                    errors.append({
                        "test": test["question"],
                        "error": result["error"]
                    })
                elif "result" in result:
                    # Truncate long responses for readability
                    result_str = str(result["result"])
                    if len(result_str) > 200:
                        result_str = result_str[:200] + "..."
                    print(f"    [SUCCESS] {result_str}")
                    passed += 1
                else:
                    print(f"    [WARNING] UNEXPECTED RESPONSE: {result}")
                    failed += 1
                    
            except Exception as e:
                print(f"    [ERROR] EXCEPTION: {str(e)}")
                failed += 1
                errors.append({
                    "test": test["question"],
                    "error": str(e)
                })
            
            # Small delay between requests to avoid rate limiting
            await asyncio.sleep(0.5)
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed} ({passed/total_tests*100:.1f}%)")
    print(f"Failed: {failed} ({failed/total_tests*100:.1f}%)")
    
    if errors:
        print("\nFailed Tests:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error['test']}")
            print(f"    Error: {error['error']}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_tests())