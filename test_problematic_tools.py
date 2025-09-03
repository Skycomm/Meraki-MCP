#!/usr/bin/env python3
"""
Test the problematic tools mentioned in the transcript to understand root causes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.main import app, meraki
from meraki_client import MerakiClient

# Initialize the client
meraki_client = MerakiClient()

def test_port_forwarding_tools():
    """Test both port forwarding tools to see which one is failing."""
    network_id = 'L_726205439913500692'  # Reserve St network
    
    print("🔍 TESTING PORT FORWARDING TOOLS")
    print("=" * 60)
    
    # Test Tool 1: get_network_appliance_port_forwarding_rules
    print("\n### Test 1: get_network_appliance_port_forwarding_rules")
    try:
        result1 = meraki.dashboard.appliance.getNetworkAppliancePortForwardingRules(network_id)
        print(f"✅ Tool 1 SUCCESS: {type(result1)} - {len(str(result1))} characters")
        if isinstance(result1, dict) and 'rules' in result1:
            print(f"   Rules found: {len(result1['rules'])}")
        else:
            print(f"   Result structure: {result1}")
    except Exception as e:
        print(f"❌ Tool 1 ERROR: {str(e)}")
    
    # Test Tool 2: get_network_appliance_firewall_port_forwarding_rules  
    print("\n### Test 2: get_network_appliance_firewall_port_forwarding_rules")
    try:
        result2 = meraki.get_network_appliance_firewall_port_forwarding_rules(network_id)
        print(f"✅ Tool 2 SUCCESS: {type(result2)} - {len(str(result2))} characters")
        print(f"   First 200 chars: {str(result2)[:200]}")
    except Exception as e:
        print(f"❌ Tool 2 ERROR: {str(e)}")


def test_uplinks_tool():
    """Test the uplinks loss and latency tool."""
    org_id = '686470'  # Skycomm org
    
    print("\n\n🔍 TESTING UPLINKS LOSS AND LATENCY TOOL (AFTER FIX)")
    print("=" * 60)
    
    try:
        # Test the fixed method directly
        result = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(org_id, timespan=300)
        print(f"✅ SUCCESS: {type(result)} - {len(str(result))} characters")
        print(f"   First 300 chars: {str(result)[:300]}")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        
        # Try with different parameters
        print("\n### Trying with different timespan...")
        try:
            result2 = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(org_id, timespan=60)
            print(f"✅ SUCCESS with timespan=60: {type(result2)}")
            print(f"   First 200 chars: {str(result2)[:200]}")
        except Exception as e2:
            print(f"❌ Still ERROR: {str(e2)}")


def test_group_policies_fixed():
    """Test the group policies tool we just fixed."""
    network_id = 'L_726205439913500692'
    
    print("\n\n🔍 TESTING GROUP POLICIES TOOL (AFTER FIX)")
    print("=" * 60)
    
    try:
        result = meraki.dashboard.networks.getNetworkGroupPolicies(network_id)
        print(f"✅ SUCCESS: {type(result)} - {len(str(result))} characters")
        if isinstance(result, list):
            print(f"   Group policies found: {len(result)}")
            for i, policy in enumerate(result[:3]):
                print(f"   {i+1}. {policy.get('name', 'Unnamed')}")
        else:
            print(f"   Result: {result}")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


if __name__ == "__main__":
    test_port_forwarding_tools()
    test_uplinks_tool()  
    test_group_policies_fixed()
    
    print("\n" + "=" * 60)
    print("🎯 TESTING COMPLETE")
    print("=" * 60)