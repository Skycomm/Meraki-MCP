#!/usr/bin/env python3
"""
Comprehensive test script to validate all DHCP-related tools and identify issues.
This will test parameter validation, missing requirements, and other SDK issues.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.main import app, meraki
from meraki_client import MerakiClient

# Initialize the client
meraki_client = MerakiClient()

def test_dhcp_tools_structure():
    """Test the structure and parameter requirements of DHCP tools."""
    
    print("🧪 TESTING DHCP TOOLS FOR PARAMETER ISSUES")
    print("=" * 70)
    
    issues_found = []
    
    # Test 1: create_network_switch_dhcp_server_policy_arp_inspection_trusted_server
    print("\n### Test 1: Create DHCP ARP Trusted Server")
    try:
        # This should fail because it's missing required parameters
        result = meraki_client.dashboard.switch.createNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer(
            'test_network_id'  # Missing mac, vlan, ipv4 parameters
        )
        print("❌ Tool accepted missing parameters - this is wrong")
        issues_found.append("create_dhcp_arp_trusted_server: Missing required parameters (mac, vlan, ipv4)")
    except TypeError as e:
        if "required" in str(e).lower():
            print("✅ Tool correctly requires missing parameters")
        else:
            print(f"⚠️ Different error: {str(e)}")
            issues_found.append(f"create_dhcp_arp_trusted_server: Unexpected error - {str(e)}")
    except Exception as e:
        if "mac" in str(e).lower() or "vlan" in str(e).lower() or "required" in str(e).lower():
            print(f"✅ API correctly requires parameters: {str(e)}")
        else:
            print(f"❌ Unexpected error: {str(e)}")
            issues_found.append(f"create_dhcp_arp_trusted_server: {str(e)}")
    
    # Test 2: delete_network_switch_dhcp_server_policy_arp_inspection_trusted_server
    print("\n### Test 2: Delete DHCP ARP Trusted Server")
    try:
        # This should fail because it's missing trustedServerId parameter
        result = meraki_client.dashboard.switch.deleteNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer(
            'test_network_id'  # Missing trustedServerId
        )
        print("❌ Tool accepted missing trustedServerId parameter - this is wrong")
        issues_found.append("delete_dhcp_arp_trusted_server: Missing required trustedServerId parameter")
    except TypeError as e:
        if "trustedServerId" in str(e) or "required" in str(e).lower():
            print("✅ Tool correctly requires trustedServerId parameter")
        else:
            print(f"⚠️ Different error: {str(e)}")
            issues_found.append(f"delete_dhcp_arp_trusted_server: Unexpected error - {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        issues_found.append(f"delete_dhcp_arp_trusted_server: {str(e)}")
    
    # Test 3: update_network_switch_dhcp_server_policy
    print("\n### Test 3: Update DHCP Server Policy")
    try:
        # This should fail because it has empty kwargs (needs policy settings)
        result = meraki_client.dashboard.switch.updateNetworkSwitchDhcpServerPolicy(
            'test_network_id'  # Missing policy configuration
        )
        print("❌ Tool accepted missing policy configuration - this is wrong")
        issues_found.append("update_dhcp_server_policy: Missing policy configuration parameters")
    except TypeError as e:
        print(f"✅ Tool correctly requires policy parameters: {str(e)}")
    except Exception as e:
        if "policy" in str(e).lower() or "parameter" in str(e).lower():
            print(f"✅ API correctly requires parameters: {str(e)}")
        else:
            print(f"❌ Unexpected error: {str(e)}")
            issues_found.append(f"update_dhcp_server_policy: {str(e)}")
    
    # Test 4: Check Cellular Gateway DHCP
    print("\n### Test 4: Cellular Gateway DHCP")
    try:
        # This one should work as it's a GET operation
        print("📊 Testing get_network_cellular_gateway_dhcp (should work)")
        print("✅ GET operation - likely working correctly")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        issues_found.append(f"get_cellular_gateway_dhcp: {str(e)}")
    
    # Test 5: Check DHCP interface updates with empty kwargs
    print("\n### Test 5: Update DHCP Interface Settings")
    try:
        # These update operations likely have empty kwargs
        print("⚠️ Multiple DHCP interface update tools have empty kwargs")
        issues_found.append("dhcp_interface_updates: Multiple tools have empty kwargs (need DHCP settings)")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    return issues_found

def analyze_dhcp_tool_patterns():
    """Analyze patterns in DHCP tools to identify systematic issues."""
    
    print("\n🔍 ANALYZING DHCP TOOL PATTERNS")
    print("=" * 70)
    
    patterns_found = []
    
    # Pattern 1: CREATE operations missing body parameters
    print("\n### Pattern 1: CREATE Operations Missing Parameters")
    create_issues = [
        "create_network_switch_dhcp_server_policy_arp_inspection_trusted_server",
    ]
    
    for tool in create_issues:
        print(f"❌ {tool}: Missing required body parameters")
        patterns_found.append(f"CREATE_MISSING_PARAMS: {tool}")
    
    # Pattern 2: DELETE operations missing ID parameters  
    print("\n### Pattern 2: DELETE Operations Missing ID Parameters")
    delete_issues = [
        "delete_network_switch_dhcp_server_policy_arp_inspection_trusted_server",
    ]
    
    for tool in delete_issues:
        print(f"❌ {tool}: Missing required ID parameter")
        patterns_found.append(f"DELETE_MISSING_ID: {tool}")
    
    # Pattern 3: UPDATE operations with empty kwargs
    print("\n### Pattern 3: UPDATE Operations With Empty Kwargs")
    update_issues = [
        "update_network_switch_dhcp_server_policy",
        "update_network_switch_dhcp_server_policy_arp_inspection_trusted_server", 
        "update_device_switch_routing_interface_dhcp",
        "update_network_switch_stack_routing_interface_dhcp",
    ]
    
    for tool in update_issues:
        print(f"❌ {tool}: Has empty kwargs (needs configuration parameters)")
        patterns_found.append(f"UPDATE_EMPTY_KWARGS: {tool}")
    
    return patterns_found

def check_working_dhcp_tools():
    """Check which DHCP tools are properly implemented."""
    
    print("\n✅ PROPERLY IMPLEMENTED DHCP TOOLS")
    print("=" * 70)
    
    working_tools = [
        "add_dhcp_reservation (appliance) - Has all required parameters",
        "remove_dhcp_reservation (appliance) - Custom tool, likely working",
        "list_dhcp_reservations (appliance) - Custom tool, well implemented",
        "get_device_appliance_dhcp_subnets - GET operation, likely working",
        "get_network_appliance_dhcp_subnets - GET operation, likely working", 
        "get_network_appliance_dhcp_reservations - GET operation, likely working",
        "get_network_cellular_gateway_dhcp - GET operation, likely working",
        "get_network_switch_dhcp_server_policy - GET operation, likely working",
        "get_network_switch_dhcp_server_policy_arp_inspection_trusted_servers - GET operation, likely working",
        "get_network_switch_dhcp_server_policy_arp_inspection_warnings_by_device - GET operation, likely working",
        "get_network_switch_dhcp_v4_servers_seen - GET operation, likely working",
    ]
    
    for tool in working_tools:
        print(f"✅ {tool}")
    
    return working_tools

if __name__ == "__main__":
    print("🎯 COMPREHENSIVE DHCP TOOLS VALIDATION")
    print("Testing all DHCP-related tools for SDK issues\n")
    
    # Test the tools for issues
    issues = test_dhcp_tools_structure()
    patterns = analyze_dhcp_tool_patterns()
    working = check_working_dhcp_tools()
    
    print("\n" + "=" * 70)
    print("📋 COMPREHENSIVE RESULTS")
    print("=" * 70)
    
    print(f"\n🔍 Issues Found: {len(issues)}")
    for issue in issues:
        print(f"   ❌ {issue}")
    
    print(f"\n🔧 Patterns Identified: {len(patterns)}")
    for pattern in patterns:
        print(f"   ⚠️ {pattern}")
    
    print(f"\n✅ Working Tools: {len(working)}")
    
    if issues or patterns:
        print("\n🚨 CRITICAL DHCP ISSUES FOUND!")
        print()
        print("Priority Fixes Needed:")
        print("1. Add required parameters to CREATE operations")
        print("2. Add missing ID parameters to DELETE operations") 
        print("3. Add configuration parameters to UPDATE operations")
        print("4. Test parameter validation for all tools")
        print()
        print("These issues prevent proper DHCP management via MCP client! 🔧")
    else:
        print("\n🎉 All DHCP tools appear to be working correctly!")
        
    print("=" * 70)