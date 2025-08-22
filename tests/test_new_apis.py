#!/usr/bin/env python3
"""
Test script for new 2025 Cisco Meraki APIs.
Tests each new API with appropriate test questions/scenarios.
"""

import json
import time
from datetime import datetime
from meraki_client import MerakiClient

# Initialize client
meraki = MerakiClient()

# Test configuration
TEST_ORG_ID = "686470"
TEST_NETWORK_ID = "L_669347494617953785"
TEST_DEVICE_SERIAL = "Q2PD-7QTD-SZG2"
TEST_SWITCH_SERIAL = "Q2HP-ZK5N-XG8L"

# Track results
results = {
    "timestamp": datetime.now().isoformat(),
    "total_tests": 0,
    "passed": 0,
    "failed": 0,
    "errors": [],
    "test_questions": {}
}

def test_api(category: str, test_name: str, test_question: str, test_func):
    """Test a single API with a specific question."""
    global results
    results["total_tests"] += 1
    
    print(f"\n{'='*60}")
    print(f"Category: {category}")
    print(f"Test: {test_name}")
    print(f"Question: {test_question}")
    print("-" * 60)
    
    try:
        result = test_func()
        
        # Store the test question and result
        if category not in results["test_questions"]:
            results["test_questions"][category] = []
            
        results["test_questions"][category].append({
            "test": test_name,
            "question": test_question,
            "success": True,
            "has_data": bool(result)
        })
        
        if result:
            print(f"✅ PASSED - Got response")
            if isinstance(result, (list, dict)):
                print(f"   Data type: {type(result).__name__}")
                if isinstance(result, list):
                    print(f"   Items: {len(result)}")
                elif isinstance(result, dict):
                    print(f"   Keys: {list(result.keys())[:5]}")
            results["passed"] += 1
        else:
            print(f"⚠️  PASSED - No data returned (may be normal)")
            results["passed"] += 1
            
    except Exception as e:
        print(f"❌ FAILED - {str(e)}")
        results["failed"] += 1
        results["errors"].append({
            "category": category,
            "test": test_name,
            "question": test_question,
            "error": str(e)
        })
        
        if category not in results["test_questions"]:
            results["test_questions"][category] = []
            
        results["test_questions"][category].append({
            "test": test_name,
            "question": test_question,
            "success": False,
            "error": str(e)
        })

print("🧪 Testing New 2025 Cisco Meraki APIs")
print("=" * 60)

# 1. SYSTEMS MANAGER TESTS
print("\n📱 SYSTEMS MANAGER (SM) TESTS")

test_api(
    "Systems Manager",
    "get_network_sm_devices",
    "What mobile devices are enrolled in our MDM system?",
    lambda: meraki.get_network_sm_devices(TEST_NETWORK_ID)
)

test_api(
    "Systems Manager", 
    "get_network_sm_profiles",
    "What configuration profiles are deployed to our managed devices?",
    lambda: meraki.get_network_sm_profiles(TEST_NETWORK_ID)
)

# Note: These require actual SM device IDs
print("\n⚠️  Skipping SM device-specific tests (need actual device IDs)")

# 2. LICENSING TESTS
print("\n\n📄 LICENSING MANAGEMENT TESTS")

test_api(
    "Licensing",
    "get_organization_licenses",
    "How many licenses do we have and when do they expire?",
    lambda: meraki.get_organization_licenses(TEST_ORG_ID)
)

test_api(
    "Licensing",
    "get_organization_licensing_coterm_licenses",
    "What is our co-termination date and license count by model?",
    lambda: meraki.get_organization_licensing_coterm_licenses(TEST_ORG_ID)
)

# Note: Skip claim/update/move as they modify production
print("\n⚠️  Skipping license modification tests (would affect production)")

# 3. POLICY OBJECTS TESTS
print("\n\n🛡️ POLICY OBJECTS TESTS")

test_api(
    "Policy Objects",
    "get_organization_policy_objects",
    "What security policy objects are defined for blocking IPs/domains?",
    lambda: meraki.get_organization_policy_objects(TEST_ORG_ID)
)

test_api(
    "Policy Objects",
    "get_organization_policy_objects_groups",
    "How are our policy objects organized into groups?",
    lambda: meraki.get_organization_policy_objects_groups(TEST_ORG_ID)
)

# Test creating a policy object (safe test object)
test_api(
    "Policy Objects",
    "create_organization_policy_object",
    "Can we create a test policy object for IP 192.168.100.100?",
    lambda: meraki.create_organization_policy_object(
        TEST_ORG_ID,
        name="TEST_API_Object_" + str(int(time.time())),
        category="network",
        type="ipv4",
        cidr="192.168.100.100/32"
    )
)

# 4. ENHANCED MONITORING TESTS
print("\n\n📊 ENHANCED MONITORING TESTS")

test_api(
    "Enhanced Monitoring",
    "get_organization_api_requests",
    "What API endpoints are being used most frequently?",
    lambda: meraki.get_organization_api_requests(TEST_ORG_ID, timespan=3600)
)

test_api(
    "Enhanced Monitoring",
    "get_organization_switch_ports_history",
    "How many switch ports are active across the organization?",
    lambda: meraki.get_organization_switch_ports_history(TEST_ORG_ID, timespan=3600)
)

test_api(
    "Enhanced Monitoring",
    "get_organization_devices_migration_status",
    "Are any devices currently being migrated between networks?",
    lambda: meraki.get_organization_devices_migration_status(TEST_ORG_ID)
)

# Device-specific monitoring (these might not return expected data)
test_api(
    "Enhanced Monitoring",
    "get_device_memory_history",
    "What is the memory usage history for device " + TEST_DEVICE_SERIAL + "?",
    lambda: meraki.get_device_memory_history(TEST_DEVICE_SERIAL, timespan=3600)
)

test_api(
    "Enhanced Monitoring",
    "get_device_wireless_cpu_load",
    "What is the current CPU load on wireless device " + TEST_DEVICE_SERIAL + "?",
    lambda: meraki.get_device_wireless_cpu_load(TEST_DEVICE_SERIAL)
)

# SUMMARY
print("\n" + "="*60)
print("📊 TEST SUMMARY")
print("="*60)
print(f"Total Tests: {results['total_tests']}")
print(f"Passed: {results['passed']} ✅")
print(f"Failed: {results['failed']} ❌")

if results["errors"]:
    print("\n⚠️  ERRORS:")
    for error in results["errors"]:
        print(f"- {error['category']}/{error['test']}: {error['error']}")

# Save detailed results
with open("test_new_apis_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\n💾 Detailed results saved to test_new_apis_results.json")

# Print test questions summary
print("\n📝 TEST QUESTIONS & ANSWERS SUMMARY:")
print("="*60)

for category, tests in results["test_questions"].items():
    print(f"\n{category}:")
    for test in tests:
        status = "✅" if test["success"] else "❌"
        print(f"  {status} Q: {test['question']}")
        if test["success"]:
            print(f"     A: {'Data retrieved' if test.get('has_data') else 'No data (may be normal)'}")
        else:
            print(f"     A: Error - {test.get('error', 'Unknown error')}")

print("\n✨ Testing complete!")