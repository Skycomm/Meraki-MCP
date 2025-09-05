#!/usr/bin/env python3
"""
Test the simple Home Assistant DHCP reservation.
"""

import os
os.environ['MCP_PROFILE'] = 'N8N_ESSENTIALS'

from server.main import app

def test_home_assistant_tools():
    """Test Home Assistant specific tools."""
    
    print("🏠 Testing Home Assistant DHCP Tools")
    print("=" * 50)
    
    # Get available tools
    tools = {}
    if hasattr(app, '_tool_manager') and hasattr(app._tool_manager, '_tools'):
        tools = app._tool_manager._tools
    
    home_assistant_tools = [
        'setup_home_assistant_ip_reservation',
        'fix_home_assistant_ip_to_10_0_5_5'
    ]
    
    print("🔍 Home Assistant Specific Tools:")
    for tool_name in home_assistant_tools:
        status = "✅" if tool_name in tools else "❌"
        print(f"   {status} {tool_name}")
    
    # Check total tool count
    tool_count = len(tools)
    print(f"\n📊 Total Tools: {tool_count} (N8N limit: 128)")
    
    # Show the magic prompts
    if 'fix_home_assistant_ip_to_10_0_5_5' in tools:
        print("\n🎯 SUPER SIMPLE PROMPTS THAT SHOULD WORK:")
        print("=" * 50)
        
        print("Option 1 (One-liner):")
        print('   "Fix Home Assistant IP to 10.0.5.5"')
        
        print("\nOption 2 (Specific):")
        print('   "Set up Home Assistant IP reservation to 10.0.5.5"')
        
        print("\nOption 3 (Detailed):")
        print('   "My Home Assistant at 10.0.5.146 needs to be reserved at 10.0.5.5"')
        
        print("\n✨ Why These Will Work:")
        print("   - Tools have pre-loaded MAC address (02:f9:16:10:d7:85)")
        print("   - Network ID is hardcoded (L_726205439913500692)")
        print("   - VLAN 5 is pre-configured")
        print("   - No need to search for device - direct action!")
        
        return True
    else:
        print("❌ Home Assistant tools not found")
        return False

if __name__ == "__main__":
    success = test_home_assistant_tools()
    
    if success:
        print("\n🎉 READY TO GO!")
        print("Your N8N flow should now work with any of the simple prompts above.")
    else:
        print("\n❌ Tools not ready")