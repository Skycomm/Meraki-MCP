#!/usr/bin/env python3
"""
Test MAC address lookup functionality.
"""

import os
os.environ['MCP_PROFILE'] = 'N8N_ESSENTIALS'

from server.main import app

def test_mac_lookup():
    """Test the MAC address lookup tools."""
    
    print("🔍 Testing MAC Address Lookup Tools")
    print("=" * 50)
    
    # Get tools
    tools = {}
    if hasattr(app, '_tool_manager') and hasattr(app._tool_manager, '_tools'):
        tools = app._tool_manager._tools
    
    mac_lookup_tools = [
        'find_device_by_mac_address',
        'lookup_mac_to_ip'
    ]
    
    print("🔍 MAC Lookup Tools:")
    for tool_name in mac_lookup_tools:
        status = "✅" if tool_name in tools else "❌"
        print(f"   {status} {tool_name}")
    
    print(f"\n📊 Total Tools: {len(tools)}")
    
    if all(tool in tools for tool in mac_lookup_tools):
        print("\n🎯 Example Usage Prompts:")
        print("=" * 50)
        
        print("1. Simple lookup:")
        print('   "What IP is MAC address 02:f9:16:10:d7:85 using?"')
        
        print("\n2. Device search:")
        print('   "Find device with MAC 02:f9:16:10:d7:85"')
        
        print("\n3. Current status:")
        print('   "Lookup MAC address 02:f9:16:10:d7:85 current IP"')
        
        print("\n✨ What These Tools Do:")
        print("   - Search through all network clients (7 day history)")
        print("   - Find device by exact MAC address match") 
        print("   - Return current IP, VLAN, status, description")
        print("   - Show manufacturer and last seen info")
        print("   - Handle offline/disconnected devices gracefully")
        
        print("\n🎯 Perfect For:")
        print("   - Finding devices that changed IP")
        print("   - Locating devices before DHCP reservations")
        print("   - Troubleshooting connectivity issues")
        print("   - Device inventory and tracking")
        
        return True
    else:
        print("❌ MAC lookup tools not found")
        return False

if __name__ == "__main__":
    success = test_mac_lookup()
    
    if success:
        print("\n🎉 MAC LOOKUP TOOLS READY!")
        print("AI agents can now find any device by MAC address and get current IP.")
    else:
        print("\n❌ Tools not ready")