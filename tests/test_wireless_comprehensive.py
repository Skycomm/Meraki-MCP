#!/usr/bin/env python3
"""
Comprehensive test of all wireless tools to ensure they work correctly.
"""

import json
import requests
from datetime import datetime

# Configuration
API_KEY = "2f301bccd61b6c642d250cd3f76e5eb66ebd170f"
BASE_URL = "https://api.meraki.com/api/v1"
ORG_ID = "1374235"
NETWORK_ID = "L_709951935762302054"  # Reserve St
SSID_NUMBER = 0  # Apple SSID

headers = {
    "X-Cisco-Meraki-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def test_api_call(name, method, endpoint, **kwargs):
    """Test a single API call."""
    print(f"Testing: {name}...", end=" ")
    try:
        response = requests.request(
            method, 
            f"{BASE_URL}{endpoint}", 
            headers=headers,
            **kwargs
        )
        
        if response.status_code in [200, 201, 202, 204]:
            print("✅ SUCCESS")
            return True, response.json() if response.text else {}
        else:
            print(f"❌ FAILED: {response.status_code}")
            return False, {"error": response.text}
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False, {"error": str(e)}

print("=" * 80)
print("TESTING WIRELESS API ENDPOINTS DIRECTLY")
print("=" * 80)

tests_passed = 0
tests_failed = 0

# Test basic wireless endpoints
print("\n📡 BASIC WIRELESS ENDPOINTS")
success, data = test_api_call(
    "Get SSIDs",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/ssids"
)
if success: tests_passed += 1
else: tests_failed += 1

success, data = test_api_call(
    "Get SSID Details",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/ssids/{SSID_NUMBER}"
)
if success: tests_passed += 1
else: tests_failed += 1

# Test connection stats
print("\n📊 CONNECTION & PERFORMANCE STATS")
success, data = test_api_call(
    "Connection Stats",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/connectionStats",
    params={"timespan": 86400}
)
if success: tests_passed += 1
else: tests_failed += 1

success, data = test_api_call(
    "Latency Stats",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/latencyStats",
    params={"timespan": 86400}
)
if success: tests_passed += 1
else: tests_failed += 1

success, data = test_api_call(
    "Failed Connections",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/failedConnections",
    params={"timespan": 86400}
)
if success: tests_passed += 1
else: tests_failed += 1

# Test SSID advanced features
print("\n🔧 SSID ADVANCED FEATURES")
success, data = test_api_call(
    "Hotspot 2.0",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/ssids/{SSID_NUMBER}/hotspot20"
)
if success: tests_passed += 1
else: tests_failed += 1

success, data = test_api_call(
    "Splash Settings",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/ssids/{SSID_NUMBER}/splash/settings"
)
if success: tests_passed += 1
else: tests_failed += 1

success, data = test_api_call(
    "SSID Schedules",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/ssids/{SSID_NUMBER}/schedules"
)
if success: tests_passed += 1
else: tests_failed += 1

success, data = test_api_call(
    "SSID VPN",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/ssids/{SSID_NUMBER}/vpn"
)
if success: tests_passed += 1
else: tests_failed += 1

success, data = test_api_call(
    "Bonjour Forwarding",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/ssids/{SSID_NUMBER}/bonjourForwarding"
)
if success: tests_passed += 1
else: tests_failed += 1

success, data = test_api_call(
    "EAP Override",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/ssids/{SSID_NUMBER}/eapOverride"
)
if success: tests_passed += 1
else: tests_failed += 1

success, data = test_api_call(
    "Device Type Policies",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/ssids/{SSID_NUMBER}/deviceTypeGroupPolicies"
)
if success: tests_passed += 1
else: tests_failed += 1

# Test Identity PSKs
print("\n🔑 IDENTITY PSKs")
success, data = test_api_call(
    "Identity PSKs",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/ssids/{SSID_NUMBER}/identityPsks"
)
if success: tests_passed += 1
else: tests_failed += 1

# Test network wireless settings
print("\n⚙️ NETWORK WIRELESS SETTINGS")
success, data = test_api_call(
    "Wireless Settings",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/settings"
)
if success: tests_passed += 1
else: tests_failed += 1

success, data = test_api_call(
    "Bluetooth Settings",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/bluetooth/settings"
)
if success: tests_passed += 1
else: tests_failed += 1

success, data = test_api_call(
    "RF Profiles",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/rfProfiles"
)
if success: tests_passed += 1
else: tests_failed += 1

# Test historical data
print("\n📈 HISTORICAL DATA")
success, data = test_api_call(
    "Client Count History",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/clientCountHistory",
    params={"timespan": 86400}
)
if success: tests_passed += 1
else: tests_failed += 1

success, data = test_api_call(
    "Usage History",
    "GET",
    f"/networks/{NETWORK_ID}/wireless/usageHistory",
    params={"timespan": 86400}
)
if success: tests_passed += 1
else: tests_failed += 1

# Test organization wireless
print("\n🏢 ORGANIZATION WIRELESS")
success, data = test_api_call(
    "Air Marshal Rules",
    "GET",
    f"/organizations/{ORG_ID}/wireless/airMarshal/rules",
    params={"networkIds[]": NETWORK_ID}
)
if success: tests_passed += 1
else: tests_failed += 1

# Summary
print("\n" + "=" * 80)
print("TEST RESULTS SUMMARY")
print("=" * 80)
print(f"✅ Passed: {tests_passed}")
print(f"❌ Failed: {tests_failed}")
print(f"📊 Success Rate: {(tests_passed/(tests_passed+tests_failed)*100):.1f}%")

if tests_failed > 0:
    print("\n⚠️ Some endpoints failed - this may be normal if features aren't enabled")
else:
    print("\n🎉 All tested endpoints are working!")
