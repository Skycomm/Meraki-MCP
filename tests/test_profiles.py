#!/usr/bin/env python3
"""
Test profile configurations for the Meraki MCP Server.
"""

import os
import sys

# Test each profile
profiles = ['WIRELESS', 'NETWORK', 'ORGANIZATIONS', 'MONITORING', 'FULL', 'MINIMAL']

for profile in profiles:
    print(f"\n{'='*60}")
    print(f"Testing {profile} profile...")
    print('='*60)
    
    # Set the profile
    os.environ['MCP_PROFILE'] = profile
    
    # Import fresh
    if 'server.main' in sys.modules:
        del sys.modules['server.main']
    if 'server.profiles' in sys.modules:
        del sys.modules['server.profiles']
    
    try:
        from server.main import app
        
        # Count tools (FastMCP stores them differently)
        tool_count = 0
        if hasattr(app, 'tools'):
            tool_count = len(app.tools)
        elif hasattr(app, '_tool_handlers'):
            tool_count = len(app._tool_handlers)
        else:
            # Try to count registered handlers
            for attr in dir(app):
                if attr.startswith('_') and 'tool' in attr.lower():
                    obj = getattr(app, attr)
                    if isinstance(obj, (dict, list)):
                        tool_count = len(obj)
                        break
        
        print(f"✅ Profile loaded successfully")
        print(f"   Estimated tools: {tool_count}")
        
    except Exception as e:
        print(f"❌ Error loading profile: {e}")

print("\n" + "="*60)
print("Testing custom module loading...")
print("="*60)

# Test custom modules
os.environ['MCP_PROFILE'] = ''
os.environ['MCP_MODULES'] = 'wireless,organizations_core,helpers,search'

if 'server.main' in sys.modules:
    del sys.modules['server.main']
if 'server.profiles' in sys.modules:
    del sys.modules['server.profiles']

try:
    from server.main import app
    print(f"✅ Custom modules loaded successfully")
except Exception as e:
    print(f"❌ Error loading custom modules: {e}")

# Clean up
del os.environ['MCP_MODULES']