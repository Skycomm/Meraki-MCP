#!/usr/bin/env python3
"""Test that all 97 tools are available in the hybrid server"""

import sys
sys.path.append('src')

from meraki_tools_simple import ALL_TOOLS

# Expected tool counts by category
EXPECTED_TOOLS = {
    'alerts': 6,
    'analytics': 4,
    'appliance': 6,
    'beta': 6,
    'camera': 6,
    'devices': 6,
    'licensing': 6,
    'live': 10,
    'monitoring': 6,
    'networks': 6,
    'organizations': 8,
    'policy': 6,
    'sm': 7,
    'switch': 5,
    'wireless': 9
}

# Count tools by category
categories = {}
for tool_name in ALL_TOOLS:
    # Extract category from tool name
    if tool_name.startswith('get_organization_'):
        if 'webhook' in tool_name or 'alert' in tool_name:
            cat = 'alerts'
        elif 'uplink' in tool_name or 'appliance_uplink' in tool_name:
            cat = 'analytics'
        elif 'early_access' in tool_name or 'api_analytics' in tool_name:
            cat = 'beta'
        elif 'license' in tool_name or 'licensing' in tool_name:
            cat = 'licensing'
        elif 'policy' in tool_name:
            cat = 'policy'
        elif 'firmware' in tool_name or 'migration' in tool_name or 'api_usage' in tool_name:
            cat = 'monitoring'
        else:
            cat = 'organizations'
    elif tool_name.startswith('get_network_'):
        if 'webhook' in tool_name or 'alert' in tool_name:
            cat = 'alerts'
        elif 'connection_stats' in tool_name or 'latency_stats' in tool_name:
            cat = 'analytics'
        elif 'appliance' in tool_name:
            cat = 'appliance'
        elif 'wireless' in tool_name:
            cat = 'wireless'
        elif 'sm_' in tool_name:
            cat = 'sm'
        else:
            cat = 'networks'
    elif tool_name.startswith('get_device_'):
        if 'camera' in tool_name:
            cat = 'camera'
        elif 'switch' in tool_name:
            cat = 'switch'
        elif 'memory' in tool_name or 'cpu' in tool_name or 'wireless_cpu' in tool_name:
            cat = 'monitoring'
        elif 'ping' in tool_name or 'throughput' in tool_name:
            cat = 'live'
        else:
            cat = 'devices'
    elif 'organization' in tool_name:
        cat = 'organizations'
    elif 'network' in tool_name:
        if 'sm_' in tool_name:
            cat = 'sm'
        elif 'webhook' in tool_name or 'alert' in tool_name:
            cat = 'alerts'
        elif 'wireless' in tool_name:
            cat = 'wireless'
        elif 'appliance' in tool_name:
            cat = 'appliance'
        else:
            cat = 'networks'
    elif 'device' in tool_name:
        if 'ping' in tool_name or 'throughput' in tool_name or 'wake_on_lan' in tool_name or 'leds' in tool_name:
            cat = 'live'
        else:
            cat = 'devices'
    elif 'switch' in tool_name:
        if 'cable_test' in tool_name or 'mac_table' in tool_name:
            cat = 'live'
        else:
            cat = 'switch'
    elif 'camera' in tool_name:
        cat = 'camera'
    elif 'policy' in tool_name:
        cat = 'policy'
    elif 'sm_' in tool_name:
        cat = 'sm'
    elif 'license' in tool_name or 'licensing' in tool_name:
        cat = 'licensing'
    elif 'beta' in tool_name:
        cat = 'beta'
    else:
        cat = 'unknown'
    
    categories[cat] = categories.get(cat, 0) + 1

print(f"Total tools found: {len(ALL_TOOLS)}")
print("\nTools by category:")
for cat, count in sorted(categories.items()):
    expected = EXPECTED_TOOLS.get(cat, 0)
    status = "✅" if count == expected else "❌"
    print(f"  {cat}: {count} {status} (expected: {expected})")

print(f"\nTotal: {sum(categories.values())} tools")

# List all tools
print("\nAll tools:")
for i, tool_name in enumerate(sorted(ALL_TOOLS.keys()), 1):
    print(f"{i:3d}. {tool_name}")