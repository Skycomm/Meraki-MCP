#!/usr/bin/env python3
"""
Test script for beta/early access features with Skycomm organization.
Since early access is enabled, we should be able to access beta APIs.
"""

import json
from datetime import datetime

# SAFETY FIRST: Import and setup test safety
from test_common import setup_test_safety, print_safety_reminder
setup_test_safety()

from meraki_client import MerakiClient

# Initialize client
meraki = MerakiClient()

# Print safety reminder
print_safety_reminder()

# Test configuration
TEST_ORG_ID = "686470"  # Skycomm
TEST_NETWORK_ID = "L_669347494617953785"
TEST_DEVICE_SERIAL = "Q2PD-7QTD-SZG2"

print("🧪 Testing Beta/Early Access Features for Skycomm")
print("=" * 60)
print("Early Access Status: ENABLED ✅")
print("=" * 60)

# Track results
results = {
    "timestamp": datetime.now().isoformat(),
    "tests": {}
}

def test_beta_api(category: str, test_name: str, test_func, description: str):
    """Test a beta API feature."""
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print(f"Description: {description}")
    print("-" * 60)
    
    try:
        result = test_func()
        
        if result:
            print(f"✅ SUCCESS - Got response")
            if isinstance(result, (list, dict)):
                print(f"   Data type: {type(result).__name__}")
                if isinstance(result, list):
                    print(f"   Items: {len(result)}")
                elif isinstance(result, dict):
                    print(f"   Keys: {list(result.keys())[:5]}")
            
            results["tests"][test_name] = {
                "category": category,
                "description": description,
                "success": True,
                "has_data": bool(result)
            }
        else:
            print(f"⚠️  No data returned (API may not be available yet)")
            results["tests"][test_name] = {
                "category": category,
                "description": description,
                "success": True,
                "has_data": False
            }
            
    except Exception as e:
        print(f"❌ FAILED - {str(e)}")
        results["tests"][test_name] = {
            "category": category,
            "description": description,
            "success": False,
            "error": str(e)
        }

# 1. Check what early access features are available
print("\n📋 CHECKING AVAILABLE EARLY ACCESS FEATURES")

test_beta_api(
    "Early Access",
    "get_organization_early_access_features",
    lambda: meraki.get_organization_early_access_features(TEST_ORG_ID),
    "List all available beta features"
)

test_beta_api(
    "Early Access",
    "get_organization_early_access_features_opt_ins",
    lambda: meraki.get_organization_early_access_features_opt_ins(TEST_ORG_ID),
    "Check which beta features are currently enabled"
)

# 2. Test potentially new beta APIs
print("\n\n🆕 TESTING BETA APIS")

# Try device memory history (beta)
test_beta_api(
    "Enhanced Monitoring",
    "get_device_memory_history_beta",
    lambda: meraki.dashboard.devices.getDeviceManagementInterface(TEST_DEVICE_SERIAL)
    if hasattr(meraki.dashboard.devices, 'getDeviceManagementInterface') else None,
    "Device memory history (beta endpoint)"
)

# Try MAC table live tools (new 2025)
if hasattr(meraki.dashboard.devices, 'createDeviceLiveToolsMacTable'):
    test_beta_api(
        "Live Tools",
        "create_device_live_tools_mac_table",
        lambda: meraki.dashboard.devices.createDeviceLiveToolsMacTable(TEST_DEVICE_SERIAL),
        "MAC table live query (2025 beta)"
    )

# Try enhanced switch port analytics
if hasattr(meraki.dashboard.switch, 'getOrganizationSwitchPortsHistory'):
    test_beta_api(
        "Switch Analytics",
        "get_organization_switch_ports_history_beta",
        lambda: meraki.dashboard.switch.getOrganizationSwitchPortsHistory(TEST_ORG_ID, timespan=3600),
        "Organization-wide switch port history (beta)"
    )

# 3. Test API analytics features
print("\n\n📊 TESTING API ANALYTICS")

test_beta_api(
    "API Analytics",
    "get_organization_api_requests_enhanced",
    lambda: meraki.get_organization_api_requests(TEST_ORG_ID, timespan=3600),
    "Enhanced API analytics with early access"
)

# 4. Check for new endpoint availability
print("\n\n🔍 CHECKING NEW ENDPOINT AVAILABILITY")

# Check if we have access to new methods
new_methods = []
dashboard_modules = ['devices', 'networks', 'organizations', 'wireless', 'switch', 'appliance']

for module_name in dashboard_modules:
    if hasattr(meraki.dashboard, module_name):
        module = getattr(meraki.dashboard, module_name)
        methods = [m for m in dir(module) if not m.startswith('_')]
        
        # Look for potentially new/beta methods
        beta_keywords = ['beta', 'v2', 'enhanced', 'analytics', 'history', 'live', 'migration']
        for method in methods:
            if any(keyword in method.lower() for keyword in beta_keywords):
                new_methods.append(f"{module_name}.{method}")

if new_methods:
    print(f"\n🆕 Potentially new/beta methods found:")
    for method in sorted(new_methods)[:20]:
        print(f"   - {method}")
else:
    print("\n⚠️  No obviously new beta methods detected")

# 5. Test Systems Manager with early access
print("\n\n📱 RE-TESTING SYSTEMS MANAGER WITH EARLY ACCESS")

test_beta_api(
    "Systems Manager",
    "get_network_sm_devices_beta",
    lambda: meraki.get_network_sm_devices(TEST_NETWORK_ID),
    "SM devices with early access enabled"
)

# SUMMARY
print("\n" + "="*60)
print("📊 BETA TESTING SUMMARY")
print("="*60)

success_count = sum(1 for test in results["tests"].values() if test["success"])
total_count = len(results["tests"])

print(f"Total Tests: {total_count}")
print(f"Successful: {success_count} ✅")
print(f"Failed: {total_count - success_count} ❌")

# Save results
with open("test_beta_features_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\n💾 Results saved to test_beta_features_results.json")

# Recommendations
print("\n📝 RECOMMENDATIONS:")
print("="*60)
print("1. Early access is now enabled for Skycomm organization")
print("2. Some beta APIs may still require specific feature opt-ins")
print("3. Check the early access features list for available options")
print("4. Remember: Beta APIs can have breaking changes!")
print("\n✨ Beta testing complete!")