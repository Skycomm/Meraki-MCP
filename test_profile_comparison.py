#!/usr/bin/env python3
"""
Compare different MCP profiles for tool counts and N8N compatibility.
"""

import os
import sys

def test_profile(profile_name):
    """Test a profile and return tool count."""
    print(f"\n🧪 Testing {profile_name} Profile")
    print("=" * 40)
    
    # Set profile environment
    os.environ['MCP_PROFILE'] = profile_name
    
    try:
        # Import fresh server instance
        if 'server.main' in sys.modules:
            del sys.modules['server.main']
        if 'server.profiles' in sys.modules:
            del sys.modules['server.profiles']
            
        from server.main import app
        
        # Get tool count
        tool_count = 0
        if hasattr(app, '_tool_manager') and hasattr(app._tool_manager, '_tools'):
            tool_count = len(app._tool_manager._tools)
            
        # Check N8N compatibility  
        n8n_compatible = "✅" if tool_count <= 128 else "❌"
        
        print(f"📊 Tool Count: {tool_count}")
        print(f"🎯 N8N Compatible (<= 128): {n8n_compatible}")
        
        return tool_count
        
    except Exception as e:
        print(f"❌ Error loading profile: {e}")
        return 0

def main():
    """Compare all profiles."""
    print("🔍 Cisco Meraki MCP Server - Profile Comparison")
    print("=" * 60)
    
    profiles = ['FULL', 'N8N_DIAGNOSTICS', 'N8N_ESSENTIALS', 'MINIMAL']
    results = {}
    
    for profile in profiles:
        results[profile] = test_profile(profile)
    
    print("\n📊 Profile Summary:")
    print("=" * 60)
    for profile, count in results.items():
        n8n_status = "✅ N8N Ready" if count <= 128 else f"❌ Too many ({count} tools)"
        print(f"{profile:15} | {count:3} tools | {n8n_status}")
    
    print("\n💡 Recommendations:")
    print("- For Local Development: FULL profile (all features)")
    print("- For N8N Automation: N8N_ESSENTIALS profile (128 tools max)")
    print("- For Testing: MINIMAL profile (basic operations)")

if __name__ == "__main__":
    main()