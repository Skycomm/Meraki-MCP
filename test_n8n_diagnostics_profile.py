#!/usr/bin/env python3
"""
Test the N8N_DIAGNOSTICS profile has all the essential tools for automated network diagnostics.

Key workflow: Caller ID → Client lookup → Network discovery → Performance diagnostics → Health checks
"""

import os
os.environ['MCP_PROFILE'] = 'N8N_DIAGNOSTICS'

from server.main import app

def test_n8n_diagnostics_tools():
    """Test that N8N_DIAGNOSTICS profile has the essential diagnostic tools."""
    
    print("🧪 Testing N8N_DIAGNOSTICS Profile")
    print("=" * 50)
    
    # Essential tools for the automated diagnostics workflow
    essential_tools = {
        # Client/Org Discovery
        "get_organizations": "Find client organizations", 
        "get_organization_networks": "Get client networks",
        "search_device_by_serial": "Cross-org device search",
        
        # Performance Diagnostics (the core tools!)
        "get_device_loss_and_latency_history": "Device latency/packet loss",
        "get_organization_devices_uplinks_loss_and_latency": "Org-wide performance",
        "get_network_wireless_latency_stats": "WiFi latency stats",
        "get_organization_wireless_devices_packet_loss_by_network": "WiFi packet loss",
        
        # Health & Status
        "get_organization_devices_statuses": "Device up/down status",
        "get_network_health_alerts": "Active alerts",
        "get_organization_uplinks_statuses": "WAN connectivity",
        
        # Client Analytics
        "get_network_clients": "Connected devices",
        "get_network_wireless_client_latency_stats": "Client performance",
        
        # Network Discovery
        "get_network_devices": "Network device list",
        "get_network": "Network details",
        "get_device": "Device details"
    }
    
    # Get all registered tools from FastMCP
    all_tools = set()
    
    # Explore FastMCP object attributes
    print(f"FastMCP object attributes: {[attr for attr in dir(app) if not attr.startswith('_')]}")
    
    # Use list_tools method to get registered tools
    try:
        tools_response = app.list_tools()
        if hasattr(tools_response, 'tools'):
            all_tools = {tool.name for tool in tools_response.tools}
            print("✅ Found tools using app.list_tools()")
        else:
            print("✅ Found app.list_tools() but no tools attribute")
    except Exception as e:
        print(f"⚠️  Error calling list_tools(): {e}")
        
    # Fallback: try _tool_manager
    if not all_tools and hasattr(app, '_tool_manager'):
        try:
            if hasattr(app._tool_manager, '_tools'):
                all_tools = set(app._tool_manager._tools.keys())
                print("✅ Found tools using _tool_manager._tools")
        except Exception as e:
            print(f"⚠️  Error accessing _tool_manager: {e}")
    
    print(f"📊 Total tools loaded: {len(all_tools)}")
    print()
    
    # Check essential tools
    missing_tools = []
    found_tools = []
    
    for tool_name, description in essential_tools.items():
        if tool_name in all_tools:
            found_tools.append(f"✅ {tool_name} - {description}")
        else:
            missing_tools.append(f"❌ {tool_name} - {description}")
    
    print("🎯 Essential Diagnostic Tools:")
    for tool in found_tools:
        print(f"  {tool}")
    
    if missing_tools:
        print("\n⚠️  Missing Essential Tools:")
        for tool in missing_tools:
            print(f"  {tool}")
    
    print(f"\n📈 Coverage: {len(found_tools)}/{len(essential_tools)} essential tools found")
    
    # Check if we're within N8N's 128 tool limit
    if len(all_tools) <= 128:
        print(f"✅ Tool count ({len(all_tools)}) is within N8N's 128 tool limit")
    else:
        print(f"⚠️  Tool count ({len(all_tools)}) exceeds N8N's 128 tool limit")
    
    return len(missing_tools) == 0

if __name__ == "__main__":
    success = test_n8n_diagnostics_tools()
    print("\n" + "=" * 50)
    if success:
        print("🎉 N8N_DIAGNOSTICS profile is ready for automated network diagnostics!")
        print("💡 Use: MCP_PROFILE=N8N_DIAGNOSTICS ./run_n8n_diagnostics.sh")
    else:
        print("❌ Profile needs adjustments - some essential tools missing")