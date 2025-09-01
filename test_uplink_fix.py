#!/usr/bin/env python3
"""Test the get_organization_appliance_uplink_statuses fix"""

import os
os.environ['MERAKI_API_KEY'] = '1ac5962056ad56da8cea908864f136adc5878a43'

from server.main import app, meraki

def test_uplink_statuses():
    print("Testing get_organization_appliance_uplink_statuses fix...")
    
    # Test with Kids ENT organization ID
    org_id = "669347494617941203"
    
    try:
        # Call the SDK method directly as the MCP tool would
        uplink_statuses = meraki.dashboard.appliance.getOrganizationApplianceUplinkStatuses(org_id)
        
        print(f"✅ Successfully retrieved uplink statuses for organization {org_id}")
        print(f"Found {len(uplink_statuses)} appliances with uplink data")
        
        # Look for Wexford Center network specifically
        for status in uplink_statuses:
            if 'Wexford' in status.get('networkName', ''):
                print(f"\n📍 Found Wexford Center network uplinks:")
                for uplink in status.get('uplinks', []):
                    interface = uplink.get('interface', 'Unknown')
                    state = uplink.get('status', 'unknown')
                    ip = uplink.get('ip', 'N/A')
                    print(f"  - {interface}: {state} (IP: {ip})")
                    
                    # Show WAN 2 specifically
                    if 'wan2' in interface.lower():
                        print(f"\n  🔍 WAN 2 Details:")
                        print(f"    Status: {uplink.get('status')}")
                        print(f"    IP: {uplink.get('ip')}")
                        print(f"    Gateway: {uplink.get('gateway')}")
                        print(f"    DNS: {uplink.get('dns')}")
                        print(f"    VLAN: {uplink.get('vlan', 'None')}")
                break
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_uplink_statuses()
