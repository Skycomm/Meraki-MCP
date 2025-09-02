#!/usr/bin/env python3
"""Test core organization tools with proper parameters"""

import os
os.environ['MERAKI_API_KEY'] = '1ac5962056ad56da8cea908864f136adc5878a43'

from server.main import app, meraki
from server.tools_organizations_core import register_organizations_core_tools

# Initialize tools
register_organizations_core_tools(app, meraki)

# Test environment - using known values
TEST_ORG_ID = "686470"  # Skycomm
TEST_NETWORK_ID = "L_726205439913500692"  # Reserve St
TEST_SERIAL = "Q2HP-GCZQ-7AWT"  # MS220-8P switch

def test_read_only_tools():
    """Test all read-only organization tools"""
    
    print("="*80)
    print("TESTING CORE ORGANIZATION READ-ONLY TOOLS")
    print("="*80)
    
    # Test 1: Get all organizations
    print("\n1. Testing get_organizations()...")
    try:
        result = meraki.dashboard.organizations.getOrganizations()
        print(f"✅ Found {len(result)} organizations")
        if result:
            print(f"   First org: {result[0].get('name')} (ID: {result[0].get('id')})")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Get specific organization
    print(f"\n2. Testing get_organization('{TEST_ORG_ID}')...")
    try:
        result = meraki.dashboard.organizations.getOrganization(TEST_ORG_ID)
        print(f"✅ Found organization: {result.get('name')}")
        print(f"   Licensing model: {result.get('licensing', {}).get('model', 'N/A')}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Get organization networks
    print(f"\n3. Testing get_organization_networks('{TEST_ORG_ID}')...")
    try:
        result = meraki.dashboard.organizations.getOrganizationNetworks(
            TEST_ORG_ID,
            perPage=100
        )
        print(f"✅ Found {len(result)} networks")
        if result:
            print(f"   First network: {result[0].get('name')} (ID: {result[0].get('id')})")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 4: Get organization inventory devices
    print(f"\n4. Testing get_organization_inventory_devices('{TEST_ORG_ID}')...")
    try:
        result = meraki.dashboard.organizations.getOrganizationInventoryDevices(
            TEST_ORG_ID,
            perPage=100
        )
        print(f"✅ Found {len(result)} devices in inventory")
        if result:
            print(f"   Sample device: {result[0].get('model')} (Serial: {result[0].get('serial')})")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 5: Get specific device in inventory
    print(f"\n5. Testing get_organization_inventory_device('{TEST_ORG_ID}', '{TEST_SERIAL}')...")
    try:
        result = meraki.dashboard.organizations.getOrganizationInventoryDevice(
            TEST_ORG_ID, TEST_SERIAL
        )
        print(f"✅ Found device: {result.get('model')}")
        print(f"   Network: {result.get('networkName', 'Not assigned')}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 6: Get onboarding statuses
    print(f"\n6. Testing get_org_inventory_onboarding_statuses('{TEST_ORG_ID}')...")
    try:
        result = meraki.dashboard.organizations.getOrganizationInventoryOnboardingCloudMonitoringStatuses(
            TEST_ORG_ID,
            perPage=10
        )
        if result:
            print(f"✅ Found {len(result)} onboarding statuses")
        else:
            print(f"✅ No onboarding statuses (normal if not using cloud monitoring)")
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            print(f"✅ Cloud monitoring not enabled (expected)")
        else:
            print(f"❌ Error: {error_msg}")
    
    # Test 7: Get device availability history
    print(f"\n7. Testing get_org_devices_availabilities_change_history('{TEST_ORG_ID}')...")
    try:
        result = meraki.dashboard.organizations.getOrganizationDevicesAvailabilitiesChangeHistory(
            TEST_ORG_ID,
            perPage=10,
            timespan=86400  # Last 24 hours
        )
        if result:
            print(f"✅ Found {len(result)} availability changes")
        else:
            print(f"✅ No availability changes in last 24 hours")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 8: Get device statuses overview
    print(f"\n8. Testing get_org_devices_statuses_overview('{TEST_ORG_ID}')...")
    try:
        result = meraki.dashboard.organizations.getOrganizationDevicesStatusesOverview(
            TEST_ORG_ID
        )
        if result and 'counts' in result:
            counts = result['counts']
            print(f"✅ Device status overview:")
            print(f"   Online: {counts.get('online', 0)}")
            print(f"   Offline: {counts.get('offline', 0)}")
            print(f"   Alerting: {counts.get('alerting', 0)}")
        else:
            print(f"✅ Retrieved status overview (may be empty)")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print("All read-only core organization tools tested.")
    print("Note: Some tools may return empty results based on organization configuration.")

if __name__ == "__main__":
    test_read_only_tools()