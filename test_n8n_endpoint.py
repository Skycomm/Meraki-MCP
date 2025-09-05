#!/usr/bin/env python3
"""
Test the N8N HTTP streamable endpoint is working correctly.
"""

import requests
import json
import os

def test_n8n_endpoint():
    """Test the MCP HTTP streamable endpoint for N8N."""
    
    endpoint = "http://localhost:8100/mcp"
    
    print("🧪 Testing N8N MCP Endpoint")
    print("=" * 40)
    print(f"📡 Endpoint: {endpoint}")
    
    try:
        # Test if server is running
        response = requests.get(endpoint, timeout=5)
        print(f"✅ Server Status: {response.status_code}")
        
        # Test tools endpoint
        tools_response = requests.post(
            f"{endpoint}/tools/list",
            json={},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if tools_response.status_code == 200:
            tools_data = tools_response.json()
            tool_count = len(tools_data.get('tools', []))
            print(f"✅ Tools Available: {tool_count}")
            
            if tool_count <= 128:
                print(f"✅ N8N Compatible: {tool_count} <= 128 tools")
            else:
                print(f"⚠️  Too many tools: {tool_count} > 128")
                
            # Show some key diagnostic tools
            tools = tools_data.get('tools', [])
            key_tools = [
                'get_organizations',
                'get_device_loss_and_latency_history', 
                'get_network_health_alerts',
                'check_network_health',
                'search_device_by_serial'
            ]
            
            print("\n🔍 Key Diagnostic Tools:")
            for tool_name in key_tools:
                found = any(tool.get('name') == tool_name for tool in tools)
                status = "✅" if found else "❌"
                print(f"  {status} {tool_name}")
                
        else:
            print(f"❌ Tools Error: {tools_response.status_code}")
            print(f"Response: {tools_response.text[:200]}...")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: MCP server not running")
        print("💡 Start with: ./run_n8n_http_server.sh")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("💡 N8N Setup:")
    print("   1. Start MCP server: ./run_n8n_http_server.sh")
    print("   2. N8N endpoint: http://localhost:8100/mcp")
    print("   3. Profile: N8N_ESSENTIALS (97 tools)")

if __name__ == "__main__":
    test_n8n_endpoint()