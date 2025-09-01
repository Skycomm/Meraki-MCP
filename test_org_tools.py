#!/usr/bin/env python3
"""
Test all Organization read-only tools with system variables
"""

from server.main import app, meraki
import json

# System test values
TEST_ORG_ID = "686470"  # Skycomm
TEST_NETWORK_ID = "L_726205439913500692"  # Reserve St
TEST_DEVICE_SERIAL = "Q2PD-JL52-H3B2"  # Office AP

print("🧪 Testing Organization Read-Only Tools")
print("=" * 80)

# Test organizations
print("\n1️⃣ Testing get_organizations...")
try:
    result = meraki.dashboard.organizations.getOrganizations()
    print(f"✅ Found {len(result)} organizations")
except Exception as e:
    print(f"❌ Error: {e}")

# Test organization details
print("\n2️⃣ Testing getOrganization...")
try:
    result = meraki.dashboard.organizations.getOrganization(TEST_ORG_ID)
    print(f"✅ Organization: {result.get('name', 'Unknown')}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test organization networks
print("\n3️⃣ Testing getOrganizationNetworks...")
try:
    result = meraki.dashboard.organizations.getOrganizationNetworks(TEST_ORG_ID, perPage=50)
    print(f"✅ Found {len(result)} networks")
except Exception as e:
    print(f"❌ Error: {e}")

# Test inventory devices
print("\n4️⃣ Testing getOrganizationInventoryDevices...")
try:
    result = meraki.dashboard.organizations.getOrganizationInventoryDevices(TEST_ORG_ID, perPage=50)
    print(f"✅ Found {len(result)} inventory devices")
except Exception as e:
    print(f"❌ Error: {e}")

# Test device statuses
print("\n5️⃣ Testing getOrganizationDevicesStatuses...")
try:
    result = meraki.dashboard.organizations.getOrganizationDevicesStatuses(TEST_ORG_ID, perPage=50)
    print(f"✅ Found {len(result)} device statuses")
except Exception as e:
    print(f"❌ Error: {e}")

# Test device availabilities  
print("\n6️⃣ Testing getOrganizationDevicesAvailabilities...")
try:
    result = meraki.dashboard.organizations.getOrganizationDevicesAvailabilities(TEST_ORG_ID, perPage=50)
    print(f"✅ Found {len(result)} device availabilities")
except Exception as e:
    print(f"❌ Error: {e}")

# Test overview
print("\n7️⃣ Testing getOrganizationDevicesStatusesOverview...")
try:
    result = meraki.dashboard.organizations.getOrganizationDevicesStatusesOverview(TEST_ORG_ID)
    print(f"✅ Overview: {result.get('summary', {}).get('total', 0)} total devices")
except Exception as e:
    print(f"❌ Error: {e}")

# Test uptime
print("\n8️⃣ Testing getOrganizationDevicesUplinksAddressesByDevice...")
try:
    result = meraki.dashboard.organizations.getOrganizationDevicesUplinksAddressesByDevice(TEST_ORG_ID, perPage=50)
    print(f"✅ Found {len(result)} device uplink addresses")
except Exception as e:
    print(f"❌ Error: {e}")

# Test onboarding
print("\n9️⃣ Testing getOrganizationInventoryOnboardingCloudMonitoringNetworks...")
try:
    result = meraki.dashboard.organizations.getOrganizationInventoryOnboardingCloudMonitoringNetworks(
        TEST_ORG_ID, 
        perPage=50
    )
    print(f"✅ Found {len(result)} onboarding networks")
except Exception as e:
    print(f"❌ Error: {e}")

# Test early access
print("\n🔟 Testing getOrganizationEarlyAccessFeatures...")
try:
    result = meraki.dashboard.organizations.getOrganizationEarlyAccessFeatures(TEST_ORG_ID)
    print(f"✅ Found {len(result)} early access features")
except Exception as e:
    print(f"❌ Error: {e}")

# Test opt-ins
print("\n1️⃣1️⃣ Testing getOrganizationEarlyAccessFeaturesOptIns...")
try:
    result = meraki.dashboard.organizations.getOrganizationEarlyAccessFeaturesOptIns(TEST_ORG_ID)
    print(f"✅ Found {len(result)} early access opt-ins")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("✅ Organization read-only tools testing complete!")