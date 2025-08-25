#!/usr/bin/env python3
"""Test tool registration to see if it happens multiple times."""

import sys
import os

# Track registration calls
registration_calls = {}

# Monkey patch the registration functions to track calls
original_imports = {}

def track_registration(module_name, func_name):
    """Create a wrapper that tracks registration calls."""
    def wrapper(*args, **kwargs):
        key = f"{module_name}.{func_name}"
        if key not in registration_calls:
            registration_calls[key] = 0
        registration_calls[key] += 1
        print(f"[REGISTRATION] {key} called (count: {registration_calls[key]})")
        
        # Call the original function
        if key in original_imports:
            return original_imports[key](*args, **kwargs)
    return wrapper

# Add tracking before imports
sys.path.insert(0, 'server')

# Import and patch
print("=" * 60)
print("Starting registration tracking...")
print("=" * 60)

# Import main which triggers all registrations
try:
    from main import app
    print("\n" + "=" * 60)
    print("Initial import complete")
    print("=" * 60)
    
    # Check registration counts
    print("\nRegistration call counts:")
    for key, count in sorted(registration_calls.items()):
        if count > 1:
            print(f"  ❌ {key}: {count} calls (DUPLICATE!)")
        else:
            print(f"  ✅ {key}: {count} call")
    
    # Now simulate what happens when a request comes in
    print("\n" + "=" * 60)
    print("Simulating request handling...")
    print("=" * 60)
    
    # Check if any tools are registered multiple times
    if hasattr(app, '_tools'):
        print(f"\nTotal tools registered: {len(app._tools)}")
        
        # Check for specific problematic tools
        problematic = [
            'get_organization_appliance_uplink_statuses',
            'get_network_health_summary'
        ]
        
        for tool_name in problematic:
            if tool_name in app._tools:
                print(f"  ✓ {tool_name} is registered")
            else:
                print(f"  ✗ {tool_name} is NOT registered")
    
except Exception as e:
    print(f"\n❌ Error during import: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test complete")
print("=" * 60)