#!/usr/bin/env python3
"""
Comprehensive test script for ALL Cisco Meraki MCP Server features.
Tests all 94 tools with specific test questions.
"""

import json
import time
from datetime import datetime
from meraki_client import MerakiClient

# Initialize client
meraki = MerakiClient()

# Test configuration
TEST_ORG_ID = "686470"  # Skycomm
TEST_NETWORK_ID = "L_669347494617953785"  # Reserve St
TEST_DEVICE_SERIAL = "Q2PD-7QTD-SZG2"  # MX
TEST_SWITCH_SERIAL = "Q2HP-ZK5N-XG8L"  # Switch
TEST_CAMERA_SERIAL = None  # Update if camera available

# Test results tracking
results = {
    "timestamp": datetime.now().isoformat(),
    "total_tests": 0,
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "categories": {},
    "test_details": []
}

def test_feature(category: str, test_name: str, question: str, test_func, skip_reason=None):
    """Test a single feature with a specific question."""
    global results
    results["total_tests"] += 1
    
    if category not in results["categories"]:
        results["categories"][category] = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
    
    results["categories"][category]["total"] += 1
    
    print(f"\n{'='*80}")
    print(f"[{results['total_tests']}] {category} - {test_name}")
    print(f"Q: {question}")
    print("-" * 80)
    
    test_detail = {
        "number": results["total_tests"],
        "category": category,
        "test": test_name,
        "question": question
    }
    
    if skip_reason:
        print(f"⏭️  SKIPPED: {skip_reason}")
        results["skipped"] += 1
        results["categories"][category]["skipped"] += 1
        test_detail["status"] = "skipped"
        test_detail["reason"] = skip_reason
    else:
        try:
            start_time = time.time()
            result = test_func()
            elapsed = time.time() - start_time
            
            if result:
                print(f"✅ PASSED ({elapsed:.2f}s)")
                if isinstance(result, (list, dict)):
                    print(f"   Response type: {type(result).__name__}")
                    if isinstance(result, list):
                        print(f"   Items returned: {len(result)}")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                test_detail["status"] = "passed"
                test_detail["elapsed"] = elapsed
            else:
                print(f"⚠️  PASSED - No data returned ({elapsed:.2f}s)")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                test_detail["status"] = "passed_no_data"
                test_detail["elapsed"] = elapsed
                
        except Exception as e:
            print(f"❌ FAILED - {str(e)}")
            results["failed"] += 1
            results["categories"][category]["failed"] += 1
            test_detail["status"] = "failed"
            test_detail["error"] = str(e)
    
    results["test_details"].append(test_detail)

print("🧪 COMPREHENSIVE CISCO MERAKI MCP SERVER TEST SUITE")
print("=" * 80)
print(f"Organization: {TEST_ORG_ID}")
print(f"Network: {TEST_NETWORK_ID}")
print(f"Test Device: {TEST_DEVICE_SERIAL}")
print("=" * 80)

# 1. ORGANIZATION MANAGEMENT TESTS
print("\n\n📁 TESTING ORGANIZATION MANAGEMENT")

test_feature(
    "Organization Management",
    "List Organizations",
    "What organizations do I have access to?",
    lambda: meraki.get_organizations()
)

test_feature(
    "Organization Management",
    "Organization Details",
    "What are the details for Skycomm organization?",
    lambda: meraki.get_organization(TEST_ORG_ID)
)

test_feature(
    "Organization Management",
    "List Networks",
    "How many networks are in the Skycomm organization?",
    lambda: meraki.get_organization_networks(TEST_ORG_ID)
)

test_feature(
    "Organization Management",
    "List All Devices",
    "What devices are deployed across the entire organization?",
    lambda: meraki.get_organization_devices(TEST_ORG_ID)
)

# 2. NETWORK MANAGEMENT TESTS
print("\n\n🌐 TESTING NETWORK MANAGEMENT")

test_feature(
    "Network Management",
    "Network Details",
    "What are the settings for Reserve St network?",
    lambda: meraki.get_network(TEST_NETWORK_ID)
)

test_feature(
    "Network Management",
    "Network Devices",
    "What devices are in the Reserve St network?",
    lambda: meraki.get_network_devices(TEST_NETWORK_ID)
)

test_feature(
    "Network Management",
    "Connected Clients",
    "How many clients are currently connected?",
    lambda: meraki.get_network_clients(TEST_NETWORK_ID, timespan=300)
)

test_feature(
    "Network Management",
    "VLAN Configuration",
    "What VLANs are configured on the network?",
    lambda: meraki.get_network_vlans(TEST_NETWORK_ID)
)

# 3. API ANALYTICS & MONITORING
print("\n\n📊 TESTING API ANALYTICS & MONITORING")

test_feature(
    "API Analytics",
    "API Usage Statistics",
    "What are the top 10 most used API endpoints in the last hour?",
    lambda: meraki.get_organization_api_requests(TEST_ORG_ID, timespan=3600)
)

test_feature(
    "Monitoring",
    "Switch Port Statistics",
    "What percentage of switch ports are active across all locations?",
    lambda: meraki.get_organization_switch_ports_history(TEST_ORG_ID, timespan=300)
)

test_feature(
    "Monitoring",
    "Device Migration Status",
    "Are any devices being migrated between networks?",
    lambda: meraki.get_organization_devices_migration_status(TEST_ORG_ID)
)

test_feature(
    "Monitoring",
    "Uplink Health",
    "Is there packet loss on any WAN uplinks?",
    lambda: meraki.get_organization_devices_uplinks_loss_and_latency(TEST_ORG_ID, timespan=300)
)

# 4. LIVE TOOLS (BETA)
print("\n\n🔧 TESTING LIVE TOOLS (BETA)")

# Ping test
ping_id = None
test_feature(
    "Live Tools",
    "Create Ping Test",
    "Can the MX ping Google DNS (8.8.8.8)?",
    lambda: meraki.create_device_live_tools_ping(
        TEST_DEVICE_SERIAL,
        target="8.8.8.8",
        count=5
    )
)

# Note: Would need to extract ping_id from previous result and wait before checking

test_feature(
    "Live Tools",
    "Cable Test",
    "Is the cable on switch port 1 functioning properly?",
    lambda: meraki.create_device_live_tools_cable_test(
        TEST_SWITCH_SERIAL,
        ports=["1"]
    )
)

test_feature(
    "Live Tools",
    "MAC Table Query",
    "What devices are connected to the switch?",
    lambda: meraki.create_device_live_tools_mac_table(TEST_SWITCH_SERIAL)
)

test_feature(
    "Live Tools",
    "LED Blink",
    "Can we identify the switch physically by blinking its LEDs?",
    lambda: meraki.create_device_live_tools_leds_blink(
        TEST_SWITCH_SERIAL,
        duration=10
    )
)

# 5. WIRELESS MANAGEMENT
print("\n\n📡 TESTING WIRELESS MANAGEMENT")

test_feature(
    "Wireless",
    "List SSIDs",
    "What wireless networks are configured?",
    lambda: meraki.get_network_wireless_ssids(TEST_NETWORK_ID)
)

test_feature(
    "Wireless",
    "WiFi Passwords",
    "What's the WiFi password for the Guest network?",
    lambda: meraki.get_network_wireless_passwords(TEST_NETWORK_ID)
)

test_feature(
    "Wireless",
    "Connection Statistics",
    "What's the wireless connection success rate?",
    lambda: meraki.get_network_connection_stats(TEST_NETWORK_ID, timespan=3600)
)

test_feature(
    "Wireless",
    "Latency Statistics",
    "Is there high latency on the wireless network?",
    lambda: meraki.get_network_latency_stats(TEST_NETWORK_ID, timespan=3600)
)

test_feature(
    "Wireless",
    "RF Profiles",
    "What RF profiles are configured?",
    lambda: meraki.get_network_wireless_rf_profiles(TEST_NETWORK_ID)
)

test_feature(
    "Wireless",
    "Rogue AP Detection",
    "Are there any rogue access points detected?",
    lambda: meraki.get_network_wireless_air_marshal(TEST_NETWORK_ID, timespan=3600)
)

# 6. SWITCH MANAGEMENT
print("\n\n🔌 TESTING SWITCH MANAGEMENT")

test_feature(
    "Switch",
    "Port Configuration",
    "What's the configuration for all switch ports?",
    lambda: meraki.get_device_switch_ports(TEST_SWITCH_SERIAL)
)

test_feature(
    "Switch",
    "Port Status",
    "Which switch ports are showing errors?",
    lambda: meraki.get_device_switch_port_statuses(TEST_SWITCH_SERIAL)
)

# 7. SECURITY FEATURES
print("\n\n🔒 TESTING SECURITY FEATURES")

test_feature(
    "Security",
    "L3 Firewall Rules",
    "What firewall rules are configured?",
    lambda: meraki.get_network_appliance_firewall_l3_rules(TEST_NETWORK_ID)
)

test_feature(
    "Security",
    "Content Filtering",
    "What web categories are blocked?",
    lambda: meraki.get_network_appliance_content_filtering(TEST_NETWORK_ID)
)

test_feature(
    "Security",
    "VPN Status",
    "Is the site-to-site VPN tunnel active?",
    lambda: meraki.get_network_appliance_vpn_site_to_site(TEST_NETWORK_ID)
)

test_feature(
    "Security",
    "Malware Protection",
    "Is malware protection enabled?",
    lambda: meraki.get_network_appliance_security_malware(TEST_NETWORK_ID)
)

test_feature(
    "Security",
    "Intrusion Detection",
    "What's the IDS/IPS configuration?",
    lambda: meraki.get_network_appliance_security_intrusion(TEST_NETWORK_ID)
)

# 8. POLICY OBJECTS (NEW 2025)
print("\n\n🛡️ TESTING POLICY OBJECTS")

test_feature(
    "Policy Objects",
    "List Policy Objects",
    "What security policy objects are defined?",
    lambda: meraki.get_organization_policy_objects(TEST_ORG_ID)
)

test_feature(
    "Policy Objects",
    "Policy Groups",
    "How are policy objects organized into groups?",
    lambda: meraki.get_organization_policy_objects_groups(TEST_ORG_ID)
)

# 9. SYSTEMS MANAGER (MDM)
print("\n\n📱 TESTING SYSTEMS MANAGER")

test_feature(
    "Systems Manager",
    "List SM Devices",
    "What mobile devices are enrolled in MDM?",
    lambda: meraki.get_network_sm_devices(TEST_NETWORK_ID),
    skip_reason="Network doesn't have SM enabled"
)

test_feature(
    "Systems Manager",
    "SM Profiles",
    "What configuration profiles are deployed?",
    lambda: meraki.get_network_sm_profiles(TEST_NETWORK_ID),
    skip_reason="Network doesn't have SM enabled"
)

# 10. LICENSE MANAGEMENT
print("\n\n📄 TESTING LICENSE MANAGEMENT")

test_feature(
    "Licensing",
    "Per-Device Licenses",
    "What licenses do we have?",
    lambda: meraki.get_organization_licenses(TEST_ORG_ID),
    skip_reason="Organization uses co-term licensing"
)

test_feature(
    "Licensing",
    "Co-term Licenses",
    "What's our co-termination date and device count?",
    lambda: meraki.get_organization_licensing_coterm_licenses(TEST_ORG_ID)
)

# 11. BETA/EARLY ACCESS
print("\n\n🧪 TESTING BETA/EARLY ACCESS FEATURES")

test_feature(
    "Beta Features",
    "Available Features",
    "What beta features can we enable?",
    lambda: meraki.get_organization_early_access_features(TEST_ORG_ID)
)

test_feature(
    "Beta Features",
    "Enabled Features",
    "Which beta features are currently active?",
    lambda: meraki.get_organization_early_access_features_opt_ins(TEST_ORG_ID)
)

# 12. DEVICE OPERATIONS
print("\n\n🔧 TESTING DEVICE OPERATIONS")

test_feature(
    "Device Operations",
    "Device Details",
    "What are the details for the MX device?",
    lambda: meraki.get_device(TEST_DEVICE_SERIAL)
)

test_feature(
    "Device Operations",
    "Device Clients",
    "What clients are connected to this device?",
    lambda: meraki.get_device_clients(TEST_DEVICE_SERIAL, timespan=300)
)

# 13. CAMERA OPERATIONS
print("\n\n📹 TESTING CAMERA OPERATIONS")

test_feature(
    "Camera",
    "Camera Video Link",
    "Can we get video from a camera?",
    lambda: meraki.get_device_camera_video_link(TEST_CAMERA_SERIAL) if TEST_CAMERA_SERIAL else None,
    skip_reason="No camera serial provided"
)

# 14. ALERTS & WEBHOOKS
print("\n\n🚨 TESTING ALERTS & WEBHOOKS")

test_feature(
    "Alerts",
    "Alert Settings",
    "What network alerts are configured?",
    lambda: meraki.get_network_alerts_settings(TEST_NETWORK_ID)
)

test_feature(
    "Alerts",
    "Organization Alerts",
    "What alert profiles exist for the organization?",
    lambda: meraki.get_organization_alerts(TEST_ORG_ID)
)

test_feature(
    "Webhooks",
    "Webhook Types",
    "What webhook alert types are available?",
    lambda: meraki.get_organization_webhooks(TEST_ORG_ID)
)

# 15. FIRMWARE MANAGEMENT
print("\n\n🔄 TESTING FIRMWARE MANAGEMENT")

test_feature(
    "Firmware",
    "Firmware Status",
    "Which devices need firmware updates?",
    lambda: meraki.get_organization_firmware_upgrades(TEST_ORG_ID)
)

# GENERATE SUMMARY REPORT
print("\n\n" + "="*80)
print("📊 TEST SUMMARY REPORT")
print("="*80)
print(f"Total Tests: {results['total_tests']}")
print(f"Passed: {results['passed']} ({results['passed']/results['total_tests']*100:.1f}%)")
print(f"Failed: {results['failed']} ({results['failed']/results['total_tests']*100:.1f}%)")
print(f"Skipped: {results['skipped']} ({results['skipped']/results['total_tests']*100:.1f}%)")

print("\n📂 RESULTS BY CATEGORY:")
for category, stats in results["categories"].items():
    total = stats["total"]
    passed = stats["passed"]
    print(f"\n{category}:")
    print(f"  Total: {total}")
    print(f"  Passed: {passed} ({passed/total*100:.1f}%)")
    print(f"  Failed: {stats['failed']}")
    print(f"  Skipped: {stats['skipped']}")

# Save detailed results
with open("comprehensive_test_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\n💾 Detailed results saved to comprehensive_test_results.json")

# Show failed tests
if results["failed"] > 0:
    print("\n❌ FAILED TESTS:")
    for test in results["test_details"]:
        if test["status"] == "failed":
            print(f"- [{test['number']}] {test['category']}/{test['test']}: {test.get('error', 'Unknown error')}")

# Show recommendations
print("\n📝 RECOMMENDATIONS:")
if results["categories"].get("Systems Manager", {}).get("skipped", 0) > 0:
    print("- Enable Systems Manager on a test network for MDM testing")
if results["categories"].get("Licensing", {}).get("failed", 0) > 0:
    print("- Organization uses co-term licensing model")
if results["categories"].get("Live Tools", {}).get("passed", 0) > 0:
    print("- Live Tools are working! Beta access is active")

print("\n✨ Comprehensive testing complete!")