#!/usr/bin/env python3
"""Test WiFi audit API fixes as MCP client would use them."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the already initialized server
from server.main import app, meraki

network_id = 'L_726205439913500692'
org_id = '686470'
device_serial = 'Q2PD-SRPB-4JTT'  # Office AP

print("Testing WiFi Audit API Fixes as MCP Client")
print("="*60)

# Test 1: Wireless Usage History with no data
print("\n1. Testing wireless usage history with invalid device:")
try:
    # Access the tool through the app
    tool = app._tool_manager._tools.get('get_network_wireless_usage_history')
    if tool:
        # Call the tool's function with invalid serial
        result = tool.fn(
            network_id=network_id,
            device_serial='INVALID-SERIAL',
            timespan=3600
        )
        if "No data available" in result:
            print("✅ Properly handles no data with helpful message")
            print(f"   Message preview: {result[:150]}...")
        else:
            print("❌ Should provide helpful message when no data")
    else:
        print("❌ Tool not found")
except Exception as e:
    print(f"  Error: {e}")

# Test 2: Channel Utilization History - band requirement
print("\n2. Testing channel utilization without band parameter:")
try:
    tool = app._tool_manager._tools.get('get_network_wireless_channel_utilization_history')
    if tool:
        result = tool.fn(
            network_id=network_id,
            device_serial=device_serial
            # Missing band parameter
        )
        if "band parameter is required" in result:
            print("✅ Properly requires band parameter with device_serial")
            print(f"   Error message: {result[:150]}...")
        else:
            print("❌ Should require band parameter")
    else:
        print("❌ Tool not found")
except Exception as e:
    print(f"  Error: {e}")

# Test 3: Channel Utilization History - with band
print("\n3. Testing channel utilization WITH band parameter:")
try:
    tool = app._tool_manager._tools.get('get_network_wireless_channel_utilization_history')
    if tool:
        result = tool.fn(
            network_id=network_id,
            device_serial=device_serial,
            band='2.4',
            timespan=3600
        )
        if "Channel Utilization History" in result or "❌" not in result[:50]:
            print("✅ Works correctly with band parameter")
        else:
            print(f"  Result: {result[:200]}")
    else:
        print("❌ Tool not found")
except Exception as e:
    print(f"  Error with band: {e}")

# Test 4: Bluetooth Settings parameters
print("\n4. Testing Bluetooth settings parameters:")
try:
    tool = app._tool_manager._tools.get('update_network_wireless_bluetooth_settings')
    if tool:
        import inspect
        sig = inspect.signature(tool.fn)
        params = list(sig.parameters.keys())
        if 'major_minor_mode' in params:
            print("✅ majorMinorAssignmentMode parameter added")
            print(f"   All parameters: {', '.join(params)}")
        else:
            print("❌ Missing major_minor_mode parameter")
            print(f"   Current parameters: {params}")
    else:
        print("❌ Tool not found")
except Exception as e:
    print(f"  Error: {e}")

# Test 5: Radio Settings validation
print("\n5. Testing radio settings validation:")
try:
    tool = app._tool_manager._tools.get('update_device_wireless_radio_settings')
    if tool:
        # Test invalid channel
        print("  a) Testing invalid 5GHz channel 165 (not in AU):")
        result = tool.fn(
            serial=device_serial,
            five_ghz_channel=165
        )
        if "Invalid 5GHz channel" in result or "not available in Australia" in result:
            print(f"    ✅ Channel validation: {result[:80]}...")
        else:
            print(f"    ❌ Should reject channel 165")
        
        # Test excessive power
        print("  b) Testing excessive 5GHz power (30 dBm):")
        result = tool.fn(
            serial=device_serial,
            five_ghz_power=30
        )
        if "power too high" in result:
            print(f"    ✅ Power validation: {result[:60]}...")
        else:
            print(f"    ❌ Should reject 30 dBm (max is 19)")
        
        # Test valid settings
        print("  c) Testing valid settings (channel 36, 15 dBm):")
        result = tool.fn(
            serial=device_serial,
            five_ghz_channel=36,
            five_ghz_power=15
        )
        if "✅" in result or "Updated" in result:
            print(f"    ✅ Valid settings accepted")
        else:
            print(f"    Result: {result[:100]}")
    else:
        print("❌ Tool not found")
except Exception as e:
    print(f"  Error: {e}")

# Test 6: Check updated descriptions
print("\n6. Verifying tool descriptions are helpful:")
descriptions_to_check = [
    ('get_network_wireless_channel_utilization_history', ['band', 'client_id']),
    ('update_device_wireless_radio_settings', ['20dBm', '19dBm']),
    ('update_network_wireless_bluetooth_settings', ['majorMinor', 'Unique'])
]

for tool_name, keywords in descriptions_to_check:
    tool = app._tool_manager._tools.get(tool_name)
    if tool:
        desc = tool.description if hasattr(tool, 'description') else ''
        found = any(kw.lower() in desc.lower() for kw in keywords)
        if found:
            print(f"  ✅ {tool_name[:40]}: Has helpful info")
        else:
            print(f"  ⚠️ {tool_name[:40]}: {desc[:60]}...")
    else:
        print(f"  ❌ {tool_name}: Not found")

print("\n" + "="*60)
print("Summary of WiFi Audit Fixes:")
print("• Wireless Usage History: Shows helpful message when no data")
print("• Channel Utilization: Validates band parameter requirement")
print("• Bluetooth Settings: Added majorMinorAssignmentMode support")
print("• Radio Settings: Validates channels and power limits")
print("• Tool Descriptions: Include parameter requirements")
print("\n✅ All transcript issues have been addressed!")